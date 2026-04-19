
Om Yadav
1:12 AM (0 minutes ago)
to me

import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta
import json
import hashlib

# ─────────────────────────────────────────────
#  PAGE CONFIG (must be first Streamlit call)
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
        "Critical": {"color": "#ef4444", "badge": "🔴", "weight": 4},
        "High":     {"color": "#f97316", "badge": "🟠", "weight": 3},
        "Stable":   {"color": "#22c55e", "badge": "🟢", "weight": 2},
        "Low":      {"color": "#38bdf8", "badge": "🔵", "weight": 1},
    }
   
    DOCTORS = ["Dr. Mehta", "Dr. Singh", "Dr. Kapoor", "Dr. Rao", "Dr. Patel", "Dr. Sharma"]
   
    DEPARTMENTS = ["Cardiology", "Neurology", "Orthopedics", "General Medicine",
                   "Pulmonology", "Gastroenterology", "Emergency"]
   
    MEDICATIONS = {
        "Viral Flu": ["Paracetamol 500mg", "Cetirizine 10mg", "Vitamin C"],
        "Anemia": ["Iron Supplements", "Folic Acid", "Vitamin B12"],
        "Hypertension": ["Amlodipine 5mg", "Losartan 50mg", "Hydrochlorothiazide"],
        "Fracture (Tibia)": ["Ibuprofen 400mg", "Calcium Supplements", "Physiotherapy"],
        "Cardiac Arrhythmia": ["Beta Blockers", "Amiodarone", "Aspirin 75mg"],
        "Dengue Fever": ["Paracetamol", "ORS", "Platelet Monitoring"],
        "Migraine": ["Sumatriptan", "Propranolol", "Avoid triggers"],
        "Type 2 Diabetes": ["Metformin 500mg", "Glimepiride", "Diet Control"],
    }

    def __init__(self):
        self._initialize_database()
        self._initialize_appointments()
        self._initialize_vitals()
        self._initialize_notifications()
        self._initialize_audit_log()
   
    def _initialize_database(self):
        if "db" not in st.session_state:
            st.session_state.db = pd.DataFrame([
                {"ID": "P-101", "Name": "Riya Sharma", "Age": 28, "Gender": "Female",
                 "Condition": "Viral Flu", "Priority": "Low", "Doctor": "Dr. Mehta",
                 "Department": "General Medicine", "Admitted": "2025-07-10",
                 "Room": "101-A", "Status": "Admitted", "Phone": "+91-9876543210",
                 "Emergency_Contact": "Rahul Sharma (+91-9876543211)", "Blood_Group": "B+"},
                {"ID": "P-102", "Name": "Aman Verma", "Age": 45, "Gender": "Male",
                 "Condition": "Anemia", "Priority": "Stable", "Doctor": "Dr. Singh",
                 "Department": "General Medicine", "Admitted": "2025-07-08",
                 "Room": "102-B", "Status": "Admitted", "Phone": "+91-9876543212",
                 "Emergency_Contact": "Priya Verma (+91-9876543213)", "Blood_Group": "O+"},
                {"ID": "P-103", "Name": "Priya Nair", "Age": 62, "Gender": "Female",
                 "Condition": "Hypertension", "Priority": "High", "Doctor": "Dr. Kapoor",
                 "Department": "Cardiology", "Admitted": "2025-07-09",
                 "Room": "ICU-01", "Status": "Critical Care", "Phone": "+91-9876543214",
                 "Emergency_Contact": "Arun Nair (+91-9876543215)", "Blood_Group": "A+"},
                {"ID": "P-104", "Name": "Rohan Das", "Age": 35, "Gender": "Male",
                 "Condition": "Fracture (Tibia)", "Priority": "Stable", "Doctor": "Dr. Mehta",
                 "Department": "Orthopedics", "Admitted": "2025-07-11",
                 "Room": "201-A", "Status": "Admitted", "Phone": "+91-9876543216",
                 "Emergency_Contact": "Sunita Das (+91-9876543217)", "Blood_Group": "AB+"},
                {"ID": "P-105", "Name": "Sunita Joshi", "Age": 71, "Gender": "Female",
                 "Condition": "Cardiac Arrhythmia", "Priority": "Critical", "Doctor": "Dr. Kapoor",
                 "Department": "Cardiology", "Admitted": "2025-07-11",
                 "Room": "ICU-02", "Status": "Critical Care", "Phone": "+91-9876543218",
                 "Emergency_Contact": "Vijay Joshi (+91-9876543219)", "Blood_Group": "O-"},
            ])
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
   
    def _initialize_appointments(self):
        if "appointments" not in st.session_state:
            today = datetime.today()
            st.session_state.appointments = pd.DataFrame([
                {"ID": "APT-001", "Patient": "Riya Sharma", "Doctor": "Dr. Mehta",
                 "Date": (today + timedelta(days=1)).strftime("%Y-%m-%d"), "Time": "10:00 AM",
                 "Type": "Follow-up", "Status": "Scheduled"},
                {"ID": "APT-002", "Patient": "Aman Verma", "Doctor": "Dr. Singh",
                 "Date": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "Time": "11:30 AM",
                 "Type": "Lab Review", "Status": "Scheduled"},
                {"ID": "APT-003", "Patient": "New Patient", "Doctor": "Dr. Kapoor",
                 "Date": today.strftime("%Y-%m-%d"), "Time": "02:00 PM",
                 "Type": "Consultation", "Status": "Pending"},
            ])
   
    def _initialize_vitals(self):
        if "vitals_history" not in st.session_state:
            st.session_state.vitals_history = {}
            for pid in ["P-101", "P-102", "P-103", "P-104", "P-105"]:
                st.session_state.vitals_history[pid] = self._generate_vitals_history(pid)
   
    def _generate_vitals_history(self, patient_id):
        history = []
        base_date = datetime.today() - timedelta(days=7)
        for i in range(7):
            history.append({
                "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
                "heart_rate": random.randint(65, 95),
                "bp_systolic": random.randint(110, 140),
                "bp_diastolic": random.randint(70, 90),
                "temperature": round(random.uniform(97.5, 99.5), 1),
                "oxygen": random.randint(94, 100),
                "respiratory_rate": random.randint(14, 20),
            })
        return history
   
    def _initialize_notifications(self):
        if "notifications" not in st.session_state:
            st.session_state.notifications = [
                {"id": 1, "type": "critical", "message": "P-105 Sunita Joshi requires immediate attention",
                 "time": "5 mins ago", "read": False},
                {"id": 2, "type": "warning", "message": "Lab results pending for P-102",
                 "time": "1 hour ago", "read": False},
                {"id": 3, "type": "info", "message": "Dr. Kapoor rounds at 3:00 PM",
                 "time": "2 hours ago", "read": True},
                {"id": 4, "type": "success", "message": "P-101 vitals stabilized",
                 "time": "3 hours ago", "read": True},
            ]
   
    def _initialize_audit_log(self):
        if "audit_log" not in st.session_state:
            st.session_state.audit_log = []

    def add_patient(self, name, age, gender, diagnosis, priority, doctor, department,
                    room, phone, emergency_contact, blood_group):
        new_id = f"P-{100 + len(st.session_state.db) + 1}"
        row = {
            "ID": new_id, "Name": name, "Age": age, "Gender": gender,
            "Condition": diagnosis, "Priority": priority, "Doctor": doctor,
            "Department": department, "Admitted": datetime.today().strftime("%Y-%m-%d"),
            "Room": room, "Status": "Admitted", "Phone": phone,
            "Emergency_Contact": emergency_contact, "Blood_Group": blood_group
        }
        st.session_state.db = pd.concat(
            [st.session_state.db, pd.DataFrame([row])], ignore_index=True
        )
        st.session_state.vitals_history[new_id] = self._generate_vitals_history(new_id)
        self._add_audit_log("Patient Added", f"New patient {name} registered as {new_id}")
        return new_id
   
    def update_patient(self, patient_id, updates):
        idx = st.session_state.db[st.session_state.db["ID"] == patient_id].index
        if len(idx) > 0:
            for key, value in updates.items():
                st.session_state.db.loc[idx[0], key] = value
            self._add_audit_log("Patient Updated", f"Patient {patient_id} record modified")
            return True
        return False
   
    def discharge_patient(self, patient_id):
        idx = st.session_state.db[st.session_state.db["ID"] == patient_id].index
        if len(idx) > 0:
            patient_name = st.session_state.db.loc[idx[0], "Name"]
            st.session_state.db.loc[idx[0], "Status"] = "Discharged"
            self._add_audit_log("Patient Discharged", f"Patient {patient_name} ({patient_id}) discharged")
            return True
        return False
   
    def add_appointment(self, patient, doctor, date, time, apt_type):
        new_id = f"APT-{len(st.session_state.appointments) + 1:03d}"
        row = {
            "ID": new_id, "Patient": patient, "Doctor": doctor,
            "Date": date, "Time": time, "Type": apt_type, "Status": "Scheduled"
        }
        st.session_state.appointments = pd.concat(
            [st.session_state.appointments, pd.DataFrame([row])], ignore_index=True
        )
        self._add_audit_log("Appointment Created", f"New appointment {new_id} for {patient}")
        return new_id
   
    def record_vitals(self, patient_id, vitals):
        if patient_id in st.session_state.vitals_history:
            vitals["date"] = datetime.today().strftime("%Y-%m-%d")
            st.session_state.vitals_history[patient_id].append(vitals)
            self._add_audit_log("Vitals Recorded", f"Vitals updated for {patient_id}")
            return True
        return False
   
    def _add_audit_log(self, action, details):
        st.session_state.audit_log.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "details": details,
            "user": "Dr. Admin"
        })

    def get_stats(self):
        df = st.session_state.db
        admitted = df[df["Status"] != "Discharged"]
        return {
            "total": len(admitted),
            "critical": len(admitted[admitted["Priority"] == "Critical"]),
            "stable": len(admitted[admitted["Priority"].isin(["Stable", "Low"])]),
            "high": len(admitted[admitted["Priority"] == "High"]),
            "discharged": len(df[df["Status"] == "Discharged"]),
            "icu": len(admitted[admitted["Room"].str.contains("ICU", na=False)]),
        }
   
    def get_patient(self, patient_id):
        df = st.session_state.db
        patient = df[df["ID"] == patient_id]
        if len(patient) > 0:
            return patient.iloc[0].to_dict()
        return None
   
    def get_medications(self, condition):
        for key in self.MEDICATIONS:
            if key.lower() in condition.lower():
                return self.MEDICATIONS[key]
        return ["Consult physician for medication"]
   
    def get_unread_notifications(self):
        return len([n for n in st.session_state.notifications if not n["read"]])

