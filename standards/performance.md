# Norma — Performance

Regra que governa esta norma: **sem medição, não há trabalho de performance.** Uma alteração
justificada por "isso deve ser mais rápido" é refatoração cosmética e é rejeitada pelo veto do
[contrato](../agents/_shared/core-contract.md).

Limiares em [10 — Métricas de qualidade](../manual/10-metricas-de-qualidade.md).

---

## Método

### F1. Meça antes de mudar **[OBRIGATÓRIA]**

Toda medição declara: ambiente, volume de dados, número de execuções, percentil e ferramenta. Um
número sem método não é evidência.

Use p95, não média. A média esconde exatamente os casos que fazem o usuário desistir.

### F2. Ataque o gargalo, não o suspeito **[OBRIGATÓRIA]**

Meça para localizar. Otimizar sem perfilar produz código pior sem ganho — e o ganho aparente é
tipicamente ruído de medição.

### F3. Volume real, não volume de teste **[OBRIGATÓRIA]**

`O(n²)` com 10 registros é irrelevante; com 100 mil é indisponibilidade. Sempre avalie sobre o
volume atual **e** o projetado.

### F4. Prove o ganho **[OBRIGATÓRIA]**

Reporte antes e depois pelo mesmo método. Se o ganho está dentro da variação da medição, não houve
ganho — e a complexidade adicionada é prejuízo líquido.

---

## Ordem de investigação

Siga esta ordem. Ela reflete onde o tempo realmente está gasto na esmagadora maioria dos casos.

### 1. Acesso a dados — quase sempre aqui

- N+1: número de consultas cresce com o tamanho do resultado.
- Consulta sem índice: verifique o plano de execução.
- Ausência de paginação.
- `SELECT *` em tabela larga.
- Consulta dentro de laço.
- Agregação em aplicação que o banco faria melhor.
- Transação longa causando contenção.

### 2. Rede e integrações

- Chamadas sequenciais que poderiam ser paralelas.
- Ausência de timeout: uma dependência lenta vira indisponibilidade própria.
- Chamada repetida para dado estável, sem cache.
- Carga útil maior que o necessário.
- Ausência de conexão reutilizada.

### 3. Trabalho repetido

- Recomputação de valor estável na mesma requisição.
- Cache ausente onde o dado é caro e estável.
- Cache mal invalidado — pior que ausência de cache, porque serve dado errado.
- Serialização e desserialização redundantes.

### 4. Carga útil

- Campos não usados na resposta.
- Imagem sem otimização: formato moderno, dimensão adequada, compressão, carregamento tardio.
- Ausência de compressão na resposta.
- Bundle inflado: dependência grande para uso pequeno, ausência de divisão de código.

### 5. Renderização e interface

- Re-render desnecessário por identidade instável de referência.
- Lista longa sem virtualização.
- Trabalho pesado na thread principal, bloqueando interação.
- Layout instável durante o carregamento.
- Animação em propriedade que força recálculo de layout.
- Fonte bloqueando a primeira pintura.

### 6. Algoritmo e estrutura de dados

- Complexidade inadequada ao volume.
- Busca linear repetida onde um índice em memória resolveria.
- Estrutura errada para o padrão de acesso.

---

## Cache

### F5. Cache é decisão, não otimização automática **[OBRIGATÓRIA]**

Antes de adicionar cache, declare: **o que** é cacheado, **por quanto tempo**, **como é
invalidado**, e **o que acontece se servir dado velho**.

Cache mal projetado transforma um problema de latência num problema de correção — e problema de
correção é mais grave.

### F6. Nunca cacheie por chave insuficiente **[OBRIGATÓRIA]**

Cache de resposta que depende de usuário, permissão, tenant, idioma ou moeda precisa incluir isso
na chave. **Servir dado de um usuário para outro é `S0`** e é a falha de cache mais frequente.

### F7. Cache mais próximo do consumidor primeiro **[RECOMENDADA]**

```
memória do processo  →  cache compartilhado  →  CDN  →  cache do cliente
```

Cada nível adiciona complexidade de invalidação. Suba um nível de cada vez, com medição.

---

## Concorrência e resiliência

### F8. Toda chamada externa tem timeout **[OBRIGATÓRIA]**

Sem timeout, uma dependência lenta esgota o pool de conexões e derruba tudo. Ausência é `S2`, e
`S1` em caminho crítico.

### F9. Retry com espera crescente e idempotência **[OBRIGATÓRIA]**

Retry imediato em massa amplifica a falha da dependência que já está sofrendo. Use espera
crescente com variação aleatória, limite de tentativas, e só em operação idempotente.

### F10. Degradação em vez de queda **[RECOMENDADA]**

Falha em recurso secundário (recomendação, avaliação, banner) não deve impedir o fluxo principal.
Defina o comportamento degradado explicitamente.

---

## Frontend

### F11. Orçamento de bundle declarado **[OBRIGATÓRIA]**

Limite declarado no [perfil do projeto](../templates/perfil-do-projeto.md) e verificado no
pipeline. Sem verificação automática, o bundle cresce monotonicamente — nunca diminui por acaso.

### F12. Dependência é decisão de performance **[OBRIGATÓRIA]**

Antes de adicionar biblioteca: qual o custo em bytes, e o que ela resolve que 30 linhas não
resolvem? Biblioteca inteira para uma função é `S2`.

### F13. Carregue o que é necessário agora **[RECOMENDADA]**

Divisão por rota, carregamento tardio do que está fora da tela, priorização do conteúdo do caminho
crítico.

### F14. Reserve espaço para conteúdo assíncrono **[OBRIGATÓRIA]**

Conteúdo que chega depois e empurra o layout causa erro de clique do usuário. Não é estética: é
defeito de interação.

---

## Antipadrões

| Antipadrão | Por que é problema |
| --- | --- |
| Otimizar sem perfilar | Complexidade sem ganho |
| Microotimização em código não crítico | Custo de leitura permanente, ganho nulo |
| Cache para esconder N+1 | O problema continua, agora com risco de dado velho |
| Paralelismo sem limite | Exaure conexões e derruba a dependência |
| Medir em máquina local com 10 registros | Conclusão inválida |
| "Ficou mais rápido" sem número | Rejeitado |
| Aumentar recurso de infraestrutura em vez de corrigir | Custo recorrente para esconder defeito |
| Remover validação para ganhar tempo | Troca correção por latência |

---

## Registro obrigatório

Toda mudança de performance entra no `CHANGE REPORT` assim:

```
Métrica: latência p95 de GET /pedidos
Antes:   840 ms  (n=200, 10k pedidos, ambiente de homologação)
Depois:  120 ms  (mesmo método)
Causa:   N+1 na carga de itens — 1 + N consultas viravam 51 em uma página de 50
Correção: carregamento em lote único
Risco:   baixo, coberto por teste de contagem de consultas
```
