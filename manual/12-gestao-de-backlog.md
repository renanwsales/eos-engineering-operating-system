# 12 — Gestão de backlog

O backlog é o que transforma o projeto de "conjunto de arquivos" em **produto vivo**. Sem ele,
cada revisão recomeça do zero: os mesmos problemas são redescobertos, redocumentados e
esquecidos de novo.

Arquivo canônico: [`backlog/BACKLOG.md`](../backlog/BACKLOG.md) — ou o rastreador de issues do
projeto, se houver. Nunca os dois; duplicidade de fonte é como o backlog morre.

---

## Regra de entrada

**Toda `OPPORTUNITY` encontrada e não corrigida entra no backlog, na mesma sessão em que foi
encontrada.**

Não é opcional e não pode ser postergado para "depois eu registro". O custo de registrar é de
dois minutos; o custo de redescobrir é a revisão inteira novamente.

Também entram:
- `MUST-FIX` que foi postergado por decisão explícita (com quem decidiu).
- Investigações necessárias (`HYPOTHESIS` que exige verificação).
- Lacunas de [DoE](09-definition-of-excellence.md) em módulos críticos.
- Itens de DoD reduzida em correção emergencial de `S0`.
- Dívida deliberada assumida para cumprir prazo.

**Não entram:**
- Ideias sem consequência nomeada.
- Preferências de estilo sem norma associada.
- "Investigar se dá para melhorar X" sem hipótese concreta.

Um backlog cheio de itens vagos é indistinguível de um backlog vazio, porque ninguém consegue
priorizá-lo.

---

## Formato

Use [`templates/entrada-de-backlog.md`](../templates/entrada-de-backlog.md). Campos mínimos:

```
[EOS-042] Regra de frete duplicada entre carrinho e checkout
Severidade: S2 | Confiança: HIGH | Esforço: M | Risco: MEDIUM | Score: 4.8
Evidência: src/cart/shipping.ts:34 e src/checkout/total.ts:91
Consequência se ignorado: divergência de valor entre telas na próxima alteração de frete
Gatilho de promoção: qualquer mudança em regra de frete
Origem: auditoria do módulo de checkout, 2026-07-29
Status: aberto
```

O campo **gatilho de promoção** é o mais importante e o mais esquecido. Ele responde: *o que
faz este item deixar de esperar?* Sem gatilho, o item depende de alguém reler o backlog por
acidente.

Exemplos de gatilho:
- "Qualquer mudança neste arquivo."
- "Quando o volume de pedidos passar de 10 mil/dia."
- "Quando migrarmos para a versão 15 do framework."
- "Na próxima auditoria de segurança."
- "Se o defeito reincidir."

---

## Estados

```
aberto → em análise → priorizado → em execução → concluído
   │                                      │
   ├──────────▶ não faremos ◀─────────────┘
   └──────────▶ obsoleto
```

| Estado | Significado |
| --- | --- |
| `aberto` | Registrado, não avaliado |
| `em análise` | Sendo investigado ou estimado |
| `priorizado` | Com score, na fila de uma rodada |
| `em execução` | Alguém está fazendo |
| `concluído` | Feito, com referência ao commit ou PR |
| `não faremos` | Decisão consciente, **com motivo escrito** |
| `obsoleto` | O código ou o contexto mudou; o item deixou de existir |

`não faremos` é um estado saudável e deve ser usado. Um backlog que só cresce perde utilidade —
ninguém lê uma lista de 400 itens.

---

## Higiene periódica

A cada rodada de revisão, o [orquestrador](../agents/00-orchestrator.md) executa:

1. **Verificar obsolescência.** Item cuja evidência (`path:line`) não existe mais é verificado:
   foi resolvido incidentalmente, ou o código mudou de lugar? Atualize ou encerre.
2. **Reavaliar severidade.** O contexto muda: mais usuários, mais dados, novo requisito. O item
   pode ter subido ou caído.
3. **Aplicar a regra das três postergações.** Item postergado três vezes é um sinal: ou a
   severidade está inflada, ou o valor é real e a prioridade está errada. Decida entre promover
   ou marcar `não faremos`. Nunca postergue uma quarta vez.
4. **Agrupar itens relacionados.** Cinco itens no mesmo módulo frequentemente são um único item
   estrutural com melhor relação custo-benefício quando feitos juntos.
5. **Recalcular scores** dos 10 itens do topo, com os modificadores de contexto da
   [matriz de priorização](06-matriz-de-priorizacao.md).

---

## Composição de cada rodada

Repetindo a regra de orçamento, porque é aqui que o backlog deixa de ser um cemitério:

```
70% MUST-FIX
20% o item de maior score do backlog (redução de risco estrutural)
10% ferramental que reduz custo futuro
```

Os 20% são a garantia de que o backlog **avança**. Sem essa reserva, `MUST-FIX` consome 100% da
capacidade indefinidamente e a dívida cresce até virar `MUST-FIX` ela mesma — normalmente na
forma de um incidente.

---

## Dívida técnica: o registro honesto

Dívida assumida deliberadamente é engenharia legítima, sob três condições:

1. **Registrada** no momento em que é assumida, não depois.
2. **Com custo estimado** — de manter e de pagar.
3. **Com gatilho** que obriga a reavaliação.

```
[EOS-057] Validação de CPF apenas no cliente
Dívida assumida em: 2026-07-29, para cumprir a data do lançamento
Custo de manter: entrada inválida chega ao banco; correção manual estimada em 2h/mês
Custo de pagar: S (4h)
Gatilho: primeiro registro inválido em produção, ou o lançamento concluído
Aceito por: <nome do dono>
```

Dívida sem esses três itens não é dívida — é defeito não registrado. A diferença é que dívida
tem plano e alguém que a assumiu.

---

## O que o backlog não é

- **Não é depósito de ideias.** Ideia sem consequência nomeada não entra.
- **Não é substituto de decisão.** Adiar para o backlog algo que é `S1` é omissão.
- **Não é métrica de produtividade.** Fechar 30 itens `S3` não é melhor do que fechar 1 `S1`.
- **Não é documentação de arquitetura.** Decisão vai para [ADR](../templates/adr.md); o backlog
  registra trabalho pendente.
