import streamlit as st
from datetime import datetime

def render():
    st.subheader("📝 New Patient Prior Authorization Intake")
    st.markdown("Register a new patient and initiate a prior authorization tracking record.")

    with st.form("patient_intake_form"):
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Patient Full Name", placeholder="e.g., Jane Doe")
            dob = st.date_input("Date of Birth")
            payer = st.selectbox("Insurance Payer", ["Aetna", "Blue Cross Blue Shield", "Cigna", "UnitedHealthcare", "Humana", "Medicare Part D"])
        
        with col2:
            treatment = st.text_input("Treatment / Medication", placeholder="e.g., Humira 40mg Injection")
            priority = st.selectbox("Priority Level", ["Routine", "Urgent / Expedited"])
            submitting_provider = st.text_input("Submitting Provider", placeholder="e.g., Dr. Robert Thorne")

        clinical_notes = st.text_area("Initial Clinical Summary / Notes", placeholder="Paste initial clinical justification or symptoms here...")
        
        submitted = st.form_submit_button("🚀 Submit & Create PA Case")
        
        if submitted:
            if patient_name and treatment:
                case_id = f"PA-{datetime.now().strftime('%H%M%S')}"
                st.success(f"Successfully created case **{case_id}** for **{patient_name}** ({payer})!")
                st.info(f"**Treatment:** {treatment} | **Priority:** {priority}")
            else:
                st.warning("Please fill in at least the Patient Full Name and Treatment fields.")
