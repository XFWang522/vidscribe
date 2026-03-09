# vidscribe

**一条命令，将任意视频链接转为文字。**

支持 **B站、YouTube、抖音/TikTok、Twitter/X、Vimeo** 等 [1000+ 个平台](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)。

[English](README.md)

---

## 快速开始

```bash
pip install vidscribe

# 配置任意一个语音识别服务（详见下方）
export VOLC_APP_KEY="your_app_id"
export VOLC_ACCESS_KEY="your_access_token"

# 转录！
vidscribe "https://www.bilibili.com/video/BV1xxx" -o transcript.txt
```

## 特性

- **一条命令** - 粘贴链接，获得文字
- **1000+ 平台** - yt-dlp 支持的所有视频网站
- **5 种语音识别服务** - 按质量、速度、价格自由选择
- **自动检测** - 根据环境变量自动选择可用的服务
- **离线模式** - 本地 Whisper 模型，无需 API Key
- **多语言** - 中文、英文、日语等 50+ 种语言

## 安装

```bash
# 基础安装（含火山引擎，无需额外依赖）
pip install vidscribe

# 按需安装特定服务支持
pip install vidscribe[openai]      # OpenAI Whisper API
pip install vidscribe[deepgram]    # Deepgram
pip install vidscribe[aliyun]      # 阿里云 DashScope
pip install vidscribe[local]       # 本地 faster-whisper（离线）
pip install vidscribe[all]         # 全部安装
```

**系统依赖：**
- [ffmpeg](https://ffmpeg.org/) - 音频转换（`brew install ffmpeg` / `apt install ffmpeg`）

## 语音识别服务

| 服务 | 适用场景 | 价格 | 速度 | 配置 |
|------|---------|------|------|------|
| **火山引擎** | 中文内容 | ~0.8元/小时 | 快 | [配置指南](#火山引擎) |
| **OpenAI** | 多语言 | ~2.6元/小时 | 快 | [配置指南](#openai-whisper-api) |
| **阿里云** | 中文内容 | ~1.2元/小时 | 快 | [配置指南](#阿里云) |
| **Deepgram** | 速度和性价比 | ~1.9元/小时 | 最快 | [配置指南](#deepgram) |
| **本地模型** | 隐私/离线 | 免费 | 慢 | [配置指南](#本地模型) |

### 火山引擎

中文最便宜的云端方案，基于豆包语音识别大模型。支持支付宝/微信支付。

```bash
export VOLC_APP_KEY="your_app_id"
export VOLC_ACCESS_KEY="your_access_token"
```

获取凭证：[火山引擎控制台](https://console.volcengine.com/speech/service/8)

### OpenAI Whisper API

多语言质量最好。需要海外支付方式。

```bash
export OPENAI_API_KEY="sk-..."
```

获取 API Key：[OpenAI Platform](https://platform.openai.com/api-keys)

### 阿里云

中文效果好。新用户免费试用 3 个月，每天 2 小时。支持支付宝支付。

```bash
export DASHSCOPE_API_KEY="sk-..."
```

获取 API Key：[百炼控制台](https://bailian.console.aliyun.com/)

### Deepgram

最快的转录速度。注册即送 **$200 免费额度**，无需信用卡。

```bash
export DEEPGRAM_API_KEY="..."
```

获取 API Key：[Deepgram Console](https://console.deepgram.com/)

### 本地模型

完全免费、离线运行。无需 API Key，在本地 CPU 上运行（速度较慢但完全隐私）。

```bash
pip install vidscribe[local]
vidscribe "https://..." -p local
```

## 使用方法

```bash
# 自动检测可用的服务
vidscribe "https://www.bilibili.com/video/BV1xxx"

# 指定服务
vidscribe "https://youtu.be/xxx" -p openai

# 保存到文件
vidscribe "https://youtu.be/xxx" -o transcript.txt

# 语言提示（有助于提高非中英文的准确率）
vidscribe "https://youtu.be/xxx" -l ja-JP

# 同时保留音频文件
vidscribe "https://youtu.be/xxx" -o transcript.txt --keep-audio
```

### 支持的视频平台

B站、YouTube、抖音、TikTok、Twitter/X、Vimeo、Dailymotion、Twitch、Instagram、Facebook、Reddit、NicoNico 等 [1000+ 个平台](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)。

## 费用对比

以一个 15 分钟的视频为例：

| 服务 | 费用 | 备注 |
|------|------|------|
| 火山引擎 | ~¥0.2 | 中文最便宜 |
| OpenAI | ~¥0.65 | 质量最好 |
| 阿里云 | ~¥0.3 | 有免费试用 |
| Deepgram | ~¥0.45 | 注册送 $200 |
| 本地模型 | 免费 | 需要 CPU 时间（~20分钟） |

## 配置

将环境变量写入 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`），或使用 `.env` 文件：

```bash
cp .env.example .env
# 编辑 .env，填入你的 Key
```

vidscribe 按以下优先级自动检测服务：
1. 火山引擎（设置了 `VOLC_APP_KEY`）
2. OpenAI（设置了 `OPENAI_API_KEY`）
3. 阿里云（设置了 `DASHSCOPE_API_KEY`）
4. Deepgram（设置了 `DEEPGRAM_API_KEY`）
5. 本地模型（安装了 `faster-whisper`）

可用 `-p <provider>` 手动指定。

## 许可证

[MIT](LICENSE)
