import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MediCore.AI",
    layout="wide",
    page_icon="⚕️",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  ENCAPSULATION — DATA ENGINE
# ─────────────────────────────────────────────
class MediCoreEngine:
    PRIORITY_MAP = {
        "Critical": {"color": "#ef4444", "badge": "🔴"},
        "High":     {"color": "#f97316", "badge": "🟠"},
        "Stable":   {"color": "#22c55e", "badge": "🟢"},
        "Low":      {"color": "#38bdf8", "badge": "🔵"},
    }

    def __init__(self):
        if "db" not in st.session_state:
            st.session_state.db = pd.DataFrame([
                {"ID": "P-101", "Name": "Riya Sharma",   "Age": 28, "Condition": "Viral Flu",       "Priority": "Low",      "Doctor": "Dr. Mehta",  "Admitted": "2025-07-10"},
                {"ID": "P-102", "Name": "Aman Verma",    "Age": 45, "Condition": "Anemia",           "Priority": "Stable",   "Doctor": "Dr. Singh",  "Admitted": "2025-07-08"},
                {"ID": "P-103", "Name": "Priya Nair",    "Age": 62, "Condition": "Hypertension",     "Priority": "High",     "Doctor": "Dr. Kapoor", "Admitted": "2025-07-09"},
                {"ID": "P-104", "Name": "Rohan Das",     "Age": 35, "Condition": "Fracture (Tibia)", "Priority": "Stable",   "Doctor": "Dr. Mehta",  "Admitted": "2025-07-11"},
                {"ID": "P-105", "Name": "Sunita Joshi",  "Age": 71, "Condition": "Cardiac Arrhythmia","Priority": "Critical", "Doctor": "Dr. Kapoor", "Admitted": "2025-07-11"},
            ])
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    def add_patient(self, name, age, diagnosis, priority, doctor):
        new_id = f"P-{100 + len(st.session_state.db) + 1}"
        row = {"ID": new_id, "Name": name, "Age": age,
               "Condition": diagnosis, "Priority": priority,
               "Doctor": doctor, "Admitted": datetime.today().strftime("%Y-%m-%d")}
        st.session_state.db = pd.concat(
            [st.session_state.db, pd.DataFrame([row])], ignore_index=True
        )
        return new_id

    def get_stats(self):
        df = st.session_state.db
        return {
            "total": len(df),
            "critical": len(df[df["Priority"] == "Critical"]),
            "stable": len(df[df["Priority"].isin(["Stable", "Low"])]),
            "high": len(df[df["Priority"] == "High"]),
        }

engine = MediCoreEngine()

# ─────────────────────────────────────────────
#  GLOBAL CSS — Obsidian-Glass Medical Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root Variables ───────────────────────────── */
:root {
    --bg:        #060d1a;
    --surface:   #0d1b2e;
    --glass:     rgba(255,255,255,0.04);
    --border:    rgba(255,255,255,0.08);
    --accent:    #00e5ff;
    --accent2:   #7c3aed;
    --green:     #00d68f;
    --red:       #ff4d6d;
    --orange:    #ff9f43;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --font-head: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
}

/* ── Base ─────────────────────────────────────── */
html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

/* remove default top padding */
.block-container { padding-top: 1.5rem !important; }

/* ── Sidebar ──────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #060d1a 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
    padding: 6px 4px !important;
    border-radius: 6px;
    transition: color 0.2s;
}
section[data-testid="stSidebar"] .stRadio label:hover { color: var(--accent) !important; }

/* ── Headings ─────────────────────────────────── */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: var(--font-head) !important;
    color: var(--text) !important;
    letter-spacing: -0.03em;
}

/* ── Glass Card ───────────────────────────────── */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 28px;
    backdrop-filter: blur(12px);
    transition: transform 0.2s, box-shadow 0.2s;
}
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 40px rgba(0,229,255,0.07);
}

/* ── Metric Cards ─────────────────────────────── */
[data-testid="stMetricValue"] {
    font-family: var(--font-head) !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: var(--accent) !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-body) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
[data-testid="metric-container"] {
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 18px 22px !important;
}

/* ── Buttons ──────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #0284c7) !important;
    color: #060d1a !important;
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    letter-spacing: 0.04em !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ───────────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #0d1b2e !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.15) !important;
}

/* ── Dataframe ────────────────────────────────── */
.stDataFrame, [data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Chat ─────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
}

