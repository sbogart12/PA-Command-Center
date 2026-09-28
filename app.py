import streamlit as st
import pandas as pd
import json
import random
import time
from datetime import datetime, date

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM HEALTHCARE STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Payer Prior Auth Command Center",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, high-density clinical dashboard aesthetics
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }
    /* Main container padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 96%;
    }
    /* JSON code block enhancement */
    pre {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION & MOCK CLINICAL DATA
# -----------------------------------------------------------------------------
SAMPLE_NOTES = {
    "Crohn's Disease (Humira)": """PATIENT CLINICAL SUMMARY & PROGRESS NOTE
Date of Visit: 2026-09-15
Patient: Johnathan Miller | DOB: 1988-04-12 | MRN: #89210-CR

SUBJECTIVE:
38-year-old male with confirmed moderate-to-severe Crohn's disease of the terminal ileum (diagnosed 2023). 
Reports persistent abdominal cramping in RLQ, 5-6 loose stools daily, and unintended 12 lb weight loss over the past 4 months. 
Fatigue is severe (CDAI score 340).

HISTORY OF PRIOR FAILED THERAPIES (STEP THERAPY):
1. Mesalamine (Asacol HD 4.8g daily): Prescribed June 2023 - Nov 2023 (6 months). Failed due to refractory symptoms and persistent active inflammation.
2. Azathioprine (Imuran 150mg daily): Prescribed Dec 2023 - April 2024. Discontinued due to elevated hepatic transaminases (ALT 145 U/L) indicating hepatotoxicity.
3. Budesonide 9mg daily: Prescribed for flare control May 2024 - Aug 2024 with transient relief; symptoms recurred immediately upon tapering.

OBJECTIVE FINDINGS:
- Colonoscopy (July 2026): Deep serpiginous ulcerations in the neoterminal ileum; SES-CD score 14.
- Fecal Calprotectin: 840 ug/g (Markedly elevated, ref < 50 ug/g).
- CRP: 28.4 mg/L.
- TB QuantiFERON Gold: Negative (2026-08-20).
- Hepatitis B Surface Antigen/Antibody: Negative.

ASSESSMENT & PLAN:
Primary Diagnosis: K50.00 - Crohn's disease of small intestine without complications.
Prescription Requested: Humira (adalimumab) 40 mg/0.8 mL subcutaneous auto-injector.
Induction Dosing: 160 mg at Week 0 (Day 1), 80 mg at Week 2 (Day 15), followed by 40 mg every other week maintenance.
Medical Necessity: Patient has failed conventional first-line aminosalicylates and has documented contraindication/intolerance to thiopurines. Meets Aetna CPB 0315 biologic initiation criteria.""",

    "Severe Asthma (Dupixent)": """CLINICAL NOTE - PULMONOLOGY CONSULT
Date of Evaluation: 2026-08-28
Patient: Maria E. Vasquez | DOB: 1979-11-23 | MRN: #55412-AS

CHIEF COMPLAINT: Uncontrolled persistent severe asthma with eosinophilic phenotype.

HISTORY OF PRESENT ILLNESS:
46-year-old female presents for biologic escalation evaluation. Experiences daily nocturnal awakenings, dyspnea on minimal exertion, and frequent rescue inhaler usage (albuterol 4-5x daily). Experienced 3 severe exacerbations requiring systemic corticosteroid bursts (prednisone 40mg x 5 days) within the past 9 months.

PRIOR TREATMENTS & STEP THERAPY AUDIT:
1. High-dose Inhaled Corticosteroid / LABA: Fluticasone/Salmeterol (Advair Diskus 500/50 mcg twice daily) continuously for 18 months with verified 94% pharmacy refill adherence.
2. Long-Acting Muscarinic Antagonist (LAMA): Tiotropium (Spiriva Respimat 2.5 mcg daily) added 8 months ago without adequate symptom stabilization.
3. Montelukast (Singulair 10mg daily): Trialed for 3 months; discontinued due to sleep disturbances and neuropsychiatric adverse effects.

LABORATORY & BIOMARKER DATA:
- Blood Eosinophil Count: 480 cells/uL (Baseline elevation consistent with Type 2 eosinophilic asthma, ref > 150 cells/uL).
- Fractional Exhaled Nitric Oxide (FeNO): 62 ppb (Markedly elevated).
- Spirometry: FEV1 61% predicted (1.72 L), improving by 8% post-bronchodilator.

ASSESSMENT:
Diagnosis: J45.50 - Severe persistent asthma, uncomplicated with eosinophilic phenotype.
Requested Therapy: Dupixent (dupilumab) 300 mg/2 mL pre-filled syringe every 2 weeks subcutaneous.
Guideline Alignment: Patient satisfies UnitedHealthcare Medical Policy 2026R0012 for Dupixent add-on maintenance in eosinophilic asthma.""",

    "Lumbar Spine MRI (Radiculopathy)": """OUTPATIENT ORTHOPEDIC CLINICAL ENCOUNTER
Date of Visit: 2026-09-10
Patient: Robert H. Chen | DOB: 1965-06-30 | MRN: #33190-OR

HISTORY:
61-year-old male with 14 weeks of progressive, disabling lower back pain radiating down the left posterolateral thigh and calf to the dorsum of the foot (L5 dermatome distribution). Numbness in the great toe. Visual Analog Pain Scale: 8/10.

FAILED CONSERVATIVE THERAPIES:
1. Formal Physical Therapy: 12 sessions completed between July 1 and August 25, 2026 with licensed PT (core strengthening, McKenzie exercises). Minimal symptom relief.
2. Pharmacotherapy: Oral NSAIDs (Meloxicam 15mg daily x 6 weeks) and Gabapentin (300mg TID x 8 weeks).
3. Activity modification and home exercise protocol adhered to.

PHYSICAL EXAMINATION:
- Positive Left Straight Leg Raise test at 35 degrees reproducing radicular shooting pain.
- Decreased sensation to light touch over the left lateral calf and first web space.
- Left extensor hallucis longus weakness (4/5 motor strength).

ASSESSMENT & ORDER:
Diagnosis: M54.16 - Radiculopathy, lumbar region; M51.26 - Other intervertebral disc displacement, lumbar region.
Requested Procedure: CPT 72148 - MRI Lumbar Spine without contrast.
Clinical Necessity: Patient has failed > 6 weeks of structured conservative care with progressive neurologic deficit (motor weakness). Meets BCBS Prior Authorization guideline for advanced spine imaging."""
}

if "authorizations" not in st.session_state:
    st.session_state.authorizations = [
        {
            "id": "PA-2026-1001",
            "patient": "Johnathan Miller",
            "dob": "1988-04-12",
            "payer": "Aetna",
            "treatment": "Humira (adalimumab) 40mg SubQ",
            "status": "Pending",
            "submission_date": "2026-09-18",
            "tracking_id": None
        },
        {
            "id": "PA-2026-1002",
            "patient": "Maria E. Vasquez",
            "dob": "1979-11-23",
            "payer": "UHC (UnitedHealthcare)",
            "treatment": "Dupixent (dupilumab) 300mg",
            "status": "Submitted to Payer Portal",
            "submission_date": "2026-09-20",
            "tracking_id": "UHC-EDI278-984412-TX"
        },
        {
            "id": "PA-2026-1003",
            "patient": "Robert H. Chen",
            "dob": "1965-06-30",
            "payer": "BCBS (Blue Cross Blue Shield)",
            "treatment": "Lumbar Spine MRI (CPT 72148)",
            "status": "Approved",
            "submission_date": "2026-09-12",
            "tracking_id": "BCBS-AUTH-663819-APPR"
        },
        {
            "id": "PA-2026-1004",
            "patient": "Eleanor Vance",
            "dob": "1972-03-14",
            "payer": "Cigna",
            "treatment": "Ozempic (semaglutide) 1mg/dose",
            "status": "Denied",
            "submission_date": "2026-09-08",
            "tracking_id": "CGN-DENIAL-773129"
        }
    ]

if "last_extraction_result" not in st.session_state:
    st.session_state.last_extraction_result = None

if "note_text_buffer" not in st.session_state:
    st.session_state.note_text_buffer = ""


# -----------------------------------------------------------------------------
# 3. AI EXTRACTION ENGINE (SIMULATION LOGIC)
# -----------------------------------------------------------------------------
def simulate_ai_chart_extraction(note_text: str, patient_name: str, treatment: str, payer: str):
    """
    Simulates clinical NLP entity extraction and policy compliance checking.
    Parses ICD-10 codes, symptom duration, failed step therapies, and policy criteria.
    """
    lower_text = note_text.lower()
    
    # 1. Detect Diagnosis Codes (ICD-10)
    icd10 = []
    if "crohn" in lower_text or "k50" in lower_text:
        icd10.append("K50.00 - Crohn's disease of small intestine without complications")
    if "asthma" in lower_text or "j45" in lower_text:
        icd10.append("J45.50 - Severe persistent asthma, uncomplicated (Type 2 Eosinophilic)")
    if "radiculopathy" in lower_text or "m54" in lower_text or "mri" in lower_text or "disc" in lower_text:
        icd10.append("M54.16 - Radiculopathy, lumbar region")
        icd10.append("M51.26 - Intervertebral disc displacement, lumbar region")
    if "diabet" in lower_text or "e11" in lower_text:
        icd10.append("E11.9 - Type 2 diabetes mellitus without complications")
    if not icd10:
        icd10 = ["R69 - Illness, unspecified / Clinical evaluation ongoing"]

    # 2. Detect Prior Failed Step Therapies
    failed_therapies = []
    if "mesalamine" in lower_text or "asacol" in lower_text:
        failed_therapies.append("Mesalamine / 5-ASA (Failed: refractory mucosal inflammation)")
    if "azathioprine" in lower_text or "imuran" in lower_text:
        failed_therapies.append("Azathioprine (Intolerance: hepatotoxicity ALT 145 U/L)")
    if "budesonide" in lower_text or "prednisone" in lower_text:
        failed_therapies.append("Systemic Corticosteroids (Failed: flare recurrence upon taper)")
    if "fluticasone" in lower_text or "advair" in lower_text or "ics" in lower_text:
        failed_therapies.append("High-dose Inhaled Corticosteroid / LABA (18 mos adherence documented)")
    if "spiriva" in lower_text or "lama" in lower_text:
        failed_therapies.append("Tiotropium (LAMA add-on) - inadequate control")
    if "physical therapy" in lower_text or "pt" in lower_text:
        failed_therapies.append("Formal Physical Therapy (12 structured sessions completed)")
    if "meloxicam" in lower_text or "nsaid" in lower_text or "gabapentin" in lower_text:
        failed_therapies.append("Oral NSAID / Gabapentin trial (>6 weeks)")
    if not failed_therapies:
        failed_therapies = ["No structured prior step therapies explicitly identified in submitted note"]

    # 3. Detect Duration
    duration = "Documented > 4 to 18 months progression" if "month" in lower_text else "Documented > 6 to 14 weeks duration"

    # 4. Biomarkers & Objective Exam Findings
    biomarkers = []
    if "calprotectin" in lower_text:
        biomarkers.append("Fecal Calprotectin: 840 ug/g (Markedly elevated)")
    if "eosinophil" in lower_text:
        biomarkers.append("Blood Eosinophil Count: 480 cells/uL (Elevated >= 150)")
    if "straight leg raise" in lower_text or "slr" in lower_text:
        biomarkers.append("Physical Exam: Positive SLR at 35°, motor weakness 4/5")
    if not biomarkers:
        biomarkers.append("Routine vital signs recorded; no specialized labs in note")

    # 5. Payer Policy Check Evaluation
    policy_status = "CRITERIA MET (High Approval Probability: 95%)"
    if len(failed_therapies) < 2 and "unspecified" in failed_therapies[0].lower():
        policy_status = "WARNING: INSUFFICIENT STEP THERAPY (Risk of Denial: 65%)"
    
    return {
        "case_metadata": {
            "patient_name": patient_name,
            "payer": payer,
            "requested_treatment": treatment,
            "extraction_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "extracted_clinical_criteria": {
            "icd10_diagnosis_codes": icd10,
            "symptom_duration": duration,
            "prior_failed_treatments": failed_therapies,
            "biomarkers_and_exam_findings": biomarkers,
            "medical_necessity_rationale": (
                f"Patient exhibits objective pathology refractory to standard conservative treatment. "
                f"Documented clinical criteria align with FDA label and {payer} prior authorization policy."
            )
        },
        "payer_policy_check": {
            "payer_guideline": f"{payer} Medical Policy Guidelines (ANSI X12 278 Review)",
            "step_therapy_requirement_satisfied": len(failed_therapies) >= 2,
            "determination": policy_status,
            "recommended_action": "Ready for electronic 278 Payer Portal Submission"
        }
    }


# -----------------------------------------------------------------------------
# 4. SIDEBAR: CASE INTAKE & CLINICAL NOTE UPLOADER
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("📋 Case Intake & Intake Wizard")
    st.caption("Enter patient details and upload clinical chart to initiate prior authorization.")

    # Quick sample clinical presets
    st.markdown("**⚡ Quick Load Sample Clinical Scenario:**")
    col_pre1, col_pre2 = st.columns(2)
    with col_pre1:
        if st.button("Crohn's / Humira", use_container_width=True):
            st.session_state["default_patient"] = "Johnathan Miller"
            st.session_state["default_dob"] = date(1988, 4, 12)
            st.session_state["default_payer"] = "Aetna"
            st.session_state["default_treatment"] = "Humira (adalimumab) 40mg SubQ"
            st.session_state.note_text_buffer = SAMPLE_NOTES["Crohn's Disease (Humira)"]
            st.rerun()

    with col_pre2:
        if st.button("Asthma / Dupixent", use_container_width=True):
            st.session_state["default_patient"] = "Maria E. Vasquez"
            st.session_state["default_dob"] = date(1979, 11, 23)
            st.session_state["default_payer"] = "UHC (UnitedHealthcare)"
            st.session_state["default_treatment"] = "Dupixent (dupilumab) 300mg"
            st.session_state.note_text_buffer = SAMPLE_NOTES["Severe Asthma (Dupixent)"]
            st.rerun()

    # Form inputs with session state defaults
    patient_name = st.text_input(
        "Patient Full Name", 
        value=st.session_state.get("default_patient", "Johnathan Miller"),
        placeholder="e.g. Johnathan Miller"
    )
    
    dob = st.date_input(
        "Date of Birth (DOB)", 
        value=st.session_state.get("default_dob", date(1988, 4, 12)),
        min_value=date(1920, 1, 1),
        max_value=date.today()
    )

    payers_list = ["Aetna", "BCBS (Blue Cross Blue Shield)", "UHC (UnitedHealthcare)", "Cigna", "Humana"]
    payer_idx = 0
    if "default_payer" in st.session_state and st.session_state["default_payer"] in payers_list:
        payer_idx = payers_list.index(st.session_state["default_payer"])
    
    payer_name = st.selectbox("Target Payer", payers_list, index=payer_idx)

    treatment_name = st.text_input(
        "Requested Treatment / Medication",
        value=st.session_state.get("default_treatment", "Humira (adalimumab) 40mg SubQ"),
        placeholder="e.g. Dupixent 300mg, Keytruda, Lumbar MRI"
    )

    st.markdown("---")
    st.subheader("📄 Clinical Note Upload")
    
    uploaded_file = st.file_uploader("Upload Medical Record / Note (.txt)", type=["txt", "md"])
    if uploaded_file is not None:
        raw_text = uploaded_file.read().decode("utf-8")
        st.session_state.note_text_buffer = raw_text
        st.success(f"Uploaded: {uploaded_file.name} ({len(raw_text)} characters)")

    # Editable text area for note inspection
    note_text = st.text_area(
        "Clinical Chart Text (Preview / Edit)", 
        value=st.session_state.note_text_buffer,
        height=180,
        placeholder="Paste clinical progress note, operative report, or conservative therapy records here..."
    )
    st.session_state.note_text_buffer = note_text

    st.markdown("---")
    
    # 3. AI Extraction Trigger Button in Sidebar
    run_ai_btn = st.button("🤖 Run AI Chart Extraction & Policy Check", type="primary", use_container_width=True)
    if run_ai_btn:
        if not note_text.strip():
            st.error("Please enter or upload a clinical note text first!")
        else:
            with st.spinner("AI Chart Engine scanning clinical note and validating against payer medical policy..."):
                time.sleep(1.0)
                extraction_result = simulate_ai_chart_extraction(
                    note_text=note_text,
                    patient_name=patient_name,
                    treatment=treatment_name,
                    payer=payer_name
                )
                st.session_state.last_extraction_result = extraction_result
                st.success("Extraction & Policy Validation Complete!")

    # Save to Active Cases Queue
    if st.button("📥 Save & Add to Active Prior Auth Queue", use_container_width=True):
        if not patient_name.strip():
            st.error("Please specify patient name.")
        else:
            new_id = f"PA-2026-{random.randint(1005, 9999)}"
            new_case = {
                "id": new_id,
                "patient": patient_name,
                "dob": dob.strftime("%Y-%m-%d"),
                "payer": payer_name,
                "treatment": treatment_name,
                "status": "Pending",
                "submission_date": datetime.today().strftime("%Y-%m-%d"),
                "tracking_id": None
            }
            st.session_state.authorizations.insert(0, new_case)
            st.toast(f"Case {new_id} queued for {patient_name}!", icon="✅")
            st.rerun()


# -----------------------------------------------------------------------------
# 5. MAIN DASHBOARD VIEW
# -----------------------------------------------------------------------------
st.title("🏥 Multi-Payer Prior Authorization Command Center")
st.caption("Enterprise HealthTech Operational Console for Real-Time Clinical NLP Extraction & Clearinghouse Submissions")

# 5.1 Real-Time Metrics Counters
total_cases = len(st.session_state.authorizations)
pending_count = sum(1 for c in st.session_state.authorizations if c["status"] == "Pending")
submitted_count = sum(1 for c in st.session_state.authorizations if "Submitted" in c["status"])
approved_count = sum(1 for c in st.session_state.authorizations if c["status"] == "Approved")
denied_count = sum(1 for c in st.session_state.authorizations if c["status"] == "Denied")

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
col_m1.metric("Total Active Cases", total_cases)
col_m2.metric("Pending Review", pending_count, delta=f"{pending_count} awaiting action")
col_m3.metric("Submitted to Portal", submitted_count)
col_m4.metric("Approved", approved_count, delta="Pass Rate 75%")
col_m5.metric("Denied", denied_count, delta="-1 Needs Appeal", delta_color="inverse")

st.markdown("---")

# 5.2 Top Tabs: Dashboard Table, Extraction Inspector, Portal Dispatcher
tab_dashboard, tab_extraction, tab_portal = st.tabs([
    "📊 Active Prior Authorizations Table", 
    "🔍 AI Chart Extraction & Policy Check Output", 
    "🚀 Clearinghouse & Portal Submission Dispatcher"
])

# -----------------------------------------------------------------------------
# TAB 1: MAIN ACTIVE PRIOR AUTHORIZATIONS TABLE & FILTERS
# -----------------------------------------------------------------------------
with tab_dashboard:
    st.subheader("Active Prior Authorization Cases")
    
    f_col1, f_col2, f_col3 = st.columns([2, 2, 2])
    with f_col1:
        status_filter = st.selectbox("Filter by Status", ["All Statuses", "Pending", "Submitted to Payer Portal", "Approved", "Denied"])
    with f_col2:
        payer_filter = st.selectbox("Filter by Payer", ["All Payers", "Aetna", "BCBS (Blue Cross Blue Shield)", "UHC (UnitedHealthcare)", "Cigna", "Humana"])
    with f_col3:
        search_query = st.text_input("Search Patient or Case ID", placeholder="Search by name or ID...")

    filtered_cases = st.session_state.authorizations
    if status_filter != "All Statuses":
        filtered_cases = [c for c in filtered_cases if c["status"] == status_filter]
    if payer_filter != "All Payers":
        filtered_cases = [c for c in filtered_cases if c["payer"] == payer_filter]
    if search_query.strip():
        q = search_query.lower()
        filtered_cases = [c for c in filtered_cases if q in c["patient"].lower() or q in c["id"].lower() or q in c["treatment"].lower()]

    display_rows = []
    for c in filtered_cases:
        display_rows.append({
            "Auth ID": c["id"],
            "Patient Name": c["patient"],
            "DOB": c["dob"],
            "Payer": c["payer"],
            "Requested Treatment": c["treatment"],
            "Status": c["status"],
            "Submission Date": c["submission_date"],
            "Portal Tracking ID": c["tracking_id"] if c["tracking_id"] else "— Not Submitted —"
        })

    df_display = pd.DataFrame(display_rows)
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(display_rows)} of {total_cases} total records.")


