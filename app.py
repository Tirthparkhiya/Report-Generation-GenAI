import streamlit as st
import html as html_lib
from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchFlow AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap');
html,body,[class*="css"]{font-family:'DM Mono',monospace;background-color:#0a0a0f;color:#e8e6e0;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:2.5rem 3rem 4rem;max-width:1100px;}
.hero{border:1px solid #2a2a3a;border-radius:2px;padding:2.8rem 3rem 2.2rem;margin-bottom:2.5rem;
  background:linear-gradient(135deg,#0d0d1a 0%,#12121f 60%,#0a0a14 100%);position:relative;overflow:hidden;}
.hero::before{content:"";position:absolute;top:-60px;right:-80px;width:320px;height:320px;
  background:radial-gradient(circle,rgba(99,102,241,.12) 0%,transparent 70%);pointer-events:none;}
.hero-eyebrow{font-size:.72rem;letter-spacing:.22em;color:#6366f1;text-transform:uppercase;margin-bottom:.6rem;}
.hero-title{font-family:'Syne',sans-serif;font-size:2.6rem;font-weight:800;color:#f0ede6;line-height:1.1;margin-bottom:.7rem;}
.hero-title span{color:#6366f1;}
.hero-sub{font-size:.82rem;color:#6b6b80;line-height:1.6;max-width:520px;}
.stTextInput>div>div>input{background:#111120!important;border:1px solid #2a2a3a!important;border-radius:2px!important;
  color:#e8e6e0!important;font-family:'DM Mono',monospace!important;font-size:.9rem!important;padding:.75rem 1rem!important;}
.stTextInput>div>div>input:focus{border-color:#6366f1!important;box-shadow:0 0 0 2px rgba(99,102,241,.15)!important;}
.stTextInput label{font-family:'DM Mono',monospace!important;font-size:.72rem!important;
  letter-spacing:.14em!important;text-transform:uppercase!important;color:#6b6b80!important;}
.stButton>button{background:#6366f1!important;color:#fff!important;border:none!important;border-radius:2px!important;
  font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:.85rem!important;
  letter-spacing:.08em!important;text-transform:uppercase!important;padding:.65rem 2.2rem!important;width:100%!important;}
.stButton>button:hover{background:#4f52d4!important;}
.stage-card{border:1px solid #1e1e2e;border-radius:2px;padding:1.4rem 1.6rem;margin-bottom:1rem;background:#0e0e1c;}
.stage-card.active{border-color:#6366f1;}.stage-card.done{border-color:#22c55e;}.stage-card.waiting{border-color:#1e1e2e;opacity:.5;}
.stage-header{display:flex;align-items:center;gap:.8rem;margin-bottom:.35rem;}
.stage-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.dot-waiting{background:#2a2a3a;}.dot-active{background:#6366f1;animation:pulse 1.2s ease-in-out infinite;}
.dot-done{background:#22c55e;}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.5;transform:scale(1.4);}}
.stage-label{font-family:'Syne',sans-serif;font-weight:700;font-size:.82rem;letter-spacing:.1em;text-transform:uppercase;color:#c4c2bb;}
.stage-desc{font-size:.74rem;color:#4a4a60;margin-left:1.5rem;}
.result-panel{border:1px solid #1e1e2e;border-radius:2px;margin-top:.8rem;overflow:hidden;}
.result-panel-header{background:#111120;padding:.5rem 1.1rem;font-size:.65rem;letter-spacing:.18em;
  text-transform:uppercase;color:#4a4a60;border-bottom:1px solid #1e1e2e;}
.result-panel-body{padding:1rem 1.2rem;font-size:.8rem;line-height:1.75;color:#b0aead;white-space:pre-wrap;
  word-break:break-word;max-height:260px;overflow-y:auto;background:#0a0a0f;}
.report-box{border:1px solid #6366f1;border-radius:2px;background:#0c0c1a;margin-top:2rem;overflow:hidden;}
.report-box-header{background:#6366f1;padding:.75rem 1.4rem;font-family:'Syne',sans-serif;font-weight:700;
  font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:#fff;}
.report-box-body{padding:1.6rem;font-size:.84rem;line-height:1.8;color:#d4d2cb;white-space:pre-wrap;word-break:break-word;}
.feedback-box{border:1px solid #22c55e;border-radius:2px;background:#0a120d;margin-top:1.2rem;overflow:hidden;}
.feedback-box-header{background:#16a34a;padding:.65rem 1.4rem;font-family:'Syne',sans-serif;font-weight:700;
  font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:#fff;}
.feedback-box-body{padding:1.4rem;font-size:.82rem;line-height:1.8;color:#a3d9b0;white-space:pre-wrap;word-break:break-word;}
hr{border-color:#1a1a28!important;margin:2rem 0!important;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:#2a2a3a;border-radius:2px;}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Multi-Agent System</div>
  <div class="hero-title">Research<span>Flow</span> AI</div>
  <div class="hero-sub">Enter any topic. Four autonomous agents — Search · Scrape · Write · Critique —
  collaborate to deliver a structured, fact-checked research report.</div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1.2])
with col_input:
    topic = st.text_input("Research Topic", placeholder="e.g. Quantum computing breakthroughs in 2025")
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run = st.button("▶ Run")

# ── Stage helpers ─────────────────────────────────────────────────────────────
STAGES = [
    ("🔍", "Search Agent",  "Querying the web for recent, reliable sources"),
    ("📄", "Reader Agent",  "Scraping & extracting deep content from top URLs"),
    ("✍️",  "Writer Chain",  "Synthesising research into a structured report"),
    ("🧐", "Critic Chain",  "Reviewing and scoring the generated report"),
]

def safe_str(val) -> str:
    """Coerce any agent/chain output to a plain string.
    Handles: str, list of content blocks, AIMessage, or anything else."""
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        parts = []
        for item in val:
            if isinstance(item, dict):
                parts.append(item.get("text") or item.get("content") or str(item))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if hasattr(val, "content"):
        return safe_str(val.content)
    return str(val)

def render_stage(idx: int, status: str, content: str = ""):
    icon, label, desc = STAGES[idx]
    card_cls = {"waiting":"waiting","active":"active","done":"done"}.get(status,"waiting")
    dot_cls  = {"waiting":"dot-waiting","active":"dot-active","done":"dot-done"}.get(status,"dot-waiting")
    result_html = ""
    if content and status == "done":
        preview = html_lib.escape(content[:1600]) + ("…" if len(content) > 1600 else "")
        result_html = (
            '<div class="result-panel">'
            '<div class="result-panel-header">◆ Output preview</div>'
            f'<div class="result-panel-body">{preview}</div>'
            '</div>'
        )
    st.markdown(
        f'<div class="stage-card {card_cls}">'
        f'  <div class="stage-header"><div class="stage-dot {dot_cls}"></div>'
        f'  <div class="stage-label">{icon} {label}</div></div>'
        f'  <div class="stage-desc">{desc}</div>'
        f'  {result_html}'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Pipeline ──────────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
        st.stop()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-family:DM Mono,monospace;font-size:.72rem;letter-spacing:.18em;"
        f"text-transform:uppercase;color:#6366f1;margin-bottom:1.2rem'>"
        f"Pipeline running for: <span style='color:#e8e6e0'>{html_lib.escape(topic)}</span></div>",
        unsafe_allow_html=True,
    )

    placeholders = [st.empty() for _ in STAGES]
    for i, ph in enumerate(placeholders):
        with ph.container():
            render_stage(i, "waiting")

    state = {}
    error = None

    try:
        # ── 0 Search ─────────────────────────────────────────────────────
        with placeholders[0].container():
            render_stage(0, "active")

        search_agent  = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        # Same extraction as pipeline.py
        state['search_result'] = safe_str(search_result['messages'][-1].content)

        with placeholders[0].container():
            render_stage(0, "done", state['search_result'])

        # ── 1 Reader ─────────────────────────────────────────────────────
        with placeholders[1].container():
            render_stage(1, "active")

        reader_agent  = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_result'][:800]}"
            )]
        })
        state['scraped_content'] = safe_str(reader_result['messages'][-1].content)

        with placeholders[1].container():
            render_stage(1, "done", state['scraped_content'])

        # ── 2 Writer ─────────────────────────────────────────────────────
        with placeholders[2].container():
            render_stage(2, "active")

        research_combined = (
            f"SEARCH RESULT : \n {state['search_result']}\n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        # writer_chain ends with StrOutputParser → plain str
        state['report'] = safe_str(writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        }))

        with placeholders[2].container():
            render_stage(2, "done", state['report'])

        # ── 3 Critic ─────────────────────────────────────────────────────
        with placeholders[3].container():
            render_stage(3, "active")

        state['feedback'] = safe_str(critic_chain.invoke({
            "report": state['report']
        }))

        with placeholders[3].container():
            render_stage(3, "done", state['feedback'])

    except Exception:
        import traceback
        error = traceback.format_exc()

    # ── Output ────────────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)

    if error:
        st.error("Pipeline error — full traceback below:")
        st.code(error, language="python")
    else:
        report_esc   = html_lib.escape(state.get('report', ''))
        feedback_esc = html_lib.escape(state.get('feedback', ''))

        st.markdown(
            f'<div class="report-box">'
            f'<div class="report-box-header">📋 Final Research Report</div>'
            f'<div class="report-box-body">{report_esc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="feedback-box">'
            f'<div class="feedback-box-header">🧐 Critic Feedback</div>'
            f'<div class="feedback-box-body">{feedback_esc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        full_output = (
            f"TOPIC: {topic}\n\n"
            f"{'='*60}\nFINAL REPORT\n{'='*60}\n{state.get('report','')}\n\n"
            f"{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n{state.get('feedback','')}"
        )
        st.download_button(
            label="⬇  Download Full Report (.pdf)",
            data=full_output,
            file_name=f"research_{topic[:40].replace(' ','_')}.pdf",
            mime="text/plain",
        )
