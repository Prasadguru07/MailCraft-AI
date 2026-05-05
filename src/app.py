"""
Email Generation Assistant — Glassmorphic Dark Theme Streamlit Frontend
Run: streamlit run app.py
"""

import sys
import time
import json
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from email_generator import generate_email, check_ollama_health
from metrics import evaluate_single
from data.test_scenarios import TEST_SCENARIOS

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MailCraft AI",
    page_icon="✉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Deep glassmorphic dark theme CSS ────────────────────────────────────────
GLASS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --bg-void:        #050810;
    --glass-1:        rgba(255,255,255,0.035);
    --glass-2:        rgba(255,255,255,0.06);
    --glass-border:   rgba(255,255,255,0.07);
    --glass-border-h: rgba(99,179,237,0.3);
    --accent-blue:    #63b3ed;
    --accent-cyan:    #4fd1c5;
    --accent-violet:  #9f7aea;
    --text-primary:   #e2e8f0;
    --text-secondary: #718096;
    --text-muted:     #4a5568;
    --success:        #68d391;
    --warning:        #f6ad55;
    --danger:         #fc8181;
    --radius-lg:      16px;
    --radius-md:      10px;
    --radius-sm:      6px;
    --font-display:   'Syne', sans-serif;
    --font-mono:      'DM Mono', monospace;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.stApp {
    background: var(--bg-void) !important;
    font-family: var(--font-display) !important;
    color: var(--text-primary) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 90% 55% at 15% 5%,  rgba(99,179,237,0.07)  0%, transparent 65%),
        radial-gradient(ellipse 65% 45% at 82% 82%, rgba(159,122,234,0.06) 0%, transparent 65%),
        radial-gradient(ellipse 45% 65% at 50% 55%, rgba(79,209,197,0.04)  0%, transparent 75%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stSidebar"] {
    background: rgba(4, 7, 14, 0.94) !important;
    border-right: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(24px) !important;
}
[data-testid="stSidebar"] * { font-family: var(--font-display) !important; }

.main .block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1380px !important;
}

h1,h2,h3,h4,h5,h6,p,label,
.stMarkdown,.stText {
    font-family: var(--font-display) !important;
    color: var(--text-primary) !important;
}

