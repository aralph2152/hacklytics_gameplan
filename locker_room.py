# packages
import streamlit as st
import pandas as pd
import plotly.express as px

# page function: choose team, load player and team stats

# load data
def load_data():
    file_path = r"C:\Users\aralp\Desktop\GamePlan\rosters_2024\miami_2024.xlsx"
    df = pd.read_excel(file_path)
    return df


def app():
    st.title("locker room")

    # Load Data
    df = load_data()

    # display as interactive table
    st.write("### Full Team Stats:")
    st.dataframe(df, use_container_width=True)

    # Select a player from the table
    st.write("### Select a Player to View Details:")
    selected_player = st.selectbox("Choose a player:", df["player"])

    # Display Player Details
    player_data = df[df["player"] == selected_player].iloc[0]

    # Profile layout
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(r"C:\Users\aralp\Desktop\GamePlan\rosters_2024\miami_img.jpg", use_container_width=True)  # Placeholder

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