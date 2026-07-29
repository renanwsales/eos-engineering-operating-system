# 📒 Volume 16 — Multi-Tenant

Prefixo: `MTN` · Regras: MTN-001 a MTN-058 · Papel: [Arquiteto](agents/01-architect.md)

Em SaaS, **inquilino** é a unidade de isolamento, cobrança, customização e conformidade. Errar a
definição custa migração de dados por cliente; errar o isolamento é `S0`.

O [Volume 14](14-escalabilidade.md) já fixa o núcleo: modelo de isolamento (`ESC-036`), mudança de
modelo como `R4` (`ESC-037`), filtro no ponto mais interno (`ESC-038`), inquilino do contexto
autenticado (`ESC-039`), chave de cache/busca com inquilino (`ESC-040`), cotas (`ESC-041`) e
operações por inquilino (`ESC-042`). Este volume **cita** essas regras e cobre a profundidade
operacional: identidade e hierarquia, provisionamento, customização, impersonação, faturamento e o
inquilino grande.

**Fronteira.** Tudo que é específico de multi-inquilino como produto e operação. Não cobre: controle
de acesso genérico (→ [06](06-seguranca.md)); sharding como técnica (→ [14](14-escalabilidade.md));
contrato HTTP (→ [15](15-apis.md)). Achados de vazamento classificam-se pelas severidades de
`SEC` / `ESC`.

---

## Fundamentos

"Tenant" ambíguo é a dívida invisível. Organização, conta de faturamento, workspace e ambiente de
sandbox misturados num único `tenant_id` forçam, meses depois, split impossível sem downtime. O
modelo de isolamento (`ESC-036`) decide custo operacional para sempre: schema compartilhado escala
em número de inquilinos e falha em restauração cirúrgica; banco por inquilino inverte a equação.

O vazamento clássico não está na query óbvia — está no cache, no índice de busca, no PDF gerado, na
fila, no e-mail e no webhook (`ESC-040`). Este volume trata esses caminhos como superfície de
primeira classe.

---

## Capítulo 16.1 — O que é um inquilino

### MTN-001 — Defina inquilino em linguagem de produto antes do schema **[IMUTÁVEL]**

Escreva: quem isola dados de quem; quem paga; quem administra usuários; quem pode ser eliminado de
uma vez. Se duas pessoas desenham tabelas diferentes a partir da frase, a definição não está pronta.

### MTN-002 — Separe organização, faturamento e workspace quando os ciclos de vida divergem **[OBRIGATÓRIA]**

| Conceito | Ciclo típico |
| --- | --- |
| Organização | Longevidade, marca, domínio |
| Conta de faturamento | Contrato, NF, inadimplência |
| Workspace / projeto | Colaboração, dados operacionais |

Colapsar os três num ID único parece simples até um cliente pedir dois workspaces numa fatura — ou
uma fatura para três marcas.

### MTN-003 — Hierarquia entre inquilinos é explícita ou inexistente **[OBRIGATÓRIA]**

Árvore (holding → filiais) exige regra de visibilidade, de admin e de relatório consolidado. Hierarquia
implícita ("às vezes o pai vê o filho") é vazamento com desculpa.

### MTN-004 — Ambiente sandbox não é o inquilino de produção com flag **[OBRIGATÓRIA]**

Mesmo banco lógico com `is_test=true` mistura backup, retenção e risco de job que processa os dois.
Sandbox isolado (outro tenant tree ou outro schema/banco) desde o dia um.

### MTN-005 — O identificador de inquilino é estável e não reutilizado **[OBRIGATÓRIA]**

Reciclar ID após cancelamento reata histórico, arquivos e webhooks ao cliente novo. É `API-004` no
nível de tenant.

---

## Capítulo 16.2 — Modelo de isolamento

### MTN-006 — Escolha o modelo com ADR e critério de promoção **[OBRIGATÓRIA]**

Fundação: `ESC-036`. Este volume exige o ADR no primeiro inquilino (`ESC-037`).

### MTN-007 — Schema compartilhado exige política no banco ou camada de acesso obrigatória **[OBRIGATÓRIA]** · `S0`

`ESC-038`, `SEC-006`. Checklist de code review não é controle.

### MTN-008 — Schema por inquilino: migração é frota **[OBRIGATÓRIA]**

Toda migração roda N vezes. Sem orquestração, observabilidade por schema e abort, o modelo não está
operável.

### MTN-009 — Banco por inquilino: restore e compliance individuais são o benefício que se compra **[RECOMENDADA]**

Justifique pelo benefício (restore, isolamento regulatório), não pelo organograma.

