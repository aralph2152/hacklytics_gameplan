# packages
import streamlit as st
import pandas as pd

def app():

    club_data = pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\rosters_2024\clubs.csv")
    club_logos = pd.Series(club_data.logo.values, index=club_data.club).to_dict()
    clubs = list(club_logos.keys())


    if "selected_clubs" not in st.session_state:
        st.session_state.selected_clubs = ["", "", ""]

    st.markdown(
        "<h1 style='text-align: center; font-style: italic; color: #a9a9a9;'>So, what's your "
        "<span style='font-weight: bold; font-style: normal; color: #ffffff;'>GamePlan</span>"
        "<span style='font-style: normal; color: #ffffff;'>?</span></h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h4 style='text-align: center; color: #a9a9a9;'>To get started, select 3 MLS clubs.</h4>",
        unsafe_allow_html=True,
    )


    col1, col2, col3 = st.columns(3)

    with col1:
        club1 = st.selectbox("", ["Select a club"] + clubs, key="club1")

    with col2:
        club2 = st.selectbox("", ["Select a club"] + clubs, key="club2")

    with col3:
        club3 = st.selectbox("", ["Select a club"] + clubs, key="club3")


    selected_clubs = [club for club in [club1, club2, club3] if club != "Select a club"]
    st.session_state.selected_clubs = selected_clubs

    st.markdown("<br>", unsafe_allow_html=True)

    if len(selected_clubs) == 3:

        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]

        for i, club in enumerate(st.session_state.selected_clubs):
            logo_url = club_logos.get(club, "").strip()

            with columns[i]:
                if logo_url and logo_url.startswith("http"):
                    st.markdown(f"<p style='text-align: center;'><img src='{logo_url}' width='100'></p>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='text-align: center;'>{club}</h5>", unsafe_allow_html=True)

    if len(selected_clubs) == 3:
        st.markdown(
            "<h4 style='text-align: center; color: #a9a9a9;'><br>Great choices! Now, view your financial data, <br>roster statistics, match-up predictions, and the playbook <br>using the navigation bar.</h4>",
            unsafe_allow_html=True,
        )