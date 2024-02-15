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
if os.path.isfile('env.py'):
    import env

# bug: instead of searching for a tag name be more specific so if two rows have the same name it won duplicate.
def kensington_chelsea_bot(startdate, enddate, wordlist):

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
    print(words_search_for)
   

    # lists
    row_list = []
    address_list = []
    name_list = []
    data = []

    parsed_startdate = pd.to_datetime(startdate, format='%Y/%m/%d')
    parsed_enddate = pd.to_datetime(enddate, format='%Y/%m/%d')
    reversed_startdate = parsed_startdate.strftime('%d/%m/%Y')
    reversed_enddate = parsed_enddate.strftime('%d/%m/%Y')
    print(reversed_startdate)
    print(reversed_enddate)


    # Set up the WebDriver (you may need to provide the path to your chromedriver executable)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)


    base_url = 'https://www.rbkc.gov.uk/planning/searches/'

    url = 'https://www.rbkc.gov.uk/planning/searches/default.aspx?adv=1#advancedSearch'
    driver.get(url)

    # Input start and end dates
    input_element1 = driver.find_element(By.ID, 'regDateFrom')
    input_element2 = driver.find_element(By.ID, 'regDateTo')
    input_element1.send_keys(reversed_startdate)
    input_element2.send_keys(reversed_enddate)



    # Select 100 and submit to show max results
    num_results_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'batch'))
    )
    num_results_element = Select(driver.find_element(By.ID, 'batch'))
    num_results_element.select_by_visible_text('100 per page')

    # Click the search button
    search_element = driver.find_element(By.ID, 'btnSearch')
    search_element.click()

    # Wait for the page to load (you may need to adjust the waiting time)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'scrollBar')))

    multiple_pages = True
    num_results = 0

    while (multiple_pages):

        # Get the page source after the search
        page_source = driver.page_source

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        searchResultsPage = soup.find('table')
        searchResults = searchResultsPage.find_all('tr')
        searchResults = searchResults[1:]
        row_list = []

        for row in searchResults:
          
            description_div = row.find_all('td')[1]
            description_text = description_div.text.strip().replace('\n', '')
            parts = description_text.split("...")
            address = parts[0].strip()
            description = parts[1].strip()

            if (re.search(words_search_for, description, flags=re.I)):
                row_list.append(row)

        print(len(row_list))
        num_results += len(row_list)
        for row in row_list:
            description_div = row.find_all('td')[1]
            description_text = description_div.text.strip().replace('\n', '')
            parts = description_text.split("...")
            address = parts[0].strip()
            print(address)
            address_list.append(address)

            a_tag = row.find('a')
            href_value = a_tag.get('href')
            next_url = (f'{base_url}{href_value}')
            summary_page = requests.get(next_url, verify=False)
            # summary_page = requests.get(
            #     url='https://app.scrapingbee.com/api/v1/',
            #     cookies= {"_ga_ZNLJF35KPL":"GS1.1.1706998240.1.0.1706998240.0.0.0"},

            #     params={
            #         'api_key': API_KEY,
            #         'url': next_url,  
            #     },
            # )
            next_page_soup = BeautifulSoup(summary_page.content, "html.parser")
            applicant_section = next_page_soup.find('table', id='applicant-details')
            applicant_tr = applicant_section.find_all('tr')[0]
            applicant_name = applicant_tr.find('td').text.strip()
            print(applicant_name)
            name_list.append(applicant_name)
        
        
        try:
            next_a_tag = driver.find_element(By.CLASS_NAME, 'pagNumber-nextPage')
            multiple_pages = True
            action = ActionChains(driver)
            action.move_to_element(next_a_tag).click().perform()
                
        except NoSuchElementException:
            # If the element is not found, handle the exception here
            multiple_pages = False
            print("Element not found. Continuing without clicking.")



    merge_data = zip(name_list, address_list)

    for item in merge_data:
        data.append(item)

    print(data)
    driver.quit()

    return data, num_results

   