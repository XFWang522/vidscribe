"""Abstract base class for ASR providers."""

from __future__ import annotations

import abc


class BaseProvider(abc.ABC):
    """All providers implement this interface."""

    @abc.abstractmethod
    def transcribe(self, audio_path: str, lang: str = "") -> str:
        """Transcribe an audio file and return the full text.

        Args:
            audio_path: Path to a local audio file (mp3/m4a/wav/etc.).
            lang: Optional language hint (e.g. "zh", "en", "ja-JP").

        Returns:
            The transcription as a single string.
        """

    @staticmethod
    @abc.abstractmethod
    def is_available() -> bool:
        """Return True if the required credentials / deps are configured."""
