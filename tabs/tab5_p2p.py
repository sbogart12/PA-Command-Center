import streamlit as st

def render():
    st.markdown("### Peer-to-Peer (P2P) Physician Briefing Sheet")
    st.info("Generate a concise 1-page talking points sheet for upcoming physician-to-medical-director calls.")
    if st.button("Build P2P Talking Points"):
        st.markdown("- **Primary Diagnosis:** Lumbar Disc Degeneration\n- **Failed Trials:** Physical therapy (8 weeks), NSAIDs (Meloxicam)\n- **Requested Intervention:** Epidural Steroid Injection\n- **Clinical Justification:** Avoid surgical intervention, preserve functional mobility.")
