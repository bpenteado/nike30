from webscraper import retrieve_deals

# scrape websites

websites = {
    "Running Warehouse": 'https://www.runningwarehouse.com/catpage-SALEMS.html'
}

current_deals = retrieve_deals(websites)

# store data in JSON format
with open('currentDeals.json', 'w') as outfile:
    json.dump(current_deals, outfile)
