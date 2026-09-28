import streamlit as st
import sys
import os

# Ensure tabs directory is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "tabs"))

import tab0_intake
import tab1_expiration
import tab2_extraction
import tab3_policy
import tab4_appeal
import tab5_p2p
import tab6_analytics

st.set_page_config(page_title="Prior Authorization Command Center", layout="wide")

st.title("🛡️ Multi-Payer Prior Authorization Command Center")
st.markdown("---")
st.subheader("⚙️ Clinical Action & Compliance Hub")

action_tab0, action_tab1, action_tab2, action_tab3, action_tab4, action_tab5, action_tab6 = st.tabs([
    "📝 Patient Intake",
    "🔄 Expiration & Renewal Log (10-Day)",
    "🤖 AI Chart Extraction",
    "📋 Policy Adherence Checklist",
    "📄 Appeal & Letter of Necessity",
    "🩺 P2P Brief Generator",
    "📊 Payer SLA & Utilization Analytics"
])

with action_tab0:
    tab0_intake.render()

with action_tab1:
    tab1_expiration.render()

with action_tab2:
    tab2_extraction.render()

with action_tab3:
    tab3_policy.render()

with action_tab4:
    tab4_appeal.render()

with action_tab5:
    tab5_p2p.render()

with action_tab6:
    tab6_analytics.render()
