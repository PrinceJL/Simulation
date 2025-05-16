import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data (replace this with your actual data load step)
data = pd.read_csv("https://docs.google.com/spreadsheets/d/1cCjvCal_UaPfWVN5YUhrryQBTmOMEXBfK_sb55X0pJQ/edit?usp=sharing")

df_jeepney = pd.DataFrame(data)

# Function to convert time in MM:SS format to minutes
def convert_to_minutes(time_str):
    mins, secs = map(int, time_str.split(':'))
    return mins + secs / 60

# Apply conversion to 'Interarrival in mins', 'Time Arrived', and 'Time Departed'
df_jeepney['Interarrival in mins'] = df_jeepney['Interarrival in mins'].apply(convert_to_minutes)
df_jeepney['Time Arrived'] = df_jeepney['Time Arrived'].apply(convert_to_minutes)
df_jeepney['Time Departed'] = df_jeepney['Time Departed'].apply(convert_to_minutes)

# 1. Interarrival Time Distribution (probability table)
interarrival_hist, interarrival_bins = np.histogram(df_jeepney['Interarrival in mins'], bins=5, density=True)
interarrival_prob = interarrival_hist / interarrival_hist.sum()  # Normalize to get probability

# 2. Number of Passengers Distribution (probability table)
passenger_hist, passenger_bins = np.histogram(df_jeepney['Number of Passengers Boarded'], bins=5, density=True)
passenger_prob = passenger_hist / passenger_hist.sum()  # Normalize to get probability

# 3. Jeepney Stopped Distribution (probability table)
stopped_prob = df_jeepney['Jeepney came from phase 3 but stopped'].value_counts(normalize=True).sort_index()

# Printing the probability tables

# Interarrival Time Distribution
print("\nInterarrival Time Distribution (probabilities):")
for i in range(len(interarrival_prob)):
    print(f"From {interarrival_bins[i]:.2f} to {interarrival_bins[i+1]:.2f} minutes: Probability = {interarrival_prob[i]:.4f}")

# Passenger Boarding Distribution
print("\nPassenger Boarding Distribution (probabilities):")
for i in range(len(passenger_prob)):
    print(f"From {passenger_bins[i]} to {passenger_bins[i+1]} passengers: Probability = {passenger_prob[i]:.4f}")

# Jeepney Stopped Probability
print("\nJeepney Stopped Probability:")
for stopped_value, prob in stopped_prob.items():
    stopped_status = "Stopped" if stopped_value == 1 else "Not Stopped"
    print(f"Probability of Jeepney {stopped_status}: {prob:.4f}")
