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

st.title("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

if login_button:
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password_hash = %s", (email, hashed_pw))
        user = cursor.fetchone()

        if user:
            st.session_state['user'] = user
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid credentials.")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
