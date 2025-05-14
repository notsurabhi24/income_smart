import streamlit as st

st.title("🤖 AI Career Advisor")

if 'user' not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

prompt = st.text_input("Ask anything about careers or salary growth:")

if prompt:
    st.markdown(f"**🧑‍💻 You:** {prompt}")
    st.markdown(f"**🤖 Answer:**")
    
    if "career" in prompt.lower():
        st.write("Based on your history, consider tech or data science roles for better income.")
    elif "income" in prompt.lower():
        st.write("Keep building skills — your predicted income can grow with upskilling.")
    elif "improve" in prompt.lower() or "tips" in prompt.lower():
        st.write("Try learning Python, SQL, or project management.")
    else:
        st.write("That's a great question! Try rephrasing it for more specific advice.")