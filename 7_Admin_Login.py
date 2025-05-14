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

st.title("🔐 Admin Login")

email = st.text_input("Admin Email")
password = st.text_input("Password", type="password")
login_button = st.button("Login as Admin")

if login_button:
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password_hash = %s", (email, hashed_pw))
        user = cursor.fetchone()

        if user and user['username'] == 'admin':
            st.session_state['admin_logged_in'] = True
            st.success("Logged in as Admin!")
            st.switch_page("pages/8_Admin_Panel.py")  # ⬅️ Auto redirect to admin panel
        else:
            st.error("Invalid admin credentials.")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()