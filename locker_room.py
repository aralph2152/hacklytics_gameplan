# packages
import streamlit as st
import pandas as pd

@st.cache_data
def load_roster_paths():
    roster_paths = pd.read_csv(r"C:\Users\aralp\Desktop\GamePlan\rosters_2024\roster_paths.csv")
    return roster_paths.set_index("club")["path"].to_dict()  # Convert to dictionary {team: file_path}

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
    st.markdown(
        "<h1 style='text-align: center; font-style: italic;'>Start, Bench, Cut? It's up to you, Coach.</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h4 style='text-align: center;'>Check out your roster in the Locker Room.</h4>",
        unsafe_allow_html=True,
    )

    roster_paths = load_roster_paths()

    selected_teams = st.session_state.get("selected_clubs", [])

    if not selected_teams:
        st.warning("Please select teams on the home page.")
        return

    tabs = st.tabs(selected_teams)

    for tab, team in zip(tabs, selected_teams):
        with tab:
            df = load_team_data(team, roster_paths)

            if df is None:
                st.error(f"Roster data for {team} not found.")
                continue

            cols = st.columns(4)
            for idx, player_data in df.iterrows():
                col = cols[idx % 4]
                with col:
                    st.subheader(f"{player_data['player']}  #{player_data['jersey']}")
                    st.image(player_data.get("photo"), use_container_width=True)
                    st.write(f"**Position:** {player_data['position']}")
                    st.write(f"**Games Played:** {player_data['games_played']}")
                    st.write(f"**Games Started:** {player_data['games_started']}")
                    st.write(f"**Minutes:** {player_data['minutes']}")

                    position = player_data['position']
                    if position == 'Forward':
                        st.write(f"**Goals:** {player_data['goals']}")
                        st.write(f"**Assists:** {player_data['assists']}")
                        st.write(f"**Attempts on Goal:** {player_data['scoring_attempts']}")
                        st.write(f"**Passes:** {player_data['passes']}")
                        st.write(f"**Pass Attempts:** {player_data['pass_attempts']}")
                        st.markdown("<p>&nbsp;</p>", unsafe_allow_html=True)
                    elif position in ['Defender', 'Midfielder']:
                        st.write(f"**Assists:** {player_data['assists']}")
                        st.write(f"**Passes:** {player_data['passes']}")
                        st.write(f"**Pass Attempts:** {player_data['pass_attempts']}")
                        st.markdown("<p>&nbsp;</p>", unsafe_allow_html=True)
                        st.markdown("<p>&nbsp;</p>", unsafe_allow_html=True)
                        st.markdown("<p>&nbsp;</p>", unsafe_allow_html=True)
                    elif position == 'Goalkeeper':
                        st.write(f"**Clean Sheets:** {player_data['clean_sheet']}")
                        st.write(f"**Goals Against:** {player_data['goals_against']}")
                        st.write(f"**Goals Saved:** {player_data['goals_saved']}")
                        st.markdown("<p>&nbsp;</p>", unsafe_allow_html=True)
                        st.markdown("<p>&nbsp;</p>", unsafe_allow_html=True)
                        st.markdown("<p>&nbsp;</p>", unsafe_allow_html=True)

            st.write(f"### {team} - Full Team Stats:")
            st.dataframe(df, use_container_width=True)