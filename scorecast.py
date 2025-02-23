import streamlit as st
import pandas as pd
import plotly.express as px

def load_roster_data():
    roster_paths = pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\rosters_2024\roster_paths.csv")
    club_rosters = {}
    for _, row in roster_paths.iterrows():
        club = row['club']
        file_path = row['path']
        try:
            club_rosters[club] = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            try:
                club_rosters[club] = pd.read_csv(file_path, encoding="ISO-8859-1")
            except Exception as e:
                st.error(f"Error loading roster for {club}: {e}")
    return club_rosters

def predict_match(team1, team2, rosters):
    if team1 not in rosters or team2 not in rosters:
        return None, None

    def calculate_team_strength(team_df):
        return (
                team_df['goals'].sum() * 3 +
                team_df['assists'].sum() * 2 +
                team_df['minutes'].sum() / 1000
        )

    strength1 = calculate_team_strength(rosters[team1])
    strength2 = calculate_team_strength(rosters[team2])

    total = strength1 + strength2
    if total == 0:
        return 50, 50

    prob_team1 = round((strength1 / total) * 100, 1)
    prob_team2 = round((strength2 / total) * 100, 1)
    return prob_team1, prob_team2

def app():
    st.markdown(
        "<h1 style='text-align: center; font-style: italic;'>They never saw it coming.</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h4 style='text-align: center;'>Good thing you have ScoreCast.</h4>",
        unsafe_allow_html=True,
    )

    rosters = load_roster_data()
    selected_teams = st.session_state.get("selected_clubs", [])

    if len(selected_teams) < 2:
        st.warning("Please select at least two teams on the home page.")
        return

    df = pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\money_2024\mls_finances.csv")
    color_map = {club: color for club, color in sorted(df.set_index('club')['color'].items())}

    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Select First Team", selected_teams)
    with col2:
        team2 = st.selectbox("Select Second Team", [t for t in selected_teams if t != team1])

    if team1 and team2:
        prob1, prob2 = predict_match(team1, team2, rosters)

        fig = px.bar(
            x=[team1, team2],
            y=[prob1, prob2],
            labels={'x': "Team", 'y': "Win Probability (%)"},
            title="Match Win Probability",
            text=[f"{prob1}%", f"{prob2}%"],
            color=[team1, team2],
            color_discrete_map=color_map
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig)

    st.markdown("### Key Players to Watch")
    for team in [team1, team2]:
        st.subheader(f"Top Performers - {team}")
        if team in rosters:
            top_players = rosters[team].nlargest(3, 'goals')
            st.dataframe(top_players[['player', 'goals', 'assists', 'minutes']], use_container_width=True)
        else:
            st.warning(f"No data available for {team}.")

    st.markdown("""
        <h5>Predictions are based on cumulative player statistics.</h5>
    """, unsafe_allow_html=True)
