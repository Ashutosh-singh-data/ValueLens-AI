import streamlit as st
import shap
import matplotlib.pyplot as plt
from data_loader import load_customer_data, load_model, load_explainer, compute_shap_values, FEATURE_COLS
from style import inject_custom_css, segment_badge

st.set_page_config(page_title="Customer Explorer", layout="wide")
inject_custom_css()

df, thresholds = load_customer_data()
model = load_model()
explainer = load_explainer(model)
shap_values = compute_shap_values(explainer, df)

st.title("Customer Explorer")

customer_id = st.selectbox("Select Customer ID", df['Customer ID'].sort_values().unique())
row_index = df[df['Customer ID'] == customer_id].index[0]
customer_row = df.loc[row_index]

col1, col2, col3 = st.columns(3)
col1.metric("Predicted 6-Month CLV", f"${customer_row['predicted_clv']:,.2f}")
with col2:
    st.markdown("**Segment**")
    st.markdown(segment_badge(customer_row['segment']), unsafe_allow_html=True)
col3.metric("Recommended Action", customer_row['recommended_action'])

st.divider()
st.subheader("Customer Profile")
profile_cols = st.columns(len(FEATURE_COLS))
for col, feature in zip(profile_cols, FEATURE_COLS):
    col.metric(feature, f"{customer_row[feature]:,.1f}")

st.divider()
st.subheader("Why did the model predict this?")
fig, ax = plt.subplots()
shap.plots.waterfall(shap_values[row_index], show=False)
st.pyplot(fig)