# 06 — Matriz de priorização

Classificação diz o quanto algo é grave. Priorização diz **o que fazer primeiro** quando há
mais trabalho do que capacidade — que é sempre.

---

## Regra zero: severidade domina o score

O score numérico só ordena itens **dentro da mesma faixa de severidade**. Ele nunca faz um
`S2` passar na frente de um `S1`.

```
1º  Todos os S0, em qualquer quantidade
2º  Todos os S1, ordenados por score
3º  MUST-FIX S2, ordenados por score
4º  OPPORTUNITY, ordenados por score
```

Isso evita a distorção clássica de fórmulas de priorização: um item trivial de esforço `XS`
ultrapassando uma falha de segurança de esforço `L` porque o denominador é pequeno.

---

## O score

```
                Impacto × Alcance × Confiança
Prioridade  =  ────────────────────────────────
                     Esforço × Risco
```

### Impacto — o dano se não for corrigido

| Valor | Significado |
| --- | --- |
| 10 | Perda de dado, dinheiro ou exposição de dado pessoal |
| 7 | Fluxo principal quebrado ou inutilizável |
| 4 | Degradação relevante, contorno existe |
| 2 | Incômodo, ou custo de manutenção futuro |
| 1 | Cosmético |

### Alcance — quem é afetado

| Valor | Significado |
| --- | --- |
| 10 | Todos os usuários, ou todo o time em cada mudança |
| 6 | Um segmento grande, ou um fluxo de alto tráfego |
| 3 | Um segmento pequeno, ou fluxo pouco usado |
| 1 | Caso raro, ambiente interno |

### Confiança — de que o problema e a solução são reais

| Valor | Nível |
| --- | --- |
| 1.0 | `HIGH` |
| 0.6 | `MEDIUM` |
| 0.3 | `LOW` |

### Esforço

| Valor | Nível |
| --- | --- |
| 1 | `XS` |
| 2 | `S` |
| 5 | `M` |
| 13 | `L` |
| 34 | `XL` |

### Risco de correção

| Valor | Nível |
| --- | --- |
| 1.0 | `LOW` |
| 1.5 | `MEDIUM` |
| 2.5 | `HIGH` |

### Leitura do resultado

| Score | Interpretação |
| --- | --- |
| ≥ 20 | Faça agora |
| 8 – 20 | Faça nesta rodada |
| 2 – 8 | Backlog priorizado |
| < 2 | Backlog frio; reavaliar só se o contexto mudar |

---

## Exemplos calculados

**Autorização ausente em endpoint de pedido (IDOR)**
Impacto 10 · Alcance 10 · Confiança 1.0 · Esforço 2 (`S`) · Risco 1.0
→ `(10 × 10 × 1.0) / (2 × 1.0) = 50` → faça agora. Sendo `S0`, já estaria no topo de qualquer
forma.

**N+1 na listagem do catálogo, 300 ms extra por requisição**
Impacto 4 · Alcance 6 · Confiança 1.0 · Esforço 2 · Risco 1.0
→ `24 / 2 = 12` → nesta rodada.

**Extrair um serviço de domínio de um controller inflado**
Impacto 2 · Alcance 10 · Confiança 0.6 · Esforço 13 (`L`) · Risco 1.5
→ `12 / 19.5 = 0.6` → backlog frio. Ganha prioridade quando um `S1` obrigar a mexer nessa
área — o momento certo de refatorar é quando outra mudança já paga o custo de contexto.

**Renomear variáveis para o padrão do projeto**
Impacto 1 · Alcance 3 · Confiança 1.0 · Esforço 2 · Risco 1.0
→ `3 / 2 = 1.5` → backlog frio. Nunca justifica um PR próprio.

---

## Desempate

Score empatado, decida na ordem:

1. **Desbloqueia outro trabalho?** O que libera mais coisas vem primeiro.
2. **Segurança ou dados?** Vence.
3. **Está no caminho de uma mudança já em curso?** O contexto já carregado é economia real.
4. **Reduz risco de perda irreversível?** Vence acréscimo de funcionalidade.
5. **Menor esforço.** Só aqui, como último critério.

---

## Modificadores de contexto

| Situação | Efeito |
| --- | --- |
| Módulo será substituído em < 3 meses | Impacto de manutenibilidade cai para 1 |
| Área com incidente nos últimos 30 dias | Impacto × 1.5 |
| Item já postergado 3 vezes | Reavaliar severidade: ou sobe, ou é encerrado como "não faremos" |
| Correção depende de decisão humana pendente | Sai da fila; vira pergunta aberta |
| Prazo externo (auditoria, contrato, regulação) | Trata-se como `S1` até a data |

---

## Orçamento por rodada

Uma rodada de revisão tem capacidade finita. Regra de composição:

```
70% MUST-FIX (S0, S1, e S2 no escopo)
20% redução de risco estrutural (o item de maior score do backlog)
10% ferramental (teste, observabilidade, automação que reduz custo futuro)
```

Se os 70% de `MUST-FIX` consomem toda a capacidade, os outros 30% são **postergados
explicitamente**, não silenciosamente. Se `MUST-FIX` excede 100% da capacidade por duas
rodadas seguidas, isso é o achado: o módulo está em dívida crítica e precisa de decisão de
produto, não de mais revisão.

---

## O que nunca entra na fila

- Item sem consequência nomeada.
- Refatoração sem defeito, métrica ou norma associada (ver o veto cosmético no
  [contrato](../agents/_shared/core-contract.md)).
- `XL` sem ADR aprovado.
- Item com confiança `LOW` — vira investigação, com esforço próprio estimado.
