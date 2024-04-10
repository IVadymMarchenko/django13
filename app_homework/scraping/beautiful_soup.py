import json

from bs4 import BeautifulSoup
# Create your views here.
import requests

BASE_URL = 'http://127.0.0.1:8000'


def get_author(url):
    author_url=f'{BASE_URL}/{url}'
    author_page = requests.get(author_url)  # робим запит
    author_soup = BeautifulSoup(author_page.text, 'html.parser')  #
    author_name = author_soup.find('h3').text.strip()  # имья автора
    author_born_date = author_soup.find('span', class_='author-born-date').text.strip()
    author_born_location = author_soup.find('span', class_='author-born-location').text.strip()
    author_description = author_soup.find('div', class_='author-description').text.strip()

    author_info = {
        'fullname': author_name,
        'born_date': author_born_date,
        'born_location': author_born_location,
        'description': author_description
    }
    return author_info


def get_authors():
    page_number = 1
    all_data = []
    while True:
        page_url = f'{BASE_URL}/{page_number}'
        page = requests.get(page_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        quotes = soup.findAll('div', class_='quote')
        if not quotes:
            break
        for quote in quotes:
            author_url = quote.find(('a'))['href']
            author_info = get_author(author_url)
            all_data.append(author_info)
        page_number += 1
    return all_data


# -----------------------------------------------------------------------------------
def get_quote(quote):
    tags = quote.find('div', class_='tags').find_all('a')
    tag_name = [tag.text for tag in tags]
    quotes = quote.find('span', class_='text').text.strip()
    author = quote.find('small', class_='author').text.strip()
    q = {
        'tag': tag_name,
        'author': author,
        'quote': quotes
    }
    return q

def get_quotes():
    page_number=1
    all_data=[]
    while True:
        page_url = f'{BASE_URL}/{page_number}'
        page = requests.get(page_url)
        quote = BeautifulSoup(page.text, 'html.parser')
        div = quote.findAll('div', class_='quote')
        if not div:
            break
        for quote in div:
            quotes_info=get_quote(quote)
            all_data.append(quotes_info)
        page_number+=1
    return all_data



def save_to_authors(author,filename):
    with open(filename,'w',encoding='utf-8') as file:
        json.dump(author,file, ensure_ascii=False, indent=4)

def save_to_quotes(quote,filename):
    with open(filename,'w',encoding='utf-8') as file:
        json.dump(quote,file,ensure_ascii=False,indent=4)




