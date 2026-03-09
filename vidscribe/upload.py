"""Upload audio files to temporary hosting for cloud ASR providers."""

from __future__ import annotations

import json
import os
import subprocess
import time


def upload_audio(file_path: str, max_retries: int = 3) -> str:
    """Upload a file to tmpfiles.org and return a direct download URL.

    Uses curl subprocess for reliability across network environments.
    """
    size_mb = os.path.getsize(file_path) / 1024 / 1024

    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["curl", "-s", "-F", f"file=@{file_path}",
                 "https://tmpfiles.org/api/v1/upload"],
                capture_output=True, text=True, timeout=300,
            )
        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            raise RuntimeError(f"Upload timed out for {size_mb:.1f} MB file")

        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError:
                pass
            else:
                if data.get("status") == "success":
                    page_url = data["data"]["url"]
                    direct_url = page_url.replace("tmpfiles.org/", "tmpfiles.org/dl/", 1)
                    if direct_url.startswith("http://"):
                        direct_url = direct_url.replace("http://", "https://", 1)
                    return direct_url

        if attempt < max_retries - 1:
            time.sleep(3)

    raise RuntimeError(f"Failed to upload after {max_retries} attempts")
