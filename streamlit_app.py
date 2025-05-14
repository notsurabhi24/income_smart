import streamlit as st

st.set_page_config(page_title="Income Predictor", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Register", "Login", "Predictor",
    "Career Path Visualizer", "Resume Analyzer",
    "Goal Checklist", "AI Career Advisor", "Admin Panel"
])

if page == "Register":
    st.switch_page("pages/1_Register.py")
elif page == "Login":
    st.switch_page("pages/2_Login.py")
elif page == "Predictor":
    st.switch_page("pages/3_Predictor.py")
elif page == "Career Path Visualizer":
    st.switch_page("pages/4_Career_Path_Visualizer.py")
elif page == "Resume Analyzer":
    st.switch_page("pages/5_Resume_Analyzer.py")
elif page == "Goal Checklist":
    st.switch_page("pages/6_Goal_Checklist.py")
elif page == "AI Career Advisor":
    st.switch_page("pages/9_AI_Chatbot.py")
elif page == "Admin Panel":
    st.switch_page("pages/8_Admin_Panel.py")