from datetime import datetime, timedelta
import numpy as np
import json
from csv import reader, writer

split = '///'

# get day and then daily skin
def get_today():
    today = str(datetime.date(datetime.now() - timedelta(hours=10)))
    return today

def get_items_json():
    items_js = open('processed_items.json', encoding='utf-8')
    items = json.load(items_js)
    items_js.close()
    return items

def get_day_count():
    today = get_today()
    items = np.recfromcsv('daily.csv', encoding='utf-8')
    return list(items['date']).index(today)

def get_skin(daily=False):
    if daily:
        today = get_today()
        items = np.recfromcsv('daily.csv', encoding='utf-8')
        # date, skin, condition
        row = items[items['date'] == today]
        secret_skin = row['skin'][0]
        secret_condition = row['condition'][0]
        # combine the two but make it easy to split
        secret = secret_skin + split + secret_condition
        return secret
    else:
        # Generate a random skin and random condition
        items = get_items_json()
        rnd_skin_index = np.random.randint(0, len(items))
        skin_key = list(items)[rnd_skin_index]
        rnd_exterior = np.random.randint(0, len(items[skin_key]['exterior']))
        skin_exterior = list(items[skin_key]['exterior'])[rnd_exterior]
        secret = skin_key + split + skin_exterior
        return secret

# # Generates random valid conditions of inputted skins
# def random_condition_daily():
#     items_js = open('processed_items.json', encoding='utf-8')
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

# random_condition_daily()