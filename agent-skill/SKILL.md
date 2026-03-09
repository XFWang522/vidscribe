---
name: vidscribe
description: Transcribe video to text from any platform (Bilibili, YouTube, Douyin, Twitter/X, TikTok, Vimeo, etc.). Use when the user provides a video URL and asks for transcript, subtitles, text content, or speech-to-text conversion.
---

# Video Transcription (vidscribe)

Transcribe any video URL to text using cloud ASR APIs or a local Whisper model.

## Prerequisites

System tools (must be installed):
- `yt-dlp`: downloads audio from 1000+ sites (`pip install yt-dlp`)
- `ffmpeg`: audio format conversion (`brew install ffmpeg` / `apt install ffmpeg`)

Python package:
- `vidscribe`: the transcription tool (`pip install vidscribe`)

If `vidscribe` is not installed, install it first:
```bash
pip install vidscribe
```

## Provider Setup

vidscribe supports 5 ASR providers. At least one must be configured via environment variables in `~/.zshrc` or `~/.bashrc`:

| Provider | Env Vars | Best For |
|----------|----------|----------|
| Volcengine (火山引擎) | `VOLC_APP_KEY`, `VOLC_ACCESS_KEY` | Chinese content, cheapest |
| OpenAI Whisper | `OPENAI_API_KEY` | Multilingual, best quality |
| Aliyun (阿里云) | `DASHSCOPE_API_KEY` | Chinese, free trial |
| Deepgram | `DEEPGRAM_API_KEY` | Fastest, $200 free credit |
| Local (faster-whisper) | None (install: `pip install vidscribe[local]`) | Offline, free |

If no provider credentials are found, ask the user which provider they want to use and help them set it up.

## Usage

```bash
# Auto-detect provider from environment variables
vidscribe "<VIDEO_URL>" -o "<OUTPUT_PATH>"

# Specify provider explicitly
vidscribe "<VIDEO_URL>" -p <provider> -o "<OUTPUT_PATH>"

# Language hint for non-Chinese/English content
vidscribe "<VIDEO_URL>" -l ja-JP -o "<OUTPUT_PATH>"
```

**Parameters:**
- `<VIDEO_URL>`: Any video URL (Bilibili, YouTube, Douyin, Twitter, TikTok, Vimeo, etc.)
- `-o <OUTPUT_PATH>`: Where to save the transcript (omit to print to stdout)
- `-p <provider>`: Force a specific provider (`volcengine`, `openai`, `aliyun`, `deepgram`, `local`)
- `-l <LANG>`: Language hint (e.g. `ja-JP`, `ko-KR`, `de-DE`)
- `--keep-audio`: Also save the downloaded audio file

## Workflow

The tool automatically:
1. Downloads audio via yt-dlp and converts to MP3
2. Uploads to a temporary host (cloud providers only) for the ASR API to access
3. Sends to the configured ASR provider for transcription
4. Outputs the full transcript text

Typical runtime: **1-3 minutes** for a 15-20 min video (cloud providers).

## Example

User says: "把这个视频转成文字 https://www.bilibili.com/video/BV1xxxx"

```bash
vidscribe "https://www.bilibili.com/video/BV1xxxx" -o /tmp/transcript.txt
```

Then read and present the output file to the user.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `vidscribe: command not found` | Run `pip install vidscribe` |
| No provider available | Ask user to set env vars for any provider (see table above) |
| yt-dlp download fails | Check URL validity; some sites need cookies (`--cookies-from-browser`) |
| Upload fails | Retry automatically; if persistent, try a different provider |
| Empty transcript | Audio may be inaccessible; re-upload or switch provider |

## Cost

| Provider | Cost per hour of audio |
|----------|----------------------|
| Volcengine | ~¥0.8 (~$0.11) |
| OpenAI | ~$0.36 |
| Aliyun | ~¥1.2 (~$0.17) |
| Deepgram | ~$0.26 |
| Local | Free |
