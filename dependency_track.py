import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

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
    # obtain the output
    output = soup.find_all('div', {'class': 's-item__info clearfix'})
    # loop all items
    for element in output:
        product_dict = {
        #'title': element.find('span', {'class': 's-item__title'}).text,
        'title': element.find('span', {'role': 'heading'}).text,
        #'solddate': element.find('span', {'class': 's_item_title--tagblock__COMPLETED'}).find('span', {'class': 'POSITIVE'}.text),
        'link': element.find('a', {'class': 's-item__link'})['href'],
        }
        product_list.append(product_dict)
    return product_list

def trans_dataframe(product_list):
    df = pd.DataFrame(product_list)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'product_list' + timestr +'.csv'
    df.to_csv(filename, index=False)
    print('Your product list has been saved to currect directory.')
    return
#soup = narrow_products(url)
#product_list = parse_and_save(soup)    
#trans_dataframe(product_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--product', help='Enter the Product Name')
    parser.add_argument('-m', '--manufacturer', help='Enter the Manufacturer Name')
    args = parser.parse_args()

    # input all the parameters 
    product = args.product
    manufacturer = args.manufacturer
    new_url = url + manufacturer + '+' + product
    soup = narrow_products(new_url)
    product_list = parse_and_save(soup)
    trans_dataframe(product_list)
