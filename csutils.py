from datetime import datetime, timedelta
from wsgiref import validate
import numpy as np
import json
from csv import reader, writer
import random

# TODO: make a new update sign maybe, update the site, finish scraping!
# TODO: SWAP DAILY AND / ROEAIJLAFKJLS

split = '///'
price_json = 'updated_prices.json'

# # get day and then daily skin
# def getToday():
#     return str(datetime.date(datetime.now() - timedelta(hours=10)))

def getItemsJson():
    items_js = open(price_json, encoding='utf-8')
    items = json.load(items_js)
    return items

def getDayCount():
    return (datetime.now() - timedelta(hours=10) - datetime(2024, 7, 14)).days
    # # inception day = 03.14.2022
    # # this is day x after today - inception
    # today = getToday()
    # items = np.recfromcsv('daily.csv', encoding='utf-8')
    # return list(items['date']).index(today)

def get_skin(daily=False):
    if daily:
        day_count = getDayCount() + 1
        dailies = np.genfromtxt('daily_random.csv', encoding='utf-8', delimiter=',', dtype=None)
        updated_prices = open(price_json, encoding='utf-8')
        items = json.load(updated_prices)
        updated_prices.close()
        for row in reversed(range(dailies.size)):
            curr = dailies[row]
            if (curr[0] == day_count):
                return curr[1] + split + curr[2]
        max_rolls = 50
        history_check = 180
        min_avg_value = 25
        prev_dailies = [str(item[1]) for item in dailies if abs(day_count - item[0] <= history_check)]
        floor_price_items = [item for item in items if items[item]['avg_price'] >= min_avg_value]
        random.seed(day_count)
        rando_item_name = random.choice(floor_price_items)
        for i in range(max_rolls):
            if (rando_item_name in prev_dailies):
                rando_item_name = random.choice(floor_price_items)
            else: break
        rando_item = items[rando_item_name]
        random_condition = list(rando_item['exterior'].keys())[random.randrange(len(rando_item['exterior'].keys()))]
        # with open('daily_random.csv', 'a', encoding='UTF8', newline='') as f:
        #     dwriter = writer(f, lineterminator='\n')
        #     dwriter.writerow([day_count, rando_item_name, random_condition])
        with open('daily_random.csv', 'a', encoding='UTF8') as f:
            dwriter = writer(f, lineterminator='\n')
            dwriter.writerow([day_count, rando_item_name, random_condition])
        return rando_item_name + split + random_condition

        # items = np.recfromcsv('daily.csv', encoding='utf-8')
        # # date, skin, condition
        # row = items[items['date'] == today]
        # secret_skin = row['skin'][0]
        # secret_condition = row['condition'][0]
        # # combine the two but make it easy to split
        # secret = secret_skin + split + secret_condition
        # return secret
    else:
        # Generate a random skin and random condition
        items = getItemsJson()
        rnd_skin_index = np.random.randint(0, len(items))
        skin_key = list(items)[rnd_skin_index]
        rnd_exterior = np.random.randint(0, len(items[skin_key]['exterior']))
        skin_exterior = list(items[skin_key]['exterior'])[rnd_exterior]
        secret = skin_key + split + skin_exterior
        return secret

# # Validates daily.csv
# def validate_daily():
#     items_js = open(price_json, encoding='utf-8')
#     items = json.load(items_js)
#     with open('daily.csv', 'r') as read_obj:
#         csv_reader = reader(read_obj)
#         for row in csv_reader:
#             if row[0] != 'date':
#                 # print(row)
#                 # print(row[1], row[2])
#                 if row[1] not in items:
#                     print("issue with finding skin:", row[1], row[2])
#                 elif row[2] not in items[row[1]]['exterior']:
#                     print('issue with exterior', row[1],row[2])

# validate_daily()

# # Generates random valid conditions of inputted skins
# def random_condition_daily():
#     items_js = open(price_json, encoding='utf-8')
#     items = json.load(items_js)
#     with open('dl_daily.csv', 'r') as read_obj:
#         with open('daily.csv', 'w', newline='', encoding='utf-8') as f:
#             wr = writer(f)
#             csv_reader = reader(read_obj)
#             for row in csv_reader:
#                 if row[0] == 'date':
#                     wr.writerow(row)
#                 elif row[1] != '':
#                     skin_name = row[1]
#                     random_condition_index = np.random.randint(0, len(items[skin_name]['exterior']))
#                     random_condition = list(items[skin_name]['exterior'])[random_condition_index]
#                     wr.writerow([row[0], skin_name, random_condition])
#     items_js.close()