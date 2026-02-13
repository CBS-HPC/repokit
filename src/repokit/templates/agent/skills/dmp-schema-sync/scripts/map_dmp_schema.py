#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_ref(schema: dict, ref: str) -> dict:
    if not ref.startswith("#/"):
        return {}
    node = schema
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict):
            return {}
        node = node.get(part, {})
    return node if isinstance(node, dict) else {}


def deref(schema: dict, node: dict) -> dict:
    if not isinstance(node, dict):
        return {}
    if "$ref" in node:
        base = resolve_ref(schema, node["$ref"])
        merged = dict(base) if isinstance(base, dict) else {}
        for k, v in node.items():
            if k != "$ref":
                merged[k] = v
        return merged
    return node


def collect_required_paths(schema: dict, node: dict, prefix: str = "") -> list[str]:
    node = deref(schema, node)
    out: list[str] = []

    if not isinstance(node, dict):
        return out

    for req in node.get("required", []):
        req_path = f"{prefix}.{req}" if prefix else req
        out.append(req_path)

    props = node.get("properties", {})
    if isinstance(props, dict):
        for key, child in props.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            out.extend(collect_required_paths(schema, child, child_prefix))

    items = node.get("items")
    if isinstance(items, dict):
        arr_prefix = f"{prefix}[*]" if prefix else "[*]"
        out.extend(collect_required_paths(schema, items, arr_prefix))

    return out


def has_path(data, path: str) -> bool:
    parts = path.split(".") if path else []

    def walk(node, idx: int) -> bool:
        if idx >= len(parts):
            return True
        part = parts[idx]
        if part.endswith("[*]"):
            key = part[:-3]
            if not isinstance(node, dict):
                return False
            arr = node.get(key)
            if not isinstance(arr, list) or not arr:
                return False
            return any(walk(item, idx + 1) for item in arr)
        if not isinstance(node, dict):
            return False
        if part not in node:
            return False
        return walk(node[part], idx + 1)

    return walk(data, 0)


def validate_with_jsonschema(data: dict, schema: dict) -> list[str]:
    try:
        from jsonschema import Draft7Validator
    except Exception:
        return ["jsonschema not installed; schema validation skipped"]

    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    out = []
    for e in errors:
        p = "/".join(str(x) for x in e.path) or "<root>"
        out.append(f"{p}: {e.message}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Map dmp.json against maDMP schema required fields.")
    ap.add_argument("--dmp", default="dmp.json")
    ap.add_argument("--schema", default="./bin/maDMP-schema-1.2.json")
    ap.add_argument("--out", default="dmp_schema_map.json")
    ns = ap.parse_args()

    dmp_path = Path(ns.dmp).resolve()
    schema_path = Path(ns.schema).resolve()
    out_path = Path(ns.out).resolve()

    if not dmp_path.exists():
        raise SystemExit(f"Missing dmp file: {dmp_path}")
    if not schema_path.exists():
        raise SystemExit(f"Missing schema file: {schema_path}")

    dmp = load_json(dmp_path)
    schema = load_json(schema_path)

    required = sorted(set(collect_required_paths(schema, schema)))
    present = [p for p in required if has_path(dmp, p)]
    missing = [p for p in required if p not in present]

    report = {
        "dmp_path": str(dmp_path),
        "schema_path": str(schema_path),
        "required_count": len(required),
        "present_required_count": len(present),
        "missing_required_count": len(missing),
        "required_paths": required,
        "present_required_paths": present,
        "missing_required_paths": missing,
        "validation_errors": validate_with_jsonschema(dmp, schema),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Wrote {out_path}")
    print(
        f"Required fields: {report['present_required_count']}/{report['required_count']} present; "
        f"{report['missing_required_count']} missing."
    )


if __name__ == "__main__":
    main()
