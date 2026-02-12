from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import load_viz1_config, load_viz2_config
from .viz1 import run_viz1
from .viz2 import run_viz2


def _repo_root_from_scripts_dir() -> Path:
    # This file is expected at: <repo>/scripts/molatlas_tools/cli.py
    # So repo root is three levels up.
    return Path(__file__).resolve().parents[2]


def _default_data_dir() -> Path:
    return _repo_root_from_scripts_dir() / "data"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="molatlas",
        description=(
            "MolAtlas CLI (YAML-driven).\n"
            "Assumes data files are located in ./data at the repository root."
        ),
    )
    sub = p.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("viz1", help="Visualization 1: 1D property distribution percentiles (optional plots).")
    p1.add_argument("--config", required=True, help="YAML config file for viz1.")
    p1.add_argument("--json", action="store_true", help="Print return values as JSON.")

    p2 = sub.add_parser("viz2", help="Visualization 2: 2D KDE density percentile (optional plot).")
    p2.add_argument("--config", required=True, help="YAML config file for viz2.")
    p2.add_argument("--json", action="store_true", help="Print return values as JSON.")

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    data_dir = _default_data_dir()

    if args.command == "viz1":
        cfg = load_viz1_config(args.config)
        percentiles = run_viz1(
            data_dir=data_dir,
            database=cfg.database,
            charge=cfg.charge,
            properties=cfg.properties,
            values=cfg.values,
            visualize=cfg.visualize,
            output_dir=_repo_root_from_scripts_dir() / cfg.output_dir,
            make_radar=cfg.make_radar,
            make_violin=cfg.make_violin,
        )
        if args.json:
            print(json.dumps(percentiles, indent=2))
        else:
            print("Visualization 1 (per-property percentiles):")
            for k, v in percentiles.items():
                print(f"  {k}: {v:.2f}th")
        return 0

    if args.command == "viz2":
        cfg = load_viz2_config(args.config)
        percentile = run_viz2(
            data_dir=data_dir,
            database=cfg.database,
            charge=cfg.charge,
            prop_x=cfg.prop_x,
            prop_y=cfg.prop_y,
            x=cfg.x,
            y=cfg.y,
            visualize=cfg.visualize,
            output_dir=_repo_root_from_scripts_dir() / cfg.output_dir,
            show_contours=cfg.show_contours,
        )
        if args.json:
            print(json.dumps({"percentile_of_density": percentile}, indent=2))
        else:
            print(f"Visualization 2 (percentile of density): {percentile:.2f}%")
        return 0

    parser.error("Unknown command.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
