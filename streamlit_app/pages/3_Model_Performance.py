import streamlit as st
import shap
import matplotlib.pyplot as plt
from data_loader import load_customer_data, load_model, load_explainer, compute_shap_values, FEATURE_COLS

st.set_page_config(page_title="Model Performance", layout="wide")

st.title("Model Performance")

st.write("Comparison of all models evaluated for predicting 6-month Customer Lifetime Value.")

comparison_data = {
    "Model": ["Linear Regression", "BG/NBD + Gamma-Gamma", "Random Forest", "XGBoost"],
    "R²": [0.353, 0.446, 0.519, 0.550],
    "MAE ($)": [560.73, 646.30, 522.73, 497.76],
    "RMSE ($)": [1677.34, 1552.41, 1446.32, 1399.11],
}
import pandas as pd

comparison_df = pd.DataFrame(comparison_data)
best_row = comparison_df['R²'].idxmax()

def highlight_best(row):
    return ['background-color: #2196F3; color: white' if row.name == best_row else '' for _ in row]

st.dataframe(comparison_df.style.apply(highlight_best, axis=1), use_container_width=True)

st.caption(
    "XGBoost was selected as the production model. Note BG/NBD has a higher MAE "
    "despite a better R² than Linear Regression — R²/RMSE weight large errors more "
    "heavily, suggesting BG/NBD is more consistent on extreme cases but less accurate "
    "on typical customers. See reports/ASSUMPTIONS.md and README for full discussion."
)

st.subheader("Global Feature Importance (SHAP)")

df, thresholds = load_customer_data()
model = load_model()
explainer = load_explainer(model)
shap_values = compute_shap_values(explainer, df)

fig, ax = plt.subplots()
shap.summary_plot(shap_values, df[FEATURE_COLS], show=False)
st.pyplot(fig)