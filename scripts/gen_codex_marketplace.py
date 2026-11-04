#!/usr/bin/env python3
"""Generate the Codex marketplace manifest and com.openai interface blocks.

Usage: python3 -I gen_codex_marketplace.py <plugins-repo-root> [--check]

Reads every plugins/<dir>/plugin.json, derives `extensions."com.openai".interface`
from `com.youmind` plus the top-level Agent Plugins fields, and writes
.agents/plugins/marketplace.json. Codex replaces its derived interface with the
com.openai one wholesale (agent_plugin_manifest.rs apply_codex_agent_plugin_extension),
so the block carries every field Codex would otherwise derive. A plugin's patch
version is bumped only when its com.openai block changes, so reruns are no-ops.
"""

import json
import sys
from pathlib import Path

MARKETPLACE_NAME = "youmind"
MARKETPLACE_DISPLAY_NAME = "YouMind"
MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
POLICY = {"installation": "AVAILABLE", "authentication": "ON_USE"}


def dump(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def openai_interface(manifest):
    youmind = manifest["extensions"]["com.youmind"]
    interface = {
        "displayName": youmind["displayName"],
        "shortDescription": manifest["description"],
        "longDescription": manifest["description"],
        "developerName": manifest["author"]["name"],
        "category": youmind["category"],
        "websiteUrl": manifest["homepage"],
    }
    icon = youmind.get("icon")
    if icon:
        interface["composerIcon"] = icon
        interface["logo"] = icon
    return interface


def bump_patch(version):
    major, minor, patch = version.split(".")
    return f"{major}.{minor}.{int(patch) + 1}"


def with_openai_extension(manifest, interface):
    extensions = {}
    for key, value in manifest["extensions"].items():
        if key != "com.openai":
            extensions[key] = value
    extensions["com.openai"] = {"interface": interface}
    return {**manifest, "extensions": extensions}


def main():
    root = Path(sys.argv[1]).resolve()
    check = "--check" in sys.argv[2:]
    plugin_dirs = sorted(p for p in (root / "plugins").iterdir() if p.is_dir())
    entries = []
    stale = []

    for plugin_dir in plugin_dirs:
        manifest_path = plugin_dir / "plugin.json"
        manifest = json.loads(manifest_path.read_text())
        if manifest["name"] != plugin_dir.name:
            sys.exit(f"{manifest_path}: name {manifest['name']!r} != dir {plugin_dir.name!r}")
        icon = manifest["extensions"]["com.youmind"].get("icon")
        if icon and not (plugin_dir / icon).is_file():
            sys.exit(f"{manifest_path}: icon {icon} does not exist")

        interface = openai_interface(manifest)
        current = manifest["extensions"].get("com.openai")
        updated = with_openai_extension(manifest, interface)
        if current != {"interface": interface}:
            updated["version"] = bump_patch(manifest["version"])
            stale.append(str(manifest_path.relative_to(root)))
            if not check:
                manifest_path.write_text(dump(updated))

        entries.append(
            {
                "name": manifest["name"],
                "source": {"source": "local", "path": f"./plugins/{plugin_dir.name}"},
                "policy": dict(POLICY),
                "category": interface["category"],
            }
        )

    marketplace = {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": MARKETPLACE_DISPLAY_NAME},
        "plugins": entries,
    }
    marketplace_path = root / MARKETPLACE_PATH
    rendered = dump(marketplace)
    if not marketplace_path.is_file() or marketplace_path.read_text() != rendered:
        stale.append(str(MARKETPLACE_PATH))
        if not check:
            marketplace_path.parent.mkdir(parents=True, exist_ok=True)
            marketplace_path.write_text(rendered)

    if check and stale:
        sys.exit("stale: " + ", ".join(stale))
    print(f"{len(entries)} plugins; {'stale' if check else 'updated'}: {stale or 'none'}")


if __name__ == "__main__":
    main()
