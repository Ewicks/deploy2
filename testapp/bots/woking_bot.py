from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import re


def woking_bot(startdate, enddate, wordlist):

    def convert(s):
 
        # initialization of string to ""
        new = ""
    
        # traverse in the string
        for x in s:
            new = new + x + '|'
    
        # return string
        return new


    words = convert(wordlist)
    words_search_for = words.rstrip(words[-1])

    parsed_startdate = pd.to_datetime(startdate, format="%Y-%m-%d")
    parsed_enddate = pd.to_datetime(enddate, format="%Y-%m-%d")
    reversed_startdate = parsed_startdate.strftime('%d/%m/%Y')
    reversed_enddate = parsed_enddate.strftime('%d/%m/%Y')
    print(reversed_startdate)
    print(reversed_enddate)


    row_list = []
    address_list = []
    name_list = []
    data = []

    # Set up the WebDriver (you may need to provide the path to your chromedriver executable)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)

    url = 'https://caps.woking.gov.uk/online-applications/search.do?action=advanced'
    driver.get(url)

    # Input start and end dates
    input_element1 = driver.find_element(By.ID, 'applicationReceivedStart')
    input_element2 = driver.find_element(By.ID, 'applicationReceivedEnd')
    input_element1.send_keys(reversed_startdate)
    input_element2.send_keys(reversed_enddate)

    # Click the search button
    search_element = driver.find_element(By.CLASS_NAME, 'recaptcha-submit')
    search_element.click()


    # Select 100 and submit to show max results
    num_results_element = Select(driver.find_element(By.ID, 'resultsPerPage'))
    num_results_element.select_by_visible_text('100')
    num_results_go = driver.find_element(By.CLASS_NAME, 'primary')
    num_results_go.click()

    next_a_tag = None
    multiple_pages = True
    num_results = 0

    while (multiple_pages):

        # Wait for the page to load (you may need to adjust the waiting time)
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
            a_tag = row.find('a')
            href_value = a_tag.get('href')
            element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@href='{href_value}']"))
            )
            element.click()

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, 'subtab_details')))
            subtab = driver.find_element(By.ID, 'subtab_details')
            subtab.click()

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'row0')))
            name_page_source = driver.page_source
            name_soup = BeautifulSoup(name_page_source, 'html.parser')


        # Find the <td> element within the <tr> where the <th> has the specified text
            applicant_name_tr = name_soup.find_all('tr', {'class': 'row0'})


            for tr in applicant_name_tr:
                tr_text = tr.text
                if 'Applicant Name' in tr_text:
                    td = tr.find('td')
                    if td is not None:
                        name_list.append(td.text)
                    else:
                        print('No Name')
                        name_list.append('N/A')

                    # Reset the td variable for the next iteration
                    td = None
            
            driver.back()
            driver.back()
            driver.execute_script("location.reload(true);")
        try:
            next_a_tag = driver.find_element(By.CLASS_NAME, 'next')
            # If the element is found, you can interact with it here
            multiple_pages = True
            next_a_tag.click()
                
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


