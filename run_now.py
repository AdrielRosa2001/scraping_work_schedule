from pluggins.selenium_schedule_bot import run_scraping, get_schedule
import os
from dotenv import load_dotenv
from pluggins.google_api_connection import create_credential
load_dotenv()

username = os.getenv("USERNAME_SCHEDULE")
password = os.getenv("PASSWORD_SCHEDULE")

credentials = {"username": username, "password": password}

if __name__ == "__main__":
    escolha = 0
    while(escolha != "3"):
        print(30*"-")
        print("******** Scraping NICE TTV ********")
        print("1 - Realizar login google.")
        print("2 - Puxar Escalas.")
        print("3 - Sair.")
        print(30*"-")
        escolha = input("Escolha a opção: ")
        print(30*"-")

        if escolha == "1":
            os.remove("token.json")
            create_credential()
        elif escolha == "2":
            return_login = run_scraping(credentials=credentials)
            get_schedule(driver=return_login)
        elif escolha == "3":
            print("Saindo...")
            escolha = "3"