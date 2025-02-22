# packages
import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    return pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\money_2024\mls_finances.csv")

def app():
    st.markdown(
        "<h1 style='text-align: center; font-style: italic;'>Profits off the Pitch.</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h4 style='text-align: center;'>You're inside the Box Office.</h4>",
        unsafe_allow_html=True,
    )

    df = load_data()
    selected_teams = st.session_state.get("selected_clubs", [])  # Use correct key

    color_map = df.set_index('club')['color'].to_dict()

    col1, col2, col3 = st.columns([2.5, 1, 2.5])
    with col2:
        highlight_selected = st.checkbox("Highlight My Clubs")

    if highlight_selected:
        for club in color_map.keys():
            if club not in selected_teams:
                color_map[club] = "gray"
    else:
        for club in color_map.keys():
            color_map[club] = df[df['club'] == club]['color'].values[0]  # Reset original colors

    # Club Values - Treemap

    fig_value = px.treemap(df, path=["club"], values="value", title="Club Values",
                        color="club", color_discrete_map=color_map)
    st.plotly_chart(fig_value)

    # Revenue - Bar Chart

    fig_revenue = px.bar(df.sort_values("revenue", ascending=True),
                        x="revenue", y="club", title="Revenue by Club",
                        orientation="h", text_auto=True, color="club", color_discrete_map=color_map)
    st.plotly_chart(fig_revenue)

    # Attendance - Bubble Chart

    fig_attendance = px.scatter(df.sort_values("attendance", ascending=True),
                                x="attendance", y="club", title="Attendance by Club",
                                color="club", size="attendance", color_discrete_map=color_map,
                                size_max=10)
    st.plotly_chart(fig_attendance)

    # Payroll - Colored Bar Chart

    fig_payroll = px.bar(df.sort_values("payroll", ascending=True),
                        x="payroll", y="club", title="Payroll by Club",
                        orientation="h", text_auto=True, color="club", color_discrete_map=color_map)
    st.plotly_chart(fig_payroll)

