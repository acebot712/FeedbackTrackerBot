from flask import Flask, request, jsonify
import os
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Constants
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SERVICE_ACCOUNT_FILE = os.environ["SERVICE_ACCOUNT_FILE"]

client = WebClient(token=SLACK_BOT_TOKEN)

# Replace with your desired range in the sheet
RANGE_NAME = 'Sheet1!A:D'

# Authenticate and construct service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=credentials)

def get_user_info(user_id):
    try:
        response = client.users_info(user=user_id)
        profile = response['user']['profile']
        user_name = profile.get('real_name', 'Unknown')
        user_email = profile.get('email', 'Unknown')
        return user_name, user_email
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")
        return 'Unknown', 'Unknown'

def write_feedback_to_google_sheet(date_time, user_info, text):
    user_name, user_email = user_info
    values = [[date_time, f"{user_name} <{user_email}>", text]]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption="RAW", body=body).execute()

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    event = data.get("event", {})
    if event.get("type") == "app_mention" or ("text" in event and "feedback" in event["text"].lower()):
        user_id = event["user"]
        text = event.get("text", "").replace(f"<@{client.api_call('auth.test')['user_id']}>", "").strip()
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_info = get_user_info(user_id)
        write_feedback_to_google_sheet(date_time, user_info, text)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
