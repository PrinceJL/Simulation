import streamlit as st
import pandas as pd
import numpy as np

# Simulate jeepney data
def jeepney_simulation():
    # Load the data
    data = pd.read_csv("https://docs.google.com/spreadsheets/d/1q5VdeoHnj1UMFGm781BDCEsNcWncX72UOlDOQrKTEgY/export?format=csv&gid=1621107266")
    df_jeepney = pd.DataFrame(data)

    # Function to convert time in MM:SS format to minutes
    def convert_to_minutes(time_str):
        mins, secs = map(int, time_str.split(':'))
        return mins + secs / 60

    # Apply conversion
    df_jeepney['Interarrival in mins'] = df_jeepney['Interarrival in mins'].apply(convert_to_minutes)
    df_jeepney['Time Arrived'] = df_jeepney['Time Arrived'].apply(convert_to_minutes)
    df_jeepney['Time Departed'] = df_jeepney['Time Departed'].apply(convert_to_minutes)

    # Interarrival Time Distribution
    interarrival_hist, interarrival_bins = np.histogram(df_jeepney['Interarrival in mins'], bins=5, density=True)
    interarrival_prob = interarrival_hist / interarrival_hist.sum()

    # Number of Passengers Distribution
    passenger_hist, passenger_bins = np.histogram(df_jeepney['Number of Passengers Boarded'], bins=5, density=True)
    passenger_prob = passenger_hist / passenger_hist.sum()

    # Jeepney Stopped Distribution
    stopped_prob = df_jeepney['Jeepney came from phase 3 but stopped'].value_counts(normalize=True).sort_index()

    return interarrival_prob, interarrival_bins, passenger_prob, passenger_bins, stopped_prob

# Simulation logic
def run_simulation(customer_interarrival_time, jeepney_interarrival_time, jeepney_capacity, simulation_time, num_replications):
    results = []
    total_customers_arrived = 0
    total_customers_served = 0
    total_customers_reneged = 0
    total_jeepneys_arrived = 0
    total_jeepney_utilization_time = 0

    np.random.seed(42)  # For reproducibility
    for replication in range(num_replications):
        time = 0
        customers_waiting = 0
        customers_served = 0
        customers_reneged = 0
        total_wait_time = 0
        jeepney_arrivals = 0
        jeepney_utilization_time = 0

        while time < simulation_time:
            # Simulate customer arrival
            interarrival_time = np.random.exponential(customer_interarrival_time)
            time += interarrival_time
            if time > simulation_time:
                break
            customers_waiting += 1
            total_customers_arrived += 1

            # Simulate reneging
            reneged = np.random.rand() < 0.1  # 10% chance of reneging
            if reneged:
                customers_waiting -= 1
                customers_reneged += 1
                total_customers_reneged += 1
                continue

            # Simulate jeepney arrival
            jeepney_arrival_time = time + np.random.exponential(jeepney_interarrival_time)
            if jeepney_arrival_time > simulation_time:
                break
            jeepney_arrivals += 1
            total_jeepneys_arrived += 1

            # Serve customers
            if customers_waiting > 0:
                num_served = min(customers_waiting, jeepney_capacity)
                customers_served += num_served
                total_customers_served += num_served
                total_wait_time += num_served * (jeepney_arrival_time - time)
                customers_waiting -= num_served
                jeepney_utilization_time += num_served

        # Store results for this replication
        results.append({
            "Replication": replication + 1,
            "Customers Arrived": customers_served + customers_reneged,
            "Customers Served": customers_served,
            "Customers Reneged": customers_reneged,
            "Jeepneys Arrived": jeepney_arrivals,
            "Average Wait Time (mins)": total_wait_time / customers_served if customers_served > 0 else 0,
            "Utilization Rate": jeepney_utilization_time / (jeepney_arrivals * jeepney_capacity) if jeepney_arrivals > 0 else 0
        })

    # Compute overall metrics
    total_customers = total_customers_arrived
    reneging_rate = total_customers_reneged / total_customers if total_customers > 0 else 0
    jeepney_utilization_rate = total_jeepney_utilization_time / (total_jeepneys_arrived * jeepney_capacity) if total_jeepneys_arrived > 0 else 0

    metrics = {
        "Total Customers Arrived": total_customers_arrived,
        "Total Customers Served": total_customers_served,
        "Total Customers Reneged": total_customers_reneged,
        "Reneging Rate": reneging_rate,
        "Total Jeepneys Arrived": total_jeepneys_arrived,
        "Jeepney Utilization Rate": jeepney_utilization_rate
    }

    return pd.DataFrame(results), metrics

