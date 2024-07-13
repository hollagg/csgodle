# Given prices scraped in results.json and giant list of items via webapi.json, return updated_prices.json
import json

f = open("webapi.json")
webapi = json.load(f)
d = open('results.json')
scraped_prices = json.load(d)

def getPrice(skin):
    skin_split = skin.split('(')
    cond = skin_split.pop().replace(')', '')
    skin_name = '('.join(skin_split).strip()
    # print(cond, skin_name)
    # given skin in str return price
    for item in scraped_prices:
        if (item == skin_name):
            # print('@@@', skin)
            if (cond in scraped_prices[item]):
                return scraped_prices[item][cond]
            print('item found but not price at condition', skin_name, cond)
            return -1
    
    print('not found at all', skin)
    return -1

items_list = [
    'cz75-auto', 'desert-eagle', 'dual-berettas', 'five-seven', 'glock-18', 'p2000', 'p250', 'r8-revolver', 'tec-9', 'usp-s',
    'ak-47', 'aug', 'famas', 'galil-ar', 'm4a1-s', 'm4a4', 'sg-553', 'awp', 'g3sg1', 'scar-20', 'ssg-08',
    'mac-10', 'mp5-sd', 'mp7', 'mp9', 'p90', 'pp-bizon', 'ump-45',
    'mag-7', 'nova', 'sawed-off', 'xm1014', 'm249', 'negev'
    ]

weapon_categories = {
    'Pistols': [
        'cz75-auto', 'desert eagle', 'dual berettas', 'five-seven', 'glock-18', 'p2000', 'p250', 'r8 revolver', 'tec-9', 'usp-s', 'desert-eagle', 'dual-berettas', 'r8-revolver'
    ],
    'Rifles': [
        'ak-47', 'awp', 'aug', 'famas', 'g3sg1', 'galil ar', 'm4a1-s', 'm4a4', 'scar-20', 'sg 553', 'ssg 08', 'ssg-08', 'galil-ar', 'sg-553'
    ],
    'SMGs': [
        'mac-10', 'mp5-sd', 'mp7', 'mp9', 'pp-bizon', 'p90', 'ump-45'
    ],
    'Heavy': [
        'mag-7', 'nova', 'sawed-off', 'xm1014', 'm249', 'negev'
    ],
    'Knives': [
        'nomad knife', 'skeleton knife', 'survival knife', 'paracord knife', 'classic knife', 'bayonet', 'bowie knife',
            'butterfly knife', 'falchion knife', 'flip knife', 'gut knife', 'huntsman knife', 'karambit', 'm9 bayonet',
            'navaja knife', 'shadow daggers', 'stiletto knife', 'talon knife', 'ursus knife'
    ]
}

def getCategory(w):
    for category, l in weapon_categories.items():
        if w in l:
            return category
    print ('failed to find category for', w)
    return -1

# itemgroup !=
# ignore_list = ['sticker', 'patch', 'graffiti', 'container', 'strange', 'tournament']
ignore_list = ['sticker', 'patch', 'graffiti', 'container']

# processed_items = {}
# price_info = {}
# # maybe do for everything in results first, then backfill
# for w in webapi:
#     for g in items_list:
#         if (g in w['slug'] and w['quality'] not in ignore_list and w['itemgroup'] not in ignore_list):
#             skin = w['markethashname']
#             skin_split = skin.split('(')
#             cond = skin_split.pop().replace(')', '')
#             skin_name = '('.join(skin_split).strip()
#             # print(w)
#             if (skin_name not in processed_items):
#                 processed_items[skin_name] = {
#                     'rarity': w['rarity'].title(),
#                     'rarity_color': w['color'],
#                     'weapon_class': skin_name.split('|')[0].strip(),
#                     'weapon_category': getCategory(w['itemtype']),
#                     'exterior': {},
#                     'highest_price': 0
#                 }
#                 price_info[skin_name] = {
#                     'total': 0,
#                     'count': 0
#                 }

#             skin_price = getPrice(skin)
#             if (skin_price) == -1:
#                 skin_price = w['pricereal']
#             processed_items[skin_name]['exterior'][cond] = {
#                 'price': skin_price,
#                 'url': w['itemimage'],
#             }
#             if (skin_price > processed_items[skin_name]['highest_price']):
#                 processed_items[skin_name]['highest_price'] = skin_price

#             price_info[skin_name]['total'] = price_info[skin_name]['total'] + skin_price
#             price_info[skin_name]['count'] = price_info[skin_name]['count'] + 1
#             break

# for i in processed_items:
#     processed_items[i]['avg_price'] = round(price_info[i]['total'] / price_info[i]['count'], 2)

# with open('updated_prices.json', 'w') as outfile:
#     json.dump(processed_items, outfile, sort_keys=True)

processed_items = {}
price_info = {}
name_ignore = [
    'Souvenir', 'Sealed Graffiti', 'Sticker', 'Patch', 'StatTrak™', 'X-Ray P250 Package', 'Doodle Lore', 'M4A4 | Emperor'
    ]
