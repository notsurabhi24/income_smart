import streamlit as st
import pandas as pd
import joblib
import mysql.connector

# Load model and encoders
try:
    model = joblib.load('models/income_model.pkl')
    le_dict = joblib.load('models/label_encoders.pkl')
except Exception as e:
    st.error("Model files not found.")
    st.stop()

# DB connection function
def get_db_connection():
    return mysql.connector.connect(
        host="Surabhi",
        user="root",
        password="Goldy@2406",
        database="income_prediction"
    )

# Check login
if 'user' not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

st.title("🃏 Income Prediction Flashcards")

user = st.session_state['user']

# Define flashcard questions (must match income_data)
flashcards = [
    {"field": "age", "label": "Age", "type": "number"},
    {"field": "workclass", "label": "Workclass", "type": "select", "options": ["Private", "Self-emp-not-inc", "Gov", "Other"]},
    {"field": "education", "label": "Education", "type": "select", "options": ["HS-grad", "Bachelors", "Masters", "PhD", "Some-college"]},
    {"field": "marital_status", "label": "Marital Status", "type": "select", "options": ["Never-married", "Married-civ-spouse", "Divorced", "Separated"]},
    {"field": "occupation", "label": "Occupation", "type": "select", "options": ["Tech-support", "Sales", "Exec-managerial", "Admin-clerical", "Other"]},
    {"field": "relationship", "label": "Relationship", "type": "select", "options": ["Not-in-family", "Husband", "Wife", "Own-child", "Other-relative"]},
    {"field": "race", "label": "Race", "type": "select", "options": ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"]},
    {"field": "sex", "label": "Gender", "type": "select", "options": ["Male", "Female"]},
    {"field": "hours_per_week", "label": "Hours per Week", "type": "number"},
    {"field": "native_country", "label": "Native Country", "type": "select", "options": ["United-States", "India", "Mexico", "Germany", "Canada", "Other"]}
]

# Session state setup
if "answers" not in st.session_state:
    st.session_state.answers = {}
    st.session_state.flashcard_index = 0

answers = st.session_state.answers

# Show current card
current_card = flashcards[st.session_state.flashcard_index]
with st.form(key=f"form_{current_card['field']}"):
    st.subheader(f"📌 {current_card['label']}")
    
    if current_card["type"] == "number":
        val = st.number_input(current_card['label'], min_value=0, key=current_card["field"])
    elif current_card["type"] == "select":
        val = st.selectbox(f"Choose {current_card['label']}", options=current_card["options"], key=current_card["field"])

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.flashcard_index > 0:
            if st.form_submit_button("⬅️ Previous"):
                st.session_state.flashcard_index -= 1
                st.rerun()
    with col2:
        if st.form_submit_button("Next ➡️"):
            answers[current_card["field"]] = val
            st.session_state.answers = answers
            if st.session_state.flashcard_index < len(flashcards) - 1:
                st.session_state.flashcard_index += 1
            st.rerun()

# Predict button
if st.session_state.flashcard_index == len(flashcards) - 1:
    if st.button("🎯 Predict Income Level", type="primary"):
        missing = [card["label"] for card in flashcards if card["field"] not in answers]
        if missing:
            st.warning(f"Missing fields: {', '.join(missing)}")
        else:
            # Add hidden fields with default values
            input_dict = {
                "age": answers.get('age', 0),
                "workclass": answers.get('workclass', 'Other'),
                "education": answers.get('education', 'HS-grad'),
                "marital_status": answers.get('marital_status', 'Never-married'),
                "occupation": answers.get('occupation', 'Other'),
                "relationship": answers.get('relationship', 'Not-in-family'),
                "race": answers.get('race', 'Other'),
                "sex": answers.get('sex', 'Male'),
                "hours_per_week": answers.get('hours_per_week', 40),
                "native_country": answers.get('native_country', 'Other'),
                "capital_gain": 0,
                "capital_loss": 0,
                "education_num": 13
            }

            # Ensure correct column order from training
            feature_order = ['age', 'workclass', 'education', 'education_num',
                             'marital_status', 'occupation', 'relationship',
                             'race', 'sex', 'capital_gain', 'capital_loss',
                             'hours_per_week', 'native_country']

            input_df = pd.DataFrame([input_dict], columns=feature_order)

            # Encode categorical features
            for col in le_dict:
                if input_dict[col] in le_dict[col].classes_:
                    input_df[col] = le_dict[col].transform([input_dict[col]])
                else:
                    input_df[col] = -1  # Unknown value

            try:
                prediction = model.predict(input_df)[0]
                income = '>50K' if prediction == 1 else '<=50K'

                career_suggestion = "Software Engineer, Data Scientist" if income == '>50K' else "Customer Support, Administrative Assistant"
                improvements = "Keep upskilling in leadership." if income == '>50K' else "Learn Python or digital marketing."

                # Save result to session state
                st.session_state.prediction_result = {
                    "income": income,
                    "career": career_suggestion,
                    "improvements": improvements,
                    "details": input_dict
                }

                # Save to DB
                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO prediction_results (
                        user_id, age, workclass, education, marital_status, occupation,
                        relationship, race, gender, hours_per_week, native_country,
                        predicted_income, career_suggestions, improvement_recommendations,
                        capital_gain, capital_loss, education_num
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    user['id'],
                    input_dict['age'], input_dict['workclass'], input_dict['education'],
                    input_dict['marital_status'], input_dict['occupation'],
                    input_dict['relationship'], input_dict['race'], input_dict['sex'],
                    input_dict['hours_per_week'], input_dict['native_country'],
                    income, career_suggestion, improvements,
                    input_dict['capital_gain'], input_dict['capital_loss'], input_dict['education_num']
                ))

                conn.commit()
                cursor.close()
                conn.close()

                # Redirect to results page
                st.switch_page("pages/10_Results_Display.py")

            except Exception as e:
                st.error("Something went wrong during prediction.")
                st.write(str(e))
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals():
                    conn.close()