engine = MediCoreEngine()

# ─────────────────────────────────────────────
#  GLOBAL CSS — Obsidian-Glass Medical Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap)');

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

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

.block-container { padding-top: 1.5rem !important; }

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

h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: var(--font-head) !important;
    color: var(--text) !important;
    letter-spacing: -0.03em;
}

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

.stDataFrame, [data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

[data-testid="stChatMessage"] {
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
}

.stSuccess { background: rgba(0,214,143,0.1) !important; border-color: var(--green) !important; border-radius: 10px !important; }
.stInfo    { background: rgba(0,229,255,0.08) !important; border-color: var(--accent) !important; border-radius: 10px !important; }
.stWarning { background: rgba(255,159,67,0.1) !important; border-color: var(--orange) !important; border-radius: 10px !important; }
.stError   { background: rgba(255,77,109,0.1) !important; border-color: var(--red) !important; border-radius: 10px !important; }

hr { border-color: var(--border) !important; }

.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; }
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-body) !important;
    color: var(--muted) !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] { color: var(--accent) !important; border-bottom: 2px solid var(--accent) !important; }

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

.notification-badge {
    background: var(--red);
    color: white;
    border-radius: 50%;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-weight: 700;
    margin-left: 8px;
}

.patient-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    transition: all 0.2s;
}
.patient-card:hover {
    border-color: var(--accent);
    transform: translateX(4px);
}

.vital-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin: 4px;
}

