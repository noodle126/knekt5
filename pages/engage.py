import streamlit as st
import components.all as ac

ac.topHeader()


st.write("this is the page to leanr more about stuff")

def is_logged_in():
    SESSION_DATA_FILE = "session_data.csv"

    # Check if session_token exists in session_state
    if not hasattr(st.session_state, 'session_token'):
        print('No session token found in session state')
        return

    token_found = False  # Initialize a flag to track if the token is found

    try:
        with open(SESSION_DATA_FILE, "r") as f:
            for line in f:
                username, token = line.strip().split(",")
                if token == st.session_state.session_token:
                    print('logged in')
                    token_found = True  # Set the flag to True if a match is found
                    break  # Exit the loop since the token is found
    except FileNotFoundError:
        print('Session data file not found')
        return

    if not token_found:
        print('No matching token found')

# Example of setting up session state
if 'session_token' not in st.session_state:
    st.session_state.session_token = None  # Initialize it to None or some default value

# Call the function to check login status
is_logged_in()