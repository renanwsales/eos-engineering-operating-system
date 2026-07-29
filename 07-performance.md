# 📔 Volume 7 — Framework de Performance

Prefixo: `PRF` · Regras: PRF-001 a PRF-038 · Papel: [Performance Engineer](agents/06-performance.md)

Camada coberta: **5 (performance)**.

Este volume trata do gargalo **medido de hoje**. As decisões estruturais de crescimento e a contrapressão sob
saturação estão no [Volume 14](14-escalabilidade.md).

**Fronteira.** É deste volume: disciplina de medição; o gargalo de hoje; acesso a dados; cache com
invalidação declarada; custo de renderização; limiares; orçamento de performance.
Não é decisão estrutural de crescimento nem contrapressão (→ [14](14-escalabilidade.md)). Não é
instrumentação, tracing nem dashboards (→ [17](17-observabilidade.md)). Normas profundas de índice e
plano: [05](05-banco-de-dados.md); UI detalhada: [04](04-frontend.md).

---

## Fundamentos

Performance sem medição é cosmética (`PRF-001`, `CON-006`, `CON-013`). O volume existe para impedir
duas falhas caras: otimizar o suspeito em vez do gargalo (`PRF-005`), e instalar cache que troca
latência por dado errado (`PRF-019`, `PRF-020`).

Modelo mental em três passos. **Meça** com método declarado e p95 no volume real (`PRF-002`–
`PRF-004`). **Ordene** a investigação do maior impacto típico — dados antes de algoritmo
(`PRF-007`). **Prove** o ganho com o mesmo método; ruído de medição não é vitória (`PRF-006`).

Escalabilidade (réplicas, sharding, backpressure) é outro volume: aqui o alvo é o gargalo **medido
hoje**, com limiar e proteção automática contra regressão (`PRF-038`).


---

## O portão de entrada do volume

### PRF-001 — Sem medição, não há achado **[IMUTÁVEL]**

Alteração justificada por "isso deve ser mais rápido" é refatoração cosmética e é rejeitada por CON-013.
Suspeita sem medição é `HYPOTHESIS` acompanhada do método que a verificaria.

### PRF-002 — Toda medição declara o método **[OBRIGATÓRIA]**

Ambiente, volume de dados, número de execuções, percentil e ferramenta. Número sem método não é evidência.

### PRF-003 — Use p95, nunca média **[OBRIGATÓRIA]**

A média esconde exatamente os casos que fazem o usuário desistir.

### PRF-004 — Meça no volume real, atual e projetado **[OBRIGATÓRIA]**

`O(n²)` com 10 registros é irrelevante; com 100 mil é indisponibilidade. Medir localmente com dados de teste
e reportar como produção é conclusão inválida.

### PRF-005 — Ataque o gargalo, não o suspeito **[OBRIGATÓRIA]**

Perfile para localizar. Otimizar sem perfilar produz código pior sem ganho, e o ganho aparente costuma ser
ruído de medição.

### PRF-006 — Prove o ganho, ou não houve ganho **[OBRIGATÓRIA]**

Antes e depois pelo mesmo método. **Se o ganho está dentro da variação da medição, não houve ganho** — e a
complexidade adicionada é prejuízo líquido.

---

## Capítulo 7.1 — Ordem de investigação

### PRF-007 — Siga a ordem de maior impacto típico **[OBRIGATÓRIA]**

```
1. Acesso a dados   ← quase sempre aqui
2. Rede e integrações
3. Trabalho repetido
4. Carga útil
5. Renderização
6. Algoritmo e estrutura de dados
```

Investigar na ordem inversa é como se perde tempo otimizando um laço enquanto o endpoint faz 51 consultas.

---

## Capítulo 7.2 — Acesso a dados

Normas completas no [Volume 6](05-banco-de-dados.md). Aqui, o recorte de performance.

### PRF-008 — Conte as consultas por requisição **[OBRIGATÓRIA]**

