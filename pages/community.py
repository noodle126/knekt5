import streamlit as st
import components.all as ac
import os
from datetime import datetime
ac.hideSideBar()
ac.topHeader()

# Title of the app
st.title("Community Paris Olympics")

# Description of the event
st.header("YOUR FEED")
st.subheader("Show your support")
st.write("""
Welcome to the discussion app for Paris Olympics . This is a place where attendees can share their thoughts, insights and predictions.
""")

# User input section
st.header("Share Your Thoughts")
user_name = st.text_input("Name", "")
user_comment = st.text_area("Comment", "")
submit_button = st.button("Submit")


st.subheader("Upload a video or picture and join the discussion!")

uploaded_file = st.file_uploader("Choose a video or image file", type=["mp4", "avi", "mov", "mkv", "jpg", "jpeg", "png", "gif"])

# Initialize session state for comments and votes
if 'comments' not in st.session_state:
    st.session_state.comments = []

if 'votes' not in st.session_state:
    st.session_state.votes = []

# Handle the submission
if submit_button:
    if user_name and user_comment:
        new_comment = {
            'name': user_name,
            'comment': user_comment,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'id': len(st.session_state.comments)
        }
        st.session_state.comments.append(new_comment)
        st.session_state.votes.append(0)  # Initialize vote count for new comment
        st.success("Thank you for your comment!")
    else:
        st.error("Please fill in both your name and comment.")

# Display comments with upvote/downvote buttons
st.header("Comments")
if st.session_state.comments:
    for i, comment in enumerate(st.session_state.comments):
        st.write(f"**{comment['name']}** ({comment['timestamp']}):")
        st.write(f"{comment['comment']}")
        cols = st.columns(3)
        with cols[0]:
            if st.button(f"Upvote {i}", key=f"upvote_{i}"):
                st.session_state.votes[i] += 1
        with cols[1]:
            if st.button(f"Downvote {i}", key=f"downvote_{i}"):
                st.session_state.votes[i] -= 1
        with cols[2]:
            st.write(f"Votes: {st.session_state.votes[i]}")
        st.write("---")
else:
    st.write("No comments yet. Be the first to share your thoughts!")

st.header("Suggestions for you!")
st.write(" Share your score!")
st.page_link("pages/stats.py", label="Stats by country, athlete and sport", icon=None)
# st.page_link("pages/stats.py", label="Stats by country, athlete and sport", icon=None)


