from django.shortcuts import render
import os
from selenium import webdriver

def index(request):
    # Set ChromeOptions
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    # Set Chrome binary location from environment variable
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Get webpage
    driver.get('https://www.bbc.com')
    test = driver.page_source

    # Close WebDriver
    driver.close()

    return render(request, 'index.html', {'test': test})
