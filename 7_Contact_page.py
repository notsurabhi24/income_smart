import streamlit as st

st.title("📬 Contact & Feedback")

name = st.text_input("Surabhi")
email = st.text_input("incomesmart@gmail.com")
message = st.text_area("1234567890")

if st.button("Send"):
    st.success("Thank you! We’ll get back to you soon.")