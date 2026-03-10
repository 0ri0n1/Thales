"""
Thon Memory Runtime — The bridge from specification to persistent intelligence.

Implements the three-layer memory architecture defined in thon_memory.yaml
and the shared_memory.yaml schema. SQLite-backed, single-writer, unified store.

Usage:
    from memory import ThonMemory
    mem = ThonMemory("engagement_id")
    mem.write("discovery", {...})
    results = mem.query("discovery", filters={...})
    mem.promote("discovery", entry_id)
    mem.close()
"""

import sqlite3
import uuid
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent / "data"
COMMITTED_DB = DATA_DIR / "committed_knowledge.db"

CONFIDENCE_TIERS = {
    "directive": (0.95, 1.0),
    "confirmed": (0.75, 0.94),
    "observed":  (0.45, 0.74),
    "inferred":  (0.15, 0.44),
    "deprecated": (0.0, 0.14),
}

MEMORY_TYPES = [
    "architecture", "targets", "threat_intelligence",
    "engagements", "incidents", "failures", "discoveries",
    "attack_chains", "detection_rules", "response_playbooks",
    "exploit_techniques", "hardening_measures", "decision_memory",
]


def _tier_for_confidence(confidence: float) -> str:
    for tier, (lo, hi) in CONFIDENCE_TIERS.items():
        if lo <= confidence <= hi:
            return tier
    return "deprecated"


