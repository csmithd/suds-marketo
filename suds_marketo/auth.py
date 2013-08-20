import hmac
import hashlib

from datetime import datetime
from suds.sax.element import Element

def sign(message, encryption_key):
    digest = hmac.new(encryption_key, message, hashlib.sha1)
    return digest.hexdigest().lower()

def header(user_id, encryption_key):
    authentication_header = Element("AuthenticationHeader")
    timestamp = datetime.utcnow()
    signature = sign(timestamp + user_id, encryption_key)

    user_id_element = Element("mktowsUserId")
    user_id_element.setText(user_id)
    authentication_header.append(user_id_element)

    request_signature_element = Element("requestSignature")
    request_signature_element.setText(signature)
    authentication_header.append(request_signature_element)

    request_timestamp_element = Element("requestTimestamp")
    request_timestamp_element.setText(timestamp)
    authentication_header.append(request_timestamp_element)

    return authentication_header
