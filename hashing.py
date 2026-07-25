import hashlib
import json


def canonical(obj):

    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_hex(obj):

    return hashlib.sha256(
        canonical(obj).encode("utf-8")
    ).hexdigest()


def input_digest(dossiers):

    return sha256_hex(dossiers)


def dossier_fingerprint(dossier):

    return sha256_hex(dossier)


def proposal_digest(proposal):

    p = {
        "dossierId": proposal["dossierId"],
        "callId": proposal["callId"],
        "action": proposal["action"],
        "target": proposal.get("target"),
        "payload": proposal["payload"],
        "evidence": sorted(proposal["evidence"]),
    }

    return sha256_hex(p)


def stable_call_id(fingerprint):

    return "call_" + hashlib.sha256(
        fingerprint.encode()
    ).hexdigest()[:24]
