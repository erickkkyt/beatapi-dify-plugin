# BeatAPI for Dify

Create and monitor asynchronous AI music video tasks from Dify Workflows,
Chatflows, and Agents.

- Website: https://beatapi.io/
- API documentation: https://docs.beatapi.io/
- Create an API key: https://beatapi.io/dashboard/apikeys

## Tools

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

## Install from GitHub

In Dify, open **Plugins > Install Plugin > GitHub**, then enter:

`erickkkyt/beatapi-dify-plugin`

## Configure

1. Create a revocable API key at https://beatapi.io/dashboard/apikeys.
2. Open **Tools > BeatAPI > Authorize** in Dify.
3. Paste the API key. Dify verifies it with `GET /v1/usage`.
4. Add **Create Music Video Task** and **Get Task** to a Workflow, Chatflow, or
   Agent.

The API key is sent only in the `Authorization: Bearer` header to
`https://api.beatapi.io`. Never place it in prompts or tool parameters.

## Example workflow

1. Produce or collect a public image URL and a 10-180 second public audio URL.
2. Call **Create Music Video Task**.
3. Store the returned `id`.
4. Wait 5-10 seconds and call **Get Task** with that ID.
5. Repeat with a bounded loop until the task reaches a terminal state.
6. Read the hosted video URL from the task output.

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

