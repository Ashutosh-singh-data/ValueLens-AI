import pandas as pd

def clean_transactions(df):
    df = df.drop(columns='Description')
    df = df.dropna(axis=0)
    df = df.drop_duplicates()
    df = df[df['Quantity'] >= 0]

    df['Revenue'] = df['Quantity'] * df['Price']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Purchased_Date'] = df['InvoiceDate'].dt.normalize()
    df['Customer ID'] = df['Customer ID'].astype(int)

    return df


def split_by_cutoff(df, cutoff_date):
    df_features = df[df['Purchased_Date'] < cutoff_date]
    df_label_window = df[df['Purchased_Date'] >= cutoff_date]
    return df_features, df_label_window