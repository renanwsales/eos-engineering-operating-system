#!/usr/bin/env python3
"""Gera RULES-INDEX.md a partir dos volumes e valida a consistência das regras.

Uso:
    python3 scripts/build-rules-index.py          # gera o índice
    python3 scripts/build-rules-index.py --check  # só valida, não escreve (para CI)

Validações (falham com código 1):
  - toda regra tem nível de obrigatoriedade reconhecido;
  - a numeração de cada prefixo é contínua e sem duplicatas no repositório inteiro;
  - cada prefixo vive num único volume;
  - o cabeçalho do volume declara a faixa correta de cada prefixo que hospeda.

Um volume pode hospedar mais de um prefixo (ver AUTHORING.md, A-008); o Volume 02
hospeda `ARC` e `SEL`.
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "RULES-INDEX.md"
VOLUME_FILE = re.compile(r"^(\d{2})-[a-z0-9-]+\.md$")

RULE = re.compile(
    r"^### ([A-Z]{3})-(\d{3}) — (.+?)"
    r"(?: \*\*\[(IMUTÁVEL|OBRIGATÓRIA|RECOMENDADA|REVOGADA)\]\*\*)?"
    r"(?: · (`S\d`.*))?\s*$"
)
CHAPTER = re.compile(r"^## Capítulo [\d.]+ — (.+)$")
RANGE = re.compile(r"([A-Z]{3})-001 a ([A-Z]{3})-(\d{3})")
SHORT = {"IMUTÁVEL": "IMUT", "OBRIGATÓRIA": "OBRIG", "RECOMENDADA": "RECOM", "REVOGADA": "REVOG"}


def volume_files() -> list[pathlib.Path]:
    return sorted(p for p in ROOT.glob("*.md") if VOLUME_FILE.match(p.name))


def parse() -> tuple[list[dict], list[dict], list[str]]:
    volumes: list[dict] = []
    rules: list[dict] = []
    errors: list[str] = []
    prefix_home: dict[str, str] = {}

    for path in volume_files():
        text = path.read_text()
        lines = text.split("\n")
        number = int(VOLUME_FILE.match(path.name).group(1))
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

        if not found:
            errors.append(f"{path.name}: nenhuma regra encontrada")
            continue

        header = "\n".join(lines[:8])
        declared = {m.group(1): int(m.group(3)) for m in RANGE.finditer(header)}
        prefixes = sorted({rule["prefix"] for rule in found})

        for prefix in prefixes:
            if prefix in prefix_home and prefix_home[prefix] != path.name:
                errors.append(
                    f"{prefix} aparece em {prefix_home[prefix]} e em {path.name}; "
                    f"um prefixo vive num único volume"
                )
            prefix_home.setdefault(prefix, path.name)

            sequence = sorted(rule["seq"] for rule in found if rule["prefix"] == prefix)
            expected = list(range(1, len(sequence) + 1))
            if sequence != expected:
                gaps = sorted(set(expected) - set(sequence))
                dups = sorted(n for n in set(sequence) if sequence.count(n) > 1)
                errors.append(f"{path.name}: numeração de {prefix} — lacunas {gaps}, duplicatas {dups}")

            if prefix not in declared:
                errors.append(f"{path.name}: cabeçalho não declara a faixa de {prefix}")
            elif declared[prefix] != max(sequence):
                errors.append(
                    f"{path.name}: cabeçalho declara {prefix} até {declared[prefix]:03d}, "
                    f"mas a última regra é {max(sequence):03d}"
                )

        for prefix in declared:
            if prefix not in prefixes:
                errors.append(f"{path.name}: cabeçalho declara {prefix}, que não tem regras no volume")

        volumes.append(
            {
                "number": number,
                "file": path.name,
                "title": lines[0].lstrip("# ").strip(),
                "prefixes": prefixes,
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
    add("Sumário e fronteiras dos volumes: [`SUMARIO.md`](SUMARIO.md) ·")
    add("contrato de autoria: [`AUTHORING.md`](AUTHORING.md)\n")
    add("## Como citar uma regra\n")
    add("Sempre pelo ID: `SEC-004`, `CON-013`, `DAT-019`. IDs são **estáveis** — uma regra removida")
    add("deixa o número aposentado, nunca reaproveitado, para que relatórios antigos continuem legíveis.\n")
    add("## Obrigatoriedade\n")
    add("| Nível | Significado | Divergir exige |")
    add("| --- | --- | --- |")
    add("| `[IMUTÁVEL]` | Núcleo do framework | Decisão do dono do produto + ADR. É mudança `MAJOR` do EOS |")
    add("| `[OBRIGATÓRIA]` | Violação é achado, com severidade | ADR registrando a divergência (ARC-037) |")
    add("| `[RECOMENDADA]` | Padrão esperado; exceção é normal | Justificativa no momento, sem ADR |")
    add("| `[REVOGADA]` | Não vale mais; o número fica aposentado | — |\n")
    add(
        f"Distribuição: **{levels['IMUTÁVEL']} imutáveis** · "
        f"**{levels['OBRIGATÓRIA']} obrigatórias** · **{levels['RECOMENDADA']} recomendadas**"
        + (f" · **{levels['REVOGADA']} revogadas**" if levels["REVOGADA"] else "")
        + ".\n"
    )
    add("## Volumes\n")
    add("| Vol | Título | Prefixo | Regras |")
    add("| --- | --- | --- | --- |")
    for volume in volumes:
        short = volume["title"].split("— ", 1)[-1]
        prefixes = " ".join(f"`{p}`" for p in volume["prefixes"])
        add(f"| {volume['number']:02d} | [{short}]({volume['file']}) | {prefixes} | {volume['count']} |")
    add(f"| | **Total** | | **{len(rules)}** |\n")
    add("---\n")

    for volume in volumes:
        add(f"## {volume['title']}\n")
        add(f"Arquivo: [`{volume['file']}`]({volume['file']}) · {volume['count']} regras\n")
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
