# Script to read the most recent json from csgobackpack API and bitskins API and generate a json of prices etc
import json
import re
import time
start_time = time.time()
# html because csgobackpack has &#39 and similar ascii
import html

weapon_categories = {
    'Pistols': [
        'cz75-auto', 'desert eagle', 'dual berettas', 'five-seven', 'glock-18', 'p2000', 'p250', 'r8 revolver', 'tec-9', 'usp-s'
    ],
    'Rifles': [
        'ak-47', 'awp', 'aug', 'famas', 'g3sg1', 'galil ar', 'm4a1-s', 'm4a4', 'scar-20', 'sg 553', 'ssg 08'
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

def get_bitskins_price(name, bitskins_prices):
    for item in bitskins_prices:
        if name == item['market_hash_name']:
            return float(item['price'])
    # If can't find return -1
    return -1

csgobackpack = open('csgobp_prices.json', encoding='utf-8')
csgobp_data = json.load(csgobackpack)
# csgobackpack api uses steam prices which have a limit, so things like dlore are listed at $0, need bitskins pricing
bitskins = open('bitskins_prices.json', encoding='utf-8')
bitskins_data = json.load(bitskins)
# 0 indexed, not by name
bitskins_prices = bitskins_data['prices']
# Fields are success, currency, timestamp, items_list
# Looking at items_list
items_list = csgobp_data['items_list']
# Dict of weapons, thinking of doing weapon name -> conditions containing prices per condition
# Example - weapons['Karambit | Fade']['Factory New'] = price, weapons[kara] = info
weapons = {}
"""
We want to loop through every weapon and search for:
Items with type weapon (no gloves or stickers etc)
Weapons that are not stattrak or souvenir (prices fluctuate too much and low supply)
"""
num_dict = 0
num_total = 0
# Base url for skin icons
url = 'http://cdn.steamcommunity.com/economy/image/'
for item in items_list:
    num_total += 1
    item_info = items_list[item]
    item_type = item_info['type']
    if item_type:
        # We do not want souvenirs or stattraks 
        if item_type.lower() == 'weapon' and 'souvenir' not in item_info and 'stattrak' not in item_info:
            item_name = html.unescape(item_info['name'])
            item_price = get_bitskins_price(item_name, bitskins_prices)
            if item_price == -1:
                # 2 issues involving csgobp, where man-o'-war is weird and presented as
                # Man-o#27-war OR man-o&#39-war, unescape handles the righthand one, other needs weird regex
                # print(item_name.encode('utf-8'))
                item_name = re.sub('%27', "'", item_name)
                if 'AWP | Man' in item_name:
                    item_price = get_bitskins_price(item_name, bitskins_prices)
                    print('Man-o-war handled')
                else:
                    try:
                        item_price = item_info['price']['all_time']['median']
                    except:
                        # There are some skins that just aren't high enough volume etc, -1 and can't do much about it
                        print(f'{item_name.encode("utf-8")} does not have a price on either site, staying with -1')
            # some item names have Japanese/Chinese chars in them, need to encode to print or switch locales
            # print(item_name_sanitized.encode('utf-8'), item_price)
            # Pistol, rifle, heavy, knife, etc
            # Knives have knife_type, guns have gun_type
            weapon_type = item_info['weapon_type']
            exterior = 'Not Painted'
            # Regex to get exterior quality
            if len(re.findall('\((.*?)\)', item_name)) > 0:
                exterior = re.findall('\((.*?)\)', item_name)[0]
            # after getting exterior, we can sanitize weapon name by removing exterior and star if in knife
            item_name_sanitized = item_name.replace('★ ', '')
            item_name_sanitized = re.sub(' \((.*?)\)', '', item_name_sanitized)

            # print(item_name_sanitized.encode('utf-8'))
            # Create dict
            if item_name_sanitized not in weapons:
                weapons[item_name_sanitized] = {}
            weapon_url = ''
            if item_info['icon_url_large']:
                weapon_url = url + item_info['icon_url_large']
            else:
                weapon_url = url + item_info['icon_url']
            rarity = item_info['rarity']
            rarity_color = item_info['rarity_color']
            # Either knife_type or gun_type so use generic
            weapon_class = ''
            if weapon_type.lower() == 'knife':
                weapon_class = item_info['knife_type']
            else:
                weapon_class = item_info['gun_type']
            weapon_category = ''
            for category in weapon_categories:
                if weapon_class.lower() in weapon_categories[category]:
                    weapon_category = category
                    break
            if weapon_category == '':
                print('Issue categorizing:', item_name)
            # We will avoid non painted aka vanilla knives for now for the sake of the game
            if exterior != 'Not Painted':
                weapons[item_name_sanitized][exterior] = {
                    'price': item_price,
                    'rarity': rarity,
                    'rarity_color': rarity_color,
                    'weapon_class': weapon_class,
                    'weapon_url': weapon_url,
                    'weapon_category': weapon_category
                }
                num_dict += 1
            
with open('processed_items.json', 'w') as outfile:
    json.dump(weapons, outfile)
print()
csgobackpack.close()
bitskins.close()
print(f'Took {time.time() - start_time} seconds to process {num_dict} skins from {num_total} items')