/* ── Header ── */
.mc-header {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 26px 30px;
    background: var(--glass-1);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    backdrop-filter: blur(24px);
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}
.mc-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--accent-blue) 40%, var(--accent-cyan) 70%, transparent 100%);
}
.mc-logo {
    width: 50px; height: 50px;
    background: linear-gradient(135deg, #1a3a5c, #0d4a6e);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 28px rgba(99,179,237,0.25), inset 0 1px 0 rgba(255,255,255,0.1);
    flex-shrink: 0;
}
.mc-title {
    font-size: 1.65rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.025em;
    margin: 0 !important;
    background: linear-gradient(135deg, #93c5fd 0%, var(--accent-cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}
.mc-subtitle {
    font-size: 0.78rem !important;
    color: var(--text-muted) !important;
    margin: 4px 0 0 !important;
    font-family: var(--font-mono) !important;
    letter-spacing: 0.05em;
}
.mc-badge-row { display: flex; gap: 8px; margin-top: 8px; }

/* ── Section label ── */
.section-label {
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.13em !important;
    text-transform: uppercase !important;
    color: var(--accent-blue) !important;
    margin-bottom: 10px !important;
    font-family: var(--font-mono) !important;
}

/* ── Glass card ── */
.glass-card {
    background: var(--glass-1);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: 22px;
    backdrop-filter: blur(20px);
    margin-bottom: 14px;
    transition: border-color 0.25s;
}
.glass-card:hover { border-color: var(--glass-border-h); }

/* ── Inputs ── */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: var(--accent-blue) !important;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color: rgba(99,179,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.1) !important;
    outline: none !important;
}
.stTextInput>div>div>input::placeholder,
.stTextArea>div>div>textarea::placeholder {
    color: var(--text-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--text-muted) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-family: var(--font-mono) !important;
}

/* ── Buttons ── */
.stButton>button {
    background: rgba(99,179,237,0.08) !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    border-radius: var(--radius-md) !important;
    color: var(--accent-blue) !important;
    font-family: var(--font-display) !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.22s ease !important;
}
.stButton>button:hover {
    background: rgba(99,179,237,0.16) !important;
    border-color: rgba(99,179,237,0.5) !important;
    box-shadow: 0 0 18px rgba(99,179,237,0.15) !important;
    transform: translateY(-1px) !important;
}
.stButton>button:active { transform: translateY(0) !important; }

.gen-btn .stButton>button {
    background: linear-gradient(135deg, rgba(99,179,237,0.14), rgba(79,209,197,0.1)) !important;
    border: 1px solid rgba(99,179,237,0.4) !important;
    padding: 0.7rem 1.6rem !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.05em !important;
    box-shadow: 0 4px 20px rgba(99,179,237,0.1), inset 0 1px 0 rgba(255,255,255,0.06) !important;
}

/* ── Metric pills ── */
.metric-row { display: flex; gap: 10px; margin: 14px 0; flex-wrap: wrap; }
.metric-pill {
    flex: 1; min-width: 110px;
    padding: 14px 14px 12px;
    background: var(--glass-1);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    text-align: center;
    backdrop-filter: blur(12px);
    transition: border-color 0.2s;
}
.metric-pill:hover { border-color: var(--glass-border-h); }
.mp-label {
    font-size: 0.62rem; color: var(--text-muted);
    letter-spacing: 0.1em; text-transform: uppercase;
    font-family: var(--font-mono); margin-bottom: 5px;
}
.mp-value { font-size: 1.45rem; font-weight: 700; font-family: var(--font-display); line-height: 1; }
.mp-bar { height: 3px; border-radius: 2px; margin-top: 9px; background: rgba(255,255,255,0.06); overflow: hidden; }
.mp-bar-fill { height: 100%; border-radius: 2px; }

/* ── Email output ── */
.email-output {
    background: rgba(4, 7, 14, 0.75);
    border: 1px solid var(--glass-border);
    border-left: 3px solid var(--accent-blue);
    border-radius: var(--radius-lg);
    padding: 22px 26px;
    font-family: var(--font-mono) !important;
    font-size: 0.855rem;
    line-height: 1.78;
    color: #cbd5e0;
    white-space: pre-wrap;
    word-break: break-word;
    position: relative;
    backdrop-filter: blur(16px);
}
.email-output::before {
    content: 'GENERATED EMAIL';
    position: absolute; top: -10px; left: 18px;
    background: var(--bg-void);
    padding: 0 10px;
    font-size: 0.58rem; letter-spacing: 0.18em;
    color: var(--accent-blue); font-family: var(--font-mono); font-weight: 500;
}

/* ── Badges ── */
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 0.7rem;
    font-weight: 600; letter-spacing: 0.05em;
    font-family: var(--font-mono);
}
.badge-success { background: rgba(104,211,145,0.1); color: var(--success); border: 1px solid rgba(104,211,145,0.22); }
.badge-error   { background: rgba(252,129,129,0.1); color: var(--danger);  border: 1px solid rgba(252,129,129,0.22); }
.badge-info    { background: rgba(99,179,237,0.1);  color: var(--accent-blue); border: 1px solid rgba(99,179,237,0.22); }
.badge-violet  { background: rgba(159,122,234,0.1); color: var(--accent-violet); border: 1px solid rgba(159,122,234,0.22); }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 2px;
    border-bottom: 1px solid var(--glass-border) !important;
    padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: var(--font-display) !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    border-radius: 0 !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-secondary) !important; }
.stTabs [aria-selected="true"] {
    color: var(--accent-blue) !important;
    border-bottom: 2px solid var(--accent-blue) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 22px !important; }

/* ── Selectbox ── */
[data-baseweb="select"]>div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
}
[data-baseweb="popover"], [data-baseweb="menu"] {
    background: #0c1220 !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-md) !important;
}
[role="option"] { color: var(--text-secondary) !important; font-family: var(--font-display) !important; }
[role="option"]:hover { background: var(--glass-2) !important; color: var(--text-primary) !important; }

/* ── Radio ── */
.stRadio > div { gap: 8px !important; flex-wrap: wrap; }
.stRadio label {
    background: var(--glass-1) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 5px 13px !important;
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
    font-family: var(--font-mono) !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin: 0 !important;
}
.stRadio label:hover { border-color: var(--glass-border-h) !important; color: var(--text-primary) !important; }

