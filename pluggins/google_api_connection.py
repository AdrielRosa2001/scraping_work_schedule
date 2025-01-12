# from __future__ import print_function
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

import os.path
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib .flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar']
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def create_events_in_calendar(list_evets: dict):
    creds = None
    
    if os.path.exists("token.json"):
        # creds = Credentials.from_authorized_user_file("token.json")
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("calendar", "v3", credentials=creds)

        # now = dt.datetime.now().isoformat() + "Z"
        # event_result = service.events().list(calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime").execute()
        # events = event_result.get("items", [])

        # if not events:
        #     print("No upcoming events found!")
        #     return
        
        # for event in events:
        #     start = event["start"].get("dateTime", event["start"].get("date"))
        #     print(start, event["summary"])

        for item in list_evets:
            now_time = dt.datetime.today()
            event = {
                "summary": "ESCALA DE TRABALHO",
                "location": "Teleperformance",
                "description": f"Escala atualizada em: {now_time}",
                "colorId": 1,
                "start": {
                    "dateTime": f"{item['complet_date']}T{item['schedule_start']}:00-03:00",
                    "timeZone": "America/Sao_Paulo"
                },
                "end": {
                    "dateTime": f"{item['complet_date']}T{item['schedule_end']}:00-03:00",
                    "timeZone": "America/Sao_Paulo"
                }
            }
            try:
                event = service.events().insert(calendarId="primary", body=event).execute()
                print(f"Event created: {event.get('htmlLink')}")
            except:
                print("Failed to create event!")

    except HttpError as error:
        print("An error occurred:", error)

