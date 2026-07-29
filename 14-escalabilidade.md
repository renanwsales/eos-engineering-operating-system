# 📒 Volume 14 — Escala e Multi-Inquilino

Prefixo: `ESC` · Regras: ESC-001 a ESC-042 · Papéis:
[Database](agents/04-database.md), [Performance](agents/06-performance.md),
[DevOps/SRE](agents/08-devops-sre.md)

O [Volume 6](05-banco-de-dados.md) trata de integridade e consulta correta. O
[Volume 7](07-performance.md) trata do gargalo medido de hoje. Este volume trata das decisões
**estruturais** de crescimento — as que são caras de reverter — e do isolamento entre inquilinos, que é
simultaneamente decisão de escala e de segurança.

**Fronteira.** É deste volume: ordem de intervenção (`ESC-002`); normalizar vs desnormalizar; réplicas
de leitura; particionamento e sharding; estado que impede escala horizontal; limites de recurso,
contrapressão, descarte de carga e disjuntor; capacidade conhecida por teste. Também hospeda o
**núcleo** de multi-inquilino: `ESC-036`–`ESC-042` (modelo de isolamento, mudança como `R4`, filtro
no ponto mais interno, inquilino do contexto autenticado, chave de cache/busca com inquilino, cotas,
operações por inquilino). Essas regras permanecem aqui — não foram movidas.

**Não é deste volume:** o gargalo pontual medido hoje (→ [07](07-performance.md)). Integridade
declarativa e migração como disciplina de schema (→ [05](05-banco-de-dados.md)). Instrumentação e
SLO (→ [17](17-observabilidade.md)). **Isolamento de inquilino em profundidade** — identidade e
hierarquia, provisionamento, customização, impersonação, faturamento, inquilino grande, inventário
de vazamento operacional — (→ [16](16-multi-tenant.md) `MTN`, que **cita** `ESC-036`–`ESC-042` e
aprofunda sem reafirmá-las).

---

## Fundamentos

Escala sem número é ambição disfarçada de engenharia (`ESC-001`). Toda decisão deste volume exige
volume atual medido, taxa de crescimento observada e o ponto em que o mecanismo atual quebra. Sem
os três, a proposta é hipótese cara.

A ordem de intervenção (`ESC-002`) existe porque o erro clássico — shardar o N+1, colocar réplica
antes de índice, desnormalizar antes de medir — troca um defeito barato por complexidade permanente.
Corrigir o caminho quente e a consulta errada vem antes de mudar a topologia. Infraestrutura não é
correção (`ESC-003`): se o código multiplica trabalho por requisição, mais máquinas multiplicam a
conta.

Multi-inquilino neste volume é o **núcleo citável** (`ESC-036`–`ESC-042`): o que todo sistema SaaS
precisa acertar no primeiro dia. O Volume 16 trata o mesmo tema como produto e operação — sem
duplicar essas regras.

---

## Capítulo 14.1 — A disciplina de escalar

### ESC-001 — Escala é sempre resposta a um número, nunca a uma ambição **[IMUTÁVEL]**

Nenhuma decisão deste volume é legítima sem: volume atual medido, taxa de crescimento observada, e o ponto em
que o mecanismo atual quebra.

```
Ruim:  "vamos precisar de sharding para suportar milhões de usuários"
Bom:   "a tabela de eventos tem 180M linhas, cresce 8M/mês, e a consulta p95 passou
        de 40 ms para 210 ms nos últimos 90 dias. O índice já não cabe em memória."
```

Sem os três números, o entregável é o **plano de medição**, não a proposta. Ver `PRF-001`.

### ESC-002 — A ordem de intervenção é fixa **[OBRIGATÓRIA]**

```
1. Corrigir o defeito       ← N+1, consulta sem índice, falta de limite
2. Cachear com invalidação declarada
3. Escalar verticalmente     ← mais barato do que qualquer mudança estrutural
4. Escalar horizontalmente o que é sem estado
5. Separar leitura de escrita (réplicas)
6. Reduzir o conjunto de dados quente (arquivamento, retenção)
7. Particionar
8. Fragmentar (sharding)     ← último recurso, e quase sempre evitável
```

