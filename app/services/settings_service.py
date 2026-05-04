import json
import os
from app.config import settings as app_settings

_SETTINGS_FILE = os.path.join(app_settings.file_storage_path, "_app_settings.json")

_data: dict = {
    "ai_provider": "anthropic",  # "anthropic" | "openai"
    "openai_model": "gpt-4o",
    "anthropic_model": "claude-haiku-4-5-20251001",
}


def _load() -> None:
    try:
        with open(_SETTINGS_FILE) as f:
            _data.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass


def _save() -> None:
    os.makedirs(os.path.dirname(_SETTINGS_FILE), exist_ok=True)
    with open(_SETTINGS_FILE, "w") as f:
        json.dump(_data, f, indent=2)


def get(key: str, default=None):
    return _data.get(key, default)


def set_value(key: str, value) -> None:
    _data[key] = value
    _save()


def all_settings() -> dict:
    return dict(_data)


_load()
