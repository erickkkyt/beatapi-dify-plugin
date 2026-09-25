from collections.abc import Generator
from typing import Any
from uuid import uuid4

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError
from tool_inputs import parse_https_urls, parse_optional_json_object


class CreateEffectTaskTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            effect_version = tool_parameters.get("effect_version")
            if effect_version is not None and effect_version != "":
                effect_version = int(effect_version)

            payload = {
                "effect_id": str(tool_parameters.get("effect_id", "")).strip(),
                "effect_version": effect_version,
                "images": parse_https_urls(
                    str(tool_parameters.get("image_urls", "")),
                    min_count=1,
                    max_count=7,
                    label="image",
                ),
                "options": parse_optional_json_object(
                    str(tool_parameters.get("options_json", ""))
                ),
            }
            idempotency_key = (
                str(tool_parameters.get("idempotency_key", "")).strip()
                or str(uuid4())
            )
            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            yield self.create_json_message(
                client.create_effect_task(
                    payload,
                    idempotency_key=idempotency_key,
                )
            )
        except BeatAPIError as exc:
            details = f"BeatAPI error [{exc.code}]: {exc}"
            if exc.request_id:
                details += f" (request_id: {exc.request_id})"
            raise InvokeError(details) from exc
        except (TypeError, ValueError) as exc:
            raise InvokeError(str(exc)) from exc
