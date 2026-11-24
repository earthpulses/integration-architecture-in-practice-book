#!/usr/bin/env python3
"""Summarize an OpenAPI 3.x document the way an architect reads it.

Usage: python3 openapi_recon.py openapi.json
"""
import json, sys

METHODS = ("get", "post", "put", "patch", "delete")
PAGING = {"limit", "page_size", "per_page", "pagesize",
          "cursor", "offset", "page"}
SINCE = {"updatedsince", "modified_since", "modifiedsince",
         "since", "updated_after"}

def params_of(item, op):
    found = {}
    for p in item.get("parameters", []) + op.get("parameters", []):
        found[p.get("name", "").lower()] = p.get("in")
    return found

def analyze(spec):
    info = {"title": spec.get("info", {}).get("title", "?"),
            "version": spec.get("info", {}).get("version", "?"),
            "servers": [s.get("url") for s in spec.get("servers", [])],
            "security": {}, "endpoints": [], "hints": [], "gaps": []}
    hints, gaps = info["hints"], info["gaps"]
    schemes = spec.get("components", {}).get("securitySchemes", {})
    for name, s in schemes.items():
        kind = s.get("type")
        if kind == "oauth2":
            kind += " (" + ", ".join(s.get("flows", {})) + ")"
        elif kind == "http":
            kind += " " + s.get("scheme", "")
        info["security"][name] = kind
    for path, item in spec.get("paths", {}).items():
        for method in METHODS:
            op = item.get(method)
            if not op:
                continue
            prm = params_of(item, op)
            codes = set(op.get("responses", {}))
            name = "%s %s" % (method.upper(), path)
            info["endpoints"].append(
                {"op": name, "params": sorted(prm), "codes": sorted(codes)})
            is_list = method == "get" and not path.rstrip("/").endswith("}")
            if is_list and not PAGING & set(prm):
                gaps.append("%s is a list with no paging parameter" % name)
            if is_list and SINCE & set(prm):
                found = ", ".join(sorted(SINCE & set(prm)))
                hints.append("%s supports incremental reads (%s)"
                             % (name, found))
            if method == "post" and "idempotency-key" not in prm:
                gaps.append("%s has no Idempotency-Key header" % name)
            if "202" in codes:
                hints.append("%s is asynchronous (202): plan polling" % name)
            if any(w in path.lower() for w in ("bulk", "batch", "import")):
                hints.append("%s is a bulk candidate" % name)
            if "429" not in codes:
                gaps.append("%s documents no 429 response" % name)
    if not info["servers"]:
        gaps.append("no servers listed: base URL and sandbox unknown")
    if not info["security"]:
        gaps.append("no security schemes declared")
    return info

def main(path):
    with open(path) as f:
        info = analyze(json.load(f))
    print("%s %s" % (info["title"], info["version"]))
    print("Servers:  ", ", ".join(info["servers"]) or "none")
    print("Security: ", info["security"] or "none")
    print("Endpoints: %d" % len(info["endpoints"]))
    for e in info["endpoints"]:
        print("  %-28s codes=%s" % (e["op"], ",".join(e["codes"])))
    for title, key in (("Hints", "hints"), ("Gaps to ask about", "gaps")):
        print("\n%s:" % title)
        for line in info[key] or ["none"]:
            print("  -", line)

if __name__ == "__main__":
    main(sys.argv[1])
