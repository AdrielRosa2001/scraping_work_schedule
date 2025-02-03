from pluggins.selenium_schedule_bot import run_scraping, get_schedule
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("USERNAME_SCHEDULE")
password = os.getenv("PASSWORD_SCHEDULE")

credentials = {"username": username, "password": password}

if __name__ == "__main__":
    return_login = run_scraping(credentials=credentials)
    get_schedule(driver=return_login)