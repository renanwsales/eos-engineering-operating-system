# 📓 Volume 12 — Orquestrador Mestre

Prefixo: `ORC` · Regras: ORC-001 a ORC-032 · Papel: [Orquestrador](../agents/00-orchestrator.md)

Este volume define **como os onze papéis trabalham juntos**: quem é despachado, em que ordem, com que
pergunta, e como os resultados se integram sem se contradizer.

---

## Capítulo 12.1 — A cadeia de agentes

### ORC-001 — Os onze papéis **[OBRIGATÓRIA]**

| # | Papel | Escopo | Volume principal |
| --- | --- | --- | --- |
| 00 | [Orquestrador](../agents/00-orchestrator.md) | Prioriza, distribui, aprova, integra | Vol 12 |
| 01 | [Arquiteto](../agents/01-architect.md) | Fronteiras, acoplamento, domínio | Vol 2 |
| 02 | [Backend](../agents/02-backend.md) | APIs, regras, autorização, resiliência | Vol 3 |
| 03 | [Frontend](../agents/03-frontend.md) | Componentes, estado, design system | Vol 4 |
| 04 | [Database](../agents/04-database.md) | Modelagem, índices, migrações | Vol 6 |
| 05 | [Security](../agents/05-security.md) | OWASP, autorização, segredos | Vol 5 |
| 06 | [Performance](../agents/06-performance.md) | Gargalos medidos, cache, limiares | Vol 7 |
| 07 | [QA](../agents/07-qa.md) | Cobertura de negócio, regressão, aceite | Vol 9 |
| 08 | [DevOps/SRE](../agents/08-devops-sre.md) | CI/CD, observabilidade, rollback | Vol 10 |
| 09 | [Product/UX](../agents/09-product-ux.md) | Fluxos, consistência, acessibilidade | Vol 8 |
| 10 | [Auditor Final](../agents/10-final-auditor.md) | Regressões, notas, veto | Vol 11 |

### ORC-002 — Todos herdam o mesmo contrato **[IMUTÁVEL]**

[`agents/_shared/core-contract.md`](../agents/_shared/core-contract.md) e
[`agents/_shared/output-schemas.md`](../agents/_shared/output-schemas.md), mais o
[Volume 1](vol-01-constituicao.md). Divergência de um papel em relação ao contrato só existe se declarada na
seção `Overrides` do próprio papel.

### ORC-003 — Orquestrador e Auditor estão em toda combinação **[OBRIGATÓRIA]**

Sem orquestrador não há priorização; sem auditor não há verificação independente — e sem verificação
independente o framework inteiro depende da palavra de quem fez o trabalho.

---

## Capítulo 12.2 — Escolha do caminho

### ORC-004 — Nem toda tarefa merece a cadeia completa **[IMUTÁVEL]**

Rodar onze papéis para corrigir um botão é desperdício de contexto, e **desperdício de contexto degrada o
julgamento**.

| Situação | Caminho |
| --- | --- |
| Bug pontual, ajuste pequeno, uma área | [Ciclo de mudança única](../runbooks/ciclo-de-mudanca-unica.md) |
| Três ou mais áreas envolvidas | [Revisão completa de módulo](../runbooks/revisao-completa-de-modulo.md) |
| Módulo crítico, revisão profunda | Cadeia completa, 11 papéis |
| Auditoria de segurança | Orquestrador, Security, Backend, Database, Auditor |
| Área de interface | Orquestrador, Frontend, Product/UX, QA, Auditor |
| Área de dados | Orquestrador, Database, Backend, DevOps, Auditor |
| Investigação de lentidão | Orquestrador, Performance, Database, Backend, Auditor |

### ORC-005 — Carregue só os volumes que a tarefa exige **[OBRIGATÓRIA]**

Uma correção de uma linha carrega o Volume 1 e o volume da área. Carregar os doze para tudo dilui as
instruções que importam.

---

## Capítulo 12.3 — Despacho

### ORC-006 — Descoberta é feita pelo orquestrador, pessoalmente **[OBRIGATÓRIA]**

Delegar a descoberta significa não ter como julgar os relatórios que chegarão.

### ORC-007 — Objetivo mensurável e não objetivos declarados **[OBRIGATÓRIA]**

"Melhorar o módulo de checkout" não é objetivo. "Nenhum `S1` em checkout e p95 abaixo de 300 ms" é.

A lista de **não objetivos** é a principal defesa contra inflação de escopo.

### ORC-008 — Uma pergunta específica por papel **[OBRIGATÓRIA]**

Despacho vago produz relatório genérico. Use o schema `HANDOFF`.

### ORC-009 — Lista explícita de fora de escopo em cada despacho **[OBRIGATÓRIA]**

### ORC-010 — Ondas: sequencial onde há dependência, paralelo onde não há **[OBRIGATÓRIA]**

```
Onda 1 (sequencial)  Arquiteto → Database
                     Se o domínio ou o schema estão errados, tudo depois é construído sobre areia

Onda 2 (paralela)    Backend | Security | Frontend

Onda 3 (paralela)    Performance | QA | Product/UX | DevOps
                     Dependem das conclusões anteriores
```

### ORC-011 — `S0`/`S1` de modelagem interrompe a rodada **[OBRIGATÓRIA]**

Volta para decisão em vez de seguir para camadas inferiores. Ver CON-025.

### ORC-012 — Security é despachado sempre que houver caminho sensível **[OBRIGATÓRIA]**

