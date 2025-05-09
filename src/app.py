import streamlit as st
import pandas as pd
import simpy
import random

# Helper function to convert time string to seconds
def to_seconds(tstr):
    m, s = map(int, tstr.split(":"))
    return m * 60 + s

# Simulation logic
def simulate(data, log_list):
    env = simpy.Environment()
    counter = simpy.Resource(env, capacity=1)

    # Customer process
    def customer(env, name, counter, patience):
        arrival = env.now
        log_list.append(f"[{env.now:.0f}s] {name} arrives")

        with counter.request() as req:
            result = yield req | env.timeout(patience)
            if req in result:
                wait_time = env.now - arrival
                log_list.append(f"[{env.now:.0f}s] {name} begins service after {wait_time:.0f}s")
                yield env.timeout(random.uniform(30, 60))
                log_list.append(f"[{env.now:.0f}s] {name} leaves after service")
            else:
                log_list.append(f"[{env.now:.0f}s] {name} reneged after waiting {patience:.0f}s")

    # Generate customer arrivals based on the data
    def generate_customers(env, data, counter):
        for i, row in data.iterrows():
            yield env.timeout(to_seconds(row['Arrival Time based on previous']))
            for j in range(int(row['No of Customer Arrived'])):
                name = f"Cust_{i}_{j}"
                if j >= (int(row['No of Customer Arrived']) - int(row['No of Reneged'])):
                    patience = random.uniform(10, 40)
                else:
                    patience = random.uniform(100, 300)
                env.process(customer(env, name, counter, patience))

    env.process(generate_customers(env, data, counter))
    env.run()

# Streamlit app code
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

    # Display logs
    st.subheader("📜 Simulation Log")
    for line in log_list:
        st.text(line)

# Optional save locally
if st.button("💾 Save Edited Data as CSV"):
    data.to_csv("edited_sim_data.csv", index=False)
    st.success("Saved as edited_sim_data.csv")
