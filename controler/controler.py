from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from time import sleep

# GLOBAL VAR:
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
URL_LOGIN = os.getenv('URL_LOGIN')
URL_SCHEDULE = os.getenv('URL_SCHEDULE')

#FUNCTIONS:
def create_drive():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    print("Driver created!")
    return driver

def identify_and_close_new_handles(driver:webdriver.Chrome):
    all_handles = driver.window_handles
    
    for handle in all_handles:
        if handle != driver.current_window_handle:
            print("New handle identify is open!")
            driver.switch_to.window(handle)
            driver.close()
            print("New handle closed!")
    
    driver.switch_to.window(all_handles[0])

def make_login(driver:webdriver.Chrome):
    print("Get to URL LOGIN page!")
    driver.get(URL_LOGIN)
    sleep(3)
    #login - id: _58_login
    login_input = driver.find_element(By.ID, "_58_login")
    print("Login input find!")
    #pass - id: _58_password
    pass_input = driver.find_element(By.ID, "_58_password")
    print("Password input find!")
    #btn login - class: aui-button-input-submit
    btn_login = driver.find_element(By.CLASS_NAME, "aui-button-input-submit")
    print("Btn input find!")

    print("Make Login!")
    login_input.send_keys(USERNAME)
    pass_input.send_keys(PASSWORD)
    sleep(1)
    btn_login.click()
    
    sleep(4)

    # Identifying new handle open:
    print("Identifying new handles!")
    identify_and_close_new_handles(driver=driver)

    # Go to work schedule page in month format
    print("Go to work schedule page in month format")
    driver.get(URL_SCHEDULE)
    sleep(4)

    html = driver.page_source

    # Close all handles
    all_handles = driver.window_handles
    print("Close all handles!")
    for handle in all_handles:
        driver.switch_to.window(handle)
        driver.close()

    return html

def scraping_work_schedule_with_bs4(html:webdriver.Chrome.page_source):
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    complete_table = soup.select_one('#mainWorkArea');
    print(complete_table)
    table_two = complete_table[1]
    title_month_schedule = complete_table[0].find_all('a')[1].get_text()
    # table_work_schedule = complete_table[1].find_all('tr')
    
    days_finded = []
    rows_table = complete_table[1].find_all('tr')
    rows_table.pop(0)

    for row in rows_table:
        columns_table = row.find_all('td')
        columns_table.pop(0)

        for column in columns_table:
            link_schedule_element = column.find('a').get_text()
            days_finded.append(link_schedule_element)
    
    scraping_days = {"month": title_month_schedule, "days": days_finded}


driver = create_drive()
html_result = make_login(driver=driver)
list_scraping_days = scraping_work_schedule_with_bs4(html_result)
print(list_scraping_days)
