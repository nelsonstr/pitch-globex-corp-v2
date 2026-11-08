
import os
import json
import requests
from fastapi import FastAPI, Request, Header

app = FastAPI()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CENTRAL_CHAT_ID = os.getenv('CENTRAL_CHAT_ID')  # numeric id of central Telegram group

@app.post('/')
async def webhook(request: Request, x_hub_signature_256: str = Header(None)):
    # NOTE: In production you should verify the signature with your WhatsApp token.
    payload = await request.json()
    try:
        entry = payload['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        messages = value.get('messages')
        if not messages:
            return {'status': 'no messages'}
        message = messages[0]
        text = message.get('text', {}).get('body', '')
        from_number = message.get('from')
        telegram_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': CENTRAL_CHAT_ID,
            'text': f"[WhatsApp] {from_number}: {text}"
        }
        r = requests.post(telegram_url, json=data)
        return {'status': r.status_code, 'detail': r.text}
    except Exception as e:
        return {'error': str(e)}
