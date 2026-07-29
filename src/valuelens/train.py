import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

FEATURE_COLS = ['Recency', 'Frequency', 'Monetary', 'Tenure', 'AvgOrderValue', 'ProductDiversity', 'WeekendRatio']

def train_model(customer_features_path, model_output_path):
    df = pd.read_csv(customer_features_path)

    X = df[FEATURE_COLS]
    y = df['future_6m_clv']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    y_train_log = np.log1p(y_train)

    xgb = XGBRegressor(n_estimators=200, learning_rate=0.05, random_state=42)
    xgb.fit(X_train, y_train_log)

    joblib.dump(xgb, model_output_path)
    return xgb