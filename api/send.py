from flask import Request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

import os
import json

if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
        # etc...
    })
    firebase_admin.initialize_app(cred)

def handler(request: Request):
    data = request.get_json()
    message = messaging.Message(
        notification=messaging.Notification(
            title=data.get('title', 'Default Title'),
            body=data.get('body', 'Default Body')
        ),
        topic=data.get('topic', 'global')
    )
    response = messaging.send(message)
    return jsonify({"success": True, "response": response})