Com 1 item e com 50. Se o número cresce, é N+1 (DAT-019). É a primeira medição a fazer, sempre, e a mais
barata.

### PRF-009 — Plano de execução verificado antes de afirmar falta de índice **[OBRIGATÓRIA]**
### PRF-010 — Paginação com limite do servidor em toda listagem **[OBRIGATÓRIA]**
### PRF-011 — Agregação no banco, não na aplicação **[RECOMENDADA]**
### PRF-012 — Transação curta para evitar contenção **[RECOMENDADA]**

Sob concorrência, o gargalo frequentemente não é a consulta: é a espera pelo bloqueio.

---

## Capítulo 7.3 — Rede e integrações

### PRF-013 — Chamadas independentes em paralelo **[RECOMENDADA]**

Três chamadas sequenciais de 200 ms são 600 ms; em paralelo, 200 ms.

### PRF-014 — Toda chamada externa tem timeout **[OBRIGATÓRIA]**

Sem timeout, uma dependência lenta esgota o pool de conexões e transforma lentidão alheia em
indisponibilidade própria. `S2`; em caminho crítico, `S1`.

### PRF-015 — Paralelismo com limite **[OBRIGATÓRIA]**

Sem limite, você exaure conexões e derruba a dependência que estava tentando usar.

### PRF-016 — Retry com espera crescente e variação aleatória **[OBRIGATÓRIA]**

Retry imediato em massa amplifica a falha da dependência que já está sofrendo.

### PRF-017 — Conexões reutilizadas **[RECOMENDADA]**

### PRF-018 — Degradação em vez de queda **[RECOMENDADA]**

Falha em recurso secundário (recomendação, avaliação, banner) não impede o fluxo principal. Defina o
comportamento degradado explicitamente.

---

## Capítulo 7.4 — Cache

O capítulo mais perigoso do volume: cache mal projetado transforma um problema de latência em problema de
**correção**, que é mais grave.

### PRF-019 — Cache é decisão, com quatro respostas obrigatórias **[OBRIGATÓRIA]**

Antes de adicionar, declare: **o que** é cacheado · **por quanto tempo** · **como é invalidado** · **o que
acontece se servir dado velho**.

Faltando qualquer uma, o cache é rejeitado.

### PRF-020 — A chave inclui tudo que altera a resposta **[OBRIGATÓRIA]** · `S0`

Usuário, permissão, tenant, idioma, moeda, versão do contrato. **Servir dado de um usuário para outro é
`S0`**, e é a falha de cache mais frequente que existe.

### PRF-021 — Invalidação definida por mutação **[OBRIGATÓRIA]**

Para cada escrita, quais chaves ficaram obsoletas. Cache sem invalidação declarada é dado errado com prazo
indeterminado.

### PRF-022 — Cache não esconde N+1 **[OBRIGATÓRIA]**

Usar cache para mascarar um problema de acesso a dados mantém o defeito e adiciona risco de dado velho.
Corrija a origem.

### PRF-023 — Suba um nível de cache por vez, com medição **[RECOMENDADA]**

```
memória do processo → cache compartilhado → CDN → cache do cliente
```

Cada nível adiciona complexidade de invalidação.

### PRF-024 — Cache de dado sensível é decisão registrada **[OBRIGATÓRIA]**

Onde ele vive, por quanto tempo, e quem pode ler o armazenamento do cache.

### PRF-025 — Prevenir avalanche de recomputação **[RECOMENDADA]**

Expiração simultânea de muitas chaves derruba a origem no momento em que ela é mais necessária. Use variação
no prazo ou recomputação coordenada.

---

## Capítulo 7.5 — Trabalho repetido e carga útil

### PRF-026 — Nenhuma recomputação de valor estável na mesma requisição **[RECOMENDADA]**
### PRF-027 — Resposta sem campos não usados **[RECOMENDADA]**

Também reduz superfície de vazamento (BAK-033).

