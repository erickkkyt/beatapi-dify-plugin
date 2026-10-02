from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError
from beatapi_client import BeatAPIClient, BeatAPIError
from tool_inputs import parse_json_object

class WebMapTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            payload = parse_json_object(str(tool_parameters.get("input_json") or ""), name="Web input")
            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            yield self.create_json_message(client.web_call("map", payload))
        except (BeatAPIError, TypeError, ValueError) as exc:
            raise InvokeError(str(exc)) from exc
