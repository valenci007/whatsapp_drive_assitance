from flask import Flask, request, jsonify
import os
from config import Config
from whatsapp.webhook import WhatsAppWebhook
from whatsapp.message_parser import WhatsAppMessageParser

app = Flask(__name__)
app.config.from_object(Config)

# Initialize components
whatsapp = WhatsAppWebhook()
message_parser = WhatsAppMessageParser()

# Initialize Google Drive client with error handling
drive_client = None
ai_summarizer = None

try:
    from google_drive.drive_client import GoogleDriveClient
    from ai.summarizer import AISummarizer

    drive_client = GoogleDriveClient(Config.GOOGLE_CREDENTIALS_FILE, Config.DRIVE_TOKEN_FILE)
    ai_summarizer = AISummarizer()
except Exception as e:
    print(f"⚠️  Google Drive not available: {e}")
    print("📱 WhatsApp commands will work, but Drive features will be disabled")


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == Config.WHATSAPP_VERIFY_TOKEN:
            return challenge
        return 'Verification failed', 403

    elif request.method == 'POST':
        data = request.get_json()
        print("Received webhook:", data)

        webhook_data = whatsapp.process_webhook(data)
        if webhook_data:
            process_user_message(webhook_data)

        return 'OK', 200


def process_user_message(webhook_data):
    """Process user message and execute commands"""
    user_id = webhook_data['from']

    try:
        if webhook_data['type'] == 'text':
            message = webhook_data['message']
            parsed = message_parser.parse_message(message)

            response = execute_command(parsed)
            whatsapp.send_message(user_id, response)

    except Exception as e:
        error_msg = f" Error processing your request: {str(e)}"
        whatsapp.send_message(user_id, error_msg)


def execute_command(parsed_command):
    """Execute the parsed command"""
    command = parsed_command['command']

    # Check if Drive is available for Drive-related commands
    drive_commands = ['LIST', 'DELETE', 'MOVE', 'SUMMARY', 'RENAME', 'UPLOAD_TEXT']
    if command in drive_commands and drive_client is None:
        return " Google Drive is not configured. Please check the server setup."

    try:
        if command == 'LIST':
            return drive_client.list_files(parsed_command['folder_path'])

        elif command == 'DELETE':
            return drive_client.delete_file(parsed_command['file_path'])

        elif command == 'MOVE':
            return drive_client.move_file(parsed_command['source_path'], parsed_command['dest_path'])

        elif command == 'SUMMARY':
            return ai_summarizer.summarize_folder(drive_client, parsed_command['folder_path'])

        elif command == 'RENAME':
            return drive_client.rename_file(parsed_command['current_name'], parsed_command['new_name'])

        elif command == 'HELP':
            return message_parser.get_help_message()

        elif command == 'UNKNOWN':
            return f" Unknown command: {parsed_command['message']}\n\nType 'HELP' for available commands."

    except Exception as e:
        return f" Error executing command: {str(e)}"


@app.route('/health', methods=['GET'])
def health_check():
    drive_status = "connected" if drive_client else "disconnected"
    return jsonify({
        'status': 'healthy',
        'service': 'WhatsApp Drive Assistant',
        'drive_status': drive_status
    })


@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Drive Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
            .success { background: #d4edda; color: #155724; }
            .info { background: #d1ecf1; color: #0c5460; }
        </style>
    </head>
    <body>
        <h1>🤖 WhatsApp Drive Assistant</h1>
        <div class="status success">✅ Service is running</div>
        <div class="status info">📞 Webhook: <a href="/webhook">/webhook</a></div>
        <div class="status info">❤️ Health: <a href="/health">/health</a></div>

        <h2>Available Commands:</h2>
        <ul>
            <li><code>HELP</code> - Show all commands</li>
            <li><code>LIST /</code> - List root directory</li>
            <li><code>SUMMARY /</code> - AI summary of files</li>
            <li><code>DELETE /filename.pdf</code> - Delete a file</li>
            <li><code>RENAME old.pdf new.pdf</code> - Rename file</li>
            <li>Send file with caption: <code>UPLOAD /Folder filename.pdf</code></li>
        </ul>

        <p><strong>Ngrok URL:</strong> https://abc123-456.ngrok.io</p>
    </body>
    </html>
    """


if __name__ == '__main__':
    os.makedirs('tokens', exist_ok=True)
    if not drive_client:
        print("Google Drive: Not connected - some features disabled")
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)

