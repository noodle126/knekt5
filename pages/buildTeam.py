import streamlit as st
import components.all as ac
from streamlit_card import card

ac.topHeader()

st.write("this is the page to build and manage teams")

col1, col2, col3 = st.columns([1,1,1])
    
with col1:
      hasClicked = card(title="Join as an individual", text="Some description", image="/images/knekt_small_logo.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "100%", "height": "100%"}}
                                )   
with col2:
      hasClicked = card(title="Join individual team", text="Some description", image="/images/knekt_small_logo.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "100%", "height": "100%"}}
                                )
with col3:
      hasClicked = card(title="Join as a global team", text="Some description", image="/images/knekt_small_logo.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "100%", "height": "100%"}}
                                )