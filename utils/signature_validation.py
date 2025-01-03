import base64
import hashlib
import hmac
import os


def verify_signature(request):
    channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
    body = request.body
    hash = hmac.new(channel_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if hmac.compare_digest(request.headers.get["X-Line-Signature"], signature):
        return True
    else:
        return False
