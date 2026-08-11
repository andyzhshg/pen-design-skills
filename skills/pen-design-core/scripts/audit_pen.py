#!/usr/bin/env python3
"""Read-only `.pen` structure/token and text-contrast audit."""

import argparse
import collections
import json
from pathlib import Path


PROPS = ("fill", "stroke", "cornerRadius", "padding", "gap", "strokeWidth", "fontSize", "fontWeight")


def is_var(value):
    return isinstance(value, str) and value.startswith("$")


def iter_values(value):
    if isinstance(value, list):
        for item in value:
            yield from iter_values(item)
    elif isinstance(value, dict):
        for key in ("color", "value"):
            if key in value:
                yield from iter_values(value[key])
                return
    else:
        yield value


def walk(node, frame, inherited_fill=None):
    if not isinstance(node, dict):
        return
    own_fill = node.get("fill")
    background = own_fill if isinstance(own_fill, str) else inherited_fill
    yield node, frame, inherited_fill
    for child in node.get("children") or []:
        yield from walk(child, frame, background)


def all_nodes(doc):
    for child in doc.get("children") or []:
        frame = child.get("name") or child.get("id") or "(unnamed)"
        yield from walk(child, frame)


def audit_structure(doc):
    stats = collections.Counter()
    frame_literals = collections.Counter()
    nodes = list(all_nodes(doc))
    for node, frame, _ in nodes:
        for prop in PROPS:
            for value in iter_values(node.get(prop)):
                if value is None:
                    continue
                kind = "var" if is_var(value) else "literal"
                stats[(prop, kind)] += 1
                if kind == "literal" and prop in ("fill", "stroke"):
                    frame_literals[frame] += 1

    variables = doc.get("variables") or {}
    imports = doc.get("imports") or []
    print(f"Document v{doc.get('version')} · top frames {len(doc.get('children') or [])} · nodes {len(nodes)}")
    print(f"Variables {len(variables)} · imports {len(imports)}")
    print("\n[Structure/token candidates]")
    for prop in PROPS:
        var, literal = stats[(prop, "var")], stats[(prop, "literal")]
        if not var and not literal:
            continue
        total = var + literal
        print(f"  {prop:14} variable {var:5} / literal {literal:5} / variable share {var / total:6.1%}")
    print("\n[Frames with most literal color candidates]")
    for name, count in frame_literals.most_common(10):
        print(f"  {count:5}  {name[:60]}")


def hex_rgb(value):
    raw = str(value).lstrip("#")
    if len(raw) == 3:
        raw = "".join(char * 2 for char in raw)
    if len(raw) not in (6, 8):
        return None
    try:
        return tuple(int(raw[index:index + 2], 16) for index in (0, 2, 4))
    except ValueError:
        return None


def luminance(rgb):
    channels = []
    for component in rgb:
        value = component / 255
        channels.append(value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(foreground, background):
    low, high = sorted((luminance(foreground), luminance(background)))
    return (high + 0.05) / (low + 0.05)


class Resolver:
    def __init__(self, doc):
        self.variables = doc.get("variables") or {}

    def themes(self, doc):
        combos = [{}]
        for axis, values in (doc.get("themes") or {}).items():
            combos = [dict(combo, **{axis: value}) for combo in combos for value in values]
        return combos

    def resolve(self, value, theme):
        if not is_var(value):
            return value
        definition = self.variables.get(value[1:])
        if not isinstance(definition, dict):
            return None
        raw = definition.get("value")
        if not isinstance(raw, list):
            return raw
        for entry in raw:
            if all(theme.get(key) == expected for key, expected in (entry.get("theme") or {}).items()):
                return entry.get("value")
        return raw[0].get("value") if raw else None


def numeric_weight(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 700 if str(value).lower() in ("bold", "semibold") else 400


def audit_contrast(doc):
    resolver = Resolver(doc)
    themes = resolver.themes(doc)
    failures = 0
    checked = 0
    print("\n[Text contrast candidates]")
    for node, _, inherited_fill in all_nodes(doc):
        if node.get("type") != "text":
            continue
        checked += 1
        label = node.get("name") or node.get("content") or node.get("id") or "(text)"
        if inherited_fill is None:
            failures += 1
            print(f"  ? {label}: no ancestor background fill")
            continue
        for theme in themes:
            foreground = hex_rgb(resolver.resolve(node.get("fill"), theme))
            background = hex_rgb(resolver.resolve(inherited_fill, theme))
            size = resolver.resolve(node.get("fontSize"), theme)
            weight = numeric_weight(resolver.resolve(node.get("fontWeight"), theme))
            large = isinstance(size, (int, float)) and (size >= 18.66 or (size >= 14 and weight >= 600))
            required = 3.0 if large else 4.5
            theme_name = ", ".join(f"{key}={value}" for key, value in theme.items()) or "default"
            if not foreground or not background:
                failures += 1
                print(f"  ? {label} [{theme_name}]: unresolved color")
                continue
            ratio = contrast_ratio(foreground, background)
            if ratio < required:
                failures += 1
                print(f"  ! {label} [{theme_name}]: {ratio:.2f}:1 < {required:.1f}:1")
    print(f"Checked {checked} text nodes · {failures} candidate failures")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--mode", choices=("structure", "contrast", "all"), default="structure")
    args = parser.parse_args()
    with args.file.open(encoding="utf-8") as handle:
        document = json.load(handle)
    if args.mode in ("structure", "all"):
        audit_structure(document)
    failures = audit_contrast(document) if args.mode in ("contrast", "all") else 0
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
