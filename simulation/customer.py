import pandas as pd
import numpy as np
from datetime import timedelta

def generate_customer_data(num_groups=50, seed=42):
    np.random.seed(seed)
    data = []

    for i in range(num_groups):
        arrival_minute = np.random.randint(0, 180)
        arrival_time = timedelta(minutes=arrival_minute)
        num_arrived = np.random.poisson(10)
        num_reneged = np.random.binomial(num_arrived, 0.1)

        # Simulate wait time for each group
        wait_time = np.random.normal(loc=5, scale=2)  # in minutes
        wait_time = max(0, wait_time)

        data.append([
            f"C{i+1}", str(arrival_time)[:-3], num_arrived,
            num_reneged, wait_time
        ])

    return pd.DataFrame(data, columns=[
        "Commuting Group", "Arrival Time (mins)",
        "No of Customer Arrived", "No of Reneged", "Avg Wait Time (mins)"
    ])
