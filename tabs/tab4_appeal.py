import streamlit as st

def render():
    st.markdown("### Automated Appeal & Letter of Necessity Generator")
    pat_name = st.text_input("Patient Name", "John Smith")
    denial_reason = st.text_input("Payer Denial Reason", "Lack of documented conservative therapy failure")
    if st.button("Generate Appeal Letter"):
        st.code(f"""DEAR MEDICAL DIRECTOR,

Please accept this formal appeal for {pat_name} regarding prior authorization denial... Reason cited: {denial_reason}. Clinical records confirm full adherence.

Sincerely,
Clinical Care Team""")