Pular para o degrau 7 ou 8 com um defeito no degrau 1 é o erro mais caro que este volume previne. Um N+1
corrigido rende mais do que qualquer sharding, e custa três ordens de magnitude menos.

### ESC-003 — Aumentar infraestrutura não é correção **[OBRIGATÓRIA]**

É mitigação com custo recorrente. Legítima para ganhar tempo, desde que declarada como tal, com o defeito
nomeado e um item de backlog. Ver `PRF-001`.

### ESC-004 — Toda decisão estrutural declara a condição de invalidação **[OBRIGATÓRIA]**

Particionamento e sharding são praticamente irreversíveis em produção. `CON-033` e `CON-041`: são `R4` por
definição.

---

## Capítulo 14.2 — Normalizar e desnormalizar

### ESC-005 — Normalize por padrão **[OBRIGATÓRIA]**

Uma fonte de verdade por fato. É `ARC-011` no schema: dois lugares guardando o mesmo dado divergem, e a
divergência é o defeito.

### ESC-006 — Desnormalizar é decisão com quatro respostas obrigatórias **[OBRIGATÓRIA]**

O que é duplicado · **quem** atualiza a cópia · **quando** · o que acontece enquanto ela está velha.

Faltando qualquer uma, a desnormalização é rejeitada. É a mesma exigência de `PRF-019` para cache — porque
uma coluna desnormalizada **é** um cache, com a diferença perigosa de parecer um dado.

### ESC-007 — Desnormalização exige detecção de divergência **[OBRIGATÓRIA]**

Uma verificação periódica que compara a cópia com a origem e alerta. Sem ela, a divergência é descoberta pelo
cliente, meses depois, sem forma de saber quando começou.

### ESC-008 — Dado histórico é cópia legítima, não desnormalização **[RECOMENDADA]**

O preço registrado no item do pedido não é cópia do preço do produto: é o preço **naquele momento**, e é fato
próprio. Confundir os dois produz o bug de "o histórico mudou quando o catálogo foi atualizado".

### ESC-009 — Contador agregado precisa de estratégia de concorrência **[OBRIGATÓRIA]**

Total, saldo e contagem mantidos de forma incremental estão sujeitos a `DAT-027`. Incremento sem proteção sob
concorrência perde atualizações silenciosamente — o pior tipo de erro em valor agregado, porque nada falha.

### ESC-010 — Visão materializada declara a janela de obsolescência **[RECOMENDADA]**

E a interface a respeita quando for visível ao usuário (`ARC-031`).

---

## Capítulo 14.3 — Réplicas de leitura

### ESC-011 — Réplica introduz atraso, e o atraso é visível **[OBRIGATÓRIA]**

O usuário salva, é redirecionado, a leitura vai à réplica que ainda não recebeu a escrita, e ele vê o valor
antigo. Conclui que a ação falhou e repete — produzindo o efeito duplicado que `UXI-007` tenta evitar.

**Mitigação obrigatória:** leitura imediatamente após escrita, no mesmo fluxo do usuário, vai à primária.

### ESC-012 — Classifique cada leitura por tolerância a atraso **[OBRIGATÓRIA]**

```
| Leitura | Tolera atraso? | Destino | Justificativa |
| Saldo antes de debitar | não | primária | decisão de negócio sobre o valor |
| Detalhe do pedido após salvar | não | primária | leitura pós-escrita do mesmo usuário |
| Listagem de catálogo | sim, segundos | réplica | |
| Relatório e exportação | sim, minutos | réplica | |
```

Enviar leitura que decide regra de negócio para réplica é `S1`: a decisão é tomada sobre dado que já mudou.

### ESC-013 — Atraso de replicação é monitorado com alerta **[OBRIGATÓRIA]**

Réplica muito atrasada serve dado arbitrariamente velho, sem nenhum erro. Falha silenciosa, portanto exige
detecção (`OPS-022`).

### ESC-014 — Réplica não é backup **[OBRIGATÓRIA]**

Replicação propaga a exclusão acidental em segundos. Ver `OPS-042`.

