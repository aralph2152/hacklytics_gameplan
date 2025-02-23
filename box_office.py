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
        "<h4 style='text-align: center;'>Take a look inside the Box Office.</h4>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        div[data-baseweb="checkbox"] * {
            outline: none !important;
            box-shadow: none !important;
            border-color: transparent !important;
        }

        div[data-baseweb="checkbox"] input:checked + div {
            background-color: #9f9f9f !important; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()
    selected_teams = st.session_state.get("selected_clubs", [])

    color_map = {club: color for club, color in sorted(df.set_index('club')['color'].items())}

    col1, col2, col3 = st.columns([2.5, 1, 2.5])
    with col2:
        highlight_selected = st.checkbox("Highlight My Clubs")

    if highlight_selected:
        for club in color_map.keys():
            if club not in selected_teams:
                color_map[club] = "#a9a9a9"
    else:
        for club in color_map.keys():
            color_map[club] = df.loc[df['club'] == club, 'color'].values[0]


    fig_value = px.treemap(df, path=["club"], values="value", title="Club Values",
                           color="club", color_discrete_map=color_map)
    fig_value.update_layout(title_font_size=24)
    st.plotly_chart(fig_value)


    fig_revenue = px.bar(df.sort_values("revenue", ascending=True),
                         x="revenue", y="club", title="Season Revenue",
                         labels={"revenue": "Revenue", "club": "Club"},
                         orientation="h", text_auto=True, color="club", color_discrete_map=color_map)
    fig_revenue.update_layout(title_font_size=24)
    st.plotly_chart(fig_revenue)


    fig_attendance = px.scatter(df.sort_values("attendance", ascending=False),
                                x="attendance", y="club", title="Cumulative Match Attendance",
                                labels={"attendance": "Attendance", "club": "Club"},
                                color="club", size="attendance", color_discrete_map=color_map,
                                size_max=10)
    fig_attendance.update_layout(title_font_size=24)
    st.plotly_chart(fig_attendance)


    fig_payroll = px.bar(df.sort_values("payroll", ascending=True),
                         x="payroll", y="club", title="Roster Payroll",
                         labels={"payroll": "Payroll", "club": "Club"},
                         orientation="h", text_auto=True, color="club", color_discrete_map=color_map)
    fig_payroll.update_layout(title_font_size=24)
    st.plotly_chart(fig_payroll)
