import pandas as pd
from valuelens.preprocessing import clean_transactions, split_by_cutoff
from valuelens.feature_engineering import build_customer_feature_table
from valuelens.train import train_model

RAW_DATA_PATH = 'data/raw/online_retail_II.csv'
PROCESSED_DATA_PATH = 'data/processed/customer_features.csv'
MODEL_OUTPUT_PATH = 'models/clv_model.pkl'
CUTOFF_DATE = '2011-06-01'

def run():
    print("Loading raw data...")
    df = pd.read_csv(RAW_DATA_PATH)

    print("Cleaning...")
    df = clean_transactions(df)

    print("Splitting by cutoff...")
    df_features, df_label_window = split_by_cutoff(df, CUTOFF_DATE)

    print("Building features + labels...")
    final = build_customer_feature_table(df_features, df_label_window, CUTOFF_DATE)
    final.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Saved {len(final)} customer rows to {PROCESSED_DATA_PATH}")

    print("Training model...")
    train_model(PROCESSED_DATA_PATH, MODEL_OUTPUT_PATH)
    print(f"Model saved to {MODEL_OUTPUT_PATH}")

if __name__ == '__main__':
    run()