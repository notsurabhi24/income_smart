import streamlit as st

if 'user' not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

st.title("🎯 Personalized Goal Checklist")

if 'goals' not in st.session_state:
    st.session_state['goals'] = [
        "Learn Python", "Take ML Course", "Apply to 5 Jobs"
    ]
    st.session_state['completed'] = [False]*len(st.session_state['goals'])

for i, goal in enumerate(st.session_state['goals']):
    col1, col2 = st.columns([4, 1])
    completed = col2.checkbox(" ", key=f"check_{i}")
    st.session_state['completed'][i] = completed
    st.progress(int(completed)*100, text=goal)

new_goal = st.text_input("Add New Goal")
if st.button("➕ Add Goal") and new_goal:
    st.session_state['goals'].append(new_goal)
    st.session_state['completed'].append(False)
    st.rerun()
