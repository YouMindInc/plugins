# YouMind plugins

Official plugins for YouAgent. Each folder in `plugins/` is one plugin in the [agent-plugins.org 1.0.0](https://agent-plugins.org/specification) layout, so other agent-plugins.org clients can load it too.

A plugin has an MCP server, skills, or both. A plugin has both only when the vendor ships them together. Skills come from the vendor or another official source and are copied unchanged, with the upstream license.

## Plugins

| Plugin | MCP server | Skills | Source |
| --- | --- | --- | --- |
| `atlassian` | `https://mcp.atlassian.com/v2/mcp` | 6 | [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) |
| `canva` | `https://mcp.canva.com/mcp` | 7 | [canva-sdks/canva-skills](https://github.com/canva-sdks/canva-skills) |
| `huggingface` | `https://huggingface.co/mcp?login` | | [Hugging Face MCP docs](https://huggingface.co/docs/hub/hf-mcp-server) |
| `linear` | `https://mcp.linear.app/mcp` | | [Linear MCP docs](https://linear.app/docs/mcp) |
| `neon` | `https://mcp.neon.tech/mcp` | 9 | [neondatabase/agent-skills](https://github.com/neondatabase/agent-skills) |
| `notion` | `https://mcp.notion.com/mcp` | 4 | [makenotion/claude-code-notion-plugin](https://github.com/makenotion/claude-code-notion-plugin) |
| `sentry` | `https://mcp.sentry.dev/mcp` | 8 | [getsentry/plugin-claude](https://github.com/getsentry/plugin-claude) |
| `slack` | `https://mcp.slack.com/mcp` | 9 | [slackapi/slack-mcp-plugin](https://github.com/slackapi/slack-mcp-plugin) |
| `stripe` | `https://mcp.stripe.com` | 10 | [stripe/ai](https://github.com/stripe/ai) |
| `supabase` | `https://mcp.supabase.com/mcp` | 2 | [supabase-community/supabase-plugin](https://github.com/supabase-community/supabase-plugin) |
| `vercel` | `https://mcp.vercel.com` | | [Vercel MCP docs](https://vercel.com/docs/agent-resources/vercel-mcp) |
| `doc` | | Word (`.docx`) | [openai/skills](https://github.com/openai/skills) |
| `pdf` | | PDF | [openai/skills](https://github.com/openai/skills) |
| `slides` | | PowerPoint (`.pptx`) | [openai/skills](https://github.com/openai/skills) |
| `spreadsheet` | | Excel (`.xlsx`), CSV, TSV | [openai/skills](https://github.com/openai/skills) |

Every MCP server above is the vendor's hosted server. Users sign in with their own account through OAuth. Each server supports dynamic client registration, except Slack, whose OAuth client YouAgent provides. The `repository` field of each `plugin.json` links the upstream commit the files came from.

## Layout

```
plugins/<name>/
  plugin.json             manifest
  mcp.json                MCP servers (optional)
  skills/<skill>/SKILL.md one folder per skill (optional)
  com.youmind/icon.svg    icon, or icon.png
  LICENSE                 upstream license, when the plugin copies upstream files
```

## Rules

YouAgent builds its plugin catalog from a commit of this repo with `youagent-plugin-catalog publish <checkout> <commit>`. The tool rejects a commit that breaks one of these rules:

- Each entry in `plugins/` is a folder, and its name equals `name` in its `plugin.json`.
- `version` is SemVer, `MAJOR.MINOR.PATCH` with an optional `-PRERELEASE`. Build metadata (`+BUILD`) is not allowed.
- A change to a published plugin raises its `version`. A published release never changes.
- Each `skills/<skill>/SKILL.md` has YAML frontmatter with a `name` equal to the folder name and a non-empty `description`.
- `mcp.json` has `"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"`. A `stdio` server's `command` is a bare name or a `./` path inside the plugin folder, and its `cwd` stays inside the plugin folder or `${PLUGIN_DATA}`.
- Every file is a regular file. Symlinks and submodules are not allowed.
- `extensions."com.youmind"` has only the keys in the next section. The icon is at most 64 KiB.
- `plugin.json` has `"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"` and no top-level keys outside the [1.0.0 plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json).
- A skill `description` is at most 1024 characters.
- A plugin folder is at most 1 MiB in total file bytes.

## The `com.youmind` extension

YouMind data goes in `extensions."com.youmind"` of `plugin.json`, because `plugin.json` allows no new top-level keys. All keys are optional.

| Key | Meaning | Values | Default |
| --- | --- | --- | --- |
| `displayName` | The name Settings shows | 1 to 64 characters | `name` |
| `category` | The group Settings shows the plugin under | 1 to 64 characters | `Other` |
| `icon` | The icon Settings shows | `./com.youmind/<file>.svg` or `.png`, at most 64 KiB | A generic icon |
| `machines` | Which machines get the plugin folder | `types`: `device`, `cloud`. `os`: `macos`, `linux`, `windows`. | Every type and every OS |

`machines` applies to the whole folder. A plugin that needs different targets for different parts ships as two plugins.

Do not declare where an MCP server runs. The publish tool derives it from `mcp.json`. A `streamable-http` server with a public `https` URL and no `Authorization` header runs on the YouMind server. Every other server runs on the machine.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "linear",
  "version": "1.0.0",
  "description": "Find, create, and update Linear issues, projects, and comments through the Linear MCP server.",
  "author": { "name": "Linear" },
  "homepage": "https://linear.app/docs/mcp",
  "extensions": {
    "com.youmind": {
      "displayName": "Linear",
      "category": "Productivity",
      "icon": "./com.youmind/icon.svg"
    }
  }
}
```
