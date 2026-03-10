# Legacy Hat Specifications — Archived

These YAML files are the original hat-based agent definitions from Thon v1.0.
They have been superseded by the unified lens architecture in `agents/thon/lenses.yaml`.

The unique operational content from each hat has been incorporated into the
corresponding lens specification:

| Legacy Hat | Superseded By | Lens Codename |
|------------|---------------|---------------|
| grey_hat   | lenses.discovery | DRIFTER |
| red_team   | lenses.offense | VANGUARD |
| blue_team  | lenses.defense | BASTION |
| black_hat  | lenses.adversary | SHADOW |
| white_hat  | lenses.governance | WARDEN |

The supervisor (ARBITER) now references lenses, not hats. The `agents/hats/`
directory is retained for reference but is no longer loaded at runtime.

**Archived:** 2026-03-09  
**Reason:** Thales evaluation — hat/lens duality resolved in favor of unified entity model.
