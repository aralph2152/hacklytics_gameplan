# packages
import streamlit as st
import pandas as pd

# Load roster file paths from Excel
@st.cache_data
def load_roster_paths():
    roster_paths = pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\rosters_2024\roster_paths.csv")
    return roster_paths.set_index("club")["path"].to_dict()  # Convert to dictionary {team: file_path}

# Load team data dynamically
def load_team_data(team, paths_dict):
    if team in paths_dict:
        file_path = paths_dict[team]
        try:
            df = pd.read_csv(file_path, encoding="utf-8")  # Specify encoding
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="ISO-8859-1")  # Try alternate encoding if utf-8 fails
        return df
    return None  # If team file is missing

def app():
    st.title("Welcome to the Locker Room!")

    # Load roster file paths
    roster_paths = load_roster_paths()

    # Get selected teams from session state
    selected_teams = st.session_state.get("selected_clubs", [])

    # Ensure there are selected teams
    if not selected_teams:
        st.warning("Please select teams on the home page.")
        return

    # Create tabs for each team
    tabs = st.tabs(selected_teams)

    for tab, team in zip(tabs, selected_teams):
        with tab:
            df = load_team_data(team, roster_paths)

            if df is None:
                st.error(f"Roster data for {team} not found.")
                continue

            # Display full team stats
            st.write(f"### {team} - Full Team Stats:")
            st.dataframe(df, use_container_width=True)

            # Player selection
            st.write("### Select a Player to View Details:")
            selected_player = st.selectbox(f"Choose a player ({team}):", df["player"], key=f"player_{team}")

            # Display player details
            player_data = df[df["player"] == selected_player].iloc[0]

            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(player_data["photo"], use_container_width=True)  # Load player photo from CSV

            with col2:
                st.subheader(f"{player_data['player']} - #{player_data['jersey']}")
                st.write(f"**Position:** {player_data['position']}")
                st.write(f"**Games Played:** {player_data['games_played']}")
                st.write(f"**Games Started:** {player_data['games_started']}")
                st.write(f"**Minutes:** {player_data['minutes']}")

                position = player_data['position'].lower()
                if position == 'forward':
                    st.write(f"**Goals:** {player_data['goals']}")
                    st.write(f"**Assists:** {player_data['assists']}")
                    st.write(f"**Attempts on Goal:** {player_data['scoring_attempts']}")
                    st.write(f"**Passes:** {player_data['passes']}")
                    st.write(f"**Pass Attempts:** {player_data['pass_attempts']}")
                elif position in ['defender', 'midfielder']:
                    st.write(f"**Assists:** {player_data['assists']}")
                    st.write(f"**Passes:** {player_data['passes']}")
                    st.write(f"**Pass Attempts:** {player_data['pass_attempts']}")
                elif position == 'goalkeeper':
                    st.write(f"**Clean Sheets:** {player_data['clean_sheet']}")
                    st.write(f"**Goals Against:** {player_data['goals_against']}")
                    st.write(f"**Goals Saved:** {player_data['goals_saved']}")