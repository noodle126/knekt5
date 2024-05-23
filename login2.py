import streamlit as st
import pandas as pd
import hashlib
import secrets  # For generating cryptographically secure tokens
import components.all as ac

# Load user data from CSV
USER_DATA_FILE = "user_data.csv"
user_data = pd.read_csv(USER_DATA_FILE)

# Load session data from CSV
SESSION_DATA_FILE = "session_data.csv"

def hash_password(password):
    # Hash the password using SHA-256 algorithm
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    # Generate a cryptographically secure session token
    return secrets.token_hex(16)

def login(username, password):
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
    with open(SESSION_DATA_FILE, "r") as f:
        for line in f:
            username, token = line.strip().split(",")
            if token == session_token:
                return True
    return False

def main():
    ac.topHeader()
    st.title("Login")

    if "session_token" in st.session_state and is_logged_in(st.session_state.session_token):
        st.success("You are already logged in.")
        st.write("Welcome to the application!")
    else:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            session_token = login(username, password)
            if session_token:
                st.session_state.session_token = session_token
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

if __name__ == "__main__":
    main()