### ESC-015 — Roteamento de leitura é explícito, nunca implícito **[RECOMENDADA]**

Configuração global que manda toda leitura à réplica quebra as leituras de `ESC-012` sem aviso.

---

## Capítulo 14.4 — Particionamento e sharding

### ESC-016 — Particione quando o problema é o conjunto quente, não o total **[RECOMENDADA]**

Particionamento por tempo ajuda quando as consultas recentes dominam e o histórico pode ficar frio. Não
ajuda quando toda consulta varre todas as partições — nesse caso, custa e não rende.

### ESC-017 — A chave de partição precisa aparecer nas consultas **[OBRIGATÓRIA]**

Se as consultas não filtram pela chave, o banco varre todas as partições e o particionamento piora o
desempenho. Verifique o plano de execução (`DAT-016`) antes e depois.

### ESC-018 — Retenção e arquivamento antes de particionar **[RECOMENDADA]**

Frequentemente o problema não é o volume: é guardar para sempre o que ninguém consulta. Ver `DAT-039` e
`SEC-055`. Retenção é mais barata, reduz exposição em caso de vazamento, e não é irreversível.

### ESC-019 — Sharding é o último recurso, e exige as cinco respostas **[OBRIGATÓRIA]**

Qual a chave de fragmentação · o que acontece com consulta que atravessa fragmentos · como se garante
unicidade global · como se rebalanceia · como se faz transação entre fragmentos (normalmente: não se faz).

Sem as cinco, a proposta é rejeitada.

### ESC-020 — Chave de fragmentação errada é praticamente irreversível **[IMUTÁVEL]**

Rebalancear em produção é migração de dados de todo o conjunto — `R4`, com janela e risco de indisponibilidade.
Esta é a decisão de arquitetura de dados mais difícil de desfazer que existe.

Em SaaS multi-inquilino, a chave costuma ser o inquilino, o que resolve a maior parte das consultas
atravessadas. Mas mede-se antes: um inquilino grande demais reintroduz o problema dentro do próprio fragmento.

### ESC-021 — Sharding e integridade referencial não coexistem bem **[OBRIGATÓRIA]**

Chave estrangeira entre fragmentos não existe. Isso move integridade para a aplicação — exatamente o que
`DAT-001` diz que será contornado. É um custo permanente que precisa estar no ADR.

---

## Capítulo 14.5 — Estado e escala horizontal

### ESC-022 — Sem estado em memória do processo **[OBRIGATÓRIA]**

Sessão, cache local com significado, contador, agendamento e trava em memória impedem escalar
horizontalmente e produzem comportamento diferente por instância — o bug que "só acontece às vezes".

### ESC-023 — Nenhuma afinidade de sessão como requisito **[RECOMENDADA]**

Depender de o usuário voltar à mesma instância impede reciclar instância sem afetar usuário.

### ESC-024 — Trabalho agendado roda uma vez, não uma vez por instância **[OBRIGATÓRIA]**

Ao escalar de uma para três instâncias, todo agendamento local passa a rodar três vezes. Se o trabalho tem
efeito externo — cobrar, enviar, provisionar — isso é `S0`.

Exige eleição de líder, agendador externo, ou trava distribuída com expiração.

### ESC-025 — Trava distribuída tem expiração e trata perda **[OBRIGATÓRIA]**

Trava sem expiração trava para sempre quando o dono morre. E o dono precisa lidar com o caso de ter perdido a
trava por expiração enquanto ainda trabalhava — caso contrário, dois processos agem acreditando ser donos.

### ESC-026 — Arquivo em disco local não sobrevive **[OBRIGATÓRIA]**

Upload, geração de relatório e cache em disco de instância desaparecem no próximo deploy.

### ESC-027 — Pool de conexões dimensionado pelo total, não por instância **[OBRIGATÓRIA]**

Dez instâncias com pool de 20 são 200 conexões. O limite do banco é o teto real de escala horizontal, e ele é
alcançado antes do que se espera. Use intermediador de conexões quando necessário.

---

## Capítulo 14.6 — Contrapressão e descarte de carga

