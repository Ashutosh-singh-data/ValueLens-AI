import pandas as pd


def compute_thresholds(predicted_clv):
    return {
        'vip': predicted_clv.quantile(0.90),
        'loyal': predicted_clv.quantile(0.65),
        'growth': predicted_clv.quantile(0.30),
    }


def assign_segment(clv, thresholds):
    if clv >= thresholds['vip']:
        return 'VIP'
    elif clv >= thresholds['loyal']:
        return 'Loyal'
    elif clv >= thresholds['growth']:
        return 'Growth'
    else:
        return 'At Risk'


def add_segments(df, clv_col='predicted_clv'):
    df = df.copy()
    df[clv_col] = df[clv_col].clip(lower=0)

    thresholds = compute_thresholds(df[clv_col])
    df['segment'] = df[clv_col].apply(lambda clv: assign_segment(clv, thresholds))

    return df, thresholds