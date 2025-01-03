import base64
import hashlib
import hmac
import os


def verify_signature(body, x_line_signature):
    channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
    if not channel_secret:
        raise ValueError("LINE_CHANNEL_SECRET is not set in environment variables.")
    gen_signature = hmac.new(channel_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    return hmac.compare_digest(x_line_signature.encode("utf-8"), base64.b64encode(gen_signature))
