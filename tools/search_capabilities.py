from collections.abc import Generator
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError


class SearchCapabilitiesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            query = {
                key: tool_parameters[key]
                for key in ("query", "kind", "platform", "limit", "cursor")
                if tool_parameters.get(key) not in (None, "")
            }
            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            yield self.create_json_message(client.search_capabilities(query))
        except (BeatAPIError, ValueError) as exc:
            raise InvokeError(str(exc)) from exc
