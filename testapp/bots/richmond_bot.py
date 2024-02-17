from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import re
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import os
import urllib3


def richmond_bot(startdate, enddate, wordlist):

    def format_address(addresss):
        formatted_address = addresss.replace('\n', ' ')
        address_list.append(formatted_address)


    def convert(s):
 
        # initialization of string to ""
        new = ""
    
        # traverse in the string
        for x in s:
            new = new + x + '|'
    
        # return string
        return new

    row_list = []
    address_list = []
    name_list = []
    data = []
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

   
    words = convert(wordlist)
    words_search_for = words.rstrip(words[-1])
    print(startdate)
    print(enddate)
    parsed_startdate = pd.to_datetime(startdate, format="%Y-%m-%d")
    parsed_enddate = pd.to_datetime(enddate, format="%Y-%m-%d")
    reversed_startdate = parsed_startdate.strftime('%d/%m/%Y')
    reversed_enddate = parsed_enddate.strftime('%d/%m/%Y')

    print(reversed_startdate)
    print(reversed_enddate)


    # Set up the WebDriver (you may need to provide the path to your chromedriver executable)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    # Set Chrome binary location from environment variable
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    # Initialize WebDriver
    # driver = webdriver.Chrome(options=chrome_options)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)


    url = 'https://www2.richmond.gov.uk/lbrplanning/Planning_Report.aspx'
    driver.get(url)

    # Input start and end dates
    input_element1 = driver.find_element(By.ID, 'ctl00_PageContent_dpValFrom')
    input_element2 = driver.find_element(By.ID, 'ctl00_PageContent_dpValTo')
    input_element1.send_keys(reversed_startdate)
    input_element2.send_keys(reversed_enddate)
    # Click the search button
    search_element = driver.find_element(By.CLASS_NAME, 'btn-primary')


    # Wait for the cookie consent popup to appear
    wait = WebDriverWait(driver, 10)
    cookie_popup = wait.until(EC.presence_of_element_located((By.ID, 'ccc-end')))

    # Locate and click the "Accept" button
    accept_button = cookie_popup.find_element(By.ID, 'ccc-dismiss-button')
    accept_button.click()

    # Select 500 to show max results
    num_results_element = Select(driver.find_element(By.ID, 'ctl00_PageContent_ddLimit'))
    num_results_element.select_by_visible_text('500')

    # Click submit for advanced results page
    search_element.click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'infocontent')))

    # Get the page source after the search
    page_source = driver.page_source

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')


    span_div = driver.find_element(By.ID, 'ctl00_PageContent_lbl_APPS')
    num_results = span_div.find_element(By.TAG_NAME, 'strong')

    if (int(num_results.text) == 500):
        print('Results over 500 please alter your search results')
        driver.quit()
    else:
        print('Number of results for this search is: ' + num_results.text)

    searchResultsPage = soup.find('ul', class_='planning-apps')
    searchResults = searchResultsPage.find_all('li')

    row_list = []

    # search the description but append all rows with key words in description to row_list
    for row in searchResults:
        address_divs = row.find_all('p')
        address_desc = address_divs[1].text

        if (re.search(words_search_for, address_desc, flags=re.I)):
            row_list.append(row)
    
    print(len(row_list))
    num_results = len(row_list)
    for row in row_list:
        # Find the address and add to address_list
        address_div = row.find('h3')
        address = address_div.text.strip()
        format_address(address)

        a_tag = row.find('a')
        href_value = a_tag.get('href')
        element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@href='{href_value}']"))
        )
        element.click()
        try:
            subtab = None
            subtab = driver.find_element(By.ID, 'ctl00_PageContent_btnShowApplicantDetails')
        except:
            driver.back()
            name_list.append('n/a')
            continue

    
        subtab.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'ctl00_PageContent_lbl_Applic_Name')))
        name_page_source = driver.page_source
        name_soup = BeautifulSoup(name_page_source, 'html.parser')
        name = name_soup.find('span', id='ctl00_PageContent_lbl_Applic_Name')
        name_list.append(name.text.strip())

        driver.back()
        driver.back()


    merge_data = zip(name_list, address_list)

    for item in merge_data:
        data.append(item)

    print(data)

    # Close the browser window
    driver.quit()
    return data, num_results




