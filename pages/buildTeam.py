import streamlit as st
import components.all as ac
from streamlit_card import card

ac.hideSideBar()
ac.topHeader()

st.write("this is the page to build and manage teams")

col1, col2, col3 = st.columns([1,1,1])    
with col1:
      hasClicked = card(title="I", text="Individual", image="https://raw.githubusercontent.com/noodle126/knekt5/images/individual.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "150px", "height": "150px"}}
                                )   
with col2:
      hasClicked = card(title="IT", text="Individual Team", image="https://raw.githubusercontent.com/noodle126/knekt5/main/images/individualteam.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "100%", "height": "100%"}}
                                )
with col3:
      hasClicked = card(title="GT", text="Global Team", image="https://raw.githubusercontent.com/noodle126/knekt5/main/images/knekt_logo.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "100%", "height": "100%"}}
                                )
      