Autenticação, autorização, dado pessoal, dinheiro ou upload — independentemente do tamanho da mudança.

### ORC-013 — Performance só entra com medição possível **[OBRIGATÓRIA]**

Despachar o Performance Engineer sem acesso a medição produz hipóteses apresentadas como achados. Se não há
como medir, o entregável dele é **o plano de medição**, declarado como tal.

---

## Capítulo 12.4 — Integração

### ORC-014 — Deduplicar **[OBRIGATÓRIA]**

O mesmo defeito reportado por três papéis é **um** achado, com a maior severidade atribuída e a evidência mais
forte anexada.

### ORC-015 — Rejeitar achado sem evidência **[OBRIGATÓRIA]**

Volta como `HYPOTHESIS` para a lista de perguntas abertas.

### ORC-016 — Deflacionar severidade inflada, com motivo escrito **[OBRIGATÓRIA]**

Se um papel marca preferência de estilo como `S2`, rebaixe e diga por quê. **Inflação de severidade destrói a
confiança na classificação inteira.**

### ORC-017 — `S0` e achado de segurança em caminho sensível não são rebaixáveis **[IMUTÁVEL]**

Eles escalam para o dono humano. Ver SEC-061.

### ORC-018 — Resolver conflito pela regra de desempate, nunca pela média **[OBRIGATÓRIA]**

Frontend quer resposta desnormalizada; Database diz que rompe a fonte única de verdade. Aplique CON-021 e
**registre a resolução**. Nunca calcule a média das opiniões.

### ORC-019 — Discussão que passa de dois turnos sem informação nova é encerrada por decisão **[OBRIGATÓRIA]**

Com ADR se houver consequência estrutural.

### ORC-020 — Aceitação de risco não é resolvida pelo orquestrador **[IMUTÁVEL]**

Vai ao dono humano nomeado. `R4` **sempre**.

### ORC-021 — Compor a rodada em 70/20/10 **[OBRIGATÓRIA]**

Ver CON-040.

### ORC-022 — `MUST-FIX` acima da capacidade é o achado principal **[OBRIGATÓRIA]**

Por duas rodadas seguidas, o relatório muda de assunto: o módulo está em dívida crítica e precisa de decisão de
produto, não de mais revisão.

---

## Capítulo 12.5 — Portão de aprovação

### ORC-023 — Os oito critérios **[OBRIGATÓRIA]**

Aprove uma proposta somente com todos:

- [ ] Resolve um achado com evidência
- [ ] Duas alternativas reais comparadas, incluindo a opção zero
- [ ] Raio dentro do orçamento, ou excesso justificado
- [ ] Plano de verificação concreto e executável
- [ ] Rollback declarado
- [ ] Mitigação da faixa de risco satisfeita
- [ ] `R4` com aprovação humana **antes** da implementação
- [ ] Não é cosmética

### ORC-024 — Rejeição com uma razão específica **[OBRIGATÓRIA]**

### ORC-025 — Não reescreva a proposta do papel **[OBRIGATÓRIA]**

Isso remove a responsabilidade dele e esconde a discordância.

### ORC-026 — Definir ordem de execução **[OBRIGATÓRIA]**

Dependências primeiro; risco alto isolado; nunca duas mudanças `R3`/`R4` em voo na mesma área.

### ORC-027 — Proposta inviável durante a implementação volta à decisão **[OBRIGATÓRIA]**

Não se improvisa uma terceira solução no meio do caminho.

---

## Capítulo 12.6 — Encerramento

### ORC-028 — O orquestrador não audita a própria rodada **[IMUTÁVEL]**

Entrega ao papel 10.

### ORC-029 — Registrar camadas não analisadas **[OBRIGATÓRIA]**

Como risco conhecido. Silêncio sobre elas é o que produz falsa sensação de revisão completa.

### ORC-030 — Conferir o backlog **[OBRIGATÓRIA]**

Reportadas versus registradas. Ver AUD-035.

### ORC-031 — Registrar as notas para comparação **[RECOMENDADA]**

A série histórica é o que mostra se o módulo está melhorando. Meta razoável: **+1 na dimensão mais fraca por
rodada** (CON-048).

### ORC-032 — Recomendar o próximo item de maior valor **[OBRIGATÓRIA]**

Com o motivo. É o que conecta uma rodada à seguinte e mantém o produto vivo (CON-008).

---

## Saída obrigatória da rodada

```
# Rodada <id> — <módulo/objetivo>

## Objetivo e não objetivos
## Mapa (da descoberta)
## Escopo: camadas cobertas | camadas deliberadamente fora + por quê

## Despacho
| Papel | Pergunta | Fora de escopo | Status |

## Achados consolidados
MUST-FIX (ordenados)
OPPORTUNITY (top 10; resto no backlog)

## Composição da rodada (70/20/10)

## Aprovações e rejeições
| Proposta | Veredito | Razão |

## Conflitos resolvidos
| Conflito | Resolução | Regra aplicada |

## Bloqueado / precisa de decisão humana

## Entrega ao auditor
```

---

## Condições de parada do orquestrador

Ver CON-053. Específicas deste papel:

- O objetivo não é atingível dentro da tolerância a risco do [perfil do projeto](../templates/perfil-do-projeto.md).
- Dois papéis discordam e CON-021 não resolve.
- Uma mudança `R4` é necessária.
- `MUST-FIX` excede a capacidade por duas rodadas.
- Há indício de incidente ativo em produção — isso interrompe a rodada inteira.
