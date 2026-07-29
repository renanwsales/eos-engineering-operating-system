# ADR-`<NNNN>` — `<título: a decisão, não o problema>`

| Campo | Valor |
| --- | --- |
| Status | `proposto` \| `aceito` \| `rejeitado` \| `substituído por ADR-NNNN` \| `obsoleto` |
| Data | `<AAAA-MM-DD>` |
| Decisor | `<nome — quem tem a autoridade>` |
| Consultados | `<papéis ou pessoas>` |
| Faixa de risco | `R1` \| `R2` \| `R3` \| `R4` |
| Reversibilidade | `<degrau 1–8 da escala de reversibilidade>` |

> ADR é obrigatório quando: muda contrato público · escolhe tecnologia ou padrão que outros vão seguir ·
> aceita risco conscientemente · é custoso de reverter (> 1 dia) · rompe deliberadamente uma norma do
> EOS · esforço `XL`.

---

## Contexto

O que é verdade hoje, que forças estão em jogo, e por que a decisão precisa ser tomada **agora**.

Fatos, não opiniões. Inclua números quando existirem: volume, latência, frequência de mudança, custo.

## Problema como restrição

Uma frase, **livre de solução**. Descreve o que precisa ser verdade, não como.

> Exemplo: "Uma operação de cobrança repetida pela rede não pode gerar dois débitos."
> Não: "Precisamos adicionar uma tabela de idempotência."

Se você não consegue enunciar sem nomear tecnologia, o problema ainda não foi entendido.

## Alternativas consideradas

Mínimo de duas, mais a opção zero. Uma alternativa é real quando existe um cenário plausível em que
seria escolhida.

### A — `<nome>`

- Como funciona: `<2–3 linhas>`
- Custo: `<esforço + manutenção contínua>`
- Risco: `<o que pode quebrar, e o dano>`
- Reversibilidade: `<degrau, e custo de desfazer em 3 meses>`
- Carga operacional: `<componente novo para monitorar, escalar, pagar>`
- Aderência: `<combina com a arquitetura atual?>`

### B — `<nome>`

`<mesmos campos>`

### C — Não fazer nada / aceitar o risco

Obrigatória. Frequentemente é a escolha certa.

- O que acontece se não fizermos: `<consequência concreta>`
- Custo de conviver: `<preencher>`
- O que faria isso deixar de ser aceitável: `<preencher>`

### Comparação

| Critério | A | B | C |
| --- | --- | --- | --- |
| Resolve o problema inteiro | | | |
| Custo | | | |
| Risco | | | |
| Reversibilidade | | | |
| Carga operacional | | | |
| Aderência | | | |

Correção é eliminatória: alternativa que não resolve o problema inteiro sai da mesa, salvo se
declarada como mitigação temporária com prazo e item de backlog.

---

## Decisão

Escolhida: **`<A | B | C>`**

### Troca aceita

Declare explicitamente o que você está pagando:

> Exemplo: "Aceito uma tabela adicional e 15% mais código de escrita, em troca de tornar o débito
> duplicado estruturalmente impossível em vez de improvável."

### Condição de invalidação

O que faria esta decisão passar a estar errada. **Sem este campo, ninguém no futuro sabe se a decisão
ainda vale.**

> Exemplo: "Se o volume de escrita passar de ~500/s, o custo do bloqueio superaria o ganho e a
> alternativa A deve ser reavaliada."

---

## Consequências

**Positivas:** `<o que fica melhor, concretamente>`

**Negativas:** `<o que fica pior — se não há nada, a análise está incompleta>`

**Novas obrigações:** `<o que passa a exigir manutenção, monitoramento ou disciplina>`

**Impacto em contratos públicos:** `<nenhum | lista, com plano de versionamento>`

---

## Plano de execução

| Fase | O que | Reversível? |
| --- | --- | --- |
| 1 | `<preencher>` | |
| 2 | `<preencher>` | |

Migração de dados: `<não | sim — plano, lotes, contagem antes/depois, reversa testada>`

Mitigação exigida pela faixa de risco (ver [matriz de risco](../volumes/vol-01-constituicao.md)):

- [ ] `<itens da faixa R2/R3/R4 aplicáveis>`
- [ ] Aprovação humana obtida antes da implementação (obrigatório em `R4`)

## Verificação

Como saberemos que funcionou:

1. `<comando, teste ou métrica>`
2. `<métrica antes → esperada depois>`

## Rollback

`<como desfazer, e quanto tempo leva>`

---

## Notas

Links para achados, propostas, itens de backlog e discussões relevantes.