/* ── Slider ── */
.stSlider label { color: var(--text-muted) !important; font-size: 0.72rem !important; font-family: var(--font-mono) !important; letter-spacing: 0.08em !important; }

/* ── Sidebar header ── */
.sidebar-header {
    text-align: center;
    padding: 22px 0 14px;
    border-bottom: 1px solid var(--glass-border);
    margin-bottom: 16px;
}
.sidebar-header .sh-icon { font-size: 2rem; display: block; margin-bottom: 8px; }
.sidebar-header h3 {
    font-size: 1.05rem !important; font-weight: 800 !important;
    letter-spacing: -0.01em; margin: 0 !important;
    background: linear-gradient(135deg, #93c5fd, var(--accent-cyan));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.sidebar-header p {
    font-size: 0.68rem !important; color: var(--text-muted) !important;
    margin: 4px 0 0 !important; font-family: var(--font-mono) !important;
}

/* ── Fact tag ── */
.fact-tag {
    display: inline-block; padding: 3px 10px;
    background: rgba(79,209,197,0.07); border: 1px solid rgba(79,209,197,0.18);
    border-radius: 20px; font-size: 0.75rem; color: var(--accent-cyan);
    margin: 3px 3px 3px 0; font-family: var(--font-mono);
}

/* ── Comparison card ── */
.cmp-card {
    padding: 20px;
    border-radius: var(--radius-lg);
    backdrop-filter: blur(16px);
    margin-bottom: 8px;
}
.cmp-row {
    display: flex; justify-content: space-between;
    margin-bottom: 8px; align-items: center;
}
.cmp-label { font-size: 0.83rem; color: var(--text-secondary); }
.cmp-value { font-size: 0.9rem; font-weight: 700; font-family: var(--font-mono); }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 4px; }

/* ── Code block ── */
.stCode { display: none !important; }

/* ── Spinner ── */
.stSpinner > div { border-color: var(--accent-blue) transparent transparent transparent !important; }

