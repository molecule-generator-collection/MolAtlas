"""MolAtlas helper scripts (YAML-driven).

This folder is intended to live under `scripts/` in the MolAtlas repository.

Entry points:
  - scripts/molatlas_tools/cli.py : CLI for viz1 and viz2 using YAML configs
  - scripts/molatlas_tools/viz1.py: Visualization 1 (1D) percentile computation (+ optional plots)
  - scripts/molatlas_tools/viz2.py: Visualization 2 (2D) density percentile computation (+ optional plots)

Data directory:
  - The scripts assume data files are located in `./data/` at the repository root.
"""

__all__ = ["config", "data", "viz1", "viz2", "cli"]
