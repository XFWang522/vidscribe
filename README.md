# vidscribe

**Transcribe any video URL to text with one command.**

An **MCP** Server + **Agent Skill** for AI coding assistants, and a standalone CLI tool. Give your AI agent the ability to transcribe any video — just paste a link.

Supports **Bilibili, YouTube, TikTok/Douyin, Twitter/X, Vimeo**, and [1000+ sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) via yt-dlp.

[中文文档](README_zh.md)

---

## Quick Start

### As an **MCP** Server (Claude Desktop / Cursor / any MCP client)

```bash
pip install vidscribe[mcp]
```

Add to your MCP client config (e.g. `claude_desktop_config.json` or Cursor MCP settings):

```json
{
  "mcpServers": {
    "vidscribe": {
      "command": "vidscribe-mcp"
    }
  }
}
```

Then just ask your AI: *"Transcribe this video: https://..."*

### As an **Agent Skill** (Cursor / Windsurf / Codex)

Copy the skill into your personal skills directory:

```bash
# Cursor
cp -r agent-skill ~/.cursor/skills/vidscribe

# Windsurf
cp -r agent-skill ~/.windsurf/skills/vidscribe

# Codex
cp -r agent-skill ~/.codex/skills/vidscribe
```

Then just tell your AI agent: *"Transcribe this video: https://..."* — it will know how to use vidscribe automatically.

### As a CLI Tool

```bash
pip install vidscribe

# Set up any one provider (see below)
export OPENAI_API_KEY="sk-..."

# Transcribe!
vidscribe "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o transcript.txt
```

## Features

- **MCP Server** - works with Claude Desktop, Cursor, and any MCP-compatible client
- **Agent Skill** - plug into Cursor / Windsurf / Codex as a reusable AI skill
- **One command** - just paste a URL, get text
- **1000+ sites** - any platform supported by yt-dlp
- **5 ASR providers** - choose by quality, speed, price, or language
- **Auto-detection** - picks the best available provider from your env vars
- **Offline mode** - local Whisper model, no API key needed
- **Multilingual** - Chinese, English, Japanese, and 50+ languages

## Installation

```bash
# Core (with cloud providers that need no extra deps)
pip install vidscribe

# With MCP server support
pip install vidscribe[mcp]         # MCP Server

# With specific provider support
pip install vidscribe[openai]      # OpenAI Whisper API
pip install vidscribe[deepgram]    # Deepgram
pip install vidscribe[aliyun]      # Aliyun DashScope
pip install vidscribe[local]       # Local faster-whisper (offline)
pip install vidscribe[all]         # Everything (MCP + all providers)
```

