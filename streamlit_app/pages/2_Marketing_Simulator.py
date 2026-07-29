import streamlit as st
from data_loader import load_customer_data
from valuelens.roi_simulator import simulate_roi, SEGMENT_ASSUMPTIONS
from style import segment_badge

st.set_page_config(page_title="Marketing Simulator", layout="wide")

df, thresholds = load_customer_data()

st.title("Marketing Simulator")
st.write("Select which customer segments to target with a campaign, and see the projected business impact.")

ALL_SEGMENTS = ['VIP', 'Loyal', 'Growth', 'At Risk']

st.write("Target Segments:")
badge_cols = st.columns(4)
for col, seg in zip(badge_cols, ALL_SEGMENTS):
    with col:
        st.markdown(segment_badge(seg), unsafe_allow_html=True)

selected_segments = st.multiselect(
    "Select segments to simulate",
    ALL_SEGMENTS,
    default=ALL_SEGMENTS
)

if selected_segments:
    result = simulate_roi(df, target_segments=selected_segments)

    col1, col2, col3 = st.columns(3)
    col1.metric("Targeted Customers", f"{result['targeted_customers']:,}")
    col2.metric("Campaign Cost", f"${result['campaign_cost']:,.0f}")
    col3.metric("Net Profit", f"${result['net_profit']:,.0f}")

    col4, col5 = st.columns(2)
    col4.metric("Incremental Revenue", f"${result['incremental_revenue']:,.0f}")
    col5.metric("ROI", f"{result['roi_percent']}%" if result['roi_percent'] is not None else "N/A")

    st.subheader("Compare: Target Everyone vs. Your Selection")
    everyone_result = simulate_roi(df, target_segments=ALL_SEGMENTS)

    comparison_df = {
        "Scenario": ["Target Everyone", "Your Selection"],
        "Campaign Cost": [everyone_result['campaign_cost'], result['campaign_cost']],
        "Net Profit": [everyone_result['net_profit'], result['net_profit']],
        "ROI %": [everyone_result['roi_percent'], result['roi_percent']],
    }
    st.dataframe(comparison_df, use_container_width=True)

    with st.expander("View assumptions used in this simulation"):
        st.write(SEGMENT_ASSUMPTIONS)
        st.caption("See reports/ASSUMPTIONS.md for full reasoning behind these uplift and cost figures.")
else:
    st.warning("Select at least one segment to see results.")