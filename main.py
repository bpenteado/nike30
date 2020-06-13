from webscraper import retrieve_current_deals
from dataparser import filter_new_deals, filter_deals, generate_email_body
import json
import smtplib
import os

# default parameters
current_dir = os.path.dirname(os.path.abspath(__file__))
websites = {"Running Warehouse": 'https://www.runningwarehouse.com/catpage-SALEMS.html'}
current_deals_path = current_dir + '/currentDeals.json'
old_deals_path = current_dir + '/oldDeals.json'
params_path = current_dir + '/params.json'

# parse JSON with user parameters
with open(params_path, 'r') as file:
    user_params = json.load(file)

# set preferences
user_preferences = user_params["preferences"]
min_discount = user_preferences["minDiscount"]
user_sex = user_preferences["userSex"]
user_sizes = user_preferences["userSizes"]

# set SMTP parameters
user_smtp = user_params["smtpParams"]
email_login = user_smtp["login"]
email_pass = user_smtp["pass"]
smtp_host = user_smtp["host"]
smtp_port = user_smtp["port"]

# # determine valid sizes on RW based on user sex and sizes
valid_sizes = []
for size in user_sizes:
    valid_sizes += [user_sex + size]
    valid_sizes += [size + " D"]

# scrape websites
current_deals = retrieve_current_deals(websites)

# store data in JSON format
with open(current_deals_path, 'w') as outfile:
    json.dump(current_deals, outfile)

# parse data (retrieve relevant new deals)
if os.path.isfile(old_deals_path):
    with open(old_deals_path) as data:  # pull all old deals from website
        old_deals = json.load(data)
else:
    old_deals = []
    with open(old_deals_path, 'w') as outfile:  # create old deals tracker
        json.dump(old_deals, outfile)
new_deals = filter_new_deals(current_deals, old_deals)  # check for new deals
filtered_new_deals = filter_deals(new_deals, min_discount, valid_sizes)  # filter new deals according to params

# if there are relevant new deals, filter deals and send email
if filtered_new_deals:
    # set up SMTP connection
    conn = smtplib.SMTP(smtp_host, smtp_port)
    conn.ehlo()
    conn.starttls()
    conn.login(email_login, email_pass)

    # create email message
    message = generate_email_body(filtered_new_deals)

    # send email
    conn.sendmail(email_login, [email_login], message)
    conn.quit()

# update old deals with current_deals
with open(old_deals_path, 'w') as data:
    json.dump(current_deals, data)
