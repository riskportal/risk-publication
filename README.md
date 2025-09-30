# RISK Network Publication

<p align="center">
  <img src="https://i.imgur.com/8TleEJs.png" width="50%" alt="RISK Network logo" />
</p>

<br>

![Python](https://img.shields.io/badge/python-3.8%2B-yellow)
![License](https://img.shields.io/badge/license-GPLv3-purple)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxxx.svg)](https://doi.org/10.5281/zenodo.xxxxxxx)

> [!CAUTION]
> This repository is designed to work with `risk-network==0.0.14`, the version submitted for publication. To ensure compatibility with these notebooks and figures, please run:
>
> ```bash
> pip install risk-network==0.0.14
> ```

This repository provides Jupyter notebooks and datasets necessary to reproduce all figures from the analyses described in:

**Horecka and Röst (2025)**, _"RISK: a next-generation tool for biological network annotation and visualization"_.
<br>
DOI: [10.5281/zenodo.xxxxxxx](https://doi.org/10.5281/zenodo.xxxxxxx)

---

## Documentation

Full documentation (with examples and usage guidance) is available at [https://riskportal.github.io/network-tutorial/](https://riskportal.github.io/network-tutorial/).

## Repository Structure

This repository contains the notebooks and data needed to reproduce figures from the RISK and SAFE analyses. The full RISK source code is available at [riskportal/network](https://github.com/riskportal/network).

### `risk_network/`

Jupyter notebooks and processed datasets for **RISK-based** clustering, annotation, and visualization:

- `fig_1_supp_fig_2_4_5_6.ipynb` – Yeast PPI network analysis, GO BP enrichment, and comparison to SAFE
- `supp_fig_1_3.ipynb` – GI network analysis and side-by-side comparison with SAFE
- `supp_fig_7.ipynb` – RISK analysis of a high-energy physics citation network (non-biological validation)
- `supp_fig_8.ipynb`, `supp_fig_8.py` – Benchmarking execution time and memory usage for RISK (vs SAFE) using synthetic networks

### `safe_network/`

Jupyter notebooks and datasets for **SAFE-based** overrepresentation analysis and benchmarking:

- `supp_fig_2_4.ipynb` – SAFE-based annotation and domain export for GI and PPI networks
- `supp_fig_8.ipynb`, `supp_fig_8.py` – Benchmarking execution time and memory usage for SAFE (vs RISK) on synthetic networks
- `safepy/` – Python implementation of SAFE, includes core logic and utilities

---

## Installation

To run the notebooks locally, follow these steps:

### Step 1: Install Python 3.8+

Download and install Python 3.8 or higher from the [official website](https://www.python.org/downloads/).

> **Windows Tip:** Check the box for **Add Python to PATH** during install. If you missed it, [this guide](https://datatofish.com/add-python-to-windows-path/) can help.

### Step 2: Create a Virtual Environment

- **Windows**

```cmd
python -m venv risk-env
risk-env\Scripts\activate
```

- **macOS/Linux**

```bash
python3 -m venv risk-env
source risk-env/bin/activate
```

### Step 3: Install Jupyter and Dependencies

```bash
pip install -r requirements.txt
pip install jupyter
```

### Step 4: Clone This Repository

```bash
git clone https://github.com/riskportal/network-publication.git
cd network-publication
```

### Step 5: Launch Jupyter Notebook

```bash
jupyter notebook
```

---

## Figure Reproduction

Use the following notebooks to regenerate all manuscript figures:

### RISK Figures

- `fig_1_supp_fig_2_4_5_6.ipynb` – Yeast PPI network annotation and layout
- `supp_fig_1_3.ipynb` – GI network module analysis
- `supp_fig_7.ipynb` – Citation network validation
- `supp_fig_8.ipynb` – Benchmarking RISK vs SAFE

### SAFE Figures

- `supp_fig_2_4.ipynb` – SAFE-based GO BP overrepresentation (GI and PPI)
- `supp_fig_8.ipynb` – Benchmarking SAFE (comparative execution time, memory usage)

---

## Citation

If you use RISK in your research, please cite the following:

**Horecka and Röst (2025)**, _"RISK: a next-generation tool for biological network annotation and visualization"_.
<br>
DOI: [10.5281/zenodo.xxxxxxx](https://doi.org/10.5281/zenodo.xxxxxxx)

---

## License

This repository follows the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html).