# Streamlit App
def main():
    st.title("Jeepney and Customer Simulation")

    # Sidebar for Simulation Parameters
    st.sidebar.header("Simulation Parameters")
    
    # Customer Parameters
    st.sidebar.subheader("Customer Parameters")
    customer_interarrival_time = st.sidebar.slider("Avg Customer Interarrival Time (mins)", 1, 10, 5)

    # Jeepney Parameters
    st.sidebar.subheader("Jeepney Parameters")
    jeepney_interarrival_time = st.sidebar.slider("Avg Jeepney Interarrival Time (mins)", 1, 15, 7)
    jeepney_capacity = st.sidebar.slider("Jeepney Capacity", 5, 30, 15)

    # Simulation Parameters
    st.sidebar.subheader("Simulation Setup")
    num_replications = st.sidebar.slider("Number of Replications", 1, 50, 10)
    simulation_time = st.sidebar.slider("Total Simulation Time (mins)", 30, 240, 120)

    # Run Jeepney Simulation
    interarrival_prob, interarrival_bins, passenger_prob, passenger_bins, stopped_prob = jeepney_simulation()

    # Run the Simulation
    results_df, metrics = run_simulation(customer_interarrival_time, jeepney_interarrival_time, jeepney_capacity, simulation_time, num_replications)

    # Tabs for Different Views
    tab1, tab2 = st.tabs(["Probability Tables", "Simulation Results"])

    # Tab 1: Probability Tables
    with tab1:
        st.subheader("Jeepney Probability Tables")

        # Interarrival Time Distribution
        interarrival_results = pd.DataFrame({
            "Range (mins)": [f"{interarrival_bins[i]:.2f} - {interarrival_bins[i+1]:.2f}" for i in range(len(interarrival_prob))],
            "Probability": interarrival_prob
        })
        st.write("**Interarrival Time Distribution (Jeepneys):**")
        st.table(interarrival_results)

        # Passenger Boarding Distribution
        passenger_results = pd.DataFrame({
            "Range (passengers)": [f"{passenger_bins[i]:.0f} - {passenger_bins[i+1]:.0f}" for i in range(len(passenger_prob))],
            "Probability": passenger_prob
        })
        st.write("**Passenger Boarding Distribution (Jeepneys):**")
        st.table(passenger_results)

        # Jeepney Stopped Probability
        stopped_results = pd.DataFrame({
            "Stopped Status": ["Stopped" if index == 1 else "Not Stopped" for index in stopped_prob.index],
            "Probability": stopped_prob.values
        })
        st.write("**Jeepney Stopped Probability:**")
        st.table(stopped_results)

    # Tab 2: Simulation Results
    with tab2:
        st.subheader("Simulation Results")

        # Simulation Table
        st.write("**Detailed Replication Results:**")
        st.dataframe(results_df)

        # Simulation Metrics
        st.write("**Aggregate Metrics:**")
        st.write(f"Total Customers Arrived: {metrics['Total Customers Arrived']}")
        st.write(f"Total Customers Served: {metrics['Total Customers Served']}")
        st.write(f"Total Customers Reneged: {metrics['Total Customers Reneged']}")
        st.write(f"Reneging Rate: {metrics['Reneging Rate']:.2%}")
        st.write(f"Total Jeepneys Arrived: {metrics['Total Jeepneys Arrived']}")
        st.write(f"Jeepney Utilization Rate: {metrics['Jeepney Utilization Rate']:.2%}")

if __name__ == "__main__":
    main()