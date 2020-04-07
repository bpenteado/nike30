from textwrap import dedent


def filter_new_deals(new_list, old_list):
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
