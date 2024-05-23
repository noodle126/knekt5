import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Read questions from the CSV file
questions_df = pd.read_csv("questions.csv")

# Group questions by topic
questions_by_topic = {}
for topic in questions_df["Topic"].unique():
    questions_by_topic[topic] = tuple(questions_df[questions_df["Topic"] == topic].to_dict(orient="records"))

# Main page: Quiz Selection
def main():
    st.title("Quiz Selection")
    selected_topic = st.selectbox("Choose a topic", [""] + list(questions_by_topic.keys()))

    if selected_topic:
        # Navigate to the quiz page
        quiz_page(selected_topic)

# Single Quiz Page
def quiz_page(selected_topic):
    questions = questions_by_topic[selected_topic]

    # Initialize session state variables
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = [""] * len(questions)
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # Sidebar menu for navigation
    with st.sidebar:
        selected = option_menu(
            "Quiz Navigation",
            options=[f"Question {i+1}" for i in range(len(questions))] + ["Submit"],
            default_index=0,
            orientation="vertical"
        )

    # Determine the current question based on the sidebar selection
    current_question = int(selected.split()[-1]) - 1 if selected != "Submit" else None

    # Function to display the current question
    def display_question(index):
        st.subheader(f"Question {index + 1}:")
        answer_options = [questions[index]["Answer A"], questions[index]["Answer B"], questions[index]["Answer C"], questions[index]["Answer D"]]
        st.session_state.user_answers[index] = st.radio(questions[index]["Question"], answer_options, key=f"q{index}", index=answer_options.index(st.session_state.user_answers[index]) if st.session_state.user_answers[index] else 0)

    # Display the current question
    if current_question is not None:
        display_question(current_question)
    else:
        st.session_state.submitted = True

    # Calculate and display the score if submitted
    if st.session_state.submitted:
        correct_answers = [q["Correct Answer"] for q in questions]
        score = sum([1 for i, ans in enumerate(st.session_state.user_answers) if ans == correct_answers[i]])
        st.write(f"Your score: {score} out of {len(questions)}")
        
        # Display correct answers
        st.subheader("Correct Answers:")
        for i, q in enumerate(questions):
            st.write(f"Question {i + 1}: {q['Correct Answer']}")

        # Display a message
        st.write("Thank you for taking the quiz!")

# Run the app
if __name__ == "__main__":
    main()