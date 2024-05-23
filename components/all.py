import streamlit as st

def topHeader():
    st.image('images/knekt_small_logo.png')
    st.header('Sonny Webster, 1220340000 rings', divider='rainbow')
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    
    with col1:
        st.page_link("pages/home.py", label="Home", icon=None)
    with col2:
        st.page_link("pages/buildTeam.py", label="Teams", icon=None)
    with col3:
        st.page_link("pages/engage.py", label="Engage", icon=None)
    with col4:
        st.page_link("pages/compete.py", label="Compete", icon=None)
    with col5:
        st.page_link("pages/community.py", label="Community", icon=None)


def hideSideBar():
    st.set_page_config(initial_sidebar_state="collapsed")
    st.markdown( """ <style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True,)
