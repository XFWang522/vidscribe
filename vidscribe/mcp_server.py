"""MCP (Model Context Protocol) server for vidscribe.

Exposes video transcription as a tool that any MCP-compatible AI client
(Claude Desktop, Cursor, etc.) can invoke directly.
"""

from __future__ import annotations

import os
import tempfile

from mcp.server.fastmcp import FastMCP

from vidscribe.download import download_audio
from vidscribe.providers import get_provider, list_providers

mcp = FastMCP(
    "vidscribe",
    description="Transcribe any video URL to text. Supports Bilibili, YouTube, TikTok/Douyin, Twitter/X, and 1000+ sites.",
)


@mcp.tool()
def transcribe(
    url: str,
    provider: str = "",
    lang: str = "",
    output_path: str = "",
) -> str:
    """Transcribe a video URL to text.

    Args:
        url: Video URL to transcribe (Bilibili, YouTube, TikTok, Twitter/X, etc.)
        provider: ASR provider name. Leave empty to auto-detect from env vars.
                  Options: volcengine, openai, aliyun, deepgram, local
        lang: Language hint (e.g. zh, en, ja-JP). Leave empty for auto-detect.
        output_path: Optional file path to save the transcript. If empty, returns text only.

    Returns:
        The full transcript text.
    """
    asr = get_provider(provider if provider else None)
    provider_name = type(asr).__name__.replace("Provider", "")

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.mp3")
        actual_path = download_audio(url, audio_path)
        transcript = asr.transcribe(actual_path, lang=lang)

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)

    return transcript


@mcp.tool()
def list_available_providers() -> dict:
    """List all ASR providers and their availability status.

    Returns a dict mapping provider names to whether they are currently
    configured and ready to use.
    """
    from vidscribe.providers import _PROVIDERS

    result = {}
    for name, cls in _PROVIDERS.items():
        result[name] = {
            "available": cls.is_available(),
            "type": "cloud" if name != "local" else "local",
        }
    return result


def main() -> None:
    """Run the MCP server (stdio transport)."""
    mcp.run()


if __name__ == "__main__":
    main()
