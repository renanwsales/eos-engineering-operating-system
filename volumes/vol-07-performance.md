# 📔 Volume 7 — Framework de Performance

Prefixo: `PRF` · Regras: PRF-001 a PRF-038 · Papel: [Performance Engineer](../agents/06-performance.md)

Camada coberta: **5 (performance)**.

Este volume trata do gargalo **medido de hoje**. As decisões estruturais de crescimento e a contrapressão sob
saturação estão no [Volume 14](vol-14-escala-e-multi-inquilino.md).

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

Normas completas no [Volume 6](vol-06-banco-de-dados.md). Aqui, o recorte de performance.

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

Regras detalhadas em [Volume 4](vol-04-frontend.md), capítulo 4.5.

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
