import streamlit as st
import hashlib
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="Surabhi",
        user="root",
        password="Goldy@2406",
        database="income_prediction"
    )

st.title("📝 Register")

with st.form("register_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("Register")

if submit:
    if password != confirm_password:
        st.error("Passwords do not match.")
    elif len(password) < 6:
        st.warning("Password must be at least 6 characters.")
    else:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed_pw)
            )
            conn.commit()
            st.success("✅ Registration successful! Go to Login page.")
        except mysql.connector.IntegrityError:
            st.warning("⚠️ Email or username already taken.")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
