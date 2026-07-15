from collections.abc import Generator
from typing import Any

from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError
from tool_inputs import parse_image_urls


class CreateMusicVideoTaskTool(Tool):
    def _invoke(
        self,
        tool_parameters: dict[str, Any],
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            client = BeatAPIClient(str(self.runtime.credentials.get("api_key", "")))
            duration = tool_parameters.get("duration")
            if duration is not None and duration != "":
                duration = int(duration)

            task = client.create_music_video_task(
                images=parse_image_urls(str(tool_parameters.get("image_urls", ""))),
                audio_url=str(tool_parameters.get("audio_url", "")).strip(),
                prompt=tool_parameters.get("prompt"),
                language=tool_parameters.get("language"),
                quality=tool_parameters.get("quality"),
                resolution=tool_parameters.get("resolution"),
                aspect_ratio=tool_parameters.get("aspect_ratio"),
                style=tool_parameters.get("style"),
                lip_sync=tool_parameters.get("lip_sync"),
                lip_ref_url=tool_parameters.get("lip_ref_url"),
                add_subtitle=tool_parameters.get("add_subtitle"),
                subtitle_color=tool_parameters.get("subtitle_color"),
                srt_url=tool_parameters.get("srt_url"),
                duration=duration,
                compose_mode=tool_parameters.get("compose_mode"),
            )
            yield self.create_json_message(task)
        except BeatAPIError as exc:
            details = f"BeatAPI error [{exc.code}]: {exc}"
            if exc.request_id:
                details += f" (request_id: {exc.request_id})"
            raise InvokeError(details) from exc
        except (TypeError, ValueError) as exc:
            raise InvokeError(str(exc)) from exc

