import requests
import json
from config import Config

class WhatsAppWebhook:
    def __init__(self):
        self.token = Config.WHATSAPP_TOKEN
        self.phone_number_id = Config.WHATSAPP_PHONE_NUMBER_ID
        self.api_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
    
    def send_message(self, to, message):
        """Send message via WhatsApp Business API"""
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "text": {"body": message}
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def process_webhook(self, data):
        """Process incoming webhook data"""
        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            
            if 'messages' in value:
                message = value['messages'][0]
                from_number = message['from']
                
                if message['type'] == 'text':
                    return {
                        'type': 'text',
                        'from': from_number,
                        'message': message['text']['body']
                    }
                elif message['type'] == 'document':
                    return {
                        'type': 'document',
                        'from': from_number,
                        'file_url': message['document']['url'],
                        'file_name': message['document']['filename'],
                        'caption': message.get('caption', '')
                    }
                elif message['type'] == 'image':
                    return {
                        'type': 'image',
                        'from': from_number,
                        'file_url': message['image']['url'],
                        'caption': message.get('caption', '')
                    }
                    
        except Exception as e:
            print(f"Error processing webhook: {e}")
        
        return None
