"""Command-line interface for vidscribe."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile

from vidscribe import __version__
from vidscribe.download import download_audio
from vidscribe.providers import get_provider, list_providers


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="vidscribe",
        description="Transcribe any video URL to text with one command.",
        epilog="Supported sites: Bilibili, YouTube, TikTok/Douyin, Twitter/X, Vimeo, and 1000+ more via yt-dlp.",
    )
    parser.add_argument("url", help="video URL to transcribe")
    parser.add_argument("-o", "--output", help="save transcript to file (default: print to stdout)")
    parser.add_argument("-p", "--provider", choices=list_providers(),
                        help="ASR provider (default: auto-detect from env vars)")
    parser.add_argument("-l", "--lang", default="",
                        help="language hint, e.g. zh, en, ja-JP (default: auto-detect)")
    parser.add_argument("--keep-audio", action="store_true",
                        help="save the downloaded audio alongside the transcript")
    parser.add_argument("-v", "--version", action="version", version=f"vidscribe {__version__}")
    args = parser.parse_args()

    try:
        provider = get_provider(args.provider)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    provider_name = type(provider).__name__.replace("Provider", "").lower()
    print(f"[vidscribe] Provider: {provider_name}")

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.mp3")

        print(f"[1/3] Downloading audio...")
        try:
            actual_path = download_audio(args.url, audio_path)
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        size_mb = os.path.getsize(actual_path) / 1024 / 1024
        print(f"       {size_mb:.1f} MB downloaded")

        if args.keep_audio and args.output:
            import shutil
            ext = os.path.splitext(actual_path)[1]
            audio_dest = os.path.splitext(args.output)[0] + ext
            shutil.copy2(actual_path, audio_dest)
            print(f"       Audio saved: {audio_dest}")

        print(f"[2/3] Transcribing...")
        try:
            transcript = provider.transcribe(actual_path, lang=args.lang)
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"[3/3] Done! ({len(transcript)} characters)")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"       Saved: {args.output}")
    else:
        print()
        print(transcript)
