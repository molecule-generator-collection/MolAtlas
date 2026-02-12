from __future__ import annotations

from pathlib import Path
from typing import Any, Tuple

import numpy as np
from scipy.interpolate import griddata  # type: ignore

from .data import load_kde_dict, kde_key


def compute_density_percentile(
    *,
    kde_info: Any,
    x: float,
    y: float,
) -> Tuple[float, float]:
    """Compute KDE density and percentile-of-density for a point (x,y).

    Returns:
        (density, percentile_of_density)

    Percentile-of-density is computed as the cumulative density mass up to the interpolated
    density value (Colab-compatible behavior).
    """
    X_info, Y_info, Z, scaler_x, scaler_y, contour_levels, percentile_levels = kde_info

    # Scale the data
    Xs, Ys = np.meshgrid(
        np.linspace(X_info[0], X_info[1], int(X_info[2])),
        np.linspace(Y_info[0], Y_info[1], int(Y_info[2])),
    )

    scaled_x = float(scaler_x.transform([[x]])[0, 0])
    scaled_y = float(scaler_y.transform([[y]])[0, 0])

    # KDE density estimation (interpolation)
    density = griddata(
        points=np.column_stack([Xs.ravel(), Ys.ravel()]),
        values=np.asarray(Z).ravel(),
        xi=np.array([[scaled_x, scaled_y]]),
        method="linear",
    )[0]
    density = float(density)

    # Compute percentiles
    Z_flat = np.asarray(Z).ravel()
    Z_sorted = np.sort(Z_flat)
    cumsum = np.cumsum(Z_sorted) / np.sum(Z_sorted)

    idx = int(np.argmax(Z_sorted >= density))
    percentile = float(cumsum[idx] * 100.0)

    return density, percentile


def run_viz2(
    *,
    data_dir: Path,
    database: str,
    charge: str,
    prop_x: str,
    prop_y: str,
    x: float,
    y: float,
    visualize: bool = True,
    output_dir: Path = Path("fig"),
    show_contours: bool = True,
) -> float:
    """Visualization 2: compute percentile-of-density (and optionally save a plot).

    Required return:
        percentile_of_density (float)

    If visualize=False:
        - no figures are generated
        - only the percentile is returned
    """
    kde_dict = load_kde_dict(data_dir, database, charge)
    key = kde_key(database, charge, prop_x, prop_y)
    if key not in kde_dict:
        raise KeyError(f"KDE key not found: {key}")

    kde_info = kde_dict[key]
    density, percentile = compute_density_percentile(kde_info=kde_info, x=x, y=y)

    if not visualize:
        return percentile

    try:
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors

        try:
            import seaborn as sns
            cmap_original = sns.cubehelix_palette(light=1, as_cmap=True)
        except Exception:
            cmap_original = plt.get_cmap()

        X_info, Y_info, Z, scaler_x, scaler_y, contour_levels, percentile_levels = kde_info
        Xs, Ys = np.meshgrid(
            np.linspace(X_info[0], X_info[1], int(X_info[2])),
            np.linspace(Y_info[0], Y_info[1], int(Y_info[2])),
        )
        X_inv = scaler_x.inverse_transform(Xs)
        Y_inv = scaler_y.inverse_transform(Ys)

        Z_flat = np.asarray(Z).ravel()
        Z_sorted = np.sort(Z_flat)
        cumsum = np.cumsum(Z_sorted) / np.sum(Z_sorted)
 
        # For drawing percentile bands
        percentilef_levels = [0.0001,0.0002,0.0005, 0.001,0.002,0.005, 0.01,0.02,0.05, 0.1, 0.2, 0.5]
        contourf_levels = [Z_sorted[int(np.argmax(cumsum >= p))] for p in percentilef_levels]
        contourf_levels = sorted(contourf_levels)

        levels = [0] + contourf_levels + [float(np.max(Z_flat))]

        # Configure colormap (values below minimum shown as white)
        new_colors = cmap_original(np.linspace(0, 1, len(levels)))
        new_colors[0] = [1, 1, 1, 1]
        custom_cmap = mcolors.ListedColormap(new_colors)
        norm = mcolors.BoundaryNorm(levels, custom_cmap.N)

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_box_aspect(1)
        contourf = ax.contourf(X_inv, Y_inv, Z, levels=levels, cmap=custom_cmap, norm=norm)
        cbar = plt.colorbar(contourf, ax=ax, shrink=0.8)
        cbar.set_label("Estimated density", size=10)
        cbar.set_ticks(levels[1:])
        cbar.set_ticklabels([f"{tick:.1e}" for tick in levels[1:]], fontsize=10)

        if show_contours:
            contour = ax.contour(X_inv, Y_inv, Z, levels=contour_levels, colors=["indigo","darkmagenta","mediumvioletred","white"], linewidths=0.8)
            ax.clabel(contour, fmt={l: f"{p*100:.2f}%" for l, p in zip(contour_levels, percentile_levels)}, fontsize=8)

        ax.scatter([x], [y], s=40, marker="X",
                   label=f"Computed data\n(percentile of density = {percentile:.2f}%)")
        ax.legend(loc="upper right", framealpha=0, fontsize=10)
        ax.set_xlabel(prop_x, fontsize=14)
        ax.set_ylabel(prop_y, fontsize=14)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / f"2D_dist_DB{database}_charge{charge}_p1{prop_x}_p2{prop_y}.pdf"
        plt.savefig(out_path, transparent=True, dpi=300)
        plt.close(fig)
    except Exception:
        pass

    return percentile
