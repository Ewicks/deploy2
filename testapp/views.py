from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager




def index(request):

    options = Options()
    options.add_argument('headless')
    print('sa')
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # print('s')

    driver.get('https://www.bbc.com')
 
    test = driver.page_source
    print(test)

    driver.close()

    return render(request, 'index.html', {'test': test})
