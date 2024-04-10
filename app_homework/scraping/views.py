from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction
import json
# Create your views here.
import os
from quotes.models import Author, Tag, Quote  # noqa
from .beautiful_soup import save_to_authors, save_to_quotes, get_authors, get_quotes


@transaction.atomic
def get_srap(request):
    if request.method == 'GET':
        authors = get_authors()
        quotes = get_quotes()
        save_to_authors(authors, 'authors.json')
        save_to_quotes(quotes, 'quotes.json')
        if os.path.exists('authors.json'):
            with open('authors.json',encoding='utf-8') as file:
                data_of_authors = json.load(file)
                for author in data_of_authors:
                    aut, created = Author.objects.get_or_create(
                        fullname=author.get('fullname'),
                        born_date=author.get('born_date'),
                        born_location=author.get('born_location'),
                        description=author.get('description')
                    )
        if os.path.exists('quotes.json'):
            with open('quotes.json',encoding='utf-8') as file:
                data_of_quotes = json.load(file)
                for quote_data in data_of_quotes:
                    author_name = quote_data.get('author')
                    author = Author.objects.filter(fullname=author_name).first() if author_name else None
                    if author:
                        quote, created = Quote.objects.get_or_create(
                            author=author,
                            quote=quote_data.get("quote")
                        )
                        if created:
                            tags_data = quote_data.get('tags')
                            if tags_data is not None:
                                for tags in tags_data:
                                    tag, _ = Tag.objects.get_or_create(tag=tags)
                                    quote.tags.add(tag)
                                else:
                                    quote.tags.clear()
        return render(request, 'scraping/views_scraping.html', context={})
    return HttpResponse('Что-то пошло не так')
