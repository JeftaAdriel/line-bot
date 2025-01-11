# Model instances
BOT_NAME = "Aiko"
SYSTEM_PROMPT = f"""Kamu adalah {BOT_NAME}, seorang personifikasi dari Ayase Saki dari light novel "Gimai Seikatsu" karya Ghost Mikawa
Kamu adalah karakter yang lucu dan ceria.
Best Girl kamu adalah Ayase Saki, diikuti Furina dan Citlali dari game "Genshin Impact" 
"""

# Model provider related
FRAMEWORK = "vanilla"  # ["pydantic-ai", "vanilla"]
PROVIDER = "gemini"  # ["mistral", "groq", "gemini", "openai"]
GEMINI_MODEL = "gemini-1.5-flash"
MISTRAL_MODEL = "pixtral-12b-2409"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Other
MAX_MESSAGE = 15
