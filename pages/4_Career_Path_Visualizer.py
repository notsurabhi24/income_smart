import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Check login
if 'user' not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

st.title("📊 Career Path Visualizer")

# Connect to DB
conn = mysql.connector.connect(
    host="Surabhi",
    user="root",
    password="Goldy@2406",
    database="income_prediction"
)
cursor = conn.cursor(dictionary=True)

# Load user's prediction history
cursor.execute("SELECT * FROM prediction_results WHERE user_id = %s ORDER BY prediction_date ASC", (st.session_state['user']['id'],))
results = cursor.fetchall()
conn.close()

if not results:
    st.info("No predictions yet. Predict your income first!")
else:
    df = pd.DataFrame(results)

    # Convert income to numerical for plotting
    df['income_level'] = df['predicted_income'].apply(lambda x: 1 if x == '>50K' else 0)

    # Career Suggestions Word Cloud
    st.subheader("📌 Your Career Suggestions")
    from wordcloud import WordCloud
    text = ' '.join(df['career_suggestions'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig_wordcloud, ax_wordcloud = plt.subplots()
    ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
    ax_wordcloud.axis("off")
    st.pyplot(fig_wordcloud)

    # Line chart - income trend over time
    st.subheader("📈 Income Prediction Trend Over Time")
    df['prediction_number'] = range(1, len(df) + 1)
    fig_income, ax_income = plt.subplots()
    ax_income.plot(df['prediction_number'], df['income_level'], marker='o', linestyle='-', color='#4CAF50')
    ax_income.set_yticks([0, 1])
    ax_income.set_yticklabels(['<=50K', '>50K'])
    ax_income.set_xlabel("Prediction No.")
    ax_income.set_title("Income Prediction Trend")
    st.pyplot(fig_income)

    # Hours per week vs income
    st.subheader("📅 Hours per Week vs Income")
    df['hour_range'] = pd.cut(df['hours_per_week'], bins=[0, 20, 40, 60, 80], labels=["<20", "20-40", "40-60", "60+"])
    grouped = df.groupby('hour_range')['income_level'].mean().reset_index()
    grouped['income_label'] = grouped['income_level'].apply(lambda x: '>50K' if x > 0.5 else '<=50K')

    fig_hours, ax_hours = plt.subplots()
    ax_hours.bar(grouped['hour_range'], grouped['income_label'], color=['#FF9999','#66B2FF'])
    ax_hours.set_ylabel("Income Range")
    ax_hours.set_title("Hours per Week vs Predicted Income")
    st.pyplot(fig_hours)

    # Show raw data
    st.subheader("📁 Raw Prediction History")
    st.dataframe(df[['prediction_date', 'predicted_income', 'career_suggestions', 'hours_per_week']])
