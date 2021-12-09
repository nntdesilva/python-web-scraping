#run this file first to generate quotes.csv with scrapped quotes before running game.py

import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import writer


def fetch_quotes():
    website_url = "http://quotes.toscrape.com"
    response = requests.get(website_url).text
    soup = BeautifulSoup(response, 'html.parser')
    arr = []
    next_page_url = soup.select('.next')
    while next_page_url:
        quotes = soup.select('.quote')
        for quote in quotes:
            quote_text = quote.select('.text')[0].get_text()
            author = quote.select('.author')[0].get_text()
            bio_link = website_url + quote.select('a')[0]['href']
            quote_data = [quote_text, author, bio_link]
            arr.append(quote_data)
        try:
            next_page_url = soup.select('.next')[0].select('a')[0]['href']
            sleep(1)
            response = requests.get(website_url + next_page_url).text
            soup = BeautifulSoup(response, 'html.parser')
        except IndexError:
            next_page_url = None
    return arr


def write_quotes(all_quotes):
    with open("quotes.csv", "w") as file:
        csv_writer = writer(file)
        for quote in all_quotes:
            csv_writer.writerow(quote)


all_quotes = fetch_quotes()
write_quotes(all_quotes)
