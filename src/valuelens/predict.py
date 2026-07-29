import pandas as pd
import numpy as np
import joblib

from valuelens.preprocessing import clean_transactions
from valuelens.feature_engineering import build_features
from valuelens.segmentation import add_segments
from valuelens.recommender import add_recommendations

FEATURE_COLS = ['Recency', 'Frequency', 'Monetary', 'Tenure', 'AvgOrderValue', 'ProductDiversity', 'WeekendRatio']


def load_model(model_path='models/clv_model.pkl'):
    return joblib.load(model_path)


def predict_from_raw_transactions(raw_df, reference_date, model_path='models/clv_model.pkl'):
    df = clean_transactions(raw_df)
    features = build_features(df, reference_date)

    model = load_model(model_path)
    X = features[FEATURE_COLS]
    features['predicted_clv'] = np.expm1(model.predict(X)).clip(min=0)

    features, thresholds = add_segments(features, clv_col='predicted_clv')
    features = add_recommendations(features)

    return features


def predict_single_customer(customer_id, raw_df, reference_date, model_path='models/clv_model.pkl'):
    results = predict_from_raw_transactions(raw_df, reference_date, model_path)
    return results[results['Customer ID'] == customer_id]