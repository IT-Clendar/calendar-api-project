import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    # 인증
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Google Calendar API 연결
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # 출력
    if not events:
        print("예정된 일정이 없습니다.")
        return

    for event in events:
        summary = event.get('summary', '제목 없음')
        location = event.get('location', '장소 없음')
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')

        if start and end:
            start_dt = datetime.datetime.fromisoformat(start)
            end_dt = datetime.datetime.fromisoformat(end)
            time_str = f"{start_dt.strftime('%Y-%m-%d %H시')}~{end_dt.strftime('%H시')}"
        else:
            time_str = event['start'].get('date', '날짜 없음') + " (종일)"

        print(f"1. 일정: {summary}")
        print(f"2. 시간: {time_str}")
        print(f"3. 장소: {location}")
        print("===")

if __name__ == '__main__':
    main()