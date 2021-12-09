import requests
from bs4 import BeautifulSoup
from random import choice
from csv import reader

total_guesses = 0
random_quote = None
res = 'y'


def read_quotes(filename):
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        quotes = list(csv_reader)
        return quotes


def reset():
    global total_guesses
    global random_quote
    total_guesses = 4
    random_quote = choice(arr)
    print("Here's a quote:\n\n")
    print(random_quote[0])
    print("\n")


def prompt_user():
    global res
    res = input("would you like to play again (y/n) ?")
    if res == 'y':
        print("Great! Here we go again...")
        reset()


def start_game():
    reset()
    global total_guesses
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
            split_arr = random_quote[1].split(" ")
            last_letter = split_arr[len(split_arr) - 1][0]
            print(f"Here's a hint: The author's last name starts with {last_letter}")
        elif answer != random_quote[1] and total_guesses == 1:
            total_guesses -= 1
            print(f"Sorry, you've run out of guesses. The answer was {random_quote[1]}")
            prompt_user()
        else:
            print("You guessed correctly! Congratulations!")
            prompt_user()

    print("Thank you for playing! Bye!")


arr = read_quotes("quotes.csv")
start_game()
