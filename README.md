
# FeedbackTracker

FeedbackTracker is a Slack bot that logs feedback messages from Slack channels into a Google Sheets document. This project is built using Flask, Google Sheets API, and Slack API.

## Features

- Listens for feedback messages in Slack channels.
- Logs feedback messages along with the user's name, email, and timestamp into a Google Sheets document.

## Prerequisites

- Python 3.9+
- A Google Cloud Platform project with Google Sheets API enabled.
- A Slack workspace with a Slack app that has the necessary permissions.

## Setup

### Google Sheets API Setup

1. **Create a Project in Google Cloud Console:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.

2. **Enable Google Sheets API:**
   - In the Google Cloud Console, go to the API & Services Dashboard.
   - Click on "Enable APIs and Services."
   - Search for "Google Sheets API" and enable it.

3. **Create Credentials:**
   - Go to "Credentials" in the API & Services section.
   - Click "Create Credentials" and select "Service Account."
   - Fill in the required information and create the service account.
   - After creating the service account, create a key for it (preferably JSON).

4. **Share Your Google Sheet with the Service Account:**
   - Open your Google Sheet.
   - Click "Share" and add the email address of your service account (found in the JSON file) with edit access.

### Slack App Setup

1. **Create a Slack App:**
   - Go to the [Slack API](https://api.slack.com/) dashboard.
   - Create a new app.

2. **Add Bot Scopes:**
   - Go to "OAuth & Permissions" and add the following scopes:
     - `channels:history`
     - `chat:write`
     - `app_mentions:read`
     - `users:read`
     - `users:read.email`

3. **Enable Event Subscriptions:**
   - Go to "Event Subscriptions."
   - Enable events and set the Request URL to `http://<your-server-ip>:5000/slack/events`.
   - Subscribe to the following bot events:
     - `app_mention`
     - `message.channels`

4. **Install the App:**
   - Install the app to your Slack workspace and copy the OAuth token.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/FeedbackTracker.git
   cd FeedbackTracker
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file in the project root and add the following variables:
   ```plaintext
   SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
   SPREADSHEET_ID=your-google-sheets-id
   SERVICE_ACCOUNT_FILE=path/to/your/service-account-file.json
   ```

## Running the Application

1. **Start the Flask Application:**
   ```bash
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

2. **Use ngrok for HTTPS (if needed):**
   ```bash
   ngrok http 5000
   ```

## Usage

- Mention the bot in any Slack channel with your feedback.
- The bot will log the feedback, along with your name, email, and the timestamp, into the specified Google Sheets document.

## Example

### Feedback Message in Slack

```
@FeedbackTrackerBot I love UGC!
```

### Logged in Google Sheets

| Date Time           | User Name          | Feedback               |
|---------------------|--------------------|------------------------|
| 2024-07-15 08:56:20 | Abhijoy Sarkar <abhijoy.sar@gmail.com> | I love UGC! |

## Contributing

Contributions are welcome! Please create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
