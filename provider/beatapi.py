from beatapi_client import BeatAPIClient, BeatAPIError
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class BeatapiProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        try:
            BeatAPIClient(str(credentials.get("api_key", ""))).get_usage()
        except (BeatAPIError, ValueError) as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc

