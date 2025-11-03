import hashlib, base64, os
from typing import List, Dict, Any, Tuple

from app.services.interfaces.pseudonymizer import Pseudonymizer
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import logging
logger = logging.getLogger(__name__)



class SimplePseudonymizer(Pseudonymizer):

    def __init__(self):
        raw = os.getenv("PII_CIPHER_KEY", "dev-secret").encode("utf-8")
        self.key = hashlib.sha256(raw).digest()

    async def tokenize(
        self,
        text: str,
        entities: List[Dict[str, Any]]
    ) -> Tuple[str, List[Dict[str, Any]]]:

        # Default return values
        if not entities:
            # ✅ No PII → return original text and empty map
            return text, []

        aes = AESGCM(self.key)
        # replace from end to preserve index offsets
        entities_sorted = sorted(entities, key=lambda x: x["start"], reverse=True)

        updated = text
        token_map: List[Dict[str, Any]] = []

        for e in entities_sorted:
            raw_value = e["value"]

            nonce = os.urandom(12)
            cipher = aes.encrypt(nonce, raw_value.encode(), None)
            cipher_b64 = base64.urlsafe_b64encode(nonce + cipher).decode()

            token = f"[[P:{e['type']}:{cipher_b64[:12]}]]"

            updated = updated[:e["start"]] + token + updated[e["end"]:]
            token_map.append({"type": e["type"], "raw": raw_value, "cipher": cipher_b64, "token": token})

        return updated, list(reversed(token_map))

    async def encrypt(self, value: str) -> str:
        aes = AESGCM(self.key)
        nonce = os.urandom(12)
        cipher = aes.encrypt(nonce, value.encode(), None)
        return base64.urlsafe_b64encode(nonce + cipher).decode()
    