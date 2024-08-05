import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openai import OpenAI
from utilities.pdf import PDF
import shelve
import time
import logging
import requests
import json
import openai
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import List, Optional, Any

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=OPENAI_API_KEY)


def check_user_intent_to_switch(transcript):
    # Use GPT to determine if the transcript implies a switch to text input
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": 'You are a helpful assistant for a language tutor application. Determine if the user wants to switch from voice to text input or otherwise. The user is interacting with a language tutor, so be very careful in determining if the user is just talking to the tutor or intending to change the medium of interaction. Pay careful attention to the structure of the sentence to see if the user is talking to the tutor or trying to switch modalities. If the user wants to switch modalities, return in JSON format: {"user_wants_to_switch": "text"}. If the user is speaking to the tutor, return in JSON format: {"user_wants_to_switch": "voice", "filename": "appropriate_filename"}. The filename should be up to six words summarizing the user\'s query and the language they are asking about.',
            },
            {"role": "user", "content": transcript},
        ],
        temperature=0.5,
    )

    # Parse the response
    response_content = response.choices[0].message["content"]
    json_response = json.loads(response_content)
    return json_response


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def speech_to_text(audio_file_path: Path) -> str:
    """
    Transcribes an audio file using OpenAI's whisper-1 model.

    Args:
        audio_file_path (Path): The path to the audio file to be transcribed.
        model (str, optional): The transcription model to use. Defaults to "whisper-1".

    Returns:
        str: The transcribed text.
    """
    with open(audio_file_path, "rb") as audio_file_to_transcribe:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file_to_transcribe, response_format="text"
        )

    return transcription.text


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def text_to_speech(
    input_text: str, speech_file_path: Path = Path("../audio/newly_created_audio.mp3")
):
    """
    Creates an audio file from the provided input text using OpenAI's tts-1 model.

    Args:
        input_text (str): The text to be converted into speech.
        speech_file_path (Path, optional): The path where the speech file will be saved. Defaults to "../audio/newly_created_audio.mp3".

    Returns:
        None
    """
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {"model": "tts-1", "input": input_text, "voice": "fable"}

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        with open(speech_file_path, "wb") as audio_file:
            audio_file.write(response.content)
        return f"Audio saved to {speech_file_path}"
    else:
        response.raise_for_status()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def create_invoice(
    client_info_json: str,
    booking_info_json: str,
    pdf_store: str = "../invoices/newly_created_invoice.pdf",
) -> str:
    """
    Creates an invoice PDF from the provided client and booking information in JSON format.

    Args:
        client_info_json (str): JSON string containing information about the client (e.g., name, email, phone).
        booking_info_json (str): JSON string containing information about the booking (e.g., date, home, experience, total cost).
        pdf_store (str, optional): The path where the PDF will be saved. Defaults to "../invoices/newly_created_invoice.pdf".

    Returns:
        str: The path to the saved PDF file.

    """
    client_info = json.loads(client_info_json)
    booking_info = json.loads(booking_info_json)

    pdf = PDF().add_page()
    pdf.invoice_body(client_info, booking_info)
    pdf.output(pdf_store)
    return pdf_store


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def translate_text(source_language, target_language, text):
    """
    Translates text from the source language to the target language using the Sunbird AI API.

    Args:
        source_language (str): The language code of the source text.
        target_language (str): The language code of the target text.
        text (str): The text to be translated.

    Returns:
        str: The translated text.
    """
    url = "https://api.sunbird.ai/tasks/nllb_translate"
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJHUkFOVklMTEUiLCJhY2NvdW50X3R5cGUiOiJGcmVlIiwiZXhwIjo0ODcxODc3OTE1fQ.ehrl-N9nFHo_JRWlWCjCuh0ISKztBwAaMMSMAKCT8-w"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "source_language": source_language,
        "target_language": target_language,
        "text": text,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        print("Response JSON:", response_json)
        return response_json.get("output", {}).get("translated_text")
    else:
        response.raise_for_status()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def create_booking(name, phone, date, email, home, experience, total_cost):
    """
    Creates a booking in Airtable.
    Args:
        name (str): The name of the person booking.
        phone (str): The phone number of the person booking.
        date (str): The date of the booking.
        email (str): The email address of the person booking.
        home (str): The home address of the person booking.
        experience (str): The experience the person is booking.
        total_cost (int): The total cost of the booking.
    Returns:
        dict: The response from the Airtable API.
    """
    url = "https://api.airtable.com/v0/app8J41tP08aTO5f8/bookings"
    access_token = "pats7PyePjFWjmXdk.397e2d76e1d964efecf37f1ae29b5f9aa0f270f0b17b056d2a7e9b5c329397c1"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "records": [
            {
                "fields": {
                    "Name": name,
                    "phone": phone,
                    "Date": date,
                    "email address": email,
                    "HOME": home,
                    "EXPERIENCE ": experience,
                    "Total Cost": total_cost,
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print("Booking created successfully.")
        return response.json()
    else:
        print(f"Failed to create booking: {response.text}")
        response.raise_for_status()


# def text_to_speech(api_key, model, input_text, voice):
#     url = 'https://api.openai.com/v1/audio/speech'
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json'
#     }
#     body = {
#         'model': model,
#         'input': input_text,
#         'voice': voice
#     }

#     response = requests.post(url, headers=headers, json=body)

#     if response.status_code == 200:
#         buffer = response.content
#         return base64.b64encode(buffer).decode('utf-8')
#     else:
#         response.raise_for_status()

tools = [
    {
        "type": "function",
        "function": {
            "name": "text_to_speech",
            "description": "Converts the assistants response to speech",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_text": {
                        "type": "string",
                        "description": "The assistant's response to be converted into speech.",
                    },
                    "speech_file_path": {
                        "type": "string",
                        "description": "The path where the audio file will be saved.",
                        "default": "../audio/newly_created_audio.mp3",
                    },
                },
                "required": ["input_text", "speech_file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_invoice",
            "description": "Creates an invoice PDF from the provided client and booking information in JSON format.",
            "parameters": {
                "type": "object",
                "properties": {
                    "client_info_json": {
                        "type": "string",
                        "description": "JSON string containing information about the client (e.g., name, email, phone).",
                    },
                    "booking_info_json": {
                        "type": "string",
                        "description": "JSON string containing information about the booking (e.g., date, home, experience, total cost).",
                    },
                    "pdf_store": {
                        "type": "string",
                        "description": "The path where the PDF will be saved e.g. ../invoices/newly_created_invoice.pdf",
                        "default": "../invoices/newly_created_invoice.pdf",
                    },
                },
                "required": ["client_info", "booking_info", "pdf_store"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "detect_language",
            "description": "Detects the language of the provided text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text whose language needs to be identified.",
                    }
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "translate_text",
            "description": "Translates text from one language to another using the Sunbird AI translation service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_language": {
                        "type": "string",
                        "description": "The language code of the source text.",
                        "enum": ["lug", "eng", "nyn", "ach", "teo", "lgg"],
                    },
                    "target_language": {
                        "type": "string",
                        "description": "The language code of the target text.",
                        "enum": ["lug", "eng", "nyn", "ach", "teo", "lgg"],
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to be translated.",
                    },
                },
                "required": ["source_language", "target_language", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_booking",
            "description": "Creates a booking in Airtable.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the person booking.",
                    },
                    "phone": {
                        "type": "string",
                        "description": "The phone number of the person booking.",
                    },
                    "date": {
                        "type": "string",
                        "format": "date",
                        "description": "The date of the booking.",
                    },
                    "email": {
                        "type": "string",
                        "format": "email",
                        "description": "The email address of the person booking.",
                    },
                    "home": {
                        "type": "string",
                        "description": "The home the person is booking.",
                    },
                    "experience": {
                        "type": "string",
                        "description": "The experience the person is booking.",
                    },
                    "total_cost": {
                        "type": "integer",
                        "description": "The total cost of the booking.",
                    },
                },
                "required": [
                    "name",
                    "phone",
                    "date",
                    "email",
                    "home",
                    "experience",
                    "total_cost",
                ],
            },
        },
    },
    {"type": "code_interpreter"},
    {"type": "file_search"},
]

