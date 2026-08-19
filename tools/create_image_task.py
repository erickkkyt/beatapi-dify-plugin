from collections.abc import Generator
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError
from tool_inputs import parse_https_urls, parse_optional_json_object


class CreateImageTaskTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            payload: dict[str, Any] = {
                "model": str(tool_parameters.get("model", "")).strip(),
                "prompt": str(tool_parameters.get("prompt", "")).strip(),
                "aspect_ratio": tool_parameters.get("aspect_ratio"),
                "resolution": tool_parameters.get("resolution"),
                "output_format": tool_parameters.get("output_format"),
            }
            raw_images = str(tool_parameters.get("image_urls", "")).strip()
            if raw_images:
                payload["images"] = parse_https_urls(
                    raw_images, min_count=1, max_count=16, label="image"
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
            yield self.create_json_message(client.create_image_task(payload))
        except BeatAPIError as exc:
            details = f"BeatAPI error [{exc.code}]: {exc}"
            if exc.request_id:
                details += f" (request_id: {exc.request_id})"
            raise InvokeError(details) from exc
        except (TypeError, ValueError) as exc:
            raise InvokeError(str(exc)) from exc
