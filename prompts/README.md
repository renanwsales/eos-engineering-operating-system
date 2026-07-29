# prompts — biblioteca de prompts do EOS

Todos os prompts operacionais do EOS, num só lugar, com a regra que evita a falha mais comum de bibliotecas de
prompt: **duplicação**.

Um prompt aqui nunca reproduz as normas de um volume. Ele diz **como operar** — missão, sequência obrigatória,
formato de saída, condições de parada, e o que não é da sua conta — e carrega as normas por referência
(`A-016`). Prompt que copia regra é uma segunda fonte de verdade que envelhece em silêncio, e a norma copiada
divergirá da original na primeira revisão.

A teoria por trás do formato está no [Volume 20 — Prompt Engineering](../20-prompt-engineering.md).

---

## Prompts de papel

São os prompts principais. Cada um é um papel da cadeia, com contrato herdado e escopo declarado. Ficam em
[`agents/`](../agents/) porque são consumidos por ferramentas que apontam para aquele diretório.

| Prompt | Arquivo | Volumes que carrega |
| --- | --- | --- |
| Orquestrador (Mestre) | [`agents/00-orchestrator.md`](../agents/00-orchestrator.md) | 01, 00 |
| Arquiteto | [`agents/01-architect.md`](../agents/01-architect.md) | 02, 16 |
| Backend | [`agents/02-backend.md`](../agents/02-backend.md) | 03, 15 |
| Frontend | [`agents/03-frontend.md`](../agents/03-frontend.md) | 04, 09 |
| Banco de Dados | [`agents/04-database.md`](../agents/04-database.md) | 05, 14 |
| Segurança | [`agents/05-security.md`](../agents/05-security.md) | 06, 16 |
| Performance | [`agents/06-performance.md`](../agents/06-performance.md) | 07, 14 |
| QA | [`agents/07-qa.md`](../agents/07-qa.md) | 11 |
| DevOps/SRE | [`agents/08-devops-sre.md`](../agents/08-devops-sre.md) | 10, 17 |
| Product/UX | [`agents/09-product-ux.md`](../agents/09-product-ux.md) | 08, 18 |
| Auditor Final | [`agents/10-final-auditor.md`](../agents/10-final-auditor.md) | 12, 13, 24 |

Herdado por todos: [`agents/_shared/core-contract.md`](../agents/_shared/core-contract.md) e
[`agents/_shared/output-schemas.md`](../agents/_shared/output-schemas.md).

---

## Prompts de volume

Cada volume termina com uma seção **Prompt do volume**: a versão canônica do prompt que aplica aquele volume
especificamente. Use quando a tarefa é estreita e um papel inteiro seria excessivo — por exemplo, revisar
apenas os tokens de um componente, sem despachar o Frontend completo.

A versão canônica é a que está no volume. Este diretório indexa; não copia.

---

## O que não existe aqui, e por quê

| Prompt pedido | Decisão | Motivo |
| --- | --- | --- |
| **Refatorador** | Recusado (`EOS-007`) | Um papel cuja missão é refatorar convida exatamente o que `CON-013` proíbe: mudança sem defeito, métrica ou norma vinculada. Refatoração legítima nasce do achado de outro papel, que já a justifica |
| **Code Review** separado do Auditor | Consolidado | O Auditor Final carrega o [Volume 13](../13-revisao-de-codigo.md), que é revisão de PR. Dois prompts para o mesmo escopo divergem |
| **Product Manager** separado do Product/UX | Consolidado | O Product/UX carrega o [Volume 18](../18-produto.md). O papel é um; os volumes são dois |

---

## Como escolher

```
Tarefa estreita, um domínio, escopo claro
  → prompt do volume correspondente

Tarefa de um domínio, mas precisa de julgamento e priorização
  → prompt de papel

Módulo inteiro, várias áreas, precisa de veredito
  → Orquestrador + runbooks/revisao-completa-de-modulo.md

Ferramenta que aceita só um system prompt
  → dist/system-prompt.md (reduzido: mantém processo, omite normas por domínio)
```

---

## Regras que valem para qualquer prompt novo

1. **Em inglês** (`A-015`). Os volumes são em português porque são lidos por pessoas; prompts são em inglês.
2. **Nunca reproduza norma** (`A-016`). Referencie por ID.
3. **Declare a sequência e o formato de saída** (`A-017`). Sem sequência, a análise sai em ordem arbitrária;
   sem formato, o relatório não é comparável com o da semana passada.
4. **Declare o que não é da sua conta.** É o que evita relatório redundante e inflação de escopo.
5. **Versione junto com o volume.** Prompt e volume mudam na mesma entrega, ou divergem.