### PRF-028 — Compressão habilitada nas respostas **[OBRIGATÓRIA]**
### PRF-029 — Nenhuma serialização redundante **[RECOMENDADA]**

---

## Capítulo 7.6 — Renderização e interface

Regras detalhadas em [Volume 4](04-frontend.md), capítulo 4.5.

### PRF-030 — Orçamento de bundle verificado no pipeline **[OBRIGATÓRIA]**
### PRF-031 — Lista longa virtualizada **[OBRIGATÓRIA]**
### PRF-032 — Nenhum trabalho pesado na thread principal **[OBRIGATÓRIA]**
### PRF-033 — Espaço reservado para conteúdo assíncrono **[OBRIGATÓRIA]**

Deslocamento de layout causa erro de clique: é defeito de interação medido por CLS.

### PRF-034 — Percepção de velocidade é tratada **[RECOMENDADA]**

Feedback imediato, esqueleto quando a estrutura é conhecida, atualização otimista onde é seguro (FRT-011).
Percepção é a métrica que o usuário sente.

---

## Capítulo 7.7 — Algoritmo e volume

### PRF-035 — Complexidade adequada ao volume real **[OBRIGATÓRIA]**

Com análise explícita quando não há medição possível.

### PRF-036 — Estrutura de dados adequada ao padrão de acesso **[RECOMENDADA]**

Busca linear repetida onde um índice em memória resolveria é o caso mais comum.

### PRF-037 — Trabalho em volume processado em lotes e retomável **[RECOMENDADA]**

---

## Capítulo 7.8 — Limiares e regressão

### PRF-038 — Limiares declarados e protegidos por verificação automática **[OBRIGATÓRIA]**

| Métrica | Limiar padrão `[perfil]` |
| --- | --- |
| API p95 | < 300 ms |
| Consulta p95 | < 100 ms |
| Consultas por requisição | constante em relação ao resultado |
| LCP | < 2,5 s |
| INP | < 200 ms |
| CLS | < 0,1 |
| Bundle inicial | < 250 KB comprimido |
| **Regressão entre versões** | **> 20% bloqueia entrega** |

Sem verificação automática que falhe na regressão, os limiares são aspiracionais: a degradação entra
gradualmente e ninguém percebe até o usuário reclamar.

---

---

## Padrões reutilizáveis

**Contagem de consultas 1× e 50×.** Primeira medição barata: se cresce com N, é N+1 (`PRF-008`,
`DAT-019`). Corrija a origem antes de cache (`PRF-022`).

**Cartão de cache.** Quatro respostas obrigatórias antes de adicionar: o quê, TTL, invalidação por
mutação, efeito de dado velho (`PRF-019`, `PRF-021`). Chave inclui tenant/usuário/permissão
(`PRF-020`).

**Paralelo com teto.** Chamadas independentes em paralelo; semáforo no paralelismo; timeout em toda
externa (`PRF-013`–`PRF-015`). Retry com jitter (`PRF-016`).

**Um nível de cache por vez.** Processo → compartilhado → CDN → cliente, medindo a cada degrau
(`PRF-023`).

**Registro antes/depois.** Mesmo método, n, ambiente; causa; proteção de regressão (ver registro
obrigatório ao final do volume).

---

## Matrizes de decisão

**Onde investigar primeiro (`PRF-007`)**

| Sintoma | Primeira hipótese | Medição |
| --- | --- | --- |
| Latência sobe com tamanho da página | N+1 / listagem sem limite | Contagem de queries (`PRF-008`) |
| Cauda alta sob carga | Contenção / timeout ausente | p95 + locks / timeouts (`PRF-012`, `PRF-014`) |
| Bom no servidor, ruim na UI | Bundle / thread principal / CLS | Orçamento + perfil (`PRF-030`–`PRF-033`) |
| Pico após deploy de cache | Chave incompleta / invalidação | Auditoria de chave (`PRF-020`) |

**Cache: adicionar ou recusar**

