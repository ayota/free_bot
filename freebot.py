from functions import scraper
from functions import tweeter
from functions import mapper

free_things = scraper()

tweeter(free_things)

mapper(free_things)