### MTN-010 — Híbrido (shared + dedicated) declara o critério de upgrade **[OBRIGATÓRIA]**

Plano, região, requisito contratual, tamanho. Upgrade é migração de dados (`R4`) — não "flag no
admin".

### MTN-011 — Mudança de modelo entre isolamentos é projeto, não tarefa **[OBRIGATÓRIA]**

`ESC-037`. Plano: dual write ou copy, validação de contagem, cutover, rollback, comunicação.

---

## Capítulo 16.3 — Identidade e contexto

### MTN-012 — Inquilino ativo vem do contexto autenticado, nunca do body/query livre **[IMUTÁVEL]** · `S0`

`ESC-039`, `BAK-011`. Header escolhido pelo cliente só é válido se assinado/amarrado à sessão e
autorizado para aquele membership.

### MTN-013 — Usuário multi-inquilino tem membership explícito e troca de contexto auditada **[OBRIGATÓRIA]**

Lista de tenancies; troca gera evento de segurança (`SEC-051`). Token que contém "todos os tenants"
sem necessidade amplia blast radius.

### MTN-014 — Token e sessão amarram o inquilino atual **[OBRIGATÓRIA]**

Trocar tenant exige novo token ou claim atualizado. Cookie de sessão com tenant só no client state
é bypass.

### MTN-015 — Convenções de subdomínio/domínio customizado resolvem para tenant no edge, com prova **[OBRIGATÓRIA]**

DNS → tenant id verificado; nunca confiar só no Host sem mapear para registro autenticado. Host
header spoofing é clássico.

### MTN-016 — Impersonação de suporte é privilegiada, temporária e registrada **[OBRIGATÓRIA]** · `S1`

Quem, por quê, em qual tenant, início/fim, ações. Sem registro, é acesso fantasma a dado pessoal
(`SEC-011`).

---

## Capítulo 16.4 — Onde o isolamento vaza

### MTN-017 — Inventário obrigatório dos caminhos fora da query **[OBRIGATÓRIA]**

Cache, CDN, busca, blob/PDF, fila, job, e-mail, webhook, export, log, analytics, backup restore.
Cada um com a pergunta: a chave/partição inclui tenant? (`ESC-040`)

### MTN-018 — Busca full-text e embeddings filtram por tenant na recuperação **[OBRIGATÓRIA]** · `S0`

Índice global sem filtro é vazamento com relevância. Em RAG, a mesma regra (`IAX` quando ativo).

### MTN-019 — Objeto em storage: path ou metadata com tenant + URL assinada **[OBRIGATÓRIA]** · `S0`

Bucket público com UUID "secreto" não é isolamento.

### MTN-020 — Mensagem de fila carrega tenant_id e o consumidor não aceita override **[OBRIGATÓRIA]**

Job que processa payload sem revalidar membership republica o vazamento.

### MTN-021 — E-mail e notificação não cruzam dado de outro tenant no template **[OBRIGATÓRIA]**

Digest "agregado" mal feito é vazamento para a caixa de entrada.

### MTN-022 — Log e suporte: query por tenant sem expor outros no mesmo painel por default **[OBRIGATÓRIA]**

`SEC-050` no conteúdo; aqui, a UI de operação não lista eventos multi-tenant na mesma tela sem
quebra explícita de isolamento (e privilégio).

### MTN-023 — Relatório e export assíncronos herdam o tenant do solicitante no momento da criação **[OBRIGATÓRIA]**

Trocar de contexto depois não amplia o arquivo já gerado — e o arquivo não é servido cross-tenant.

---

## Capítulo 16.5 — Autorização dentro e entre inquilinos

### MTN-024 — Papéis são por membership, não globais por padrão **[OBRIGATÓRIA]**

Admin do tenant A não é admin do tenant B. Papel global só para operadores da plataforma, com
`MTN-016`.

### MTN-025 — Autorização por objeto continua obrigatória dentro do tenant **[OBRIGATÓRIA]** · `S0`

`SEC-004`. Isolar tenant não autoriza todo membro a ver todo registro.

### MTN-026 — Endpoints de plataforma (super-admin) são superfície separada **[OBRIGATÓRIA]**

Rotas, auth, auditoria e rate limit próprios. Misturar com API do tenant convida escalada.

### MTN-027 — Convite cria membership com expiração e papel mínimo **[OBRIGATÓRIA]**

Link de convite é capability. Sem expiração e sem vínculo ao tenant certo, é sequestro de acesso.

---

## Capítulo 16.6 — Provisionamento e desprovisionamento

