from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver



def index(request):


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)


    url = 'https://www.google.com'
    driver.get(url)
    test = driver.page_source

    return render(request, 'index.html', {'test': test})
