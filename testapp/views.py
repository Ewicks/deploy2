from django.shortcuts import render
from bs4 import BeautifulSoup
import requests


def index(request):

    page = requests.get('http://www.google.com')
  
    summary_soup = BeautifulSoup(page.content, "html.parser")
    print(summary_soup)


    return render(request, 'index.html', {'test': summary_soup})
