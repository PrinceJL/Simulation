import simpy
import random

def to_seconds(tstr):
    m, s = map(int, tstr.split(":"))
    return m * 60 + s

def simulate(data, log_list):
    env = simpy.Environment()
    counter = simpy.Resource(env, capacity=1)

    def customer(env, name, counter, patience):
        arrival = env.now
        log_list.append({
            "Time": f"{env.now:.0f}s",
            "Commuter": name,
            "Action": "arrives"
        })

        with counter.request() as req:
            result = yield req | env.timeout(patience)
            if req in result:
                wait_time = env.now - arrival
                log_list.append({
                    "Time": f"{env.now:.0f}s",
                    "Commuter": name,
                    "Action": f"begins service after {wait_time:.0f}s"
                })
                yield env.timeout(random.uniform(30, 60))
                log_list.append({
                    "Time": f"{env.now:.0f}s",
                    "Commuter": name,
                    "Action": "leaves after service"
                })
            else:
                log_list.append({
                    "Time": f"{env.now:.0f}s",
                    "Commuter": name,
                    "Action": f"reneged after waiting {patience:.0f}s"
                })

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
