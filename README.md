# BeatAPI for Dify

Discover BeatAPI models, social data, web tools and workflows, and create or
monitor image, video, Effect, and music-video tasks from Dify.

- Website: https://beatapi.io/
- API documentation: https://docs.beatapi.io/
- Create an API key: https://beatapi.io/dashboard/apikeys
- Source code: https://github.com/erickkkyt/beatapi-dify-plugin

## Tools

The plugin exposes eleven tools against the current BeatAPI public contract:

- **Search Capabilities**, **Inspect Capability**, and **Run Capability** —
  discover current model, social data, web, or workflow capabilities and inspect
  their fields, price, readiness, and execution strategy. Use Run only when
  Inspect says it is supported; direct API capabilities use their documented
  endpoint instead. These are advanced tools for agents that discover
  capabilities at run time. A Run start may spend BeatAPI credits.

- **List Generation Models** — discover stable image/video aliases and input modes.
- **Create Image Task** — generate or edit images with `nano-banana`,
  `nano-banana-pro`, `gpt-image-2`, or `seedream-5-pro`.
- **Create Video Task** — generate text, frame, or reference video with
  `minimax-h3`, `seedance-2`, `seedance-2-fast`, `seedance-2-mini`, `veo-3.1`,
  `seedance-2.5`, or `kling-3`.
- **List Effects** and **Get Effect** — read each published Effect's versioned
  image-count, media, output, and option contract.
- **Create Effect Task** — run a selected Effect with a retry-safe idempotency key.
- **Create Music Video Task** — run the higher-level Music Video workflow.
- **Get Task** — poll every asynchronous task through the shared lifecycle.

Model aliases are BeatAPI's public contract. The plugin never exposes or
selects internal providers, templates, or routing IDs.

For the native Dify LLM node, configure BeatAPI as an OpenAI-compatible model
provider using `https://api.beatapi.io/v1`. Text models that Inspect marks as
`direct_api` use their documented endpoint, not the Run tool. This tool plugin
does not add models to Dify's native model picker.

### Create Music Video Task

Starts a BeatAPI `music-video` workflow using one to seven public HTTPS image
URLs and one public HTTPS audio URL. It returns a task ID immediately, so long
renders do not block the Dify tool call.

The tool exposes BeatAPI's optional creative, quality, aspect-ratio, lip-sync,
subtitle, duration-fallback, and composition controls. `auto` composition is the
default and returns a finished hosted video. `manual` returns a storyboard that
can be edited and composed through the BeatAPI API.

### Get Task

Returns the current task status, stage, output, usage, request ID, and public
error fields. Poll every 5-10 seconds until the task reaches `succeeded` or
`failed`; manual tasks can pause at `storyboard_ready` for later editing.

Every current task includes `task_kind`, `capability_id`, and
`capability_version`. Usage values are decimal USD amounts. Compatibility field
names such as `credits_reserved` remain in the response, where 1 Credit equals
$1 USD.

## Install from GitHub

In Dify, open **Plugins > Install Plugin > GitHub**, then enter:

`erickkkyt/beatapi-dify-plugin`

## Configure

1. Create a revocable API key at https://beatapi.io/dashboard/apikeys.
2. Open **Tools > BeatAPI > Authorize** in Dify.
3. Paste the API key. Dify verifies it with `GET /v1/usage`.
4. Add the named media tools you need to a Workflow or Chatflow. For an Agent
   that discovers capabilities dynamically, add Search, Inspect, and Run.

The API key is sent only in the `Authorization: Bearer` header to
`https://api.beatapi.io`. Never place it in prompts or tool parameters.

## Example workflow

1. Call **List Generation Models** or **List Effects** when the capability is
   not already known.
2. Supply public HTTPS media URLs and call the matching create tool.
3. Store the returned `id`.
4. Wait 5-10 seconds and call **Get Task** with that ID.
5. Repeat with a bounded loop until the task reaches a terminal state.
6. Read the BeatAPI-hosted image or video URL from `output.media` or `output.r2_url`.

## Local development

The plugin requires Python 3.12 and the Dify CLI.

```bash
uv sync
cp .env.example .env
uv run python -m main
```

Run the behavior tests:

```bash
PYTHONPATH=. uv run python -m unittest discover -s tests -v
```

Package the plugin from the parent directory:

```bash
dify plugin package ./beatapi
```

## Support

Email support@beatapi.io or visit https://beatapi.io/.

## Current gateway update (0.3.0)

Added named Web Search, Read, Map and Research tools with JSON input matching
`https://docs.beatapi.io/web-search`. Search supports `view` and `group_by`.
Run already supports preview, fields and free stored-result reads. Web Research
can return a pending task after 85 seconds; use Run operation=status to poll,
never start another research request. Requests preserve raw result envelopes,
use bounded operation-specific timeouts and do not follow authenticated redirects.
Models and pricing are discovered at runtime through Search and Inspect.
