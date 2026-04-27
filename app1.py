import streamlit as st
from ai_engine1 import generate_roadmap, generate_explanation, generate_resources, chatbot_response
from auth1 import signup_user, login_user, save_history, get_history

st.set_page_config(page_title="Learnova", page_icon="⚡", layout="centered")

# ---------------- SESSION STATE ----------------
defaults = {
    "logged_in": False,
    "username": "",
    "selected_query": None,
    "selected_response": None,
    "chat_history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    -webkit-text-size-adjust: 100%;
}

.stApp {
    background: #0a0a0f !important;
    color: #f0eeff !important;
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }

.stApp::before {
    content: '';
    position: fixed;
    top: -150px; left: -150px;
    width: clamp(250px, 40vw, 500px);
    height: clamp(250px, 40vw, 500px);
    background: radial-gradient(circle, rgba(124,92,252,0.13) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
    animation: orb1 8s ease-in-out infinite alternate;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -150px; right: -150px;
    width: clamp(200px, 35vw, 420px);
    height: clamp(200px, 35vw, 420px);
    background: radial-gradient(circle, rgba(0,212,170,0.09) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
    animation: orb2 10s ease-in-out infinite alternate-reverse;
}
@keyframes orb1 { to { transform: translate(50px, 35px); } }
@keyframes orb2 { to { transform: translate(-40px, 25px); } }

.block-container {
    max-width: 860px !important;
    padding-left:  clamp(12px, 4vw, 40px) !important;
    padding-right: clamp(12px, 4vw, 40px) !important;
    padding-top:   clamp(14px, 3vw, 36px) !important;
    padding-bottom: 60px !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 0.5px solid rgba(255,255,255,0.07) !important;
    min-width: 200px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] * { color: #b0aac8 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    color: #b0aac8 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    text-align: left !important;
    width: 100% !important;
    padding: 10px 12px !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-height: 42px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(124,92,252,0.12) !important;
    border-color: #7c5cfc !important;
    color: #a98bff !important;
}

/* ===== TEXT INPUTS ===== */
div[data-testid="stTextInput"] input {
    background: #111118 !important;
    border: 0.5px solid rgba(255,255,255,0.14) !important;
    border-radius: 14px !important;
    color: #f0eeff !important;
    padding: 14px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
    width: 100% !important;
    min-height: 50px !important;
    -webkit-appearance: none;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #7c5cfc !important;
    box-shadow: 0 0 0 3px rgba(124,92,252,0.15) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #6b6585 !important; }
div[data-testid="stTextInput"] label {
    color: #8884a0 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

/* ===== BUTTONS ===== */
div.stButton > button {
    background: linear-gradient(135deg, #7c5cfc, #5a3dd4) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 13px 22px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
    width: 100% !important;
    min-height: 50px !important;
    touch-action: manipulation !important;
    -webkit-tap-highlight-color: transparent;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(124,92,252,0.4) !important;
}
div.stButton > button:active { transform: scale(0.97) !important; }

/* ===== SPINNER ===== */
.stSpinner > div { border-top-color: #7c5cfc !important; }

/* ===== ALERTS ===== */
div[data-testid="stAlert"] { border-radius: 12px !important; font-size: 14px !important; }
.stSuccess { background: rgba(0,212,170,0.10) !important; border: 0.5px solid rgba(0,212,170,0.28) !important; color: #00d4aa !important; }
.stError   { background: rgba(255,107,107,0.10) !important; border: 0.5px solid rgba(255,107,107,0.28) !important; color: #ff6b6b !important; }
.stInfo    { background: rgba(124,92,252,0.09) !important; border: 0.5px solid rgba(124,92,252,0.22) !important; color: #a98bff !important; }

/* ===== DIVIDER ===== */
hr { border-color: rgba(255,255,255,0.07) !important; margin: clamp(18px, 3.5vw, 34px) 0 !important; }

/* ===== SELECTBOX ===== */
div[data-testid="stSelectbox"] > div > div {
    background: #111118 !important;
    border: 0.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #f0eeff !important;
}
div[data-testid="stSelectbox"] ul,
[data-baseweb="popover"] ul {
    background: #1a1a2e !important;
    border: 1px solid rgba(124,92,252,0.3) !important;
    border-radius: 12px !important;
}
div[data-testid="stSelectbox"] li,
[data-baseweb="popover"] li {
    color: #d4c4ff !important;
    font-family: 'DM Sans', sans-serif !important;
    background: transparent !important;
}
div[data-testid="stSelectbox"] li:hover,
[data-baseweb="popover"] li:hover {
    background: rgba(124,92,252,0.2) !important;
}

/* ===== AUTH CARD ===== */
[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(2) > div:first-child {
    background: #111118;
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: clamp(14px, 2vw, 20px);
    padding: clamp(22px, 4vw, 38px) clamp(18px, 4vw, 34px) !important;
}

/* ===== SPACING CLEANUP ===== */
.stMarkdown p:empty { display: none !important; margin: 0 !important; padding: 0 !important; }
.ln-hero + div,
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]:has(.auth-card-wrapper) {
    margin-top: 0 !important;
}
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container { margin-bottom: 0 !important; }
.auth-page .element-container { margin-bottom: 6px !important; }

/* ===== MOBILE TOP BAR ===== */
.ln-mobile-bar {
    display: none;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: #111118;
    border: 0.5px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    margin-bottom: 10px;
}
.ln-mobile-logo {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(135deg, #7c5cfc, #00d4aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.ln-mobile-user {
    font-size: 13px;
    color: #a98bff;
    font-weight: 500;
}
@media (max-width: 768px) {
    .ln-mobile-bar { display: flex !important; }
}
@media (min-width: 769px) {
    .ln-mobile-bar { display: none !important; }
}

/* ===== STACK COLUMNS ON TINY SCREENS ===== */
@media (max-width: 480px) {
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 10px !important;
    }
    [data-testid="stHorizontalBlock"] > div {
        width: 100% !important;
        flex: none !important;
        min-width: 100% !important;
    }
}

/* ===== KEYFRAMES ===== */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(124,92,252,0.5); }
    50%      { opacity:.7; box-shadow: 0 0 0 7px transparent; }
}

/* ===== COMPONENT CLASSES ===== */
.ln-hero {
    text-align:center;
    padding: clamp(20px,5vw,46px) 0 clamp(6px,1.5vw,12px);
    animation: fadeUp .6s ease;
    display:flex; flex-direction:column; align-items:center;
}
.ln-badge {
    display:inline-flex; align-items:center; gap:7px;
    padding:5px 13px; border-radius:999px;
    border:0.5px solid rgba(124,92,252,0.3); background:rgba(124,92,252,0.07);
    font-size:11px; color:#a98bff; margin-bottom:14px;
    letter-spacing:.6px; text-transform:uppercase;
}
.ln-dot { width:6px;height:6px;border-radius:50%;background:#7c5cfc;display:inline-block;animation:pulse 2s ease infinite; }
.ln-h1 {
    font-family:'Syne',sans-serif;
    font-size: clamp(26px, 6.5vw, 60px);
    font-weight:800; line-height:1.1;
    letter-spacing: clamp(-1px, -0.03em, -2px);
    margin:0 0 12px;
    background:linear-gradient(135deg,#f0eeff 0%,#a98bff 50%,#00d4aa 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.ln-sub {
    font-size:clamp(13px,2.3vw,17px); color:#8884a0;
    max-width:460px; margin:0 auto; line-height:1.7;
    text-align:center; display:block; width:100%;
}

.ln-stats {
    display:grid; grid-template-columns:repeat(3,1fr);
    gap:clamp(6px,1.5vw,14px); margin:clamp(18px,4vw,30px) 0;
}
.ln-stat {
    background:#111118; border:0.5px solid rgba(255,255,255,0.08);
    border-radius:clamp(10px,1.5vw,14px);
    padding:clamp(12px,2.5vw,22px) 8px; text-align:center;
}
.ln-stat-num {
    font-family:'Syne',sans-serif; font-size:clamp(18px,4vw,30px); font-weight:800;
    background:linear-gradient(135deg,#7c5cfc,#00d4aa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.ln-stat-lbl { font-size:clamp(9px,1.2vw,12px); color:#6b6585; margin-top:3px; text-transform:uppercase; letter-spacing:.5px; }

.ln-section { font-family:'Syne',sans-serif; font-size:clamp(14px,2.2vw,18px); font-weight:700; margin:clamp(16px,3vw,26px) 0 clamp(8px,1.5vw,13px); }

.ln-card {
    background:#111118; border:0.5px solid rgba(255,255,255,0.08);
    border-radius:clamp(12px,1.8vw,16px);
    padding:clamp(16px,3vw,28px); margin-bottom:clamp(10px,1.5vw,16px);
    position:relative; overflow:hidden; animation:fadeUp .5s ease;
    word-break:break-word; overflow-wrap:break-word;
}
.ln-card-top { position:absolute;top:0;left:0;right:0;height:2px; }
.ln-card-header { display:flex;align-items:center;gap:10px;margin-bottom:clamp(10px,2vw,16px); }
.ln-card-icon {
    width:clamp(28px,4vw,36px); height:clamp(28px,4vw,36px);
    border-radius:9px; display:flex;align-items:center;justify-content:center;
    font-size:clamp(13px,2vw,17px); background:#18181f; flex-shrink:0;
}
.ln-card-title { font-family:'Syne',sans-serif; font-size:clamp(13px,2vw,16px); font-weight:700; color:#f0eeff; }
.ln-card-body { color:#b8b4d0; font-size:clamp(13px,1.8vw,15px); line-height:1.75; }

.ln-bubble-user { display:flex;justify-content:flex-end;margin-bottom:10px; }
.ln-bubble-user > div {
    background:rgba(124,92,252,0.14); border:0.5px solid rgba(124,92,252,0.28);
    border-radius:14px 14px 4px 14px;
    padding:clamp(9px,1.8vw,13px) clamp(11px,2vw,16px);
    max-width:min(85%,520px); color:#f0eeff;
    font-size:clamp(13px,1.8vw,15px); line-height:1.6; word-break:break-word;
}
.ln-bubble-ai { display:flex;justify-content:flex-start;margin-bottom:10px; }
.ln-bubble-ai > div {
    background:#111118; border:0.5px solid rgba(255,255,255,0.08);
    border-radius:14px 14px 14px 4px;
    padding:clamp(9px,1.8vw,13px) clamp(11px,2vw,16px);
    max-width:min(85%,520px); color:#b8b4d0;
    font-size:clamp(13px,1.8vw,15px); line-height:1.65; word-break:break-word;
}

.ln-warn {
    background:rgba(255,107,107,0.09); color:#ff9090;
    padding:clamp(10px,2vw,14px) clamp(13px,2.5vw,18px);
    border-radius:12px; border-left:3px solid #ff6b6b;
    font-weight:500; font-size:clamp(13px,1.8vw,15px); margin-bottom:14px;
}

.ln-prev { margin-bottom:14px; }
.ln-prev-label { font-size:11px;color:#6b6585;text-transform:uppercase;letter-spacing:.7px;margin-bottom:5px; }
.ln-prev-title { font-family:'Syne',sans-serif;font-size:clamp(15px,2.5vw,20px);font-weight:700;color:#f0eeff; }

.ln-sb-logo { padding:12px 0 5px; }
.ln-sb-logo-text {
    font-family:'Syne',sans-serif; font-size:18px; font-weight:800;
    background:linear-gradient(135deg,#7c5cfc,#00d4aa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:3px;
}
.ln-sb-welcome { font-size:12px; color:#6b6585 !important; }
.ln-sb-welcome span { color:#a98bff !important; }
.ln-sb-hist-label { margin-top:16px;font-size:11px;color:#6b6585 !important;text-transform:uppercase;letter-spacing:.7px;font-weight:600;margin-bottom:7px; }

@media (min-width:481px) and (max-width:768px) {
    .ln-h1 { font-size: clamp(30px, 5.5vw, 44px); }
    .ln-card { padding: 20px; }
    .ln-stats { gap: 10px; }
}
@media (max-width:480px) {
    .ln-hero { padding: 14px 0 6px; }
    div.stButton > button { min-height: 52px !important; font-size: 15px !important; }
    div[data-testid="stTextInput"] input { font-size: 16px !important; min-height: 52px !important; }
    .ln-stats { gap: 5px; }
    .ln-stat { padding: 11px 5px; }
    .ln-stat-num { font-size: 17px; }
    .ln-stat-lbl { font-size: 8px; }
    .ln-card { padding: 15px; border-radius: 12px; }
    .ln-bubble-user > div, .ln-bubble-ai > div { max-width: 92%; }
}
@media (min-width:1100px) {
    .stApp::before { width: 650px; height: 650px; }
    .stApp::after  { width: 550px; height: 550px; }
    .ln-h1 { font-size: 58px; }
}
</style>
""", unsafe_allow_html=True)


# ================================================================
#  COMPONENTS
# ================================================================

def hero_banner(title: str, subtitle: str, tag: str = ""):
    badge = f'<div class="ln-badge"><span class="ln-dot"></span>{tag}</div><br>' if tag else ""
    st.markdown(f"""
    <div class="ln-hero">
        {badge}
        <h1 class="ln-h1">{title}</h1>
        <p class="ln-sub">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def stat_row():
    st.markdown("""
    <div class="ln-stats">
        <div class="ln-stat"><div class="ln-stat-num">500+</div><div class="ln-stat-lbl">Topics</div></div>
        <div class="ln-stat"><div class="ln-stat-num">10K+</div><div class="ln-stat-lbl">Learners</div></div>
        <div class="ln-stat"><div class="ln-stat-num">∞</div><div class="ln-stat-lbl">Possibilities</div></div>
    </div>
    """, unsafe_allow_html=True)


def result_card(icon: str, title: str, content: str, accent: str = "#7c5cfc"):
    st.markdown(f"""
    <div class="ln-card">
        <div class="ln-card-top" style="background:linear-gradient(90deg,transparent,{accent},transparent);"></div>
        <div class="ln-card-header">
            <div class="ln-card-icon">{icon}</div>
            <div class="ln-card-title">{title}</div>
        </div>
        <div class="ln-card-body">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def section_header(text: str, color: str = "#a98bff"):
    st.markdown(f'<div class="ln-section" style="color:{color};">{text}</div>', unsafe_allow_html=True)


# ================================================================
#  AUTH PAGES
# ================================================================

def page_login():
    hero_banner("Welcome Back ⚡", "Sign in to continue your personalized learning journey.", "AI-Powered Learning")

    _, col, _ = st.columns([1, 3, 1])
    with col:
        username = st.text_input("Username", placeholder="Enter your username", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("🔐 Sign In", use_container_width=True):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")


def page_signup():
    hero_banner("Join Learnova 🚀", "Create your account and start learning with AI today.", "Get Started Free")

    _, col, _ = st.columns([1, 3, 1])
    with col:
        new_user = st.text_input("Choose Username", placeholder="Pick a cool username", key="signup_user")
        new_pass = st.text_input("Create Password", type="password", placeholder="Strong password", key="signup_pass")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("✨ Create Account", use_container_width=True):
            if signup_user(new_user, new_pass):
                st.success("Account created ✅ Now login!")
            else:
                st.error("Username already exists ❌")


# ================================================================
#  MAIN APP
# ================================================================

def page_main():
    # ---- SIDEBAR (desktop) — logout + history only ----
    with st.sidebar:
        st.markdown(f"""
        <div class="ln-sb-logo">
            <div class="ln-sb-logo-text">⚡ Learnova</div>
            <div class="ln-sb-welcome">Welcome back, <span>{st.session_state.username}</span></div>
        </div>
        <hr style="border-color:rgba(255,255,255,0.07);margin:10px 0;">
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.chat_history = []
            st.rerun()

        st.markdown('<div class="ln-sb-hist-label">📂 History</div>', unsafe_allow_html=True)

        history = get_history(st.session_state.username)
        for i, (q, r) in enumerate(history[::-1][:10]):
            label = q[:24] + ("…" if len(q) > 24 else "")
            if st.button(f"🔖 {label}", key=f"hist_{i}", use_container_width=True):
                st.session_state.selected_query = q
                st.session_state.selected_response = r
                st.session_state.chat_history = []

    # ---- MOBILE TOP BAR (info only, no logout button) ----
    st.markdown(f"""
    <div class="ln-mobile-bar">
        <span class="ln-mobile-logo">⚡ Learnova</span>
        <span class="ln-mobile-user">👤 {st.session_state.username}</span>
    </div>
    """, unsafe_allow_html=True)

    # ---- HERO ----
    hero_banner(
        "Learn Anything.<br>Master Everything.",
        "Enter any topic and get a personalized roadmap, deep explanation, and curated resources — instantly.",
        "AI-Powered Learning Mentor"
    )
    stat_row()

    # ---- INPUT ----
    section_header("📚 Enter Topic")
    topic = st.text_input("", placeholder="e.g. Machine Learning, React, Quantum Physics...",
                          key="topic_input", label_visibility="collapsed")
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        generate_clicked = st.button("✨ Generate", use_container_width=True)

    # ---- GENERATE ----
    if generate_clicked:
        if not topic:
            st.markdown('<div class="ln-warn">⚠️ Please enter a topic first.</div>', unsafe_allow_html=True)
        else:
            st.session_state.chat_history = []
            st.session_state.selected_query = None
            st.session_state.selected_response = None
            with st.spinner("🤖 Generating your personalized learning plan..."):
                roadmap     = generate_roadmap(topic)
                explanation = generate_explanation(topic)
                resources   = generate_resources(topic)
            result_card("🗺️", "Learning Roadmap", roadmap,     "#7c5cfc")
            result_card("📘", "Explanation",       explanation, "#00d4aa")
            result_card("🔗", "Resources",         resources,   "#ff6b6b")
            save_history(st.session_state.username, topic, f"{roadmap}\n\n{explanation}\n\n{resources}")

    # ---- PREVIOUS SEARCH ----
    if st.session_state.selected_query:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="ln-prev">
            <div class="ln-prev-label">📌 Previous Search</div>
            <div class="ln-prev-title">{st.session_state.selected_query}</div>
        </div>
        """, unsafe_allow_html=True)
        result_card("📋", "Saved Response", st.session_state.selected_response, "#7c5cfc")

    # ---- CHATBOT ----
    st.markdown("<hr>", unsafe_allow_html=True)
    section_header("🤖 Ask Learnova", "#c084fc")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="ln-bubble-user"><div>{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ln-bubble-ai"><div>{msg["content"]}</div></div>', unsafe_allow_html=True)

    chat_q = st.text_input("", placeholder="Ask anything about the topic...",
                           key="chat_input_box", label_visibility="collapsed")

    if st.button("Send"):
        if chat_q:
            st.session_state.chat_history.append({"role": "user", "content": chat_q})
            with st.spinner("Thinking..."):
                response = chatbot_response(chat_q)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    # ---- MOBILE HISTORY SECTION ----
    st.markdown("<hr>", unsafe_allow_html=True)
    section_header("📂 Search History", "#6b6585")
    history = get_history(st.session_state.username)
    if history:
        for i, (q, r) in enumerate(history[::-1][:10]):
            label = q[:40] + ("…" if len(q) > 40 else "")
            if st.button(f"🔖 {label}", key=f"mob_hist_{i}", use_container_width=True):
                st.session_state.selected_query = q
                st.session_state.selected_response = r
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.markdown('<p style="color:#6b6585;font-size:13px;text-align:center;">No history yet — generate something!</p>', unsafe_allow_html=True)


# ================================================================
#  ROUTER
# ================================================================
if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center;padding:18px 0 4px;">
        <span style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
            background:linear-gradient(135deg,#7c5cfc,#00d4aa);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;">⚡ Learnova</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    div[data-testid="stRadio"] {
        display: flex;
        justify-content: center;
        margin: 0 auto 8px auto;
    }
    div[data-testid="stRadio"] > div {
        display: flex;
        flex-direction: row;
        gap: 0;
        background: #111118;
        border: 1.5px solid rgba(124,92,252,0.4);
        border-radius: 999px;
        padding: 4px;
        width: fit-content;
    }
    div[data-testid="stRadio"] label {
        padding: 10px 32px !important;
        border-radius: 999px !important;
        cursor: pointer !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        color: #8884a0 !important;
        transition: all 0.2s !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, #7c5cfc, #5a3dd4) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div[data-testid="stRadio"] label p {
        color: inherit !important;
        -webkit-text-fill-color: inherit !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] input { display: none !important; }
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        menu_choice = st.radio("", ["Login", "Signup"], horizontal=True, label_visibility="collapsed", key="auth_menu")

    if menu_choice == "Login":
        st.markdown('<p style="text-align:center;color:#a98bff;font-family:\'Syne\',sans-serif;font-weight:700;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin:0 0 6px;">🔐 Login Page</p>', unsafe_allow_html=True)
        page_login()
    else:
        st.markdown('<p style="text-align:center;color:#00d4aa;font-family:\'Syne\',sans-serif;font-weight:700;font-size:13px;letter-spacing:1px;text-transform:uppercase;margin:0 0 6px;">✨ Signup Page</p>', unsafe_allow_html=True)
        page_signup()
else:
    page_main()
