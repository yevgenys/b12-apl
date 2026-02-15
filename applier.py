import hashlib
import hmac
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from datetime import timezone

import requests


@dataclass
class Payload:
    timestamp: str
    name: str
    email: str
    resume_link: str
    repository_link: str
    action_run_link: str


def now_in_iso():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def validate_mandatory_env_variables():
    for key in ["FULL_NAME", "CV_LINK", "EMAIL", "REPOSITORY_LINK", "ACTION_RUN_LINK", "SIGNING_SECRET"]:
        assert os.environ.get(key), f"{key} is not set"


def get_signature(payload_str: str):
    hex_value = hmac.new(
        os.environ["SIGNING_SECRET"].encode("utf-8"),
        payload_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={hex_value}"


def request(payload: Payload) -> requests.Response:
    payload_str = json.dumps(asdict(payload), separators=(",", ":"), sort_keys=True)

    headers = {
        "X-Signature-256": get_signature(payload_str)
    }

    return requests.post("https://b12.io/apply/submission", headers=headers, data=payload_str)


if __name__ == '__main__':
    validate_mandatory_env_variables()

    p = Payload(
        timestamp=now_in_iso(),
        name=os.environ["FULL_NAME"],
        email=os.environ["EMAIL"],
        resume_link=os.environ["CV_LINK"],
        repository_link=os.environ["REPOSITORY_LINK"],
        action_run_link=os.environ["ACTION_RUN_LINK"],
    )
    response = request(p)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, body: {response.text}"
    response_json = response.json()
    assert response_json["success"], response_json["success"]
    print(response_json['receipt'])
