#!/usr/bin/env python3
"""Detect or add the public scite MCP. No secrets. No tokens on argv or disk.

Cursor layout observed in the wild: ~/.cursor/mcp.json → mcpServers.scite
with url https://api.scite.ai/mcp and empty headers (OAuth in the editor UI).
Zed: ~/.config/zed/settings.json → context_servers.scite.url
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCITE_URL = "https://api.scite.ai/mcp"
CURSOR_MCP = Path(os.environ.get("CBA_SCITE_CURSOR_MCP", Path.home() / ".cursor" / "mcp.json"))
ZED_SETTINGS = Path(os.environ.get("CBA_SCITE_ZED_SETTINGS", Path.home() / ".config" / "zed" / "settings.json"))
APP_SUPPORT_MCP = (
    Path.home()
    / "Library"
    / "Application Support"
    / "Cursor"
    / "User"
    / "globalStorage"
    / "cursor.mcp"
    / "mcp.json"
)

NAME_HINTS = ("scite", "user-scite")
URL_HINTS = ("scite.ai", "api.scite.ai/mcp")


def _looks_like_scite(name: str, entry: object) -> bool:
    n = (name or "").lower()
    if n in NAME_HINTS or "scite" in n:
        return True
    blob_parts: list[str] = []
    if isinstance(entry, dict):
        for key in ("url", "command", "serverUrl", "href"):
            val = entry.get(key)
            if val:
                blob_parts.append(str(val))
        args = entry.get("args")
        if isinstance(args, list):
            blob_parts.extend(str(a) for a in args)
        elif args:
            blob_parts.append(str(args))
    elif isinstance(entry, str):
        blob_parts.append(entry)
    blob = " ".join(blob_parts).lower()
    if "scite" in blob:
        return True
    return any(h in blob for h in URL_HINTS)


def _load_json(path: Path) -> tuple[object | None, str]:
    """Return (data, mode). mode is 'json', 'jsonc-header', or 'comments'."""
    if not path.is_file():
        return None, "missing"
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text), "json"
    except json.JSONDecodeError:
        pass
    # Zed default: // comments, then a JSON object.
    stripped = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    stripped = re.sub(r"/\*.*?\*/", "", stripped, flags=re.S)
    try:
        json.loads(stripped)
    except json.JSONDecodeError:
        return None, "comments"
    if re.search(r"^\s*//", text, re.M) and "{" in text:
        return json.loads(stripped), "jsonc-header"
    return None, "comments"


def _mcp_servers(data: object) -> dict:
    if not isinstance(data, dict):
        return {}
    for key in ("mcpServers", "servers"):
        val = data.get(key)
        if isinstance(val, dict):
            return val
    return {}


def _context_servers(data: object) -> dict:
    if not isinstance(data, dict):
        return {}
    val = data.get("context_servers")
    return val if isinstance(val, dict) else {}


def detect_cursor() -> bool:
    for path in (CURSOR_MCP, APP_SUPPORT_MCP):
        data, _mode = _load_json(path)
        if data is None:
            continue
        servers = _mcp_servers(data)
        for name, entry in servers.items():
            if _looks_like_scite(str(name), entry):
                return True
        if (
            isinstance(data, dict)
            and "scite" in data
            and _looks_like_scite("scite", data.get("scite"))
        ):
            return True
    return False


def detect_zed() -> bool:
    data, _mode = _load_json(ZED_SETTINGS)
    if data is None:
        return False
    servers = _context_servers(data)
    for name, entry in servers.items():
        if _looks_like_scite(str(name), entry):
            return True
    return False


def merge_cursor() -> str:
    """Add mcpServers.scite url entry. Returns 'added' | 'present' | 'snippet'."""
    if detect_cursor():
        return "present"
    data, mode = _load_json(CURSOR_MCP)
    # Cursor mcp.json: never rewrite a file that already has comments.
    if mode in ("comments", "jsonc-header"):
        return "snippet"
    if data is None or mode == "missing":
        data = {"mcpServers": {}}
        mode = "json"
    if not isinstance(data, dict):
        return "snippet"
    servers = data.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        return "snippet"
    for name, entry in servers.items():
        if _looks_like_scite(str(name), entry):
            return "present"
    servers["scite"] = {"url": SCITE_URL}
    CURSOR_MCP.parent.mkdir(parents=True, exist_ok=True)
    CURSOR_MCP.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return "added"


def merge_zed() -> str:
    if detect_zed():
        return "present"
    path = ZED_SETTINGS
    data, mode = _load_json(path)
    if mode == "comments":
        return "snippet"
    header = ""
    raw = path.read_text(encoding="utf-8") if path.is_file() else ""
    if mode == "jsonc-header":
        idx = raw.find("{")
        header = raw[:idx]
        data = json.loads(re.sub(r"/\*.*?\*/", "", re.sub(r"^\s*//.*$", "", raw[idx:], flags=re.M), flags=re.S))
    if data is None or mode == "missing":
        data = {}
        header = ""
    if not isinstance(data, dict):
        return "snippet"
    servers = data.setdefault("context_servers", {})
    if not isinstance(servers, dict):
        return "snippet"
    for name, entry in servers.items():
        if _looks_like_scite(str(name), entry):
            return "present"
    servers["scite"] = {"url": SCITE_URL}
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(data, indent=2) + "\n"
    path.write_text(header + body, encoding="utf-8")
    return "added"


def snippet_cursor() -> str:
    return (
        '{"mcpServers":{"scite":{"url":"https://api.scite.ai/mcp"}}}'
    )


def snippet_zed() -> str:
    return (
        '{"context_servers":{"scite":{"url":"https://api.scite.ai/mcp"}}}'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect or add scite MCP (no secrets)")
    parser.add_argument("action", choices=("detect-cursor", "detect-zed", "merge-cursor", "merge-zed"))
    args = parser.parse_args()
    if args.action == "detect-cursor":
        print("present" if detect_cursor() else "absent")
        return 0
    if args.action == "detect-zed":
        print("present" if detect_zed() else "absent")
        return 0
    if args.action == "merge-cursor":
        result = merge_cursor()
        print(result)
        return 0
    result = merge_zed()
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
