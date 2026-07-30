import os
import streamlit as st
from datetime import datetime
from  langchain_core.messages import HumanMessage
from langgraph_backend import travel_app
from datetime import datetime, timedelta

#---------------------------------PAGE-------------------------------------
st.set_page_config( 
    page_title="AI JOURNEY BUDDY", 
    page_icon="✈️",  
    layout="wide" 
) 
#---------------------------------CSS-----------------------------------------
st.markdown("""
<style>
@import url('https://googleapis.com');
html, body, .stApp { font-family: 'Inter', sans-serif; background-color: #060b07; }

/* ── Hero ── */
.hero-wrapper { position: relative; border-radius: 20px; overflow: hidden; margin-bottom: 2rem; height: 280px; }
.hero-bg { width: 100%; height: 100%; object-fit: cover; display: block; filter: brightness(0.35); position: absolute; top: 0; left: 0; }
.hero-content { position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 2rem; }
.hero-badge { background: rgba(107, 142, 35, 0.2); border: 1px solid rgba(128, 168, 46, 0.4); color: #a3d977 !important; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.3rem 0.9rem; border-radius: 20px; margin-bottom: 0.9rem; display: inline-block; }
.hero-title { font-size: 2.6rem; font-weight: 700; color: #ffffff; margin: 0 0 0.6rem; line-height: 1.2; }
.hero-sub { color: #a4bfa3; font-size: 1rem; max-width: 560px; }

/* ── Input card ── */
.input-card { background: #0c140d; border: 1px solid #1a2b1d; border-radius: 16px; padding: 1.6rem 1.8rem; margin-bottom: 1.5rem; }
.input-label { color: #8cb86b; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; }

/* ── Quick destinations ── */
.dest-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.8rem 0 1.2rem; }
.dest-chip { background: #0f1a10; border: 1px solid #1b301d; color: #f4fdf5; padding: 0.35rem 0.85rem; border-radius: 20px; font-size: 0.82rem; cursor: pointer; transition: all 0.2s; }
.dest-chip:hover { background: #1a2e1d; border-color: #556b2f; color: #fff; }

/* ── Generate button ── */
div[data-testid="stButton"] > button { background: linear-gradient(135deg, #556b2f 0%, #3a4d1d 50%, #253313 100%) !important; color: #ffffff !important; border: none !important; border-radius: 12px !important; padding: 0.85rem 2.5rem !important; font-size: 1.05rem !important; font-weight: 700 !important; letter-spacing: 0.03em !important; width: 100% !important; box-shadow: 0 0 24px rgba(85, 107, 47, 0.35), 0 4px 15px rgba(0,0,0,0.4) !important; transition: all 0.3s ease !important; }
div[data-testid="stButton"] > button:hover { box-shadow: 0 0 40px rgba(107, 142, 35, 0.5), 0 6px 20px rgba(0,0,0,0.5) !important; transform: translateY(-2px) !important; background: linear-gradient(135deg, #6b8e23 0%, #465c22 50%, #3a4d1d 100%) !important; }
div[data-testid="stButton"] > button:active { transform: translateY(0px) !important; }

/* ── Agent status cards ── */
[data-testid="stStatusWidget"] { background: #0c140d !important; border: 1px solid #1a2b1d !important; border-radius: 12px !important; }
[data-testid="stStatusWidget"] > div:first-child { background: #0c140d !important; border-radius: 12px 12px 0 0 !important; }
[data-testid="stStatusWidget"] details, [data-testid="stStatusWidget"] details > div, [data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] { background: #080d08 !important; color: #ffffff !important; padding: 0.25rem 0.5rem !important; }
[data-testid="stStatusWidget"] * { color: #ffffff !important; }
[data-testid="stStatusWidget"] a { color: #a3d977 !important; }
[data-testid="stStatusWidget"] hr { border-color: #1a2b1d !important; }

/* ── Section headers ── */
.sec-head { display: flex; align-items: center; gap: 0.6rem; margin: 2rem 0 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #1a2b1d; }
.sec-head span { font-size: 1.15rem; font-weight: 600; color: #e2ede0; }

/* ── Metric bar ── */
.metric-row { display: flex; gap: 1rem; margin: 1.5rem 0; }
.metric-box { flex: 1; background: #0c140d; border: 1px solid #1a2b1d; border-radius: 12px; padding: 1rem 1.2rem; text-align: center; }
.metric-val { font-size: 1.8rem; font-weight: 700; color: #8cb86b; }
.metric-lbl { font-size: 0.78rem; color: #6a8568; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Final plan ── */
.final-card { background: linear-gradient(160deg, #09120a 0%, #060b07 100%); border: 1px solid #1f3322; border-left: 4px solid #556b2f; border-radius: 14px; padding: 1.8rem; line-height: 1.8; color: #cedecd; font-size: 0.95rem; }

/* ── Save bar ── */
.save-bar { background: #0c140d; border: 1px solid #1a2b1d; border-radius: 10px; padding: 0.85rem 1.2rem; color: #6e8a6c; font-size: 0.88rem; margin-top: 0.5rem; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: #070c08 !important; border-right: 1px solid #111c13 !important; }
.sidebar-chip { background: #132015; border: 1px solid #1e3322; border-radius: 8px; padding: 0.45rem 0.75rem; margin-bottom: 0.4rem; font-size: 0.83rem; color: #a9cfa7; display: block; }
.sidebar-title { color: #e2ede0; font-size: 1rem; font-weight: 600; margin: 1rem 0 0.5rem; }
.duration-badge { font-size: 0.85rem; color: #8cb86b; font-weight: 500; margin-top: -0.2rem; margin-bottom: 0.8rem; }

/* Branding */
#MainMenu, footer, [data-testid="stDecoration"] { visibility: hidden; }

/* Interactive form field dark green overrides */
.stTextArea textarea { background: #080d08 !important; border: 1px solid #1a2b1d !important; border-radius: 10px !important; color: #eff5ef !important; font-size: 0.95rem !important; resize: none !important; }
.stTextArea textarea:focus { border-color: #556b2f !important; box-shadow: 0 0 0 2px rgba(85,107,47,0.2) !important; }
.stTextArea textarea::placeholder { color: #4b6649 !important; }

/* Text & Date input design */
input[type="text"], .stTextInput input, div[data-testid="stDateInput"] button { background: #0c140d !important; border: 1px solid #1a2b1d !important; border-radius: 8px !important; color: #e2ede0 !important; width: 100%; text-align: left; }
input[type="text"]:focus, .stTextInput input:focus { border-color: #556b2f !important; box-shadow: 0 0 0 2px rgba(85,107,47,0.2) !important; }

/* Datepicker specific styles */
div[data-testid="stDateInput"] div { color: #e2ede0 !important; }

/* Labels */
.stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label, div[data-testid="stDateInput"] label { color: #8cb86b !important; font-size: 0.82rem !important; font-weight: 600 !important; letter-spacing: 0.08em !important; }

/* Markdown rules */
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { color: #cedecd !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #eff5ef !important; }
.stMarkdown code { background: #0c140d !important; color: #8cb86b !important; padding: 0.15em 0.4em; border-radius: 4px; }
.metric-lbl { color: #6a8568 !important; }
.save-bar { color: #7da17a !important; }
.save-bar code { color: #8cb86b !important; background: #080d08 !important; }

/* Alerts */
.stAlert { background: #0c140d !important; border-radius: 10px !important; }
.stAlert p, .stAlert div { color: #e2ede0 !important; }

/* Sidebar contents override */
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] .stMarkdown { color: #9bbfa2 !important; }
section[data-testid="stSidebar"] hr { border-color: #1a2b1d !important; }
div[data-testid="stDownloadButton"] > button { background: #1c3320 !important; color: #eff5ef !important; border: 1px solid #2d4f33 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Content Layout ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🌍 AI Travel Planner</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    thread_id = st.text_input(
        "👤 User ID", 
        value="Naz", 
        help="Your session ID — keeps travel history across queries"
    )
    
    st.markdown("<div class='sidebar-title'>📅 Travel Dates</div>", unsafe_allow_html=True)
    
    # Date Pickers
    today = datetime.now().date()
    from_date = st.date_input("🛫 From", value=today, min_value=today)
    to_date = st.date_input("🛬 To ", value=today + timedelta(days=5), min_value=from_date)
    
    # Calculate and show duration
    if from_date and to_date:
        duration = (to_date - from_date).days
        st.markdown(f"<div class='duration-badge'>⏱️ Total Duration: <b>{duration} Days</b></div>", unsafe_allow_html=True)
        
        
    st.markdown("<div class='sidebar-title'>Agent Pipeline</div>", unsafe_allow_html=True)
    
    pipeline_steps = ["① Flight Agent", "② Hotel Agent", "③ Itinerary Agent", "④ Final Agent"]
    for step in pipeline_steps:
        st.markdown(f"<div class='sidebar-chip'>{step}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='sidebar-title'>Tech Stack</div>", unsafe_allow_html=True)
    
    tech_stack = ["🔗 LangGraph", "🧠 Groq · LLaMA 3.3 70B", "🐘 PostgreSQL", "🔍 Tavily Search", "✈️ AviationStack"]
    for tech in tech_stack:
        st.markdown(f"<div class='sidebar-chip'>{tech}</div>", unsafe_allow_html=True)

        
# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <img class="hero-bg"
        src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1600&q=80"
        alt="airplane above clouds"/>
    <div class="hero-content">
        <div class="hero-badge">✦ Multi-Agent AI System</div>
        <div class="hero-title">✈ WELCOME TO AI JOURNEY BUDDY </br><span class="brand-sub">PLAN SMARTER</span></div>
        <div class="hero-badge">Discover Your Next Adventure with AI JourneyBuddy</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)

#Initialize the session state variable for the input text area
if "user_query_input" not in st.session_state:
    st.session_state.user_query_input = ""

QUICK = ["7-day Japan under ₹2L", "Paris trip for 5 days", "Dubai weekend trip", "Bali backpacking 10 days"]
qcols = st.columns(len(QUICK))
quick_fill = ""
for qc, label in zip(qcols, QUICK):
    with qc:
        if st.button(label, key=f"q_{label}"):
            quick_fill = label 
            st.session_state.user_query_input = label
            st.rerun()  # Forces immediate rerun to display the text instantly
            
user_query = st.text_area(
    "",
    key="user_query_input",  # This handles the value tracking automatically
    value=quick_fill,
    placeholder="e.g. Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs",
    height=100,
    label_visibility="collapsed",
)

generate = st.button("🛫 Generate My Travel Plan", use_container_width=True)

            
# ── Agent pipeline ────────────────────────────────────────────────────────────
AGENT_META = {
    "flight_agent":    ("✈️", "Flight Agent"),
    "hotel_agent":     ("🏨", "Hotel Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
    "final_agent":     ("🧠", "Final Plan Agent"),
}

if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        config = {"configurable": {"thread_id": thread_id}}
        collected = {"flight_results": "", "hotel_results": "",
                    "itinerary": "", "final_response": ""}

        st.markdown("---")
        st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline — Live</span></div>",
                    unsafe_allow_html=True)

        for chunk in travel_app.stream(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": ""
            },
            config= {"configurable": {"thread_id": thread_id}},
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))

                with st.status(f"{icon}  {label}", state="complete", expanded=True):
                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No flight data returned._")

                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data returned._")

                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")

                    elif node_name == "travel_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text or "_No final response._")


        # Metrics
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Agents Run</div></div>
            <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Status</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Final plan card
        if collected["final_response"]:
            st.markdown("<div class='sec-head'><span>🧠 Final Travel Plan</span></div>",
                        unsafe_allow_html=True)
            st.markdown(f"<div class='final-card'>{collected['final_response']}</div>",
                        unsafe_allow_html=True)

        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan
**Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User ID:** {thread_id}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## 🗓️ Itinerary
{collected['itinerary'] or 'N/A'}

---

## 🧠 Final Travel Plan
{collected['final_response'] or 'N/A'}

---
*FIND YOUR FINAL PLAN BELOW*
"""
        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button("Download Itinerary Plan Here ⬇️", data=file_content,
                            file_name=filename, mime="text/markdown",use_container_width=True)
        with info_col:
            st.markdown(f"<div class='save-bar'>📁 Auto-saved → <code>travel_plans/{filename}</code></div>",
                        unsafe_allow_html=True)
            
#── Destination image strip ───────────────────────────────────────────────────
DESTINATIONS = [
    ("🇯🇵 Tokyo",     "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇫🇷 Paris",     "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),
    ("🇹🇭 Bangkok",   "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),
    ("🇮🇹 Rome",      "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70"),
    ("🇦🇪 Dubai",     "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]

cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(f"""
        <div style="border-radius:10px;overflow:hidden;position:relative;height:90px;cursor:pointer;">
            <img src="{img_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.55);" />
            <div style="position:absolute;bottom:8px;left:0;right:0;text-align:center;
                        color:#fff;font-size:0.8rem;font-weight:600;">{name}</div>
        </div>
        """, unsafe_allow_html=True)