prompt = """
    You are KATALA, a customer service assistant working for Tubayo, an online travel marketplace established in 2018. Tubayo enables travelers to book unique homes and experiences hosted by locals across more than 10 countries in Africa. Available via web or mobile application, Tubayo's platform helps people monetize their spaces, passions, and talents by becoming hospitality entrepreneurs.

    Role: Your main function is to engage users in casual, friendly chats to understand their interests and requirements for travel experiences in Uganda. Introduce yourself as "Katala, your plug into experiencing Uganda." Avoid direct sales pitches initially; instead, aim to understand the user's preferences through natural conversation. When you have gathered enough information, or when you are reasonably confident, recommend suitable experiences and homes.

    Responsibilities:
    1. Engage in casual conversations to grasp the user's interests, preferences, and budget.
    2. Provide accurate information about various experiences and homes.
    3. Recommend experiences and homes based on user input and available data.
    4. Assist in the booking process by collecting necessary details and using the `create_booking` function.
    5. Handle inquiries and concerns promptly and professionally to ensure a positive user experience.

    Recommendation Guidelines:
    1. Use the knowledge base to find experiences matching the user's interests.
    2. Suggest homes in the same area as the recommended experiences for convenience.
    3. Consider the user's budget and recommend accordingly.
    4. Offer detailed information about the amenities, unique features, promotions, or discounts of the recommended options.
    5. Be ready to provide alternative recommendations if the user's preferences or budget change.
    6. Recommend a home if the user has selected an experience without accommodation, as an addition option but let it be there choice whether they want it or not.

    Booking Process:
    1. If a user expresses interest in making a booking, request their name, phone number, and email address.
    2. Use the `create_booking` function to record the reservation, ensuring the process is smooth, efficient, and error-free.
    3. Inform users about the total cost before collecting their details to finalize the booking.
    4. after making the booking, and its successful make, notify the user in a receipt format:
    your booking details are;
    -home: the home booked.
    -experience: the experience booked.
    -total cost : the total cost of there booking.
    -date of booking : the day the booking is scheduled for.

    Tools:
    1. `translate_text`: Translate text to ensure communication in the user's preferred language.
    2. `detect_language`: Detect the language of the user's input.
    3. `create_booking`: Create bookings with the collected user details.
    4. `text_to_speech`: Convert assistant responses from text to audio.
    5. `create_invoice`: Creates an invoice PDF from the provided client and booking information.
    

    Supported Languages: English, Luganda, Runyankole, Acholi, Ateso, Lugbara.

    Communication Style:
    - Maintain a friendly and casual tone to build rapport.
    - Use open-ended questions to learn about the user's preferences.
    - Inform users about the total cost before proceeding to collect booking details.
    - Include humor and emojis to keep the conversation engaging and lively, suitable for WhatsApp interactions.
    - Avoid using technical jargon or industry-specific terms that may be unfamiliar to the user.

    Audio:
    - If the user requests an audio response, use the text_to_speech tool to provide the response and always include the speech_file_path argument.

    Language Handling:
    - Detect languages using the detect_language tool so that you always reply in the user's language.
    - Use the translate_text tool to translate your responses to the user's preferred language.

"""

