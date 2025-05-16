import pandas as pd
import numpy as np

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