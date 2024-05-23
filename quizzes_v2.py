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

# Main page: Quiz Selection
def main():
    title_placeholder = st.empty()
    selectbox_placeholder = st.empty()
    
    title_placeholder.title("Quiz Selection")
    selected_topic = selectbox_placeholder.selectbox("Choose a topic", [""] + list(questions_by_topic.keys()))

    if selected_topic:
        # Navigate to the quiz page
        quiz_page(selected_topic)
        title_placeholder.empty()  # Hide the title
        selectbox_placeholder.empty()  # Hide the selectbox

def quiz_page(selected_topic):
    questions = questions_by_topic[selected_topic]

    # Initialize session state variables
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = [""] * len(questions)
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'back_to_selection_clicked' not in st.session_state:
        st.session_state.back_to_selection_clicked = False

    # Sidebar menu for navigation
    with st.sidebar:
        selected = option_menu(
            "Question Navigation",
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
        if st.session_state.submitted:
            # Display score and correct answers
            correct_answers = [q["Correct Answer"] for q in questions]
            score = sum([1 for i, ans in enumerate(st.session_state.user_answers) if ans == correct_answers[i]])
            st.subheader("Results:")
            st.write(f"Your scored {score} out of {len(questions)}")
            
            st.subheader("Correct Answers:")
            for i, q in enumerate(questions):
                st.write(f"Question {i + 1}: {q['Correct Answer']}")

            # Button to go back to quiz selection
            if st.button("Back to Quiz Selection"):
                st.session_state.back_to_selection_clicked = True
                st.session_state.submitted = False
                st.experimental_rerun()  # Redirect to the quiz selection page
        else:
            st.session_state.submitted = True
            st.experimental_rerun()  # Redirect to the submit page

            # Display a message
            st.write("Thank you for taking the quiz!")

    # Write user's results to CSV only if the quiz is submitted
    if st.session_state.submitted and not st.session_state.back_to_selection_clicked:
        with open('user_results.csv', mode='a', newline='') as file:
            fieldnames = ['Question IDs', 'Total Score']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Serialize question IDs and correctness to a JSON string
            question_ids_str = json.dumps([{"Question ID": q["ID"], "Correct": st.session_state.user_answers[i] == q["Correct Answer"]} for i, q in enumerate(questions)])
            
            writer.writerow({'Question IDs': question_ids_str, 'Total Score': score})


# Run the app
if __name__ == "__main__":
    main()