### MTN-028 — Provisionar é uma transação de produto com estados **[OBRIGATÓRIA]**

Criando → ativo → suspenso → em eliminação → eliminado. Estado inválido representável é achado
(`ARC-009`).

### MTN-029 — Suspensão bloqueia escrita e efeitos externos, não só o login **[OBRIGATÓRIA]**

API keys, webhooks de saída, jobs e billing extension. Login bloqueado com workers cobrando é falha.

### MTN-030 — Eliminação é processo, não DELETE cascade na raiva **[OBRIGATÓRIA]**

`SEC-056`, `ESC-042`. Soft hold, export opcional, hard delete, confirmação de limpeza em busca,
cache e blobs.

### MTN-031 — Desprovisionamento verifica resíduos nos caminhos do inventário `MTN-017` **[OBRIGATÓRIA]**

Tenant "apagado" com PDF no CDN é incidente de conformidade.

### MTN-032 — Reativação após suspensão é explícita; após hard delete, é novo tenant **[OBRIGATÓRIA]**

Não reanime o mesmo ID (`MTN-005`).

---

## Capítulo 16.7 — Customização

### MTN-033 — Customização por configuração, não por fork de código por tenant **[OBRIGATÓRIA]**

Fork por cliente destrói o produto único. Preferência, tema, limites e flags tipadas.

### MTN-034 — Campo customizado tem tipo, validação e cota **[OBRIGATÓRIA]**

JSON livre ilimitado vira schema paralelo não indexável e superfície de XSS/injeção se renderizado.

### MTN-035 — Domínio customizado: TLS, verificação de posse, rollback **[OBRIGATÓRIA]**

Sem verificação de posse, alguém aponta o domínio do vizinho.

### MTN-036 — Tema/branding não remove contraste nem estados de foco **[OBRIGATÓRIA]**

`UXI` / `DSY`. White-label que quebra acessibilidade é regressão, não customização.

### MTN-037 — Limite: customização que exige regra de negócio divergente é produto separado ou recusa **[RECOMENDADA]**

Registrar "não faremos" com motivo. Um cliente não define o roadmap silencioso (`PRD` quando ativo).

---

## Capítulo 16.8 — Vizinho ruidoso e inquilino grande

### MTN-038 — Cotas por tenant em API, jobs, storage e busca **[OBRIGATÓRIA]**

`ESC-041`, `ESC-034`. Sem cota, um tenant é uma arma de DoS contra os outros.

### MTN-039 — Fair scheduling em filas multi-tenant **[RECOMENDADA]**

Fila FIFO global permite que um tenant ocupe todos os workers. Particione ou use weighted fair
queueing.

### MTN-040 — Detecte o tenant grande antes que ele force sharding de pânico **[OBRIGATÓRIA]**

Métricas de uso por tenant (`ESC-042`). Gatilho de upgrade para dedicado (`MTN-010`).

### MTN-041 — Hot key de tenant: plano de mitigação declarado **[OBRIGATÓRIA]**

Cache stampede, lock, rate limit mais agressivo, leitura em réplica só onde `ESC-012` permite.

### MTN-042 — Teste de carga multi-tenant inclui vizinho ruidoso **[RECOMENDADA]**

Um cenário com 1 tenant agressivo + N quietos. Sem isso, capacidade mentida.

---

## Capítulo 16.9 — Dados, exportação e faturamento

### MTN-043 — Exportação completa por tenant é requisito desde cedo **[OBRIGATÓRIA]**

`ESC-042`. Formato documentado; assíncrono; só dados daquele tenant; link expirável.

### MTN-044 — Restauração de um tenant não reescreve os outros **[OBRIGATÓRIA]**

Em shared schema, restore seletivo é difícil — por isso entra no ADR do modelo (`MTN-006`).

### MTN-045 — Medição de uso para billing é append-only e reconciliável **[OBRIGATÓRIA]**

Contador só em memória ou só em cache diverge da fatura. Evento de uso + agregação.

### MTN-046 — Fatura e uso são do tenant de faturamento, não do workspace filho sem regra **[OBRIGATÓRIA]**

Ambiguidade de `MTN-002` explode no financeiro.

### MTN-047 — Inadimplência: degradação controlada, não delete imediato **[OBRIGATÓRIA]**

Somente leitura → suspensão (`MTN-029`) → eliminação com aviso. Delete no primeiro webhook do
gateway é brutalidade operacional e legal.

---

## Capítulo 16.10 — Testes e operação

### MTN-048 — Todo teste de feature multi-tenant usa pelo menos dois tenants **[OBRIGATÓRIA]**

