# network-publication

<p align="center">
  <img src="https://i.imgur.com/8TleEJs.png" width="50%" alt="RISK Network logo" />
</p>

<br>

![Python](https://img.shields.io/badge/python-3.8%2B-yellow)
![License](https://img.shields.io/badge/license-GPLv3-purple)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxxx.svg)](https://doi.org/10.5281/zenodo.xxxxxxx)

This repository provides Jupyter notebooks and datasets necessary to reproduce all figures from the **RISK** and **SAFE** analyses described in:

**Horecka et al.**, *"RISK: a next-generation tool for biological network annotation and visualization"*, *Bioinformatics*, 2025.  
[DOI: 10.1234/zenodo.xxxxxxx](https://doi.org/10.1234/zenodo.xxxxxxx)

---

## Documentation

Full documentation (with examples and usage guidance) is available at [https://riskportal.github.io/network-tutorial/](https://riskportal.github.io/network-tutorial/).

## Repository Structure

This repository contains the notebooks and data needed to reproduce figures from the RISK and SAFE analyses. The full RISK source code is available at [riskportal/network](https://github.com/riskportal/network).

### `risk_network/`

Jupyter notebooks and processed datasets for **RISK-based** clustering, annotation, and visualization:

- `fig_1_supp_fig_3_6_7_8.ipynb` – Yeast PPI network analysis, RISK workflow overview, GO BP enrichment, and comparison to SAFE
- `supp_fig_1_4.ipynb` – GI network analysis (RISK) and side-by-side comparison with SAFE
- `supp_fig_2_5.ipynb` – RISK analysis of the full yeast PPI network and comparative clustering (RISK vs SAFE)
- `supp_fig_9.ipynb` – RISK analysis of a high-energy physics citation network (non-biological validation)
- `supp_fig_10.ipynb`, `supp_fig_10.py` – Benchmarking: execution time and memory usage for RISK (vs SAFE) using synthetic networks

### `safe_network/`

Jupyter notebooks and datasets for **SAFE-based** overrepresentation analysis and benchmarking:

- `supp_fig_3_4_5.ipynb` – SAFE-based annotation and domain export for GI and PPI networks, including pruned/full networks
- `supp_fig_10.ipynb`, `supp_fig_10.py` – Benchmarking: execution time and memory usage for SAFE (vs RISK) on synthetic networks
- `safepy/` – Lightweight Python implementation of SAFE, includes core logic and utilities

---

## Installation

To run the notebooks locally, follow these steps:

### Step 1: Install Python 3.8+

Download and install Python 3.8 or higher from the [official website](https://www.python.org/downloads/).

> 💡 **Windows Tip:** Check the box for **Add Python to PATH** during install. If you missed it, [this guide](https://datatofish.com/add-python-to-windows-path/) can help.

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

- `fig_1_supp_fig_3_6_7_8.ipynb` – Yeast PPI network annotation and layout
- `supp_fig_1_4.ipynb` – GI network module analysis
- `supp_fig_2_5.ipynb` – PPI comparisons (RISK vs SAFE)
- `supp_fig_9.ipynb` – Citation network validation
- `supp_fig_10.ipynb` – Benchmarking RISK vs SAFE

### SAFE Figures

- `supp_fig_3_4_5.ipynb` – SAFE-based GO BP overrepresentation (GI and PPI)
- `supp_fig_10.ipynb` – Benchmarking SAFE (comparative execution time, memory usage)

---

## Citation

If you use RISK or SAFE benchmarking in your research, please cite:

**Horecka et al.**, *"RISK: a next-generation tool for biological network annotation and visualization"*, **Bioinformatics**, 2025.  
DOI: [10.1234/zenodo.xxxxxxx](https://doi.org/10.1234/zenodo.xxxxxxx)

---

## License

This repository is distributed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
