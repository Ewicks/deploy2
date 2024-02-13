
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd
import time
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


# when start and end date is same the website can't handle that
# got to have at least 2 keywords
# finding the name of applicant only works sometimes due to the code


def kingston_bot(startdate, enddate, wordlist):

    

    def split_dates(start_date_str, end_date_str):
        date_format = "%d/%m/%Y"
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)

        date_ranges = []
        current_date = start_date

        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)  # Add 9 days to current date
            if next_date > end_date:
                next_date = end_date
            date_ranges.append((current_date.strftime(date_format), next_date.strftime(date_format)))
            current_date = next_date + timedelta(days=1)  # Move to the next day

        return date_ranges
    
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
    list_of_dates = split_dates(reversed_startdate, reversed_enddate)


    # def create_driver_with_rotating_user_agent():
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_options.add_argument('headless')
    #     chrome_options.add_argument('window-size=1200x600')

    #     # Rotate user agents using fake_useragent library
    #     user_agent = UserAgent().random
    #     chrome_options.add_argument(f'user-agent={user_agent}')

    #     driver = webdriver.Chrome(options=chrome_options)
    #     return driver

    # driver = create_driver_with_rotating_user_agent()

    driver = webdriver.Chrome()


    for x in list_of_dates:
        print(list_of_dates)

        print(x)
        start = x[0]
        end = x[1]

    
       

        url = 'https://publicaccess.kingston.gov.uk/online-applications/search.do?action=advanced'
        driver.get(url)


        # Input start and end dates
        input_element1 = driver.find_element(By.ID, 'applicationReceivedStart')
        input_element2 = driver.find_element(By.ID, 'applicationReceivedEnd')
        input_element1.send_keys(start)
        input_element2.send_keys(end)
        # Click the search button
        search_element = driver.find_element(By.CLASS_NAME, 'recaptcha-submit')
        action = ActionChains(driver)
        action.move_to_element(search_element).click().perform()
        # search_element.click()

        # Wait for the page to load (you may need to adjust the waiting time)
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, 'resultsPerPage')))
        except TimeoutException:
            continue

        # Select 100 and submit to show max results
        num_results_element = Select(driver.find_element(By.ID, 'resultsPerPage'))
        num_results_element.select_by_visible_text('100')
        num_results_go = driver.find_element(By.CLASS_NAME, 'primary')
        action = ActionChains(driver)
        action.move_to_element(num_results_go).click().perform()

        # time.sleep(2)
        # num_results_go.click()
        next_a_tag = None
        multiple_pages = True


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
            print(len(searchResults))
            for row in searchResults:
                address_div = row.find('a')
                address_desc = address_div.text

                if (re.search(words_search_for, address_desc, flags=re.I)):
                    row_list.append(row)

            print(len(row_list))
            for row in row_list:

                # Find the address and add to address_list
                address_div = row.find('p', class_='address')
                address = address_div.text.strip()
                address_list.append(address)
                print(address)
                a_tag = row.find('a')
                href_value = a_tag.get('href')

                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//a[@href='{href_value}']"))
                    )
                except TimeoutException:
                    name_list.append('n/a')
                    driver.back()
                    # driver.back()
                    # driver.execute_script("location.reload(true);")
                    continue
                except StaleElementReferenceException:
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//a[@href='{href_value}']"))
                        )
                    except TimeoutException:
                        name_list.append('n/a')
                        driver.back()
                        # driver.back()
                        # driver.execute_script("location.reload(true);")
                        continue
                    

                # Now, you can perform actions on the found element
                # For example, click the link

                element.click()

                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.ID, 'subtab_details')))
                subtab = driver.find_element(By.ID, 'subtab_details')
                subtab.click()
                try:
                    applicant_row = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//th[text()="Applicant Name"]/following-sibling::td'))
                    )
                except NoSuchElementException as e:
                    print(f"NoSuchElementException: {e}")
                    applicant_name_value = 'no-name'
                except:
                    applicant_name_value = 'n/aa'
                # Extract the "Applicant Name" text content
                if applicant_row:
                    applicant_name_value = applicant_row.text
                else:
                    applicant_name_value = 'n/a'

                name_list.append(applicant_name_value)
                print(applicant_name_value)
                driver.back()
                driver.back()
                driver.execute_script("location.reload(true);")

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
    return data

