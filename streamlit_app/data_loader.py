import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap

from valuelens.segmentation import add_segments
from valuelens.recommender import add_recommendations

FEATURE_COLS = ['Recency', 'Frequency', 'Monetary', 'Tenure', 'AvgOrderValue', 'ProductDiversity', 'WeekendRatio']


@st.cache_resource
def load_model():
    return joblib.load('models/clv_model.pkl')


@st.cache_resource
def load_explainer(_model):
    return shap.TreeExplainer(_model)


@st.cache_data
def load_customer_data():
    df = pd.read_csv('data/processed/customer_features.csv')
    model = load_model()
    X = df[FEATURE_COLS]

    df['predicted_clv'] = np.expm1(model.predict(X)).clip(min=0)
    df, thresholds = add_segments(df, clv_col='predicted_clv')
    df = add_recommendations(df)

    return df, thresholds


@st.cache_data
def compute_shap_values(_explainer, df):
    X = df[FEATURE_COLS]
    return _explainer(X)