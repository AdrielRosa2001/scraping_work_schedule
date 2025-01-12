from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from time import sleep
from google_api_connection import create_events_in_calendar
# import re
load_dotenv()

# GLOBAL VAR:
USERNAME = os.getenv('USERNAME_SCHEDULE')
PASSWORD = os.getenv('PASSWORD_SCHEDULE')
URL_LOGIN = os.getenv('URL_LOGIN')
# URL_SCHEDULE = os.getenv('URL_SCHEDULE')

meses_do_ano = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]

#FUNCTIONS:
def create_drive():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    print("Driver created!")
    return driver

def identify_and_close_new_handles(driver:webdriver.Chrome):
    all_handles = driver.window_handles
    print(f"All handles identify: {all_handles}")
    print(f"Current handler: {driver.current_window_handle}")
    
    for handle in all_handles:
        if handle != driver.current_window_handle:
            print("New handle identify is open!")
            driver.switch_to.window(handle)
            print(f"handler to closed: {driver.current_window_handle}")
            print(f"url handler to closed: {driver.current_url}")
            driver.close()
            print("New handle closed!")
    
    driver.switch_to.window(all_handles[0])
    print(f"New actualy window handler: {driver.current_window_handle}")
    print(f"Current url handler: {driver.current_url}")

def close_all_handles(driver:webdriver.Chrome):
    # Close all handles
    all_handles = driver.window_handles
    print("Close all handles!")
    for handle in all_handles:
        driver.switch_to.window(handle)
        driver.close()

def make_login(driver:webdriver.Chrome):
    html = None # HTML elements var

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
    try:
        css_selector_element_failed_login = "#_58_fm > div.portlet-msg-error" # Failed Messege login
        failed_messege_login = WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_element_failed_login))
        )
        print("Failed login!")
        return None
    except Exception as error_exception:
        try:
            print("Trying node name!")
            css_selector_element_success_login = "#banner > div > div.asi-header-top > div.main-menu > ul.username.k-widget.k-reset.k-header.k-menu.k-menu-horizontal > li > span"
            node_name_painel = WebDriverWait(driver=driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_element_success_login))
            )
            print("Node name find!")

            # Identifying new handle open:
            print("Identifying new handles!")
            identify_and_close_new_handles(driver=driver)

            try:
                print("Search iframe main...")
                iframe_main = WebDriverWait(driver=driver, timeout=10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#_webstationhome_WAR_agentwebstationportlet_iframe'))
                )
                driver.switch_to.frame(iframe_main)
                try:
                    print("Try: open schedule view")
                    css_selector_element_open_scheduleview = "#workarea > table.margin10 > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(4) > td > table > tbody > tr > td > a"
                    url_link_open_schedule_view = WebDriverWait(driver=driver, timeout=10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_element_open_scheduleview))
                    )
                    print("Open schedule view link find!")
                    url_link_open_schedule_view.click()
                    
                    try:
                        driver.switch_to.default_content()
                        print("Trying find iframe schedule view...")
                        iframe_schedule_view = WebDriverWait(driver=driver, timeout=10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '#_webstationscheduleviewer_WAR_agentwebstationportlet_iframe'))
                        )
                        print("Trying find iframe schedule view...")
                        driver.switch_to.frame(iframe_schedule_view)

                        try:
                            print("Trying link scheduleview format month...")
                            css_selector_element_view_month = "#viewFormatBarANDnavigationDate > table.dkGreyBar > tbody > tr > td > a:nth-child(2)"
                            url_view_month_format = WebDriverWait(driver=driver, timeout=10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_element_view_month))
                            )
                            print("Scheduleview format month find!")
                            url_view_month_format.click()

                            try: 
                                print("Trying find iframe with work schedule table...")
                                driver.switch_to.default_content()
                                iframe_wordk_schedule = WebDriverWait(driver=driver, timeout=10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, '#_webstationscheduleviewer_WAR_agentwebstationportlet_iframe'))
                                )
                                print("Find iframe with work schedule table!")
                                driver.switch_to.frame(iframe_wordk_schedule)

                                try:
                                    print("Trying search table with work schedule...")
                                    css_selector_table_complete_element = "#mainWorkArea"
                                    table_complete_element = WebDriverWait(driver=driver, timeout=10).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_table_complete_element))
                                    )
                                    print("Table with work schedule is find!")

                                    # print("Writhing in html file...")
                                    # html_re = re.sub(r"\u25c4", " ", driver.page_source) 
                                    # with open('./output_files/output.html', 'w', encoding="utf-8") as f:
                                    #     f.write(html_re)
                                    # print("HTML file saved!")
                                    html = driver.page_source
                                    driver.switch_to.default_content()
                                    close_all_handles(driver=driver)
                                    return html
                                except Exception as error_exception:
                                    print(f"Error to located table complete element!\n{error_exception}")
                                    close_all_handles(driver=driver)
                                    return None
                            except Exception as error_exception:
                                print(f"Error to located iframe with work schedule table!\n{error_exception}")
                                driver.switch_to.default_content()
                                close_all_handles(driver=driver)
                                return None
                        except Exception as error_exception:
                            print(f"Error to located link to work schedule in month format!")
                    except Exception as error_exception:
                        print(f"Error to located new iframe schedule view!\n{error_exception}")
                        driver.switch_to.default_content()
                        close_all_handles(driver=driver)
                        return None
                except Exception as error_exception:
                    # print(f"Error to located link view in month!\n{error_exception}")
                    print(f"Error to click in scheduleview link!\n{error_exception}")
                    close_all_handles(driver=driver)
                    return None
            except Exception as error_exception:
                print(f"Iframe main not detected!")
                close_all_handles(driver=driver)
                return None
        except Exception as error_exception:
            print(f"Failed to load page!\n{error_exception}")
            close_all_handles(driver=driver)
            return None
    
    

