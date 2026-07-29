# ROI Simulator Assumptions

This dataset has no experimental (A/B tested) campaign response data, so uplift
rates below are reasoned estimates, not measured values, informed by typical
retention-marketing benchmarks (personalized offers commonly report single-digit
to low-teens percentage lifts in repeat spend).

| Segment | Assumed spend uplift | Assumed cost per targeted customer | Reasoning |
|---|---|---|---|
| VIP | 5% | $15 (premium support/early access) | Already high-value; uplift is modest, cost reflects white-glove service |
| Loyal | 8% | $5 (loyalty reward) | Reinforcement of existing behavior, low-cost reward |
| Growth | 12% | $8 (personalized discount) | Discounts have historically higher relative impact on mid-tier spenders |
| At Risk | 15% | $10 (win-back email) | Highest relative uplift potential since baseline is near zero, low email cost |

These are placeholder estimates for demonstration purposes. In a real deployment,
these would be calibrated using an actual holdout A/B test.