### ESC-028 — Todo recurso tem limite explícito **[OBRIGATÓRIA]**

Concorrência, tamanho de fila, tamanho de lote, conexões, memória por requisição. Sem limite, a degradação
não é gradual: é colapso, e no momento de maior demanda.

### ESC-029 — Rejeitar rápido é melhor que aceitar e morrer **[OBRIGATÓRIA]**

Ao saturar, responda 429 ou 503 com indicação de nova tentativa. Aceitar trabalho que não será concluído
consome recurso, aumenta latência de todos, e transforma sobrecarga parcial em indisponibilidade total.

### ESC-030 — Fila com limite e política de descarte declarada **[OBRIGATÓRIA]**

Fila ilimitada não é resiliência: é latência ilimitada, e memória crescendo até o processo morrer. Ver
`BAK-047`.

### ESC-031 — Interromper trabalho abandonado **[RECOMENDADA]**

Se o cliente desistiu, continuar processando gasta recurso por nada. Propague o cancelamento.

### ESC-032 — Disjuntor em dependência que pode ficar lenta **[RECOMENDADA]**

Abrir o circuito protege você e dá à dependência a chance de recuperar. Retry sem disjuntor amplifica a falha
(`PRF-016`).

### ESC-033 — Priorize tráfego quando saturado **[RECOMENDADA]**

Checkout continua; recomendação e relatório degradam. Definir isso é projeto; descobrir durante o incidente é
sorte.

### ESC-034 — Limite de taxa por sujeito, não global **[OBRIGATÓRIA]**

Limite global permite que um cliente abusivo consuma a cota de todos. Ver `BAK-035`.

### ESC-035 — Capacidade conhecida por teste, não por inferência **[RECOMENDADA]**

O ponto de saturação precisa ser medido antes de ser encontrado em produção. Ver `OPS-046`.

---

## Capítulo 14.7 — Multi-inquilino

Simultaneamente decisão de escala e de segurança. Os achados de vazamento entre inquilinos são `S0` e vão
para o [Volume 5](06-seguranca.md).

### ESC-036 — Escolha o modelo de isolamento com critério declarado **[OBRIGATÓRIA]**

| Modelo | Isolamento | Custo operacional | Serve quando |
| --- | --- | --- | --- |
| **Schema compartilhado** (coluna de inquilino) | Mais fraco: depende de cada consulta | Menor | Muitos inquilinos pequenos, mesmo schema, sem exigência regulatória de separação |
| **Schema por inquilino** | Médio: erro de consulta não atravessa | Médio: migração precisa rodar por schema | Dezenas ou centenas de inquilinos, alguma customização |
| **Banco por inquilino** | Mais forte | Maior: migração, backup e monitoramento por banco | Poucos inquilinos grandes, exigência contratual ou regulatória, necessidade de restauração individual |

Modelos híbridos são legítimos e comuns: compartilhado para o plano básico, banco dedicado para
empresarial. A regra é declarar o critério de promoção.

### ESC-037 — Mudar de modelo depois é migração de dados **[OBRIGATÓRIA]**

`R4`, por inquilino, com janela. Por isso o modelo é decisão de ADR desde o primeiro dia, mesmo com um
inquilino só.

### ESC-038 — Isolamento aplicado no ponto mais interno possível **[OBRIGATÓRIA]** · `S0`

Política no banco ou camada de acesso obrigatória — nunca a disciplina de cada consulta. Consulta sem filtro
de inquilino é `S0`. Ver `SEC-006` e `BAK-019`.

### ESC-039 — O inquilino vem do contexto autenticado, nunca da requisição **[OBRIGATÓRIA]** · `S0`

Identificador de inquilino aceito de parâmetro, corpo ou cabeçalho controlável pelo cliente é troca de
inquilino por vontade do atacante. Ver `BAK-011`.

### ESC-040 — Toda chave de cache e de busca inclui o inquilino **[OBRIGATÓRIA]** · `S0`

Cache, índice de busca, arquivo gerado, relatório e fila. Ver `PRF-020`. É o caminho de vazamento entre
inquilinos que passa por mais revisões sem ser notado, porque não está no código de consulta.

