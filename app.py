import os
import re

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        API_KEY = None

MODEL = "openai/gpt-oss-20b"


st.set_page_config(
    page_title="DebateX | AI Debate Partner",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


if "screen" not in st.session_state:
    st.session_state.screen = "home"

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "position" not in st.session_state:
    st.session_state.position = "For"

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Intermediate"

if "style" not in st.session_state:
    st.session_state.style = "Academic"

if "rounds" not in st.session_state:
    st.session_state.rounds = 4

if "current_round" not in st.session_state:
    st.session_state.current_round = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "evaluation" not in st.session_state:
    st.session_state.evaluation = ""


st.markdown(
    """
<style>
.stApp {
    background: #f4f7fb;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: #081b33;
}

section[data-testid="stSidebar"] * {
    color: #ffffff;
}

.sidebar-brand {
    text-align: center;
    padding: 10px 0 20px;
}

.sidebar-icon {
    font-size: 38px;
}

.sidebar-name {
    font-size: 25px;
    font-weight: 800;
}

.sidebar-gold {
    color: #f4c430 !important;
}

.sidebar-label {
    color: #9cb4d0 !important;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin: 18px 0 8px;
}

.sidebar-step {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 7px;
    font-size: 13px;
}

.sidebar-step.active {
    background: rgba(244,196,48,0.15);
    border-color: rgba(244,196,48,0.35);
}

.brand {
    color: #081b33 !important;
    font-size: 20px;
    font-weight: 850;
    margin-bottom: 15px;
}

.brand span {
    color: #d7a900 !important;
}

.hero-shell {
    background: linear-gradient(120deg, #07182e 0%, #0d2d52 55%, #145da0 100%);
    border-radius: 26px;
    padding: 44px 48px;
    margin-bottom: 28px;
    box-shadow: 0 18px 45px rgba(8,27,51,0.16);
}

.hero-eyebrow {
    color: #ffd95a !important;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: 1.3px;
}

.hero-title {
    color: white !important;
    font-size: 48px;
    line-height: 1.06;
    font-weight: 900;
    margin-top: 12px;
}

.hero-title span {
    color: #ffd95a !important;
}

.hero-description {
    color: #d7e5f5 !important;
    font-size: 16px;
    line-height: 1.7;
    max-width: 760px;
    margin-top: 12px;
}

.section-title {
    color: #081b33 !important;
    font-size: 22px;
    font-weight: 850;
    margin-top: 22px;
}

.section-caption {
    color: #7b899c !important;
    font-size: 13px;
}

.feature-title {
    color: #081b33 !important;
    font-weight: 800;
}

.feature-text {
    color: #728096 !important;
    font-size: 13px;
    line-height: 1.55;
}

.debate-title {
    color: #081b33 !important;
    font-size: 22px;
    font-weight: 850;
}

.ai-label {
    color: #145da0 !important;
    font-size: 12px;
    font-weight: 850;
}

.user-label {
    color: #937000 !important;
    font-size: 12px;
    font-weight: 850;
}

.stButton > button {
    min-height: 44px;
    border-radius: 10px !important;
    font-weight: 800;
}

.stButton > button[kind="primary"] {
    background: #f4c430 !important;
    color: #081b33 !important;
    border: none !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e1e7ef;
    border-radius: 14px;
    padding: 13px;
}

.footer {
    text-align: center;
    color: #8a96a7 !important;
    font-size: 11px;
    border-top: 1px solid #dfe5ed;
    margin-top: 40px;
    padding-top: 22px;
}
</style>
""",
    unsafe_allow_html=True,
)


def get_client():
    if not API_KEY:
        return None
    return Groq(api_key=API_KEY)


def reset_app():
    st.session_state.screen = "home"
    st.session_state.topic = ""
    st.session_state.position = "For"
    st.session_state.difficulty = "Intermediate"
    st.session_state.style = "Academic"
    st.session_state.rounds = 4
    st.session_state.current_round = 0
    st.session_state.messages = []
    st.session_state.evaluation = ""


def extract_scores(text):
    patterns = {
        "Argument Quality": r"Argument Quality\s*:\s*(\d+(?:\.\d+)?)\s*/?\s*10",
        "Relevance": r"Relevance\s*:\s*(\d+(?:\.\d+)?)\s*/?\s*10",
        "Reasoning": r"Reasoning\s*:\s*(\d+(?:\.\d+)?)\s*/?\s*10",
        "Counterargument": r"Counterargument\s*:\s*(\d+(?:\.\d+)?)\s*/?\s*10",
        "Overall Performance": r"Overall Performance\s*:\s*(\d+(?:\.\d+)?)\s*/?\s*10",
    }

    scores = {}
    for name, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            scores[name] = float(match.group(1))
    return scores


def evaluate_debate():
    if not API_KEY:
        st.error("AI service configuration is missing.")
        return False

    user_arguments = [
        message["content"]
        for message in st.session_state.messages
        if message["role"] == "user"
    ]

    if not user_arguments:
        st.warning("Please submit at least one argument.")
        return False

    try:
        client = get_client()

        arguments_text = "\n\n".join(
            f"Argument {index + 1}: {argument}"
            for index, argument in enumerate(user_arguments)
        )

        with st.spinner("🧠 Analysing your debate performance..."):
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a professional debate evaluator.

Evaluate the user's debating performance objectively.

Return these exact score lines:

Argument Quality: X/10
Relevance: X/10
Reasoning: X/10
Counterargument: X/10
Overall Performance: X/10

Then provide:

### Strengths
Explain what the user did well.

### Areas for Improvement
Explain specific weaknesses and how to improve them.

### Practical Tip
Give one practical tip for the next debate.

Be specific, fair, constructive, and easy to understand.
""",
                    },
                    {
                        "role": "user",
                        "content": f"""
Debate Topic:
{st.session_state.topic}

User Position:
{st.session_state.position}

Difficulty:
{st.session_state.difficulty}

Style:
{st.session_state.style}

User Arguments:
{arguments_text}
""",
                    },
                ],
            )

        st.session_state.evaluation = response.choices[0].message.content
        st.session_state.screen = "result"
        return True

    except Exception as error:
        st.error(f"Unable to evaluate the debate: {error}")
        return False


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-icon">⚡</div>
            <div class="sidebar-name">
                Debate<span class="sidebar-gold">X</span>
            </div>
            <div class="sidebar-gold">
                AI DEBATE PARTNER
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### WORKFLOW")

    current = st.session_state.screen

    steps = [
        ("home", "01", "🎯 Create Debate"),
        ("debate", "02", "⚔️ Debate Arena"),
        ("result", "03", "🏆 Performance"),
    ]

    for name, number, title in steps:
        if current == name:
            st.markdown(
                f'<div class="sidebar-step active">🟡 {number} — {title}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="sidebar-step">⚪ {number} — {title}</div>',
                unsafe_allow_html=True,
            )

    if current == "debate":
        st.divider()
        st.markdown("### CURRENT SESSION")
        st.write(
            f"Round: {st.session_state.current_round}/"
            f"{st.session_state.rounds}"
        )
        st.write(
            f"Position: {st.session_state.position}"
        )

        if st.button("↩ Exit Debate", use_container_width=True):
            reset_app()
            st.rerun()

    elif current == "result":
        st.divider()
        if st.button("＋ New Debate", use_container_width=True):
            reset_app()
            st.rerun()


top_left, top_right = st.columns([8, 1])

with top_left:
    st.markdown(
        '<div class="brand">Debate<span>X</span></div>',
        unsafe_allow_html=True,
    )

with top_right:
    st.success("Online")


if st.session_state.screen == "home":

    hero = st.container(border=True)
    with hero:
        st.markdown(
            '<div class="hero-eyebrow">⚡ AI-POWERED DEBATE PLATFORM</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="hero-title">Think sharper.<br><span>Debate smarter.</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="hero-description">Practice real debate skills with an intelligent AI opponent. Defend your position, handle counterarguments, and discover how strong your reasoning really is.</div>',
            unsafe_allow_html=True,
        )

        h1, h2, h3 = st.columns(3)
        with h1:
            st.write("🎯 Choose your topic")
        with h2:
            st.write("⚔️ Defend your position")
        with h3:
            st.write("🏆 Get AI feedback")

    st.markdown(
        '<div class="section-title">🎯 Create Your Debate</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-caption">Choose your topic and configure your debate session.</div>',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Debate Topic",
        placeholder="Example: Should AI replace human jobs?",
    )

    topics = [
        "Choose a topic idea",
        "Should AI replace human jobs?",
        "Is online education better than classroom education?",
        "Should college education be free?",
        "Does social media do more harm than good?",
        "Should school uniforms be mandatory?",
        "Is remote work better than office work?",
        "Should voting be mandatory?",
    ]

    selected = st.selectbox("💡 Quick Topic Ideas", topics)

    if selected != "Choose a topic idea":
        topic = selected

    st.markdown(
        '<div class="section-title">⚙️ Debate Settings</div>',
        unsafe_allow_html=True,
    )
    st.caption("Control the challenge level and debate format.")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        difficulty = st.selectbox(
            "Difficulty",
            ["Beginner", "Intermediate", "Advanced"],
            index=1,
        )

    with c2:
        style = st.selectbox(
            "Style",
            ["Academic", "Casual", "Competitive"],
        )

    with c3:
        rounds = st.selectbox(
            "Rounds",
            [2, 3, 4, 5],
            index=2,
        )

    with c4:
        position = st.selectbox(
            "Your Position",
            ["For", "Against"],
        )

    if position == "For":
        st.info(
            "⚔️ You support the topic. AI will argue against you."
        )
    else:
        st.info(
            "⚔️ You oppose the topic. AI will argue in favour."
        )

    st.markdown(
        '<div class="section-title">🚀 DebateX Features</div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        with st.container(border=True):
            st.markdown(
                '<div class="feature-title">🤖 AI Challenger</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="feature-text">Strong counterarguments, examples, and challenging questions.</div>',
                unsafe_allow_html=True,
            )

    with f2:
        with st.container(border=True):
            st.markdown(
                '<div class="feature-title">⚔️ Live Debate</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="feature-text">Defend your position round by round against the AI.</div>',
                unsafe_allow_html=True,
            )

    with f3:
        with st.container(border=True):
            st.markdown(
                '<div class="feature-title">🏆 AI Evaluation</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="feature-text">Scores, strengths, weaknesses, and practical improvement tips.</div>',
                unsafe_allow_html=True,
            )

    st.write("")

    if st.button(
        "⚡ Enter Debate Arena",
        type="primary",
        use_container_width=True,
    ):

        if not topic.strip():
            st.warning("Please enter a debate topic first.")
            st.stop()

        if not API_KEY:
            st.error("AI service configuration is missing.")
            st.stop()

        try:
            client = get_client()

            with st.spinner(
                "🤖 Preparing your AI opponent..."
            ):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": f"""
You are an expert debate opponent.

Topic:
{topic}

User position:
{position}

Difficulty:
{difficulty}

Style:
{style}

Start the debate from the opposite side.

Give:
1. A clear opening position.
2. Strong reasoning.
3. One useful example.
4. One challenging question.

Do not conclude the debate.
Do not evaluate the user.

Be respectful and intellectually challenging.
""",
                        }
                    ],
                )

            st.session_state.topic = topic
            st.session_state.position = position
            st.session_state.difficulty = difficulty
            st.session_state.style = style
            st.session_state.rounds = rounds
            st.session_state.current_round = 1

            st.session_state.messages = [
                {
                    "role": "ai",
                    "content": response.choices[0].message.content,
                }
            ]

            st.session_state.evaluation = ""
            st.session_state.screen = "debate"

            st.rerun()

        except Exception as error:
            st.error(f"Unable to start the debate: {error}")


elif st.session_state.screen == "debate":

    st.markdown(
        '<div class="debate-title">⚔️ Debate Arena</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Defend your position, respond to the AI, and build stronger arguments."
    )

    with st.container(border=True):
        st.markdown(
            f"### {st.session_state.topic}"
        )
        st.write(
            f"**Your Position:** {st.session_state.position}"
        )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Round",
            f"{st.session_state.current_round}/"
            f"{st.session_state.rounds}",
        )

    with m2:
        st.metric(
            "Your Side",
            st.session_state.position,
        )

    with m3:
        st.metric(
            "Difficulty",
            st.session_state.difficulty,
        )

    with m4:
        st.metric(
            "Style",
            st.session_state.style,
        )

    completed = min(
        st.session_state.current_round - 1,
        st.session_state.rounds,
    )

    st.progress(
        completed / st.session_state.rounds,
        text=(
            f"Debate Progress: "
            f"{completed}/{st.session_state.rounds}"
        ),
    )

    for message in st.session_state.messages:

        if message["role"] == "ai":

            with st.chat_message(
                "assistant",
                avatar="🤖",
            ):
                st.markdown(
                    "**AI Debate Partner**"
                )
                st.markdown(
                    message["content"]
                )

        else:

            with st.chat_message(
                "user",
                avatar="👤",
            ):
                st.markdown(
                    "**Your Argument**"
                )
                st.markdown(
                    message["content"]
                )

    st.markdown(
        "## ✍️ Your Turn"
    )

    st.caption(
        "Use reasoning, examples, and evidence to defend your position."
    )

    user_argument = st.text_area(
        "Your Argument",
        placeholder=(
            "Write your argument here...\n\n"
            "Example: I believe this because..."
        ),
        height=160,
        key=f"argument_{st.session_state.current_round}",
    )

    submit_col, finish_col = st.columns(2)

    with submit_col:

        if st.button(
            "🔄 Submit & Continue",
            type="primary",
            use_container_width=True,
        ):

            if not user_argument.strip():

                st.warning(
                    "Please write your argument first."
                )
                st.stop()

            try:

                client = get_client()

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": user_argument,
                    }
                )

                conversation = [
                    {
                        "role": "system",
                        "content": f"""
You are an expert opposing debate partner.

Topic:
{st.session_state.topic}

User position:
{st.session_state.position}

Difficulty:
{st.session_state.difficulty}

Style:
{st.session_state.style}

Respond to the user's latest argument.

You MUST:
1. Address their main point.
2. Give a strong counterargument.
3. Identify a weakness or assumption.
4. Give an example when useful.
5. Ask one challenging question.

Do not conclude the debate.
Do not evaluate the user.

Remain respectful but challenging.
""",
                    }
                ]

                for message in st.session_state.messages:

                    if message["role"] == "ai":

                        conversation.append(
                            {
                                "role": "assistant",
                                "content": message["content"],
                            }
                        )

                    else:

                        conversation.append(
                            {
                                "role": "user",
                                "content": message["content"],
                            }
                        )

                with st.spinner(
                    "🤖 AI is thinking..."
                ):

                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=conversation,
                    )

                st.session_state.messages.append(
                    {
                        "role": "ai",
                        "content": response.choices[0].message.content,
                    }
                )

                if (
                    st.session_state.current_round
                    >= st.session_state.rounds
                ):

                    evaluate_debate()
                    st.rerun()

                else:

                    st.session_state.current_round += 1
                    st.rerun()

            except Exception as error:

                st.error(
                    f"Unable to process your argument: {error}"
                )

    with finish_col:

        if st.button(
            "🏁 Finish & Evaluate",
            use_container_width=True,
        ):

            if evaluate_debate():
                st.rerun()


elif st.session_state.screen == "result":

    st.markdown(
        "## 🏆 Debate Performance Report"
    )

    st.caption(
        "Your debate has been analysed by the AI evaluator."
    )

    scores = extract_scores(
        st.session_state.evaluation
    )

    overall = scores.get(
        "Overall Performance"
    )

    if overall is not None:

        st.metric(
            "⭐ Overall Performance",
            f"{overall:g}/10"
        )

        if overall >= 8:
            st.success(
                "🔥 Excellent performance! Your debating skills are strong."
            )
        elif overall >= 6:
            st.info(
                "👍 Good performance! You have a solid foundation."
            )
        else:
            st.warning(
                "💪 Keep practising! Focus on reasoning and stronger counterarguments."
            )

    st.markdown(
        "## 📊 Performance Breakdown"
    )

    st.caption(
        "Your performance across the most important debate skills."
    )

    s1, s2, s3, s4 = st.columns(4)

    score_items = [
        ("Argument Quality", s1),
        ("Relevance", s2),
        ("Reasoning", s3),
        ("Counterargument", s4),
    ]

    for name, column in score_items:

        value = scores.get(name)

        with column:

            if value is not None:
                st.metric(
                    name,
                    f"{value:g}/10"
                )
            else:
                st.metric(
                    name,
                    "—"
                )

    st.markdown(
        "## 🧠 AI Feedback"
    )

    st.caption(
        "Detailed analysis of your debate performance."
    )

    with st.container(border=True):

        st.markdown(
            st.session_state.evaluation
        )

    st.markdown(
        "## 📌 Debate Summary"
    )

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Position",
            st.session_state.position
        )

    with b:
        st.metric(
            "Rounds",
            st.session_state.rounds
        )

    with c:
        st.metric(
            "Difficulty",
            st.session_state.difficulty
        )

    st.write("")

    new_col, home_col = st.columns(2)

    with new_col:

        if st.button(
            "⚡ Start New Debate",
            type="primary",
            use_container_width=True,
        ):

            reset_app()
            st.rerun()

    with home_col:

        if st.button(
            "🏠 Back to Home",
            use_container_width=True,
        ):

            reset_app()
            st.rerun()


st.markdown(
    '<div class="footer">DebateX • AI Debate Partner<br>Built with Python • Streamlit • Groq AI</div>',
    unsafe_allow_html=True,
)
