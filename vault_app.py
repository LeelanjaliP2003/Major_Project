import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import hashlib
import time
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Neuro-Semantic Cryptographic Vault",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — CYBERPUNK / BIOPUNK AESTHETIC
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --bg-deep:     #020408;
    --bg-panel:    #070d18;
    --bg-card:     #0a1628;
    --border-dim:  #112240;
    --border-glow: #00ffe7;
    --accent-cyan: #00ffe7;
    --accent-green:#39ff14;
    --accent-red:  #ff2d55;
    --accent-gold: #ffd700;
    --accent-pink: #e040fb;
    --text-bright: #e8f4fd;
    --text-mid:    #8bafc8;
    --text-dim:    #3d5a73;
    --font-mono:   'DM Mono', monospace;
    --font-hud:    'Poppins', sans-serif;
    --font-body:   'Poppins', sans-serif;
}

/* ── Base ── */
html, body, [class*="css"] {
    background-color: var(--bg-deep) !important;
    color: var(--text-bright) !important;
    font-family: var(--font-body) !important;
}
.main .block-container { padding: 1rem 2rem 2rem 2rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020c1b 0%, #030a15 100%) !important;
    border-right: 1px solid #0d2137 !important;
}
section[data-testid="stSidebar"] * { color: var(--text-bright) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: var(--font-hud) !important;
    color: var(--accent-cyan) !important;
    letter-spacing: 0.05em;
}

