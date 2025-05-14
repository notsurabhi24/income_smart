import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import seaborn as sns
from collections import Counter

# Protect page
if not st.session_state.get('admin_logged_in', False):
    st.warning("Admin login required.")
    st.stop()

st.title("🔒 Admin Panel – Data Science Mode")

# Connect to DB
try:
    conn = mysql.connector.connect(
        host="Surabhi",
        user="root",
        password="Goldy@2406",
        database="income_prediction"
    )
    cursor = conn.cursor(dictionary=True)

    # Load data with username
    cursor.execute("""
        SELECT pr.*, u.username 
        FROM prediction_results pr
        JOIN users u ON pr.user_id = u.id
    """)
    results = cursor.fetchall()
    df = pd.DataFrame(results)

    if df.empty:
        st.info("No predictions found. Users haven't used the app yet.")
        st.stop()

    # Sidebar: Filter by User
    st.sidebar.title("🔍 Filter by User")
    usernames = df['username'].unique().tolist()
    selected_user = st.sidebar.selectbox("Select a user", options=["All"] + usernames)

    if selected_user != "All":
        df = df[df['username'] == selected_user]

    # Show basic stats
    st.markdown(f"### Total Predictions: {len(df)}")
    st.markdown(f"### Unique Users: {df['username'].nunique()}")

    # 📊 Graph 1: Income Distribution
    st.subheader("📈 Income Distribution")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df, x='predicted_income', palette=['#FF9999', '#66B2FF'], ax=ax1)
    ax1.set_title("Predicted Income Levels")
    st.pyplot(fig1)

    # 📊 Graph 2: Career Suggestions Word Cloud
    st.subheader("☁️ Career Suggestions Word Cloud")
    from wordcloud import WordCloud

    text = ' '.join(df['career_suggestions'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.imshow(wordcloud, interpolation='bilinear')
    ax2.axis("off")
    st.pyplot(fig2)

    # 📊 Graph 3: Hours per Week vs Income Level
    st.subheader("📅 Hours per Week vs Income")
    try:
        df['hours_per_week'] = pd.to_numeric(df['hours_per_week'], errors='coerce')
        df['hour_range'] = pd.cut(df['hours_per_week'], bins=[0, 20, 40, 60, 80], labels=["<20", "20-40", "40-60", "60+"])
        grouped = df.groupby('hour_range')['predicted_income'].apply(lambda x: (x == '>50K').mean()).reset_index(name='high_income_ratio')

        fig3, ax3 = plt.subplots()
        ax3.bar(grouped['hour_range'], grouped['high_income_ratio'], color=['#4CAF50', '#FFA726', '#EF5350', '#29B6F6'])
        ax3.set_ylabel("High Income (%)")
        ax3.set_title("Hours per Week vs High Income Rate")
        st.pyplot(fig3)
    except Exception as e:
        st.error("📊 Error generating hours vs income graph.")
        st.write(str(e))

    # 📊 Graph 4: Top Careers Suggested
    st.subheader("🎯 Most Suggested Careers")
    try:
        career_list = [item.strip() for career in df['career_suggestions'].str.split(', ').dropna() for item in career]
        career_counter = Counter(career_list)
        career_df = pd.DataFrame(list(career_counter.items()), columns=['Career', 'Count']).sort_values(by='Count', ascending=False)

        fig4, ax4 = plt.subplots()
        sns.barplot(x='Count', y='Career', data=career_df, palette="viridis", ax=ax4)
        ax4.set_title("Most Suggested Careers")
        st.pyplot(fig4)
    except Exception as e:
        st.error("📌 Error generating career suggestions graph.")
        st.write(str(e))

    # 📊 Graph 5: Income Over Time (per user)
    st.subheader("⏳ Income Trend Over Time")
    try:
        for user in df['username'].unique():
            st.markdown(f"#### 👤 {user}")
            user_df = df[df['username'] == user].copy()
            user_df['prediction_number'] = range(1, len(user_df) + 1)
            
            fig, ax = plt.subplots()
            ax.plot(user_df['prediction_number'], user_df['predicted_income'].apply(lambda x: 1 if x == '>50K' else 0), marker='o', linestyle='--')
            ax.set_yticks([0, 1])
            ax.set_yticklabels(['<=50K', '>50K'])
            ax.set_xlabel("Prediction No.")
            ax.set_title(f"{user}'s Income Prediction History")
            st.pyplot(fig)
    except Exception as e:
        st.error("📉 Error generating income trend graphs.")
        st.write(str(e))

    # 🗂 Raw Data Table
    st.subheader("📁 Raw Prediction Data")
    st.dataframe(df[['username', 'predicted_income', 'career_suggestions', 'hours_per_week']])

except Exception as e:
    st.error("Database error:")
    st.write(str(e))