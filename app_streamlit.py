import os
import streamlit as st
from dotenv import load_dotenv
from core.team import run_contract_team

load_dotenv()

st.set_page_config(page_title="Talent Performer | Agno Contract Expert", layout="wide")

# Header / Branding 
col1, col2 = st.columns([1, 5], vertical_alignment="center")

with col1:
    logo_path = os.path.join("assets", "talentperformer_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
    else:
        # Fallback if no logo file yet
        st.markdown("**Talent Performer**")

with col2:
    st.title("Contract Review Expert")
    st.caption(
        "Upload a contract as a document (PDF/DOCX/TXT), "
        "and get a consolidated analysis (structure, legal risks, negotiation strategy)."
    )

st.divider()

uploaded = st.file_uploader(
    "Upload the contract (Document: PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"],
    help="Tip: upload it as a *file/document*"
)

goal = st.text_area(
    "Your goal (optional)",
    placeholder="e.g., reduce liability, strengthen termination clause, add GDPR/DPA safeguards...",
    height=90,
)

analyze = st.button("Analyze the contract", type="primary", use_container_width=True)

if uploaded and analyze:
    with st.spinner("Analyzing the contract ..."):
        file_bytes = uploaded.read()
        output_md = run_contract_team(
            file_bytes=file_bytes,
            filename=uploaded.name,
            user_goal=goal,
        )

    st.success("Analysis complete.")
    st.markdown(output_md)
elif analyze and not uploaded:
    st.warning("Please upload a contract document!")

