import pandas as pd
import numpy as np
from datetime import timedelta

def generate_jeepney_data(num_jeeps=30, seed=42):
    np.random.seed(seed)
    data = []
    time_now = timedelta(minutes=0)
    jeep_capacity = 20  # Assume 20 seats per jeep

    for i in range(num_jeeps):
        interarrival = np.random.randint(5, 15)
        time_now += timedelta(minutes=interarrival)
        passengers = np.random.randint(5, jeep_capacity + 1)
        onboard = np.random.choice([0, 1])
        stopped = np.random.choice([0, 1])
        not_stopped = 1 - stopped
        utilization = passengers / jeep_capacity

        data.append([
            f"J{i+1:02d}", interarrival, str(time_now)[:-3],
            str(time_now + timedelta(minutes=2))[:-3],
            passengers, onboard, stopped, not_stopped, round(utilization, 2)
        ])

    return pd.DataFrame(data, columns=[
        "Plate Number", "Interarrival in mins", "Time Arrived", "Time Departed",
        "Number of Passengers Boarded", "Jeepney arrived without passengers onboard",
        "Jeepney came from phase 3 but stopped", "Jeepney came from phase 3 but did not stop",
        "Utilization"
    ])