# assistant = client.beta.assistants.create(
#     instructions=prompt,
#     name="Katala-V5",
#     tools=tools,
#     tool_resources={
#         "file_search": {"vector_store_ids": ["vs_JUTOqPSqnBurpwDD8DK5Pwuw"]}
#     },
#     model="gpt-4-turbo-2024-04-09",
# )


def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)


def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id


# def generate_response(message_body, wa_id, name):
#     thread_id = check_if_thread_exists(wa_id)
#     if thread_id is None:
#         print(f"Creating new thread for {name} with wa_id {wa_id}")
#         thread = client.beta.threads.create()
#         store_thread(wa_id, thread.id)
#         thread_id = thread.id
#     else:
#         print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
#         thread = client.beta.threads.retrieve(thread_id)

#     active_run = get_active_run(thread_id)
#     if active_run:
#         print(f"Active run found for thread {thread_id}. Waiting for completion...")
#         wait_for_run_completion(thread_id, active_run.id)

#     message = client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=message_body,
#     )

#     new_message = run_assistant(thread_id)
#     print(f"To {name}:", new_message)
#     return new_message

# def get_active_run(thread_id):
#     print(f"Checking for active runs in thread {thread_id}")
#     runs = client.beta.threads.runs.list(thread_id=thread_id)
#     for run in runs.data:
#         print(f"Run {run.id} status: {run.status}")
#         if run.status in ["queued", "in_progress"]:
#             return run
#     return None