### ESC-041 — Vizinho ruidoso é contido por cota **[OBRIGATÓRIA]**

Um inquilino não pode consumir a capacidade dos outros. Limite de taxa, de concorrência e de tamanho de
trabalho **por inquilino** (`ESC-034`).

### ESC-042 — Operações por inquilino precisam existir desde cedo **[RECOMENDADA]**

Exportar tudo de um inquilino · eliminar tudo de um inquilino (`SEC-056`) · restaurar um inquilino sem afetar
os outros · medir consumo por inquilino. Descobrir na primeira solicitação que a eliminação é inviável é
falha de conformidade, não inconveniente.

---

## Padrões reutilizáveis

**Degrau antes de topologia.** Percorra `ESC-002` por escrito antes de propor réplica, partição ou
shard. *Use sempre.* *Não pule* para o degrau 4 porque "vamos crescer".

**Classificação de leitura.** Cada consulta marcada: tolera atraso / não tolera (`ESC-012`). Só as
que toleram vão à réplica. *Não roteie* "tudo de leitura" para réplica por padrão.

**Desnormalização com dono.** Quatro respostas obrigatórias + detecção de divergência (`ESC-006`,
`ESC-007`). *Use* quando a leitura agregada domina e a fonte não aguenta. *Não use* como atalho de
modelagem.

**Processo sem estado local.** Sessão, upload e job fora da memória/disco da instância (`ESC-022`,
`ESC-026`). *Use* antes de horizontalizar. Agendamento com líder ou fila, nunca `cron` em cada pod
(`ESC-024`).

**Limite explícito + rejeição rápida.** Todo recurso com teto; ao saturar, 503/backpressure em vez de
fila infinita (`ESC-028`–`ESC-030`). *Use* em API, worker e dependência externa.

**Núcleo multi-tenant.** ADR do modelo (`ESC-036`), enforcement interno (`ESC-038`), tenant da auth
(`ESC-039`), prefixo de chave (`ESC-040`). Profundidade operacional → [16](16-multi-tenant.md).

---

## Matrizes de decisão

**Degrau de intervenção (`ESC-002`)**

| Degrau | Quando basta | Quando não |
| --- | --- | --- |
| 1. Corrigir defeito (N+1, lock, scan) | Caminho quente mal escrito | Já medido e limpo |
| 2. Índice / schema local | Consulta correta, plano ruim | Hot set ainda não cabe |
| 3. Cache com invalidação | Leitura repetida, escrita rara | Consistência forte demais |
| 4. Réplica de leitura | Leitura tolera atraso (`ESC-012`) | Decisão de negócio na réplica |
| 5. Partição / shard | Hot set / limite físico | Ainda dá para arquivar (`ESC-018`) |

**Modelo de isolamento — núcleo (`ESC-036`; detalhe em [16](16-multi-tenant.md))**

| Modelo | Isolamento | Serve quando |
| --- | --- | --- |
| Schema compartilhado | Depende do enforcement | Muitos inquilinos pequenos |
| Schema por inquilino | Médio | Dezenas/centenas, alguma customização |
| Banco por inquilino | Forte | Poucos grandes / restore individual |
| Híbrido | Por faixa de plano | Critério de promoção declarado |

**Leitura e atraso (`ESC-011`–`ESC-012`)**

| Tipo de leitura | Réplica? |
| --- | --- |
| Lista, relatório, busca | Sim, se atraso aceitável e monitorado |
| Autorização, saldo, transição de estado | Não — primário |
| "Read-your-writes" do usuário após mutação | Primário ou sessão sticky explícita |

---

## Fluxo de trabalho

```
1. Medir                    → volume, crescimento, ponto de quebra (ESC-001)
2. Degraus 1–2 limpos?      → se não, o achado é o defeito, não a topologia (ESC-002–003)
3. Classificar leituras     → tolerância a atraso; só então réplica (ESC-012)
4. Estado do processo       → remover afinidade, disco local, cron por instância (ESC-022–027)
5. Limites e contrapressão  → teto, rejeição rápida, disjuntor, cota por sujeito (ESC-028–034)
6. Núcleo multi-tenant      → ADR + ESC-036–042; vazamento = S0
7. Se precisar de profundidade de inquilino → Volume 16 (MTN), citando ESC, sem reescrever
8. Toda decisão estrutural  → condição de invalidação na ADR (ESC-004)
```

