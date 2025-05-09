import streamlit as st
import pandas as pd
from simulate import simulate  # <-- import from simulate.py

st.set_page_config(page_title="Customer Simulation", layout="wide")
st.title("🧪 Customer Arrival and Reneging Simulation")

CSV_URL = "https://docs.google.com/spreadsheets/d/1q5VdeoHnj1UMFGm781BDCEsNcWncX72UOlDOQrKTEgY/export?format=csv"

try:
    data = pd.read_csv(CSV_URL)
    st.session_state.data = data
except Exception as e:
    st.error("Failed to load data from Google Sheets.")
    st.stop()

st.subheader("📋 Edit Simulation Data (local changes only)")
data = st.data_editor(st.session_state.data, num_rows="dynamic", key="editor")

if st.button("🚦 Run Simulation"):
    log_list = []
    simulate(data, log_list)
    log_df = pd.DataFrame(log_list)
    st.subheader("📊 Tabulated Simulation Log")
    st.dataframe(log_df, use_container_width=True)

if st.button("💾 Save Edited Data as CSV"):
    data.to_csv("edited_sim_data.csv", index=False)
    st.success("Saved as edited_sim_data.csv")
