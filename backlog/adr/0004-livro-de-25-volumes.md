# ADR-0004 — Livro de 25 volumes com contrato de autoria

- **Status:** aceito
- **Data:** 2026-07-29
- **Decisores:** dono do produto
- **Versão do EOS:** 2.1.0 → 3.0.0 (`MAJOR` — renumeração de arquivos e expansão estrutural do livro)

---

## Contexto

Após a v2.1 (15 volumes / 735 regras), a direção do produto pediu o livro completo no layout
`00`–`24`, com profundidade de manual profissional e consistência sob contexto limitado de autoria
(várias sessões / vários agentes).

Já existiam: [`AUTHORING.md`](../../AUTHORING.md) (contrato de autoria), [`SUMARIO.md`](../../SUMARIO.md)
(fronteiras), e a reestruturação de arquivos na raiz. Faltavam 11 volumes novos e o fechamento
editorial (ADR, backlog, anatomia dos volumes herdados da era `volumes/`).

## Problema, como restrição

1. Escrever ~25 volumes sem memória compartilhada produz contradição e reafirmação (`A-001`).
2. Expandir para 25 volumes sem fronteira normativa duplica normas (`ARC-011` no livro).
3. Checklists de 500–1000 itens e um papel "Refatorador" foram recusados antes (`EOS-005`, `EOS-007`)
   e não devem voltar pela porta dos volumes novos.

## Alternativas

### A — Parar em 15 volumes (v2.1)

- **A favor:** menor superfície, já validado.
- **Contra:** lacunas explícitas (API como produto, multi-tenant operacional, observabilidade
  profunda, produto, revisão de PR, design system, métricas de engenharia, portão final) permaneceriam
  só como menções dispersas.

### B — 25 volumes sem AUTHORING/SUMARIO

- **A favor:** entrega rápida de texto.
- **Contra:** inconsistência garantida entre autores; reafirmação de regras; IDs inventados.

### C — 25 volumes + AUTHORING + SUMARIO + verificação mecânica **(escolhida)**

Cada volume novo cita por ID; fronteira no SUMARIO; `build-rules-index` / `check-links` no fechamento
de sessão (`A-021`).

## Decisão

Alternativa **C**. Layout `00`–`24` na raiz; 11 volumes novos escritos; Volume 02 hospeda `ARC`+`SEL`;
Volume 19 existe como **referência** (IA no produto) com banner de estado ligado a `EOS-004`; Volume 20
(Prompt Engineering) existe como doutrina operacional do próprio EOS — o que invalida o "não faremos"
literal de `EOS-006` sem invalidar a tese de que prompt monolítico degrada.

Contagem na aceitação: **25 volumes**, **1391 regras**, links internos verdes.

## Contrapartidas aceitas

- Volumes herdados (00–08, 10–12, 14, 21) ainda carecem da anatomia completa de `AUTHORING.md`
  (Fundamentos, Padrões, Prompt, etc.). Registrado como trabalho ativo — não como "pronto".
- Alvo de "80–200 páginas por volume" não foi meta desta entrega; densidade normativa prevaleceu sobre
  padding (`A-005`).
- `MAJOR` 3.0.0: caminhos `volumes/vol-*` deixam de existir; consumidores do layout antigo quebram.

## Condições de invalidação

- Dois volumes reivindicando a mesma norma sem citação (`A-001` falho em escala).
- Volume com >~90 regras num único domínio sem partição (sinal de fronteira errada).
- Playbooks (`PLB`) divergindo do conteúdo das regras que citam (`EOS-009`).

## Consequências

`AGENTS.md` e `README.md` apontam para 25 volumes. Cadeia de 11 papéis inalterada em contagem; papéis
ganham volumes adicionais (ex.: Backend → 03+15). Próximo incremento editorial: completar anatomia dos
volumes herdados e calibrar limiares (`EOS-002`).
