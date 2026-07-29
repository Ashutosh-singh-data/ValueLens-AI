import pandas as pd

def build_features(df_features, reference_date):
    reference_date = pd.Timestamp(reference_date)

    Recency = pd.DataFrame(reference_date - df_features.groupby('Customer ID')['Purchased_Date'].max())
    Recency.columns = ['Recency']

    Frequency = pd.DataFrame(df_features.groupby('Customer ID')['Purchased_Date'].nunique())
    Frequency.columns = ['Frequency']

    Monetary = pd.DataFrame(df_features.groupby('Customer ID')['Revenue'].sum())
    Monetary.columns = ['Monetary']

    Tenure = pd.DataFrame(reference_date - df_features.groupby('Customer ID')['Purchased_Date'].min())
    Tenure.columns = ['Tenure']

    AvgOrderValue = pd.DataFrame(Monetary['Monetary'] / Frequency['Frequency'])
    AvgOrderValue.columns = ['AvgOrderValue']

    ProductDiversity = pd.DataFrame(df_features.groupby('Customer ID')['StockCode'].nunique())
    ProductDiversity.columns = ['ProductDiversity']

    df_features = df_features.copy()
    df_features['is_weekend'] = df_features['Purchased_Date'].dt.dayofweek >= 5
    WeekendRatio = pd.DataFrame(df_features.groupby('Customer ID')['is_weekend'].mean())
    WeekendRatio.columns = ['WeekendRatio']

    customer_features = Recency.merge(Frequency, on='Customer ID') \
        .merge(Monetary, on='Customer ID') \
        .merge(Tenure, on='Customer ID') \
        .merge(AvgOrderValue, on='Customer ID') \
        .merge(ProductDiversity, on='Customer ID') \
        .merge(WeekendRatio, on='Customer ID')

    customer_features['Recency'] = customer_features['Recency'].dt.days
    customer_features['Tenure'] = customer_features['Tenure'].dt.days

    return customer_features.reset_index()


def build_labels(df_label_window):
    labels = df_label_window.groupby('Customer ID')['Revenue'].sum().reset_index()
    labels.columns = ['Customer ID', 'future_6m_clv']
    return labels


def build_customer_feature_table(df_features, df_label_window, reference_date):
    customer_features = build_features(df_features, reference_date)
    labels = build_labels(df_label_window)

    final = customer_features.merge(labels, on='Customer ID', how='left')
    final['future_6m_clv'] = final['future_6m_clv'].fillna(0)
    return final