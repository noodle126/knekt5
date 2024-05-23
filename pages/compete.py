import streamlit as st
import pandas as pd
import csv
import json
from streamlit_option_menu import option_menu
import components.all as ac
import threading
import time
from datetime import datetime
from streamlit_card import card

ac.hideSideBar()
ac.topHeader()


st.write("this is the page is about the quizs and ways to collect points")

col1, col2, col3 = st.columns([1,1,1])    
with col1:
      hasClicked = card(title="IQ", text="Individual Quizzes", image="https://raw.githubusercontent.com/noodle126/knekt5/main/images/individual.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "100%", "height": "100%"}}
                                ) 
with col2:
      hasClicked = card(title="1V1", text="1v1 Quizzes", image="https://raw.githubusercontent.com/noodle126/knekt5/main/images/individualteam.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "100%", "height": "100%"}}
                                )
with col3:
      hasClicked = card(title="P", text="Predictions", image="https://raw.githubusercontent.com/noodle126/knekt5/main/images/knekt_logo.png", url="https://www.bbc.co.uk/",
                        styles={"card": {"width": "100%", "height": "100%"}}
                                )

# Read questions from the CSV file
questions_df = pd.read_csv("/workspaces/knekt5/data/questions.csv")

# Group questions by topic
questions_by_topic = {}
for topic in questions_df["Topic"].unique():
    questions_by_topic[topic] = tuple(questions_df[questions_df["Topic"] == topic].to_dict(orient="records"))

def display_time():
    st.write(f"Time of day: {datetime.now().strftime('%H:%M:%S')}")

# Function to reset session state
def reset_state():
    st.session_state.clear()

# Main page: Quiz Selection
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "selection"
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'countdown_seconds' not in st.session_state:
        st.session_state.countdown_seconds = 5
    if 'countdown_active' not in st.session_state:
        st.session_state.countdown_active = False

    if st.session_state.page == "selection":
        show_quiz_selection()
    elif st.session_state.page == "quiz":
        show_quiz_page(st.session_state.selected_topic)
    elif st.session_state.page == "results":
        show_results()
    
    # st.title("Time of Day Display")
    # time_placeholder = st.empty()  # Create an empty placeholder for time display
    # while True:
    #     display_time()
    #     time.sleep(1)

def show_quiz_selection():
    st.title("Quiz Selection")
    selected_topic = st.selectbox("Choose a topic", [""] + list(questions_by_topic.keys()))

    if selected_topic:
        st.session_state.selected_topic = selected_topic
        st.session_state.user_answers = [""] * len(questions_by_topic[selected_topic])
        st.session_state.page = "quiz"
        st.experimental_rerun()

def show_quiz_page(selected_topic):
    questions = questions_by_topic[selected_topic]
    current_question = st.session_state.current_question

    if st.session_state.current_question < len(questions):
        display_question(current_question, questions)
    else:
        st.session_state.page = "results"
        st.experimental_rerun()

def display_question(index, questions):
    st.subheader(f"Question {index + 1}:")
    question = questions[index]
    options = [question["Answer A"], question["Answer B"], question["Answer C"], question["Answer D"]]
    st.session_state.user_answers[index] = st.radio(question["Question"], options, index=options.index(st.session_state.user_answers[index]) if st.session_state.user_answers[index] else 0)

    next_button_placeholder = st.empty()

    # Start or resume countdown timer
    if not st.session_state.countdown_active:
        st.session_state.countdown_seconds = 5
        st.session_state.countdown_active = True
        countdown_thread = threading.Thread(target=countdown, args=(next_button_placeholder,), daemon=True)
        countdown_thread.start()
    else:
        countdown_thread = threading.Thread(target=countdown, args=(next_button_placeholder,), daemon=True)
        countdown_thread.start()

    if next_button_placeholder.button("Next"):
        st.session_state.current_question += 1
        st.session_state.countdown_active = False
        st.experimental_rerun()

    st.write(f"Time remaining: {st.session_state.countdown_seconds} seconds")

def countdown(next_button_placeholder):
    while st.session_state.countdown_seconds > 0 and st.session_state.countdown_active:
        st.session_state.countdown_seconds -= 1
        time.sleep(1)
        st.experimental_rerun()  # Update the time remaining every second
    if st.session_state.countdown_active:
        next_button_placeholder.click()

def show_results():
    selected_topic = st.session_state.selected_topic
    questions = questions_by_topic[selected_topic]
    user_answers = st.session_state.user_answers

    correct_answers = [q["Correct Answer"] for q in questions]
    score = sum([1 for i, ans in enumerate(user_answers) if ans == correct_answers[i]])
    st.subheader("Results:")
    st.write(f"Your scored {score} out of {len(questions)}")

    st.subheader("Correct Answers:")
    for i, q in enumerate(questions):
        st.write(f"Question {i + 1}: {q['Correct Answer']}")

    if st.button("Back to Quiz Selection"):
        reset_state()
        st.session_state.page = "selection"
        st.experimental_rerun()

    if not st.session_state.get('results_written'):
        with open('user_results.csv', mode='a', newline='') as file:
            fieldnames = ['Question IDs', 'Total Score']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            question_ids_str = json.dumps([{"Question ID": q["ID"], "Correct": user_answers[i] == q["Correct Answer"]} for i, q in enumerate(questions)])
            writer.writerow({'Question IDs': question_ids_str, 'Total Score': score})
        st.session_state.results_written = True

# Run the app
if __name__ == "__main__":
    main()