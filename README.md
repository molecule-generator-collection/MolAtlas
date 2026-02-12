# MolAtlas

This repository provides **MolAtlas**, a visualization framework for molecular property distributions to guide functional molecule development.

- **[Google Colaboratory version](https://colab.research.google.com/github/molecule-generator-collection/MolAtlas/blob/main/Visualization_via_MolAtlas.ipynb)** is availabile for interactive use. 
- The `scripts/` folder provides a **reproducible, YAML-driven CLI workflow** that separates:
  - **Visualization 1**: 1D property distributions → returns **per-property percentiles**
  - **Visualization 2**: 2D property map (KDE) → returns **percentile of density**

## Reference (ChemRxiv)

If you use MolAtlas in your research, please cite:

**MolAtlas: a visualization framework for molecular property distributions to guide functional molecule development.**  
ChemRxiv. 27 August 2025.  
DOI: https://doi.org/10.26434/chemrxiv-2025-lm0fz


## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/MolAtlas.git
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
https://zenodo.org/record/xxxxx   
```

## SMILES Dataset of MolAtlas
The SMILES lists of prepared molecules for MolAtlas is available in the Zenodo public repository at https://doi.org/10.5281/zenodo.16885261.
