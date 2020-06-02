from webscraper import retrieve_current_deals
from dataparser import filter_new_deals, filter_deals, generate_email_body
import json
import smtplib

# parameters
websites = {"Running Warehouse": 'https://www.runningwarehouse.com/catpage-SALEMS.html'}
min_discount = 0.3
valid_sizes = ['M9.5', 'M9.0', '9.5 D', '9.0 D']
gecko_exe_path = "/Users/bernardopenteado/.envs/nike30/geckodriver.exe"
gecko_log_path = "/Users/bernardopenteado/.envs/nike30/geckodriver.log"
current_deals_path = '/Users/bernardopenteado/Desktop/Projects/Nike30%/currentDeals.json'
old_deals_path = '/Users/bernardopenteado/Desktop/Projects/Nike30%/oldDeals.json'
email_login = 'bernardopbf3@gmail.com'
email_pass = 'ksnczdktlbwzajzl'
smtp_host = 'smtp.gmail.com'
smtp_port = 587

# scrape websites
current_deals = retrieve_current_deals(websites, gecko_exe_path, gecko_log_path)

# store data in JSON format
with open(current_deals_path, 'w') as outfile:
    json.dump(current_deals, outfile)

# parse data (retrieve relevant new deals)
with open(old_deals_path) as data:  # pull all old deals from website
    old_deals = json.load(data)
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

print("OK")