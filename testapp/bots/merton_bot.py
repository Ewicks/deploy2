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
def merton_bot(startdate, enddate, wordlist):

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

    base_url = 'https://planning.merton.gov.uk/Northgate/PlanningExplorerAA/Generic/'

    url = 'https://planning.merton.gov.uk/Northgate/PlanningExplorerAA/GeneralSearch.aspx'
    driver.get(url)
    cookies = driver.get_cookies()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    print(cookies_dict)

    # Input start and end dates
    input_element1 = driver.find_element(By.ID, 'dateStart')
    input_element2 = driver.find_element(By.ID, 'dateEnd')
    input_element1.send_keys(reversed_startdate)
    input_element2.send_keys(reversed_enddate)
    # Click the search button
    search_element = driver.find_element(By.ID, 'csbtnSearch')
    search_element.click()

    # Wait for the page to load (you may need to adjust the waiting time)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'display_table')))

    multiple_pages = True
    num_results = 0

    while (multiple_pages):

        # Get the page source after the search
        page_source = driver.page_source

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        searchResultsPage = soup.find('table', class_='display_table')
        searchResults = searchResultsPage.find_all('tr', class_=['Row0', 'Row1'])
        searchResults = searchResults[1:]

        row_list = []

        for row in searchResults:
          
            # print(address_desc)
            description_div = row.find('td', {'title': 'Development Description'})
            description_text = description_div.text


            if (re.search(words_search_for, description_text, flags=re.I)):
                row_list.append(row)

        print(len(row_list))
        num_results += len(row_list)
        for row in row_list:
            address_div = row.find('td', {'title': 'Site Address'})
            address = address_div.text.strip()
            address_list.append(address)
            print(address)

            a_tag = row.find('a')
            href_value = a_tag.get('href')
            next_url = (f'{base_url}{href_value}')
            # cookies = {"MVMSession":"ID=c721a245-35e4-4b40-ba1d-b947403f27da"}
            # cookies = {"ar_debug":"1"}
            # cookies = {"_ga_ZNLJF35KPL":"GS1.1.1706998240.1.0.1706998240.0.0.0"}
            # summary_page = requests.get(next_url, verify=False)

            # summary_page = requests.get(next_url, cookies=cookies_dict, verify=False)
            summary_page = requests.get(
                url='https://app.scrapingbee.com/api/v1/',
                cookies=cookies_dict,

                params={
                    'api_key': API_KEY,
                    'url': next_url,  
                },
            )
            next_page_soup = BeautifulSoup(summary_page.content, "html.parser")
            print(next_page_soup)
            applicant_sections = next_page_soup.find_all('ul', class_='list')
            print(applicant_sections)
            sections = applicant_sections[1]
            applicant_span = sections.find('span', text='Applicant')
            parent_div = applicant_span.find_parent('div')
            applicant_name = ''.join([
                text
                for text in parent_div.stripped_strings
                if text.lower() != 'applicant'
            ])
            name_list.append(applicant_name)
            print(applicant_name)

        try: 
            next_a_tag = soup.find('img', {'title': 'Go to next page '})
        except:
            next_a_tag = False
    
        if (next_a_tag):
            multiple_pages = True
            next_a_tag = driver.find_element(By.CLASS_NAME, 'noborder')
            action = ActionChains(driver)
            action.move_to_element(next_a_tag).click().perform()
   
        else:
            # If the element is not found, handle the exception here
            multiple_pages = False
            print("Element not found. Continuing without clicking.")


    merge_data = zip(name_list, address_list)

    for item in merge_data:
        data.append(item)

    print(data)
    driver.quit()

    return data, num_results

