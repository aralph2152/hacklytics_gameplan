# packages
import streamlit as st

# import additional pages
import home
import box_office
import locker_room
import scorecast
import play_book

st.set_page_config(page_title="GamePlan", layout="wide")

st.image(r"C:\Users\aralp\Desktop\GamePlan\banner.jpg", use_container_width=True)

st.markdown("""
    <style>
        
        div.stButton > button {
            width: 100%;
            background-color: #dcdcdc; 
            color: black !important; 
            border-radius: 10px;
            padding: 10px;
            border: none;
            font-size: 18px;
        }
        div.stButton > button:hover {
            background-color: #a9a9a9; 
            color: black !important; 
        }
        div.stButton > button:focus, 
        div.stButton > button:active {
            outline: none !important;
            box-shadow: none !important;
            border-color: transparent !important;
            background-color: #a9a9a9 !important; 
            color: black !important; 
        }

        div[data-baseweb="select"] * {
            outline: none !important;
            box-shadow: none !important;
            border-color: transparent !important;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

if col1.button("GamePlan"):
    st.session_state["page"] = "GamePlan"
if col2.button("Box Office"):
    st.session_state["page"] = "Box Office"
if col3.button("Locker Room"):
    st.session_state["page"] = "Locker Room"
if col4.button("ScoreCast"):
    st.session_state["page"] = "ScoreCast"
if col5.button("Play Book"):
    st.session_state["page"] = "Play Book"

if "page" not in st.session_state:
    st.session_state["page"] = "GamePlan"

if st.session_state["page"] == "GamePlan":
    home.app()
elif st.session_state["page"] == "Box Office":
    box_office.app()
elif st.session_state["page"] == "Locker Room":
    locker_room.app()
elif st.session_state["page"] == "ScoreCast":
    scorecast.app()
elif st.session_state["page"] == "Play Book":
    play_book.app()