Papéis: Database, Performance, DevOps/SRE. Capacidade sem medição de [07](07-performance.md) é
decoração.

---

## Exemplos de implementação

**Réplica na decisão de negócio (`ESC-012`)**

```js
// Ruim — autoriza e debita lendo réplica
const saldo = await replica.saldo(contaId)
if (saldo < valor) throw new ErroSaldo()
await primario.debitar(contaId, valor) // saldo na réplica já estava velho

// Bom — leitura que decide regra vai ao primário
const saldo = await primario.saldo(contaId)
```

**Fila ilimitada (`ESC-030`)**

```js
// Ruim
await fila.enqueue(job) // profundidade sem teto

// Bom
if (await fila.profundidade() >= LIMITE) {
  metricas.contador('fila_rejeitada_total', 1)
  throw new ErroSaturacao() // rejeitar rápido (ESC-029)
}
await fila.enqueue(job)
```

**Cache sem inquilino (`ESC-040`)**

```js
// Ruim — S0
cache.get(`pedido:${pedidoId}`)

// Bom
cache.get(`tenant:${tenantId}:pedido:${pedidoId}`)
```

**Sharding antes do N+1 (`ESC-002`, `ESC-019`)**

```
# Ruim
Proposta: shard por tenant_id porque a listagem de pedidos está lenta.
Medição ausente; EXPLAIN mostra N+1 por item.

# Bom
Degrau 1: eliminar N+1 (medido: 1200ms → 40ms).
Shard só quando o hot set persistir após degraus 1–4, com as cinco respostas de ESC-019.
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Shardear antes de corrigir o N+1 | Complexidade permanente para um problema que era um defeito |
| Réplica servindo leitura que decide regra de negócio | `S1` — decisão sobre dado que já mudou |
| Tratar réplica como backup | Exclusão acidental replica em segundos |
| Desnormalizar sem definir quem atualiza | Divergência descoberta pelo cliente |
| Contador incremental sem proteção de concorrência | Perde atualizações sem falhar |
| Fila ilimitada | Latência ilimitada e memória até morrer |
| Aceitar trabalho ao saturar | Sobrecarga parcial vira indisponibilidade total |
| Agendamento em memória com várias instâncias | Executa uma vez por instância; `S0` se tem efeito externo |
| Trava distribuída sem expiração | Trava para sempre quando o dono morre |
| Pool dimensionado por instância | O limite de conexões do banco é o teto real |
| Filtro de inquilino na disciplina do desenvolvedor | `S0` na primeira consulta esquecida |
| Chave de cache sem inquilino | Vazamento que nenhuma revisão de consulta detecta |
| Limite de taxa global | Um cliente abusivo consome a cota de todos |
| Escolher modelo de inquilino sem ADR | Mudar depois é migração de dados por inquilino |

---

## Checklist

- [ ] Proposta de escala cita volume, crescimento e ponto de quebra. (`ESC-001`)
- [ ] Degraus 1–2 limpos antes de topologia; ou justificativa de por que não bastam. (`ESC-002`)
- [ ] Desnormalização com dono e detecção de divergência. (`ESC-006`, `ESC-007`)
- [ ] Leituras classificadas por tolerância a atraso; réplica monitorada. (`ESC-012`, `ESC-013`)
- [ ] Réplica não tratada como backup. (`ESC-014`)
- [ ] Processo sem estado local; jobs uma vez no cluster. (`ESC-022`, `ESC-024`)
- [ ] Todo recurso com limite e comportamento ao saturar. (`ESC-028`–`ESC-030`)
- [ ] Limite de taxa por sujeito/inquilino, não só global. (`ESC-034`)
- [ ] Núcleo multi-tenant: ADR, enforcement interno, tenant da auth, chaves com inquilino.
      (`ESC-036`–`ESC-040`)
- [ ] Cotas por inquilino; operações exportar/eliminar/restaurar/medir previstas ou no backlog.
      (`ESC-041`, `ESC-042`)
- [ ] Decisão estrutural com condição de invalidação. (`ESC-004`)

---

## Prompt do volume

```
You are operating EOS Volume 14 — Scalability (`ESC`).

