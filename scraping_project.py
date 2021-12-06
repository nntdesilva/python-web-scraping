import requests
from bs4 import BeautifulSoup
from random import choice


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
            response = requests.get(website_url + next_page_url).text
            soup = BeautifulSoup(response, 'html.parser')
        except IndexError:
            next_page_url = None
    return arr


arr = fetch_quotes()
total_guesses = 4
res = 'y'
random_quote = choice(arr)
print("Here's a quote:\n\n")
print(random_quote[0])
print("\n")
while total_guesses >= 0 and res == 'y':
    answer = input(f"Who said this? Guesses remaining: {total_guesses}.")
    if answer != random_quote[1] and total_guesses == 4:
        total_guesses -= 1
        response = requests.get(random_quote[2]).text
        soup = BeautifulSoup(response, 'html.parser')
        born_date = soup.select('.author-born-date')[0].get_text()
        born_location = soup.select('.author-born-location')[0].get_text()
        print(f"Here's a hint: The author was born in {born_date} {born_location}")
    elif answer != random_quote[1] and total_guesses == 3:
        total_guesses -= 1
        first_letter = random_quote[1][0]
        print(f"Here's a hint: The author's first name starts with {first_letter}")
    elif answer != random_quote[1] and total_guesses == 2:
        total_guesses -= 1
        last_letter = random_quote[1].split(" ")[1][0]
        print(f"Here's a hint: The author's last name starts with {last_letter}")
    elif answer != random_quote[1] and total_guesses == 1:
        total_guesses -= 1
        print(f"Sorry, you've run out of guesses. The answer was {random_quote[1]}")
        res = input("would you like to play again (y/n) ?")
        if res == 'y':
            print("Great! Here we go again...")
            total_guesses = 4
            random_quote = choice(arr)
            print("Here's a quote:\n\n")
            print(random_quote[0])
            print("\n")
    else:
        print("You guessed correctly! Congratulations!")
        res = input("would you like to play again (y/n) ?")
        if res == 'y':
            total_guesses = 4
            random_quote = choice(arr)
            print("Here's a quote:\n\n")
            print(random_quote[0])
            print("\n")

print("Thank you for playing! Bye!")