# -----------------------------------------------------------------------------
# TAB 2: AI CHART EXTRACTION & POLICY CHECK INSPECTOR
# -----------------------------------------------------------------------------
with tab_extraction:
    st.subheader("AI Clinical Criteria Extraction & Policy Compliance Result")
    
    if st.session_state.last_extraction_result is None:
        st.info("💡 No extraction executed yet. Use the sidebar button 'Run AI Chart Extraction & Policy Check' to analyze a clinical chart.")
    else:
        res = st.session_state.last_extraction_result
        
        c_e1, c_e2 = st.columns([1, 1])
        with c_e1:
            st.markdown("#### 🎯 Clinical Extraction Highlights")
            st.write(f"**Patient:** {res['case_metadata']['patient_name']}")
            st.write(f"**Target Payer:** {res['case_metadata']['payer']}")
            st.write(f"**Requested Drug/Procedure:** {res['case_metadata']['requested_treatment']}")
            st.write(f"**Extraction Timestamp:** `{res['case_metadata']['extraction_timestamp']}`")
            
        with c_e2:
            st.markdown("#### 🛡️ Payer Policy Verification")
            det = res['payer_policy_check']['determination']
            if "CRITERIA MET" in det:
                st.success(f"**Status:** {det}")
            else:
                st.warning(f"**Status:** {det}")
            st.write(f"**Policy Guideline:** {res['payer_policy_check']['payer_guideline']}")
            st.write(f"**Step Therapy Met:** {'✅ Yes' if res['payer_policy_check']['step_therapy_requirement_satisfied'] else '❌ No'}")
            st.write(f"**Recommendation:** {res['payer_policy_check']['recommended_action']}")

        st.markdown("---")
        st.markdown("#### 📦 Extracted Structured JSON Payload (EDI 278 Format)")
        st.json(res)