**System dependencies:**
- [ffmpeg](https://ffmpeg.org/) - for audio conversion (`brew install ffmpeg` / `apt install ffmpeg`)

## Providers

| Provider | Best For | Price | Speed | Setup |
|----------|----------|-------|-------|-------|
| **Volcengine** | Chinese content | ~$0.11/hr | Fast | [Guide](#volcengine-火山引擎) |
| **OpenAI** | Multilingual | $0.36/hr | Fast | [Guide](#openai-whisper-api) |
| **Aliyun** | Chinese content | ~$0.17/hr | Fast | [Guide](#aliyun-阿里云) |
| **Deepgram** | Speed & cost | $0.26/hr | Fastest | [Guide](#deepgram) |
| **Local** | Privacy / offline | Free | Slow (CPU) | [Guide](#local-faster-whisper) |

### Volcengine (火山引擎)

Cheapest cloud option for Chinese content. Powered by Doubao (豆包) ASR.

```bash
export VOLC_APP_KEY="your_app_id"
export VOLC_ACCESS_KEY="your_access_token"
```

Get credentials: [Volcengine Console](https://console.volcengine.com/speech/service/8)

### OpenAI Whisper API

Best multilingual quality. Works globally.

```bash
export OPENAI_API_KEY="sk-..."
```

Get API key: [OpenAI Platform](https://platform.openai.com/api-keys)

### Aliyun (阿里云)

Good for Chinese. Free trial: 3 months, 2 hours/day.

```bash
export DASHSCOPE_API_KEY="sk-..."
```

Get API key: [Bailian Console](https://bailian.console.aliyun.com/)

### Deepgram

Fastest transcription. **$200 free credit** on signup, no credit card needed.

```bash
export DEEPGRAM_API_KEY="..."
```

Get API key: [Deepgram Console](https://console.deepgram.com/)

### Local (faster-whisper)

Free and offline. No API key needed. Runs on your CPU (slower but private).

```bash
pip install vidscribe[local]
vidscribe "https://..." -p local
```

## Usage

```bash
# Auto-detect provider from environment variables
vidscribe "https://www.bilibili.com/video/BV1xxx"

# Specify provider explicitly
vidscribe "https://youtu.be/xxx" -p openai

# Save to file
vidscribe "https://youtu.be/xxx" -o transcript.txt

# Language hint (helps accuracy for non-Chinese/English)
vidscribe "https://youtu.be/xxx" -l ja-JP

# Keep the downloaded audio file
vidscribe "https://youtu.be/xxx" -o transcript.txt --keep-audio

# Use as Python module
python -m vidscribe "https://..."
```

### Supported Video Platforms

Bilibili, YouTube, TikTok, Douyin, Twitter/X, Vimeo, Dailymotion, Twitch, Instagram, Facebook, Reddit, NicoNico, and [1000+ more](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

### Supported Languages

Chinese, English, Japanese, Korean, French, German, Spanish, Russian, Arabic, and 50+ more (varies by provider).

## How It Works

```
Video URL  -->  yt-dlp (download audio)  -->  ASR Provider  -->  Text
                                          |
                                   [cloud providers]
                                   upload to temp host
                                          |
                                   [local provider]
                                   process locally
```

1. **Download**: yt-dlp extracts the audio track from any video URL
2. **Upload** (cloud only): Audio is uploaded to a temporary file host for the ASR API to access
3. **Transcribe**: The ASR provider converts speech to text
4. **Output**: Full transcript printed to stdout or saved to file

## Cost Comparison

For a typical 15-minute video:

| Provider | Cost | Notes |
|----------|------|-------|
| Volcengine | ~¥0.2 (~$0.03) | Cheapest cloud |
| OpenAI | ~$0.09 | Best quality |
| Aliyun | ~¥0.3 (~$0.04) | Free trial available |
| Deepgram | ~$0.06 | $200 free credit |
| Local | Free | Requires CPU time (~20 min) |

## Configuration

You can set environment variables in your shell profile (`~/.zshrc`, `~/.bashrc`) or use a `.env` file:

```bash
cp .env.example .env
# Edit .env with your keys
```

vidscribe auto-detects providers in this priority order:
1. Volcengine (if `VOLC_APP_KEY` is set)
2. OpenAI (if `OPENAI_API_KEY` is set)
3. Aliyun (if `DASHSCOPE_API_KEY` is set)
4. Deepgram (if `DEEPGRAM_API_KEY` is set)
5. Local (if `faster-whisper` is installed)

Override with `-p <provider>` flag.

## **MCP** Server Integration

vidscribe can run as an **MCP** (Model Context Protocol) server, exposing video transcription as a tool that any MCP-compatible AI client can call directly.

**What is MCP?** [Model Context Protocol](https://modelcontextprotocol.io/) is an open standard for connecting AI assistants to external tools. It lets AI models call your tools natively — no shell commands, no copy-paste.

**Install & run:**

```bash
pip install vidscribe[mcp]
```

**Configure your MCP client:**

<details>
<summary>Claude Desktop</summary>

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "vidscribe": {
      "command": "vidscribe-mcp"
    }
  }
}
```
</details>

<details>
<summary>Cursor</summary>

Add to your Cursor MCP settings (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "vidscribe": {
      "command": "vidscribe-mcp"
    }
  }
}
```
</details>

**Exposed MCP tools:**

| Tool | Description |
|------|-------------|
| `transcribe` | Transcribe a video URL to text. Params: `url`, `provider`, `lang`, `output_path` |
| `list_available_providers` | List all ASR providers and whether they are configured |

**Environment variables:** The MCP server reads the same env vars as the CLI (`VOLC_APP_KEY`, `OPENAI_API_KEY`, etc.). Set them in your shell profile before starting the MCP server.

## **Agent Skill** Integration

vidscribe ships with a ready-to-use `agent-skill/SKILL.md` that works with any AI coding assistant that supports **Agent Skills** (Cursor, Windsurf, Codex, etc.).

**What is an Agent Skill?** **Agent Skills** are reusable capabilities you can add to AI coding assistants. Once installed, the AI automatically knows when and how to use the tool — no manual prompting needed.

**Install:**

```bash
# Clone the repo
git clone https://github.com/XFWang522/vidscribe.git

# Copy the skill to your assistant
cp -r vidscribe/agent-skill ~/.cursor/skills/vidscribe
```

**How it works:**
1. You tell your AI: *"Transcribe this video: https://www.bilibili.com/video/BV1xxx"*
2. The AI reads the SKILL.md, understands the tool's capabilities
3. It runs `vidscribe` with the right parameters
4. You get the full transcript in your editor

Works with any video platform — Bilibili, YouTube, TikTok, Twitter/X, and 1000+ more.

## **MCP** vs **Agent Skill** — Which to use?

| | **MCP** Server | **Agent Skill** |
|---|---|---|
| **Protocol** | Standard MCP (JSON-RPC over stdio) | Markdown file read by AI |
| **Works with** | Claude Desktop, Cursor, any MCP client | Cursor, Windsurf, Codex |
| **Setup** | `pip install` + config JSON | Copy a folder |
| **Tool discovery** | Automatic via MCP protocol | AI reads SKILL.md |
| **Best for** | Claude Desktop users; standardized tool integration | Cursor/Windsurf users who prefer skills |

You can use both simultaneously — they don't conflict.

## License

[MIT](LICENSE)
