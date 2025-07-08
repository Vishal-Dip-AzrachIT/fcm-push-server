from flask import jsonify, Request
import firebase_admin
from firebase_admin import credentials, messaging
import os

# Only initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": os.environ["FIREBASE_TYPE"],
        "project_id": os.environ["FIREBASE_PROJECT_ID"],
        "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
        "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace('\\n', '\n'),
        "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
        "client_id": os.environ["FIREBASE_CLIENT_ID"],
        "auth_uri": os.environ["FIREBASE_AUTH_URI"],
        "token_uri": os.environ["FIREBASE_TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": os.environ["FIREBASE_CLIENT_X509_CERT_URL"],
        "universe_domain": os.environ["FIREBASE_UNIVERSE_DOMAIN"]
    })
    firebase_admin.initialize_app(cred)

# Main handler function
def handler(request: Request):
    try:
        data = request.get_json()

        title = data.get("title", "Default Title")
        body = data.get("body", "Default Body")
        topic = data.get("topic", "global")

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            topic=topic
        )

        response = messaging.send(message)
        return jsonify({"success": True, "response": response}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

