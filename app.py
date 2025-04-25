import streamlit as st
import mysql.connector
from analyze import analyze_text
from datetime import datetime


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  
        port=3306, 
        user="root",  
        password="1234",
        database="mentalhealth_pal"  
    )


def save_entry_to_db(text, analysis):
 
    conn = get_db_connection()
    cursor = conn.cursor()

   
    query = """
    INSERT INTO journal_entries (date, text, emotion, emotion_score, sentiment, sentiment_score)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        text,
        analysis["emotion"],
        analysis["emotion_score"],
        analysis["sentiment"],
        analysis["sentiment_score"]
    )

   
    cursor.execute(query, values)
    conn.commit()

    
    cursor.close()
    conn.close()


def get_entries_from_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) 

   
    cursor.execute("SELECT * FROM journal_entries ORDER BY date DESC")

   
    entries = cursor.fetchall()

   
    cursor.close()
    conn.close()

    return entries


st.title("🧠 MentalHealthPal – AI Mood Tracker")

st.markdown("Write your journal entry and let the AI detect your emotion:")

text = st.text_area("How are you feeling today?", height=200)

if st.button("🧪 Analyze and Save"):
    if text.strip():
        analysis = analyze_text(text)
        save_entry_to_db(text, analysis)  
        st.success(f"**Emotion:** {analysis['emotion']} ({analysis['emotion_score']}) | "
                   f"**Sentiment:** {analysis['sentiment']} ({analysis['sentiment_score']})")
    else:
        st.warning("Please write something before analyzing.")


st.subheader("📜 Journal History")
entries = get_entries_from_db()  

for entry in entries:
    st.markdown(f"""
    <div class="entry-box">
        <b>{entry['date']}</b><br>
        {entry['text']}<br>
        <i>Emotion: {entry['emotion']} ({entry['emotion_score']})</i><br>
        <i>Sentiment: {entry['sentiment']} ({entry['sentiment_score']})</i>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # Close the theme wrapper div

import pandas as pd
import matplotlib.pyplot as plt

st.subheader("📈 Mood Analytics")

# Get journal entries
entries = get_entries_from_db()

if entries:
    df = pd.DataFrame(entries)
    df["date"] = pd.to_datetime(df["date"])

    # Line chart for emotion & sentiment scores
    st.markdown("### Emotion & Sentiment Over Time")
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["emotion_score"], label="Emotion Score", marker="o")
    ax.plot(df["date"], df["sentiment_score"], label="Sentiment Score", marker="x")
    ax.set_xlabel("Date")
    ax.set_ylabel("Score")
    ax.legend()
    st.pyplot(fig)

    # Emotion distribution
    st.markdown("### Emotion Distribution")
    emotion_counts = df["emotion"].value_counts()
    st.bar_chart(emotion_counts)

    # Sentiment distribution
    st.markdown("### Sentiment Distribution")
    sentiment_counts = df["sentiment"].value_counts()
    st.bar_chart(sentiment_counts)

else:
    st.info("No entries yet. Your graphs will show here once you start journaling!")
