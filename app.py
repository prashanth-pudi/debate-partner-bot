import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Streamlit Cloud secrets support
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

# Page configuration
st.set_page_config(
    page_title="Debate Partner Bot",
    page_icon="🗣️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #f5f9ff;
}

.block-container {
    max-width: 900px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #0d47a1, #1976d2);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(13, 71, 161, 0.20);
}

.hero h1 {
    color: white;
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    color: #fff8d6;
    font-size: 18px;
}

.section-title {
    color: #0d47a1;
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
}

.info-box {
    background-color: #fff8d6;
    border-left: 6px solid #fbc02d;
    padding: 18px;
    border-radius: 10px;
    margin: 20px 0;
}

.footer {
    text-align: center;
    color: #666;
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid #ddd;
}

.stButton > button {
    width: 100%;
    background-color: #fbc02d;
    color: #0d47a1;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 17px;
}

.stButton > button:hover {
    background-color: #f9a825;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero">
    <h1>🗣️ Debate Partner Bot</h1>
    <p>Challenge your ideas. Explore both sides. Think critically.</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="info-box">
<b>How it works:</b><br>
Enter any debate topic and the AI will generate a structured,
balanced debate with clear arguments and reasoning.
</div>
""", unsafe_allow_html=True)

# Topic input
st.markdown(
    '<div class="section-title">🎯 Choose Your Debate Topic</div>',
    unsafe_allow_html=True
)

topic = st.text_input(
    "Enter a debate topic:",
    placeholder="Example: Should AI replace human jobs?"
)

# Start debate
if st.button("⚡ Start Debate"):

    if not topic.strip():
        st.warning("Please enter a debate topic.")
    
    elif not api_key:
        st.error("AI service configuration is missing.")
    
    else:
        try:
            client = Groq(api_key=api_key)

            with st.spinner("🤖 Preparing your debate..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are an intelligent and balanced debate partner.

For the given topic:
1. Clearly state the debate question.
2. Give strong arguments supporting the topic.
3. Give strong arguments opposing the topic.
4. Explain the reasoning behind each argument.
5. Give practical examples where useful.
6. Present counterarguments.
7. End with a balanced conclusion.

Use clear headings, bullet points, and simple language.
Do not take an extreme or biased position.
"""
                        },
                        {
                            "role": "user",
                            "content": f"Create a detailed debate on this topic: {topic}"
                        }
                    ]
                )

            st.markdown(
                '<div class="section-title">💬 Debate Result</div>',
                unsafe_allow_html=True
            )

            st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error("Something went wrong while generating the debate.")
            st.info("Please try again.")

# Footer
st.markdown("""
<div class="footer">
    🗣️ <b>Debate Partner Bot</b><br>
    Built with Python • Streamlit • Groq AI
</div>
""", unsafe_allow_html=True)