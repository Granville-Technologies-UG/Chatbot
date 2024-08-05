import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import requests
from services.openai_service import generate_response
import re
import logging
from flask import current_app, jsonify
import json
import requests
from requests_toolbelt import MultipartEncoder


def transcript_audio(media_id):
    token = os.getenv("ACCESS_TOKEN")
    try:
        # Fetch the media URL using the media ID
        media_response = requests.get(
            f"https://graph.facebook.com/v19.0/{media_id}?access_token={token}"
        )
        media_response.raise_for_status()
        media_url = media_response.json()["url"]
        # Download the audio file
        file_response = requests.get(
            media_url, headers={"Authorization": f"Bearer {token}"}, stream=True
        )
        file_response.raise_for_status()
        # Prepare the file for transcription
        multipart_data = MultipartEncoder(
            fields={
                "file": ("grabacion.ogg", file_response.content, "audio/ogg"),
                "model": ("model", "whisper-1"),
            }
        )
        # Send the file for transcription
        openai_response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_TOKEN')}",
                "Content-Type": multipart_data.content_type,
            },
            data=multipart_data,
        )
        openai_response.raise_for_status()
        return openai_response.json()["text"]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise


def upload_whatsapp_media(
    phone_number_id: str, file_path: str, file_type: str, access_token: str
) -> str:
    """
    Uploads media to WhatsApp using Meta's WhatsApp Cloud API.

    Parameters:
    phone_number_id (str): The phone number ID associated with your WhatsApp business account.
    file_path (str): The local path to the file to be uploaded.
    file_type (str): The MIME type of the file (e.g., 'image/jpeg').
    access_token (str): The authorization token for Meta's WhatsApp Cloud API.

    Returns:
    str: The media ID of the uploaded file if successful.
    """

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/media"

    files = {
        "file": ("file", open(file_path, "rb")),
        "type": (None, file_type),
        "messaging_product": (None, "whatsapp"),
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        media_id = response.json().get("id")
        return media_id
    else:
        raise Exception(f"Error uploading media: {response.text}")


# TODO: Find out why the image isn't received even after a successful POST request.
def send_whatsapp_image(
    recipient_number: str, image_link: str, image_caption: str, access_token: str
) -> str:
    """
    Sends an image to a specified WhatsApp number using Meta's WhatsApp Cloud API.

    Parameters:
    recipient_number (str): The WhatsApp number of the recipient in international format (e.g., '256760238318').
    image_link (str): The URL link to the image to be sent.
    image_caption (str): The caption for the image.
    access_token (str): The authorization token for Meta's WhatsApp Cloud API.

    Returns:
    str: The response from the API call, usually in JSON format indicating success or failure.
    """

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_number,
            "type": "image",
            "image": {"link": image_link, "caption": image_caption},
        }
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def send_whatsapp_document(
    recipient_number: str,
    document_link: str,
    document_caption: str,
    document_filename: str,
    access_token: str,
) -> str:
    """
    Sends a document to a specified WhatsApp number using Meta's WhatsApp Cloud API.

    Parameters:
    recipient_number (str): The WhatsApp number of the recipient in international format (e.g., '256760238318').
    document_link (str): The URL link to the document to be sent.
    document_caption (str): The caption for the document.
    document_filename (str): The name of the document file to be displayed in WhatsApp.
    access_token (str): The authorization token for Meta's WhatsApp Cloud API.

    Returns:
    str: The response from the API call, usually in JSON format indicating success or failure.
    """

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_number,
            "type": "document",
            "document": {
                "link": document_link,
                "caption": document_caption,
                "filename": document_filename,
            },
        }
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except requests.RequestException as e:
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    pattern = r"\【.*?\】"
    text = re.sub(pattern, "", text).strip()
    pattern = r"\*\*(.*?)\*\*"
    replacement = r"*\1*"
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    response = generate_response(message_body, wa_id, name)
    response = process_text_for_whatsapp(response)

    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