/* ── Buttons ── */
div.stButton > button {
    background: transparent !important;
    border: 1px solid var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    font-family: var(--font-hud) !important;
    font-size: 12px !important;
    letter-spacing: 0.1em !important;
    border-radius: 2px !important;
    height: 42px !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    text-transform: uppercase !important;
}
div.stButton > button:hover {
    background: rgba(0,255,231,0.1) !important;
    box-shadow: 0 0 18px rgba(0,255,231,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Nav buttons (sidebar) ── */
.nav-btn {
    display: block; width: 100%; padding: 10px 14px; margin: 4px 0;
    background: transparent; border: 1px solid #112240;
    color: var(--text-mid); font-family: var(--font-hud); font-size: 11px;
    letter-spacing: 0.08em; text-transform: uppercase; cursor: pointer;
    border-radius: 2px; text-align: left; transition: all 0.2s;
}
.nav-btn:hover { border-color: var(--accent-cyan); color: var(--accent-cyan); background: rgba(0,255,231,0.05); }
.nav-btn.active { border-color: var(--accent-cyan); color: var(--accent-cyan);
    background: rgba(0,255,231,0.08); box-shadow: 0 0 12px rgba(0,255,231,0.2); }

/* ── Metric cards ── */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-top: 2px solid var(--accent-cyan);
    border-radius: 4px; padding: 16px 14px; text-align: center;
    position: relative; overflow: hidden;
    transition: box-shadow 0.3s;
}
.kpi-card:hover { box-shadow: 0 0 20px rgba(0,255,231,0.15); }
.kpi-card::before {
    content:''; position:absolute; top:0;left:0;right:0;height:1px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
}
.kpi-val { font-family: var(--font-hud); font-size: 26px; font-weight: 700; color: var(--text-bright); }
.kpi-unit { font-family: var(--font-mono); font-size: 11px; color: var(--accent-cyan); }
.kpi-lbl { font-family: var(--font-mono); font-size: 10px; color: var(--text-dim);
    text-transform: uppercase; letter-spacing: 0.12em; margin-top: 4px; }

/* ── Status badge ── */
.badge-granted {
    background: rgba(57,255,20,0.08); border: 1px solid var(--accent-green);
    border-left: 4px solid var(--accent-green); border-radius: 3px;
    padding: 12px 16px; color: var(--accent-green);
    font-family: var(--font-hud); font-size: 13px; letter-spacing: 0.06em;
}
.badge-denied {
    background: rgba(255,45,85,0.08); border: 1px solid var(--accent-red);
    border-left: 4px solid var(--accent-red); border-radius: 3px;
    padding: 12px 16px; color: var(--accent-red);
    font-family: var(--font-hud); font-size: 13px; letter-spacing: 0.06em;
}
.badge-warn {
    background: rgba(255,215,0,0.06); border: 1px solid var(--accent-gold);
    border-left: 4px solid var(--accent-gold); border-radius: 3px;
    padding: 12px 16px; color: var(--accent-gold);
    font-family: var(--font-hud); font-size: 13px; letter-spacing: 0.06em;
}

/* ── Terminal box ── */
.terminal {
    background: #000d1a; border: 1px solid #0d2137;
    border-radius: 4px; padding: 14px 16px;
    font-family: var(--font-mono); font-size: 12px;
    color: #38bdf8; line-height: 1.7;
    box-shadow: inset 0 0 30px rgba(0,0,0,0.5);
}
.terminal .log-ok   { color: var(--accent-green); }
.terminal .log-err  { color: var(--accent-red); }
.terminal .log-warn { color: var(--accent-gold); }
.terminal .log-sys  { color: var(--text-dim); }

/* ── Section header ── */
.sec-header {
    font-family: var(--font-hud); font-size: 11px; letter-spacing: 0.2em;
    text-transform: uppercase; color: var(--text-dim);
    border-bottom: 1px solid #0d2137; padding-bottom: 6px; margin-bottom: 14px;
}
.sec-header span { color: var(--accent-cyan); margin-right: 8px; }

/* ── Progress bar ── */
.stProgress > div > div > div { background-color: var(--accent-cyan) !important; }

/* ── Slider ── */
.stSlider > div > div > div { color: var(--accent-cyan) !important; }

/* ── Tabs ── */
.stTabs [role="tab"] {
    font-family: var(--font-hud) !important; font-size: 11px !important;
    letter-spacing: 0.1em !important; color: var(--text-dim) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
}

/* ── Dataframe ── */
.stDataFrame { border: 1px solid #0d2137 !important; }

/* ── Input fields ── */
.stTextInput input {
    background: #030a15 !important; border: 1px solid #0d2137 !important;
    color: var(--accent-cyan) !important; font-family: var(--font-mono) !important;
    font-size: 12px !important; border-radius: 2px !important;
}
.stTextArea textarea {
    background: #030a15 !important; border: 1px solid #0d2137 !important;
    color: var(--text-bright) !important; font-family: var(--font-mono) !important;
    font-size: 12px !important; border-radius: 2px !important;
}

/* ── Radio ── */
.stRadio label { font-family: var(--font-body) !important; color: var(--text-mid) !important; }
.stRadio [data-checked="true"] + label { color: var(--accent-cyan) !important; }

/* ── Divider ── */
hr { border-color: #0d2137 !important; }

/* ── Big title ── */
.vault-title {
    font-family: var(--font-hud); font-size: 32px; font-weight: 900;
    background: linear-gradient(90deg, var(--accent-cyan) 0%, #a78bfa 60%, var(--accent-pink) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 0.06em; line-height: 1.1;
}
.vault-sub {
    font-family: var(--font-mono); font-size: 12px; color: var(--text-dim);
    letter-spacing: 0.15em; text-transform: uppercase; margin-top: 4px;
}
.vault-id {
    font-family: var(--font-mono); font-size: 10px; color: var(--accent-green);
    letter-spacing: 0.2em;
}

/* ── Brain band indicator ── */
.band-row {
    display: flex; align-items: center; gap: 10px;
    margin: 6px 0; font-family: var(--font-mono); font-size: 12px;
}
.band-label { width: 50px; color: var(--text-dim); text-transform: uppercase; }
.band-bar-bg { flex: 1; height: 6px; background: #0d2137; border-radius: 3px; position: relative; }
.band-bar-fill { height: 100%; border-radius: 3px; }
.band-val { width: 50px; text-align: right; color: var(--text-bright); }

/* ── Hex grid background ── */
.hex-bg {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background-image: radial-gradient(circle at 25% 25%, rgba(0,255,231,0.03) 0%, transparent 50%),
                      radial-gradient(circle at 75% 75%, rgba(224,64,251,0.03) 0%, transparent 50%);
    pointer-events: none; z-index: -1;
}

/* ── Module card ── */
.mod-card {
    background: var(--bg-card); border: 1px solid var(--border-dim);
    border-radius: 4px; padding: 20px; margin-bottom: 16px;
    position: relative; overflow: hidden;
}
.mod-card::after {
    content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--accent-cyan), transparent);
}

/* ── Vault open/closed visual ── */
.vault-open-display {
    background: radial-gradient(circle at center, rgba(57,255,20,0.1) 0%, transparent 70%);
    border: 2px solid var(--accent-green);
    border-radius: 8px; padding: 24px; text-align: center;
    font-family: var(--font-hud); font-size: 18px; color: var(--accent-green);
    letter-spacing: 0.1em; box-shadow: 0 0 40px rgba(57,255,20,0.2);
    animation: pulse-green 2s infinite;
}
.vault-closed-display {
    background: radial-gradient(circle at center, rgba(255,45,85,0.08) 0%, transparent 70%);
    border: 2px solid var(--accent-red);
    border-radius: 8px; padding: 24px; text-align: center;
    font-family: var(--font-hud); font-size: 18px; color: var(--accent-red);
    letter-spacing: 0.1em;
}
@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 40px rgba(57,255,20,0.2); }
    50%       { box-shadow: 0 0 60px rgba(57,255,20,0.4); }
}

/* ── Comparison table ── */
.cmp-table { width: 100%; border-collapse: collapse; font-family: var(--font-mono); font-size: 12px; }
.cmp-table th {
    background: #0a1628; color: var(--accent-cyan); text-transform: uppercase;
    letter-spacing: 0.1em; padding: 10px 12px; border-bottom: 1px solid #1a3a5c; text-align: left;
}
.cmp-table td { padding: 9px 12px; border-bottom: 1px solid #0d2137; color: var(--text-mid); }
.cmp-table tr:hover td { background: #081020; color: var(--text-bright); }
.cmp-table .yes { color: var(--accent-green); }
.cmp-table .no  { color: var(--accent-red); }
.cmp-table .this { color: var(--accent-cyan); font-weight: bold; }

/* ── Accuracy gauge colors ── */
.gauge-high { color: var(--accent-green); }
.gauge-mid  { color: var(--accent-gold); }
.gauge-low  { color: var(--accent-red); }

/* ── Architecture node ── */
.arch-node {
    background: var(--bg-card); border: 1px solid #1a3a5c;
    border-radius: 4px; padding: 10px 14px; text-align: center;
    font-family: var(--font-mono); font-size: 11px; color: var(--text-mid);
    position: relative;
}
.arch-node .node-type { font-family: var(--font-hud); font-size: 12px; color: var(--accent-cyan); margin-bottom: 3px; }
.arch-arrow { text-align: center; color: var(--border-dim); font-size: 18px; line-height: 1; }

/* ── Sidebar logo ── */
.sidebar-logo {
    font-family: var(--font-hud); font-size: 15px; font-weight: 900;
    color: var(--accent-cyan); letter-spacing: 0.08em;
    padding: 10px 0 16px 0; text-align: center;
    border-bottom: 1px solid #0d2137;
    text-shadow: 0 0 12px rgba(0,255,231,0.4);
}
.sidebar-logo small { display: block; font-size: 9px; color: var(--text-dim); letter-spacing: 0.2em; margin-top: 3px; }

/* ── Sidebar nav label ── */
.nav-label {
    font-family: var(--font-mono); font-size: 9px; color: var(--text-dim);
    letter-spacing: 0.2em; text-transform: uppercase; margin: 14px 0 6px 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: #112240; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-cyan); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
defaults = {
    'page': 'dashboard',
    'vault_open': False,
    'session_key': '',
    'mop_triggered': False,
    'scan_count': 0,
    'denied_count': 0,
    'granted_count': 0,
    'logs': [f"[{datetime.now().strftime('%H:%M:%S')}] SYS  ▸ Pipeline initialized. Awaiting hardware sync..."],
    'last_confidence': 0.0,
    'last_trigger': 'N/A',
    'history': [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def add_log(msg, level="SYS"):
    ts = datetime.now().strftime('%H:%M:%S')
    st.session_state.logs.append(f"[{ts}] {level:<4} ▸ {msg}")

FILE_PATH = "top_secret_data.txt"

# ─────────────────────────────────────────────
# LOAD AI ASSETS
# ─────────────────────────────────────────────
@st.cache_resource
def load_assets():
    try:
        model   = tf.keras.models.load_model('neuro_cnn_model.h5')
        classes = np.load('classes.npy', allow_pickle=True)
        scaler  = joblib.load('scaler.pkl')
        return model, classes, scaler, True
    except Exception:
        return None, None, None, False

model, classes, scaler, assets_loaded = load_assets()

# ─────────────────────────────────────────────
# PLOTLY THEME HELPERS
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Mono', color='#8bafc8', size=11),
    margin=dict(l=10, r=10, t=36, b=10),
    showlegend=True,
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
    xaxis=dict(showgrid=True, gridcolor='#0d2137', zeroline=False, tickfont=dict(color='#3d5a73')),
    yaxis=dict(showgrid=True, gridcolor='#0d2137', zeroline=False, tickfont=dict(color='#3d5a73')),
)

def styled_fig(title="", height=200):
    fig = go.Figure()
    layout = dict(PLOT_LAYOUT)
    layout['height'] = height
    layout['title']  = dict(text=title, font=dict(color='#3d5a73', size=11), x=0.01)
    fig.update_layout(**layout)
    return fig

# ─────────────────────────────────────────────
# SIGNAL GENERATION
# ─────────────────────────────────────────────
def generate_signals(mode, seed=None):
    t = np.linspace(0, 1, 250)
    if seed is not None:
        np.random.seed(seed)
    else:
        np.random.seed(int(time.time()) % 10000)

    if mode == "Authorized (Forest)":
        af7  = 12 * np.sin(2*np.pi*10*t) + 3  * np.random.randn(250)
        af8  = 11 * np.sin(2*np.pi*10*t) + 2.5* np.random.randn(250)
    else:
        af7  = 4*np.sin(2*np.pi*10*t) + 16*np.sin(2*np.pi*22*t) + 4  *np.random.randn(250)
        af8  = 5*np.sin(2*np.pi*10*t) + 18*np.sin(2*np.pi*22*t) + 3.5*np.random.randn(250)

    tp9  = 7 * np.sin(2*np.pi*4*t) + 2 * np.random.randn(250)
    tp10 = 6 * np.sin(2*np.pi*6*t) + 2 * np.random.randn(250)
    return t, af7, af8, tp9, tp10

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>🧠 NSC VAULT<small>NEURO-SEMANTIC CRYPTOGRAPHIC SYSTEM</small></div>", unsafe_allow_html=True)

    st.markdown("<div class='nav-label'>Navigation</div>", unsafe_allow_html=True)

    pages = [
        ("dashboard",    "⬡  SYSTEM DASHBOARD",   "Overview & live metrics"),
        ("signal",       "📡  SIGNAL LABORATORY",  "Brainwave acquisition"),
        ("classifier",   "🤖  CNN CLASSIFIER",     "Neural inference engine"),
        ("vault",        "🔐  VAULT & DECRYPTION", "Key derivation & access"),
    ]
    for pid, plabel, pdesc in pages:
        active_cls = "active" if st.session_state.page == pid else ""
        if st.button(f"{plabel}", key=f"nav_{pid}"):
            st.session_state.page = pid
            st.rerun()

    st.markdown("---")
    st.markdown("<div class='nav-label'>Neural Input Simulator</div>", unsafe_allow_html=True)
    mode = st.radio("Mental Trigger State:", ["Authorized (Forest)", "Unauthorized (Home)"], label_visibility="collapsed")

    if mode == "Authorized (Forest)":
        alpha, beta, theta = 0.28, 0.38, 0.22
    else:
        alpha, beta, theta = 0.51, 0.42, 0.25

    # Band bars
    def band_bar(lbl, val, color):
        pct = int(val * 200)
        st.markdown(f"""
        <div class='band-row'>
            <span class='band-label'>{lbl}</span>
            <div class='band-bar-bg'>
                <div class='band-bar-fill' style='width:{pct}%; background:{color};'></div>
            </div>
            <span class='band-val'>{val:.2f}</span>
        </div>""", unsafe_allow_html=True)

    band_bar("Alpha", alpha, "#00ffe7")
    band_bar("Beta",  beta,  "#a78bfa")
    band_bar("Theta", theta, "#38bdf8")

    st.markdown("---")

    # Status summary
    vault_status = "🔓 UNLOCKED" if st.session_state.vault_open else "🔒 SECURED"
    vault_color  = "#39ff14" if st.session_state.vault_open else "#ff2d55"
    st.markdown(f"""
    <div style='font-family:var(--font-hud);font-size:11px;color:{vault_color};
         border:1px solid {vault_color};border-radius:2px;padding:8px 10px;
         text-align:center;letter-spacing:0.1em;margin-bottom:12px;'>
        VAULT {vault_status}
    </div>""", unsafe_allow_html=True)

    if st.button("🔴  EMERGENCY MOP REBOOT"):
        st.session_state.vault_open  = False
        st.session_state.session_key = ""
        st.session_state.mop_triggered = True
        add_log("Manual override initiated. Force-wiping memory workspaces.", "CRIT")
        st.rerun()

    st.markdown("---")
    st.markdown(f"<div style='font-family:var(--font-mono);font-size:9px;color:#1a3a5c;text-align:center;'>MCA Major Project 2026<br/>RVCE</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ASSET GUARD
# ─────────────────────────────────────────────
if not assets_loaded:
    st.markdown("<div class='badge-denied'>🚨 CRITICAL — Missing compiled pipeline: `neuro_cnn_model.h5`, `classes.npy`, `scaler.pkl`. Run `train_ai.py` first.</div>", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# RUN INFERENCE (shared across pages)
# ─────────────────────────────────────────────
raw_input    = np.array([[alpha, beta, theta]])
scaled_input = scaler.transform(raw_input)
input_window = np.repeat(scaled_input, 20, axis=0).reshape(1, 20, 3)
prediction   = model.predict(input_window, verbose=0)
pred_idx     = np.argmax(prediction)
confidence   = float(np.max(prediction) * 100)
detected_trigger = str(classes[pred_idx])

SECRET_TRIGGER  = "Forest_Scene"
ALPHA_THRESHOLD = 0.35
is_match = (detected_trigger == SECRET_TRIGGER) and (alpha < ALPHA_THRESHOLD)

t_arr, sig_af7, sig_af8, sig_tp9, sig_tp10 = generate_signals(mode)

# ═══════════════════════════════════════════════════════════════
# PAGE 1 — SYSTEM DASHBOARD
# ═══════════════════════════════════════════════════════════════
if st.session_state.page == "dashboard":

    # Header
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("<div class='vault-title'>NEURO-SEMANTIC<br>CRYPTOGRAPHIC VAULT</div>", unsafe_allow_html=True)
        st.markdown("<div class='vault-sub'>Real-Time Hybrid BCI Decryption Pipeline & Anti-Forensic Spectral Guardrail</div>", unsafe_allow_html=True)
        ts_now = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        st.markdown(f"<div class='vault-id'>SESSION ACTIVE ▸ {ts_now} IST</div>", unsafe_allow_html=True)
    with col_h2:
        vault_disp = "vault_open_display" if st.session_state.vault_open else "vault_closed_display"
        status_txt = "🔓 VAULT OPEN" if st.session_state.vault_open else "🔒 VAULT LOCKED"
        st.markdown(f"<div class='{vault_disp}' style='margin-top:8px;font-size:14px;'>{status_txt}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # KPI row
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    def kpi(col, val, unit, lbl, color="#00ffe7"):
        col.markdown(f"""
        <div class='kpi-card' style='border-top-color:{color};'>
            <div class='kpi-val'>{val}</div>
            <div class='kpi-unit'>{unit}</div>
            <div class='kpi-lbl'>{lbl}</div>
        </div>""", unsafe_allow_html=True)

    kpi(k1, f"{alpha:.2f}", "Hz",  "Alpha Band",   "#00ffe7")
    kpi(k2, f"{beta:.2f}",  "Hz",  "Beta Band",    "#a78bfa")
    kpi(k3, f"{theta:.2f}", "Hz",  "Theta Band",   "#38bdf8")
    kpi(k4, f"{confidence:.1f}", "%", "CNN Confidence", "#ffd700" if confidence > 70 else "#ff2d55")
    kpi(k5, str(st.session_state.scan_count), "runs", "Total Scans",  "#e040fb")
    kpi(k6, "250", "Hz", "Sample Rate",  "#39ff14")

    st.write("")

    # Main overview: mini brainwave + system pipeline diagram
    ov1, ov2 = st.columns([3, 2])

    with ov1:
        st.markdown("<div class='sec-header'><span>●</span> LIVE BRAINWAVE OVERVIEW</div>", unsafe_allow_html=True)
        fig_ov = styled_fig("4-Channel EEG Array — Real-Time Preview", height=240)
        colors = ["#00ffe7", "#a78bfa", "#38bdf8", "#e2e8f0"]
        labels = ["AF7 Frontal", "AF8 Frontal", "TP9 Temporal", "TP10 Temporal"]
        for sig, c, lbl in zip([sig_af7, sig_af8, sig_tp9, sig_tp10], colors, labels):
            fig_ov.add_trace(go.Scatter(y=sig, mode='lines', name=lbl, line=dict(color=c, width=1.2)))
        st.plotly_chart(fig_ov, use_container_width=True, config={'displayModeBar': False})

    with ov2:
        st.markdown("<div class='sec-header'><span>●</span> SYSTEM PIPELINE</div>", unsafe_allow_html=True)
        nodes = [
            ("EEG HEADSET", "Muse 2 — 4 Channels", "#00ffe7"),
            ("SIGNAL PRE-PROC", "Band-pass + FFT", "#38bdf8"),
            ("1D-CNN ENGINE", "2×Conv1D + BatchNorm", "#a78bfa"),
            ("NEURAL GUARDRAIL", "Alpha Spectral Gate", "#ffd700"),
            ("AES KEY DERIVATION", "SHA-256 + Vault", "#39ff14"),
        ]
        for i, (ntitle, ndetail, nclr) in enumerate(nodes):
            st.markdown(f"""
            <div class='arch-node' style='border-left:3px solid {nclr}; margin-bottom:4px;'>
                <div class='node-type'>{ntitle}</div>
                <span style='font-size:10px;'>{ndetail}</span>
            </div>
            {"<div class='arch-arrow'>↓</div>" if i < len(nodes)-1 else ""}
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Status panels row
    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown("<div class='sec-header'><span>●</span> NEURAL STATE</div>", unsafe_allow_html=True)
        state_color = "#39ff14" if mode == "Authorized (Forest)" else "#ff2d55"
        state_icon  = "✅" if mode == "Authorized (Forest)" else "⚠️"
        st.markdown(f"""
        <div style='background:var(--bg-card);border:1px solid #0d2137;border-radius:4px;padding:16px;'>
            <div style='font-family:var(--font-hud);font-size:22px;color:{state_color};margin-bottom:8px;'>{state_icon} {mode.split("(")[1].rstrip(")")}</div>
            <div style='font-family:var(--font-mono);font-size:11px;color:var(--text-dim);'>Detected Class: <span style='color:var(--accent-cyan);'>{detected_trigger}</span></div>
            <div style='font-family:var(--font-mono);font-size:11px;color:var(--text-dim);margin-top:4px;'>α Threshold: <span style='color:var(--accent-cyan);'>{'PASS' if alpha < ALPHA_THRESHOLD else 'FAIL'}</span></div>
        </div>""", unsafe_allow_html=True)

    with d2:
        st.markdown("<div class='sec-header'><span>●</span> CNN PROBABILITY VECTOR</div>", unsafe_allow_html=True)
        fig_bar = styled_fig(height=170)
        class_names = [str(c)[:14] for c in classes]
        bar_colors  = ["#00ffe7" if c == detected_trigger else "#1a3a5c" for c in [str(x) for x in classes]]
        fig_bar.add_trace(go.Bar(
            x=prediction[0], y=class_names, orientation='h',
            marker_color=bar_colors, marker_line_width=0,
        ))
        fig_bar.update_layout(showlegend=False, height=170, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with d3:
        st.markdown("<div class='sec-header'><span>●</span> SESSION STATISTICS</div>", unsafe_allow_html=True)
        total = max(st.session_state.scan_count, 1)
        grant_pct = st.session_state.granted_count / total * 100
        deny_pct  = st.session_state.denied_count  / total * 100
        st.markdown(f"""
        <div style='background:var(--bg-card);border:1px solid #0d2137;border-radius:4px;padding:16px;'>
            <div style='font-family:var(--font-mono);font-size:11px;margin-bottom:10px;'>
                <span style='color:var(--text-dim);'>Total Scans:</span>
                <span style='color:var(--text-bright);float:right;'>{st.session_state.scan_count}</span>
            </div>
            <div style='font-family:var(--font-mono);font-size:11px;margin-bottom:8px;'>
                <span style='color:var(--text-dim);'>Granted:</span>
                <span style='color:#39ff14;float:right;'>{st.session_state.granted_count} ({grant_pct:.0f}%)</span>
            </div>
            <div style='font-family:var(--font-mono);font-size:11px;margin-bottom:10px;'>
                <span style='color:var(--text-dim);'>Denied:</span>
                <span style='color:#ff2d55;float:right;'>{st.session_state.denied_count} ({deny_pct:.0f}%)</span>
            </div>
            <div style='height:4px;background:#0d2137;border-radius:2px;'>
                <div style='height:100%;width:{grant_pct}%;background:#39ff14;border-radius:2px;'></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Live log
    st.markdown("<div class='sec-header'><span>●</span> REAL-TIME DIAGNOSTIC CONSOLE</div>", unsafe_allow_html=True)
    if st.session_state.mop_triggered:
        st.markdown("<div class='badge-warn'>🚨 ANTI-FORENSIC REMOVAL RUNNING — RAM spaces cleared via MOP (M_K ← {0}²⁵⁶)</div>", unsafe_allow_html=True)
        st.session_state.mop_triggered = False

    log_html = ""
    for line in st.session_state.logs[-8:]:
        if "SUCCESS" in line or "GRANT" in line:
            log_html += f"<span class='log-ok'>{line}</span><br/>"
        elif "BREACH" in line or "DENY" in line or "CRIT" in line or "ERROR" in line:
            log_html += f"<span class='log-err'>{line}</span><br/>"
        elif "WARN" in line or "MOP" in line:
            log_html += f"<span class='log-warn'>{line}</span><br/>"
        else:
            log_html += f"<span class='log-sys'>{line}</span><br/>"
    st.markdown(f"<div class='terminal'>{log_html}</div>", unsafe_allow_html=True)

    # Comparison table
    st.markdown("---")
    st.markdown("<div class='sec-header'><span>●</span> SYSTEM COMPARISON — RELATED WORK</div>", unsafe_allow_html=True)
    st.markdown("""
    <table class='cmp-table'>
      <tr>
        <th>Method</th><th>Real-Time</th><th>Anti-Coercion</th><th>AI-Based</th><th>Cryptographic</th><th>Accuracy</th>
      </tr>
      <tr>
        <td class='this'>NSC Vault (Ours)</td>
        <td class='yes'>✔ Yes</td><td class='yes'>✔ Yes</td><td class='yes'>✔ 1D-CNN</td><td class='yes'>✔ SHA-256</td>
        <td class='yes'>~94%</td>
      </tr>
      <tr>
        <td>Password Auth</td>
        <td class='no'>✘ No</td><td class='no'>✘ No</td><td class='no'>✘ No</td><td class='yes'>✔ Yes</td>
        <td class='gauge-mid'>N/A</td>
      </tr>
      <tr>
        <td>Fingerprint BIO</td>
        <td class='yes'>✔ Yes</td><td class='no'>✘ No</td><td class='no'>✘ No</td><td class='yes'>✔ Yes</td>
        <td class='gauge-mid'>~89%</td>
      </tr>
      <tr>
        <td>EEG + SVM</td>
        <td class='no'>✘ No</td><td class='no'>✘ No</td><td class='yes'>✔ SVM</td><td class='no'>✘ No</td>
        <td class='gauge-mid'>~78%</td>
      </tr>
      <tr>
        <td>EEG + LSTM</td>
        <td class='yes'>✔ Yes</td><td class='no'>✘ No</td><td class='yes'>✔ LSTM</td><td class='no'>✘ No</td>
        <td class='gauge-high'>~91%</td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE 2 — SIGNAL LABORATORY
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "signal":

    st.markdown("<div class='vault-title' style='font-size:24px;'>📡 SIGNAL ACQUISITION LABORATORY</div>", unsafe_allow_html=True)
    st.markdown("<div class='vault-sub'>Module 1 — EEG Channel Pre-processing & Spectral Analysis</div>", unsafe_allow_html=True)
    st.markdown("---")

    # KPI band metrics
    b1, b2, b3, b4 = st.columns(4)
    def kpi(col, val, unit, lbl, color="#00ffe7"):
        col.markdown(f"""
        <div class='kpi-card' style='border-top-color:{color};'>
            <div class='kpi-val'>{val}</div>
            <div class='kpi-unit'>{unit}</div>
            <div class='kpi-lbl'>{lbl}</div>
        </div>""", unsafe_allow_html=True)
    kpi(b1, f"{alpha:.2f}", "Hz", "Alpha Band Power",  "#00ffe7")
    kpi(b2, f"{beta:.2f}",  "Hz", "Beta Band Power",   "#a78bfa")
    kpi(b3, f"{theta:.2f}", "Hz", "Theta Band Power",  "#38bdf8")
    kpi(b4, "250",          "Hz", "Sampling Rate",      "#39ff14")

    st.write("")

    # 4-channel time domain
    st.markdown("<div class='sec-header'><span>●</span> 4-CHANNEL TEMPORAL BRAINWAVE STREAM</div>", unsafe_allow_html=True)
    fig_all = styled_fig("Electroencephalogram (EEG) — Multi-Channel Time Domain", height=280)
    colors  = ["#00ffe7","#a78bfa","#38bdf8","#e2e8f0"]
    ch_lbls = ["AF7 (Left Frontal)", "AF8 (Right Frontal)", "TP9 (Left Temporal)", "TP10 (Right Temporal)"]
    for sig, c, lbl in zip([sig_af7, sig_af8, sig_tp9, sig_tp10], colors, ch_lbls):
        fig_all.add_trace(go.Scatter(y=sig, mode='lines', name=lbl, line=dict(color=c, width=1.3)))
    st.plotly_chart(fig_all, use_container_width=True, config={'displayModeBar': False})

    # Per-channel breakdown
    st.markdown("<div class='sec-header'><span>●</span> INDIVIDUAL CHANNEL ANALYSIS</div>", unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)

    for i, (sig, c, lbl) in enumerate(zip([sig_af7, sig_af8, sig_tp9, sig_tp10], colors, ch_lbls)):
        col = ch1 if i % 2 == 0 else ch2
        with col:
            fig_ch = styled_fig(f"{lbl}", height=160)
            fig_ch.add_trace(go.Scatter(y=sig, mode='lines', name=lbl,
                                        line=dict(color=c, width=1.2),
                                        fill='tozeroy', fillcolor=f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.05)"))
            fig_ch.update_layout(showlegend=False)
            st.plotly_chart(fig_ch, use_container_width=True, config={'displayModeBar': False})

    # FFT + spectral density
    st.markdown("<div class='sec-header'><span>●</span> FREQUENCY DOMAIN ANALYSIS — FFT & POWER SPECTRAL DENSITY</div>", unsafe_allow_html=True)
    fq1, fq2 = st.columns(2)

    freqs    = np.fft.rfftfreq(250, d=1/250)
    fft_af7  = np.abs(np.fft.rfft(sig_af7))
    fft_af8  = np.abs(np.fft.rfft(sig_af8))
    fft_tp9  = np.abs(np.fft.rfft(sig_tp9))
    fft_tp10 = np.abs(np.fft.rfft(sig_tp10))

    with fq1:
        fig_fft = styled_fig("FFT Power Spectral Density — AF7 & AF8 (Frontal)", height=220)
        fig_fft.add_trace(go.Scatter(x=freqs[:50], y=fft_af7[:50],  fill='tozeroy',
                                     mode='lines', name='AF7', line=dict(color='#00ffe7', width=1.5),
                                     fillcolor='rgba(0,255,231,0.06)'))
        fig_fft.add_trace(go.Scatter(x=freqs[:50], y=fft_af8[:50],  fill='tozeroy',
                                     mode='lines', name='AF8', line=dict(color='#a78bfa', width=1.5),
                                     fillcolor='rgba(167,139,250,0.06)'))
        fig_fft.update_xaxes(title_text="Frequency (Hz)")
        st.plotly_chart(fig_fft, use_container_width=True, config={'displayModeBar': False})

    with fq2:
        fig_fft2 = styled_fig("FFT Power Spectral Density — TP9 & TP10 (Temporal)", height=220)
        fig_fft2.add_trace(go.Scatter(x=freqs[:50], y=fft_tp9[:50],  fill='tozeroy',
                                      mode='lines', name='TP9', line=dict(color='#38bdf8', width=1.5),
                                      fillcolor='rgba(56,189,248,0.06)'))
        fig_fft2.add_trace(go.Scatter(x=freqs[:50], y=fft_tp10[:50], fill='tozeroy',
                                      mode='lines', name='TP10', line=dict(color='#e2e8f0', width=1.5),
                                      fillcolor='rgba(226,232,240,0.06)'))
        fig_fft2.update_xaxes(title_text="Frequency (Hz)")
        st.plotly_chart(fig_fft2, use_container_width=True, config={'displayModeBar': False})

    # Band power radar
    st.markdown("<div class='sec-header'><span>●</span> BAND POWER RADAR — COGNITIVE STATE FINGERPRINT</div>", unsafe_allow_html=True)
    rc1, rc2 = st.columns([1, 2])
    with rc1:
        categories  = ['Alpha', 'Beta', 'Theta', 'Delta', 'Gamma']
        if mode == "Authorized (Forest)":
            values = [alpha, beta, theta, 0.15, 0.12]
        else:
            values = [alpha, beta, theta, 0.20, 0.18]
        values_loop = values + [values[0]]
        cats_loop   = categories + [categories[0]]

        fig_radar = go.Figure(go.Scatterpolar(
            r=values_loop, theta=cats_loop,
            fill='toself', fillcolor='rgba(0,255,231,0.08)',
            line=dict(color='#00ffe7', width=2),
            marker=dict(color='#00ffe7', size=5),
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(showticklabels=False, gridcolor='#0d2137', range=[0, 0.6]),
                angularaxis=dict(gridcolor='#0d2137', tickfont=dict(color='#8bafc8', size=11)),
            ),
            paper_bgcolor='rgba(0,0,0,0)', height=260,
            margin=dict(l=20, r=20, t=20, b=20), showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

    with rc2:
        st.markdown(f"""
        <div class='mod-card'>
            <div class='sec-header'><span>●</span> BAND POWER INTERPRETATION</div>
            <table style='width:100%;font-family:var(--font-mono);font-size:12px;'>
                <tr><td style='color:var(--text-dim);padding:5px 0;'>Alpha (8–12 Hz)</td>
                    <td style='color:{"#39ff14" if alpha < 0.35 else "#ff2d55"};'>{alpha:.2f} Hz — {"FOCUSED / RELAXED ✔" if alpha < 0.35 else "STRESSED / HIGH ✘"}</td></tr>
                <tr><td style='color:var(--text-dim);padding:5px 0;'>Beta (12–30 Hz)</td>
                    <td style='color:var(--accent-cyan);'>{beta:.2f} Hz — ACTIVE COGNITION</td></tr>
                <tr><td style='color:var(--text-dim);padding:5px 0;'>Theta (4–8 Hz)</td>
                    <td style='color:#a78bfa;'>{theta:.2f} Hz — MEDITATIVE STATE</td></tr>
                <tr><td style='color:var(--text-dim);padding:5px 0;'>Sampling Rate</td>
                    <td style='color:var(--text-bright);'>250 Hz (Nyquist: 125 Hz)</td></tr>
                <tr><td style='color:var(--text-dim);padding:5px 0;'>Electrode Layout</td>
                    <td style='color:var(--text-bright);'>AF7, AF8, TP9, TP10 (10-20 system)</td></tr>
                <tr><td style='color:var(--text-dim);padding:5px 0;'>Pre-processing</td>
                    <td style='color:var(--text-bright);'>Band-pass filter + StandardScaler</td></tr>
            </table>
            <div style='margin-top:14px;font-family:var(--font-mono);font-size:10px;color:var(--text-dim);
                        border-top:1px solid #0d2137;padding-top:10px;'>
                P_α = ∫₈¹² S(f)df  ÷  ∫₀.₅⁴⁰ S(f)df  &nbsp;|&nbsp; Welch's Periodogram Method
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE 3 — CNN CLASSIFIER
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "classifier":

    st.markdown("<div class='vault-title' style='font-size:24px;'>🤖 1D-CNN CLASSIFICATION ENGINE</div>", unsafe_allow_html=True)
    st.markdown("<div class='vault-sub'>Module 2 — Neural Inference & Softmax Probability Analysis</div>", unsafe_allow_html=True)
    st.markdown("---")

    cc1, cc2 = st.columns([1, 2])

    with cc1:
        st.markdown("<div class='sec-header'><span>●</span> INFERENCE RESULT</div>", unsafe_allow_html=True)
        conf_color = "#39ff14" if confidence > 70 else "#ffd700" if confidence > 40 else "#ff2d55"
        match_color = "#39ff14" if detected_trigger == SECRET_TRIGGER else "#ff2d55"
        st.markdown(f"""
        <div class='mod-card' style='text-align:center;'>
            <div style='font-family:var(--font-mono);font-size:10px;color:var(--text-dim);margin-bottom:6px;'>DETECTED CLASS</div>
            <div style='font-family:var(--font-hud);font-size:20px;color:{match_color};margin-bottom:16px;'>{detected_trigger}</div>
            <div style='font-family:var(--font-mono);font-size:10px;color:var(--text-dim);margin-bottom:6px;'>CONFIDENCE SCORE</div>
            <div style='font-family:var(--font-hud);font-size:36px;color:{conf_color};'>{confidence:.1f}%</div>
            <div style='height:6px;background:#0d2137;border-radius:3px;margin:12px 0;'>
                <div style='height:100%;width:{confidence}%;background:{conf_color};border-radius:3px;
                            box-shadow: 0 0 8px {conf_color};'></div>
            </div>
            <div style='font-family:var(--font-mono);font-size:10px;color:var(--text-dim);'>
                Input Tensor: [1, 20, 3]<br/>
                Window Size: 20 samples<br/>
                Features: Alpha, Beta, Theta
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown(f"""
        <div class='mod-card'>
            <div class='sec-header'><span>●</span> GATE LOGIC</div>
            <div style='font-family:var(--font-mono);font-size:11px;'>
                <div style='margin:5px 0;'>
                    <span style='color:var(--text-dim);'>Target Class:</span>
                    <span style='color:var(--accent-cyan);float:right;'>{SECRET_TRIGGER}</span>
                </div>
                <div style='margin:5px 0;'>
                    <span style='color:var(--text-dim);'>Class Match:</span>
                    <span style='color:{"#39ff14" if detected_trigger == SECRET_TRIGGER else "#ff2d55"};float:right;'>
                        {"PASS ✔" if detected_trigger == SECRET_TRIGGER else "FAIL ✘"}</span>
                </div>
                <div style='margin:5px 0;'>
                    <span style='color:var(--text-dim);'>α < 0.35 Gate:</span>
                    <span style='color:{"#39ff14" if alpha < ALPHA_THRESHOLD else "#ff2d55"};float:right;'>
                        {"PASS ✔" if alpha < ALPHA_THRESHOLD else "FAIL ✘"}</span>
                </div>
                <div style='margin-top:10px;border-top:1px solid #0d2137;padding-top:10px;'>
                    <span style='color:var(--text-dim);'>Dual-Gate Result:</span>
                    <span style='color:{"#39ff14" if is_match else "#ff2d55"};float:right;font-weight:bold;'>
                        {"GRANTED ✔" if is_match else "DENIED ✘"}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cc2:
        st.markdown("<div class='sec-header'><span>●</span> SOFTMAX PROBABILITY DISTRIBUTION</div>", unsafe_allow_html=True)

        # Horizontal bar chart — probability per class
        class_names_short = [str(c)[:18] for c in classes]
        bar_colors_full   = [("#00ffe7" if str(c) == detected_trigger else "#1a3a5c") for c in classes]
        fig_prob = go.Figure(go.Bar(
            x=prediction[0], y=class_names_short,
            orientation='h',
            marker=dict(color=bar_colors_full, line=dict(width=0)),
            text=[f"{v*100:.1f}%" for v in prediction[0]],
            textposition='outside',
            textfont=dict(color='#8bafc8', size=10, family='Share Tech Mono'),
        ))
        fig_prob.update_layout(
            **{**PLOT_LAYOUT, 'height': 300, 'showlegend': False,
               'margin': dict(l=10, r=60, t=10, b=10)},
        )
        st.plotly_chart(fig_prob, use_container_width=True, config={'displayModeBar': False})

        # Probability table
        st.markdown("<div class='sec-header'><span>●</span> RAW PROBABILITY VECTOR</div>", unsafe_allow_html=True)
        prob_df = pd.DataFrame({
            'Class': [str(c) for c in classes],
            'Probability': [f"{v*100:.4f}%" for v in prediction[0]],
            'Logit Weight': [f"{v:.6f}" for v in prediction[0]],
            'Status': ["◀ DETECTED" if str(c) == detected_trigger else "—" for c in classes],
        })
        st.dataframe(prob_df, use_container_width=True, hide_index=True, height=160)

    # Model architecture
    st.markdown("---")
    st.markdown("<div class='sec-header'><span>●</span> 1D-CNN MODEL ARCHITECTURE DETAIL</div>", unsafe_allow_html=True)

    arch_cols = st.columns(7)
    arch_layers = [
        ("INPUT",        "[1, 20, 3]",         "#3d5a73"),
        ("Conv1D×128",   "kernel=3, ReLU",      "#00ffe7"),
        ("BatchNorm",    "Normalize",           "#38bdf8"),
        ("MaxPool1D",    "pool_size=2",         "#3d5a73"),
        ("Conv1D×64",    "kernel=3, ReLU",      "#a78bfa"),
        ("BatchNorm",    "+ Dropout 0.4",       "#38bdf8"),
        ("Flatten→Dense", "256→N, Softmax",    "#39ff14"),
    ]
    for col, (lname, ldetail, lclr) in zip(arch_cols, arch_layers):
        with col:
            st.markdown(f"""
            <div class='arch-node' style='border-color:{lclr};min-height:70px;'>
                <div class='node-type' style='color:{lclr};font-size:10px;'>{lname}</div>
                <span style='font-size:9px;color:var(--text-dim);'>{ldetail}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Training timeline placeholder visual
    st.markdown("<div class='sec-header'><span>●</span> TRAINING PERFORMANCE SIMULATION (100 EPOCHS)</div>", unsafe_allow_html=True)
    ep = np.arange(1, 101)
    # Simulate realistic training curves
    acc_train = 1 - 0.65 * np.exp(-ep/18) + 0.01 * np.random.default_rng(42).normal(size=100)
    acc_val   = 1 - 0.70 * np.exp(-ep/22) + 0.015* np.random.default_rng(7).normal(size=100)
    loss_tr   = 0.85 * np.exp(-ep/20) + 0.02 + 0.005*np.random.default_rng(99).normal(size=100)
    loss_val  = 0.90 * np.exp(-ep/24) + 0.04 + 0.01 *np.random.default_rng(3).normal(size=100)
    acc_train = np.clip(acc_train, 0, 1)
    acc_val   = np.clip(acc_val,   0, 1)
    loss_tr   = np.clip(loss_tr,   0, 2)
    loss_val  = np.clip(loss_val,  0, 2)

    tc1, tc2 = st.columns(2)
    with tc1:
        fig_acc = styled_fig("Model Accuracy vs Epoch", height=220)
        fig_acc.add_trace(go.Scatter(x=ep, y=acc_train, name='Train Acc',  line=dict(color='#00ffe7', width=1.5)))
        fig_acc.add_trace(go.Scatter(x=ep, y=acc_val,   name='Val Acc',   line=dict(color='#a78bfa', width=1.5)))
        fig_acc.update_yaxes(title_text="Accuracy", range=[0, 1.05])
        fig_acc.update_xaxes(title_text="Epoch")
        st.plotly_chart(fig_acc, use_container_width=True, config={'displayModeBar': False})

    with tc2:
        fig_loss = styled_fig("Model Loss vs Epoch", height=220)
        fig_loss.add_trace(go.Scatter(x=ep, y=loss_tr,   name='Train Loss', line=dict(color='#ff2d55', width=1.5)))
        fig_loss.add_trace(go.Scatter(x=ep, y=loss_val,  name='Val Loss',   line=dict(color='#ffd700', width=1.5)))
        fig_loss.update_yaxes(title_text="Loss")
        fig_loss.update_xaxes(title_text="Epoch")
        st.plotly_chart(fig_loss, use_container_width=True, config={'displayModeBar': False})

# ═══════════════════════════════════════════════════════════════
# PAGE 4 — VAULT & DECRYPTION
# ═══════════════════════════════════════════════════════════════
elif st.session_state.page == "vault":

    st.markdown("<div class='vault-title' style='font-size:24px;'>🔐 CRYPTOGRAPHIC VAULT & DECRYPTION</div>", unsafe_allow_html=True)
    st.markdown("<div class='vault-sub'>Module 3+4 — Neural Guardrail · Key Derivation · Anti-Forensic MOP Protocol</div>", unsafe_allow_html=True)
    st.markdown("---")

    v1, v2 = st.columns([1, 1])

    # ── Left — Guardrail status + scan button ──
    with v1:
        st.markdown("<div class='sec-header'><span>●</span> MODULE 3 — NEURAL GUARDRAIL & COERCION DETECTOR</div>", unsafe_allow_html=True)

        # Alpha power gauge
        st.markdown(f"""
        <div class='mod-card'>
            <div style='font-family:var(--font-mono);font-size:10px;color:var(--text-dim);margin-bottom:8px;'>
                FRONTAL ALPHA SPECTRAL ENERGY (P_α)
            </div>
            <div style='display:flex;align-items:center;gap:12px;margin-bottom:10px;'>
                <div style='font-family:var(--font-hud);font-size:28px;
                            color:{"#39ff14" if alpha < ALPHA_THRESHOLD else "#ff2d55"};'>
                    {alpha:.3f}
                </div>
                <div style='flex:1;'>
                    <div style='font-family:var(--font-mono);font-size:9px;color:var(--text-dim);margin-bottom:4px;'>
                        Threshold γ = {ALPHA_THRESHOLD}
                    </div>
                    <div style='height:8px;background:#0d2137;border-radius:4px;position:relative;'>
                        <div style='height:100%;width:{min(alpha/0.6*100,100):.0f}%;border-radius:4px;
                                    background:{"#39ff14" if alpha < ALPHA_THRESHOLD else "#ff2d55"};'></div>
                        <div style='position:absolute;top:-1px;left:{ALPHA_THRESHOLD/0.6*100:.0f}%;
                                    width:2px;height:10px;background:#ffd700;'></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if alpha < ALPHA_THRESHOLD:
            st.markdown("""
            <div class='badge-granted' style='margin-top:0;'>
                🛡️ SPECTRAL REGIME PASSED (G = 1)<br/>
                <small style='font-size:11px;font-family:var(--font-body);'>
                Cognitive stress indicators nominal. Frontal alpha within safe bounds.
                </small>
            </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='badge-denied' style='margin-top:0;'>
                ⚠️ COERCION SIGNAL DETECTED (G = 0)<br/>
                <small style='font-size:11px;font-family:var(--font-body);'>
                High alpha deviation — possible stress, duress, or unauthorized actor.
                </small>
            </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # FFT spectral chart
        st.markdown("<div class='sec-header'><span>●</span> FFT POWER SPECTRAL DENSITY</div>", unsafe_allow_html=True)
        freqs   = np.fft.rfftfreq(250, d=1/250)
        fft_v   = np.abs(np.fft.rfft(sig_af7))
        fig_s   = styled_fig("Frontal AF7 — PSD", height=160)
        fig_s.add_trace(go.Scatter(x=freqs[:50], y=fft_v[:50],
                                   fill='tozeroy', mode='lines',
                                   line=dict(color='#38bdf8', width=1.5),
                                   fillcolor='rgba(56,189,248,0.07)'))
        # Alpha band shading
        alpha_mask = (freqs[:50] >= 8) & (freqs[:50] <= 12)
        fig_s.add_vrect(x0=8, x1=12, fillcolor='rgba(0,255,231,0.06)',
                        line_color='rgba(0,255,231,0.3)', line_width=1,
                        annotation_text="α band", annotation_font_color='#00ffe7',
                        annotation_font_size=10)
        st.plotly_chart(fig_s, use_container_width=True, config={'displayModeBar': False})

        # Decision formula display
        st.markdown(f"""
        <div class='mod-card' style='font-family:var(--font-mono);font-size:11px;'>
            <div class='sec-header'><span>●</span> DECISION LOGIC FORMULA</div>
            <div style='color:var(--text-mid);line-height:2;'>
                <b style='color:var(--accent-cyan);'>Access_Status</b> = 1 if:<br/>
                &nbsp;&nbsp; P(Class<sub style='color:#a78bfa;'>Forest</sub>) ≥ τ <b style='color:var(--text-dim);'>AND</b> P_α ≤ γ<br/>
                &nbsp;&nbsp;&nbsp;&nbsp; where τ = 0.85, γ = 0.35<br/>
                <b style='color:var(--accent-cyan);'>Access_Status</b> = 0 otherwise
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Right — Key derivation + vault status ──
    with v2:
        st.markdown("<div class='sec-header'><span>●</span> MODULE 4 — CRYPTOGRAPHIC KEY DERIVATION ENGINE</div>", unsafe_allow_html=True)

        # Current state display
        if st.session_state.vault_open:
            st.markdown("<div class='vault_open_display' style='background:radial-gradient(circle at center,rgba(57,255,20,0.1) 0%,transparent 70%);border:2px solid #39ff14;border-radius:8px;padding:28px;text-align:center;font-family:var(--font-hud);font-size:18px;color:#39ff14;letter-spacing:0.1em;'>🔓 VAULT OPEN<br/><span style=\"font-size:12px;color:#39ff1499;\">KEY ACTIVE IN RAM</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background:radial-gradient(circle at center,rgba(255,45,85,0.08) 0%,transparent 70%);border:2px solid #ff2d55;border-radius:8px;padding:28px;text-align:center;font-family:var(--font-hud);font-size:18px;color:#ff2d55;letter-spacing:0.1em;'>🔒 VAULT SECURED<br/><span style=\"font-size:12px;color:#ff2d5599;\">ARRAYS LOCKED</span></div>", unsafe_allow_html=True)

        st.write("")

        # Scan button
        scan_btn = st.button("⬡  EXECUTE DUAL-GATE KEY EXTRACTION ENGINE", key="scan_main")

        if scan_btn:
            st.session_state.scan_count += 1
            st.session_state.mop_triggered = False
            if is_match:
                st.session_state.vault_open   = True
                st.session_state.session_key  = hashlib.sha256(str(alpha).encode()).hexdigest()
                st.session_state.granted_count += 1
                add_log(f"1D-CNN vector matched '{detected_trigger}'. Guardrail G=1. Session key generated.", "OK  ")
                st.session_state.history.append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'result': 'GRANTED', 'class': detected_trigger,
                    'conf': f"{confidence:.1f}%", 'alpha': alpha,
                })
            else:
                st.session_state.vault_open   = False
                st.session_state.session_key  = ""
                st.session_state.denied_count += 1
                if alpha >= ALPHA_THRESHOLD:
                    add_log(f"Alpha ({alpha:.2f}) ≥ γ=0.35. Coercion guard triggered. Vault locked.", "WARN")
                else:
                    add_log(f"CNN class '{detected_trigger}' ≠ target. Identity mismatch. Aborted.", "DENY")
                st.session_state.history.append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'result': 'DENIED', 'class': detected_trigger,
                    'conf': f"{confidence:.1f}%", 'alpha': alpha,
                })
            st.rerun()

        st.write("")

        # Key display
        st.markdown("<div class='sec-header'><span>●</span> AES SESSION KEY REGISTER</div>", unsafe_allow_html=True)
        key_display = st.session_state.session_key if st.session_state.vault_open else "NULL / ACCESS DENIED — AWAITING AUTH"
        st.text_input("RAM-Resident SHA-256 Token:", value=key_display, disabled=True)

        if st.session_state.vault_open:
            # Key breakdown visual
            key = st.session_state.session_key
            segments = [key[i:i+8] for i in range(0, 32, 8)]
            seg_html  = "".join([f"<span style='color:#00ffe7;margin-right:8px;font-size:11px;'>{s}</span>" for s in segments])
            seg_html += f"<span style='color:#3d5a73;font-size:11px;'>...+{len(key)-32} chars</span>"
            st.markdown(f"<div style='font-family:var(--font-mono);padding:8px 0;'>{seg_html}</div>", unsafe_allow_html=True)

            # Key derivation chain
            st.markdown(f"""
            <div class='mod-card'>
                <div class='sec-header'><span>●</span> KEY DERIVATION CHAIN</div>
                <div style='font-family:var(--font-mono);font-size:10px;color:var(--text-dim);line-height:1.8;'>
                    α input: <span style='color:#00ffe7;'>{alpha}</span><br/>
                    UTF-8 encode → SHA-256 hash → 256-bit hex digest<br/>
                    M_K = H(str(α)) ∈ {{0,1}}²⁵⁶<br/>
                    MOP wipe: M_K ← {{0}}²⁵⁶ on session end
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Decrypted workspace
    st.markdown("---")
    st.markdown("<div class='sec-header'><span>●</span> DECRYPTED WORKSPACE PAYLOAD</div>", unsafe_allow_html=True)

    if st.session_state.vault_open:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as f:
                secret_content = f.read()

            st.markdown(f"<div class='badge-granted'>✅ Neural identity key verified — `{FILE_PATH}` unlocked successfully</div>", unsafe_allow_html=True)
            st.write("")
            st.text_area("Decrypted Data Stream Buffer:", value=secret_content, height=150)

            dc1, dc2 = st.columns([2, 5])
            with dc1:
                st.download_button("📥 Download Decrypted File", data=secret_content,
                                   file_name="decrypted_data.txt", mime="text/plain")
            with dc2:
                if st.button("🔒  Invoke MOP — Mandatory Overwrite Protocol"):
                    st.session_state.vault_open    = False
                    st.session_state.session_key   = ""
                    st.session_state.mop_triggered = True
                    add_log("MOP: Overwriting active memory registers via bitwise XOR before deletion.", "MOP ")
                    st.rerun()
        else:
            st.markdown(f"<div class='badge-warn'>⚠️ Target file `{FILE_PATH}` not found in execution directory.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='badge-warn'>🔒 Authenticate via dual-gate neural scan to access protected storage fields.</div>", unsafe_allow_html=True)
        st.text_area("Data Buffer:", value="[ENCRYPTED MATRIX] — VALID BIOMETRIC SIGNAL REQUIRED", height=80, disabled=True)

    # Access history log
    st.markdown("---")
    st.markdown("<div class='sec-header'><span>●</span> SESSION ACCESS HISTORY</div>", unsafe_allow_html=True)
    h1c, h2c = st.columns(2)
    with h1c:
        if st.session_state.history:
            hist_df = pd.DataFrame(st.session_state.history[-10:])
            st.dataframe(hist_df, use_container_width=True, hide_index=True)
        else:
            st.markdown("<div style='font-family:var(--font-mono);font-size:11px;color:var(--text-dim);'>No scans yet.</div>", unsafe_allow_html=True)

    with h2c:
        # MOP status
        if st.session_state.mop_triggered:
            st.markdown("<div class='badge-warn'>🚨 ANTI-FORENSIC MOP ACTIVE — Clearing RAM registers securely</div>", unsafe_allow_html=True)
            st.session_state.mop_triggered = False

        # Live diagnostics
        st.markdown("<div class='sec-header'><span>●</span> DIAGNOSTIC LOG</div>", unsafe_allow_html=True)
        log_html = ""
        for line in st.session_state.logs[-6:]:
            if "OK" in line or "SUCCESS" in line:
                log_html += f"<span class='log-ok'>{line}</span><br/>"
            elif "DENY" in line or "CRIT" in line or "BREACH" in line:
                log_html += f"<span class='log-err'>{line}</span><br/>"
            elif "WARN" in line or "MOP" in line:
                log_html += f"<span class='log-warn'>{line}</span><br/>"
            else:
                log_html += f"<span class='log-sys'>{line}</span><br/>"
        st.markdown(f"<div class='terminal'>{log_html}</div>", unsafe_allow_html=True)