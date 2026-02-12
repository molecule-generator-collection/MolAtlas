# MolAtlas

This repository provides **MolAtlas**, a visualization framework for molecular property distributions to guide functional molecule development.

- **[Google Colaboratory version](https://colab.research.google.com/github/molecule-generator-collection/MolAtlas/blob/main/Visualization_via_MolAtlas.ipynb)** is availabile for interactive use. 
- The `scripts/` folder provides a **reproducible, YAML-driven CLI workflow** that separates:
  - **Visualization 1**: 1D property distributions → returns **per-property percentiles**
  - **Visualization 2**: 2D property map (KDE) → returns **percentile of density**

## Reference 

If you use MolAtlas in your research, please cite:

**MolAtlas: a visualization framework for molecular property distributions to guide functional molecule development.**  
ChemRxiv. 27 August 2025.  
DOI: https://doi.org/10.26434/chemrxiv-2025-lm0fz


## Installation

### Requirements
- Python 3.9 or later

### 1. Clone the repository

```bash
git clone https://github.com/molecule-generator-collection/MolAtlas.git
cd MolAtlas
```

### 2. Install dependencies
Install all required packages using:
```bash
pip install -r requirements.txt
```

## Data files

### 1) Percentile tables (CSV; lightweight; included in GitHub)

These CSV files are used by **Visualization 1**:

- `data/DB<DBNAME>_charge<CHARGE>.csv`

Examples:
- `data/DBAll_charge0.csv`
- `data/DBZINC_chargeAll.csv`

### 2) KDE models (pickle; large; hosted on Zenodo)

The KDE models are used by **Visualization 2**:

- `data/kde_info_dict_DB<DBNAME>_charge<CHARGE>.pickle`

Because these files are large, they are hosted externally.

**Download from Zenodo :**
Download the KDE files from Zenodo and place them in the `data/` directory.
```
https://zenodo.org/10.5281/zenodo.18621610
```

## Usage (CLI)

Run from the **repository root**.

All visualization outputs are saved in the `fig/` directory.

### Visualization 1: 1D property distributions

Compute percentiles for each molecular property and generate radar chart visualizations.

**Return value:** per-property percentiles `{property: percentile}`

**Example config**  
`scripts/configs/viz1_example.yaml`

In this YAML file, you provide the molecular properties and their numeric values:

```yaml
# Provide the molecule properties and values (property -> numeric value)
properties: ["MW", "HOMO", "LUMO", "HOMO-LUMO gap", "Abs_wl_1", "Abs_f_1"]
values:
  MW: 300
  HOMO: -6
  LUMO: -2
  HOMO-LUMO gap: 4
  Abs_wl_1: 350
  Abs_f_1: 0.03
```

These values are used to compute percentiles and generate a radar chart saved in fig/.

**Run**
```
python -m scripts.molatlas_tools.cli viz1 --config scripts/configs/viz1_example.yaml --json
```

**Example output (JSON):**
```json
{
  "MW": 62.31,
  "HOMO": 41.02
}
```

### Visualization 2: 2D map defined by two properties (KDE)

Compute the percentile of density for a 2D property pair and generate a KDE map.

**Return value:** percentile of density (float)

Example config: `scripts/configs/viz2_example.yaml`

In this YAML file, you specify the two properties and their values:

```yaml
# 2D property pair and your molecule values
prop_x: MW
prop_y: Abs_wl_1
x: 300
y: 350
```

These values are used to locate the molecule on the KDE map and compute the percentile of density.
The visualization is saved in fig/.

**Run**

```bash
python -m scripts.molatlas_tools.cli viz2 --config scripts/configs/viz2_example.yaml --json
```

**Example output (JSON):**
```json
{
  "percentile_of_density": 12.45
}
```

## Available Properties

The following molecular properties are supported:

```
MW, HOMO, LUMO, HOMO-LUMO gap, VIP, VEA, Dipole, Energy, DEEN, Chrg_var, Spin_sum, Freq, E_free, E_enth, Ei, Et, Ezp, Cv, Si, polar_iso, polar_aniso, IR, Raman, Abs_wl_1, Abs_f_1, CD_mu_1, CD_theta_1, CD_g_1, FL_wl_1, FL_f_1, CPL_mu_1, CPL_theta_1, CPL_g_1, charge
```

These property names must match exactly when specified in the YAML configuration files. 
The details of these properties are described in Table S1 of the Supporting Information.


## Options

Common options in the YAML config:

- **database**: `ZINC` | `PubChem` | `GDB` | `All`  
  Dataset to use.

- **charge**: `"0"` | `"All"`  
  Filter molecules by charge state.

- **output_dir**: e.g. `fig`  
  Directory where figures are saved.

- **visualize**: `true` | `false`  
  - `true` → compute results and save figures  
  - `false` → compute only (no figures)

- **show_contours** (viz2 only): `true` | `false`  
  Show contour lines in the 2D KDE map.


### Output

- Figures are saved in the directory specified by `output_dir` (default: `fig/`).
- viz1 → radar chart  
- viz2 → 2D KDE map  


### `--json` option

Add `--json` to return results in JSON format.

Example:

python -m scripts.molatlas_tools.cli viz1 --config config.yaml --json

Without `--json`:
- Results are printed in a human-readable format.
- Figures are still generated if `visualize: true`.

## SMILES Dataset of MolAtlas
The SMILES lists of prepared molecules for MolAtlas is available in the Zenodo public repository at https://doi.org/10.5281/zenodo.16885261.
