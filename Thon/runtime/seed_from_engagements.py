"""
Seed committed_knowledge from existing engagement reports.

Parses the markdown engagement files in hak5/*/engagements/ and converts
them into structured memory entries in the committed knowledge store.
"""

import re
import os
import sys
from pathlib import Path
from memory import ThonMemory

THON_ROOT = Path(__file__).parent.parent
ENGAGEMENT_DIRS = [
    THON_ROOT / "hak5" / "wifi-pineapple-mk7" / "engagements",
    THON_ROOT / "hak5" / "lan-turtle" / "engagements",
]


def extract_engagement_metadata(filepath: Path) -> dict:
    """Extract structured data from an engagement markdown file."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    name = filepath.stem

    metadata = {
        "filename": name,
        "source_path": str(filepath.relative_to(THON_ROOT)),
        "device": _infer_device(filepath),
    }

    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", name)
    if date_match:
        metadata["date"] = date_match.group(1)

    target_match = re.search(r"(?:SSID|Target|Network|BSSID)[:\s]*[`*]*([^\n`*]+)", text, re.I)
    if target_match:
        metadata["target"] = target_match.group(1).strip()

    for section in ["Findings", "Results", "Observations", "Summary", "Key Findings"]:
        pattern = rf"#+\s*{section}\s*\n([\s\S]*?)(?=\n#+\s|\Z)"
        match = re.search(pattern, text, re.I)
        if match:
            metadata["findings_raw"] = match.group(1).strip()[:2000]
            break

    for section in ["Recommendations", "Remediation", "Next Steps"]:
        pattern = rf"#+\s*{section}\s*\n([\s\S]*?)(?=\n#+\s|\Z)"
        match = re.search(pattern, text, re.I)
        if match:
            metadata["recommendations_raw"] = match.group(1).strip()[:1000]
            break

    metadata["engagement_type"] = _classify_engagement(name, text)
    metadata["word_count"] = len(text.split())

    return metadata


def _infer_device(filepath: Path) -> str:
    parts = filepath.parts
    for i, part in enumerate(parts):
        if part == "hak5" and i + 1 < len(parts):
            return parts[i + 1]
    return "unknown"


def _classify_engagement(name: str, text: str) -> str:
    name_lower = name.lower()
    text_lower = text.lower()
    if "exploit" in name_lower or "exploit" in text_lower[:500]:
        return "exploitation"
    if "recon" in name_lower:
        return "reconnaissance"
    if "harvest" in name_lower:
        return "collection"
    if "validation" in name_lower or "audit" in name_lower:
        return "validation"
    return "reconnaissance"


def seed():
    mem = ThonMemory("seed_initial", data_dir=Path(__file__).parent / "data")
    seeded = 0

    for eng_dir in ENGAGEMENT_DIRS:
        if not eng_dir.exists():
            continue

        for filepath in sorted(eng_dir.rglob("*.md")):
            metadata = extract_engagement_metadata(filepath)

            mem.write(
                memory_type="engagements",
                data=metadata,
                confidence=0.8,
                lens_source="discovery",
                tags=["seeded", metadata["device"], metadata["engagement_type"]],
                layer="committed",
                decay_exempt=True,
            )
            seeded += 1
            print(f"  [+] {metadata['source_path']}")

            if "findings_raw" in metadata:
                mem.write(
                    memory_type="discoveries",
                    data={
                        "source_engagement": metadata["filename"],
                        "device": metadata["device"],
                        "findings": metadata["findings_raw"],
                        "engagement_type": metadata["engagement_type"],
                    },
                    confidence=0.7,
                    lens_source="discovery",
                    tags=["seeded", "historical"],
                    layer="committed",
                )

    summary = mem.stats()
    mem.close()

    print(f"\nSeeded {seeded} engagement records into committed_knowledge.")
    print(f"Stats: {summary.get('committed', [])}")
    return seeded


if __name__ == "__main__":
    print("Seeding committed_knowledge from existing engagement reports...\n")
    seed()
