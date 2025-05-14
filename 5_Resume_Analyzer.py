import streamlit as st
from PyPDF2 import PdfReader
import re

if 'user' not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

st.title("📄 Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf"])

if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        st.success("✅ Resume uploaded successfully!")

        keywords = ['Python', 'SQL', 'Data Analysis', 'Machine Learning']
        found = [word for word in keywords if re.search(word, text, re.IGNORECASE)]
        st.markdown("### 🔍 Skills Found:")
        st.write(", ".join(found) if found else "None found.")

    except Exception as e:
        st.error("Could not read file. Make sure it's a valid PDF.")
