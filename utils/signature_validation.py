import base64
import hashlib
import hmac
import os


def verify_signature(body, x_line_signature):
    channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
    if not channel_secret:
        raise ValueError("LINE_CHANNEL_SECRET is not set in environment variables.")
    hash = hmac.new(channel_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if hmac.compare_digest(x_line_signature, signature):
        return True
    else:
        return False
