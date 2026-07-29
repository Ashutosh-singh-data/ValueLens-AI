import pandas as pd
from valuelens.feature_engineering import build_features, build_labels, build_customer_feature_table


def make_sample_df_features():
    return pd.DataFrame({
        'Customer ID': [1, 1, 2],
        'Purchased_Date': pd.to_datetime(['2011-01-01', '2011-03-01', '2011-02-01']),
        'Revenue': [100.0, 50.0, 200.0],
        'StockCode': ['A', 'B', 'C'],
    })


def test_build_features_known_values():
    df_features = make_sample_df_features()
    features = build_features(df_features, reference_date='2011-06-01')

    row1 = features[features['Customer ID'] == 1].iloc[0]
    assert row1['Frequency'] == 2
    assert row1['Monetary'] == 150.0
    assert row1['AvgOrderValue'] == 75.0
    assert row1['Recency'] == (pd.Timestamp('2011-06-01') - pd.Timestamp('2011-03-01')).days

    row2 = features[features['Customer ID'] == 2].iloc[0]
    assert row2['Frequency'] == 1
    assert row2['Monetary'] == 200.0


def test_build_labels_sums_revenue_per_customer():
    df_label_window = pd.DataFrame({
        'Customer ID': [1, 1, 3],
        'Revenue': [30.0, 20.0, 40.0],
    })
    labels = build_labels(df_label_window)
    assert labels[labels['Customer ID'] == 1]['future_6m_clv'].iloc[0] == 50.0
    assert labels[labels['Customer ID'] == 3]['future_6m_clv'].iloc[0] == 40.0


def test_build_customer_feature_table_fills_zero_for_no_future_purchase():
    df_features = make_sample_df_features()
    df_label_window = pd.DataFrame({'Customer ID': [1], 'Revenue': [999.0]})  # customer 2 never buys again

    final = build_customer_feature_table(df_features, df_label_window, reference_date='2011-06-01')

    customer_2_label = final[final['Customer ID'] == 2]['future_6m_clv'].iloc[0]
    assert customer_2_label == 0.0