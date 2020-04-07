from bs4 import BeautifulSoup
from selenium import webdriver
import json

# initialize webdriver
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options = options)
driver.get('https://www.runningwarehouse.com/catpage-SALEMS.html')

# scrape website
url = driver.page_source
content = BeautifulSoup(url, "html.parser")

# extract all deals
deals = content.findAll('div', attrs={"class": "product_wrapper cf gtm_impression"})

# extract name, link, sizing, and pricing information from each deal
deal_arr = []
for deal in deals:

	# extract shoe name and link
	shoe = deal.find('div', attrs={"class":"name"})
	shoe_name = shoe.text
	shoe_link = shoe.find('a')['href']

	# extract sizing information
	sizes_tag = deal.find('span', attrs={"class":"sizes"})
	sizes = sizes_tag.text if sizes_tag is not None else "All"

	# extract pricing information
	pricing_tag = deal.find('span', attrs={"class": "pricing"})
	sale_price = pricing_tag.find('span', attrs={"class": "sale"}) # sale price class seems to change in Running Warehouse
	if sale_price:
		sale_price = float(sale_price.text[1:])
	else:
		sale_price = float(pricing_tag.find('span', attrs={"class": "price"}).text[1:])
	initial_price = float(pricing_tag.find('span', attrs={"class": "list strike"}).text[1:])

	# store shoe information
	new_deal = {
		"shoeName": shoe_name,
		"shoeLink": shoe_link,
		"sizes": sizes,
		"salePrice": sale_price,
		"initialPrice": initial_price
	}

	deal_arr += [new_deal]

# store data in JSON format
with open('currentDeals.json', 'w') as outfile:
	json.dump(deal_arr, outfile)

driver.quit()
