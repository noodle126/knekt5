import streamlit as st
import pandas as pd
import csv
import json
from streamlit_option_menu import option_menu
import components.all as ac


ac.topHeader()

# Read questions from the CSV file
questions_df = pd.read_csv("questions.csv")

# Group questions by topic
questions_by_topic = {}
for topic in questions_df["Topic"].unique():
    questions_by_topic[topic] = tuple(questions_df[questions_df["Topic"] == topic].to_dict(orient="records"))

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

    if st.session_state.page == "selection":
        show_quiz_selection()
    elif st.session_state.page == "quiz":
        show_quiz_page(st.session_state.selected_topic)
    elif st.session_state.page == "results":
        show_results()

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

    if st.button("Next"):
        st.session_state.current_question += 1
        st.experimental_rerun()

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