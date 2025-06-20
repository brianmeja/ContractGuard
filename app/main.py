import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import tempfile
from app.file_utils import extract_text, SUPPORTED_EXTENSIONS
from app.analyzer import analyze_contract

# --- Custom CSS for premium mobile experience ---
st.markdown(
    """
    <style>
    html, body, .main { background-color: #f7f7f9; }
    .st-bb { background: #fff !important; border-radius: 10px; }
    .risk-badge { display: inline-block; padding: 0.2em 0.7em; border-radius: 1em; font-size: 0.95em; font-weight: 600; }
    .risk-High { background: #ff4b4b; color: #fff; }
    .risk-Medium { background: #ffb300; color: #fff; }
    .risk-Low { background: #00b86b; color: #fff; }
    .risk-None { background: #bdbdbd; color: #fff; }
    /* Responsive font and padding */
    @media (max-width: 600px) {
        .stApp { font-size: 1.08em; }
        .stButton>button, .stFileUploader>div { font-size: 1.1em; padding: 0.8em 1.2em; }
        .risk-badge { font-size: 1.1em; }
        .st-expanderHeader { font-size: 1.08em; }
        .footer-emblem { font-size: 1em !important; }
    }
    /* Floating Action Button (FAB) */
    .fab-upload {
        position: fixed;
        bottom: 80px;
        right: 24px;
        z-index: 100;
        background: #00b86b;
        color: #fff;
        border-radius: 50%;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        font-size: 2em;
        cursor: pointer;
        transition: background 0.2s;
    }
    .fab-upload:hover { background: #009e5c; }
    /* Scroll to top button */
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
        transition: background 0.2s;
    }
    .scroll-top-btn:hover { background: #ff9800; }
    </style>
    <script>
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

# --- Floating Action Button for Upload (simulated) ---
st.markdown("""
<div class='fab-upload' onclick="document.querySelector('input[type=file]').click()" title='Upload contract'>
    <span>+</span>
</div>
""", unsafe_allow_html=True)

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
        # --- Clause-by-Clause Breakdown ---
        st.markdown("---")
        for idx, r in enumerate(results):
            if risk_filter != "All" and r["risk"] != risk_filter:
                continue
            badge = f"<span class='risk-badge risk-{r['risk']}'> {r['risk']} </span>"
            with st.expander(f"Clause {idx+1}"):
                st.markdown(f"{badge} &nbsp; {r['clause']}", unsafe_allow_html=True)
                if r["risk"] != "None":
                    st.caption(f"Flagged keyword: {r['keyword']}")

# --- Company Emblem/Footer ---
st.markdown("""
---
<div class='footer-emblem' style='text-align: center; margin-top: 2em;'>
    <img src='https://img.icons8.com/ios-filled/50/000000/briefcase.png' width='32' style='vertical-align:middle; margin-right:8px;'>
    <span style='font-size: 1.1em; color: #888;'>©2025 Meja Tech Solutions</span>
</div>
""", unsafe_allow_html=True) 