def scraping_work_schedule_with_bs4(html:webdriver.Chrome.page_source):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        select_primary_table = soup.find(id='mainWorkArea')
        complete_table = select_primary_table.find_all('table')
        title_month_schedule = complete_table[0].find_all('a')[1].get_text()
        
        days_finded = []
        rows_table = complete_table[1].find_all('tr')
        rows_table.pop(0)
        
        var_a = 1

        for row in rows_table:
            columns_table = row.find_all('td')
            columns_table.pop(0)

            for column in columns_table:
                try:
                    for tag_img in column.find_all('img'):
                        tag_img.decompose()
                except:
                    pass
                try:
                    all_finds_a = column.find_all('a') 
                    if len(all_finds_a) > 0:
                        for tag_a in all_finds_a:
                            column = str(tag_a).replace('<br/>', '-').split('>')[1].replace('</a', '')
                    else:
                        column = str(column).replace('<br/>', '-').split('>')[1].replace('</td', '')
                except:
                    pass
                
                list_extract_data = column.split('-')
                dict_data = {}
                dict_data['year'] = str(title_month_schedule).split(" ")[1]
                dict_data['month'] = str(meses_do_ano.index(str(title_month_schedule).split(" ")[0])+1)
                dict_data['day'] = list_extract_data[0]
                dict_data['schedule_start'] = list_extract_data[1]
                dict_data['schedule_end'] = list_extract_data[2]
                dict_data['status'] = list_extract_data[3]
                
                dict_data['complet_date'] = f"{dict_data['year']}-{(meses_do_ano.index(str(title_month_schedule).split(' ')[0])+1)}-{dict_data['day']}"
                if int(dict_data['day']) <= var_a:
                    if int(dict_data['day']) > len(days_finded):
                        days_finded.append(dict_data)
                        var_a = int(dict_data['day'])+1
    
        return days_finded
    else:
        print("Not detecter html for scraping!")


driver = create_drive()
html_result = make_login(driver=driver)
list_scraping_days = scraping_work_schedule_with_bs4(html_result)
print(30*"-")
print("Create event in calendar Google!")
create_events_in_calendar(list_scraping_days)
# for item in list_scraping_days:
#     print(f"Dia: {item['complet_date']}")
#     print(f"Entrada: {item['schedule_start']}")
#     print(f"Saída: {item['schedule_end']}")
#     print(f"Status: {item['status']}")
#     print(30*"-")

# print(list_scraping_days)

