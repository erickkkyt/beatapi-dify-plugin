from __future__ import annotations

import json
import re
from urllib.parse import urlparse


def parse_https_urls(
    value: str,
    *,
    min_count: int,
    max_count: int,
    label: str,
) -> list[str]:
    """Normalize Dify text into a bounded list of public HTTPS URLs."""

    raw = (value or "").strip()
    if not raw:
        raise ValueError(
            f"Provide {min_count} to {max_count} public HTTPS {label} URLs."
        )

    if raw.startswith("["):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"{label.capitalize()} URLs must be valid JSON or comma/newline text."
            ) from exc
        if not isinstance(parsed, list) or not all(
            isinstance(item, str) for item in parsed
        ):
            raise ValueError(f"{label.capitalize()} URL JSON must be an array of strings.")
        candidates = parsed
    else:
        candidates = re.split(r"[,\n\r]+", raw)

    urls: list[str] = []
    for candidate in candidates:
        item_url = candidate.strip()
        if not item_url or item_url in urls:
            continue
        parsed_url = urlparse(item_url)
        if parsed_url.scheme != "https" or not parsed_url.netloc:
            raise ValueError(f"Every {label} URL must use a public HTTPS URL.")
        urls.append(item_url)

    if not min_count <= len(urls) <= max_count:
        raise ValueError(
            f"Provide {min_count} to {max_count} public HTTPS {label} URLs."
        )
    return urls


def parse_image_urls(value: str) -> list[str]:
    """Normalize music-video input into BeatAPI's one-to-seven image list."""

    return parse_https_urls(
        value,
        min_count=1,
        max_count=7,
        label="image",
    )


def parse_optional_json_object(value: str | None) -> dict[str, object]:
    raw = (value or "").strip()
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Advanced options must be a valid JSON object.") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Advanced options must be a JSON object.")
    return parsed
