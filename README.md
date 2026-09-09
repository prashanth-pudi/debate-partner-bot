# DebateX — AI Debate Partner

A Streamlit-based interactive debate application using Groq AI.

## Features

- Professional blue/gold UI
- Debate topic selection
- Difficulty levels
- Debate styles
- Configurable rounds
- For / Against positions
- Interactive AI counterarguments
- Automatic evaluation after the final round
- Performance scores
- AI strengths and improvement feedback

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file and add:

```env
GROQ_API_KEY=your_actual_key_here
```

Then run:

```bash
streamlit run app.py
```

## Streamlit Cloud

Set the secret:

```toml
GROQ_API_KEY = "your_actual_key_here"
```

Do not upload your `.env` file or API key to GitHub.
