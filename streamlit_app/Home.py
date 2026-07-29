import streamlit as st
from data_loader import load_customer_data
from style import inject_custom_css, SEGMENT_COLORS

st.set_page_config(page_title="ValueLens AI", layout="wide", page_icon="💡")
inject_custom_css()

df, thresholds = load_customer_data()

st.title("ValueLens AI — Executive Dashboard")
st.caption("Predictive customer lifetime value and marketing decision support")

col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Customers", f"{len(df):,}")
col2.metric("💰 Total Predicted 6-Month Revenue", f"${df['predicted_clv'].sum():,.0f}")
col3.metric("📊 Average Predicted CLV", f"${df['predicted_clv'].mean():,.0f}")

st.subheader("Segment Distribution")

segment_order = ['At Risk', 'Growth', 'Loyal', 'VIP']
counts = df['segment'].value_counts().reindex(segment_order)

import plotly.express as px
fig = px.bar(
    x=counts.index, y=counts.values,
    color=counts.index,
    color_discrete_map=SEGMENT_COLORS,
    labels={'x': 'Segment', 'y': 'Customer Count'}
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

with st.expander("View exact segment thresholds"):
    st.json(thresholds)