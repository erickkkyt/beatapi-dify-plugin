from __future__ import annotations

import json
import re
from urllib.parse import urlparse


def parse_image_urls(value: str) -> list[str]:
    """Normalize Dify's text input into BeatAPI's one-to-seven image list."""

    raw = (value or "").strip()
    if not raw:
        raise ValueError("Provide 1 to 7 public HTTPS image URLs.")

    if raw.startswith("["):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("Image URLs must be valid JSON or comma/newline text.") from exc
        if not isinstance(parsed, list) or not all(
            isinstance(item, str) for item in parsed
        ):
            raise ValueError("Image URL JSON must be an array of strings.")
        candidates = parsed
    else:
        candidates = re.split(r"[,\n\r]+", raw)

    images: list[str] = []
    for candidate in candidates:
        image_url = candidate.strip()
        if not image_url or image_url in images:
            continue
        parsed_url = urlparse(image_url)
        if parsed_url.scheme != "https" or not parsed_url.netloc:
            raise ValueError("Every image must use a public HTTPS URL.")
        images.append(image_url)

    if not 1 <= len(images) <= 7:
        raise ValueError("Provide 1 to 7 public HTTPS image URLs.")
    return images
