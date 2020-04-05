import json
import smtplib
from textwrap import dedent


def select_new_deals(new_list, old_list):
    return [deal for deal in new_list if deal not in old_list]


def check_sizes(deal, valid_sizes):
    available_sizes = deal['sizes']
    return deal['sizes'] == "All" or any(size in available_sizes for size in valid_sizes)


def check_discount(deal, discount):
    sale_price = deal['salePrice']
    initial_price = deal['initialPrice']
    return sale_price / initial_price < (1 - discount)


def filter_deals(deal_list, min_discount, valid_sizes):
    filtered_deals = []
    for deal in deal_list:
        if check_sizes(deal, valid_sizes):
            if check_discount(deal, min_discount):
                filtered_deals += [deal]
    return filtered_deals


def generate_email_body(deal_list):
    n_deals = len(deal_list)
    message = f'There are {n_deals} new deals waiting for you!\n'
    for deal in deal_list:

        # create strings for deal message
        shoe_name = deal["shoeName"].replace('\n', '')
        shoe_discount = str(round((1 - deal["salePrice"] / deal["initialPrice"]) * 100)) + "%"
        shoe_price = "$" + str(deal["salePrice"])
        shoe_initial_price = "$" + str(deal["initialPrice"])
        shoe_link = deal["shoeLink"]

        # create deal message
        deal_message = f"""
                        Shoe Model: {shoe_name}
                        Link: {shoe_link}
                        Price: {shoe_price}
                        Initial Price: {shoe_initial_price}
                        Discount: {shoe_discount}
                        """

        # add deal message to email body
        message += dedent(deal_message)

    return message


# pull all current deals from website
with open('currentDeals.json') as data:
    current_deals = json.load(data)

# pull all old deals from website
with open('oldDeals.json') as data:
    old_deals = json.load(data)

# select new deals in website
new_deals = select_new_deals(current_deals, old_deals)

# filter new deals in website
best_deals = filter_deals(new_deals, 0.3, ['M9.5', 'M9.0', '9.5 D', '9.0 D'])

# update old deals list with current deals
with open('oldDeals.json', 'w') as data:
    json.dump(current_deals, data)

new_deals = current_deals[:3]

if new_deals:
    # set up SMTP connection
    conn = smtplib.SMTP('smtp.gmail.com', 587)
    conn.ehlo()
    conn.starttls()
    conn.login('bernardopbf3@gmail.com', 'ksnczdktlbwzajzl')

    # create email message
    message = generate_email_body(new_deals)

    # send email
    conn.sendmail('bernardopbf3@gmail.com', ['bernardopbf3@gmail.com'], message)
    conn.quit()

    print("Emails Sent!")