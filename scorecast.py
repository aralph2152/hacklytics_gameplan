import streamlit as st
import pandas as pd
import random
import plotly.express as px


def load_roster_paths():
    roster_paths = pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\rosters_2024\roster_paths.csv")
    return roster_paths.set_index("club")["path"].to_dict()


def load_team_data(team, paths_dict):
    if team in paths_dict:
        file_path = paths_dict[team]
        try:
            df = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="ISO-8859-1")
        return df
    return None


def generate_random_11(selected_teams, formation, roster_paths):
    all_players = []
    for team in selected_teams:
        df = load_team_data(team, roster_paths)
        if df is not None:
            df = df[df['jersey'].apply(lambda x: str(x).isdigit())]  # Filter players with numerical jersey values
            all_players.extend(df.to_dict('records'))

    if len(all_players) < 11:
        return []

    positions = {
        "5-3-2": {"Goalkeeper": 1, "Defender": 5, "Midfielder": 3, "Forward": 2},
        "4-4-2": {"Goalkeeper": 1, "Defender": 4, "Midfielder": 4, "Forward": 2},
        "4-3-3": {"Goalkeeper": 1, "Defender": 4, "Midfielder": 3, "Forward": 3}
    }

    squad = []
    for position, count in positions[formation].items():
        players_in_position = [p for p in all_players if p["position"] == position]
        squad.extend(random.sample(players_in_position, min(count, len(players_in_position))))

    return squad


def generate_team_stats(squad):
    if not squad:
        return None

    # Compute team-level aggregated stats
    goals = sum(player.get("goals", 0) for player in squad)
    assists = sum(player.get("assists", 0) for player in squad)
    passes = sum(player.get("passes", 0) for player in squad)
    pass_accuracy = round(
        sum(player.get("passes", 0) / max(player.get("pass_attempts", 1), 1) for player in squad) / len(squad) * 100, 2
    )
    clean_sheets = sum(player.get("clean_sheet", 0) for player in squad if player["position"] == "Goalkeeper")
    goals_against = sum(player.get("goals_against", 0) for player in squad if player["position"] == "Goalkeeper")

    # Compute Team Strength Index (TSI) with weights
    TSI = (
            (2.0 * goals) +
            (2.0 * assists) +
            (1.5 * pass_accuracy) +
            (1.8 * clean_sheets) -
            (1.5 * goals_against)
    )

    return {
        "Goals": goals,
        "Assists": assists,
        "Pass Accuracy (%)": pass_accuracy,
        "Clean Sheets": clean_sheets,
        "Goals Against": goals_against,
        "Team Strength Index (TSI)": round(TSI, 2)
    }


def app():
    st.title("Random Team Generator & Strength Analysis")

    if "squad" in st.session_state:
        squad = st.session_state.squad
        team_stats = generate_team_stats(squad)

        if team_stats:
            df_stats = pd.DataFrame.from_dict(team_stats, orient='index', columns=['Value'])
            st.dataframe(df_stats)

            fig = px.bar(df_stats, x=df_stats.index, y='Value', title="Team Performance Metrics", text_auto=True)
            st.plotly_chart(fig)
        else:
            st.error("Could not generate team stats.")