.timeline-item {
    border-left: 2px solid var(--accent);
    padding-left: 20px;
    margin-left: 10px;
    padding-bottom: 20px;
    position: relative;
}
.timeline-item::before {
    content: '';
    position: absolute;
    left: -6px;
    top: 0;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--accent);
}

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
                        text-transform:uppercase; margin-top:2px;'>Clinical Intelligence OS v2.0</div>
        </div>
    """, unsafe_allow_html=True)
   
    unread = engine.get_unread_notifications()
    notification_badge = f"<span class='notification-badge'>{unread}</span>" if unread > 0 else ""
   
    st.markdown(f"<div style='font-size:0.7rem;color:#64748b;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;'>Navigation {notification_badge}</div>", unsafe_allow_html=True)

    menu = st.radio(
        "MODULES",
        ["📊  Dashboard", "🤖  AI Chatbot", "🧪  Symptom Checker", "👨‍⚕️  Patient Records",
         "📋  Patient Details", "📅  Appointments", "💊  Medications", "📈  Vitals Monitor",
         "🔔  Notifications", "➕  Add Patient", "📜  Audit Log"],
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
            🏥 {stats['total']} Active Patients<br>
            🚨 {stats['critical']} Critical<br>
            🛏️ {stats['icu']} in ICU
        </div>
    """, unsafe_allow_html=True)
   
    st.divider()
   
    # Quick Actions
    st.markdown("<div style='font-size:0.7rem;color:#64748b;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:10px;'>Quick Actions</div>", unsafe_allow_html=True)
   
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆘 Emergency", use_container_width=True):
            st.session_state.notifications.insert(0, {
                "id": len(st.session_state.notifications) + 1,
                "type": "critical",
                "message": "Emergency alert triggered!",
                "time": "Just now",
                "read": False
            })
            st.rerun()
    with col2:
        if st.button("📞 On-Call", use_container_width=True):
            st.info("On-call: Dr. Kapoor (Cardiology)")

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
                {stats['icu']} patient{"s" if stats["icu"]!=1 else ""} in ICU. All AI diagnostic services running normally.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Metrics row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.metric("Total Patients", stats["total"], "+2 today")
    with c2: st.metric("Critical", stats["critical"], delta_color="inverse")
    with c3: st.metric("High Priority", stats["high"], delta_color="off")
    with c4: st.metric("Stable / Low", stats["stable"])
    with c5: st.metric("ICU Beds Used", stats["icu"])
    with c6: st.metric("AI Accuracy", "94.5%", "+0.3%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        tab1, tab2 = st.tabs(["📈 Weekly Inflow", "🏥 Department Load"])
       
        with tab1:
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            inflow = [12, 18, 22, 35, 29, 41, 33]
            chart_df = pd.DataFrame({"Patients": inflow}, index=days)
            st.area_chart(chart_df, color="#00e5ff", use_container_width=True, height=220)
       
        with tab2:
            df = st.session_state.db[st.session_state.db["Status"] != "Discharged"]
            dept_counts = df["Department"].value_counts()
            dept_df = pd.DataFrame({"Department": dept_counts.index, "Patients": dept_counts.values})
            st.bar_chart(dept_df.set_index("Department"), color="#7c3aed", height=220)

    with col_right:
        st.markdown("### 🗂 Priority Breakdown")
        df = st.session_state.db[st.session_state.db["Status"] != "Discharged"]
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
       
        # Today's Appointments
        st.markdown("### 📅 Today's Appointments")
        today = datetime.today().strftime("%Y-%m-%d")
        today_apts = st.session_state.appointments[st.session_state.appointments["Date"] == today]
        if len(today_apts) > 0:
            for _, apt in today_apts.iterrows():
                st.markdown(f"""
                    <div class='patient-card'>
                        <div style='font-weight:600;color:#e2e8f0;'>{apt['Patient']}</div>
                        <div style='font-size:0.8rem;color:#64748b;'>{apt['Time']} · {apt['Doctor']} · {apt['Type']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appointments scheduled for today.")

    st.divider()
   
    # Critical Patients Section
    st.markdown("### 🚨 Critical & High Priority Patients")
    urgent_df = df[df["Priority"].isin(["Critical", "High"])].reset_index(drop=True)
    if urgent_df.empty:
        st.info("No critical patients currently.")
    else:
        st.dataframe(
            urgent_df[["ID", "Name", "Age", "Condition", "Priority", "Doctor", "Room", "Department"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Priority": st.column_config.TextColumn("Priority"),
                "Room": st.column_config.TextColumn("Room/Bed"),
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
        "fever": "Fever may indicate viral/bacterial infection. Monitor temperature. If >103°F persists >48h, recommend full blood panel. Consider antipyretics like Paracetamol 500mg every 6 hours.",
        "headache": "Headaches can stem from tension, dehydration, or migraines. Check BP and hydration levels first. For migraines, consider Sumatriptan if no contraindications.",
        "chest pain": "⚠️ **URGENT**: Chest pain requires immediate evaluation. Rule out cardiac causes (ECG, troponin). Check for radiation to arm/jaw, diaphoresis. Consider aspirin 325mg if MI suspected.",
        "cough": "Persistent cough (>3 weeks) may indicate TB, asthma, or GERD. Chest X-ray advised. For productive cough, consider mucolytics; for dry cough, antitussives.",
        "diabetes": "Manage with HbA1c monitoring (target <7%), diet control, and medication adherence. First-line: Metformin 500mg BD. Monitor renal function quarterly.",
        "hypertension": "Target BP <130/80 mmHg. Lifestyle modifications essential. First-line: ACE inhibitors or ARBs. Monitor kidney function and potassium levels.",
        "patient": "I can look up patient records. Please provide the patient ID (e.g., P-101) or name for detailed information.",
        "medication": "I can provide medication guidance. Please specify the condition or drug name for dosing information and contraindications.",
        "emergency": "🚨 For emergencies: 1) Secure airway, 2) Check breathing, 3) Assess circulation. Call code team if needed. What is the nature of the emergency?",
        "lab": "Common lab interpretations: CBC for infections/anemia, LFT for liver function, RFT for kidney function, HbA1c for diabetes control. Which test results need review?",
        "help": "I can assist with:\n• Symptom analysis & differential diagnosis\n• Medication queries & dosing\n• Patient lookup & records\n• Lab result interpretation\n• Clinical protocols & guidelines\n• Emergency procedures",
    }
   
    # Patient lookup capability
    def lookup_patient(query):
        df = st.session_state.db
        # Try ID match
        patient = df[df["ID"].str.lower() == query.lower()]
        if len(patient) == 0:
            # Try name match
            patient = df[df["Name"].str.lower().str.contains(query.lower())]
       
        if len(patient) > 0:
            p = patient.iloc[0]
            return f"""
**Patient Found: {p['Name']}** ({p['ID']})

| Field | Value |
|-------|-------|
| Age | {p['Age']} years ({p['Gender']}) |
| Condition | {p['Condition']} |
| Priority | {p['Priority']} |
| Doctor | {p['Doctor']} |
| Department | {p['Department']} |
| Room | {p['Room']} |
| Status | {p['Status']} |
| Blood Group | {p['Blood_Group']} |
| Admitted | {p['Admitted']} |

**Recommended Medications**: {', '.join(engine.get_medications(p['Condition']))}
"""
        return None

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if not st.session_state.chat_history:
        with st.chat_message("assistant"):
            st.markdown("""👋 Hello, Doctor. I'm **Dr. Aria**, your AI clinical assistant.

I can help you with:
- 🔍 Patient lookup (try "lookup P-101" or a patient name)
- 💊 Medication guidance
- 🩺 Symptom analysis
- 📋 Clinical protocols

What can I assist you with today?""")

    user_input = st.chat_input("Type a clinical query…")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        lower = user_input.lower()
        response = None
       
        # Check for patient lookup
        if "lookup" in lower or "find patient" in lower or "patient" in lower:
            # Extract potential patient ID or name
            words = user_input.split()
            for word in words:
                if word.upper().startswith("P-") or len(word) > 2:
                    result = lookup_patient(word)
                    if result:
                        response = result
                        break
       
        if not response:
            response = next(
                (v for k, v in ARIA_RESPONSES.items() if k in lower),
                f"I've logged your query: *\"{user_input}\"*. For complex diagnostics, please consult the clinical team or run a full symptom analysis in the Symptom Checker module."
            )

        with st.chat_message("assistant"):
            placeholder = st.empty()
            displayed = ""
            for char in response:
                displayed += char
                placeholder.markdown(displayed + "▌")
                time.sleep(0.008)
            placeholder.markdown(displayed)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
   
    # Quick query buttons
    st.markdown("---")
    st.markdown("**Quick Queries:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📋 Patient Lookup", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "How do I lookup a patient?"})
            st.rerun()
    with col2:
        if st.button("🚨 Emergency Protocol", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Emergency protocol"})
            st.rerun()
    with col3:
        if st.button("💊 Medication Help", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Help with medications"})
            st.rerun()
    with col4:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# ─────────────────────────────────────────────
#  SYMPTOM CHECKER
# ─────────────────────────────────────────────
elif "Symptom" in menu:
    st.markdown("## 🧪 Symptom Analysis Engine")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>AI-powered triage and diagnosis suggestion</p>", unsafe_allow_html=True)
    st.divider()

    SYMPTOM_RULES = {
        frozenset(["Fever", "Cough", "Fatigue"]):         ("Viral Respiratory Infection", "Stable", ["Rest", "Hydration", "Paracetamol PRN"]),
        frozenset(["Chest Pain", "Shortness of Breath"]): ("Possible Cardiac Event — Urgent", "Critical", ["ECG STAT", "Troponin", "Aspirin 325mg", "Cardiology consult"]),
        frozenset(["Headache", "Dizziness", "Nausea"]):   ("Migraine / Vestibular Disorder", "High", ["Dark quiet room", "Sumatriptan if indicated", "Antiemetics"]),
        frozenset(["Fever", "Body Ache"]):                ("Dengue / Viral Fever", "High", ["CBC with platelets", "NS Drip", "Paracetamol only"]),
        frozenset(["Fatigue", "Pale Skin"]):              ("Anemia", "Stable", ["CBC", "Iron studies", "Peripheral smear"]),
        frozenset(["Frequent Urination", "Thirst"]):      ("Type 2 Diabetes — Screening", "Stable", ["FBS", "HbA1c", "Renal panel"]),
        frozenset(["Fever", "Cough", "Chest Pain"]):      ("Pneumonia — Suspected", "High", ["Chest X-ray", "Sputum culture", "Start empirical antibiotics"]),
        frozenset(["Abdominal Pain", "Nausea", "Vomiting"]): ("Gastroenteritis / Acute Abdomen", "High", ["NPO", "IV fluids", "Ultrasound abdomen"]),
        frozenset(["Joint Pain", "Swelling", "Fever"]):   ("Septic Arthritis / Rheumatic Fever", "High", ["Joint aspiration", "ESR/CRP", "Blood culture"]),
    }

    col1, col2 = st.columns(2, gap="large")
    with col1:
        name = st.text_input("Patient Name *", placeholder="Full name")
        age  = st.number_input("Age *", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        doctor = st.selectbox("Attending Doctor", engine.DOCTORS)
    with col2:
        symptoms = st.multiselect(
            "Select Symptoms *",
            ["Fever", "Cough", "Fatigue", "Chest Pain", "Shortness of Breath",
             "Headache", "Dizziness", "Nausea", "Body Ache", "Vomiting",
             "Pale Skin", "Frequent Urination", "Thirst", "Abdominal Pain",
             "Joint Pain", "Swelling", "Loss of Appetite", "Weight Loss"],
            placeholder="Choose symptoms…"
        )
        department = st.selectbox("Department", engine.DEPARTMENTS)
        room = st.text_input("Room/Bed Assignment", placeholder="e.g., 101-A or ICU-01")
        notes = st.text_area("Additional Notes", placeholder="Describe briefly…", height=80)

    if st.button("🔍 Run Analysis", use_container_width=True):
        if not name or not symptoms:
            st.warning("Please fill in patient name and at least one symptom.")
        else:
            with st.spinner("Analyzing symptoms with AI engine…"):
                time.sleep(1.5)

            syms_set = frozenset(symptoms)
            diagnosis, priority, recommendations = "General Illness — Further Tests Needed", "Low", ["Consult physician", "Basic vitals monitoring"]
           
            # Find best matching rule
            best_match = None
            best_overlap = 0
            for key, val in SYMPTOM_RULES.items():
                overlap = len(key.intersection(syms_set))
                if overlap >= 2 and overlap > best_overlap:
                    best_match = val
                    best_overlap = overlap
           
            if best_match:
                diagnosis, priority, recommendations = best_match

            new_id = engine.add_patient(name, age, gender, diagnosis, priority, doctor,
                                        department, room if room else "TBA",
                                        "+91-0000000000", "Not provided", "Unknown")

            color_map = {"Critical": "#ef4444", "High": "#f97316", "Stable": "#22c55e", "Low": "#38bdf8"}
            badge_color = color_map.get(priority, "#38bdf8")

            st.markdown(f"""
                <div class='glass-card' style='border-color:{badge_color}40; margin-top:16px;'>
                    <div style='font-family:"Syne",sans-serif;font-size:1.3rem;font-weight:800;color:#fff;margin-bottom:16px;'>
                        ✅ Analysis Complete — {new_id}
                    </div>
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:16px;'>
                        <div><span style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;'>Patient</span><br>
                             <span style='color:#e2e8f0;font-weight:500;font-size:1.1rem;'>{name}, {age}y ({gender})</span></div>
                        <div><span style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;'>Doctor</span><br>
                             <span style='color:#e2e8f0;font-weight:500;font-size:1.1rem;'>{doctor}</span></div>
                        <div><span style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;'>AI Diagnosis</span><br>
                             <span style='color:#00e5ff;font-weight:600;font-size:1.1rem;'>{diagnosis}</span></div>
                        <div><span style='color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;'>Priority</span><br>
                             <span style='color:{badge_color};font-weight:700;font-size:1.1rem;'>{priority}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
           
            # Recommendations
            st.markdown("### 📋 AI Recommendations")
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}.** {rec}")
           
            # Add notification for critical
            if priority in ["Critical", "High"]:
                st.session_state.notifications.insert(0, {
                    "id": len(st.session_state.notifications) + 1,
                    "type": "critical" if priority == "Critical" else "warning",
                    "message": f"New {priority.lower()} patient: {name} - {diagnosis}",
                    "time": "Just now",
                    "read": False
                })

# ─────────────────────────────────────────────
#  PATIENT RECORDS
# ─────────────────────────────────────────────
elif "Records" in menu:
    st.markdown("## 👨‍⚕️ Patient Records Archive")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>Live database · All entries encrypted</p>", unsafe_allow_html=True)
    st.divider()

    df = st.session_state.db.copy()

    col_search, col_filter, col_status = st.columns([2, 1, 1])
    with col_search:
        search = st.text_input("🔍 Search by name, condition, or ID", placeholder="Search…")
    with col_filter:
        priority_filter = st.selectbox("Priority", ["All", "Critical", "High", "Stable", "Low"])
    with col_status:
        status_filter = st.selectbox("Status", ["All", "Admitted", "Critical Care", "Discharged"])

    if search:
        df = df[df["Name"].str.contains(search, case=False) |
                df["Condition"].str.contains(search, case=False) |
                df["ID"].str.contains(search, case=False)]
    if priority_filter != "All":
        df = df[df["Priority"] == priority_filter]
    if status_filter != "All":
        df = df[df["Status"] == status_filter]

    st.markdown(f"<p style='color:#64748b;font-size:0.85rem;'>Showing {len(df)} record(s)</p>", unsafe_allow_html=True)

    st.dataframe(
        df.reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID":         st.column_config.TextColumn("Patient ID", width="small"),
            "Name":       st.column_config.TextColumn("Full Name"),
            "Age":        st.column_config.NumberColumn("Age", format="%d yrs", width="small"),
            "Gender":     st.column_config.TextColumn("Gender", width="small"),
            "Condition":  st.column_config.TextColumn("Diagnosis"),
            "Priority":   st.column_config.TextColumn("Priority"),
            "Doctor":     st.column_config.TextColumn("Attending"),
            "Department": st.column_config.TextColumn("Department"),
            "Room":       st.column_config.TextColumn("Room"),
            "Status":     st.column_config.TextColumn("Status"),
            "Admitted":   st.column_config.DateColumn("Admitted", format="DD MMM YYYY"),
        },
        height=420,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "⬇️ Export as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"medicore_records_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col2:
        st.download_button(
            "📄 Export as JSON",
            data=df.to_json(orient="records", indent=2),
            file_name=f"medicore_records_{datetime.today().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )

# ─────────────────────────────────────────────
#  PATIENT DETAILS (NEW)
# ─────────────────────────────────────────────
elif "Patient Details" in menu:
    st.markdown("## 📋 Patient Details & Management")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>View and manage individual patient records</p>", unsafe_allow_html=True)
    st.divider()
   
    df = st.session_state.db
    patient_options = [f"{row['ID']} - {row['Name']}" for _, row in df.iterrows()]
   
    selected = st.selectbox("Select Patient", patient_options)
   
    if selected:
        patient_id = selected.split(" - ")[0]
        patient = engine.get_patient(patient_id)
       
        if patient:
            col1, col2 = st.columns([2, 1])
           
            with col1:
                priority_colors = {"Critical": "#ef4444", "High": "#f97316", "Stable": "#22c55e", "Low": "#38bdf8"}
                p_color = priority_colors.get(patient["Priority"], "#38bdf8")
               
                st.markdown(f"""
                    <div class='glass-card' style='border-left: 4px solid {p_color};'>
                        <div style='display:flex;justify-content:space-between;align-items:start;'>
                            <div>
                                <h2 style='margin:0;color:#fff;font-family:"Syne",sans-serif;'>{patient['Name']}</h2>
                                <p style='color:#64748b;margin:4px 0;'>{patient['ID']} · {patient['Age']} years · {patient['Gender']}</p>
                            </div>
                            <div style='text-align:right;'>
                                <span class='badge badge-{patient["Priority"].lower()}'>{patient['Priority']}</span>
                                <p style='color:#64748b;margin:4px 0;font-size:0.8rem;'>{patient['Status']}</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
               
                # Patient Information Tabs
                tab1, tab2, tab3 = st.tabs(["📊 Overview", "📝 Edit Details", "🏥 Discharge"])
               
                with tab1:
                    info_col1, info_col2 = st.columns(2)
                    with info_col1:
                        st.markdown("**Medical Information**")
                        st.write(f"🩺 **Condition:** {patient['Condition']}")
                        st.write(f"👨‍⚕️ **Doctor:** {patient['Doctor']}")
                        st.write(f"🏥 **Department:** {patient['Department']}")
                        st.write(f"🛏️ **Room:** {patient['Room']}")
                        st.write(f"📅 **Admitted:** {patient['Admitted']}")
                   
                    with info_col2:
                        st.markdown("**Contact Information**")
                        st.write(f"📞 **Phone:** {patient['Phone']}")
                        st.write(f"🆘 **Emergency:** {patient['Emergency_Contact']}")
                        st.write(f"🩸 **Blood Group:** {patient['Blood_Group']}")
                   
                    st.markdown("---")
                    st.markdown("**Recommended Medications**")
                    meds = engine.get_medications(patient['Condition'])
                    for med in meds:
                        st.markdown(f"• {med}")
               
                with tab2:
                    with st.form("edit_patient"):
                        new_condition = st.text_input("Condition", value=patient['Condition'])
                        new_priority = st.selectbox("Priority", ["Low", "Stable", "High", "Critical"],
                                                   index=["Low", "Stable", "High", "Critical"].index(patient['Priority']))
                        new_doctor = st.selectbox("Doctor", engine.DOCTORS,
                                                 index=engine.DOCTORS.index(patient['Doctor']) if patient['Doctor'] in engine.DOCTORS else 0)
                        new_room = st.text_input("Room", value=patient['Room'])
                        new_status = st.selectbox("Status", ["Admitted", "Critical Care", "Stable", "Recovering"])
                       
                        if st.form_submit_button("💾 Save Changes", use_container_width=True):
                            engine.update_patient(patient_id, {
                                "Condition": new_condition,
                                "Priority": new_priority,
                                "Doctor": new_doctor,
                                "Room": new_room,
                                "Status": new_status
                            })
                            st.success("Patient record updated successfully!")
                            st.rerun()
               
                with tab3:
                    st.warning("⚠️ This action will mark the patient as discharged.")
                    discharge_notes = st.text_area("Discharge Notes", placeholder="Enter discharge summary...")
                   
                    if st.button("🚪 Discharge Patient", type="primary", use_container_width=True):
                        if engine.discharge_patient(patient_id):
                            st.success(f"Patient {patient['Name']} has been discharged.")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
           
            with col2:
                st.markdown("### 📈 Recent Vitals")
                if patient_id in st.session_state.vitals_history:
                    vitals = st.session_state.vitals_history[patient_id][-1]
                    st.markdown(f"""
                        <div class='vital-indicator'>❤️ HR: <strong>{vitals['heart_rate']} bpm</strong></div>
                        <div class='vital-indicator'>🩸 BP: <strong>{vitals['bp_systolic']}/{vitals['bp_diastolic']}</strong></div>
                        <div class='vital-indicator'>🌡️ Temp: <strong>{vitals['temperature']}°F</strong></div>
                        <div class='vital-indicator'>💨 O₂: <strong>{vitals['oxygen']}%</strong></div>
                        <div class='vital-indicator'>🫁 RR: <strong>{vitals['respiratory_rate']}/min</strong></div>
                    """, unsafe_allow_html=True)
               
                st.markdown("---")
                st.markdown("### 🕐 Timeline")
                st.markdown(f"""
                    <div class='timeline-item'>
                        <strong>Admitted</strong><br>
                        <span style='color:#64748b;font-size:0.85rem;'>{patient['Admitted']}</span>
                    </div>
                    <div class='timeline-item'>
                        <strong>Diagnosis</strong><br>
                        <span style='color:#64748b;font-size:0.85rem;'>{patient['Condition']}</span>
                    </div>
                    <div class='timeline-item'>
                        <strong>Current Status</strong><br>
                        <span style='color:#64748b;font-size:0.85rem;'>{patient['Status']}</span>
                    </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  APPOINTMENTS (NEW)
# ─────────────────────────────────────────────
elif "Appointments" in menu:
    st.markdown("## 📅 Appointment Management")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>Schedule and manage patient appointments</p>", unsafe_allow_html=True)
    st.divider()
   
    tab1, tab2 = st.tabs(["📋 View Appointments", "➕ Schedule New"])
   
    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            date_filter = st.date_input("Filter by Date", value=None)
        with col2:
            doctor_filter = st.selectbox("Filter by Doctor", ["All"] + engine.DOCTORS)
       
        apt_df = st.session_state.appointments.copy()
       
        if date_filter:
            apt_df = apt_df[apt_df["Date"] == date_filter.strftime("%Y-%m-%d")]
        if doctor_filter != "All":
            apt_df = apt_df[apt_df["Doctor"] == doctor_filter]
       
        st.dataframe(
            apt_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.TextColumn("Apt. ID"),
                "Patient": st.column_config.TextColumn("Patient"),
                "Doctor": st.column_config.TextColumn("Doctor"),
                "Date": st.column_config.DateColumn("Date", format="DD MMM YYYY"),
                "Time": st.column_config.TextColumn("Time"),
                "Type": st.column_config.TextColumn("Type"),
                "Status": st.column_config.TextColumn("Status"),
            }
        )
   
    with tab2:
        with st.form("new_appointment"):
            col1, col2 = st.columns(2)
            with col1:
                patients = st.session_state.db[st.session_state.db["Status"] != "Discharged"]["Name"].tolist()
                apt_patient = st.selectbox("Patient *", patients + ["New Patient"])
                apt_doctor = st.selectbox("Doctor *", engine.DOCTORS)
                apt_type = st.selectbox("Appointment Type *",
                                       ["Consultation", "Follow-up", "Lab Review", "Procedure", "Emergency"])
            with col2:
                apt_date = st.date_input("Date *", min_value=datetime.today())
                apt_time = st.selectbox("Time *",
                                       ["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM",
                                        "11:30 AM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
                                        "04:00 PM", "04:30 PM", "05:00 PM"])
                apt_notes = st.text_area("Notes", placeholder="Optional notes...")
           
            if st.form_submit_button("📅 Schedule Appointment", use_container_width=True):
                new_apt_id = engine.add_appointment(
                    apt_patient, apt_doctor, apt_date.strftime("%Y-%m-%d"), apt_time, apt_type
                )
                st.success(f"Appointment {new_apt_id} scheduled successfully!")
                st.rerun()

# ─────────────────────────────────────────────
#  MEDICATIONS (NEW)
# ─────────────────────────────────────────────
elif "Medications" in menu:
    st.markdown("## 💊 Medication Reference")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>Drug information and prescription guidelines</p>", unsafe_allow_html=True)
    st.divider()
   
    # Common medications database
    DRUG_INFO = {
        "Paracetamol": {
            "class": "Analgesic/Antipyretic",
            "dosage": "500-1000mg every 4-6 hours",
            "max_daily": "4000mg",
            "contraindications": ["Severe hepatic impairment", "Hypersensitivity"],
            "side_effects": ["Rare: Hepatotoxicity at high doses", "Allergic reactions"]
        },
        "Metformin": {
            "class": "Biguanide (Antidiabetic)",
            "dosage": "500mg BD, increase gradually to 2000mg/day",
            "max_daily": "2550mg",
            "contraindications": ["Renal impairment (eGFR <30)", "Metabolic acidosis", "Contrast procedures"],
            "side_effects": ["GI upset", "Lactic acidosis (rare)", "B12 deficiency"]
        },
        "Amlodipine": {
            "class": "Calcium Channel Blocker",
            "dosage": "5mg OD, may increase to 10mg",
            "max_daily": "10mg",
            "contraindications": ["Severe aortic stenosis", "Cardiogenic shock"],
            "side_effects": ["Peripheral edema", "Flushing", "Headache"]
        },
        "Aspirin": {
            "class": "NSAID/Antiplatelet",
            "dosage": "75-325mg OD for cardiac protection",
            "max_daily": "4000mg (analgesic)",
            "contraindications": ["Active GI bleeding", "Aspirin-sensitive asthma", "Children <16"],
            "side_effects": ["GI irritation", "Bleeding risk", "Tinnitus"]
        },
        "Omeprazole": {
            "class": "Proton Pump Inhibitor",
            "dosage": "20-40mg OD",
            "max_daily": "40mg",
            "contraindications": ["Hypersensitivity to PPIs"],
            "side_effects": ["Headache", "GI disturbances", "Long-term: B12/Mg deficiency"]
        },
    }
   
    tab1, tab2 = st.tabs(["🔍 Drug Lookup", "📋 Condition-Based"])
   
    with tab1:
        drug_search = st.selectbox("Select Medication", list(DRUG_INFO.keys()))
       
        if drug_search:
            drug = DRUG_INFO[drug_search]
            st.markdown(f"""
                <div class='glass-card'>
                    <h3 style='color:#00e5ff;margin-top:0;'>{drug_search}</h3>
                    <p style='color:#64748b;'>{drug['class']}</p>
                </div>
            """, unsafe_allow_html=True)
           
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Dosage**")
                st.info(drug['dosage'])
                st.markdown("**Maximum Daily Dose**")
                st.info(drug['max_daily'])
           
            with col2:
                st.markdown("**Contraindications**")
                for c in drug['contraindications']:
                    st.markdown(f"• ⚠️ {c}")
               
                st.markdown("**Side Effects**")
                for s in drug['side_effects']:
                    st.markdown(f"• {s}")
   
    with tab2:
        condition = st.selectbox("Select Condition", list(engine.MEDICATIONS.keys()))
       
        if condition:
            st.markdown(f"### Recommended medications for {condition}")
            meds = engine.MEDICATIONS[condition]
            for i, med in enumerate(meds, 1):
                st.markdown(f"**{i}.** {med}")

# ─────────────────────────────────────────────
#  VITALS MONITOR (NEW)
# ─────────────────────────────────────────────
elif "Vitals" in menu:
    st.markdown("## 📈 Vitals Monitoring")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>Track and record patient vital signs</p>", unsafe_allow_html=True)
    st.divider()
   
    df = st.session_state.db[st.session_state.db["Status"] != "Discharged"]
    patient_options = [f"{row['ID']} - {row['Name']}" for _, row in df.iterrows()]
   
    selected = st.selectbox("Select Patient", patient_options)
   
    if selected:
        patient_id = selected.split(" - ")[0]
       
        tab1, tab2 = st.tabs(["📊 Vitals History", "➕ Record New Vitals"])
       
        with tab1:
            if patient_id in st.session_state.vitals_history:
                vitals_data = st.session_state.vitals_history[patient_id]
                vitals_df = pd.DataFrame(vitals_data)
               
                # Current vitals display
                latest = vitals_data[-1]
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Heart Rate", f"{latest['heart_rate']} bpm",
                             f"{latest['heart_rate'] - vitals_data[-2]['heart_rate'] if len(vitals_data) > 1 else 0}")
                with col2:
                    st.metric("Blood Pressure", f"{latest['bp_systolic']}/{latest['bp_diastolic']}")
                with col3:
                    st.metric("Temperature", f"{latest['temperature']}°F")
                with col4:
                    st.metric("Oxygen Sat.", f"{latest['oxygen']}%")
                with col5:
                    st.metric("Resp. Rate", f"{latest['respiratory_rate']}/min")
               
                st.markdown("---")
               
                # Charts
                st.markdown("### 📈 Trends (Last 7 Days)")
               
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.markdown("**Heart Rate**")
                    hr_df = vitals_df[["date", "heart_rate"]].set_index("date")
                    st.line_chart(hr_df, color="#ef4444", height=200)
               
                with chart_col2:
                    st.markdown("**Blood Pressure**")
                    bp_df = vitals_df[["date", "bp_systolic", "bp_diastolic"]].set_index("date")
                    st.line_chart(bp_df, height=200)
               
                chart_col3, chart_col4 = st.columns(2)
                with chart_col3:
                    st.markdown("**Temperature**")
                    temp_df = vitals_df[["date", "temperature"]].set_index("date")
                    st.line_chart(temp_df, color="#f97316", height=200)
               
                with chart_col4:
                    st.markdown("**Oxygen Saturation**")
                    o2_df = vitals_df[["date", "oxygen"]].set_index("date")
                    st.line_chart(o2_df, color="#00e5ff", height=200)
       
        with tab2:
            with st.form("record_vitals"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
                    bp_systolic = st.number_input("BP Systolic", min_value=70, max_value=200, value=120)
                with col2:
                    bp_diastolic = st.number_input("BP Diastolic", min_value=40, max_value=130, value=80)
                    temperature = st.number_input("Temperature (°F)", min_value=95.0, max_value=108.0, value=98.6, step=0.1)
                with col3:
                    oxygen = st.number_input("Oxygen Saturation (%)", min_value=70, max_value=100, value=98)
                    respiratory_rate = st.number_input("Respiratory Rate (/min)", min_value=8, max_value=40, value=16)
               
                notes = st.text_area("Clinical Notes", placeholder="Any observations...")
               
                if st.form_submit_button("💾 Record Vitals", use_container_width=True):
                    vitals = {
                        "heart_rate": heart_rate,
                        "bp_systolic": bp_systolic,
                        "bp_diastolic": bp_diastolic,
                        "temperature": temperature,
                        "oxygen": oxygen,
                        "respiratory_rate": respiratory_rate
                    }
                    if engine.record_vitals(patient_id, vitals):
                        st.success("Vitals recorded successfully!")
                       
                        # Check for abnormal vitals
                        warnings = []
                        if heart_rate > 100 or heart_rate < 60:
                            warnings.append(f"Heart rate abnormal: {heart_rate} bpm")
                        if bp_systolic > 140 or bp_diastolic > 90:
                            warnings.append(f"Blood pressure elevated: {bp_systolic}/{bp_diastolic}")
                        if temperature > 100.4:
                            warnings.append(f"Fever detected: {temperature}°F")
                        if oxygen < 95:
                            warnings.append(f"Low oxygen saturation: {oxygen}%")
                       
                        if warnings:
                            st.warning("⚠️ Abnormal values detected:\n" + "\n".join(f"• {w}" for w in warnings))
                       
                        st.rerun()

# ─────────────────────────────────────────────
#  NOTIFICATIONS (NEW)
# ─────────────────────────────────────────────
elif "Notifications" in menu:
    st.markdown("## 🔔 Notifications Center")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>System alerts and updates</p>", unsafe_allow_html=True)
    st.divider()
   
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark All Read", use_container_width=True):
            for n in st.session_state.notifications:
                n["read"] = True
            st.rerun()
   
    notification_icons = {
        "critical": "🚨",
        "warning": "⚠️",
        "info": "ℹ️",
        "success": "✅"
    }
   
    notification_colors = {
        "critical": "#ef4444",
        "warning": "#f97316",
        "info": "#00e5ff",
        "success": "#22c55e"
    }
   
    for notification in st.session_state.notifications:
        icon = notification_icons.get(notification["type"], "📌")
        color = notification_colors.get(notification["type"], "#64748b")
        read_style = "opacity: 0.6;" if notification["read"] else ""
       
        st.markdown(f"""
            <div class='glass-card' style='padding:16px;margin-bottom:12px;border-left:3px solid {color};{read_style}'>
                <div style='display:flex;justify-content:space-between;align-items:start;'>
                    <div>
                        <span style='font-size:1.2rem;'>{icon}</span>
                        <span style='color:#e2e8f0;margin-left:8px;'>{notification['message']}</span>
                    </div>
                    <span style='color:#64748b;font-size:0.8rem;'>{notification['time']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ADD PATIENT
# ─────────────────────────────────────────────
elif "Add Patient" in menu:
    st.markdown("## ➕ Register New Patient")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>Manually enter patient admission details</p>", unsafe_allow_html=True)
    st.divider()

    with st.form("add_patient_form", clear_on_submit=True):
        st.markdown("### Personal Information")
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Full Name *", placeholder="e.g. Neha Gupta")
            age = st.number_input("Age *", min_value=1, max_value=120, value=25)
        with c2:
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
        with c3:
            phone = st.text_input("Phone Number", placeholder="+91-XXXXXXXXXX")
            emergency_contact = st.text_input("Emergency Contact", placeholder="Name (Phone)")
       
        st.markdown("### Medical Information")
        c4, c5, c6 = st.columns(3)
        with c4:
            diagnosis = st.text_input("Diagnosis *", placeholder="e.g. Dengue Fever")
            priority = st.selectbox("Priority Level *", ["Low", "Stable", "High", "Critical"])
        with c5:
            doctor = st.selectbox("Attending Doctor *", engine.DOCTORS)
            department = st.selectbox("Department *", engine.DEPARTMENTS)
        with c6:
            room = st.text_input("Room/Bed Assignment", placeholder="e.g., 101-A or ICU-01")
            notes = st.text_area("Clinical Notes", placeholder="Optional notes…", height=80)

        submitted = st.form_submit_button("✅ Register Patient", use_container_width=True)

        if submitted:
            if not name or not diagnosis:
                st.error("Name and Diagnosis are required fields.")
            else:
                new_id = engine.add_patient(
                    name, age, gender, diagnosis, priority, doctor, department,
                    room if room else "TBA", phone if phone else "Not provided",
                    emergency_contact if emergency_contact else "Not provided",
                    blood_group
                )
                st.success(f"Patient **{name}** successfully registered as **{new_id}**.")
                st.balloons()
               
                # Add notification for critical patients
                if priority in ["Critical", "High"]:
                    st.session_state.notifications.insert(0, {
                        "id": len(st.session_state.notifications) + 1,
                        "type": "critical" if priority == "Critical" else "warning",
                        "message": f"New {priority.lower()} patient admitted: {name}",
                        "time": "Just now",
                        "read": False
                    })

# ─────────────────────────────────────────────
#  AUDIT LOG (NEW)
# ─────────────────────────────────────────────
elif "Audit Log" in menu:
    st.markdown("## 📜 Audit Log")
    st.markdown("<p style='color:#64748b;margin-top:-8px;'>System activity and change history</p>", unsafe_allow_html=True)
    st.divider()
   
    if st.session_state.audit_log:
        audit_df = pd.DataFrame(st.session_state.audit_log)
        audit_df = audit_df.sort_values("timestamp", ascending=False)
       
        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "timestamp": st.column_config.TextColumn("Timestamp"),
                "action": st.column_config.TextColumn("Action"),
                "details": st.column_config.TextColumn("Details"),
                "user": st.column_config.TextColumn("User"),
            }
        )
       
        st.download_button(
            "⬇️ Export Audit Log",
            data=audit_df.to_csv(index=False).encode("utf-8"),
            file_name=f"medicore_audit_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No audit log entries yet.")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
    <div style='text-align:center;color:#64748b;font-size:0.8rem;padding:20px 0;'>
        <strong>MediCore.AI</strong> v2.0 · Clinical Intelligence Platform<br>
        🔐 HIPAA Compliant · AES-256 Encrypted · Built for Healthcare Professionals
    </div>
""", unsafe_allow_html=True)
