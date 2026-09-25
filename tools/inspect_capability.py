from collections.abc import Generator
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError


class InspectCapabilityTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        reference = str(tool_parameters.get("reference", "")).strip()
        if not reference:
            raise InvokeError("A capability reference from Search is required.")
        try:
            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            yield self.create_json_message(client.inspect_capability(reference))
        except (BeatAPIError, ValueError) as exc:
            raise InvokeError(str(exc)) from exc
