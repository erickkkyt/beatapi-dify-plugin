from collections.abc import Generator
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError
from tool_inputs import parse_https_urls, parse_optional_json_object


class CreateVideoTaskTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            duration = tool_parameters.get("duration")
            if duration is not None and duration != "":
                duration = int(duration)

            payload: dict[str, Any] = {
                "model": str(tool_parameters.get("model", "")).strip(),
                "prompt": str(tool_parameters.get("prompt", "")).strip(),
                "duration": duration,
                "aspect_ratio": tool_parameters.get("aspect_ratio"),
                "resolution": tool_parameters.get("resolution"),
                "generate_audio": tool_parameters.get("generate_audio"),
            }
            url_fields = (
                ("image_urls", "images", 2, "frame image"),
                ("reference_image_urls", "reference_images", 30, "reference image"),
                ("reference_video_urls", "reference_videos", 10, "reference video"),
                ("reference_audio_urls", "reference_audios", 10, "reference audio"),
            )
            for parameter, request_field, maximum, label in url_fields:
                raw = str(tool_parameters.get(parameter, "")).strip()
                if raw:
                    payload[request_field] = parse_https_urls(
                        raw, min_count=1, max_count=maximum, label=label
                    )

            advanced = parse_optional_json_object(
                str(tool_parameters.get("advanced_options_json", ""))
            )
            conflicts = set(payload) & set(advanced)
            if conflicts:
                names = ", ".join(sorted(conflicts))
                raise ValueError(f"Advanced options duplicate structured fields: {names}.")
            payload.update(advanced)

            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            yield self.create_json_message(client.create_video_task(payload))
        except BeatAPIError as exc:
            details = f"BeatAPI error [{exc.code}]: {exc}"
            if exc.request_id:
                details += f" (request_id: {exc.request_id})"
            raise InvokeError(details) from exc
        except (TypeError, ValueError) as exc:
            raise InvokeError(str(exc)) from exc
