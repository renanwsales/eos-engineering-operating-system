#!/usr/bin/env python3
"""Garante que passos PLB citam normas de domínio por ID (EOS-009 / A-001).

Playbooks ordenam trabalho; não são segunda fonte de verdade. Cada regra `PLB-***`
deve citar ao menos um ID de outro prefixo (SEC, DAT, CON, …). A existência desses
IDs continua a cargo de `check-links.py`.

Uso:
    python3 scripts/check-playbook-refs.py
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLAYBOOK = ROOT / "21-playbooks.md"
RULE_HEAD = re.compile(r"^### (PLB-\d{3}) — ", re.M)
RULE_REF = re.compile(r"\b([A-Z]{3})-(\d{3})\b")


def main() -> int:
    text = PLAYBOOK.read_text()
    parts = re.split(r"(?=^### PLB-\d{3} — )", text, flags=re.M)
    errors: list[str] = []
    checked = 0

    for part in parts:
        head = RULE_HEAD.match(part)
        if not head:
            continue
        rid = head.group(1)
        body = part[head.end() :]
        refs = {f"{p}-{n}" for p, n in RULE_REF.findall(body)}
        foreign = sorted(r for r in refs if not r.startswith("PLB-"))
        checked += 1
        if not foreign:
            errors.append(
                f"{rid}: passo sem citação a regra de domínio (não-PLB). "
                "Referencie por ID; não reafirme a norma (A-001 / EOS-009)."
            )

    print(f"playbook: {checked} regras PLB verificadas")
    if errors:
        print(f"\nFALHOU com {len(errors)} problema(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("OK: todo passo PLB cita ao menos uma norma de domínio por ID.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
