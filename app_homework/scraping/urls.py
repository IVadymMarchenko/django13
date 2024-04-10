from django.urls import path, include
from . import views

app_name = 'scraping'

urlpatterns = [
    path('to_db/',views.get_srap,name='scrap'),
]