for w in webapi:
    ignore = False
    for n in name_ignore:
        if (n in w['markethashname']):
            ignore = True
            break
    if (w['isstattrack'] or w['isstar'] or ignore):
            continue
    for g in items_list:
        if (g in w['slug'] and
            (getPrice(w['markethashname']) or
            (w['quality'] == 'normal' and w['itemgroup'] not in ignore_list))):
            skin_price = getPrice(w['markethashname'])
            if (skin_price == -1):
                skin_price = w['pricereal']
            if (skin_price == 0):
                skin_price = w['pricereal24h']
            skin = w['markethashname']
            skin_split = skin.split('(')
            cond = skin_split.pop().replace(')', '')
            skin_name = '('.join(skin_split).strip()
            if (skin_name not in processed_items):
                processed_items[skin_name] = {
                    'exterior': {},
                    'weapon_class': skin_name.split('|')[0].strip(),
                    'highest_price': 0
                }
                price_info[skin_name] = {
                    'total': 0,
                    'count': 0
                }
            processed_items[skin_name]['exterior'][cond] = {
                'price': skin_price,
                'url': w['itemimage']
            }

            if (w['rarity']):
                processed_items[skin_name]['rarity'] = w['rarity'].title()

            if (w['color']):
                processed_items[skin_name]['rarity_color'] = w['color']
            processed_items[skin_name]['weapon_category'] = getCategory(g)
            if (skin_price > processed_items[skin_name]['highest_price']):
                processed_items[skin_name]['highest_price'] = skin_price

            price_info[skin_name]['total'] = price_info[skin_name]['total'] + skin_price
            price_info[skin_name]['count'] = price_info[skin_name]['count'] + 1

# manually add inheritance zzz
processed_items['AK-47 | Inheritance']['rarity_color'] = 'eb4b4b'
processed_items['AK-47 | Inheritance']['rarity'] = 'Covert'

for i in processed_items:
    if ('rarity_color' not in processed_items[i].keys()):
        print('123 issue with', i)
    processed_items[i]['avg_price'] = round(price_info[i]['total'] / price_info[i]['count'], 2)

with open('updated_prices.json', 'w') as outfile:
    json.dump(processed_items, outfile, sort_keys=True)
# count = 0
# for item in items_list:
#     for i in webapi:
#         if(item in i['slug'] and i['quality'] == 'normal' and i['itemgroup'] not in ignore_list):

#             # 'Desert Eagle | Sunset Storm \u58f1'
#             if(getPrice(i['markethashname'])) == -1:
#                 print('failed to fetch', i['marketname'], i['itemgroup'])
#                 print(i)
#             else:
#                 count += 1
# print(count, 'items in cs api')
# count = 0
# for i in scraped_prices:
#     count += len(scraped_prices[i].keys())
# print(count, 'prices in scraped_prices')


# color is built in, also a bordercolor
# color is rarity, bordercolor is if special statrak, unusual, souvenir
# can probably use itemgroup, try to ignore souv/stattrak
# quality: normal - tournament, strange, unusual avoids
"""
{
    'id': '026830b2-ae3e-48af-b27e-146551cd9992',
    'markethashname': 'Souvenir P250 | Drought (Factory New)',
    'marketname': 'Souvenir P250 | Drought (Factory New)',
    'slug': 'souvenir-p250-drought-factory-new',
    'color': 'b0c3d9',
    'bordercolor': 'ffd700',
    'pricelatest': 0.03,
    'pricelatestsell': 0.03,
    'priceupdatedat': '2024-07-01 10:40:22',
    'pricereal': 0.01,
    'pricerealcreatedat': '2024-06-06 23:07:39',
    'winLosspercentage': '66.67',
    'pricemedian': 0.05,
    'points': 0,
    'priceavg': 0.05,
    'pricemin': 0.03,
    'pricemax': 0.03,
    'pricereal24h': 0.01,
    'pricereal7d': 0.01,
    'pricereal30d': 0.01,
    'pricereal90d': 0.02,
    'pricerealchangepercent24h': 0,
    'pricerealchangepercent7d': 0,
    'pricerealchangepercent30d': 0,
    'pricerealchangepercent90d': -50,
    'buyorderprice': 0,
    'buyordermedian': 0,
    'buyorderavg': 0,
    'buyordervolume': None,
    'unstable': 0,
    'unstablereason': None,
    'offervolume': 15911,
    'sold24h': 489,
    'sold7d': 2226,
    'sold30d': 11038,
    'sold90d': 50351,
    'wear': 'fn',
    'itemgroup': 'pistol',
    'itemtype': 'p250',
    'itemname': 'drought',
    'rarity': 'consumer grade',
    'quality': 'tournament',
    'isstattrack': 0,
    'isstar': 0,
    'markettradablerestriction': 7,
    'updatedat': '2024-07-01 16:52:40',
    'itemimage': 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpopujwezhzw8zMdC5H_siJh4uem_vnDL_QgWVu5Mx2gv3--Y3nj1H6-xY6ZGD1IoXEewc5Z1rQrlPvk-fuhZG0vZzMy3Jj6HYg4nvanRO-0AYMMLL4kbEedA'
}
"""