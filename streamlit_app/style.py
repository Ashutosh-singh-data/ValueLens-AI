import streamlit as st

SEGMENT_COLORS = {
    'VIP': '#FFD700',
    'Loyal': '#4CAF50',
    'Growth': '#2196F3',
    'At Risk': '#F44336',
}

SEGMENT_TEXT_COLORS = {
    'VIP': '#1a1a1a',      # dark text on gold — good contrast
    'Loyal': '#FFFFFF',    # white text on green
    'Growth': '#FFFFFF',   # white text on blue
    'At Risk': '#FFFFFF',  # white text on red
}


def inject_custom_css():
    st.markdown("""
        <style>
        [data-testid="stMetric"] {
            background-color: #1E1E2F;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 15px 10px;
        }
        [data-testid="stMetricLabel"] {
            font-size: 14px;
            color: #AAAAAA;
        }
        h1 {
            padding-bottom: 10px;
            border-bottom: 2px solid #2196F3;
        }
        .segment-badge {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 10px 0;
            border-radius: 20px;
            font-weight: 800;
            font-size: 18px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            box-sizing: border-box;
        }
        </style>
    """, unsafe_allow_html=True)


def segment_badge(segment):
    bg_color = SEGMENT_COLORS.get(segment, '#888888')
    text_color = SEGMENT_TEXT_COLORS.get(segment, '#FFFFFF')
    return (
        f"<div class='segment-badge' style='background-color:{bg_color}; color:{text_color};'>"
        f"{segment}</div>"
    )