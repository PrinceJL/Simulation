import simpy
import random
import pandas as pd

# -- Configuration --
MAX_CAPACITY = 30  # default jeepney capacity if not specified

# Convert time string ("MM:SS") to seconds
def time_to_seconds(time_str):
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60  # Convert to seconds
    except ValueError:
        print(f"Invalid time format: {time_str}")
        return 0  # or handle it differently as needed
# Simulation logic
def simulate_gate2(env, customer_data, jeepney_data, log_list):
    queue = []  # waiting customers

    def customer_generator():
        for i, row in customer_data.iterrows():
            yield env.timeout(time_to_seconds(row['Arrival Time based on previous']))
            for j in range(int(row['No of Customer Arrived'])):
                cust = {
                    "id": f"Cust_{i}_{j}",
                    "arrival_time": env.now,
                    "patience": random.uniform(100, 300)
                }
                queue.append(cust)
                log_list.append(f"[{env.now:.0f}s] {cust['id']} joins queue")

    def jeepney_generator():
        for i, row in jeepney_data.iterrows():
            interarrival = row['Interarrival in mins']
            if pd.isna(interarrival):
                delay = 0
            else:
                delay = int(interarrival) * 60
            yield env.timeout(delay)

            jeep_id = row['Jeepney Plate']
            arrives_empty = int(row.get('Jeepney arrived without passengers onboard', 1))
            onboard_capacity = MAX_CAPACITY if arrives_empty else random.randint(0, MAX_CAPACITY - 5)
            can_board = MAX_CAPACITY - onboard_capacity

            boarded = 0
            while queue and can_board > 0:
                cust = queue.pop(0)
                boarded += 1
                can_board -= 1
                log_list.append(f"[{env.now:.0f}s] {cust['id']} boards {jeep_id}")

            log_list.append(f"[{env.now:.0f}s] {jeep_id} departs with {boarded} customers")

    env.process(customer_generator())
    env.process(jeepney_generator())
    env.run()