# LINE-Bot Project

Introducing Aikomiawase Aiko!

This project is a LINE chatbot designed to interact with users, provide meaningful responses, and manage chat history using Pantry Cloud as a lightweight backend. The bot can intelligently process group and personal messages and is configurable for specific triggers, such as responding to mentions of a specific keyword (e.g., "Aiko").

---

## Table of Contents
1. [Features](#features)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Configuration](#configuration)
4. [Code Structure](#code-structure)
5. [Acknowledgements](#acknowledgements)
6. [Plans of Improvements](#plans-of-improvements)
7. [Scan to Add the Bot](#scan-to-add-the-bot)
8. [References](#references)

---

## Features
- **User and Group Interaction**: Responds differently based on the source of the message (user or group).
- **Keyword Detection**: Detects specific keywords (e.g., variations of "Aiko") in group messages to trigger responses.
- **Chat History Management**: Utilizes Pantry Cloud to store and sync chat history and AI model responses.
- **AI-Powered Responses**: Integrates with Google’s Gemini model to generate intelligent and contextual responses.
- **Configurable Maximum Messages**: Limits the number of stored messages per chatroom for efficient memory usage (maximum of 15 messages from the user and the bot).

---

## Getting Started

### Prerequisites
- Python 3.12+
- Creating a Line Official Account
- Pantry Cloud account for backend storage
- FastAPI and Vercel for hosting the webhook endpoint
- Gemini API Key

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/JeftaAdriel/line-bot.git
   cd line-bot
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
   LINE_CHANNEL_SECRET=your_line_channel_secret
   PANTRY_ID=your_pantry_id
   VERCEL_TOKEN=your_vercel_token if you choose to host in Vercel
   ```

---

## Configuration

Modify the `configuration.py` file to set project-wide settings:
- **BOT_FULL_NAME**: The full name of the bot.
- **BOT_CALL_NAME**: The name the bot will use when responding.
- **SYSTEM_PROMPT**: The persona of the bot (how the bot will respond).
- **MAX_MESSAGE**: The maximum number of messages stored in chat history.
- **Model Related Part**: Which AI Model do you want to use.

---

## Code Structure

```
line-bot/
|-- configuration.py             # Configuration settings
|-- __init__.py                  # Just here I suppose
|-- requirements.txt             # Python dependencies
|-- vercel.json                  # Vercel configuration
|-- readme.md                    # Readme settings
|-- .env                         # Store API Key and other credentials
|-- .gitignore                   # Make sure to not commit redundant files and folders (.venv, __pycache__, etc) and confidential files (.env)
|-- api/
    |-- webhook.py               # The main code
|-- utils/
    |-- line_related.py          # Helper functions for LINE API interactions
    |-- memory.py                # Functions for managing chat history and Pantry syncing
    |-- database_pantry.py       # Functions or wrapper for Pantry utilities (create basket, update basket, etc.)
|-- services/
    |-- llm_models/
        |-- model.py             # AI model integration logic
        |-- response_parser.py   # Extract parts from model responses (TODO)
    |-- chatbot/
        |-- chatbot.py           # Logic for the chatbot process (TODO)
    |-- dependencies.py          # Dependencies for the project (TODO)
```

---

## Acknowledgements

This project was heavily inspired by Muhammad Nur Ichsan’s LINE chatbot implementation ([Sara-Vanasi](https://gitlab.com/mnurichsan49/sara-vanasi)).

---

## Plans of Improvements

Feature Wise:
1. Making the bot able to process input other than text (image, documents, videos) and output other than text
2. Integrating a search API (google, tavily, ... IDK yet), trace.moe API, and waifu.it API
3. Making the bot able to keep in a mind for a to-do list of the user

Code Wise:
1. Refactoring the code for better code quality
2. Add documentation for the functions and classes for better readibility

---

## Scan to Add the Bot

Experience the bot firsthand on your LINE app using one of these simple methods:

1. Directly scan the QR Code below

<div align="center">
  <img src="https://qr-official.line.me/gs/M_590wfnrk_GW.png" alt="LINE Bot QR Code" style="max-width: 200px;">
</div>

2. Click the button below and then scan the QR Code displayed on the website

<div align=center> <a href="https://lin.ee/I1ALAga"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/id.png" alt="Berteman" height="36" border="0"></a>
</div>

3. Search for an official account by ID:
- Tap the Add friends icon at the top right of the Home tab > Search > ID.
- Search for the official account you want to add by entering <b> <u> @590wfnrk </u> </b>
- Tap "Add" and you're good to go!

---

## References

1. https://developers.line.biz/en/reference/messaging-api/
2. https://gitlab.com/mnurichsan49

---