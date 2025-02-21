from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/scrape/', views.api_scraper, name='api_scraper'),  # JSON API for web scraping
    path('curl/', views.curl_test, name='curl_test'),  # cURL test endpoint
]