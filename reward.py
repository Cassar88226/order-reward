import datetime
import json
from dateutil.parser import parse
import numpy as np


def calc_reward(amount, timestamp):
    date_time_obj = parse(timestamp)
    ttime = date_time_obj.time()

    reward = 0
    if ttime > datetime.time(12,0) and ttime <= datetime.time(13,0):
        reward = amount / 3
    elif (ttime > datetime.time(11,0) and ttime <= datetime.time(12,0)) or \
        (ttime > datetime.time(13,0) and ttime <= datetime.time(14,0)):
        reward = amount / 2
    elif (ttime > datetime.time(10,0) and ttime <= datetime.time(11,0)) or \
        (ttime > datetime.time(14,0) and ttime <= datetime.time(15,0)):
        reward = amount
    else:
        reward = amount * 4
    return reward

with open('example (2).json') as f:
    events = json.load(f)

customers = []
orders = []
order_cnts = []
for event in events["events"]:
    if event["action"] == "new_customer" and event["name"] not in customers:
        customers.append(event["name"])
order_cnts = [0] * len(customers)
orders = [0] * len(customers)
for event in events["events"]:
    if event["action"] == "new_order" and event["customer"] in customers:
        # get index of customer
        index = customers.index(event["customer"])
        orders[index] += calc_reward(event["amount"], event["timestamp"])
        order_cnts[index] += 1

orders = [round(x) for x in orders]


index_list = np.argsort(-np.array(orders))
for index in index_list:
    try:
        average = orders[index]/order_cnts[index]
    except ZeroDivisionError:
        average = 0
    print(customers[index] + " : " + str(orders[index]) + " points with " + str(average) + " points per order")