Um tenant só não pega vazamento. Fixture A e B; assert que A não vê B.

### MTN-049 — Teste de regressão de isolamento para cache e busca **[OBRIGATÓRIA]**

Além da query. É onde `ESC-040` falha.

### MTN-050 — Proibido tenant de teste permanente em produção com dado real misturado **[OBRIGATÓRIA]**

`SEC-057`. Dados de demo sintéticos; ou sandbox isolado (`MTN-004`).

### MTN-051 — Runbook: vazamento entre tenants **[OBRIGATÓRIA]**

Contenção, identificação do blast radius, comunicação, patch, auditoria. Exercitado em tabletop.

### MTN-052 — Migração de schema em frota (schema-por-tenant) tem canário e progresso **[OBRIGATÓRIA]**

`MTN-008`. Falha no tenant 47 de 200 não deixa frota pela metade sem telemetria.

### MTN-053 — Backup prova restore de um tenant no modelo escolhido **[OBRIGATÓRIA]**

`OPS` de backup + `MTN-044`. Backup que só restaura o cluster inteiro, quando o contrato promete
restore por tenant, é falsa conformidade.

---

## Capítulo 16.11 — Observabilidade multi-tenant

### MTN-054 — Todo log e métrica de request carregam tenant_id quando houver contexto **[OBRIGATÓRIA]**

Sem cardinalidade explosiva de user_id solto; tenant é a dimensão certa para cotas e incidentes.
Cuidado com cardinalidade alta demais de tenant em métricas (`OBS` quando ativo).

### MTN-055 — Alertas de saturação por tenant, não só globais **[RECOMENDADA]**

`ESC-041`. Alerta global esconde o ofensor.

### MTN-056 — Painel de uso por tenant para suporte e success **[RECOMENDADA]**

Com autorização de plataforma (`MTN-026`).

---

## Capítulo 16.12 — Produto e limites

### MTN-057 — Onboarding declara o que o tenant isola e o que é compartilhado (catálogo global, etc.) **[RECOMENDADA]**

Expectativa errada ("meu catálogo é só meu" quando é da plataforma) vira ticket de "vazamento".

### MTN-058 — Recusar requisito que quebra isolamento em nome de conveniência **[OBRIGATÓRIA]**

"Endpoint que lista todos os tenants para o parceiro" sem controle de plataforma é `S0` disfarçado.
Escale ao orquestrador / segurança.

---

## Padrões reutilizáveis

**Padrão: TenantContext obrigatório.** Objeto de request derivado da auth; repositórios recebem
contexto, não `tenantId` solto do controller.

**Padrão: row-level policy + testes A/B.** Em shared schema, RLS ou equivalente + testes de dois
tenants.

**Padrão: prefixo de chave `tenant:{id}:`.** Cache, lock, fila — um helper único; greppável.

**Padrão: delete pipeline.** Fila de eliminação com etapas verificáveis (DB → search → blob → cache).

**Padrão: metering events.** `UsageRecord{tenant, metric, qty, at}` imutável.

---

## Matrizes de decisão

| Situação | Modelo tende a |
| --- | --- |
| Muitos tenants pequenos, mesmo schema | Shared + RLS (`ESC-036`) |
| Poucos enterprise, restore individual | Database per tenant |
| Mix freemium + enterprise | Híbrido com critério (`MTN-010`) |
| Regulação de residência de dados | Banco/região por tenant ou pool |

| Caminho | Inclui tenant? |
| --- | --- |
| Query | Obrigatório (`ESC-038`) |
| Cache key | Obrigatório (`ESC-040`) |
| Search index | Obrigatório (`MTN-018`) |
| Object path | Obrigatório (`MTN-019`) |
| Job payload | Obrigatório (`MTN-020`) |

---

## Fluxo de trabalho

```
1. Definir organização / billing / workspace (MTN-001–003)
2. ADR do modelo de isolamento (MTN-006)
3. TenantContext + enforcement interno (ESC-038)
4. Inventário de vazamento (MTN-017) e correção
5. Cotas e metering (MTN-038, MTN-045)
6. Export/delete/restore paths (MTN-043–044, MTN-030)
7. Testes com dois tenants + cache/busca (MTN-048–049)
8. Runbook de vazamento (MTN-051)
```

---

## Exemplos de implementação

```
// Ruim — MTN-012
const tenantId = req.headers['x-tenant-id']
const orders = await db.orders.findMany({ where: { tenantId } })

// Bom — tenant da sessão/membership
const tenantId = auth.session.tenantId
assert(await membership.exists(auth.userId, tenantId))
const orders = await ordersRepo.listForTenant(tenantId, auth.actor)
```

