import streamlit as st
import pandas as pd
from simulation import simulate

st.set_page_config(page_title="Customer Simulation", layout="wide")
st.title("🧪 Customer Arrival and Reneging Simulation")

# Load CSV from Google Sheets
CSV_URL = "https://docs.google.com/spreadsheets/d/1q5VdeoHnj1UMFGm781BDCEsNcWncX72UOlDOQrKTEgY/export?format=csv"

try:
    data = pd.read_csv(CSV_URL)
    st.session_state.data = data
except Exception as e:
    st.error("Failed to load data from Google Sheets.")
    st.stop()

# Editable table
st.subheader("📋 Edit Simulation Data (local changes only)")
data = st.data_editor(st.session_state.data, num_rows="dynamic", key="editor")

# Run simulation
if st.button("🚦 Run Simulation"):
    log_list = []
    simulate(data, log_list)

    # Display logs in a tabular format using st.dataframe
    st.subheader("📜 Simulation Log")
    log_df = pd.DataFrame(log_list)
    st.dataframe(log_df)  # This will display the log as a table in Streamlit

# Optional save locally
if st.button("💾 Save Edited Data as CSV"):
    data.to_csv("edited_sim_data.csv", index=False)
    st.success("Saved as edited_sim_data.csv")
