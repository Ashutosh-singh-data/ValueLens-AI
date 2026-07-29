import pandas as pd
from valuelens.preprocessing import clean_transactions, split_by_cutoff


def test_clean_transactions_removes_negative_quantity():
    df = pd.DataFrame({
        'Invoice': [1, 2, 3],
        'StockCode': ['A', 'B', 'C'],
        'Description': ['x', 'y', 'z'],
        'Quantity': [5, -3, 2],
        'InvoiceDate': ['2011-01-01 10:00:00', '2011-01-01 10:00:00', '2011-01-02 10:00:00'],
        'Price': [1.0, 2.0, 3.0],
        'Customer ID': [100, 101, 102],
        'Country': ['UK', 'UK', 'UK'],
    })
    cleaned = clean_transactions(df)
    assert (cleaned['Quantity'] >= 0).all()
    assert len(cleaned) == 2


def test_clean_transactions_removes_nulls_and_duplicates():
    df = pd.DataFrame({
        'Invoice': [1, 1, 2],
        'StockCode': ['A', 'A', 'B'],
        'Description': ['x', 'x', None],
        'Quantity': [5, 5, 3],
        'InvoiceDate': ['2011-01-01 10:00:00', '2011-01-01 10:00:00', '2011-01-01 10:00:00'],
        'Price': [1.0, 1.0, 2.0],
        'Customer ID': [100, 100, None],
        'Country': ['UK', 'UK', 'UK'],
    })
    cleaned = clean_transactions(df)
    assert len(cleaned) == 1  # duplicate row dropped, null Customer ID row dropped
    assert cleaned['Customer ID'].isnull().sum() == 0


def test_clean_transactions_adds_revenue_column():
    df = pd.DataFrame({
        'Invoice': [1],
        'StockCode': ['A'],
        'Description': ['x'],
        'Quantity': [4],
        'InvoiceDate': ['2011-01-01 10:00:00'],
        'Price': [2.5],
        'Customer ID': [100],
        'Country': ['UK'],
    })
    cleaned = clean_transactions(df)
    assert cleaned['Revenue'].iloc[0] == 10.0  # 4 * 2.5


def test_split_by_cutoff():
    df = pd.DataFrame({
        'Customer ID': [1, 1, 2],
        'Purchased_Date': pd.to_datetime(['2011-01-01', '2011-07-01', '2011-08-01']),
        'Revenue': [50, 60, 70],
    })
    df_features, df_label_window = split_by_cutoff(df, '2011-06-01')
    assert len(df_features) == 1
    assert len(df_label_window) == 2