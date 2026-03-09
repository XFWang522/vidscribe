"""Download audio from video URLs using yt-dlp."""

from __future__ import annotations

import os
import subprocess
import sys


def download_audio(video_url: str, output_path: str) -> str:
    """Download audio track from a video URL and convert to mp3.

    Returns the path to the downloaded mp3 file.
    """
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-x", "--audio-format", "mp3", "--audio-quality", "5",
        "-o", output_path,
        "--no-playlist",
        "--quiet", "--no-warnings",
        video_url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    base = os.path.splitext(output_path)[0]

    if result.returncode != 0:
        if "ffprobe and ffmpeg not found" in result.stderr:
            for ext in (".m4a", ".webm", ".opus", ".ogg", ".wav"):
                candidate = base + ext
                if os.path.exists(candidate):
                    mp3_path = base + ".mp3"
                    conv = subprocess.run(
                        ["ffmpeg", "-i", candidate, "-codec:a", "libmp3lame",
                         "-q:a", "5", mp3_path, "-y", "-loglevel", "error"],
                        capture_output=True, text=True,
                    )
                    if conv.returncode == 0 and os.path.exists(mp3_path):
                        os.remove(candidate)
                        return mp3_path
            raise RuntimeError(
                f"ffmpeg is required for audio conversion. Install it first.\n"
                f"  macOS: brew install ffmpeg\n"
                f"  Ubuntu: sudo apt install ffmpeg"
            )
        raise RuntimeError(f"Failed to download audio: {result.stderr.strip()}")

    # yt-dlp may output with a different extension; find the actual file
    for ext in (".mp3", ".m4a", ".webm", ".opus", ".ogg", ".wav"):
        candidate = base + ext
        if os.path.exists(candidate):
            return candidate

    if os.path.exists(output_path):
        return output_path

    raise RuntimeError(f"Downloaded file not found at {output_path}")
