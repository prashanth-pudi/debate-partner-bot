import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

st.title("🗣️ Debate Partner Bot")

topic = st.text_input("Enter a debate topic:")

if st.button("Start Debate"):
    if topic:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an intelligent debate partner. Give clear arguments, counterarguments, and reasoning."
                },
                {
                    "role": "user",
                    "content": f"Let's debate this topic: {topic}"
                }
            ]
        )

        st.write(response.choices[0].message.content)
    else:
        st.warning("Please enter a debate topic.")