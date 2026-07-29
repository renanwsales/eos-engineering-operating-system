#!/usr/bin/env python3
"""Valida links internos, âncoras e referências a IDs de regra em todos os markdown do EOS.

Uso:
    python3 scripts/check-links.py

Falha com código 1 quando encontra:
  - link relativo para arquivo inexistente;
  - âncora que não corresponde a nenhum cabeçalho do arquivo alvo;
  - referência a um ID de regra (ex.: `SEC-004`) que não existe em nenhum volume.
"""

from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules"}

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.*)$")
RULE_DEF = re.compile(r"^### ([A-Z]{3}-\d{3}) — ", re.M)
RULE_REF = re.compile(r"\b(CON|ARC|BAK|FRT|SEC|DAT|PRF|UXI|QAT|OPS|AUD|ORC)-(\d{3})\b")


def slug(text: str) -> str:
    text = re.sub(r"`|\*\*|\*|\[|\]|\([^)]*\)", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def markdown_files() -> list[pathlib.Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in SKIP_DIRS for part in path.parts)
    )


def main() -> int:
    files = markdown_files()
    anchors = {
        path: {slug(m.group(1)) for m in (HEADING.match(line) for line in path.read_text().split("\n")) if m}
        for path in files
    }
    known_rules = {
        rule
        for path in (ROOT / "volumes").glob("vol-*.md")
        for rule in RULE_DEF.findall(path.read_text())
    }

    errors: list[str] = []
    links = anchor_checks = rule_refs = 0

    for path in files:
        text = path.read_text()
        rel = path.relative_to(ROOT)

        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, anchor = target.partition("#")
            links += 1

            if file_part:
                resolved = (path.parent / file_part).resolve()
                if not resolved.exists():
                    errors.append(f"{rel}: alvo inexistente -> {target}")
                    continue
            else:
                resolved = path

            if anchor:
                anchor_checks += 1
                if resolved in anchors and anchor not in anchors[resolved]:
                    errors.append(f"{rel}: âncora inexistente -> {target}")

        for prefix, number in RULE_REF.findall(text):
            rule_refs += 1
            if f"{prefix}-{number}" not in known_rules:
                errors.append(f"{rel}: referência a regra inexistente -> {prefix}-{number}")

    print(f"arquivos: {len(files)} | links: {links} | âncoras: {anchor_checks} | refs de regra: {rule_refs}")

    if errors:
        print(f"\nFALHOU com {len(errors)} problema(s):", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("OK: nenhum link, âncora ou referência de regra quebrada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
