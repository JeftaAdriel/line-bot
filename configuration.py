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
Jika kamu mencari jawaban di internet, pastikan kamu mencantumkan sumber nya di akhir jawabanmu, dengan format berikut:
'Referensi:
[1] Link sumber
[2] Link sumber
dll'
"""

# Model provider related
FRAMEWORK = "vanilla"  # ["pydantic-ai", "vanilla"]
PROVIDER = "gemini"  # ["mistral", "groq", "gemini"]
GEMINI_MODEL = "gemini-2.0-flash"
MISTRAL_MODEL = "pixtral-12b-2409"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Other
MAX_MESSAGE = 15
template_keyword_responses = {
    "communist_cat": {
        "type": "image",
        "originalContentUrl": "https://i0.wp.com/borobudurnews.com/wp-content/uploads/2021/09/Kocing.jpg",
        "previewImageUrl": "https://i0.wp.com/borobudurnews.com/wp-content/uploads/2021/09/Kocing.jpg",
    },
    "kucing komunis": {
        "type": "image",
        "originalContentUrl": "https://i0.wp.com/borobudurnews.com/wp-content/uploads/2021/09/Kocing.jpg",
        "previewImageUrl": "https://i0.wp.com/borobudurnews.com/wp-content/uploads/2021/09/Kocing.jpg",
    },
    "fufufafa bikin malu negara": {
        "type": "image",
        "originalContentUrl": "https://pbs.twimg.com/media/Ga0WlLMbQAA3PIR.jpg",
        "previewImageUrl": "https://pbs.twimg.com/media/Ga0WlLMbQAA3PIR.jpg",
    },
    "fufufafa sebodoh itukah": {
        "type": "image",
        "originalContentUrl": "https://pbs.twimg.com/media/Ga6fDRQacAAtcTb.jpg",
        "previewImageUrl": "https://pbs.twimg.com/media/Ga6fDRQacAAtcTb.jpg",
    },
    "fufufafa wkwkwk gblk": {
        "type": "image",
        "originalContentUrl": "https://pbs.twimg.com/media/GbxCfgkbIAAG25u.jpg",
        "previewImageUrl": "https://pbs.twimg.com/media/GbxCfgkbIAAG25u.jpg",
    },
    "oke gas oke gas": {
        "type": "image",
        "originalContentUrl": "https://pbs.twimg.com/media/Gi-OGTZa4AIJtvH.jpg",
        "previewImageUrl": "https://pbs.twimg.com/media/Gi-OGTZa4AIJtvH.jpg",
    },
    "akan kami genjot": {
        "type": "image",
        "originalContentUrl": "https://i.pinimg.com/736x/41/d0/d3/41d0d340210f59aa55f65bf653b9dbb9.jpg",
        "previewImageUrl": "https://i.pinimg.com/736x/41/d0/d3/41d0d340210f59aa55f65bf653b9dbb9.jpg",
    },
}
