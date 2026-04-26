# MovieLens 1M Data Mining & Recommendation System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-red.svg)](https://plotly.com/)
[![mlxtend](https://img.shields.io/badge/mlxtend-FP--Growth-purple.svg)](https://rasbt.github.io/mlxtend/)
[![License](https://img.shields.io/badge/License-MovieLens-yellow.svg)](https://grouplens.org/)

> Data mining course assignment analyzing the MovieLens 1M dataset with EDA, Association Rule Mining (Apriori/FP-Growth), and future implementations of Collaborative Filtering & Content-Based Filtering.

## 📊 Dataset Overview

| Metric | Value |
|--------|-------|
| Total Ratings | 1,000,209 |
| Unique Users | 6,040 |
| Unique Movies | 3,883 |
| Genres | 18 |
| Time Range | Apr 2000 - Feb 2003 |

**Source:** [MovieLens 1M Dataset](https://grouplens.org/datasets/movielens/1m/) by GroupLens Research

## 📚 Project Notebooks

| Phần | Nội dung | Người thực hiện | Colab |
|------|----------|----------------|-------|
| 🧠 **Part 1** | EDA + Apriori | **Lê Chí Đại** | [![Open in Colab](https://img.shields.io/badge/Colab-Open-orange?logo=googlecolab)](https://colab.research.google.com/drive/1EXQfRIjImTzHXtLIBKAWVd4RTO_6TCMm#scrollTo=bKX6njM94V-Q) |
| 🤝 **Part 2** | Collaborative Filtering (User-based, Item-based) | **Lương Minh Thuận** | [![Open in Colab](https://img.shields.io/badge/Colab-Open-orange?logo=googlecolab)](https://colab.research.google.com/drive/186mV-rzJzykv6N9NI9gGj3Q9s0XEpxyB) |
| 🎯 **Part 3** | Content-Based Filtering | **Nguyễn Quốc Huy** | [![Open in Colab](https://img.shields.io/badge/Colab-Open-orange?logo=googlecolab)](https://colab.research.google.com/drive/1oS8C_EHvhNbWyd49yC3RFRIaaP0EtUzC) |

---

## 🗂️ Project Structure

```
.
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── movielens_analysis.ipynb     # Main analysis notebook
├── ml-1m/                      # Dataset directory
│   ├── ratings.dat
│   ├── users.dat
│   ├── movies.dat
│   └── README
└── .venv/                      # Virtual environment
```

---

## 🚀 Quick Start

### 1. Setup

Recommend way is to using Google Colab attach at the beginning.

Or:
```bash
# Navigate to project directory
cd /path/to/project

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Notebook

```bash
# Start Jupyter Lab
jupyter lab movielens_analysis.ipynb

# Or use Jupyter Notebook
jupyter notebook movielens_analysis.ipynb
```

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.11+ |
| Data Processing | pandas, numpy |
| Visualization | Plotly, Seaborn |
| Mining | mlxtend (FP-Growth, Apriori) |
| Development | Jupyter Notebook |

---

## 📜 License

This dataset is provided by [GroupLens Research](https://grouplens.org/) under their usage terms. See `ml-1m/README` for details.

This project is for educational purposes as part of the Data Mining course assignment.

---

## 👥 Contributors

| Role | Description |
|------|-------------|
| Data Mining Course | Assignment |
| Dataset | MovieLens 1M by GroupLens |

---

## 🔗 References

1. [MovieLens Dataset](https://grouplens.org/datasets/movielens/1m)
2. [Harper, F. M., & Konstan, J. A. (2015)](https://dl.acm.org/doi/10.1145/2827872) - The MovieLens Datasets: History and Context
3. [FP-Growth Algorithm](https://rasbt.github.io/mlxtend/api_reference/frequent_patterns/mlxtend.frequent_patterns.fpgrowth/)
4. [Association Rules](https://rasbt.github.io/mlxtend/api_reference/frequent_patterns/mlxtend.frequent_patterns.association_rules/)

---

*Last Updated: April 2026*