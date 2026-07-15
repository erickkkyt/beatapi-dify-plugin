# BeatAPI Dify Plugin Privacy Notice

Last updated: July 15, 2026

This plugin connects a Dify workspace to the BeatAPI service.

## Data sent to BeatAPI

When a user invokes a tool, the plugin sends the following data to
`https://api.beatapi.io`:

- the BeatAPI API key stored in Dify, in the `Authorization` request header;
- public image, audio, subtitle, or lip-reference URLs supplied by the user;
- optional prompts and video-generation settings;
- the BeatAPI task ID when checking task status.

BeatAPI may retrieve the public media URLs to perform the requested workflow.
The plugin itself does not add analytics, advertising trackers, or independent
data storage.

## Credential handling

The API key is managed by Dify's provider credential system. The plugin does not
write the API key to prompts, tool output, logs, URLs, or local files. Users can
create and revoke API keys at https://beatapi.io/dashboard/apikeys.

## Service policies and contact

BeatAPI's service privacy policy applies to data processed by BeatAPI. See
https://beatapi.io/privacy. For privacy or support questions, contact
support@beatapi.io.

