# Validates daily.csv
import json
from csv import reader
import numpy as np

price_json = 'updated_prices.json'

def validate_daily():
    items_js = open(price_json, encoding='utf-8')
    items = json.load(items_js)
    dailies = np.genfromtxt('daily_random.csv', encoding='utf-8', delimiter=',', dtype=None)
    for i in range(dailies.size):
        row = dailies[i]
        if row[0]:
            print(row)
            # print(row[1], row[2])
            if row[1] not in items:
                print("issue with finding skin:", row[1], row[2])
            elif row[2] not in items[row[1]]['exterior']:
                print('issue with exterior', row[1],row[2])
    

    print('finished validating')

validate_daily()