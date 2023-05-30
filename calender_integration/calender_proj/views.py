from django.shortcuts import render
from googleapiclient.discovery import build
from django.http import HttpResponse
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = '678207984088-0ue09i7uo43d38end9sdma2tq7ee52p9.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect/'

class GoogleCalendarInitView:
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly']
        )
        authorization_url, _ = flow.authorization_url(prompt='consent')
        return HttpResponse(f"Please go to: {authorization_url}")

class GoogleCalendarRedirectView:
    def get(self, request):
        code = request.GET.get('code')
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly']
        )
        flow.fetch_token(
            token_uri='https://oauth2.googleapis.com/token',
            code=code,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI
        )
        credentials = flow.credentials

        # Use the credentials to access the Google Calendar API and retrieve events
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        # Process the events as needed
        for event in events:
            print(event['summary'])

        return HttpResponse("Events retrieved successfully.")
