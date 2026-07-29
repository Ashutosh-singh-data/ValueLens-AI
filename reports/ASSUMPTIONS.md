# Assumptions & Methodological Decisions

This document records the key assumptions and design decisions made throughout ValueLens AI, so results can be interpreted correctly and reproduced. Every number here is either derived directly from the data or explicitly flagged as an estimate.

---

## 1. Time-Based Train/Label Split

**Decision:** `2011-06-01` is used as the observation cutoff. All predictive features are built exclusively from transactions **before** this date; the target label (`future_6m_clv`) is real revenue **after** it, within a 6-month window.

**Reasoning:** The dataset spans 2009-12-01 to 2011-12-09 (~24 months). A 6-month label window requires holding out the final 6 months; the remaining ~18 months (including two holiday seasons) provide feature history. Building features and label from overlapping time periods would let the model "see" the answer during training — the single most common correctness failure in CLV modeling projects.

**Consequence:** Customers whose first purchase occurs after the cutoff are excluded from training (no feature history exists for them). Customers with feature history but no post-cutoff purchase receive a label of `$0` — a real churn signal, not missing data.

## 2. Target Transformation

**Decision:** The target (`future_6m_clv`) is log-transformed (`log1p`) before training linear models, and predictions are converted back (`expm1`) for reporting.

**Reasoning:** Customer spend is heavily right-skewed (a small number of high-value customers dominate raw scale). Training directly on raw dollars causes models to over-index on minimizing error for extreme values at the expense of typical customers. All reported MAE/RMSE figures are in real dollars (post-`expm1`), not log-space, for interpretability. R² is reported in log-space for model comparison, since it is scale-invariant and standard practice for skewed targets.

## 3. Feature Scaling

**Decision:** `PowerTransformer` (Yeo-Johnson) is fit only on training data and applied to the Linear Regression baseline. Tree-based models (Random Forest, XGBoost) are trained on raw, untransformed features.

**Reasoning:** Tree-based models split on feature order, not scale — a monotonic transform cannot change their splits, so applying one adds complexity without benefit. This is a deliberate simplification, not an inconsistency.

## 4. BG/NBD + Gamma-Gamma Benchmark

**Decision:** The probabilistic CLV model (industry-standard for this problem class) is fit **only on training-set customers' transactions** and evaluated on held-out test customers, using the same train/test split as the ML models.

**Reasoning:** Fitting on the full population (including test customers) before evaluation would let population-level parameters be influenced by the customers being scored — a milder form of leakage than label leakage, but still inconsistent with how the other three models were evaluated. Matching evaluation protocol across all four models keeps the comparison table fair.

## 5. Customer Segmentation Thresholds

**Decision:** Segments (VIP / Loyal / Growth / At Risk) are assigned using quantiles of predicted CLV (90th / 65th / 30th percentile), recalculated from whichever customer set is being scored — not fixed dollar amounts.

**Reasoning:** Fixed thresholds tuned to one dataset's currency and scale don't generalize. Quantile-based cutoffs make the logic portable and simple to explain ("VIP = top 10% of predicted future value").

**Limitation:** In production, thresholds should be fixed on a periodic cadence (e.g., quarterly) rather than recomputed on every scoring run, to avoid segment definitions drifting with each batch.

## 6. ROI Simulator — Uplift & Cost Assumptions

**This is the one set of numbers in this project that is not derived from the data.** The Online Retail II dataset contains no experimental (A/B tested) campaign response data, so there is no way to measure the actual causal effect of a coupon, discount, or win-back email on this population. The figures below are **reasoned placeholder estimates**, informed by commonly cited ranges in retention-marketing literature (personalized offers typically report single-digit to low-teens percentage lifts in repeat spend), and are presented as assumptions, not measured facts.

| Segment | Assumed Spend Uplift | Assumed Cost / Customer | Reasoning |
|---|---|---|---|
| VIP | 5% | $15 (premium support / early access) | Already high-value; uplift is modest by design, cost reflects white-glove service tier |
| Loyal | 8% | $5 (loyalty reward) | Reinforcement of existing behavior; low-cost recognition |
| Growth | 12% | $8 (personalized discount) | Discounts historically show higher relative impact on mid-tier spenders |
| At Risk | 15% | $10 (win-back email) | Highest relative uplift potential off a near-zero baseline; low-cost channel |

**In a real deployment**, these figures would be calibrated using a holdout A/B test — running the campaign on a randomly held-out subset of each segment and measuring actual incremental spend, rather than assuming it.

## 7. Data Cleaning Rules

- Transactions with `Invoice` starting with `"C"` (cancellations) are removed
- Rows with `Quantity <= 0` or missing `Customer ID` are removed (no reliable customer attribution or no genuine transaction)
- Exact duplicate rows are removed
- `Revenue` is computed as `Quantity × Price`

These mirror standard practice for this dataset and are implemented in `src/valuelens/preprocessing.py`.
