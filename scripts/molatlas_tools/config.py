from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Union

import yaml


@dataclass
class CommonConfig:
    database: str  # "All" | "ZINC" | "PubChem" | "GDB"
    charge: str    # "0" | "All"
    output_dir: Path = Path("fig")
    visualize: bool = True  # if False, do not create/save figures

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CommonConfig":
        return CommonConfig(
            database=str(d.get("database", "All")),
            charge=str(d.get("charge", "0")),
            output_dir=Path(d.get("output_dir", "fig")),
            visualize=bool(d.get("visualize", True)),
        )


@dataclass
class Viz1Config(CommonConfig):
    properties: List[str] = None
    values: Dict[str, float] = None
    make_radar: bool = True
    make_violin: bool = True

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Viz1Config":
        common = CommonConfig.from_dict(d)
        props = d.get("properties", None)
        values = d.get("values", None)

        if props is None and isinstance(values, dict):
            props = list(values.keys())
        if props is None:
            raise ValueError("viz1: 'properties' (list) or 'values' (mapping) is required.")
        if not isinstance(props, list):
            raise TypeError("viz1: 'properties' must be a list of strings.")
        if values is None:
            raise ValueError("viz1: 'values' mapping is required (property -> numeric value).")
        if not isinstance(values, dict):
            raise TypeError("viz1: 'values' must be a mapping {property: value}.")

        return Viz1Config(
            database=common.database,
            charge=common.charge,
            output_dir=common.output_dir,
            visualize=common.visualize,
            properties=[str(p).strip() for p in props],
            values={str(k).strip(): float(v) for k, v in values.items()},
            make_radar=bool(d.get("make_radar", True)),
            make_violin=bool(d.get("make_violin", True)),
        )


@dataclass
class Viz2Config(CommonConfig):
    prop_x: str = ""
    prop_y: str = ""
    x: float = 0.0
    y: float = 0.0
    show_contours: bool = True

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Viz2Config":
        common = CommonConfig.from_dict(d)

        prop_x = d.get("prop_x")
        prop_y = d.get("prop_y")
        x = d.get("x")
        y = d.get("y")

        if prop_x is None and "properties" in d:
            props = d.get("properties")
            if isinstance(props, list) and len(props) == 2:
                prop_x, prop_y = props[0], props[1]
        if (x is None or y is None) and "values" in d:
            vals = d.get("values")
            if isinstance(vals, dict) and prop_x in vals and prop_y in vals:
                x, y = vals[prop_x], vals[prop_y]

        if prop_x is None or prop_y is None:
            raise ValueError("viz2: 'prop_x' and 'prop_y' are required (or 'properties' with 2 items).")
        if x is None or y is None:
            raise ValueError("viz2: 'x' and 'y' are required (or 'values' containing them).")

        return Viz2Config(
            database=common.database,
            charge=common.charge,
            output_dir=common.output_dir,
            visualize=common.visualize,
            prop_x=str(prop_x).strip(),
            prop_y=str(prop_y).strip(),
            x=float(x),
            y=float(y),
            show_contours=bool(d.get("show_contours", True)),
        )


def load_yaml(path: Union[str, Path]) -> Dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_viz1_config(path: Union[str, Path]) -> Viz1Config:
    d = load_yaml(path)
    section = d.get("viz1", d)
    return Viz1Config.from_dict(section)


def load_viz2_config(path: Union[str, Path]) -> Viz2Config:
    d = load_yaml(path)
    section = d.get("viz2", d)
    return Viz2Config.from_dict(section)
