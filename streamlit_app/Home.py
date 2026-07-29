import streamlit as st
from data_loader import load_customer_data

st.set_page_config(page_title="ValueLens AI", layout="wide")

df, thresholds = load_customer_data()

st.title("ValueLens AI — Executive Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{len(df):,}")
col2.metric("Total Predicted 6-Month Revenue", f"${df['predicted_clv'].sum():,.0f}")
col3.metric("Average Predicted CLV", f"${df['predicted_clv'].mean():,.0f}")

st.subheader("Segment Distribution")
st.bar_chart(df['segment'].value_counts())

st.subheader("Segment Thresholds")
st.write(thresholds)