import pandas as pd
import numpy as np

def customer_simulation():
    # Load the customer data
    data = pd.read_csv("https://docs.google.com/spreadsheets/d/1q5VdeoHnj1UMFGm781BDCEsNcWncX72UOlDOQrKTEgY/export?format=csv&gid=0")
    df_base = pd.DataFrame(data)

    # Get distributions
    customer_arrived_probs = df_base['No of Customer Arrived'].value_counts(normalize=True).sort_index()
    reneged_ratio = (df_base['No of Reneged'] / df_base['No of Customer Arrived']).fillna(0)

    return customer_arrived_probs, reneged_ratio