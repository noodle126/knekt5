import streamlit as st
from streamlit.components.v1 import html
import pages.home as home
import pages.buildTeam as buildteam

# common functionality
def remove_side_bar():
    st.set_page_config(initial_sidebar_state="collapsed") 
    st.markdown( """ <style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True,)

remove_side_bar()

PAGES = {
    "Home": home,
    "BuildTeams": buildteam
}

def topHeader():
    st.header('Sonny Webster, 1220340000 rings', divider='rainbow')
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        st.page_link("pages/home.py", label="Home", icon=None)
    with col2:
        st.page_link("pages/buildTeam.py", label="Build Team", icon=None)
    with col3:
        st.page_link("pages/buildTeam.py", label="Build Team", icon=None)

topHeader()