from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime, timedelta
import re
import time
import pprint
import requests
import urllib3
import os

# bug: instead of searching for a tag name be more specific so if two rows have the same name it won duplicate.
def epsom_bot(startdate, enddate, wordlist):

    # Access the API key
    API_KEY = os.getenv('API-KEY', '')

    def convert(s):
    
        # initialization of string to ""
        new = ""
    
        # traverse in the string
        for x in s:
            new = new + x + '|'
    
        # return string
        return new

    # Suppress only the InsecureRequestWarning from urllib3 needed for your request
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    words = convert(wordlist)
    words_search_for = words.rstrip(words[-1])
   

    # lists
    row_list = []
    address_list = []
    name_list = []
    data = []

    parsed_startdate = pd.to_datetime(startdate, format="%Y-%m-%d")
    parsed_enddate = pd.to_datetime(enddate, format="%Y-%m-%d")
    reversed_startdate = parsed_startdate.strftime('%d/%m/%Y')
    reversed_enddate = parsed_enddate.strftime('%d/%m/%Y')
    print(reversed_startdate)
    print(reversed_enddate)

    # Set up the WebDriver (you may need to provide the path to your chromedriver executable)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)

    base_url = 'https://eplanning.epsom-ewell.gov.uk/'

    url = 'https://eplanning.epsom-ewell.gov.uk/online-applications/search.do?action=advanced'
    driver.get(url)

    # Input start and end dates
    input_element1 = driver.find_element(By.ID, 'applicationReceivedStart')
    input_element2 = driver.find_element(By.ID, 'applicationReceivedEnd')
    input_element1.send_keys(reversed_startdate)
    input_element2.send_keys(reversed_enddate)
    # Click the search button
    search_element = driver.find_element(By.CLASS_NAME, 'recaptcha-submit')
    search_element.click()

    # Wait for the page to load (you may need to adjust the waiting time)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'resultsPerPage')))

    # Select 100 and submit to show max results
    num_results_element = Select(driver.find_element(By.ID, 'resultsPerPage'))
    num_results_element.select_by_visible_text('100')
    num_results_go = driver.find_element(By.CLASS_NAME, 'primary')
    num_results_go.click()

    next_a_tag = None
    multiple_pages = True
    num_results = 0



    while (multiple_pages):

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'resultsPerPage')))
        # Get the page source after the search
        page_source = driver.page_source

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        searchResultsPage = soup.find('div', class_='col-a')
        searchResults = searchResultsPage.find_all('li', class_='searchresult')

        row_list = []

        for row in searchResults:
            address_div = row.find('a')
            address_desc = address_div.text


            if (re.search(words_search_for, address_desc, flags=re.I)):
                row_list.append(row)

        print(len(row_list))
        num_results += len(row_list)
        for row in row_list:
            # Find the address and add to address_list
            address_div = row.find('p', class_='address')
            address = address_div.text.strip()
            address_list.append(address)
            print(address)

            a_tag = row.find('a')
            href_value = a_tag.get('href')
            test_url = (f'{base_url}{href_value}')
         
            summary_page = requests.get(
                url='https://app.scrapingbee.com/api/v1/',
                params={
                    'api_key': API_KEY,
                    'url': test_url,  
                },
            )
            summary_soup = BeautifulSoup(summary_page.content, "html.parser")
            info_tab = summary_soup.find(id='subtab_details')
            info_href = info_tab.get('href')
            info_atag = (f'{base_url}{info_href}')
            # further_info = requests.get(info_atag, verify=False)
            further_info = requests.get(
                url='https://app.scrapingbee.com/api/v1/',
                params={
                    'api_key': API_KEY,
                    'url': info_atag,  
                },
            )
            further_info_soup = BeautifulSoup(further_info.content, "html.parser")
            applicant_row = further_info_soup.find('th', string='Applicant Name').find_next('td')
            applicant_name = applicant_row.get_text(strip=True)

            print(applicant_name)
            name_list.append(applicant_name)

        try:
            next_a_tag = driver.find_element(By.CLASS_NAME, 'next')
            # If the element is found, you can interact with it here
            multiple_pages = True
            action = ActionChains(driver)
            action.move_to_element(next_a_tag).click().perform()
            # time.sleep(2)
            # next_a_tag.click()
            
        except NoSuchElementException:
            # If the element is not found, handle the exception here
            multiple_pages = False
            print("Element not found. Continuing without clicking.")




    merge_data = zip(name_list, address_list)

    for item in merge_data:
        data.append(item)

    print(data)
    # Close the browser window
    driver.quit()
    return data, num_results

 