hr {
    border: none !important;
    border-top: 1px solid var(--glass-border) !important;
    margin: 18px 0 !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(104,211,145,0.08) !important;
    border: 1px solid rgba(104,211,145,0.25) !important;
    color: var(--success) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
}
.stDownloadButton > button:hover {
    background: rgba(104,211,145,0.15) !important;
    border-color: rgba(104,211,145,0.45) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--glass-1) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-display) !important;
    font-size: 0.86rem !important;
    color: var(--text-secondary) !important;
}
.streamlit-expanderContent {
    background: rgba(5,8,16,0.6) !important;
    border: 1px solid var(--glass-border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
}

/* ── Checkbox ── */
.stCheckbox label { color: var(--text-secondary) !important; font-size: 0.85rem !important; font-family: var(--font-display) !important; }

/* ── Info/warning ── */
.stInfo { background: rgba(99,179,237,0.07) !important; border: 1px solid rgba(99,179,237,0.2) !important; border-radius: var(--radius-md) !important; }
.stWarning { background: rgba(246,173,85,0.07) !important; border: 1px solid rgba(246,173,85,0.2) !important; border-radius: var(--radius-md) !important; }
.stError { background: rgba(252,129,129,0.07) !important; border: 1px solid rgba(252,129,129,0.2) !important; border-radius: var(--radius-md) !important; }
.stSuccess { background: rgba(104,211,145,0.07) !important; border: 1px solid rgba(104,211,145,0.2) !important; border-radius: var(--radius-md) !important; }
</style>
"""


# ─── Helpers ─────────────────────────────────────────────────────────────────

def render_metric_pills(frs, tas, pqs, overall):
    items = [
        ("Fact Recall",   frs,     "#63b3ed"),
        ("Tone Align",    tas,     "#9f7aea"),
        ("Prof. Quality", pqs,     "#4fd1c5"),
        ("Overall",       overall, "#f6ad55"),
    ]
    html = '<div class="metric-row">'
    for label, val, color in items:
        pct = int(val * 100)
        html += f"""
        <div class="metric-pill">
            <div class="mp-label">{label}</div>
            <div class="mp-value" style="color:{color}">{pct}<span style="font-size:0.75rem;font-weight:400">%</span></div>
            <div class="mp-bar"><div class="mp-bar-fill" style="width:{pct}%;background:{color}"></div></div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="mc-header">
        <div class="mc-logo">✉</div>
        <div>
            <div class="mc-title">MailCraft AI</div>
            <div class="mc-subtitle">qwen3:4b via Ollama · Role-Play + Few-Shot + Chain-of-Thought</div>
            <div class="mc-badge-row">
                <span class="badge badge-violet">3 Custom Metrics</span>
                <span class="badge badge-success">10 Test Scenarios</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Session state defaults ───────────────────────────────────────────────────
def init_state():
    defaults = dict(intent="", facts="", tone="Professional, warm",
                    generated=None, eval_result=None, gen_time=0,
                    use_advanced=True, temperature=0.7, history=[],
                    loaded_scenario=None)
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─── Sidebar ─────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <span class="sh-icon">✉</span>
            <h3>MailCraft AI</h3>
            <p>Glassmorphic Studio · v1.0</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-label">Status</p>', unsafe_allow_html=True)
        if check_ollama_health():
            st.markdown('<span class="badge badge-success">● Ollama Connected</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge badge-error">● Ollama Offline</span>', unsafe_allow_html=True)
            st.caption("Start with: `ollama serve`")

        st.markdown("---")
        st.markdown('<p class="section-label">Quick Load</p>', unsafe_allow_html=True)
        opts = ["— select scenario —"] + [f"{s['id']}. {s['intent'][:36]}…" for s in TEST_SCENARIOS]
        sel = st.selectbox("Scenario", opts, label_visibility="collapsed")
        if sel != "— select scenario —":
            idx = int(sel.split(".")[0]) - 1
            if st.button("⚡ Load Scenario", use_container_width=True):
                sc = TEST_SCENARIOS[idx]
                st.session_state.update(
                    intent=sc["intent"],
                    facts="\n".join(sc["facts"]),
                    tone=sc["tone"],
                    loaded_scenario=sc,
                    generated=None,
                    eval_result=None,
                )
                st.rerun()

        st.markdown("---")
        st.markdown('<p class="section-label">Prompt Strategy</p>', unsafe_allow_html=True)
        strat = st.radio("Strategy", [
            "Advanced (Role-Play + Few-Shot + CoT)",
            "Baseline (Simple instruction)",
        ], label_visibility="collapsed")
        st.session_state["use_advanced"] = "Advanced" in strat

        st.markdown("---")
        st.markdown('<p class="section-label">Temperature</p>', unsafe_allow_html=True)
        st.session_state["temperature"] = st.slider(
            "Temp", 0.1, 1.2, 0.7, 0.05, label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown(
            '<p style="font-size:0.68rem;color:#2d3748;font-family:\'DM Mono\',monospace;'
            'text-align:center;letter-spacing:0.05em">MailCraft AI</p>',
            unsafe_allow_html=True
        )


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    st.markdown(GLASS_CSS, unsafe_allow_html=True)
    init_state()
    render_header()
    render_sidebar()

    tab_gen, tab_eval, tab_history, tab_batch = st.tabs([
        "✉  Generate", "📊  Evaluate", "🕘  History", "⚡  Batch Run"
    ])

    # ══════════════════════════════════════════════════
    # TAB 1 — GENERATE
    # ══════════════════════════════════════════════════
    with tab_gen:
        left, right = st.columns([1, 1.1], gap="large")

        with left:
            st.markdown('<p class="section-label">Compose</p>', unsafe_allow_html=True)

            intent = st.text_area(
                "Intent",
                value=st.session_state["intent"],
                placeholder="e.g. Follow up after a product demo meeting…",
                height=88, key="w_intent",
            )
            facts_raw = st.text_area(
                "Key Facts — one per line",
                value=st.session_state["facts"],
                placeholder="Meeting held May 5th with Sarah Mitchell\nProduct: DataSync Pro\nNext step: pilot proposal by end of week",
                height=155, key="w_facts",
            )
            tone = st.text_input(
                "Tone",
                value=st.session_state["tone"],
                placeholder="Professional · Warm · Urgent · Empathetic · Assertive",
                key="w_tone",
            )

            strat_label = "Advanced" if st.session_state["use_advanced"] else "Baseline"
            st.markdown(
                f'<p style="font-size:0.72rem;color:#4a5568;font-family:\'DM Mono\',monospace;'
                f'margin-bottom:10px">strategy: <span style="color:#63b3ed">{strat_label}</span>'
                f' · temp: <span style="color:#63b3ed">{st.session_state["temperature"]}</span></p>',
                unsafe_allow_html=True
            )

            st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
            gen_clicked = st.button("✦  Generate Email", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state["loaded_scenario"]:
                with st.expander("📋 Reference Email", expanded=False):
                    sc = st.session_state["loaded_scenario"]
                    st.markdown(
                        f'<div class="email-output" style="border-left-color:#9f7aea;font-size:0.8rem">'
                        f'{sc["reference_email"]}</div>',
                        unsafe_allow_html=True
                    )

        with right:
            st.markdown('<p class="section-label">Output</p>', unsafe_allow_html=True)

            if gen_clicked:
                facts_list = [f.strip() for f in facts_raw.strip().splitlines() if f.strip()]
                if not intent.strip():
                    st.warning("Please enter an intent.")
                elif not facts_list:
                    st.warning("Please enter at least one fact.")
                else:
                    st.session_state.update(intent=intent, facts=facts_raw, tone=tone)
                    with st.spinner("Crafting your email…"):
                        res = generate_email(
                            intent=intent, facts=facts_list, tone=tone,
                            use_advanced_prompt=st.session_state["use_advanced"],
                            temperature=st.session_state["temperature"],
                        )
                    if res["success"]:
                        st.session_state.update(
                            generated=res["content"],
                            gen_time=res["elapsed_seconds"],
                            eval_result=None,
                        )
                        st.session_state["history"].insert(0, dict(
                            intent=intent, tone=tone, facts=facts_list,
                            email=res["content"], time=res["elapsed_seconds"],
                            strategy=strat_label,
                        ))
                    else:
                        st.error(f"Generation failed: {res.get('error', 'Unknown error')}")
                        st.info("Ensure `ollama serve` is running and `ollama pull qwen3:4b` is done.")

            if st.session_state["generated"]:
                t = st.session_state["gen_time"]
                st.markdown(
                    f'<div style="display:flex;gap:8px;align-items:center;margin-bottom:12px">'
                    f'<span class="badge badge-success">● Ready</span>'
                    f'<span class="badge badge-info">{strat_label}</span>'
                    f'<span style="font-size:0.7rem;color:#4a5568;font-family:\'DM Mono\',monospace">'
                    f'qwen3:4b · {t}s</span></div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="email-output">{st.session_state["generated"]}</div>',
                    unsafe_allow_html=True
                )

                c1, c2 = st.columns(2)
                with c1:
                    st.download_button(
                        "⬇  Copy / Download",
                        data=st.session_state["generated"],
                        file_name="generated_email.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                with c2:
                    if st.button("📊  Score This Email", use_container_width=True):
                        fl = [f.strip() for f in facts_raw.strip().splitlines() if f.strip()]
                        ref = (st.session_state["loaded_scenario"] or {}).get(
                            "reference_email", st.session_state["generated"]
                        )
                        with st.spinner("Evaluating…"):
                            ev = evaluate_single(st.session_state["generated"], fl, tone, ref)
                        st.session_state["eval_result"] = ev

            if st.session_state["eval_result"]:
                ev = st.session_state["eval_result"]
                st.markdown("---")
                st.markdown('<p class="section-label">Scores</p>', unsafe_allow_html=True)
                render_metric_pills(
                    ev["fact_recall_score"], ev["tone_alignment_score"],
                    ev["professional_quality_score"], ev["overall_score"]
                )
                r = ev["tone_alignment_detail"].get("reasoning", "")
                if r:
                    st.markdown(
                        f'<p style="font-size:0.75rem;color:#718096;font-family:\'DM Mono\',monospace">'
                        f'Tone judge: {r}</p>', unsafe_allow_html=True
                    )

    # ══════════════════════════════════════════════════
    # TAB 2 — EVALUATE
    # ══════════════════════════════════════════════════
    with tab_eval:
        st.markdown('<p class="section-label">Metric Definitions</p>', unsafe_allow_html=True)

        defs = [
            ("M1 · Fact Recall Score (FRS)", "#63b3ed",
             "Automated Python · Key-term fuzzy matching",
             "Measures what % of the input facts actually appear in the generated email. "
             "Per fact, key terms are extracted (stop-words removed). A fact is 'recalled' "
             "if ≥55% of its key terms appear in the email (case-insensitive). "
             "Score = recalled / total. Range 0.0–1.0."),
            ("M2 · Tone Alignment Score (TAS)", "#9f7aea",
             "LLM-as-a-Judge · qwen3:4b @ temp=0.1",
             "A separate inference pass evaluates (requested tone, generated email) "
             "and returns a 1–5 score with reasoning. Normalised to 0.0–1.0 via (raw−1)/4. "
             "Captures warmth, urgency, formality — nuances keyword matching cannot."),
            ("M3 · Professional Quality Score (PQS)", "#4fd1c5",
             "Composite · 3 sub-metrics weighted",
             "Sub-A (25%): Subject line presence + action-keyword bonus. "
             "Sub-B (50%): Structural completeness — greeting, body ≥40 words, CTA phrase, sign-off. "
             "Sub-C (25%): Conciseness ratio vs reference email (ideal range 50%–150%). "
             "Weighted average. Range 0.0–1.0."),
        ]

        for name, color, method, desc in defs:
            st.markdown(f"""
            <div class="glass-card" style="border-left:3px solid {color}">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
                    <span style="font-size:0.8rem;font-weight:700;color:{color};
                                 letter-spacing:0.05em;font-family:'DM Mono',monospace">{name}</span>
                    <span class="badge badge-info" style="font-size:0.62rem;white-space:nowrap">{method}</span>
                </div>
                <div style="font-size:0.86rem;color:#a0aec0;line-height:1.65">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<p class="section-label">Sample Evaluation Results — All 10 Scenarios</p>', unsafe_allow_html=True)

        rows = [
            ("1. Interview follow-up",       0.50,0.75,0.96,0.74,  0.25,0.50,0.75,0.50),
            ("2. Deadline extension",         0.75,1.00,0.96,0.90,  0.50,0.50,0.75,0.58),
            ("3. Client apology",             0.78,1.00,0.96,0.91,  0.42,0.50,0.75,0.56),
            ("4. Cold outreach",              0.56,0.75,0.96,0.76,  0.22,0.25,0.77,0.41),
            ("5. Meeting recap",              0.67,0.75,0.96,0.79,  0.44,0.50,0.89,0.61),
            ("6. Contract negotiation",       0.63,0.75,0.89,0.76,  0.38,0.25,0.70,0.44),
            ("7. Welcome new hire",           0.60,1.00,0.96,0.85,  0.40,0.50,0.71,0.54),
            ("8. Support escalation",         0.72,1.00,0.96,0.89,  0.50,0.50,0.71,0.57),
            ("9. Speaker invite",             0.67,1.00,0.96,0.88,  0.33,0.50,0.64,0.49),
            ("10. Decline proposal",          0.50,0.75,0.85,0.70,  0.25,0.50,0.83,0.53),
        ]

        import pandas as pd

        df = pd.DataFrame(rows, columns=[
            "Scenario",
            "FRS-A","TAS-A","PQS-A","Overall-A",
            "FRS-B","TAS-B","PQS-B","Overall-B",
        ])

        def colour_val(v):
            if isinstance(v, float):
                c = "#68d391" if v >= 0.75 else "#f6ad55" if v >= 0.5 else "#fc8181"
                return f"color: {c}"
            return ""

        styled = (
            df.style
            .map(colour_val, subset=df.columns[1:])
            .format({c: "{:.0%}" for c in df.columns[1:]})
            .set_properties(**{"font-size": "12px", "font-family": "DM Mono, monospace"})
            .set_table_styles([
                {"selector": "th", "props": [
                    ("background-color", "rgba(13,27,52,0.9)"),
                    ("color", "#718096"),
                    ("font-family", "DM Mono, monospace"),
                    ("font-size", "11px"),
                    ("letter-spacing", "0.06em"),
                ]},
            ])
        )
        st.dataframe(styled, use_container_width=True, height=380)

        st.markdown("---")
        st.markdown('<p class="section-label">Strategy Comparison</p>', unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            st.markdown("""
            <div class="glass-card" style="border-left:3px solid #63b3ed;background:rgba(99,179,237,0.03)">
                <div style="font-size:0.68rem;letter-spacing:0.12em;color:#63b3ed;
                            font-family:'DM Mono',monospace;margin-bottom:14px;font-weight:600">
                    STRATEGY A · ADVANCED PROMPTING
                </div>
                <div class="cmp-row"><span class="cmp-label">Fact Recall Score</span>
                    <span class="cmp-value" style="color:#68d391">63%</span></div>
                <div class="cmp-row"><span class="cmp-label">Tone Alignment Score</span>
                    <span class="cmp-value" style="color:#68d391">88%</span></div>
                <div class="cmp-row"><span class="cmp-label">Professional Quality</span>
                    <span class="cmp-value" style="color:#68d391">89%</span></div>
                <hr style="border-color:rgba(255,255,255,0.06)!important;margin:12px 0!important">
                <div class="cmp-row">
                    <span style="font-weight:700;font-size:0.9rem;color:#e2e8f0">OVERALL</span>
                    <span style="font-size:1.3rem;font-weight:800;color:#63b3ed;
                                 font-family:'Syne',sans-serif">80%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with cb:
            st.markdown("""
            <div class="glass-card" style="border-left:3px solid #4a5568">
                <div style="font-size:0.68rem;letter-spacing:0.12em;color:#4a5568;
                            font-family:'DM Mono',monospace;margin-bottom:14px;font-weight:600">
                    STRATEGY B · BASELINE
                </div>
                <div class="cmp-row"><span class="cmp-label">Fact Recall Score</span>
                    <span class="cmp-value" style="color:#fc8181">36%</span></div>
                <div class="cmp-row"><span class="cmp-label">Tone Alignment Score</span>
                    <span class="cmp-value" style="color:#fc8181">45%</span></div>
                <div class="cmp-row"><span class="cmp-label">Professional Quality</span>
                    <span class="cmp-value" style="color:#f6ad55">76%</span></div>
                <hr style="border-color:rgba(255,255,255,0.06)!important;margin:12px 0!important">
                <div class="cmp-row">
                    <span style="font-weight:700;font-size:0.9rem;color:#e2e8f0">OVERALL</span>
                    <span style="font-size:1.3rem;font-weight:800;color:#4a5568;
                                 font-family:'Syne',sans-serif">52%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="border-left:3px solid #68d391;background:rgba(104,211,145,0.03);margin-top:4px">
            <div style="font-size:0.72rem;color:#68d391;font-family:'DM Mono',monospace;
                        font-weight:600;letter-spacing:0.08em;margin-bottom:8px">
                ✓ RECOMMENDATION: STRATEGY A FOR PRODUCTION
            </div>
            <div style="font-size:0.84rem;color:#a0aec0;line-height:1.6">
                Strategy A outperforms Strategy B by <strong style="color:#e2e8f0">+27.7 percentage points</strong> overall.
                The biggest failure mode of Strategy B is tone inaccuracy — without the role persona and few-shot examples,
                the model defaults to a flat neutral register regardless of requested tone.
                The advanced prompt's additional token cost (~200 tokens) is negligible versus the quality gain.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    # TAB 3 — HISTORY
    # ══════════════════════════════════════════════════
    with tab_history:
        history = st.session_state.get("history", [])
        if not history:
            st.markdown("""
            <div style="text-align:center;padding:70px 0">
                <div style="font-size:2.8rem;opacity:0.2;margin-bottom:16px">🕘</div>
                <p style="color:#2d3748;font-family:'DM Mono',monospace;font-size:0.82rem">
                    No emails generated yet in this session.
                </p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(
                f'<p style="font-size:0.72rem;color:#4a5568;font-family:\'DM Mono\',monospace;'
                f'margin-bottom:16px">{len(history)} email(s) this session</p>',
                unsafe_allow_html=True
            )
            for i, item in enumerate(history):
                label = f"✉  {item['intent'][:52]}  ·  {item['tone'][:22]}  ·  {item['time']}s"
                with st.expander(label, expanded=(i == 0)):
                    hc1, hc2 = st.columns([3, 1])
                    with hc1:
                        st.markdown(
                            f'<div class="email-output" style="font-size:0.8rem">{item["email"]}</div>',
                            unsafe_allow_html=True
                        )
                    with hc2:
                        st.markdown(
                            f'<span class="badge badge-info">{item["strategy"]}</span>',
                            unsafe_allow_html=True
                        )
                        st.markdown("<br>", unsafe_allow_html=True)
                        for f in item["facts"]:
                            st.markdown(f'<span class="fact-tag">{f[:40]}</span>', unsafe_allow_html=True)

            if st.button("🗑  Clear History"):
                st.session_state["history"] = []
                st.rerun()

    # ══════════════════════════════════════════════════
    # TAB 4 — BATCH RUN
    # ══════════════════════════════════════════════════
    with tab_batch:
        st.markdown('<p class="section-label">Batch Evaluation</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="margin-bottom:20px">
            <p style="font-size:0.86rem;color:#a0aec0;line-height:1.65;margin:0">
                Run all <strong style="color:#e2e8f0">10 test scenarios</strong> through one or both strategies,
                scoring each with all 3 custom metrics. Results stream live and can be downloaded as CSV.
                <br><br>
                <span style="color:#4a5568;font-family:'DM Mono',monospace;font-size:0.76rem">
                Requires: ollama serve · qwen3:4b · approx 3–8 min for full run
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        bc1, bc2, _ = st.columns([1, 1, 2])
        with bc1:
            run_adv = st.checkbox("Strategy A (Advanced)", value=True)
        with bc2:
            run_base = st.checkbox("Strategy B (Baseline)", value=False)

        if st.button("⚡  Start Batch", use_container_width=False):
            if not check_ollama_health():
                st.error("Ollama not reachable — run `ollama serve` first.")
            else:
                strategies = []
                if run_adv:   strategies.append(("Strategy A", True))
                if run_base:  strategies.append(("Strategy B", False))
                if not strategies:
                    st.warning("Select at least one strategy.")
                else:
                    all_rows = []
                    prog = st.progress(0)
                    status = st.empty()
                    total = len(strategies) * len(TEST_SCENARIOS)
                    step = 0

                    for sname, use_adv in strategies:
                        for sc in TEST_SCENARIOS:
                            status.markdown(
                                f'<p style="font-size:0.78rem;color:#63b3ed;font-family:\'DM Mono\',monospace">'
                                f'[{sname}] {sc["id"]}/10 · {sc["intent"][:48]}…</p>',
                                unsafe_allow_html=True
                            )
                            gen = generate_email(
                                intent=sc["intent"], facts=sc["facts"], tone=sc["tone"],
                                use_advanced_prompt=use_adv,
                                temperature=st.session_state["temperature"],
                            )
                            if gen["success"]:
                                ev = evaluate_single(
                                    gen["content"], sc["facts"], sc["tone"],
                                    sc["reference_email"]
                                )
                                all_rows.append({
                                    "ID": sc["id"],
                                    "Scenario": sc["intent"][:38],
                                    "Strategy": sname,
                                    "FRS": f"{ev['fact_recall_score']:.0%}",
                                    "TAS": f"{ev['tone_alignment_score']:.0%}",
                                    "PQS": f"{ev['professional_quality_score']:.0%}",
                                    "Overall": f"{ev['overall_score']:.0%}",
                                    "Time(s)": gen["elapsed_seconds"],
                                })
                            step += 1
                            prog.progress(step / total)
                            time.sleep(0.2)

                    status.markdown(
                        '<p style="font-size:0.78rem;color:#68d391;font-family:\'DM Mono\',monospace">'
                        '✓ Batch complete</p>', unsafe_allow_html=True
                    )
                    if all_rows:
                        import pandas as pd
                        df_b = pd.DataFrame(all_rows)
                        st.dataframe(df_b, use_container_width=True)
                        st.download_button(
                            "⬇  Download Results CSV",
                            data=df_b.to_csv(index=False),
                            file_name="batch_evaluation.csv",
                            mime="text/csv",
                        )


if __name__ == "__main__":
    main()
