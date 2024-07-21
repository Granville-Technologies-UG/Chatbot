import logging
from app import create_app

app = create_app()

if __name__ == "__main__":
    logging.info("Flask app started.")
    app.run(host="0.0.0.0", port=8000)

# import requests
# import json

# def send_whatsapp_image(recipient_number: str, image_link: str, image_caption: str, access_token: str) -> str:
#     """
#     Sends an image to a specified WhatsApp number using Meta's WhatsApp Cloud API.

#     Parameters:
#     recipient_number (str): The WhatsApp number of the recipient in international format (e.g., '256760238318').
#     image_link (str): The URL link to the image to be sent.
#     image_caption (str): The caption for the image.
#     access_token (str): The authorization token for Meta's WhatsApp Cloud API.

#     Returns:
#     str: The response from the API call, usually in JSON format indicating success or failure.
#     """

#     url = "https://graph.facebook.com/v19.0/111779138685682/messages"
    
#     payload = json.dumps({
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": recipient_number,
#         "type": "image",
#         "image": {
#             "link": image_link,
#             "caption": image_caption
#         }
#     })
    
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)
    
#     return response.text

# # Example usage:
# recipient_number = "256760238318"
# image_link = "https://imgur.com/a/FqO0eMZ"
# image_caption = "OpenAI LOGO"
# access_token = "EAAD1Mz1qtCkBOyFGu3GHKjJ5eidaqKWAZCFMnUoS6EBhxWjS1ZBoxJOztsVbOlXyDlE5WVerkfZAKsuhUIjSFNvpIuZCZASmPLhvh03xAhj3jBPviwxIYpdYqJZAyZBcv1xF5TbUkl92NR01cyaQVlbZCHLcMxHvgqlCNlE0nsLZBXdGphE1G5eWFzcT0uJPgVYCaYSDcfB9Dpgcsal7tUyEZD"

# response = send_whatsapp_image(recipient_number, image_link, image_caption, access_token)
# print(response)

