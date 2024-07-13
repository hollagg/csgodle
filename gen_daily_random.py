import json
import datetime
import random
import csv
'''
Quick script to generate csv random skins of certain value threshold
'''
updated_prices = open('updated_prices.json', encoding='utf-8')
items = json.load(updated_prices)
# set min usd value of skin
min_value = 9

def swap(arr,a,b):
    print(a,b)
    tmp = arr[a]
    arr[a] = arr[b]
    arr[b] = tmp
    return arr

filtered_items = []
# create list of tuples (skin name, condition) where price of skin + condition is >= min_value
for item in items:
    curr = items[item]
    possible_conditions = []
    for condition in curr['exterior']:
        if curr['exterior'][condition]['price'] >= min_value:
            possible_conditions.append(condition)
    if len(possible_conditions) > 0:
        filtered_items.append((item, possible_conditions[random.randint(0,len(possible_conditions) - 1)]))
l = len(filtered_items)
start_date = datetime.datetime.strptime('10/04/22', '%m/%d/%y')
# randomize
left_index = 0
while left_index < l:
    r = random.randint(left_index, l - 1)
    filtered_items = swap(filtered_items, left_index, r)
    left_index += 1
header = ['date', 'skin', 'condition']
with open('random_daily.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for t in filtered_items:
        writer.writerow([str(start_date.date()), t[0], t[1]])
        start_date = start_date + datetime.timedelta(days=1)

print('finished randomizing, last day: ', start_date)
