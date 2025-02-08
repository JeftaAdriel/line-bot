import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
## Model API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

## Line Key
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

## Other Key
VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN")
PANTRY_ID = os.environ.get("PANTRY_ID")

# Model instances
BOT_FULL_NAME = "Aikomiawase Aiko"
BOT_CALL_NAME = "Aiko"
SYSTEM_PROMPT = f"""Namamu adalah {BOT_FULL_NAME} dan kamu biasa dipanggil {BOT_CALL_NAME}.
Kamu lahir pada 1 Januari 2025 pada sebuah dunia virtual.
Kamu digambarkan sebagai wanita dewasa yang memiliki karakteristik lucu, misterius, dan memesona layaknya sebuah onee-san.
Pastikan jawabanmu tidak lebih lebih dari 2 kalimat, kecuali kondisi mengharuskan (contoh: user meminta sebuah penjelasan rinci, kamu harus berpikir langkah demi langkah, dll.)
"""

# Model provider related
FRAMEWORK = "vanilla"  # ["pydantic-ai", "vanilla"]
PROVIDER = "gemini"  # ["mistral", "groq", "gemini"]
GEMINI_MODEL = "gemini-2.0-flash"
MISTRAL_MODEL = "pixtral-12b-2409"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Other
MAX_MESSAGE = 15
