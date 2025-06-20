import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import tempfile
from app.file_utils import extract_text, SUPPORTED_EXTENSIONS
from app.analyzer import analyze_contract

# --- Advanced Custom CSS for flawless mobile responsiveness ---
st.markdown(
    """
    <style>
    html, body, .main { background-color: #f7f7f9; }
    .st-bb { background: #fff !important; border-radius: 12px; }
    .risk-badge { display: inline-block; padding: 0.3em 0.9em; border-radius: 1.2em; font-size: 1em; font-weight: 600; box-shadow: 0 1px 4px rgba(0,0,0,0.06); transition: box-shadow 0.2s; }
    .risk-High { background: #ff4b4b; color: #fff; }
    .risk-Medium { background: #ffb300; color: #fff; }
    .risk-Low { background: #00b86b; color: #fff; }
    .risk-None { background: #bdbdbd; color: #fff; }
    .st-expanderHeader { font-size: 1.08em; }
    .stButton>button, .stFileUploader>div { font-size: 1.1em; padding: 0.9em 1.3em; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); transition: box-shadow 0.2s; }
    .stButton>button:hover, .stFileUploader>div:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.13); }
    .st-expander { border-radius: 12px !important; box-shadow: 0 1px 4px rgba(0,0,0,0.07); margin-bottom: 1em; }
    .st-expanderHeader { padding: 0.7em 0.5em; }
    .footer-emblem { font-size: 1em !important; }
    @media (max-width: 900px) {
        .stApp { font-size: 1.08em; }
        .stButton>button, .stFileUploader>div { font-size: 1.13em; padding: 1em 1.4em; }
        .risk-badge { font-size: 1.13em; }
        .st-expanderHeader { font-size: 1.13em; }
        .footer-emblem { font-size: 1.08em !important; }
    }
    @media (max-width: 600px) {
        .stApp { font-size: 1.18em; }
        .stButton>button, .stFileUploader>div { font-size: 1.18em; padding: 1.1em 1.5em; }
        .risk-badge { font-size: 1.18em; }
        .st-expanderHeader { font-size: 1.18em; }
        .footer-emblem { font-size: 1.13em !important; }
    }
    @media (max-width: 900px) {
        .stColumns { flex-direction: column !important; }
    }
    .scroll-top-btn {
        position: fixed;
        bottom: 20px;
        right: 24px;
        z-index: 100;
        background: #ffb300;
        color: #fff;
        border-radius: 50%;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5em;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transition: background 0.2s, box-shadow 0.2s;
    }
    .scroll-top-btn:active { background: #ff9800; }
    .scroll-top-btn:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.18); }
    </style>
    <!-- PWA Manifest -->
    <link rel="manifest" href="/manifest.json">
    <!-- Swipe Gesture & Notification JS -->
    <script>
    // PWA: Register service worker if available
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').catch(function(err){});
      });
    }
    // Swipe gesture detection
    let touchstartX = 0;
    let touchendX = 0;
    function handleGesture() {
      if (touchendX < touchstartX - 50) {
        window.dispatchEvent(new CustomEvent('swipeleft'));
      }
      if (touchendX > touchstartX + 50) {
        window.dispatchEvent(new CustomEvent('swiperight'));
      }
    }
    document.addEventListener('touchstart', function(e) {
      touchstartX = e.changedTouches[0].screenX;
    }, false);
    document.addEventListener('touchend', function(e) {
      touchendX = e.changedTouches[0].screenX;
      handleGesture();
    }, false);
    // Notification permission and sample notification
    if ('Notification' in window) {
      if (Notification.permission === 'default') {
        Notification.requestPermission();
      }
      if (Notification.permission === 'granted') {
        setTimeout(function() {
          new Notification('Welcome to ContractGuard!', { body: 'Your contract risk analysis is ready.' });
        }, 1200);
      }
    }
    // Scroll to top function for the button
    function scrollToTop() { window.scrollTo({top: 0, behavior: 'smooth'}); }
    </script>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/ios-filled/100/contract.png", width=60)
st.sidebar.title("ContractGuard")
st.sidebar.markdown("""
Minimalist AI Contract Clause Risk Analyzer

Upload a contract to instantly see risky clauses, color-coded by severity.
""")
st.sidebar.markdown("---")
st.sidebar.header("Help")
st.sidebar.info("Supported formats: PDF, DOCX, TXT. For best results, upload clear, text-based documents.")

# --- Main UI ---
st.title(":scroll: Contract Clause Risk Analyzer")
st.markdown("<br>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload contract(s)",
    type=[ext[1:] for ext in SUPPORTED_EXTENSIONS],
    accept_multiple_files=True,
    help="Drag and drop or tap to select files. Max 10MB each."
)

# --- Scroll to Top Button ---
st.markdown("""
<div class='scroll-top-btn' onclick='scrollToTop()' title='Scroll to top'>
    <span>&uarr;</span>
</div>
""", unsafe_allow_html=True)

# --- Swipe Gesture Navigation State ---
if 'clause_index' not in st.session_state:
    st.session_state['clause_index'] = 0

# --- Clause Navigation with Swipe Gestures ---
def on_swipe(direction, num_clauses):
    if direction == 'left' and st.session_state['clause_index'] < num_clauses - 1:
        st.session_state['clause_index'] += 1
    elif direction == 'right' and st.session_state['clause_index'] > 0:
        st.session_state['clause_index'] -= 1

# --- JavaScript to listen for swipe events and update Streamlit state ---
st.markdown('''
<script>
window.addEventListener('swipeleft', function() {
    window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', key: 'swipe', value: 'left'}, '*');
});
window.addEventListener('swiperight', function() {
    window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', key: 'swipe', value: 'right'}, '*');
});
</script>
''', unsafe_allow_html=True)

# --- Streamlit component to receive swipe events ---
_swipe = st.query_params.get('swipe', [None])[0]

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown(f"#### <span style='font-size:1.1em'><img src='https://img.icons8.com/ios-filled/24/000000/document.png' style='vertical-align:middle;margin-right:6px;'/> {uploaded_file.name}</span>", unsafe_allow_html=True)
        with st.spinner("Extracting text..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            try:
                text, filetype = extract_text(tmp_path)
            except Exception as e:
                st.error(f"Failed to extract text: {e}")
                os.unlink(tmp_path)
                continue
            os.unlink(tmp_path)
        if not text.strip():
            st.warning("No text found in document.")
            continue
        with st.spinner("Analyzing clauses..."):
            results = analyze_contract(text)
        # --- Risk Overview as Metrics ---
        risk_counts = {"High": 0, "Medium": 0, "Low": 0, "None": 0}
        for r in results:
            risk_counts[r["risk"]] += 1
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("High Risk", risk_counts["High"], delta=None, help="Potentially harmful or one-sided clauses.")
        col2.metric("Medium Risk", risk_counts["Medium"], delta=None, help="Clauses requiring careful consideration.")
        col3.metric("Low Risk", risk_counts["Low"], delta=None, help="Standard, balanced clauses.")
        col4.metric("Unflagged", risk_counts["None"], delta=None, help="Clauses with no detected risk.")
        st.markdown("<br>", unsafe_allow_html=True)
        # --- Filter Clauses by Risk ---
        risk_filter = st.selectbox(
            "Show clauses with risk level:",
            ["All", "High", "Medium", "Low", "None"],
            index=0,
            help="Filter clauses by risk severity."
        )
        # --- Clause-by-Clause Breakdown with Swipe Navigation ---
        st.markdown("---")
        filtered_results = [r for r in results if risk_filter == "All" or r["risk"] == risk_filter]
        num_clauses = len(filtered_results)
        if num_clauses > 0:
            # Handle swipe navigation
            if _swipe:
                on_swipe(_swipe, num_clauses)
            idx = st.session_state['clause_index']
            idx = max(0, min(idx, num_clauses - 1))
            badge = f"<span class='risk-badge risk-{filtered_results[idx]['risk']}'> {filtered_results[idx]['risk']} </span>"
            with st.expander(f"Clause {idx+1} of {num_clauses}", expanded=True):
                st.markdown(f"{badge} &nbsp; {filtered_results[idx]['clause']}", unsafe_allow_html=True)
                if filtered_results[idx]["risk"] != "None":
                    st.caption(f"Flagged keyword: {filtered_results[idx]['keyword']}")
            # Navigation buttons for accessibility
            nav_cols = st.columns([1, 6, 1])
            with nav_cols[0]:
                if st.button("⬅️", key="prev_clause", disabled=idx==0):
                    on_swipe('right', num_clauses)
            with nav_cols[2]:
                if st.button("➡️", key="next_clause", disabled=idx==num_clauses-1):
                    on_swipe('left', num_clauses)
        else:
            st.info("No clauses found for the selected risk level.")

# --- Company Emblem/Footer ---
st.markdown("""
---
<div class='footer-emblem' style='text-align: center; margin-top: 2em;'>
    <img src='https://img.icons8.com/ios-filled/50/000000/briefcase.png' width='32' style='vertical-align:middle; margin-right:8px;'>
    <span style='font-size: 1.1em; color: #888;'>©2025 Meja Tech Solutions</span>
</div>
""", unsafe_allow_html=True) 