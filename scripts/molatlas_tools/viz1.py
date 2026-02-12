from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from .data import load_percentile_dataframe


def _calc_percentile_lookup(value: float, percentile_values: np.ndarray) -> float:
    """Interpolate percentile for a given value using a precomputed percentile vector.

    The percentile vector should be monotonic and represents cutpoints from low to high.
    We map value -> percentile in [0, 100].
    """
    percentiles = np.linspace(0.0, 100.0, len(percentile_values))
    return float(np.interp(value, percentile_values, percentiles))


def compute_property_percentiles(
    data_df: pd.DataFrame,
    properties: List[str],
    values: Dict[str, float],
) -> Dict[str, float]:
    """Return per-property percentiles for the given molecule values.

    Returns:
        {property_name: percentile_float}
    """
    out: Dict[str, float] = {}
    for prop in properties:
        if prop not in data_df.columns:
            raise KeyError(f"Property '{prop}' not found in percentile CSV columns.")
        if prop not in values:
            raise KeyError(f"Value for property '{prop}' is missing in config.")

        tmp = np.asarray(data_df[prop].values, dtype=float)
        # tmp[2:] are percentile cutpoints (Colab convention)
        out[prop] = _calc_percentile_lookup(float(values[prop]), tmp[2:])
    return out


def run_viz1(
    *,
    data_dir: Path,
    database: str,
    charge: str,
    properties: List[str],
    values: Dict[str, float],
    visualize: bool = True,
    output_dir: Path = Path("fig"),
    make_radar: bool = True,
    make_violin: bool = True,
) -> Dict[str, float]:
    """Visualization 1: compute per-property percentiles (and optionally save figures).

    Required return:
        dict of per-property percentiles.

    If visualize=False:
        - no figures are generated
        - only the percentiles are returned
    """
    data_df = load_percentile_dataframe(data_dir, database, charge)
    percentiles = compute_property_percentiles(data_df, properties, values)

    if not visualize:
        return percentiles

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Radar chart (optional)
    if make_radar:
        try:
            from pycirclize import Circos  # type: ignore
            import matplotlib.pyplot as plt  # noqa
            import pandas as pd  # noqa

            df = pd.DataFrame(
                data=[
                    [percentiles[p] for p in properties],
                    [50.0] * len(properties),
                ],
                index=["Target mol.", "Median"],
                columns=[
                    f"{p}\n{values[p]}\n({percentiles[p]:.2f}th)"
                    for p in properties
                ],
            )
            circos = Circos.radar_chart(
                df,
                vmax=100,
                marker_size=6,
                grid_interval_ratio=0.2,
                grid_label_formatter=lambda v: f"{v:.0f} th",
                label_kws_handler=lambda _: dict(size=16),
            )
            fig = circos.plotfig()
            _ = circos.ax.legend(bbox_to_anchor=(0.97, 1.15), loc="upper left", fontsize=16)
            radar_path = output_dir / f"radar_DB{database}_charge{charge}.pdf"
            plt.savefig(radar_path, transparent=True, dpi=300)
            plt.close(fig)
        except Exception:
            pass

    # 1D distribution plots (optional)
    if make_violin:
        try:
            import matplotlib.pyplot as plt  # noqa

            fig, axs = plt.subplots(nrows=1, ncols=len(properties), figsize=(max(4, len(properties) * 2), 5))
            if len(properties) == 1:
                axs = [axs]

            for i, prop in enumerate(properties):
                tmp = np.asarray(data_df[prop].values, dtype=float)
                # Use percentile cutpoints as a compact representation
                cutpoints = tmp[2:]
                axs[i].violinplot(cutpoints, showmeans=False, showmedians=True)
                axs[i].set_xticks([1], labels=[prop], fontsize=12)
                axs[i].scatter([1], [values[prop]], s=40, marker="o", c="black")
                axs[i].set_title(f"{values[prop]} ({percentiles[prop]:.2f}th)", fontsize=12)

            plt.tight_layout()
            vpath = output_dir / f"1D_dist_DB{database}_charge{charge}.pdf"
            plt.savefig(vpath, transparent=True, dpi=300)
            plt.close(fig)
        except Exception:
            pass

    return percentiles
