"""Volcengine (火山引擎) 豆包录音文件识别模型2.0 provider.

Best for Chinese content. ~0.8 CNY/hour.
Requires: VOLC_APP_KEY and VOLC_ACCESS_KEY environment variables.
"""

from __future__ import annotations

import json
import os
import time
import uuid

import requests

from vidscribe.providers.base import BaseProvider
from vidscribe.upload import upload_audio

_SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
_QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
_RESOURCE_ID = "volc.seedasr.auc"


class VolcengineProvider(BaseProvider):

    def __init__(self) -> None:
        self.app_key = os.environ["VOLC_APP_KEY"]
        self.access_key = os.environ["VOLC_ACCESS_KEY"]

    @staticmethod
    def is_available() -> bool:
        return bool(os.environ.get("VOLC_APP_KEY") and os.environ.get("VOLC_ACCESS_KEY"))

    def transcribe(self, audio_path: str, lang: str = "") -> str:
        public_url = upload_audio(audio_path)
        task_id = str(uuid.uuid4())

        headers = {
            "X-Api-App-Key": self.app_key,
            "X-Api-Access-Key": self.access_key,
            "X-Api-Resource-Id": _RESOURCE_ID,
            "X-Api-Request-Id": task_id,
            "X-Api-Sequence": "-1",
            "Content-Type": "application/json",
        }

        payload = {
            "user": {"uid": "vidscribe"},
            "audio": {"url": public_url, "format": "mp3", "language": lang},
            "request": {"model_name": "bigmodel"},
        }

        resp = requests.post(_SUBMIT_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"Volcengine submit failed: HTTP {resp.status_code}")

        # Poll for results
        deadline = time.time() + 600
        while time.time() < deadline:
            time.sleep(5)
            r = requests.post(_QUERY_URL, headers=headers, json={}, timeout=30)
            result = r.json().get("result", {})

            utterances = result.get("utterances", [])
            if utterances:
                return "\n".join(u.get("text", "") for u in utterances)

            text = result.get("text", "")
            if text:
                return text

        raise RuntimeError("Volcengine transcription timed out (600s)")
