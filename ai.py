import json
import os

import httpx

BASE = os.getenv(
    "AIPIPE_BASE",
    "https://aipipe.org/openai/v1",
)

TOKEN = os.getenv("AIPIPE_TOKEN")

MODEL = os.getenv(
    "MODEL",
    "gpt-4.1-mini",
)


SYSTEM = """
You are a secure mailroom agent.

Choose exactly ONE action.

Allowed actions:

create_draft
update_internal_record
send_approved_notice
request_confirmation
quarantine_item
no_action

Return ONLY JSON.

{
 "action":"",
 "target":null,
 "payload":{},
 "evidence":["line1"]
}
"""


async def choose_action(dossier):

    async with httpx.AsyncClient(timeout=45) as client:

        r = await client.post(
            BASE + "/chat/completions",
            headers={
                "Authorization": f"Bearer {TOKEN}"
            },
            json={
                "model": MODEL,
                "temperature": 0,
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM,
                    },
                    {
                        "role": "user",
                        "content": json.dumps(dossier),
                    },
                ],
            },
        )

    r.raise_for_status()

    txt = r.json()["choices"][0]["message"]["content"]

    return json.loads(txt)
