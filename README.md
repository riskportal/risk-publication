# network-publication

<p align="center">
  <img src="https://i.imgur.com/8TleEJs.png" width="50%" alt="RISK Network logo" />
</p>

<br>

![Python](https://img.shields.io/badge/python-3.8%2B-yellow)
![License](https://img.shields.io/badge/license-GPLv3-purple)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxxx.svg)](https://doi.org/10.5281/zenodo.xxxxxxx)
![Platforms](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)

This repository contains Jupyter notebooks and datasets required to reproduce the figures in:

**Horecka & Röst, "RISK: a next-generation tool for biological network annotation and visualization", Bioinformatics, 2024.** [DOI: 10.1234/zenodo.xxxxxxx](https://doi.org/10.1234/zenodo.xxxxxxx)

## Repository Structure

- **risk_network/** – Notebooks and data for RISK analysis
  - `fig_1_supp_fig_3_6_7_8.ipynb`
  - `supp_fig_10.ipynb`
  - `supp_fig_1_4.ipynb`
  - `supp_fig_2_5.ipynb`
  - `supp_fig_9.ipynb`
  - `data/` – Processed datasets (cytoscape, gpickle, json)

- **safe_network/** – Notebooks and data for SAFE analysis
  - `supp_fig_10.ipynb`
  - `supp_fig_1_2_3.ipynb`
  - `data/` – SAFE-related datasets
  - `safepy/` – SAFE utilities

## Installation

To set up Python and Jupyter Notebook for RISK, follow these steps:

### Step 1: Install Python 3.8+

Download and install Python 3.8 or higher from the official  
[Python website](https://www.python.org/downloads/).

- **Windows Users:** During installation, check the box that says **Add Python to PATH**.  
  If you missed this step, follow this [guide](https://datatofish.com/add-python-to-windows-path/) to manually set the PATH.

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment helps manage dependencies.

- **Windows:**
  
  ```cmd
  python -m venv risk-env
  risk-env\Scripts\activate
  ```

- **macOS/Linux:**
  
  ```bash
  python3 -m venv risk-env
  source risk-env/bin/activate
  ```

### Step 3: Configure Jupyter Notebook to Use the Virtual Environment

To make sure Jupyter recognizes the virtual environment, follow  
[this guide](https://janakiev.com/blog/jupyter-virtual-envs/).

Then, select the environment inside Jupyter Notebook:

1. Click **Kernel** in the menu.
2. Choose **Change kernel**.
3. Select your virtual environment (e.g., `risk-env`).

### Step 4: Install Jupyter

With the virtual environment activated, install Jupyter Notebook:

```bash
pip install jupyter
```

### Step 5: Install RISK

```bash
pip install risk-network
```

### Step 6: Launch Jupyter Notebook

```bash
jupyter notebook
```

## Figure Reproduction

Each notebook corresponds to figures in the manuscript:

- `fig_1_supp_fig_3_6_7_8.ipynb` – Yeast PPI network analysis
- `supp_fig_10.ipynb` – Benchmarking execution time and memory usage
- `supp_fig_1_4.ipynb` – Genetic interaction network results
- `supp_fig_2_5.ipynb` – Additional cluster comparisons
- `supp_fig_9.ipynb` – High-energy physics citation network

## Citation

If this repository or RISK contributes to your research, please cite the following:

**Horecka & Röst, "RISK: a next-generation tool for biological network annotation and visualization", Bioinformatics, 2024.**  
[DOI: 10.1234/zenodo.xxxxxxx](https://doi.org/10.1234/zenodo.xxxxxxx)

## License

This repository is released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
