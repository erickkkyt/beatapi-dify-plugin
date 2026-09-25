from collections.abc import Generator
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError
from tool_inputs import parse_json_fields, parse_json_object


class RunCapabilityTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        reference = str(tool_parameters.get("reference", "")).strip()
        operation = str(tool_parameters.get("operation") or "start").strip()
        if not reference:
            raise InvokeError("An inspected capability reference is required.")
        if operation not in ("start", "status", "result"):
            raise InvokeError("Operation must be start, status, or result.")

        request: dict[str, Any] = {"reference": reference, "operation": operation}
        try:
            if operation == "start":
                raw_input = str(tool_parameters.get("input_json") or "").strip()
                if not raw_input:
                    raise ValueError("Input JSON is required to start a capability.")
                request["input"] = parse_json_object(raw_input, name="Input")
                if tool_parameters.get("idempotency_key"):
                    request["idempotency_key"] = str(tool_parameters["idempotency_key"]).strip()
            elif operation == "status":
                task_id = str(tool_parameters.get("task_id") or "").strip()
                if not task_id:
                    raise ValueError("Task ID is required for status.")
                request["task_id"] = task_id
            else:
                request_id = str(tool_parameters.get("request_id") or "").strip()
                if not request_id:
                    raise ValueError("Request ID is required for result.")
                request["request_id"] = request_id

            request["view"] = str(tool_parameters.get("view") or "preview")
            if tool_parameters.get("max_items") not in (None, ""):
                request["max_items"] = int(tool_parameters["max_items"])
            if tool_parameters.get("fields_json"):
                request["fields"] = parse_json_fields(str(tool_parameters["fields_json"]))
            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            yield self.create_json_message(client.run_capability(request))
        except (BeatAPIError, TypeError, ValueError) as exc:
            raise InvokeError(str(exc)) from exc
