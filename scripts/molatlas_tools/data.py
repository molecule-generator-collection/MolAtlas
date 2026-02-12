from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pandas as pd
import pickle


def _db_prefix(database: str) -> str:
    return f"DB{database}"


def percentile_csv_filename(database: str, charge: str) -> str:
    return f"{_db_prefix(database)}_charge{charge}.csv"


def kde_pickle_filename(database: str, charge: str) -> str:
    return f"kde_info_dict_{_db_prefix(database)}_charge{charge}.pickle"


def load_percentile_dataframe(data_dir: Path, database: str, charge: str) -> pd.DataFrame:
    """Load percentile lookup table (CSV).

    The original Colab notebook skips the second row (index 1). We preserve that behavior.
    """
    path = Path(data_dir) / percentile_csv_filename(database, charge)
    if not path.exists():
        raise FileNotFoundError(f"Percentile CSV not found: {path}")
    return pd.read_csv(path, skiprows=[1])


def load_kde_dict(data_dir: Path, database: str, charge: str) -> Dict[str, Any]:
    """Load KDE dictionary (pickle)."""
    path = Path(data_dir) / kde_pickle_filename(database, charge)
    if not path.exists():
        raise FileNotFoundError(
            f"KDE pickle not found: {path}\n"
            f"Download it from Zenodo (see README) and extract into: {data_dir}"
        )
    with path.open("rb") as f:
        return pickle.load(f)


def kde_key(database: str, charge: str, prop_x: str, prop_y: str) -> str:
    return f"{_db_prefix(database)}_charge{charge}_p1{prop_x}_p2{prop_y}"
