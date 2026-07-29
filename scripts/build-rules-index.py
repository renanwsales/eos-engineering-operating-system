#!/usr/bin/env python3
"""Gera RULES-INDEX.md a partir dos volumes e valida a consistência das regras.

Uso:
    python3 scripts/build-rules-index.py          # gera o índice
    python3 scripts/build-rules-index.py --check  # só valida, não escreve (para CI)

Validações (falham com código 1):
  - toda regra tem nível de obrigatoriedade reconhecido;
  - a numeração de cada prefixo é contínua e sem duplicatas;
  - todo volume tem exatamente um prefixo;
  - o cabeçalho do volume declara a faixa de regras correta.
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOLUMES = ROOT / "volumes"
INDEX = ROOT / "RULES-INDEX.md"

RULE = re.compile(
    r"^### ([A-Z]{3})-(\d{3}) — (.+?)"
    r"(?: \*\*\[(IMUTÁVEL|OBRIGATÓRIA|RECOMENDADA)\]\*\*)?"
    r"(?: · (`S\d`.*))?\s*$"
)
CHAPTER = re.compile(r"^## Capítulo [\d.]+ — (.+)$")
RANGE = re.compile(r"Regras: ([A-Z]{3})-(\d{3}) a ([A-Z]{3})-(\d{3})")
SHORT = {"IMUTÁVEL": "IMUT", "OBRIGATÓRIA": "OBRIG", "RECOMENDADA": "RECOM"}


def parse() -> tuple[list[dict], list[dict], list[str]]:
    volumes, rules, errors = [], [], []

    for path in sorted(VOLUMES.glob("vol-*.md")):
        lines = path.read_text().split("\n")
        number = int(re.search(r"vol-(\d+)", path.name).group(1))
        chapter = "-"
        found: list[dict] = []

        for line in lines:
            if match := CHAPTER.match(line):
                chapter = match.group(1)
                continue
            if match := RULE.match(line):
                if match.group(4) is None:
                    errors.append(f"{path.name}: {match.group(1)}-{match.group(2)} sem nível")
                found.append(
                    {
                        "volume": number,
                        "id": f"{match.group(1)}-{match.group(2)}",
                        "prefix": match.group(1),
                        "seq": int(match.group(2)),
                        "title": match.group(3).strip(),
                        "level": match.group(4) or "OBRIGATÓRIA",
                        "severity": (match.group(5) or "").strip(),
                        "chapter": chapter,
                    }
                )

        prefixes = {rule["prefix"] for rule in found}
        if len(prefixes) != 1:
            errors.append(f"{path.name}: esperava 1 prefixo, encontrou {sorted(prefixes)}")

        prefix = prefixes.pop() if len(prefixes) == 1 else "???"
        sequence = sorted(rule["seq"] for rule in found)
        expected = list(range(1, len(sequence) + 1))
        if sequence != expected:
            gaps = sorted(set(expected) - set(sequence))
            dups = sorted(n for n in set(sequence) if sequence.count(n) > 1)
            errors.append(f"{path.name}: numeração de {prefix} — lacunas {gaps}, duplicatas {dups}")

        if declared := RANGE.search(lines[2] if len(lines) > 2 else ""):
            last = f"{prefix}-{max(sequence):03d}" if sequence else "-"
            if declared.group(3) + "-" + declared.group(4) != last:
                errors.append(
                    f"{path.name}: cabeçalho declara até {declared.group(3)}-{declared.group(4)}, "
                    f"mas a última regra é {last}"
                )

        volumes.append(
            {
                "number": number,
                "file": path.name,
                "title": lines[0].lstrip("# ").strip(),
                "prefix": prefix,
                "count": len(found),
            }
        )
        rules.extend(found)

    return volumes, rules, errors


def render(volumes: list[dict], rules: list[dict]) -> str:
    levels = collections.Counter(rule["level"] for rule in rules)
    out: list[str] = []
    add = out.append

    add("# RULES-INDEX — índice de regras do EOS\n")
    add(f"**{len(rules)} regras** em {len(volumes)} volumes. Este arquivo é **gerado** por")
    add("`scripts/build-rules-index.py`; não edite à mão. Se um volume e este índice divergirem,")
    add("**o volume** é a fonte de verdade.\n")
    add("## Como citar uma regra\n")
    add("Sempre pelo ID: `SEC-004`, `CON-013`, `DAT-019`. IDs são **estáveis** — uma regra removida")
    add("deixa o número aposentado, nunca reaproveitado, para que relatórios antigos continuem legíveis.\n")
    add("## Obrigatoriedade\n")
    add("| Nível | Significado | Divergir exige |")
    add("| --- | --- | --- |")
    add("| `[IMUTÁVEL]` | Núcleo do framework | Decisão do dono do produto + ADR. É mudança `MAJOR` do EOS |")
    add("| `[OBRIGATÓRIA]` | Violação é achado, com severidade | ADR registrando a divergência (ARC-037) |")
    add("| `[RECOMENDADA]` | Padrão esperado; exceção é normal | Justificativa no momento, sem ADR |\n")
    add(
        f"Distribuição: **{levels['IMUTÁVEL']} imutáveis** · "
        f"**{levels['OBRIGATÓRIA']} obrigatórias** · **{levels['RECOMENDADA']} recomendadas**.\n"
    )
    add("## Volumes\n")
    add("| Vol | Título | Prefixo | Regras |")
    add("| --- | --- | --- | --- |")
    for volume in volumes:
        short = volume["title"].split("— ", 1)[-1]
        add(f"| {volume['number']:02d} | [{short}](volumes/{volume['file']}) | `{volume['prefix']}` | {volume['count']} |")
    add(f"| | **Total** | | **{len(rules)}** |\n")
    add("---\n")

    for volume in volumes:
        add(f"## {volume['title']}\n")
        add(f"Arquivo: [`volumes/{volume['file']}`](volumes/{volume['file']}) · {volume['count']} regras\n")
        add("| ID | Regra | Nível | Sev. | Capítulo |")
        add("| --- | --- | --- | --- | --- |")
        for rule in (r for r in rules if r["volume"] == volume["number"]):
            add(
                f"| `{rule['id']}` | {rule['title']} | {SHORT[rule['level']]} | "
                f"{rule['severity'] or '—'} | {rule['chapter']} |"
            )
        add("")

    return "\n".join(out) + "\n"


def main() -> int:
    check_only = "--check" in sys.argv
    volumes, rules, errors = parse()

    if errors:
        print("FALHOU:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    content = render(volumes, rules)

    if check_only:
        current = INDEX.read_text() if INDEX.exists() else ""
        if current != content:
            print("FALHOU: RULES-INDEX.md está desatualizado. Rode o script sem --check.", file=sys.stderr)
            return 1
        print(f"OK: {len(rules)} regras, índice em dia.")
        return 0

    INDEX.write_text(content)
    print(f"OK: RULES-INDEX.md gerado com {len(rules)} regras em {len(volumes)} volumes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
