from collections.abc import Generator
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError


class GetTaskTool(Tool):
    def _invoke(
        self,
        tool_parameters: dict[str, Any],
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            task = client.get_task(str(tool_parameters.get("task_id", "")))
            yield self.create_json_message(task)
        except BeatAPIError as exc:
            details = f"BeatAPI error [{exc.code}]: {exc}"
            if exc.request_id:
                details += f" (request_id: {exc.request_id})"
            raise InvokeError(details) from exc
        except ValueError as exc:
            raise InvokeError(str(exc)) from exc