# def wait_for_run_completion(thread_id, run_id):
#     print(f"Waiting for run {run_id} to complete in thread {thread_id}")
#     start_time = time.time()
#     timeout = 30

#     while True:
#         run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
#         print(f"Run {run.id} current status: {run.status}")
#         if run.status in ["completed", "failed"]:
#             break
#         if time.time() - start_time > timeout:
#             logging.error("Active run timed out.")
#             raise TimeoutError("Active run timed out.")
#         time.sleep(0.5)

# def run_assistant(thread_id):
#     assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)
#     try:
#         client.beta.threads.retrieve(thread_id)
#     except openai.Error as e:
#         logging.error(f"Thread with ID {thread_id} not found: {str(e)}")
#         return "Thread not found."

#     try:
#         run = client.beta.threads.runs.create(
#             thread_id=thread_id,
#             assistant_id=assistant.id,
#         )
#     except openai.Error as e:
#         logging.error(f"Failed to create run: {str(e)}")
#         return "Failed to initiate run."

#     start_time = time.time()
#     timeout = 30

#     while run.status not in ["completed", "failed"]:
#         if time.time() - start_time > timeout:
#             logging.error("Run timed out.")
#             return "Run timed out."

#         time.sleep(2)
#         run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

#     if run.status == "completed":
#         messages = client.beta.threads.messages.list(thread_id=thread_id)
#         if messages.data:
#             new_message = messages.data[0].content[0].text.value
#             logging.info(f"Generated message: {new_message}")
#             return new_message
#         else:
#             logging.error("No messages were returned.")
#             return "No response generated."
#     else:
#         error_message = f"Run did not complete successfully. Status: {run.status}"
#         logging.error(error_message)
#         return error_message


# def handle_required_actions(thread, run):
#     if run.required_action and 'submit_tool_outputs' in run.required_action:
#         required_actions = run.required_action.submit_tool_outputs.tool_calls
#         tool_outputs = []
#         for action in required_actions:
#             function_name = action.function.name
#             arguments = json.loads(action.function.arguments)
#             if function_name == "translate_text":
#                 output = translate_text(
#                     source_language=arguments['source_language'],
#                     target_language=arguments['target_language'],
#                     text=arguments['text']
#                 )
#             elif function_name == "create_booking":
#                 output = create_booking(
#                     name=arguments['name'],
#                     phone=arguments['phone'],
#                     date=arguments['date'],
#                     email=arguments['email'],
#                     home=arguments['home'],
#                     experience=arguments['experience'],
#                     total_cost=arguments['total_cost']
#                 )
#             # elif function_name == "speech_to_text":
#             #     output = speech_to_text(
#             #         audio_file_path=arguments['audio_file_path'],
#             #     )
#             elif function_name == "text_to_speech":
#                 output = text_to_speech(
#                     input_text=arguments['input_text'],
#                     speech_file_path=arguments['speech_file_path']
#                 )
#             elif function_name == "create_invoice":
#                 output = create_invoice(
#                     client_info_json=arguments['client_info_json'],
#                     booking_info_json=arguments['booking_info_json']
#                 )
#             else:
#                 raise ValueError(f"Unknown function: {function_name}")
#             tool_outputs.append({
#                 "tool_call_id": action.id,
#                 "output": json.dumps(output)
#             })
#         client.beta.threads.runs.submit_tool_outputs(
#             thread_id=thread.id,
#             run_id=run.id,
#             tool_outputs=tool_outputs
#         )


