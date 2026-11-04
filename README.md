# YouMind plugins

Plugins for YouAgent, with integrations for developer tools, productivity apps, and document workflows. Each plugin provides an MCP server, skills, or both, using the [agent-plugins.org 1.0.0 format](https://agent-plugins.org/specification).

MCP integrations connect to vendor-hosted servers. Sign in with your account through OAuth to authorize access. Skills provide instructions and tools for specific workflows.

## Plugin structure

```text
plugins/<name>/
  plugin.json             Plugin metadata
  mcp.json                MCP server configuration, when included
  skills/<skill>/SKILL.md  Skills, when included
  com.youmind/icon.svg     Plugin icon
  LICENSE                 Upstream license, when included
```

See each plugin's `plugin.json` for its description, version, and upstream links, and `mcp.json` for its server configuration. Compatible clients can load these folders using the agent-plugins.org format.

Codex reads the repository through `.agents/plugins/marketplace.json` and each plugin's `extensions."com.openai"` block. Both are generated from `plugin.json`: after changing a plugin, run `python3 -I scripts/gen_codex_marketplace.py .` and commit the result. `--check` fails when they are stale.

## Contributing

- Follow the [plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json). The plugin's `name` must match its folder name.
- Use vendor-hosted MCP endpoints and skills from official sources. Preserve upstream skill content and licenses.
- Give each skill YAML frontmatter with a `name` matching its folder and a non-empty `description`.
- Use a vector SVG icon with `width="64"`, `height="64"`, and `viewBox="0 0 64 64"`, at most 64 KiB, referenced by `extensions."com.youmind".icon`.
- Increment the plugin's SemVer version when changing a released plugin.

## Attribution

Upstream skills retain their original licenses, included in the corresponding plugin folders. Upstream sources are linked in each plugin’s `plugin.json`.

Cloudflare and Notion icons use [Devicon](https://github.com/devicons/devicon) artwork; its license is included in each plugin's `com.youmind/LICENSE`. The PostHog icon comes from [PostHog's brand assets](https://brand.posthog.com/).
