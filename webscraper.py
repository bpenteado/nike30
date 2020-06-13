from bs4 import BeautifulSoup
from selenium import webdriver


def retrieve_current_deals(websites):

	# scrape websites
	retrieved_deals = []
	content = scrape_websites(websites)

	# retrieve deals from each website
	for website, content in content.items():
		if website == "Running Warehouse":
			retrieved_deals += retrieve_rw(content)

	return retrieved_deals


def scrape_websites(websites):

	# initialize webdriver
	options = webdriver.firefox.options.Options()
	options.headless = True
	driver = webdriver.Firefox(options=options)

	content_dict = {}
	for website, url in websites.items():
		driver.get(url)
		source = driver.page_source
		content = BeautifulSoup(source, "html.parser")
		content_dict.update({website: content})

	driver.quit()
	return content_dict


def retrieve_rw(content):

	# extract all deals
	deal_content = content.findAll('div', attrs={"class": "product_wrapper cf gtm_impression"})

	# extract name, link, sizing, and pricing information from each deal
	deals = []
	for deal in deal_content:

		# extract shoe name and link
		shoe = deal.find('div', attrs={"class":"name"})
		shoe_name = shoe.text
		shoe_link = shoe.find('a')['href']

		# extract sizing information
		sizes_tag = deal.find('span', attrs={"class": "sizes"})
		sizes = sizes_tag.text if sizes_tag is not None else "All"

		# extract sale pricing information
		pricing_tag = deal.find('span', attrs={"class": "pricing"})
		sale_price = pricing_tag.find('span', attrs={"class": "sale"})  # sale price class seems to change in RW
		if sale_price:
			sale_price = float(sale_price.text[1:])
		else:
			sale_price = float(pricing_tag.find('span', attrs={"class": "price"}).text[1:])

		# extract initial pricing information
		initial_price = pricing_tag.find('span', attrs={"class": "list strike"}) # initial price sometimes not available in RW
		if initial_price:
			initial_price = float(pricing_tag.find('span', attrs={"class": "list strike"}).text[1:])
		else:
			initial_price = sale_price

		# store shoe information
		new_deal = {
			"shoeName": shoe_name,
			"shoeLink": shoe_link,
			"sizes": sizes,
			"salePrice": sale_price,
			"initialPrice": initial_price
		}

		deals += [new_deal]

	return deals
