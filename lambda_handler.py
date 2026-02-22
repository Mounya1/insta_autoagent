import json
import os
import logging
from datetime import datetime
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
IG_ID = os.getenv('INSTAGRAM_USER_ID')
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN', 'your_verify_token')
BRAND_NAME = os.getenv('BRAND_NAME', 'YourBrand')

GRAPH_API_BASE = "https://graph.instagram.com/v24.0"
MESSAGES_ENDPOINT = f"{GRAPH_API_BASE}/{IG_ID}/messages"

stats = {"total_received": 0, "total_sent": 0, "total_errors": 0}
processed_messages = set()

def handler(event, context):
    try:
        logger.info(f"Event: {json.dumps(event)}")
        
        http_method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod', 'GET')
        path = event.get('rawPath') or event.get('path', '/')
        
        if 'webhook' in path or path == '/':
            if http_method == 'GET':
                return handle_verification(event)
            elif http_method == 'POST':
                return handle_webhook(event)
        elif 'health' in path:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'status': 'healthy',
                    'service': 'instagram-autodm',
                    'timestamp': datetime.now().isoformat()
                })
            }
        elif 'stats' in path:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'stats': stats, 'timestamp': datetime.now().isoformat()})
            }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': f'<h1>Instagram Auto-DM Active</h1><p>Brand: {BRAND_NAME}</p><p>Endpoints: /webhook, /health, /stats</p>'
        }
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def handle_verification(event):
    try:
        params = event.get('queryStringParameters') or {}
        mode = params.get('hub.mode')
        token = params.get('hub.verify_token')
        challenge = params.get('hub.challenge')
        
        logger.info(f"Verification: mode={mode}")
        
        if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
            logger.info("Verification success")
            return {'statusCode': 200, 'body': challenge}
        
        return {'statusCode': 403, 'body': 'Forbidden'}
    except Exception as e:
        logger.error(f"Verification error: {e}")
        return {'statusCode': 500, 'body': str(e)}

def handle_webhook(event):
    try:
        body = event.get('body', '{}')
        data = json.loads(body) if isinstance(body, str) else body
        
        logger.info("Webhook received")
        stats['total_received'] += 1
        
        if 'entry' in data:
            for entry in data['entry']:
                if 'messaging' in entry:
                    for msg_event in entry['messaging']:
                        process_message(msg_event)
        
        return {'statusCode': 200, 'body': json.dumps({'status': 'ok'})}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        stats['total_errors'] += 1
        return {'statusCode': 500, 'body': str(e)}

def process_message(event):
    try:
        sender_id = event.get('sender', {}).get('id')
        message = event.get('message', {})
        message_id = message.get('mid')
        message_text = message.get('text', '')
        
        if not message_text or message_id in processed_messages:
            return
        
        processed_messages.add(message_id)
        logger.info(f"Message from {sender_id}: {message_text}")
        
        reply = generate_reply(message_text)
        send_dm(sender_id, reply)
    except Exception as e:
        logger.error(f"Process error: {e}")

def generate_reply(text):
    t = text.lower().strip()
    
    if any(w in t for w in ["hi", "hello", "hey"]):
        return f"Hi! 👋 Welcome to {BRAND_NAME}! How can I help?"
    if any(w in t for w in ["price", "cost", "how much"]):
        return "All prices are on our posts! 💰 Looking for something specific?"
    if any(w in t for w in ["ship", "delivery"]):
        return "📦 We ship fast! 3-5 business days."
    if any(w in t for w in ["return", "refund"]):
        return "We have hassle-free returns! 😊 Share your order number."
    if any(w in t for w in ["discount", "coupon"]):
        return "🏷️ Follow us for exclusive deals!"
    
    return f"Thanks for contacting {BRAND_NAME}! How can I help?"

def send_dm(recipient_id, text):
    try:
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": text[:1000]}
        }
        
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(MESSAGES_ENDPOINT, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info("Reply sent")
            stats['total_sent'] += 1
            return True
        
        logger.error(f"Send failed: {response.status_code}")
        stats['total_errors'] += 1
        return False
    except Exception as e:
        logger.error(f"Send error: {e}")
        stats['total_errors'] += 1
        return False