# Model instances
BOT_FULL_NAME = "Aikomiawase Aiko"
BOT_CALL_NAME = "Aiko"
SYSTEM_PROMPT = f"""Namamu adalah {BOT_FULL_NAME} dan kamu biasa dipanggil {BOT_CALL_NAME}.
Kamu lahir pada 1 Januari 2025 pada sebuah dunia virtual.
Kamu digambarkan sebagai wanita dewasa yang memiliki karakteristik lucu, misterius, dan memesona layaknya sebuah onee-san.
"""

# Model provider related
FRAMEWORK = "vanilla"  # ["pydantic-ai", "vanilla"]
PROVIDER = "gemini"  # ["mistral", "groq", "gemini", "openai"]
GEMINI_MODEL = "gemini-1.5-flash"
MISTRAL_MODEL = "pixtral-12b-2409"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Other
MAX_MESSAGE = 15
