from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any
from urllib.parse import quote, urlencode


RequestFn = Callable[..., Any]


class BeatAPIError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        code: str = "beatapi_request_failed",
        request_id: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.request_id = request_id
        self.status_code = status_code


def _default_request(**kwargs: Any) -> Any:
    import requests

    return requests.request(**kwargs)


class BeatAPIClient:
    """Small public interface for BeatAPI task and discovery requests."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.beatapi.io",
        timeout: int = 30,
        request: RequestFn | None = None,
    ) -> None:
        normalized_key = api_key.strip()
        if not normalized_key:
            raise ValueError("A BeatAPI API key is required.")

        self._api_key = normalized_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._request_fn = request or _default_request

    def get_usage(self) -> dict[str, Any]:
        return self._request("GET", "/v1/usage")

    def list_generation_models(self) -> list[dict[str, Any]]:
        return self._list_data(self._request("GET", "/v1/media/models"))

    def create_image_task(self, input_data: Mapping[str, Any]) -> dict[str, Any]:
        return self._request(
            "POST",
            "/v1/images/tasks",
            json=self._compact(input_data),
        )

    def create_video_task(self, input_data: Mapping[str, Any]) -> dict[str, Any]:
        return self._request(
            "POST",
            "/v1/videos/tasks",
            json=self._compact(input_data),
        )

    def list_effects(
        self,
        *,
        output_type: str | None = None,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        query = urlencode(
            self._compact({"output_type": output_type, "category": category})
        )
        path = f"/v1/effects?{query}" if query else "/v1/effects"
        return self._list_data(self._request("GET", path))

    def get_effect(self, effect_id: str) -> dict[str, Any]:
        normalized_effect_id = effect_id.strip()
        if not normalized_effect_id:
            raise ValueError("A BeatAPI Effect ID is required.")
        return self._request(
            "GET",
            f"/v1/effects/{quote(normalized_effect_id, safe='')}",
        )

    def create_effect_task(
        self,
        input_data: Mapping[str, Any],
        *,
        idempotency_key: str,
    ) -> dict[str, Any]:
        normalized_key = idempotency_key.strip()
        if not normalized_key:
            raise ValueError("An idempotency key is required for Effect tasks.")
        return self._request(
            "POST",
            "/v1/effects/tasks",
            json=self._compact(input_data),
            headers={"Idempotency-Key": normalized_key},
        )

    def create_music_video_task(
        self,
        *,
        images: list[str],
        audio_url: str,
        **options: Any,
    ) -> dict[str, Any]:
        payload = {
            "images": images,
            "audio_url": audio_url,
            **options,
        }
        return self._request(
            "POST",
            "/v1/music-video/tasks",
            json=self._compact(payload),
        )

    def get_task(self, task_id: str) -> dict[str, Any]:
        normalized_task_id = task_id.strip()
        if not normalized_task_id:
            raise ValueError("A BeatAPI task ID is required.")
        return self._request("GET", f"/v1/tasks/{quote(normalized_task_id, safe='')}")

    def search_capabilities(self, query: Mapping[str, Any]) -> dict[str, Any]:
        return self._request_envelope("POST", "/v1/capabilities/search", json=query)

    def inspect_capability(self, reference: str) -> dict[str, Any]:
        return self._request_envelope(
            "POST", "/v1/capabilities/inspect", json={"reference": reference}
        )

    def run_capability(self, request: Mapping[str, Any]) -> dict[str, Any]:
        return self._request_envelope("POST", "/v1/capabilities/run", json=request)

    def web_call(self, action: str, input_data: Mapping[str, Any]) -> dict[str, Any]:
        if action not in ("search", "read", "map", "research"):
            raise ValueError("Unknown Web action.")
        return self._request_envelope("POST", f"/v1/web/{action}", json=input_data)

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        payload = self._request_envelope(method, path, json=json, headers=headers)
        data = payload.get("data")
        if not isinstance(data, dict):
            raise BeatAPIError(
                "BeatAPI returned an unexpected response shape.",
                code="invalid_beatapi_response",
            )
        return data

    def _request_envelope(
        self,
        method: str,
        path: str,
        *,
        json: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        request_headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "BeatAPI-Dify-Plugin/0.3.0",
            **(headers or {}),
        }
        response = self._request_fn(
            method=method,
            url=f"{self._base_url}{path}",
            headers=request_headers,
            json=json,
            timeout=max(self._timeout, {"/v1/capabilities/run":95,"/v1/web/research":95,"/v1/web/read":75,"/v1/web/map":60}.get(path,30)),
            allow_redirects=False,
        )

        try:
            payload = response.json()
        except Exception as exc:
            raise BeatAPIError(
                "BeatAPI returned a non-JSON response.",
                status_code=getattr(response, "status_code", None),
            ) from exc

        status_code = getattr(response, "status_code", None)
        if status_code is None or status_code < 200 or status_code >= 300:
            error = payload.get("error", {}) if isinstance(payload, dict) else {}
            message = error.get("message") or "BeatAPI request failed."
            raise BeatAPIError(
                message,
                code=error.get("code") or "beatapi_request_failed",
                request_id=error.get("request_id"),
                status_code=status_code,
            )

        if not isinstance(payload, dict):
            raise BeatAPIError(
                "BeatAPI returned an unexpected response shape.",
                code="invalid_beatapi_response",
                status_code=status_code,
            )
        return payload

    @staticmethod
    def _compact(payload: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: value
            for key, value in payload.items()
            if value is not None and value != "" and value != []
        }

    @staticmethod
    def _list_data(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
        data = payload.get("data")
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise BeatAPIError(
                "BeatAPI returned an unexpected list response shape.",
                code="invalid_beatapi_response",
            )
        return data
