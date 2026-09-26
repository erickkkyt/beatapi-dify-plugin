# BeatAPI Dify Plugin Privacy Notice

Last updated: September 26, 2026

This plugin connects a Dify workspace to the BeatAPI service.

## Data sent to BeatAPI

When a user invokes a tool, the plugin sends the following data to
`https://api.beatapi.io`:

- the BeatAPI API key stored in Dify, in the `Authorization` request header;
- public image, audio, subtitle, or lip-reference URLs supplied by the user;
- prompts, generation settings, and inputs passed to a selected capability;
- social data and web search queries, which may contain personal data if the
  user includes it;
- the BeatAPI task ID when checking task status.

BeatAPI may retrieve user-supplied public media URLs and send task inputs to
upstream providers as needed for the requested capability. Search and Inspect
read the capability catalogue; Run can initiate a chargeable operation. The
plugin itself does not add analytics, advertising trackers, or independent
data storage. Dify and BeatAPI may retain requests and results under their
respective service policies.

## Credential handling

The API key is managed by Dify's provider credential system. The plugin does not
write the API key to prompts, tool output, logs, URLs, or local files. Users can
create and revoke API keys at https://beatapi.io/dashboard/apikeys.

## Service policies and contact

BeatAPI's service privacy policy applies to data processed by BeatAPI. See
https://beatapi.io/privacy-policy. For privacy or support questions, contact
support@beatapi.io.