Mission: judge structural growth decisions and the multi-tenant nucleus (ESC-036–042) with numbers,
not ambition. Do not deepen tenant product/ops here — that is Volume 16 (MTN), which cites ESC.

Load: agents/_shared/core-contract.md, 00-constituicao-da-engenharia.md, 14-escalabilidade.md,
07-performance.md (measurement discipline), 05-banco-de-dados.md as needed, 16-multi-tenant.md when
tenant depth is in scope (cite ESC-036–042; do not restate them as new rules).

Mandatory sequence:
1. Demand current volume, growth rate, and break point (ESC-001). Missing numbers = primary finding.
2. Walk ESC-002 steps; if steps 1–2 are dirty, that defect is the finding — not a shard proposal.
3. Classify reads by staleness tolerance before any replica recommendation (ESC-012).
4. Inventory process-local state that blocks horizontal scale (ESC-022–027).
5. Inventory limits and backpressure behaviour (ESC-028–034).
6. Audit multi-tenant nucleus ESC-036–042; cross-tenant leak is S0. For provisioning, customization,
   billing, large-tenant ops → report against Volume 16, citing ESC ids.
7. Every structural proposal states its invalidation condition (ESC-004).

Do not: treat infrastructure as a fix for bad queries (ESC-003); move or renumber ESC rules;
reaffirm MTN rules.

Output: exactly the "Verificação obrigatória de saída" block of Volume 14, in Brazilian Portuguese,
MUST-FIX vs OPPORTUNITY separated (CON-018).
```

---

## Critérios de aceite

Uma proposta ou módulo passa em escalabilidade quando:

1. Números de `ESC-001` estão presentes e medidos (não inventados).
2. A intervenção proposta respeita `ESC-002`, ou justifica por que os degraus anteriores não bastam.
3. Leituras em réplica são só as que toleram atraso; atraso monitorado (`ESC-012`, `ESC-013`).
4. Nenhum estado em memória/disco local impede N instâncias sem plano (`ESC-022`, `ESC-026`).
5. Recursos críticos têm limite e comportamento de saturação declarados (`ESC-028`–`ESC-030`).
6. Núcleo multi-tenant `ESC-036`–`ESC-040` satisfeito no ponto interno; vazamento = reprovação.
7. Decisões estruturais registradas com condição de invalidação (`ESC-004`).

Profundidade de produto/operação multi-tenant não é cobrada neste volume — cobrada em
[16](16-multi-tenant.md), sobre o núcleo acima.

---

## Verificação obrigatória de saída

```
## Números que embasam a proposta
Volume atual: <medido> | Crescimento: <observado> | Ponto de quebra: <onde e por quê>

## Degrau de intervenção (ESC-002)
Degraus 1 e 2 estão limpos? <sim/não — se não, o achado é o defeito>
Degrau proposto: <n> | Por quê os anteriores não bastam: <...>

## Leituras e réplicas
| Leitura | Tolera atraso? | Destino | Justificativa |

## Desnormalizações (existentes e propostas)
| Cópia | Origem | Quem atualiza | Quando | Detecção de divergência |

## Estado que impede escala horizontal
| Local | Tipo de estado | Consequência com N instâncias | Severidade |

## Limites e contrapressão
| Recurso | Limite atual | Comportamento ao saturar | Lacuna |

## Multi-inquilino
Modelo: <compartilhado | schema | banco | híbrido> | Registrado em ADR? <...>
| Caminho | Filtro de inquilino aplicado onde | Veredito |
| Chave de cache/busca/arquivo | Inclui inquilino? | Severidade |
Cotas por inquilino: <presentes/ausentes>
Operações por inquilino: exportar <> | eliminar <> | restaurar <> | medir <>
```
