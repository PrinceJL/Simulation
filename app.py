import streamlit as st
import pandas as pd
from simulation.customer import generate_customer_data
from simulation.jeepney import generate_jeepney_data

st.set_page_config(page_title="Jeepney-Customer Simulation", layout="wide")
st.title("🚌 Jeepney and Customer Simulation with Replications")

# Sidebar configuration
st.sidebar.header("Simulation Settings")
num_groups = st.sidebar.slider("Customer Groups", 10, 100, 50)
num_jeeps = st.sidebar.slider("Jeepneys", 10, 100, 30)
replications = st.sidebar.slider("Replications", 1, 10, 3)

# Run simulations
customer_runs = []
jeepney_runs = []
for i in range(replications):
    customer_runs.append(generate_customer_data(num_groups=num_groups, seed=42+i))
    jeepney_runs.append(generate_jeepney_data(num_jeeps=num_jeeps, seed=99+i))

# Compute metrics
def compute_metrics():
    total_arrived, total_reneged, total_wait, total_boarded, total_util = 0, 0, 0, 0, 0

    for cust_df, jeep_df in zip(customer_runs, jeepney_runs):
        total_arrived += cust_df["No of Customer Arrived"].sum()
        total_reneged += cust_df["No of Reneged"].sum()
        total_wait += cust_df["Avg Wait Time (mins)"].mean()
        total_boarded += jeep_df["Number of Passengers Boarded"].sum()
        total_util += jeep_df["Utilization"].mean()

    return {
        "Avg Total Arrived": total_arrived // replications,
        "Avg Reneged": total_reneged // replications,
        "Avg Reneging Rate (%)": round((total_reneged / total_arrived) * 100, 2),
        "Avg Wait Time (mins)": round(total_wait / replications, 2),
        "Avg Jeepney Boarded": total_boarded // replications,
        "Avg Jeepney Utilization": round(total_util / replications, 2)
    }

metrics = compute_metrics()

# Display metrics
st.subheader("📊 Aggregated Metrics Across Replications")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers Arrived", metrics["Avg Total Arrived"])
col1.metric("Total Reneged", metrics["Avg Reneged"])
col2.metric("Avg Wait Time", f"{metrics['Avg Wait Time (mins)']} mins")
col2.metric("Reneging Rate", f"{metrics['Avg Reneging Rate (%)']}%")
col3.metric("Total Boarded", metrics["Avg Jeepney Boarded"])
col3.metric("Jeepney Utilization", f"{metrics['Avg Jeepney Utilization']}")

# --- 🔄 NEW: Replication selector ---
st.subheader("📑 View Individual Replication Details")
selected_replication = st.selectbox("Select replication run:", range(1, replications+1), index=0)
rep_index = selected_replication - 1

st.markdown(f"### 👥 Customer Arrivals (Replication {selected_replication})")
st.dataframe(customer_runs[rep_index])

st.markdown(f"### 🛺 Jeepney Arrivals (Replication {selected_replication})")
st.dataframe(jeepney_runs[rep_index])
