"""Provider registry with auto-detection."""

from __future__ import annotations

from vidscribe.providers.base import BaseProvider
from vidscribe.providers.volcengine import VolcengineProvider
from vidscribe.providers.openai_whisper import OpenaiProvider
from vidscribe.providers.aliyun import AliyunProvider
from vidscribe.providers.deepgram import DeepgramProvider
from vidscribe.providers.local import LocalProvider

_PROVIDERS: dict[str, type[BaseProvider]] = {
    "volcengine": VolcengineProvider,
    "openai": OpenaiProvider,
    "aliyun": AliyunProvider,
    "deepgram": DeepgramProvider,
    "local": LocalProvider,
}

# Auto-detection priority order
_PRIORITY = ["volcengine", "openai", "aliyun", "deepgram", "local"]


def list_providers() -> list[str]:
    return list(_PROVIDERS.keys())


def get_provider(name: str | None = None) -> BaseProvider:
    """Get a provider instance by name, or auto-detect from environment.

    Raises RuntimeError if no provider is available.
    """
    if name:
        if name not in _PROVIDERS:
            raise RuntimeError(
                f"Unknown provider '{name}'. "
                f"Available: {', '.join(_PROVIDERS)}"
            )
        cls = _PROVIDERS[name]
        if not cls.is_available():
            raise RuntimeError(
                f"Provider '{name}' is not configured. "
                f"Check environment variables or install dependencies.\n"
                f"See: https://github.com/XFWang522/vidscribe#providers"
            )
        return cls()

    for key in _PRIORITY:
        cls = _PROVIDERS[key]
        if cls.is_available():
            return cls()

    raise RuntimeError(
        "No ASR provider configured. Set up at least one:\n"
        "  - Volcengine:  export VOLC_APP_KEY=... VOLC_ACCESS_KEY=...\n"
        "  - OpenAI:      export OPENAI_API_KEY=sk-...\n"
        "  - Aliyun:      export DASHSCOPE_API_KEY=sk-...\n"
        "  - Deepgram:    export DEEPGRAM_API_KEY=...\n"
        "  - Local:       pip install vidscribe[local]\n"
        "See: https://github.com/XFWang522/vidscribe#providers"
    )
