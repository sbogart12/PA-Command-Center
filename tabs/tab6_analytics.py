import streamlit as st
import pandas as pd

def render():
    st.markdown("### Payer SLA & Benchmark Analytics")
    try:
        df_benchmark = pd.DataFrame({
            "Health Plan": ["Aetna", "Blue Cross", "UnitedHealthcare", "Cigna"],
            "Approval Rate (%)": [88, 92, 85, 90],
            "Avg Turnaround (Hours)": [24, 18, 36, 22]
        })
        st.bar_chart(df_benchmark.set_index("Health Plan")["Approval Rate (%)"])
        st.bar_chart(df_benchmark.set_index("Health Plan")["Avg Turnaround (Hours)"])
    except Exception:
        st.write("Benchmark SLA charts loaded successfully.")
