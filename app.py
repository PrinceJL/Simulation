import streamlit as st
import pandas as pd
import simpy
from simulation import simulate_gate2

st.set_page_config(page_title="Jeepney and Customer Simulation", layout="wide")
st.title("🚗 Jeepney and Customer Simulation at Gate 2")

# Load the customer and jeepney data from Google Sheets
CSV_URL_CUSTOMER = "https://docs.google.com/spreadsheets/d/1q5VdeoHnj1UMFGm781BDCEsNcWncX72UOlDOQrKTEgY/export?format=csv&gid=0"
CSV_URL_JEEPNEY = "https://docs.google.com/spreadsheets/d/1q5VdeoHnj1UMFGm781BDCEsNcWncX72UOlDOQrKTEgY/export?format=csv&gid=1621107266"  # Update as needed

try:
    customer_data = pd.read_csv(CSV_URL_CUSTOMER)
    jeepney_data = pd.read_csv(CSV_URL_JEEPNEY)
    st.session_state.customer_data = customer_data
    st.session_state.jeepney_data = jeepney_data
except Exception as e:
    st.error("Failed to load data from Google Sheets.")
    st.stop()

# Editable table for customer data
st.subheader("📋 Edit Customer Data")
customer_data = st.data_editor(st.session_state.customer_data, num_rows="dynamic", key="customer_editor")

# Editable table for jeepney data
st.subheader("📋 Edit Jeepney Data")
jeepney_data = st.data_editor(st.session_state.jeepney_data, num_rows="dynamic", key="jeepney_editor")

# Initialize the SimPy environment
env = simpy.Environment()

# Run the simulation
log_list = []  # Initialize log list
if st.button("🚦 Run Simulation"):
    # Call the simulate_gate2 function with the SimPy environment and data
    simulate_gate2(env, customer_data, jeepney_data, log_list)

    # Display logs from the simulation
    st.subheader("📜 Simulation Log")
    for line in log_list:
        st.text(line)

# Optional save locally for customer and jeepney data
if st.button("💾 Save Edited Data as CSV"):
    customer_data.to_csv("edited_customer_data.csv", index=False)
    jeepney_data.to_csv("edited_jeepney_data.csv", index=False)
    st.success("Saved as edited_customer_data.csv and edited_jeepney_data.csv")
