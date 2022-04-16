import json
'''
We want to take processed_items.json and update with results.json
'''
def truncate(n, decimals=0):
                    multiplier = 10 ** decimals
                    return int(n * multiplier) / multiplier
op = open('processed_items.json', encoding='utf-8')
old_prices = json.load(op)
up = open('results.json', encoding='utf-8')
updated_prices = json.load(up)
new_json = old_prices
# Go through each item
for item in old_prices:
    num_ext = 0
    total_price = 0
    highest_price = 0
    for ext in old_prices[item]['exterior']:
        updated_price = 0
        # Low volume items may not have prices
        try:
            updated_price = updated_prices[item][ext]
        except:
            updated_price = old_prices[item]['exterior'][ext]['price']
            print('issue with ' + item + ' | ' + ext)
        if updated_price > highest_price:
            highest_price = updated_price
        num_ext += 1
        total_price += updated_price
        new_json[item]['exterior'][ext]['price'] = updated_price
    avg_price = truncate(total_price/num_ext, 2)
    new_json[item]['avg_price'] = avg_price
    new_json[item]['highest_price'] = highest_price

with open('updated_prices.json', 'w') as outfile:
    print('dumping into updated_prices.json')
    json.dump(new_json, outfile)
print('finished updating')