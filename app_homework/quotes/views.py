from django.shortcuts import render
from .models import Quote,Author,Tag
from django.core.paginator import Paginator
from django.db.models import Count

# Create your views here.

def main(request,page=1):
    quote_list = Quote.objects.all().order_by('-created_at')
    author_ids = set(quote.author_id for quote in quote_list)
    authors = Author.objects.filter(id__in=author_ids)
    per_page=10
    paginator=Paginator(list(quote_list),per_page)
    quote_on_page=paginator.page(page)
    top_tags=Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    tag_font_sizes = {tag: 16 + tag.num_quotes // 10 for tag in top_tags}
    return render(request, 'quotes/index.html', {'quotes_list': quote_on_page, 'authors': authors,'top_tags':top_tags,'tag_font_sizes': tag_font_sizes})


def author_data(request,author_id):
    author=Author.objects.get(id=author_id)
    return render(request,'quotes/author_detail.html', {'author': author})


def tag_data(request,tag_id):
    tag = Tag.objects.get(pk=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    authors = Author.objects.filter(quote__in=quotes).distinct()
    return render(request, 'quotes/quote_detail.html', context={'quotes': quotes, 'authors': authors})



