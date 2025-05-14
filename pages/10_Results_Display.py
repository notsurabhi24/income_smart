import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns  # ✅ Added missing import

st.title("📊 Prediction Result & Visualizations")

if 'prediction_result' not in st.session_state:
    st.warning("No prediction found. Please go back and predict first.")
    st.stop()

result = st.session_state.prediction_result

# Show result
st.markdown(f"### 🎯 Predicted Income: `{result['income']}`")
st.markdown("### 👔 Career Suggestions:")
st.write(result['career'])
st.markdown("### 📈 Improvement Tips:")
st.write(result['improvements'])

# Show inputs
st.markdown("### 🧾 Your Inputs:")
for k, v in result['details'].items():
    st.write(f"- **{k.replace('_', ' ').title()}:** {v}")

# Session state history
if 'user_predictions' not in st.session_state:
    st.session_state.user_predictions = []

st.session_state.user_predictions.append(result['details'])
df_user = pd.DataFrame(st.session_state.user_predictions)

# --- GRAPH SECTION ---
st.markdown("### 📈 Graphs Based on Your Data")

# 1. Income Level
fig1, ax1 = plt.subplots()
ax1.bar(['Predicted Income'], [1], color=['#FF9999'] if result['income'] == '<=50K' else ['#66B2FF'])
ax1.bar_label(ax1.containers[0], labels=[result['income']], label_type='center')
ax1.set_title("Your Predicted Income Level")
ax1.axis('off')
st.pyplot(fig1)

# 2. Career Suggestions Word Cloud
st.markdown("### ☁️ Career Suggestions Word Cloud")
text = result['career']
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

fig2, ax2 = plt.subplots()
ax2.imshow(wordcloud, interpolation='bilinear')
ax2.axis("off")
st.pyplot(fig2)

# 3. Hours per Week vs Career Suggestion
st.markdown("### 🕒 Hours per Week vs Career Suggestions")

career_list = [item.strip() for item in result['career'].split(', ')]

fig3, ax3 = plt.subplots()
ax3.barh(career_list, [result['details']['hours_per_week']] * len(career_list), color='#4CAF50')
ax3.set_xlabel("Hours per Week")
ax3.set_title("Estimated Weekly Hours for Each Career")
st.pyplot(fig3)

# 4. User Input Breakdown (Pie Chart)
st.markdown("### 🥧 Your Profile Summary")

pie_labels = list(result['details'].keys())
pie_sizes = [1] * len(pie_labels)  # Equal slices

fig4, ax4 = plt.subplots()
palette = sns.color_palette("pastel", len(pie_labels))
ax4.pie(pie_sizes, labels=pie_labels, autopct='%1.1f%%', startangle=140, colors=palette)
ax4.axis('equal')  # Equal aspect ratio
st.pyplot(fig4)

# Button to predict again
if st.button("🔁 Predict Again"):
    st.switch_page("pages/3_Predictor.py")
