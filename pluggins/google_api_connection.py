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

def create_event(item, service: build):
    now_time = dt.datetime.today().strftime("%d/%m/%Y às %H:%M:%S")
    if item['schedule_start'] != "":
        event = {
            "summary": "ESCALA DE TRABALHO TP",
            "location": "Teleperformance",
            "description": f"Escala atualizada em: {now_time}",
            "colorId": 3,
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

def search_and_delete_event(item, service:build):
    # now = dt.datetime.now().isoformat() + "Z"
    time_event = f"{item['complet_date']}T00:00:00.000000Z"
    # print(now)
    event_result = service.events().list(calendarId="primary", timeMin=time_event, maxResults=31, singleEvents=True, orderBy="startTime").execute()
    events = event_result.get("items", [])

    if not events:
        print("No upcoming events found!")
        return
    
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        event_ref = f"{start} {event['summary']}"
        # print(event)
        # service.events().delete
        if event['summary'] == "ESCALA DE TRABALHO TP":
            service.events().delete(calendarId="primary", eventId=event['id'], sendNotifications=None, sendUpdates=None).execute()
            print(f"{event_ref} - Event deleted successfuly!")


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

        for item in list_evets:
            search_and_delete_event(item=item, service=service)

        for item in list_evets:
            create_event(item=item, service=service)
            

    except HttpError as error:
        print("An error occurred:", error)

