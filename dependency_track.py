import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import math

url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='

# Utilizes BeautifulSoup and requests package to obtain initial data 
def narrow_products(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html5lib')
    return soup

# Parsing elements for the searching
def parse_and_save(soup):
    # store the outputs
    product_list = []
    # obtain the number for items / page
    count = str(soup.find('h1', {'class': 'srp-controls__count-heading'}).find('span', {'class':'BOLD'}))
    nums = ''
    for char in count:
        if char.isdigit():
            nums += char
    count_heading = int(nums)
    # obtain the output
    output = soup.find_all('div', {'class': 's-item__info clearfix'})
    # loop all items
    for element in output:
        product_dict = {
        #'title': element.find('span', {'class': 's-item__title'}).text,
        'title': element.find('span', {'role': 'heading'}).text,
        'link': element.find('a', {'class': 's-item__link'})['href'],
        }
        product_list.append(product_dict)
    return product_list, count_heading

def trans_dataframe(product_list):
    df = pd.DataFrame(product_list)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'product_list' + timestr +'.csv'
    df.to_csv(filename, index=False)
    print('Your product list has been saved to currect directory.')
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--product', help='Enter the Product Name')
    parser.add_argument('-m', '--manufacturer', help='Enter the Manufacturer Name')
    args = parser.parse_args()

    # input all the parameters 
    product = args.product
    manufacturer = args.manufacturer
    # store the product name and manufacturer name in a txt file
    # first print the product name
    print('The product name is', product)
    print('The manufacturer name is', manufacturer)
    # save the manufaturer name to a txt file
    with open('manufacturer.txt', 'w') as f:
        f.write(manufacturer)
    new_url = url + manufacturer + '+' + product + '&_ipg=240'
    soup = narrow_products(new_url)
    product_list, count_heading  = parse_and_save(soup)
    #print(count_heading)
    page_num = math.ceil(count_heading / 240) + 1
    new_product_list = product_list
    for i in range(2, page_num):
        #print('Now PAGE ', i, '!!!')
        page_url = new_url + '&_pgn=' + str(i)
        page_soup = narrow_products(page_url)
        product_list, _ = parse_and_save(page_soup)
        new_product_list += product_list
    trans_dataframe(new_product_list)

   
