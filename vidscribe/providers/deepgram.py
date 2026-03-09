"""Deepgram provider.

Fastest and cheapest cloud option. $200 free credit on signup.
Requires: DEEPGRAM_API_KEY environment variable.
Install: pip install vidscribe[deepgram]
"""

from __future__ import annotations

import os

from vidscribe.providers.base import BaseProvider


class DeepgramProvider(BaseProvider):

    @staticmethod
    def is_available() -> bool:
        return bool(os.environ.get("DEEPGRAM_API_KEY"))

    def transcribe(self, audio_path: str, lang: str = "") -> str:
        try:
            from deepgram import DeepgramClient, PrerecordedOptions, FileSource
        except ImportError:
            raise RuntimeError(
                "Deepgram SDK not installed. Run: pip install vidscribe[deepgram]"
            )

        client = DeepgramClient(os.environ["DEEPGRAM_API_KEY"])

        with open(audio_path, "rb") as f:
            buffer = f.read()

        payload: FileSource = {"buffer": buffer}

        options = PrerecordedOptions(
            model="nova-3",
            smart_format=True,
            language=lang.split("-")[0] if lang else None,
            detect_language=not bool(lang),
            punctuate=True,
            paragraphs=True,
        )

        response = client.listen.rest.v("1").transcribe_file(payload, options)
        result = response.to_dict()

        paragraphs = (
            result.get("results", {})
            .get("channels", [{}])[0]
            .get("alternatives", [{}])[0]
            .get("paragraphs", {})
            .get("paragraphs", [])
        )

        if paragraphs:
            texts = []
            for p in paragraphs:
                sentences = [s.get("text", "") for s in p.get("sentences", [])]
                texts.append(" ".join(sentences))
            return "\n".join(texts)

        # Fallback to plain transcript
        transcript = (
            result.get("results", {})
            .get("channels", [{}])[0]
            .get("alternatives", [{}])[0]
            .get("transcript", "")
        )

        if not transcript:
            raise RuntimeError("Deepgram returned empty transcription")

        return transcript
