# ValueLens AI

**Predicting customer lifetime value and turning it into targeted marketing decisions.**

[![CI](https://github.com/Ashutosh-singh-data/ValueLens-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Ashutosh-singh-data/ValueLens-AI/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/dashboard-Streamlit-FF4B4B)](https://streamlit.io/)

🔗 **Live Demo:** https://valuelens-ai-analytics.streamlit.app/
---

## The Problem

An e-commerce company with thousands of customers can't afford to treat every customer the same. Coupons, cashback, free shipping, and premium support all cost money — spending them on the wrong customers is a wasted budget.

ValueLens AI answers four questions a marketing team actually asks:

1. Which customers will spend the most in the next 6 months?
2. Which customers are likely to churn?
3. How much should we spend to retain each customer?
4. Which campaign should each customer receive?

Rather than stopping at a prediction, this project turns that prediction into a full decision-support pipeline: **raw transactions → predicted CLV → customer segment → recommended action → simulated ROI**, wrapped in an interactive dashboard.

## Results

Four models were built and benchmarked on identical train/test splits, including the domain-standard probabilistic method (BG/NBD + Gamma-Gamma), not just off-the-shelf ML:

| Model | R² | MAE | RMSE |
|---|---|---|---|
| Linear Regression | 0.353 | $560.73 | $1,677.34 |
| BG/NBD + Gamma-Gamma | 0.446 | $646.30 | $1,552.41 |
| Random Forest | 0.519 | $522.73 | $1,446.32 |
| **XGBoost (selected)** | **0.550** | **$497.76** | **$1,399.11** |

**Notable finding:** BG/NBD outperforms Linear Regression on R² and RMSE but underperforms on MAE — because R²/RMSE penalize large errors more heavily, while MAE weights all errors equally. This suggests BG/NBD is more consistent on extreme cases but less accurate for typical customers, an artifact of its narrower feature set (frequency, recency, monetary only) versus the richer engineered features (product diversity, weekend ratio, tenure) available to XGBoost. Full discussion in [`reports/RESULTS.md`](reports/RESULTS.md).

Top predictive drivers (SHAP): **Monetary** (43%), **Recency** (15%), **Frequency** (11%) — consistent with retail CLV literature.

## Architecture

```
Raw Transactions (1.07M rows, Online Retail II)
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Time-Based Split (cutoff: 2011-06-01)
   ├── Feature Window (pre-cutoff, 18 months)
   └── Label Window (post-cutoff, 6 months)
        │
        ▼
Feature Engineering (RFM, tenure, diversity, seasonality)
        │
        ▼
Model Benchmarking (Linear Reg · BG/NBD · Random Forest · XGBoost)
        │
        ▼
SHAP Explainability
        │
        ▼
Customer Segmentation (quantile-based: VIP / Loyal / Growth / At Risk)
        │
        ▼
Marketing Recommendation Engine
        │
        ▼
ROI Simulator
        │
        ▼
Interactive Streamlit Dashboard
```

## Why the time-based split matters

Features are built only from transactions **before** the cutoff date; the label (`future_6m_clv`) is real revenue **after** it. This prevents the model from "predicting" the future using data from the future — the single most common correctness bug in CLV projects. See [`reports/ASSUMPTIONS.md`](reports/ASSUMPTIONS.md) for the full reasoning.

## Customer Segmentation

Segments are assigned by **quantile**, not fixed dollar thresholds, so the logic generalizes beyond this dataset's currency/scale:

| Segment | Threshold (predicted CLV) | Customers | Recommended Action |
|---|---|---|---|
| VIP | ≥ $949.57 (top 10%) | 494 | Early access + premium support |
| Loyal | ≥ $67.98 | 1,233 | Loyalty rewards |
| Growth | ≥ $4.81 | 1,727 | Personalized discounts |
| At Risk | < $4.81 | 1,481 | Win-back campaign |

## Tech Stack

- **Data & ML:** Python, pandas, scikit-learn, XGBoost, [lifetimes](https://github.com/CamDavidsonPilon/lifetimes) (BG/NBD + Gamma-Gamma)
- **Explainability:** SHAP
- **Dashboard:** Streamlit, Plotly
- **Testing/CI:** pytest, GitHub Actions
- **Packaging:** editable pip install, pinned dependencies

## Project Structure

```
ValueLens-AI/
├── .github/workflows/ci.yml     # automated tests on every push
├── config/config.yaml           # paths, cutoff date, thresholds
├── data/
│   ├── raw/                     # source dataset (not committed)
│   └── processed/               # engineered feature table
├── models/                      # trained model artifacts
├── notebooks/                   # exploration & experiment log
├── src/valuelens/
│   ├── preprocessing.py         # cleaning, time-based split
│   ├── feature_engineering.py   # RFM/tenure feature construction
│   ├── train.py                 # model training (XGBoost)
│   ├── predict.py               # inference on new raw transactions
│   ├── segmentation.py          # quantile-based customer segments
│   ├── recommender.py           # segment → action mapping
│   ├── roi_simulator.py         # campaign ROI simulation
│   └── explain.py               # SHAP explainability
├── streamlit_app/                # 4-page interactive dashboard
├── tests/                       # unit tests for all core logic
├── reports/
│   ├── ASSUMPTIONS.md           # documented business assumptions
│   └── RESULTS.md               # full model comparison & analysis
└── requirements.txt
```

## Setup

```bash
git clone https://github.com/Ashutosh-singh-data/ValueLens-AI.git
cd ValueLens-AI

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -e .

pytest tests/ -v                 # run the test suite

streamlit run streamlit_app/Home.py   # launch the dashboard
```

Dataset: [Online Retail II (UCI)](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci) — download and place at `data/raw/online_retail_II.csv`.

## Key Design Decisions

- **Time-based train/label split** to prevent leakage (see above)
- **Log-transformed target** to handle heavy right-skew in customer spend, with `PowerTransformer` fit only on training data for the linear baseline
- **Tree models trained on raw (untransformed) features** — scale/skew doesn't affect split-based models, so this was a deliberate choice, not an oversight
- **BG/NBD + Gamma-Gamma benchmarked with the same train/test customer split** as the ML models, for a fair, leakage-free comparison
- **Quantile-based segmentation** instead of fixed dollar thresholds, for portability across datasets/currencies
- **Explicit, documented ROI assumptions** rather than presenting estimates as measured fact — see [`reports/ASSUMPTIONS.md`](reports/ASSUMPTIONS.md)

## Limitations & Future Work

- ROI uplift figures are reasoned estimates, not derived from an A/B test — a real deployment would calibrate these against holdout campaign data
- Segmentation thresholds are recalculated from whichever customer base is scored; production use would fix thresholds periodically rather than recomputing per batch
- Feature set does not yet include product-category-level signals or marketing channel history, which could improve model performance further

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

## Author

Ashutosh singh — B.Tech, Production & Industrial Engineering, MNNIT Allahabad. Built as a portfolio project exploring the intersection of applied ML and business decision support.
