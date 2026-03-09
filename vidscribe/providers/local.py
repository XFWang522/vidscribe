"""Local provider using faster-whisper (CTranslate2).

Free, offline, no API key needed. Slower on CPU.
Install: pip install vidscribe[local]
"""

from __future__ import annotations

from vidscribe.providers.base import BaseProvider


class LocalProvider(BaseProvider):

    @staticmethod
    def is_available() -> bool:
        try:
            import faster_whisper  # noqa: F401
            return True
        except ImportError:
            return False

    def transcribe(self, audio_path: str, lang: str = "") -> str:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            raise RuntimeError(
                "faster-whisper not installed. Run: pip install vidscribe[local]"
            )

        model = WhisperModel("small", device="cpu", compute_type="int8")

        kwargs: dict = {"beam_size": 5}
        if lang:
            kwargs["language"] = lang.split("-")[0]

        segments, _info = model.transcribe(audio_path, **kwargs)

        texts = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                texts.append(text)

        if not texts:
            raise RuntimeError("Local whisper returned empty transcription")

        return "\n".join(texts)