| Condição | Decisão |
| --- | --- |
| Quatro respostas de `PRF-019` incompletas | Recusar |
| N+1 ainda presente | Corrigir dados primeiro (`PRF-022`) |
| Dado sensível | Só com decisão registrada (`PRF-024`) |
| Ganho dentro do ruído | Não houve ganho (`PRF-006`) |

---

## Fluxo de trabalho

1. Declarar método de medição (ambiente, volume, n, percentil, ferramenta) (`PRF-002`).
2. Obter baseline p95 no volume real (`PRF-003`, `PRF-004`).
3. Percorrer a ordem de `PRF-007` até achar o gargalo (`PRF-005`).
4. Corrigir a causa (dados → rede → trabalho repetido → payload → UI → algoritmo).
5. Se cache: cartão completo + invalidação por mutação (`PRF-019`, `PRF-021`).
6. Remedir com o mesmo método; registrar ganho (`PRF-006`).
7. Proteger limiar no pipeline (`PRF-038`); se N+1 corrigido, teste de contagem (`QAT-029`).

Crescimento estrutural e contrapressão: parar e abrir [14](14-escalabilidade.md).

---

## Exemplos de implementação

**Otimizar sem perfilar (`PRF-001`, `PRF-005`)**

```
Ruim — "troquei for por map; deve ficar mais rápido"
Bom  — p95 GET /pedidos 840→120ms (n=200, 10k pedidos, homologação); causa: 1+N itens;
       correção: batch load; teste falha se queries > 3 na página de 50
```

**Chave de cache incompleta (`PRF-020`)**

```ts
// Ruim — S0: serve plano de um tenant a outro
const key = `planos:${planoId}`;

// Bom
const key = `planos:${tenantId}:${userId}:${planoId}:${locale}`;
```

**Cache escondendo N+1 (`PRF-022`)**

```
Ruim — TTL 60s sobre endpoint que faz 51 queries
Bom  — eliminar N+1; só então cachear DTO estável com invalidação na mutação do pedido
```


## Antipadrões

| Antipadrão | Por que é problema |
| --- | --- |
| Otimizar sem perfilar | Complexidade sem ganho |
| Microotimização em código não crítico | Custo de leitura permanente, ganho nulo |
| Cache para esconder N+1 | Mantém o defeito e adiciona risco de dado velho |
| Chave de cache sem tenant ou usuário | `S0` — dado de um usuário para outro |
| Paralelismo sem limite | Exaure conexões e derruba a dependência |
| Medir com 10 registros | Conclusão inválida |
| "Ficou mais rápido" sem número | Rejeitado por PRF-001 |
| Aumentar infraestrutura em vez de corrigir | Custo recorrente para esconder defeito |
| Remover validação para ganhar tempo | Troca correção por latência |
| Memoizar por precaução | Complexidade sem ganho medido |

---

## Registro obrigatório da correção

```
Métrica: latência p95 de GET /pedidos
Antes:   840 ms  (n=200, 10k pedidos, homologação, ferramenta X)
Depois:  120 ms  (mesmo método)
Causa:   N+1 na carga de itens — 1 + N consultas viravam 51 em página de 50
Correção: carregamento em lote único
Risco:   baixo, coberto por teste de contagem de consultas
Proteção contra regressão: teste que falha se a contagem crescer
```

---

## Checklist

- [ ] Achado de performance tem medição com método. (`PRF-001`, `PRF-002`)
- [ ] Métrica em p95 (ou percentil declarado), não média. (`PRF-003`)
- [ ] Volume de dados realista. (`PRF-004`)
- [ ] Gargalo localizado por perfil/ordem, não por suspeita. (`PRF-005`, `PRF-007`)
- [ ] Ganho provado pelo mesmo método. (`PRF-006`)
- [ ] Consultas contadas em 1 e em 50 itens. (`PRF-008`)
- [ ] Listagens com limite do servidor. (`PRF-010`)
- [ ] Chamadas externas com timeout; paralelo com limite.
      (`PRF-014`, `PRF-015`)
