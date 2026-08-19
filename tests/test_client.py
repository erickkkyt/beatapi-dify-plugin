from __future__ import annotations

import unittest
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError


class FakeResponse:
    def __init__(self, status_code: int, payload: dict[str, Any]) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, Any]:
        return self._payload


class RequestRecorder:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.calls: list[dict[str, Any]] = []

    def __call__(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(kwargs)
        return self.response


class BeatAPIClientTests(unittest.TestCase):
    def test_get_usage_authenticates_and_unwraps_the_public_envelope(self) -> None:
        request = RequestRecorder(
            FakeResponse(
                200,
                {"data": {"object": "usage", "credit_balance": 120}},
            )
        )
        client = BeatAPIClient("sk_test", request=request)

        result = client.get_usage()

        self.assertEqual(
            result,
            {"object": "usage", "credit_balance": 120},
        )
        self.assertEqual(len(request.calls), 1)
        self.assertEqual(request.calls[0]["method"], "GET")
        self.assertEqual(request.calls[0]["url"], "https://api.beatapi.io/v1/usage")
        self.assertEqual(
            request.calls[0]["headers"]["Authorization"],
            "Bearer sk_test",
        )

    def test_create_music_video_task_sends_only_meaningful_inputs(self) -> None:
        request = RequestRecorder(
            FakeResponse(
                201,
                {"data": {"id": "task_123", "status": "queued"}},
            )
        )
        client = BeatAPIClient("sk_test", request=request)

        result = client.create_music_video_task(
            images=["https://media.example.com/cover.png"],
            audio_url="https://media.example.com/song.mp3",
            prompt="Neon city performance",
            quality=None,
        )

        self.assertEqual(result, {"id": "task_123", "status": "queued"})
        self.assertEqual(
            request.calls[0]["json"],
            {
                "images": ["https://media.example.com/cover.png"],
                "audio_url": "https://media.example.com/song.mp3",
                "prompt": "Neon city performance",
            },
        )

    def test_unified_generation_and_effect_methods_use_public_routes(self) -> None:
        request = RequestRecorder(
            FakeResponse(200, {"data": {"object": "list", "data": []}})
        )
        client = BeatAPIClient("sk_test", request=request)

        self.assertEqual(client.list_generation_models(), [])
        client.create_image_task({"model": "nano-banana", "prompt": "Still"})
        client.create_video_task({"model": "seedance-2-mini", "prompt": "Orbit"})
        self.assertEqual(client.list_effects(output_type="video"), [])

        request.response = FakeResponse(
            200, {"data": {"id": "video-muscle-max", "object": "effect"}}
        )
        client.get_effect("video/muscle")
        client.create_effect_task(
            {
                "effect_id": "video-muscle-max",
                "images": ["https://media.example.com/portrait.png"],
            },
            idempotency_key="effect-dify-123",
        )

        self.assertEqual(
            [(call["method"], call["url"]) for call in request.calls],
            [
                ("GET", "https://api.beatapi.io/v1/media/models"),
                ("POST", "https://api.beatapi.io/v1/images/tasks"),
                ("POST", "https://api.beatapi.io/v1/videos/tasks"),
                ("GET", "https://api.beatapi.io/v1/effects?output_type=video"),
                ("GET", "https://api.beatapi.io/v1/effects/video%2Fmuscle"),
                ("POST", "https://api.beatapi.io/v1/effects/tasks"),
            ],
        )
        self.assertEqual(
            request.calls[-1]["headers"]["Idempotency-Key"],
            "effect-dify-123",
        )

    def test_api_errors_keep_the_public_error_code_and_request_id(self) -> None:
        request = RequestRecorder(
            FakeResponse(
                402,
                {
                    "error": {
                        "code": "insufficient_credits",
                        "message": "Account balance is not sufficient.",
                        "request_id": "req_123",
                    }
                },
            )
        )
        client = BeatAPIClient("sk_test", request=request)

        with self.assertRaises(BeatAPIError) as captured:
            client.get_task("task_123")

        self.assertEqual(captured.exception.code, "insufficient_credits")
        self.assertEqual(captured.exception.request_id, "req_123")
        self.assertIn("Account balance is not sufficient", str(captured.exception))


if __name__ == "__main__":
    unittest.main()
