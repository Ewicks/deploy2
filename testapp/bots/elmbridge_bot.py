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
def elmbridge_bot(startdate, enddate, wordlist):

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

    base_url = 'https://emaps.elmbridge.gov.uk/ebc_planning.aspx'

    url = 'https://emaps.elmbridge.gov.uk/ebc_planning.aspx?requesttype=parseTemplate&template=AdvancedSearchTab.tmplt&pagerecs=2000'
    driver.get(url)

    # Input start and end dates
    input_element1 = driver.find_element(By.ID, 'datevalidatedfrom')
    input_element2 = driver.find_element(By.ID, 'datevalidatedto')
    input_element1.send_keys(reversed_startdate)
    input_element2.send_keys(reversed_enddate)
    search_elements = driver.find_elements(By.CSS_SELECTOR, "input.atSpacing")

    # Select 500 and submit to show max results
    num_results_element = Select(driver.find_element(By.ID, 'maxrecords'))
    num_results_element.select_by_visible_text('500')

    # Filter the elements by their value attribute
    search_element = None

    for element in search_elements:
        if element.get_attribute("value") == "Search":
            search_element = element
            search_element.click()


    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.ID, 'resultsPerPage')))
    # Get the page source after the search
    page_source = driver.page_source

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    searchResultsPage = soup.find('div', id='atWeeklyListTable')
    searchResults = searchResultsPage.find_all('tr')
    searchResultsSnip = searchResults[1:]

    row_list = []

    for row in searchResultsSnip:
        address_div = row.find('td', class_='proposal')
        address_desc = address_div.text

        if (re.search(words_search_for, address_desc, flags=re.I)):
            row_list.append(row)

    print(len(row_list))
    num_results = len(row_list)
    for row in row_list:
        # Find the address and add to address_list
        address_div = row.find('td', class_='address')
        address = address_div.text.strip()
        address_list.append(address)
        print(address)
        a_tag = row.find('a')
        next_url = a_tag.get('href')
        summary_page = requests.get(next_url, verify=False)
        # summary_page = requests.get(
        #         url='https://app.scrapingbee.com/api/v1/',
        #         params={
        #             'api_key': API_KEY,
        #             'url': next_url,  
        #         },
        #     )
        summary_soup = BeautifulSoup(summary_page.content, "html.parser")
        info_section = summary_soup.find('div', id='atPubMenu')
        
        info_tabs = info_section.find_all('li')
        info_tab = info_tabs[1]
        info_a_tag = info_tab.find('a')
        info_href = info_a_tag.get('href')
        link_atag = (f'{base_url}{info_href}')
        further_info = requests.get(link_atag, verify=False)
        further_info_soup = BeautifulSoup(further_info.content, "html.parser")
        name_section = further_info_soup.find('div', class_='atLeftPanel')
        try:
            name_dt = name_section.find('dt', text="Applicant Name :")
            if name_dt:
                dd_tag = name_dt.find_next_sibling('dd')
                name = dd_tag.text.strip()
                print(name)
                name_list.append(name)
            
        except:
            name = 'n/a'
            name_list.append(name)


    merge_data = zip(name_list, address_list)

    for item in merge_data:
        data.append(item)

    print(data)
    # Close the browser window
    driver.quit()
    return data, num_results

   