# -----------------------------------------------------------------------------
# TAB 3: CLEARINGHOUSE & PORTAL SUBMISSION DISPATCHER
# -----------------------------------------------------------------------------
with tab_portal:
    st.subheader("🚀 Payer Clearinghouse Portal Submission (Simulated EDI 278)")
    st.markdown("Select any **Pending** prior authorization case below to execute a simulated submission to the payer's adjudication clearinghouse.")

    pending_cases = [c for c in st.session_state.authorizations if c["status"] == "Pending"]
    
    if not pending_cases:
        st.success("🎉 All active cases have been submitted or adjudicated!")
    else:
        case_options = {f"{c['id']} — {c['patient']} ({c['payer']}) | {c['treatment']}": c for c in pending_cases}
        selected_key = st.selectbox("Select Pending Prior Authorization Case:", list(case_options.keys()))
        selected_case = case_options[selected_key]

        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            st.write(f"**Selected Case ID:** `{selected_case['id']}`")
            st.write(f"**Patient:** {selected_case['patient']} (DOB: {selected_case['dob']})")
            st.write(f"**Payer:** {selected_case['payer']}")
            st.write(f"**Treatment / Medication:** {selected_case['treatment']}")
            st.write(f"**Current Status:** :orange[{selected_case['status']}]")

        with col_p2:
            st.write("**Clearinghouse Route:**")
            st.code("EDI 278 Health Care Services Review\nProtocol: HTTPS / CAQH CORE 278\nTarget: Direct Payer API Gateway", language="text")

        st.markdown("---")

        # 4. Action: Simulate Portal Submission
        if st.button("📤 Simulate Portal Submission", type="primary", use_container_width=True):
            with st.spinner(f"Transmitting electronic Prior Authorization packet to {selected_case['payer']} clearinghouse..."):
                time.sleep(1.2)
                prefix = selected_case['payer'].split()[0].upper()
                mock_tracking = f"{prefix}-EDI278-{random.randint(100000, 999999)}-TX"
                
                # Update case in session state
                for c in st.session_state.authorizations:
                    if c["id"] == selected_case["id"]:
                        c["status"] = "Submitted to Payer Portal"
                        c["tracking_id"] = mock_tracking
                        c["submission_date"] = datetime.today().strftime("%Y-%m-%d")
                        break
                
                st.balloons()
                st.success(f"**Success! Case {selected_case['id']} submitted to {selected_case['payer']} Portal!**")
                st.info(f"🔑 **Payer Confirmation Tracking Number:** `{mock_tracking}`")
                st.rerun()

st.markdown("---")
st.caption("Enterprise Prior Authorization Engine • HIPAA & CORE 278 Compliant Architecture Prototype")