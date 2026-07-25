import base64
import json

from nacl.signing import VerifyKey

from hashing import canonical


def verify_receipt(
    public_key_bytes,
    evaluation_id,
    input_digest,
    receipt,
):
    """
    receipt is WITHOUT receiptSignature
    """

    verify_key = VerifyKey(public_key_bytes)

    body = {
        "profile": "ga5-mailroom-action-gate/v2",
        "evaluationId": evaluation_id,
        "inputDigest": input_digest,
        "receipt": receipt,
    }

    message = canonical(body).encode()

    signature = base64.b64decode(
        receipt["receiptSignature"]
    )

    verify_key.verify(message, signature)

    return True
