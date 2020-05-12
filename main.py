from webscraper import retrieve_current_deals
from dataparser import filter_new_deals, filter_deals, generate_email_body
import json
import smtplib

# parameters
websites = {"Running Warehouse": 'https://www.runningwarehouse.com/catpage-SALEMS.html'}
min_discount = 0.3
valid_sizes = ['M9.5', 'M9.0', '9.5 D', '9.0 D']

# scrape websites
current_deals = retrieve_current_deals(websites)

# store data in JSON format
with open('/Users/bernardopenteado/Desktop/Projects/Nike30%/currentDeals.json', 'w') as outfile:
    json.dump(current_deals, outfile)

# parse data (retrieve relevant new deals)
with open('/Users/bernardopenteado//Desktop/Projects/Nike30%/oldDeals.json') as data:  # pull all old deals from website
    old_deals = json.load(data)
new_deals = filter_new_deals(current_deals, old_deals)  # check for new deals
filtered_new_deals = filter_deals(new_deals, min_discount, valid_sizes)  # filter new deals according to params

# if there are relevant new deals, filter deals and send email
if filtered_new_deals:
    # set up SMTP connection
    conn = smtplib.SMTP('smtp.gmail.com', 587)
    conn.ehlo()
    conn.starttls()
    conn.login('bernardopbf3@gmail.com', 'ksnczdktlbwzajzl')

    # create email message
    message = generate_email_body(filtered_new_deals)

    # send email
    conn.sendmail('bernardopbf3@gmail.com', ['bernardopbf3@gmail.com'], message)
    conn.quit()

# update old deals with current_deals
with open('/Users/bernardopenteado//Desktop/Projects/Nike30%/oldDeals.json', 'w') as data:
    json.dump(current_deals, data)

print("OK")