import streamlit as st
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt

from data_loader import load_customer_data, load_model, load_explainer, FEATURE_COLS
from valuelens.segmentation import compute_thresholds, assign_segment
from valuelens.recommender import get_recommendation

st.set_page_config(page_title="What-If Predictor", layout="wide")

st.title("🔮 What-If Customer Predictor")
st.write("Adjust a customer's behavior below and see the model's live prediction — no need to pick an existing customer.")

df, _ = load_customer_data()
model = load_model()
explainer = load_explainer(model)
thresholds = compute_thresholds(df['predicted_clv'])

# --- Optional: prefill from a real customer, then let them tweak ---
prefill = st.selectbox(
    "Start from a real customer (optional)",
    ["Custom"] + list(df['Customer ID'].sort_values().unique())
)

if prefill != "Custom":
    base = df[df['Customer ID'] == prefill].iloc[0]
else:
    base = df[FEATURE_COLS].median()

st.divider()

col1, col2 = st.columns(2)
with col1:
    recency = st.slider("Recency (days since last purchase)", 0, 600, int(base['Recency']))
    frequency = st.slider("Frequency (number of orders)", 1, 50, int(base['Frequency']))
    monetary = st.number_input("Monetary (total historical spend, $)", 0.0, 100000.0, float(base['Monetary']))
    tenure = st.slider("Tenure (days as a customer)", 1, 700, int(base['Tenure']))

with col2:
    avg_order_value = st.number_input("Average Order Value ($)", 0.0, 20000.0, float(base['AvgOrderValue']))
    product_diversity = st.slider("Product Diversity (distinct products bought)", 1, 300, int(base['ProductDiversity']))
    weekend_ratio = st.slider("Weekend Purchase Ratio", 0.0, 1.0, float(base['WeekendRatio']))

st.divider()

# --- Build the input row and predict ---
input_row = pd.DataFrame([{
    'Recency': recency,
    'Frequency': frequency,
    'Monetary': monetary,
    'Tenure': tenure,
    'AvgOrderValue': avg_order_value,
    'ProductDiversity': product_diversity,
    'WeekendRatio': weekend_ratio,
}])

predicted_log = model.predict(input_row[FEATURE_COLS])[0]
predicted_clv = max(0, np.expm1(predicted_log))
segment = assign_segment(predicted_clv, thresholds)
recommendation = get_recommendation(segment)

segment_colors = {
    'VIP': '#FFD700', 'Loyal': '#4CAF50', 'Growth': '#2196F3', 'At Risk': '#F44336'
}

st.subheader("Prediction Result")
result_col1, result_col2, result_col3 = st.columns(3)
result_col1.metric("Predicted 6-Month CLV", f"${predicted_clv:,.2f}")

with result_col2:
    st.markdown(
        f"<div style='background-color:{segment_colors[segment]}; padding:10px; "
        f"border-radius:8px; text-align:center; font-weight:bold; color:black;'>"
        f"{segment}</div>", unsafe_allow_html=True
    )

result_col3.metric("Recommended Action", recommendation['action'])

st.caption(recommendation['description'])

st.subheader("Why did the model predict this?")
shap_values = explainer(input_row[FEATURE_COLS])
fig, ax = plt.subplots()
shap.plots.waterfall(shap_values[0], show=False)
st.pyplot(fig)