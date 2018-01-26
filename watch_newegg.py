import requests
import smtplib
import time

from bs4 import BeautifulSoup


URL = (
  'https://www.newegg.com/Product/ProductList.aspx?'
  'Submit=ENE&N=100007709%20600494828%20601107976%20601203818%20601296707&'
  'IsNodeId=1&bop=And&Order=PRICE&PageSize=36')
UL_ELEMENT_CLASS = 'item-container'
SLEEP_TIME = 60


def get_page():
  response = requests.get(URL)
  return response.content


def find_element(html, label, attributes):
  return BeautifulSoup(html, 'html.parser').findAll(label, attributes)


def get_lowest_price():
  content = get_page()
  list_items = find_element(
    content,
    'div',
    attributes={'class': UL_ELEMENT_CLASS})

  lowest_available = list_items[0]
  lowest_label = lowest_available.find('li', {'class': 'price-current'})
  lowest_price = int(lowest_label.find('strong').text)

  return lowest_price

def work_loop():
  saved_price = None

  while True:
    lowest_price = get_lowest_price()

    if lowest_price != saved_price:
      print 'new lowest price: ${}'.format(lowest_price)
      saved_price = lowest_price

    time.sleep(SLEEP_TIME)


if __name__ == '__main__':
  work_loop()
