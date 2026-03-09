"""OpenAI Whisper API provider.

Best multilingual quality. $0.006/min.
Requires: OPENAI_API_KEY environment variable.
Install: pip install vidscribe[openai]
"""

from __future__ import annotations

import os

from vidscribe.providers.base import BaseProvider


class OpenaiProvider(BaseProvider):

    @staticmethod
    def is_available() -> bool:
        return bool(os.environ.get("OPENAI_API_KEY"))

    def transcribe(self, audio_path: str, lang: str = "") -> str:
        try:
            from openai import OpenAI
        except ImportError:
            raise RuntimeError(
                "OpenAI SDK not installed. Run: pip install vidscribe[openai]"
            )

        client = OpenAI()
        file_size = os.path.getsize(audio_path)

        # Whisper API has a 25 MB limit; split if needed
        if file_size > 25 * 1024 * 1024:
            return self._transcribe_large(client, audio_path, lang)

        kwargs: dict = {"model": "whisper-1", "response_format": "text"}
        if lang:
            kwargs["language"] = lang.split("-")[0]

        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(file=f, **kwargs)

        return result if isinstance(result, str) else result.text

    def _transcribe_large(self, client, audio_path: str, lang: str) -> str:
        """Split large files into chunks using ffmpeg and transcribe each."""
        import subprocess
        import tempfile

        duration_cmd = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True,
        )
        total_seconds = float(duration_cmd.stdout.strip())
        chunk_duration = 600  # 10 minutes per chunk

        segments = []
        with tempfile.TemporaryDirectory() as tmpdir:
            offset = 0
            chunk_idx = 0
            while offset < total_seconds:
                chunk_path = os.path.join(tmpdir, f"chunk_{chunk_idx}.mp3")
                subprocess.run(
                    ["ffmpeg", "-i", audio_path, "-ss", str(offset),
                     "-t", str(chunk_duration), "-q:a", "5",
                     chunk_path, "-y", "-loglevel", "error"],
                    capture_output=True,
                )

                kwargs: dict = {"model": "whisper-1", "response_format": "text"}
                if lang:
                    kwargs["language"] = lang.split("-")[0]

                with open(chunk_path, "rb") as f:
                    result = client.audio.transcriptions.create(file=f, **kwargs)
                    text = result if isinstance(result, str) else result.text
                    segments.append(text.strip())

                offset += chunk_duration
                chunk_idx += 1

        return "\n".join(segments)
