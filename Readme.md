# WhatsApp Google Drive Assistant 🤖📁

A powerful Python-based assistant that allows you to manage your Google Drive through WhatsApp messages. Built with Flask, Google Drive API, and WhatsApp Business API.

![WhatsApp Drive Assistant](https://img.shields.io/badge/WhatsApp-Drive%20Assistant-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey)

## 🚀 Features

- **📁 File Management**: List, delete, move, and rename files in Google Drive
- **🤖 AI Summarization**: Get AI-powered summaries of PDF, DOCX, and TXT files
- **📱 WhatsApp Integration**: Complete control via WhatsApp messages
- **⬆️ File Uploads**: Upload files to Drive directly from WhatsApp
- **🔐 Secure Authentication**: OAuth2 and Service Account support
- **💾 Persistent Storage**: Token management for seamless operation

## Tech Stack

- **Backend**: Python, Flask
- **APIs**: WhatsApp Business API, Google Drive API v3
- **AI**: OpenAI GPT for file summarization
- **Authentication**: Google OAuth2, Service Accounts
- **Development**: Ngrok for webhook tunneling
- **File Processing**: PyPDF2, python-docx

## Prerequisites

- Python 3.8+
- WhatsApp Business Account
- Google Cloud Project with Drive API enabled
- OpenAI API account (for summaries)

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd whatsapp-drive-assistant
```
 2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Set up environment variables**   
   Create .env file:

```env
# WhatsApp Business API
WHATSAPP_TOKEN=your_whatsapp_business_token
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
```

# Google Drive
GOOGLE_CREDENTIALS_FILE=credentials.json

# OpenAI
OPENAI_API_KEY=your_openai_api_key
AI_MODEL=gpt-3.5-turbo

# Flask
SECRET_KEY=your_secret_key
PORT=5000

# Google Drive Setup
Option A: Service Account (Recommended)  
1. Go to [Google Cloud Console](https://developers.google.com/workspace/guides/create-credentials)   
2. Create Service Account with Editor role
3. Download JSON key as service_account.json
4. Share your Google Drive with the service account email

## Option B: OAuth 2.0
1. Enable Google Drive API
2. Create OAuth 2.0 Desktop Application credentials
3. Download as credentials.json

# WhatsApp Setup
### 3. Configure Webhook
- Go to **WhatsApp** → **Configuration** → **Webhook**
- Click **Edit**
- Enter:
  - **Callback URL**: `https://your-ngrok-url.ngrok.io/webhook`
  - **Verify Token**: `your_verify_token_from_env`
- Click **Verify and Save**
- Subscribe to **messages** events

### 4. Get Access Tokens
- Copy **Phone Number ID** and **Access Token** from WhatsApp Configuration
- Add to your `.env` file

## 🚀 Running the Application

### 1. Start the Flask App
```bash
python app.py
Start Ngrok (in separate terminal)
```

```bash
ngrok http 5000
Configure webhook with Ngrok URL
```

### 3. Configure Webhook
- Use the Ngrok HTTPS URL in your WhatsApp webhook configuration
- Example: `https://abc123-456.ngrok.io/webhook`

##  Available Commands

Send these commands to your WhatsApp Business number:

| Command | Description | Example |
|---------|-------------|---------|
| `HELP` | Show all commands | `HELP` |
| `LIST /folder` | List files in folder | `LIST /Documents` |
| `DELETE /file.pdf` | Delete a file | `DELETE /old.pdf` |
| `MOVE /file.pdf /folder` | Move file | `MOVE /file.pdf /Archive` |
| `SUMMARY /folder` | AI summary of files | `SUMMARY /Reports` |
| `RENAME old.pdf new.pdf` | Rename file | `RENAME doc.pdf new.pdf` |
| File + `UPLOAD /folder name.pdf` | Upload file | Send file with caption |

##  Project Structure
```
whatsapp-drive-assistant/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── google_drive/        # Google Drive integration
│   ├── drive_client.py
│   ├── auth.py
│   └── service_client.py
├── whatsapp/           # WhatsApp integration
│   ├── webhook.py
│   └── message_parser.py
├── ai/                 # AI summarization
│   └── summarizer.py
├── tokens/             # OAuth tokens storage
└── utils/              # Helper functions
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome page |
| `/health` | GET | Health check |
| `/webhook` | GET | Webhook verification |

## Troubleshooting

### Common Issues and Solutions

#### 1. 401 Unauthorized Error (WhatsApp)
**Problem**: Invalid or expired WhatsApp token
**Solution**:
- Get new token from Meta Developer Portal
- Update .env file with new token
- Restart the application

#### 2. Google OAuth Redirect URI Mismatch
**Problem**: `Error 400: redirect_uri_mismatch`
**Solution**:
- Use Service Account instead of OAuth
- Or add redirect URIs in Google Cloud Console

#### 3. Webhook Verification Failed
**Problem**: WhatsApp can't verify webhook
**Solution**:
- Ensure Verify Token matches exactly in .env and Meta
- Check Ngrok URL is HTTPS
- Verify Flask app is running

#### 4. File Upload Issues
- Check file size limits (WhatsApp: 100MB)
- Verify Google Drive permissions


**Problem**: Files not uploading to Drive
**Solution**:
- Check file size limits (WhatsApp: 100MB)
- Verify Google Drive permissions
- Ensure proper caption format: `UPLOAD /folder filename.pdf`

## Security Best Practices
- Never commit .env or token files to version control
- Use different tokens for development and production

### Token Management
- Rotate WhatsApp tokens regularly
- Use different tokens for development/production
- Store tokens securely in environment variables

##  Deployment

### Production Deployment with Gunicorn
1. Use production WSGI server (Gunicorn)

2. Set up proper SSL certificates

3. Use environment variables for configuration

4. Implement proper logging and monitoring

### Example Production Deployment:
```bash
# Install Gunicorn
pip install gunicorn
````

# Run with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
# Future Enhancements
- Multi-user support with OAuth

- File search functionality

- Folder creation commands

- File sharing via WhatsApp

- Advanced AI features (OCR, translation)

- Database integration for user management

- Rate limiting and usage analytics

# Contributing
1. Fork the repository

2. Create feature branch (git checkout -b feature/AmazingFeature)

3. Commit changes (git commit -m 'Add AmazingFeature')

4. Push to branch (git push origin feature/AmazingFeature)

5. Open a Pull Request

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Support
If you encounter any issues:

- Check the troubleshooting section

- Verify all API credentials

- Ensure all dependencies are installed

- Check Flask and Ngrok logs for errors

# Acknowledgments
- Google Drive API team

- WhatsApp Business API documentation

- OpenAI for AI capabilities

- Flask and Python communities

