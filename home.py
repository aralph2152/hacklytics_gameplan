# packages
import streamlit as st
import pandas as pd

st.set_page_config(page_title="MLS Team Selector", layout="wide")

def app():

    club_data = pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\rosters_2024\clubs.csv")
    club_logos = pd.Series(club_data.logo.values, index=club_data.club).to_dict()
    clubs = list(club_logos.keys())


    if "selected_teams" not in st.session_state:
        st.session_state.selected_teams = ["", "", ""]


    st.markdown(
        "<h1 style='text-align: center; font-style: italic;'>So, what's the "
        "<span style='font-weight: bold; font-style: normal; color: #FF5733;'>GamePlan</span>"
        "<span style='font-style: normal; color: #FF5733;'>?</span></h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h4 style='text-align: center; font-style: italic;'>To get started, select 3 MLS clubs.</h4>",
        unsafe_allow_html=True,
    )


    col1, col2, col3 = st.columns(3)

    with col1:
        club1 = st.selectbox("Club 1", ["Select a club"] + clubs, key="club1")

    with col2:
        club2 = st.selectbox("Club 2", ["Select a club"] + clubs, key="club2")

    with col3:
        club3 = st.selectbox("Club 3", ["Select a club"] + clubs, key="club3")


    selected_teams = [club for club in [club1, club2, club3] if club != "Select a club"]
    st.session_state.selected_teams = selected_teams


    if len(selected_teams) == 3:
        st.subheader("Your Selected Teams:")

        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]

        for i, club in enumerate(st.session_state.selected_teams):
            logo_url = club_logos.get(club, "").strip()

            with columns[i]:
                if logo_url and logo_url.startswith("http"):
                    st.image(logo_url, width=100)
                st.write(f"**{club}**")