- [ ] Cache com quatro respostas + invalidação por mutação.
      (`PRF-019`, `PRF-021`)
- [ ] Chave de cache inclui tenant/usuário/permissão. (`PRF-020`)
- [ ] Cache não mascara N+1. (`PRF-022`)
- [ ] Orçamento de bundle no pipeline. (`PRF-030`)
- [ ] Limiares declarados; regressão >20% bloqueia. (`PRF-038`)
- [ ] Registro obrigatório da correção preenchido.

---

## Prompt do volume

```
ROLE: Performance engineer under EOS Volume 07 (`PRF`). You attack measured bottlenecks only.

MISSION
Find today's bottleneck with declared measurement method, fix the cause in investigation order,
and prove the gain. Never present an unmeasured suspicion as a FINDING.

LOAD
- `AGENTS.md`, `agents/_shared/core-contract.md`, `agents/_shared/output-schemas.md`
- `00-constituicao-da-engenharia.md`, `07-performance.md`, `agents/06-performance.md`
- Cite `05-banco-de-dados.md`, `04-frontend.md` by ID; do not restate them
- Growth/backpressure → escalate to Volume 14; dashboards → Volume 17
- Filled project profile (`[perfil]` thresholds)

MANDATORY SEQUENCE
1. Measurement method first (`PRF-002`). No method → HYPOTHESIS only (`PRF-001`).
2. Baseline p95 at realistic volume (`PRF-003`, `PRF-004`).
3. Investigate in order (`PRF-007`); attack the bottleneck (`PRF-005`).
4. Data access before cache; never hide N+1 (`PRF-008`, `PRF-022`).
5. Cache only with four answers + mutation invalidation + complete key
   (`PRF-019`–`PRF-021`).
6. Re-measure same method; record before/after (`PRF-006`).
7. Enforce thresholds in pipeline (`PRF-038`).

OUTPUT
Use "Verificação obrigatória de saída" and fill "Registro obrigatório da correção" when a fix ships.
Separate MUST-FIX from OPPORTUNITY. Unmeasured "make it faster" is rejected (`CON-013`).
```

---

## Critérios de aceite

Uma correção de performance passa neste volume quando:

1. Baseline e pós-correção usam o mesmo método declarado. (`PRF-002`, `PRF-006`)
2. O gargalo foi o medido, não o suspeito. (`PRF-005`)
3. Se havia N+1, a contagem de queries ficou constante vs tamanho do resultado. (`PRF-008`)
4. Cache novo (se houver) tem cartão completo e chave segura. (`PRF-019`, `PRF-020`)
5. Limiar relevante está protegido no pipeline. (`PRF-038`)
6. Registro obrigatório da correção está preenchido.
7. Nenhuma validação de negócio foi removida "para ganhar tempo" (`CON-001`).

Falha em 1 ou 4 é reprovação: sem prova não há ganho; cache inseguro é `S0`.

---

## Verificação obrigatória de saída

```
## Medição
Método: <ambiente, volume, n, percentil, ferramenta>
Baseline: <métrica = valor>
Pós: <métrica = valor> | Ganho fora do ruído: <sim/não>

## Ordem PRF-007
| Etapa | Investigada? | Evidência | Gargalo? |

## Acesso a dados
Queries (1 item / 50 itens): <n / n> | N+1: <sim/não> | Evidência:

## Rede
| Chamada | Timeout | Limite paralelo | Retry/jitter | Degradação |

## Cache
| Chave | TTL | Invalidação | Dado velho | Sensível? |

## UI / bundle (se aplicável)
Bundle: <KB> | LCP/INP/CLS: <...> | Evidência:

## Limiares
| Métrica | Limiar | Atual | Protegido no pipeline? |

## Registro da correção
<colar bloco do volume>

## Não verificado
| Item | Por quê | Como medir |
```
