SEGMENT_ASSUMPTIONS = {
    'VIP':      {'uplift': 0.05, 'cost_per_customer': 15},
    'Loyal':    {'uplift': 0.08, 'cost_per_customer': 5},
    'Growth':   {'uplift': 0.12, 'cost_per_customer': 8},
    'At Risk':  {'uplift': 0.15, 'cost_per_customer': 10},
}


def simulate_roi(df, target_segments, clv_col='predicted_clv', segment_col='segment'):
    targeted = df[df[segment_col].isin(target_segments)]

    baseline_revenue = targeted[clv_col].sum()

    incremental_revenue = 0.0
    campaign_cost = 0.0

    for segment in target_segments:
        segment_df = targeted[targeted[segment_col] == segment]
        assumptions = SEGMENT_ASSUMPTIONS.get(segment)
        if assumptions is None:
            continue

        incremental_revenue += segment_df[clv_col].sum() * assumptions['uplift']
        campaign_cost += len(segment_df) * assumptions['cost_per_customer']

    net_profit = incremental_revenue - campaign_cost
    roi = (net_profit / campaign_cost) if campaign_cost > 0 else None

    return {
        'targeted_customers': len(targeted),
        'baseline_revenue': round(baseline_revenue, 2),
        'incremental_revenue': round(incremental_revenue, 2),
        'campaign_cost': round(campaign_cost, 2),
        'net_profit': round(net_profit, 2),
        'roi_percent': round(roi * 100, 2) if roi is not None else None,
    }