class ThonMemory:
    """
    Unified memory runtime for Thon.

    Two databases:
      - engagement DB: cached_recall for the current engagement
      - committed DB:  committed_knowledge persisting across all engagements
    """

    def __init__(self, engagement_id: str, data_dir: Optional[Path] = None):
        self.engagement_id = engagement_id
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

        engagement_db = self.data_dir / f"engagement_{engagement_id}.db"
        committed_db = self.data_dir / "committed_knowledge.db"
        self._engagement_conn = sqlite3.connect(str(engagement_db))
        self._engagement_conn.row_factory = sqlite3.Row
        self._committed_conn = sqlite3.connect(str(committed_db))
        self._committed_conn.row_factory = sqlite3.Row

        self._init_schema(self._engagement_conn)
        self._init_schema(self._committed_conn)

    def _init_schema(self, conn: sqlite3.Connection):
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                entry_id       TEXT PRIMARY KEY,
                memory_type    TEXT NOT NULL,
                layer          TEXT NOT NULL DEFAULT 'cached',
                data           TEXT NOT NULL,
                confidence     REAL NOT NULL DEFAULT 0.5,
                confidence_tier TEXT NOT NULL DEFAULT 'observed',
                lens_source    TEXT DEFAULT NULL,
                engagement_id  TEXT DEFAULT NULL,
                created_at     TEXT NOT NULL,
                updated_at     TEXT NOT NULL,
                last_accessed  TEXT NOT NULL,
                access_count   INTEGER NOT NULL DEFAULT 0,
                decay_exempt   INTEGER NOT NULL DEFAULT 0,
                superseded_by  TEXT DEFAULT NULL,
                tags           TEXT DEFAULT '[]'
            );

            CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type);
            CREATE INDEX IF NOT EXISTS idx_layer ON memories(layer);
            CREATE INDEX IF NOT EXISTS idx_confidence ON memories(confidence);
            CREATE INDEX IF NOT EXISTS idx_lens_source ON memories(lens_source);

            CREATE TABLE IF NOT EXISTS audit_log (
                log_id     TEXT PRIMARY KEY,
                action     TEXT NOT NULL,
                entry_id   TEXT,
                details    TEXT,
                timestamp  TEXT NOT NULL
            );
        """)
        conn.commit()

    def _log_audit(self, conn: sqlite3.Connection, action: str,
                   entry_id: str = None, details: str = None):
        conn.execute(
            "INSERT INTO audit_log (log_id, action, entry_id, details, timestamp) "
            "VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), action, entry_id, details, _now())
        )

    # ── WRITE ────────────────────────────────────────────────────────────

    def write(self, memory_type: str, data: dict,
              confidence: float = 0.5, lens_source: str = None,
              tags: list = None, decay_exempt: bool = False,
              layer: str = "cached") -> str:
        """
        Store a new memory. Returns the entry_id.

        Per doctrine: check for duplicates/contradictions before writing.
        """
        if memory_type not in MEMORY_TYPES:
            raise ValueError(f"Unknown memory_type: {memory_type}. Valid: {MEMORY_TYPES}")

        conn = self._committed_conn if layer == "committed" else self._engagement_conn
        entry_id = str(uuid.uuid4())
        now = _now()

        existing = self._find_duplicate(conn, memory_type, data)
        if existing:
            return self.reinforce(existing["entry_id"], confidence_boost=0.05,
                                  layer=layer)

        conn.execute(
            "INSERT INTO memories "
            "(entry_id, memory_type, layer, data, confidence, confidence_tier, "
            " lens_source, engagement_id, created_at, updated_at, last_accessed, "
            " decay_exempt, tags) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (entry_id, memory_type, layer, json.dumps(data), confidence,
             _tier_for_confidence(confidence), lens_source,
             self.engagement_id, now, now, now,
             1 if decay_exempt else 0, json.dumps(tags or []))
        )
        self._log_audit(conn, "write", entry_id,
                        f"type={memory_type} confidence={confidence} lens={lens_source}")
        conn.commit()
        return entry_id

    def _find_duplicate(self, conn: sqlite3.Connection,
                        memory_type: str, data: dict) -> Optional[dict]:
        """Check if substantially similar memory already exists."""
        data_str = json.dumps(data, sort_keys=True)
        row = conn.execute(
            "SELECT * FROM memories WHERE memory_type = ? AND data = ? "
            "AND superseded_by IS NULL LIMIT 1",
            (memory_type, data_str)
        ).fetchone()
        return dict(row) if row else None

    # ── READ / QUERY ─────────────────────────────────────────────────────

    def query(self, memory_type: str = None, layer: str = None,
              min_confidence: float = 0.0, lens_source: str = None,
              tags: list = None, limit: int = 50,
              search_committed: bool = True) -> list:
        """
        Query memories across engagement and optionally committed stores.

        Returns list of dicts sorted by confidence DESC, updated_at DESC.
        """
        results = []
        conns = [self._engagement_conn]
        if search_committed:
            conns.append(self._committed_conn)

        for conn in conns:
            where, params = ["superseded_by IS NULL"], []
            if memory_type:
                where.append("memory_type = ?"); params.append(memory_type)
            if layer:
                where.append("layer = ?"); params.append(layer)
            if min_confidence > 0:
                where.append("confidence >= ?"); params.append(min_confidence)
            if lens_source:
                where.append("lens_source = ?"); params.append(lens_source)

            sql = (
                f"SELECT * FROM memories WHERE {' AND '.join(where)} "
                f"ORDER BY confidence DESC, updated_at DESC LIMIT ?"
            )
            params.append(limit)
            rows = conn.execute(sql, params).fetchall()

            for row in rows:
                entry = dict(row)
                entry["data"] = json.loads(entry["data"])
                entry["tags"] = json.loads(entry["tags"])
                if tags and not set(tags).intersection(set(entry["tags"])):
                    continue
                conn.execute(
                    "UPDATE memories SET last_accessed = ?, access_count = access_count + 1 "
                    "WHERE entry_id = ?", (_now(), entry["entry_id"])
                )
                results.append(entry)
            conn.commit()

        results.sort(key=lambda x: (-x["confidence"], x["updated_at"]))
        return results[:limit]

    def get(self, entry_id: str) -> Optional[dict]:
        """Retrieve a single memory by ID from either store."""
        for conn in [self._engagement_conn, self._committed_conn]:
            row = conn.execute(
                "SELECT * FROM memories WHERE entry_id = ?", (entry_id,)
            ).fetchone()
            if row:
                entry = dict(row)
                entry["data"] = json.loads(entry["data"])
                entry["tags"] = json.loads(entry["tags"])
                conn.execute(
                    "UPDATE memories SET last_accessed = ?, access_count = access_count + 1 "
                    "WHERE entry_id = ?", (_now(), entry_id)
                )
                conn.commit()
                return entry
        return None

    # ── REINFORCE ────────────────────────────────────────────────────────

    def reinforce(self, entry_id: str, confidence_boost: float = 0.05,
                  layer: str = "cached") -> str:
        """
        Strengthen existing memory. Resets decay timer.
        Per doctrine: each reinforcement adds 0.05 confidence (max 1.0).
        """
        conn = self._committed_conn if layer == "committed" else self._engagement_conn
        row = conn.execute(
            "SELECT * FROM memories WHERE entry_id = ?", (entry_id,)
        ).fetchone()
        if not row:
            conn = self._committed_conn if conn is self._engagement_conn else self._engagement_conn
            row = conn.execute(
                "SELECT * FROM memories WHERE entry_id = ?", (entry_id,)
            ).fetchone()
        if not row:
            raise ValueError(f"Memory {entry_id} not found")

        new_conf = min(1.0, row["confidence"] + confidence_boost)
        now = _now()
        conn.execute(
            "UPDATE memories SET confidence = ?, confidence_tier = ?, "
            "updated_at = ?, last_accessed = ?, access_count = access_count + 1 "
            "WHERE entry_id = ?",
            (new_conf, _tier_for_confidence(new_conf), now, now, entry_id)
        )
        self._log_audit(conn, "reinforce", entry_id,
                        f"boost={confidence_boost} new_confidence={new_conf}")
        conn.commit()
        return entry_id

    # ── PROMOTE ──────────────────────────────────────────────────────────

    def promote(self, entry_id: str) -> str:
        """
        Promote memory from cached_recall (engagement DB) to committed_knowledge.
        Per doctrine: promotion adds 0.1 to confidence.
        """
        row = self._engagement_conn.execute(
            "SELECT * FROM memories WHERE entry_id = ?", (entry_id,)
        ).fetchone()
        if not row:
            raise ValueError(f"Memory {entry_id} not found in engagement store")

        new_conf = min(1.0, row["confidence"] + 0.1)
        now = _now()
        self._committed_conn.execute(
            "INSERT OR REPLACE INTO memories "
            "(entry_id, memory_type, layer, data, confidence, confidence_tier, "
            " lens_source, engagement_id, created_at, updated_at, last_accessed, "
            " access_count, decay_exempt, tags) "
            "VALUES (?, ?, 'committed', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (row["entry_id"], row["memory_type"], row["data"],
             new_conf, _tier_for_confidence(new_conf),
             row["lens_source"], row["engagement_id"],
             row["created_at"], now, now,
             row["access_count"], row["decay_exempt"], row["tags"])
        )
        self._engagement_conn.execute(
            "UPDATE memories SET layer = 'promoted' WHERE entry_id = ?", (entry_id,)
        )
        self._log_audit(self._committed_conn, "promote", entry_id,
                        f"from_engagement={self.engagement_id} new_confidence={new_conf}")
        self._committed_conn.commit()
        self._engagement_conn.commit()
        return entry_id

    # ── CONTRADICT ───────────────────────────────────────────────────────

    def contradict(self, old_entry_id: str, new_data: dict,
                   new_confidence: float = 0.5,
                   reason: str = "", lens_source: str = None) -> str:
        """
        Record contradicting evidence. Per doctrine: both are preserved.
        Old memory is marked superseded. New memory is linked.
        """
        new_id = self.write(
            memory_type=self.get(old_entry_id)["memory_type"],
            data=new_data, confidence=new_confidence,
            lens_source=lens_source,
            tags=["contradiction", f"supersedes:{old_entry_id}"]
        )
        for conn in [self._engagement_conn, self._committed_conn]:
            conn.execute(
                "UPDATE memories SET superseded_by = ? WHERE entry_id = ?",
                (new_id, old_entry_id)
            )
            self._log_audit(conn, "contradict", old_entry_id,
                            f"superseded_by={new_id} reason={reason}")
            conn.commit()
        return new_id

    # ── DECAY / PRUNE ────────────────────────────────────────────────────

    def apply_decay(self, days_inactive_threshold: int = 30,
                    confidence_penalty: float = 0.05):
        """
        Apply confidence decay to memories not accessed within threshold.
        Per doctrine: confidence erodes 0.1/quarter for committed,
        faster for cached. Never auto-deletes committed — archives instead.
        """
        cutoff = (datetime.utcnow() - timedelta(days=days_inactive_threshold)).isoformat()

        for conn, store_name in [(self._engagement_conn, "cached"),
                                 (self._committed_conn, "committed")]:
            rows = conn.execute(
                "SELECT entry_id, confidence FROM memories "
                "WHERE last_accessed < ? AND decay_exempt = 0 "
                "AND superseded_by IS NULL",
                (cutoff,)
            ).fetchall()

            for row in rows:
                new_conf = max(0.0, row["confidence"] - confidence_penalty)
                tier = _tier_for_confidence(new_conf)
                if store_name == "committed" and new_conf < 0.1:
                    conn.execute(
                        "UPDATE memories SET layer = 'archived', confidence = ?, "
                        "confidence_tier = 'deprecated', updated_at = ? WHERE entry_id = ?",
                        (new_conf, _now(), row["entry_id"])
                    )
                    self._log_audit(conn, "archive", row["entry_id"],
                                    f"confidence_decayed_to={new_conf}")
                else:
                    conn.execute(
                        "UPDATE memories SET confidence = ?, confidence_tier = ?, "
                        "updated_at = ? WHERE entry_id = ?",
                        (new_conf, tier, _now(), row["entry_id"])
                    )
            conn.commit()

    # ── PATTERN DETECTION ────────────────────────────────────────────────

    def detect_patterns(self, min_occurrences: int = 3) -> list:
        """
        Scan for recurring patterns across memories.
        Per doctrine: 3+ independent observations → candidate pattern.
        """
        rows = self._committed_conn.execute(
            "SELECT memory_type, data, COUNT(*) as occurrences "
            "FROM memories WHERE superseded_by IS NULL AND layer = 'committed' "
            "GROUP BY memory_type, data HAVING COUNT(*) >= ?",
            (min_occurrences,)
        ).fetchall()

        patterns = []
        for row in rows:
            patterns.append({
                "memory_type": row["memory_type"],
                "data": json.loads(row["data"]),
                "occurrences": row["occurrences"],
                "pattern_candidate": True,
            })
        return patterns

    # ── ENGAGEMENT CLOSEOUT ──────────────────────────────────────────────

    def closeout(self, auto_promote_threshold: float = 0.75) -> dict:
        """
        Post-engagement review. Promotes high-confidence memories.
        Returns closeout summary.
        """
        rows = self._engagement_conn.execute(
            "SELECT * FROM memories WHERE confidence >= ? "
            "AND layer = 'cached' AND superseded_by IS NULL",
            (auto_promote_threshold,)
        ).fetchall()

        promoted = []
        for row in rows:
            self.promote(row["entry_id"])
            promoted.append(row["entry_id"])

        stats = self._engagement_conn.execute(
            "SELECT memory_type, COUNT(*) as count, AVG(confidence) as avg_confidence "
            "FROM memories GROUP BY memory_type"
        ).fetchall()

        summary = {
            "engagement_id": self.engagement_id,
            "closed_at": _now(),
            "total_memories": sum(r["count"] for r in stats),
            "promoted_to_committed": len(promoted),
            "promoted_ids": promoted,
            "by_type": {r["memory_type"]: {"count": r["count"],
                        "avg_confidence": round(r["avg_confidence"], 3)}
                        for r in stats},
        }

        self.write("decision_memory", {
            "decision_type": "engagement_closeout",
            "decision": f"Closed engagement {self.engagement_id}",
            "rationale": f"Promoted {len(promoted)} memories above {auto_promote_threshold} confidence",
            "summary": summary,
        }, confidence=0.9, decay_exempt=True, layer="committed")

        return summary

    # ── STATS ────────────────────────────────────────────────────────────

    def stats(self) -> dict:
        """Return memory statistics for both stores."""
        result = {}
        for name, conn in [("engagement", self._engagement_conn),
                           ("committed", self._committed_conn)]:
            rows = conn.execute(
                "SELECT layer, memory_type, COUNT(*) as count, "
                "AVG(confidence) as avg_conf, MIN(confidence) as min_conf, "
                "MAX(confidence) as max_conf "
                "FROM memories WHERE superseded_by IS NULL "
                "GROUP BY layer, memory_type"
            ).fetchall()
            result[name] = [dict(r) for r in rows]
        return result

    # ── LIFECYCLE ────────────────────────────────────────────────────────

    def close(self):
        self._engagement_conn.close()
        self._committed_conn.close()


def _now() -> str:
    return datetime.utcnow().isoformat()
