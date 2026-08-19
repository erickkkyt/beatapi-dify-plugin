from collections.abc import Generator
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError


class ListGenerationModelsTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            yield self.create_json_message(
                {"object": "list", "data": client.list_generation_models()}
            )
        except BeatAPIError as exc:
            details = f"BeatAPI error [{exc.code}]: {exc}"
            if exc.request_id:
                details += f" (request_id: {exc.request_id})"
            raise InvokeError(details) from exc
