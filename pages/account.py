import streamlit as st
import pandas as pd
import hashlib
import secrets  # For generating cryptographically secure tokens
import components.all as ac

# Load user data from CSV
USER_DATA_FILE = "/data/out/tables/USERS.csv"
user_data = pd.read_csv(USER_DATA_FILE)

def hash_password(password):
    # Hash the password using SHA-256 algorithm
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    # Generate a cryptographically secure session token
    return secrets.token_hex(16)

def login(username, password):
    SESSION_DATA_FILE = "/data/out/tables/SESSION_DATA.csv"
    if (user_data['username'] == username).any():
        user_row = user_data[user_data['username'] == username].iloc[0]
        hashed_password = user_row.iloc[1]
        if hashed_password == hash_password(password):
            # Generate and store session token
            session_token = generate_session_token()
            with open(SESSION_DATA_FILE, "a") as f:
                f.write(f"{username},{session_token}\n")
            return session_token
    return None

def is_logged_in(session_token):
    SESSION_DATA_FILE = "/data/out/tables/SESSION_DATA.csv"
    with open(SESSION_DATA_FILE, "r") as f:
        for line in f:
            username, token = line.strip().split(",")
            if token == session_token:
                return True
    return False

def main():
    ac.topHeader()

    if "session_token" in st.session_state and is_logged_in(st.session_state.session_token):
        st.title("Account")
        st.success("You are already logged in.")
        st.write("Welcome to the application!")
        if st.button("Logout"):
            st.session_state.pop("session_token")
            st.experimental_rerun()  # To refresh the page after logout
    else:
        st.title("Account")
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            session_token = login(username, password)
            if session_token:
                st.session_state.session_token = session_token
                st.success("Login successful!")
                st.experimental_rerun()  # To refresh the page after login
            else:
                st.error("Invalid username or password")

if __name__ == "__main__":
    main()