```
// Ruim — cache sem tenant (ESC-040 / MTN-017)
cache.get(`order:${orderId}`)

// Bom
cache.get(`tenant:${tenantId}:order:${orderId}`)
```

```
# Ruim — teste de um tenant só
it('lists orders', async () => { ... })

# Bom — MTN-048
it('does not include orders from other tenants', async () => {
  await createOrder({ tenant: 'A' })
  await createOrder({ tenant: 'B' })
  const list = await listOrders(asUserOf('A'))
  expect(list.every(o => o.tenantId === 'A')).toBe(true)
})
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| `tenant_id` do client sem membership | Troca de tenant (`ESC-039`) |
| Um ID para org+billing+workspace | Migração impossível depois (`MTN-002`) |
| Cache/busca sem tenant | `S0` (`ESC-040`) |
| Admin global na API do tenant | Escalada (`MTN-026`) |
| Delete cascade sem limpar blob/busca | Resíduo de dado pessoal (`MTN-031`) |
| Fork de código por cliente | Produto fragmentado (`MTN-033`) |
| Fila FIFO sem fairness | Vizinho ruidoso (`MTN-039`) |
| Teste com um tenant | Vazamento não detectado (`MTN-048`) |
| Tenant demo com PII em prod | `SEC-057` |
| Restore só do cluster quando o contrato é por tenant | Falsa conformidade (`MTN-053`) |

---

## Checklist

- [ ] Definição de inquilino e hierarquia claras. (`MTN-001`–`MTN-003`)
- [ ] ADR de isolamento. (`MTN-006`, `ESC-036`)
- [ ] Tenant só do contexto autenticado. (`MTN-012`)
- [ ] Inventário cache/busca/blob/fila/email. (`MTN-017`)
- [ ] Authz por objeto dentro do tenant. (`MTN-025`)
- [ ] Impersonação auditada. (`MTN-016`)
- [ ] Suspensão e eliminação com resíduos. (`MTN-029`–`MTN-031`)
- [ ] Cotas por tenant. (`MTN-038`)
- [ ] Export por tenant. (`MTN-043`)
- [ ] Metering reconciliável. (`MTN-045`)
- [ ] Testes com ≥2 tenants. (`MTN-048`)
- [ ] Runbook de vazamento. (`MTN-051`)
- [ ] Restore conforme o modelo. (`MTN-053`)

---

## Prompt do volume

```
You are reviewing or designing multi-tenant behaviour under EOS Volume 16 (MTN).

Load: core-contract, 00-constituicao, 16-multi-tenant.md, 14-escalabilidade.md
(ESC-036–042), 06-seguranca.md, 03-backend.md as needed.

Sequence:
1. Define tenant vs billing vs workspace; reject ambiguous IDs.
2. Confirm isolation model ADR and enforcement point (not per-query discipline).
3. Inventory non-query leak paths: cache, search, blob, queue, email, export, logs.
4. Check membership, impersonation, platform vs tenant surfaces.
5. Check quotas, metering, export/delete/restore.
6. Require tests with two tenants including cache/search.
7. Classify cross-tenant leak as S0; do not invent new SEC rules — cite SEC/ESC.

Output: findings with evidence, isolation matrix, leak inventory, open R4 migrations.
```

---

## Critérios de aceite

1. ADR de isolamento existe e é seguido (`MTN-006`).
2. Nenhum tenant id controlável pelo cliente sem membership (`MTN-012`).
3. Inventário `MTN-017` percorrido com evidência.
4. Cotas por tenant em superfícies públicas (`MTN-038`).
5. Export e delete com verificação de resíduo (`MTN-043`, `MTN-031`).
6. Testes com dois tenants + pelo menos um caminho de cache ou busca (`MTN-048`, `MTN-049`).
7. Runbook de vazamento existe (`MTN-051`).

---

## Verificação obrigatória de saída

```
## Definição
Inquilino: <...> | Billing: <...> | Workspace: <...>
Modelo: <shared | schema | database | hybrid> | ADR: <...>

## Isolamento
Enforcement: <onde> | Tenant source: <auth context>
| Caminho | Tenant na chave/partição? | Evidência |

## Operação
Cotas: <> | Metering: <> | Export: <> | Delete residual check: <>
Impersonação: <> | Testes ≥2 tenants: <>

## Achados
| ID | Sev | Evidência |

## Não verificado
| Item | Motivo |
```