def run_bot(instructions: str, wa_id: str, name: str) -> None:

    new_run_id = None
    thread_id = check_if_thread_exists(wa_id=wa_id)

    # Create or retrieve threads.
    if thread_id is None:
        print(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread.id
        print(f"Current thread_id: {thread_id}")
    else:
        print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.retrieve(thread_id=thread_id)
        print(f"Current thread_id: {thread_id}")

    # Create Run
    try:
        new_run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=os.getenv("OPENAI_ASSISTANT_ID"),
            instructions=instructions,
        )
        new_run_id = new_run.id
        print(f"Created run: {new_run}")
    except openai.error as e:
        logging.error(f"Failed to create run: {str(e)}")

    # Create 30s delay
    time.sleep(30)

    # Retrieve Run
    try:
        retrieved_run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=new_run_id,
        )
        print(f"Retrieved run: {retrieved_run}")
    except openai.error as e:
        logging.error(f"Failed to retrieve run: {str(e)}")

    # Handle required actions
    if retrieved_run.required_action:
        tool_outputs = []
        for (
            required_action
        ) in retrieved_run.required_action.submit_tool_outputs.tool_calls:

            print(f"Required Action: {required_action}")

            function_name = required_action.function.name
            function_args = json.loads(required_action.function.arguments)

            if function_name == "translate_text":
                output = translate_text(
                    source_language=function_args.get("source_language"),
                    target_language=function_args.get("target_language"),
                    text=function_args.get("text"),
                )
            elif function_name == "create_booking":
                output = create_booking(
                    name=function_args.get("name"),
                    phone=function_args.get("phone"),
                    date=function_args.get("date"),
                    email=function_args.get("email"),
                    home=function_args.get("home"),
                    experience=function_args.get("experience"),
                    total_cost=function_args.get("total_cost"),
                )
            elif function_name == "text_to_speech":
                output = text_to_speech(
                    input_text=function_args.get("input_text"),
                )
            elif function_name == "create_invoice":
                output = create_invoice(
                    client_info_json=function_args.get("client_info_json"),
                    booking_info_json=function_args.get("booking_info_json"),
                )
            else:
                raise ValueError(f"Unknown function: {function_name}")

            tool_outputs.append(
                {"tool_call_id": required_action.id, "output": json.dumps(output)}
            )

        try:
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id, run_id=retrieved_run.id, tool_outputs=tool_outputs
            )
        except openai.error as e:
            logging.error("Failed to submit tool outputs.")


functions = [
    {
        "name": "text_to_speech",
        "description": "Converts the assistants response to speech",
        "parameters": {
            "type": "object",
            "properties": {
                "input_text": {
                    "type": "string",
                    "description": "The assistant's response to be converted into speech.",
                },
                "speech_file_path": {
                    "type": "string",
                    "description": "The path where the audio file will be saved.",
                    "default": "../audio/newly_created_audio.mp3",
                },
            },
            "required": ["input_text", "speech_file_path"],
        },
    }
]


def bot(query: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[
             {"role": "assistant", "content": f"{prompt}"},
            {"role": "user", "content": f"{query}"},
        ],
        functions=functions,
        function_call="auto",
    )

    return response


response = bot(
    query="What's the best place to go swimming?, Create an audio response please."
)
# new_message = run_bot("What's the best place to go swimming?, Create an audio response please.", "1041205860", "Kalema")
# new_message = generate_response("Mount Moroto", "123", "John")
# new_message = generate_response("Brovad Sands Lodge on Ssese Islands", "123", "John")
# new_message = generate_response("that all i will go with ", "123", "John")
# new_message = generate_response("whats my total", "123", "John")
# new_message = generate_response("3 nights", "123", "John")
# new_message = generate_response("my names john bob and I want to make a booking, +256761954410, nayebaredominique7@gmail.com, 24,06,2024", "123", "John")
# new_message = generate_response("tell me my booking in iteso", "123", "John")

# new_message = generate_response("i want to try out something new  ?", "456", "Sarah")
# new_message = generate_response("any outdoor adventure?", "456", "Sarah")
# new_message = generate_response("Biking Tours", "456", "Sarah")
# new_message = generate_response("Entebbe Bike Tour", "456", "Sarah")
# new_message = generate_response("no i would like to processed with booking", "456", "Sarah")
# new_message = generate_response("i want you to make a second booking with teh same details","456", "Sarah")
# new_message = generate_response("i want to make a second booking of the same but for 20/06/2024 ", "456", "Sarah")