/* ── Info / Success / Error boxes ────────────── */
.stSuccess { background: rgba(0,214,143,0.1) !important; border-color: var(--green) !important; border-radius: 10px !important; }
.stInfo    { background: rgba(0,229,255,0.08) !important; border-color: var(--accent) !important; border-radius: 10px !important; }
.stWarning { background: rgba(255,159,67,0.1) !important; border-color: var(--orange) !important; border-radius: 10px !important; }
.stError   { background: rgba(255,77,109,0.1) !important; border-color: var(--red) !important; border-radius: 10px !important; }

/* ── Divider ──────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── Tabs ─────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; }
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-body) !important;
    color: var(--muted) !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] { color: var(--accent) !important; border-bottom: 2px solid var(--accent) !important; }

/* ── Priority Badges ──────────────────────────── */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: var(--font-body);
    letter-spacing: 0.05em;
}
.badge-critical { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
.badge-high     { background: rgba(249,115,22,0.15); color: #f97316; border: 1px solid rgba(249,115,22,0.3); }
.badge-stable   { background: rgba(34,197,94,0.15);  color: #22c55e; border: 1px solid rgba(34,197,94,0.3); }
.badge-low      { background: rgba(56,189,248,0.15); color: #38bdf8; border: 1px solid rgba(56,189,248,0.3); }

/* ── Hero Banner ──────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0d2137 0%, #0a1628 50%, #0d1b2e 100%);
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(0,229,255,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(124,58,237,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: var(--font-head);
    font-size: 2rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.04em;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-title span { color: var(--accent); }
.hero-sub { color: var(--muted); font-size: 0.95rem; margin: 0; line-height: 1.6; }

/* ── Section Title ────────────────────────────── */
.section-title {
    font-family: var(--font-head);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
    margin-bottom: 4px;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: var(--muted);
}

/* ── Status dot ───────────────────────────────── */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 6px var(--green);
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; }
    50%      { opacity:0.4; }
}

/* ── Scrollbar ────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='padding: 8px 0 20px 0;'>
            <div style='font-family:"Syne",sans-serif; font-size:1.5rem; font-weight:800;
                        color:#00e5ff; letter-spacing:-0.03em;'>⚕️ MediCore<span style='color:#7c3aed;'>.AI</span></div>
            <div style='font-size:0.7rem; color:#64748b; letter-spacing:0.1em;
                        text-transform:uppercase; margin-top:2px;'>Clinical Intelligence OS</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem;color:#64748b;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;'>Navigation</div>", unsafe_allow_html=True)

    menu = st.radio(
        "MODULES",
        ["📊  Dashboard", "🤖  AI Chatbot", "🧪  Symptom Checker", "👨‍⚕️  Patient Records", "➕  Add Patient"],
        label_visibility="collapsed"
    )

    st.divider()

    stats = engine.get_stats()
    st.markdown(f"""
        <div style='font-size:0.7rem;color:#64748b;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px;'>System Status</div>
        <div style='display:flex;align-items:center;margin-bottom:8px;'>
            <span class='status-dot'></span>
            <span style='font-size:0.82rem;color:#e2e8f0;'>All systems operational</span>
        </div>
        <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                    border-radius:10px;padding:12px 14px;font-size:0.8rem;color:#94a3b8;'>
            🔐 AES-256 Encrypted<br>
            📅 {datetime.today().strftime("%d %b %Y")}<br>
            🏥 {stats['total']} Active Patients
        </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────
if "Dashboard" in menu:
    stats = engine.get_stats()

    st.markdown(f"""
        <div class='hero-banner'>
            <p class='hero-title'>Welcome back,<br><span>Dr. Admin</span></p>
            <p class='hero-sub'>
                {stats['critical']} critical patient{"s" if stats["critical"]!=1 else ""} require immediate attention.
                All AI diagnostic services running normally.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ── Metrics row ──
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Patients", stats["total"], "+2 today")
    with c2: st.metric("Critical", stats["critical"], delta_color="inverse")
    with c3: st.metric("Stable / Low", stats["stable"])
    with c4: st.metric("AI Accuracy", "94.5%", "+0.3%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown("### 📈 Weekly Patient Inflow")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        inflow = [12, 18, 22, 35, 29, 41, 33]
        chart_df = pd.DataFrame({"Patients": inflow}, index=days)
        st.area_chart(chart_df, color="#00e5ff", use_container_width=True, height=220)

    with col_right:
        st.markdown("### 🗂 Priority Breakdown")
        df = st.session_state.db
        priority_counts = df["Priority"].value_counts()
        priority_df = pd.DataFrame({
            "Priority": priority_counts.index,
            "Count": priority_counts.values
        })
        st.dataframe(
            priority_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Priority": st.column_config.TextColumn("Priority Level"),
                "Count": st.column_config.ProgressColumn("Patients", max_value=int(priority_counts.max()) + 2, format="%d"),
            }
        )

    st.divider()
    st.markdown("### 🚨 Critical & High Priority Patients")
    urgent_df = df[df["Priority"].isin(["Critical", "High"])].reset_index(drop=True)
    if urgent_df.empty:
        st.info("No critical patients currently.")
    else:
        st.dataframe(
            urgent_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Priority": st.column_config.TextColumn("Priority"),
                "Admitted": st.column_config.DateColumn("Admitted", format="DD MMM YYYY"),
            }
        )

# ─────────────────────────────────────────────
#  AI CHATBOT
# ─────────────────────────────────────────────
elif "Chatbot" in menu:
    st.markdown("## 🤖 Neural Core — Dr. Aria")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>AI Clinical Assistant · Powered by MediCore Intelligence</p>", unsafe_allow_html=True)
    st.divider()

    ARIA_RESPONSES = {
        "fever":         "Fever may indicate viral/bacterial infection. Monitor temperature. If >103°F persists >48h, recommend full blood panel.",
        "headache":      "Headaches can stem from tension, dehydration, or migraines. Check BP and hydration levels first.",
        "chest pain":    "⚠️ Chest pain requires immediate evaluation. Rule out cardiac causes (ECG, troponin). Treat as urgent.",
        "cough":         "Persistent cough (>3 weeks) may indicate TB, asthma, or GERD. Chest X-ray advised.",
        "diabetes":      "Manage with HbA1c monitoring, diet control, and medication adherence. Target HbA1c <7%.",
        "hypertension":  "Target BP <130/80 mmHg. Lifestyle + pharmacotherapy. Monitor kidney function.",
        "help":          "I can assist with symptom analysis, medication queries, patient lookup, and protocol guidance.",
    }

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if not st.session_state.chat_history:
        with st.chat_message("assistant"):
            st.write("👋 Hello, Doctor. I'm **Dr. Aria**, your AI clinical assistant. Ask me about symptoms, medications, or patient protocols.")

    user_input = st.chat_input("Type a clinical query…")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        lower = user_input.lower()
        response = next(
            (v for k, v in ARIA_RESPONSES.items() if k in lower),
            f"I've logged your query: *\"{user_input}\"*. For complex diagnostics, please consult the clinical team or run a full symptom analysis."
        )

        with st.chat_message("assistant"):
            placeholder = st.empty()
            displayed = ""
            for char in response:
                displayed += char
                placeholder.markdown(displayed + "▌")
                time.sleep(0.012)
            placeholder.markdown(displayed)

        st.session_state.chat_history.append({"role": "assistant", "content": response})

# ─────────────────────────────────────────────
#  SYMPTOM CHECKER
# ─────────────────────────────────────────────
elif "Symptom" in menu:
    st.markdown("## 🧪 Symptom Analysis Engine")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>AI-powered triage and diagnosis suggestion</p>", unsafe_allow_html=True)
    st.divider()

    SYMPTOM_RULES = {
        frozenset(["Fever", "Cough", "Fatigue"]):         ("Viral Respiratory Infection", "Stable"),
        frozenset(["Chest Pain", "Shortness of Breath"]): ("Possible Cardiac Event — Urgent", "Critical"),
        frozenset(["Headache", "Dizziness", "Nausea"]):   ("Migraine / Vestibular Disorder", "High"),
        frozenset(["Fever", "Body Ache"]):                ("Dengue / Viral Fever", "High"),
        frozenset(["Fatigue", "Pale Skin"]):              ("Anemia", "Stable"),
        frozenset(["Frequent Urination", "Thirst"]):      ("Type 2 Diabetes — Screening", "Stable"),
    }

    col1, col2 = st.columns(2, gap="large")
    with col1:
        name = st.text_input("Patient Name", placeholder="Full name")
        age  = st.number_input("Age", min_value=1, max_value=120, value=30)
        doctor = st.selectbox("Attending Doctor", ["Dr. Mehta", "Dr. Singh", "Dr. Kapoor", "Dr. Rao"])
    with col2:
        symptoms = st.multiselect(
            "Select Symptoms",
            ["Fever", "Cough", "Fatigue", "Chest Pain", "Shortness of Breath",
             "Headache", "Dizziness", "Nausea", "Body Ache",
             "Pale Skin", "Frequent Urination", "Thirst"],
            placeholder="Choose symptoms…"
        )
        notes = st.text_area("Additional Notes", placeholder="Describe briefly…", height=100)

    if st.button("🔍 Run Analysis", use_container_width=True):
        if not name or not symptoms:
            st.warning("Please fill in patient name and at least one symptom.")
        else:
            with st.spinner("Analyzing symptoms…"):
                time.sleep(1.2)

            syms_set = frozenset(symptoms)
            diagnosis, priority = "General Illness — Further Tests Needed", "Low"
            for key, val in SYMPTOM_RULES.items():
                if key.issubset(syms_set):
                    diagnosis, priority = val
                    break

            new_id = engine.add_patient(name, age, diagnosis, priority, doctor)

            color_map = {"Critical": "#ef4444", "High": "#f97316", "Stable": "#22c55e", "Low": "#38bdf8"}
            badge_color = color_map.get(priority, "#38bdf8")

            st.markdown(f"""
                <div class='glass-card' style='border-color:{badge_color}40; margin-top:16px;'>
                    <div style='font-family:"Syne",sans-serif;font-size:1.2rem;font-weight:800;color:#fff;margin-bottom:12px;'>
                        ✅ Analysis Complete — {new_id}
                    </div>
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;'>
                        <div><span style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;'>Patient</span><br>
                             <span style='color:#e2e8f0;font-weight:500;'>{name}, {age}y</span></div>
                        <div><span style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;'>Doctor</span><br>
                             <span style='color:#e2e8f0;font-weight:500;'>{doctor}</span></div>
                        <div><span style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;'>Diagnosis</span><br>
                             <span style='color:#e2e8f0;font-weight:500;'>{diagnosis}</span></div>
                        <div><span style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;'>Priority</span><br>
                             <span style='color:{badge_color};font-weight:700;'>{priority}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PATIENT RECORDS
# ─────────────────────────────────────────────
elif "Records" in menu:
    st.markdown("## 👨‍⚕️ Patient Records Archive")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>Live database · All entries encrypted</p>", unsafe_allow_html=True)
    st.divider()

    df = st.session_state.db.copy()

    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search = st.text_input("🔍 Search by name or condition", placeholder="Search…")
    with col_filter:
        priority_filter = st.selectbox("Filter by Priority", ["All", "Critical", "High", "Stable", "Low"])

    if search:
        df = df[df["Name"].str.contains(search, case=False) | df["Condition"].str.contains(search, case=False)]
    if priority_filter != "All":
        df = df[df["Priority"] == priority_filter]

    st.markdown(f"<p style='color:#64748b;font-size:0.85rem;'>Showing {len(df)} record(s)</p>", unsafe_allow_html=True)

    st.dataframe(
        df.reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID":        st.column_config.TextColumn("Patient ID", width="small"),
            "Name":      st.column_config.TextColumn("Full Name"),
            "Age":       st.column_config.NumberColumn("Age", format="%d yrs", width="small"),
            "Condition": st.column_config.TextColumn("Diagnosis"),
            "Priority":  st.column_config.TextColumn("Priority"),
            "Doctor":    st.column_config.TextColumn("Attending"),
            "Admitted":  st.column_config.DateColumn("Admitted", format="DD MMM YYYY"),
        },
        height=420,
    )

    st.download_button(
        "⬇️ Export as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"medicore_records_{datetime.today().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────
#  ADD PATIENT
# ─────────────────────────────────────────────
elif "Add Patient" in menu:
    st.markdown("## ➕ Register New Patient")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>Manually enter patient admission details</p>", unsafe_allow_html=True)
    st.divider()

    with st.form("add_patient_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name     = st.text_input("Full Name *", placeholder="e.g. Neha Gupta")
            age      = st.number_input("Age *", min_value=1, max_value=120, value=25)
            priority = st.selectbox("Priority Level *", ["Low", "Stable", "High", "Critical"])
        with c2:
            diagnosis = st.text_input("Diagnosis *", placeholder="e.g. Dengue Fever")
            doctor    = st.selectbox("Attending Doctor *", ["Dr. Mehta", "Dr. Singh", "Dr. Kapoor", "Dr. Rao"])
            notes     = st.text_area("Clinical Notes", placeholder="Optional notes…", height=108)

        submitted = st.form_submit_button("✅ Register Patient", use_container_width=True)

        if submitted:
            if not name or not diagnosis:
                st.error("Name and Diagnosis are required fields.")
            else:
                new_id = engine.add_patient(name, age, diagnosis, priority, doctor)
                st.success(f"Patient **{name}** successfully registered as **{new_id}**.")
                st.balloons()
