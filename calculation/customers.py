import numpy as np
import pandas as pd

# Load the customer data
data = pd.read_csv("https://docs.google.com/spreadsheets/d/1q5VdeoHnj1UMFGm781BDCEsNcWncX72UOlDOQrKTEgY/export?format=csv&gid=0")

df_base = pd.DataFrame(data)

# Get distributions
customer_arrived_probs = df_base['No of Customer Arrived'].value_counts(normalize=True).sort_index()
reneged_diff = df_base['No of Customer Arrived'] - df_base['No of Reneged']
reneged_ratio = (df_base['No of Reneged'] / df_base['No of Customer Arrived']).fillna(0)

# Summary stats
print("Customer Arrival Distribution:\n", customer_arrived_probs)
print("\nReneging Rate (mean ± std):", reneged_ratio.mean(), "±", reneged_ratio.std())

# Simulate 50 groups based on real data distribution
num_groups = 50
sim_df = pd.DataFrame({
    'Commuting Group': [f'C{i+1}' for i in range(num_groups)]
})

# Reuse minutes_to_time_str
def minutes_to_time_str(minutes):
    h = int(minutes // 60)
    m = int(minutes % 60)
    return f"{h:02}:{m:02}"

arrival_minutes_list = []
np.random.seed(42)  # For reproducibility

for i in range(num_groups):
    # Random arrival time
    arrival_time = np.random.uniform(0, 180)
    arrival_minutes_list.append(arrival_time)
    sim_df.loc[i, 'Arrival Time (mins)'] = minutes_to_time_str(arrival_time)

    # Sample number of arrivals using actual distribution
    customer_arrival_choices = customer_arrived_probs.index.tolist()
    customer_arrival_weights = customer_arrived_probs.values
    num_customers = np.random.choice(customer_arrival_choices, p=customer_arrival_weights)
    sim_df.loc[i, 'No of Customer Arrived'] = num_customers

    # Reneging based on empirical mean rate
    reneging_rate = reneged_ratio.mean()
    expected_renegers = int(np.round(num_customers * reneging_rate))
    expected_renegers = min(expected_renegers, num_customers)
    sim_df.loc[i, 'No of Reneged'] = expected_renegers

# Convert to integers
sim_df['No of Customer Arrived'] = sim_df['No of Customer Arrived'].astype(int)
sim_df['No of Reneged'] = sim_df['No of Reneged'].astype(int)

# Recompute stats
arrival_minutes_series = pd.Series(arrival_minutes_list)
mean_arrival = arrival_minutes_series.mean()
std_arrival = arrival_minutes_series.std()
var_arrival = std_arrival ** 2

print(sim_df)

print("\nArrival Time Statistics:")
print(f"Mean Arrival Time: {int(mean_arrival // 60)}:{int(mean_arrival % 60):02} mins")
print(f"Standard Deviation: {int(std_arrival // 60)}:{int(std_arrival % 60):02} mins")
print(f"Variance: {var_arrival:.2f} mins^2")
