"""Aliyun DashScope (阿里云百炼) Paraformer provider.

Good for Chinese content. Free trial 3 months.
Requires: DASHSCOPE_API_KEY environment variable.
Install: pip install vidscribe[aliyun]
"""

from __future__ import annotations

import json
import os
import time

import requests

from vidscribe.providers.base import BaseProvider
from vidscribe.upload import upload_audio


class AliyunProvider(BaseProvider):

    @staticmethod
    def is_available() -> bool:
        return bool(os.environ.get("DASHSCOPE_API_KEY"))

    def transcribe(self, audio_path: str, lang: str = "") -> str:
        try:
            from dashscope.audio.asr import Transcription
        except ImportError:
            raise RuntimeError(
                "DashScope SDK not installed. Run: pip install vidscribe[aliyun]"
            )

        public_url = upload_audio(audio_path)

        language_hints = [lang] if lang else ["zh", "en"]

        task_response = Transcription.async_call(
            model="paraformer-v2",
            file_urls=[public_url],
            language_hints=language_hints,
        )

        if not hasattr(task_response, "output") or not task_response.output:
            raise RuntimeError(f"Aliyun submit failed: {task_response}")

        transcribe_response = Transcription.wait(
            task=task_response.output.task_id
        )

        if transcribe_response.status_code != 200:
            raise RuntimeError(
                f"Aliyun transcription failed: {transcribe_response.message}"
            )

        results = transcribe_response.output.get("results", [])
        texts = []
        for r in results:
            if r.get("subtask_status") == "SUCCEEDED" and r.get("transcription_url"):
                try:
                    tr = requests.get(r["transcription_url"], timeout=30).json()
                    for t in tr.get("transcripts", []):
                        for s in t.get("sentences", []):
                            text = s.get("text", "").strip()
                            if text:
                                texts.append(text)
                except Exception:
                    pass

        if not texts:
            raise RuntimeError("Aliyun returned empty transcription")

        return "\n".join(texts)
