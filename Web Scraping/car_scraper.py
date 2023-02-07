# Importing Libraries
import requests
import random
import os
from bs4 import BeautifulSoup
from logger import logging


# Defining User Agents to prevent being banned for scrapping
user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
]

# Car Brands
# car_brands = ['aston-martin', 'bentley', 'bugatti', 'rolls-royce', 'koenigsegg', 'porsche', 'ferrari',
#               'maserati', 'lamborghini', 'mclaren', 'mercedes-benz',
#               'bmw', 'lexus', 'audi', 'volvo', 'jaguar', 'land-rover', 'tesla']

car_brands = ['lamborghini', 'mclaren', 'mercedes-benz', 'bmw', 'lexus',
              'audi', 'volvo', 'jaguar', 'land-rover', 'tesla']

# Creating a directory to save pics
car_dir = os.path.join(os.getcwd(), "cars")

# Looping through each brand
for brand in car_brands:

    # Creating directory within car directory to save pics on basis of their brand
    brand_dir = os.path.join(car_dir, brand)
    os.makedirs(brand_dir, exist_ok=True)
    logging.info(f"{'>>'*10} {brand} {'<<'*10}")
    logging.info(f"Brand Directory Created:- {brand_dir}")

    # Getting into website and getting link of all models
    website_link = f"https://www.drivespark.com/photos/{brand}/"
    brand_main_page = requests.get(website_link, headers={'User-Agent': random.choice(user_agents_list)}).text
    soup = BeautifulSoup(brand_main_page, 'lxml')
    model_links = []
    home_car_cards = soup.find_all('h3', class_='text-latest')
    for card in home_car_cards:
        model_links.append(card.a['href'])
    logging.info(f"Got Model Links:- {model_links[0]}")

    icount = 1

    # Now we have list of all models of this brand.
    # We will loop through each model and get the link of pics of that model
    for each_model in model_links:
        pic_link_source = requests.get(each_model, headers={'User-Agent': random.choice(user_agents_list)}).text
        soup = BeautifulSoup(pic_link_source, 'lxml')
        pic_urls = []
        pic_cards = soup.find_all('div', class_="pstorythumb rel")
        for card in pic_cards:
            link = "https://www.drivespark.com/" + card.img['src']
            pic_urls.append(link)
        logging.info(f"Got Pic Links:- {pic_urls[0]}")
        # Now we will start pic download process

        # Getting into new directory specific to brand to save each pic
        os.chdir(brand_dir)

        for url in pic_urls:
            response = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
            if response.status_code:
                fp = open(f'model{icount}.jpg', 'wb')
                fp.write(response.content)
                fp.close()
            icount += 1

        # Getting back into parent directory
        os.system("car_scraper.py")

    logging.info(f"{brand} pics saved")
