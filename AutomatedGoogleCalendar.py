from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import random

SCOPES = ['https://www.googleapis.com/auth/calendar']

#Enter list of events required
listOfEvents = []

#Generate random time after a specific time, here it is set to 3pm
def randomTimeRange():     

    n = random.randrange(0, 300, 30)
    
    lowerBoundary = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day + 1, 15, 00)
    
    start = lowerBoundary + datetime.timedelta(minutes = n)
    end = start + datetime.timedelta(minutes = 30)
    
    return [start.strftime("%Y-%m-%dT%H:%M:%S+01:00"), end.strftime("%Y-%m-%dT%H:%M:%S+01:00")]
    

#Authentication and initiation of google calendar API
def get_calendar_service():
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
    return service

service = get_calendar_service()

busyStarts = []

#Checks if a time slot has already been taken
def smartTimeRange():
    
    
    timeRange = randomTimeRange()
    
    startTime = timeRange[0]
    endTime = timeRange[1]

    
    while startTime in busyStarts:
        
        timeRange = randomTimeRange()
    
        startTime = timeRange[0]
        endTime = timeRange[1]
        
    busyStarts.append(startTime)
    
    return [startTime, endTime]

def main():
    
    #Update google calendar with events and their respective random times
    for item in listOfEvents:
        
        time = smartTimeRange()
        
        service.events().insert(calendarId='primary', body={"summary": item, "start": {"dateTime": time[0]}, "end": {"dateTime": time[1]}}).execute()
        
if __name__ == '__main__':
    
    main()