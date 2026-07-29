# 📙 Volume 15 — APIs

Prefixo: `API` · Regras: API-001 a API-058 · Papel: [Backend](agents/02-backend.md)

Uma API publicada é um **produto com usuários que você não controla**. Eles versionam clientes, cacheiam
respostas, geram SDK a partir do seu schema e cobram o custo de qualquer mudança incompatível — em
suporte, em incidentes e em confiança.

O [Volume 03](03-backend.md) é o lado de **dentro**: validação, autorização aplicada, erros no código,
idempotência, webhooks e GraphQL como implementação (`BAK-031`–`BAK-037`, `BAK-049`–`BAK-065`). Este
volume é o **contrato**: o que se promete, como evolui, como se documenta, e o que nunca se quebra em
silêncio.

**Fronteira.** Desenho e evolução do contrato público (e do contrato interno tratado como público).
Não cobre: regra de negócio nem autorização em código (→ [03](03-backend.md)); isolamento de
inquilino (→ [16](16-multi-tenant.md)); implementação de cache e performance (→ [07](07-performance.md)).

---

## Fundamentos

Contrato de API diverge de interface de biblioteca num ponto decisivo: **você não força o upgrade do
consumidor**. App móvel fica meses na mesma build; integração de parceiro congela; script de cliente
copia um exemplo de 2022. Por isso compatibilidade não é cortesia — é a propriedade que mantém o
sistema vivo enquanto você muda o servidor.

Três falhas recorrentes nascem da mesma confusão: tratar o modelo interno como o recurso exposto;
versionar só quando já quebrou alguém; documentar o que o código fazia ontem. Este volume existe para
tornar essas falhas detectáveis antes do consumidor.

---

## Capítulo 15.1 — API como produto

### API-001 — Toda API pública tem dono, consumidores conhecidos e política de compatibilidade **[OBRIGATÓRIA]**

Sem dono, ninguém responde quando um campo muda de significado. Sem mapa de consumidores, "ninguém
usa" é palpite. Sem política publicada, cada breaking change é uma discussão improvisada.

### API-002 — Distinga API pública, parceiro e interna — por escrito **[OBRIGATÓRIA]**

| Tipo | Promessa | Exemplo |
| --- | --- | --- |
| Pública | Compatibilidade forte, depreciação medida | API de loja para apps |
| Parceiro | Contrato bilateral, prazo negociado | Integração com ERP |
| Interna | Pode mudar com deploy coordenado | Serviço a serviço no mesmo monólito modular |

Tratar interna como pública sem necessidade engessa. Tratar pública como interna quebra clientes.

### API-003 — O modelo de recurso não é o modelo de tabela **[OBRIGATÓRIA]**

Expor linha de banco é vazar schema, forçar JOIN no cliente e acoplar evolução de dado a contrato
(`BAK-033`). Recurso é linguagem de negócio: `Order`, `InvoiceLine`, não `orders` + `order_items`
cru.

### API-004 — Estabilidade do identificador é parte do contrato **[OBRIGATÓRIA]**

ID que muda, que é reciclado, ou que é sequencial previsível em recurso sensível (`BAK-037`) não é
detalhe de implementação — é falha de contrato e, no caso sequencial, de segurança.

### API-005 — Erros de projeto que só aparecem com consumidores **[OBRIGATÓRIA]**

Enum que não prevê valor desconhecido; data sem fuso; dinheiro como float; lista sem paginação;
filtro que aceita SQL criativo; campo que significa duas coisas conforme o status. Liste-os no ADR
do contrato antes do primeiro cliente externo.

---

## Capítulo 15.2 — REST e recursos

### API-006 — Recurso é substantivo; ação arriscada vira sub-recurso ou comando explícito **[OBRIGATÓRIA]**

`POST /orders/{id}/cancellation` é auditável e autorizável. `POST /orders` com `{ "action": "cancel" }`
impede autorização e métrica por operação (`BAK` antipadrão de ação por parâmetro).

### API-007 — Semântica de método é parte do contrato **[OBRIGATÓRIA]**

`GET` não altera estado. `PUT` é substituição completa do recurso sob o contrato. `PATCH` é parcial
com campos nomeados. `DELETE` é idempotente na prática (404 ou 204 na segunda chamada — declare
qual). Cite `BAK-031` para o lado servidor; aqui a regra é: o consumidor pode confiar na semântica.

### API-008 — Coleções têm forma estável **[OBRIGATÓRIA]**

Envelope consistente: itens, paginação, eventualmente agregados declarados. Misturar array cru numa
rota e objeto noutra força cada cliente a ramificar.

### API-009 — Hipermídia é opcional; links documentados para ações principais são recomendados **[RECOMENDADA]**

Não obrigue HATEOAS completo. Documente as URLs de transição de estado que o cliente precisa
(`cancel`, `pay`, `invoice`).

### API-010 — Quando não usar REST puro **[RECOMENDADA]**

Upload multipart, SSE/streaming, RPC de operação longa com job id — declare o estilo. Fingir que é
REST e quebrar a semântica de método é pior que um endpoint RPC honesto.

---

## Capítulo 15.3 — GraphQL no contrato

### API-011 — GraphQL é contrato de schema, não "REST flexível" **[OBRIGATÓRIA]**

Toda mudança de campo, tipo e nullability é mudança de contrato. As regras de implementação
(`BAK-060`–`BAK-065`) continuam; aqui: o schema publicado é a API.

### API-012 — Escolha GraphQL por necessidade de forma de leitura divergente, não por moda **[RECOMENDADA]**

Clientes com necessidades de dados muito diferentes e overfetching medido. Um cliente só, com
recursos estáveis — REST costuma ser mais simples de cachear, limitar e versionar.

### API-013 — Nullability e depreciação no schema são decisões irreversíveis na prática **[OBRIGATÓRIA]**

Campo non-null que passa a poder falhar quebra clientes. Prefira nullable + erro parcial explícito
(`BAK-063`) a mentir com non-null.

### API-014 — Limite de profundidade e custo faz parte do contrato publicado **[OBRIGATÓRIA]**

`BAK-061` no servidor; no contrato, documente os limites para o consumidor não descobrir com 429/5xx
opacos.

---

## Capítulo 15.4 — Formato de erro

### API-015 — Erro é contrato: código estável, mensagem, campo, correlação **[OBRIGATÓRIA]**

```
{
  "error": {
    "code": "order.not_cancellable",
    "message": "Pedido já enviado não pode ser cancelado",
    "field": null,
    "trace_id": "..."
  }
}
```

Código estável para o cliente ramificar. Mensagem para humano. Campo para formulário. `trace_id`
para suporte (`BAK-026`). Mudar o significado de um `code` é breaking change.

### API-016 — Status HTTP alinhado à classe de erro, nunca 200 com falha escondida em REST **[OBRIGATÓRIA]**

4xx cliente, 5xx servidor. Em GraphQL, 200 com errors é permitido — e então `BAK-063` e monitoramento
obrigatórios. Não misture os dois estilos na mesma superfície sem documentar.

### API-017 — Não vaze detalhe interno na mensagem pública **[OBRIGATÓRIA]**

Stack, nome de tabela, query — `SEC-032`, `BAK-027`. Mensagem pública + detalhe só em log com
correlação.

### API-018 — Catálogo de códigos de erro versionado com a API **[RECOMENDADA]**

Lista publicada. Código novo é aditivo. Código removido segue depreciação (`API-036`).

---

## Capítulo 15.5 — Paginação, filtro e ordenação

### API-019 — Toda coleção listável é paginada com limite do servidor **[OBRIGATÓRIA]**

`BAK-032`. Adicionar paginação depois é breaking se clientes dependiam do array completo.

### API-020 — Escolha offset vs cursor com critério declarado **[OBRIGATÓRIA]**

| | Offset | Cursor |
| --- | --- | --- |
| Serve | Admin, páginas estáveis, datasets pequenos | Feed, alta escrita, listas longas |
| Falha | Página instável sob inserção; custo em offset alto | Difícil "ir à página 7"; ordenação precisa de chave estável |

Declare no contrato qual e por quê.

### API-021 — Cursor é opaco para o cliente **[OBRIGATÓRIA]**

Cliente que decodifica cursor acopla-se à implementação. Opaco + documentação de expiração.

### API-022 — Ordenação só por campos allowlisted **[OBRIGATÓRIA]**

Ordenar por coluna arbitrária é vetor de carga e de vazamento de schema. Lista publicada de sort keys.

### API-023 — Filtro é allowlist de campos e operadores **[OBRIGATÓRIA]**

Não aceite árvore de expressão livre do cliente. Cada filtro documentado; tipos e limites claros.

### API-024 — Resposta declara a paginação de forma consistente **[OBRIGATÓRIA]**

`next_cursor` / `has_more` / `total` (total só se barato e declarado). Misturar metadados entre rotas
é defeito de contrato.

---

## Capítulo 15.6 — Versionamento e evolução

### API-025 — Política de versionamento publicada antes do segundo consumidor **[OBRIGATÓRIA]**

URL (`/v1`), cabeçalho, ou evolução só aditiva. A matriz:

| Estratégia | Quando | Custo |
| --- | --- | --- |
| Só aditiva (sem número) | API jovem, poucos clientes | Disciplina forte; um breaking exige vN |
| Versão na URL | Públicos diversos, SDKs | Duplicação de rotas; clareza |
| Versão no cabeçalho | Mesma URL, conteúdo negocia | Mais difícil de depurar e cachear |

### API-026 — O que é mudança compatível **[OBRIGATÓRIA]**

Adicionar campo opcional; adicionar valor de enum **se** clientes toleram desconhecido; adicionar
endpoint; afrouxar validação de entrada; documentar comportamento já existente.

### API-027 — O que é mudança incompatível **[OBRIGATÓRIA]**

Remover campo; renomear; mudar tipo ou significado; tornar obrigatório o que era opcional; restringir
enum; mudar código de erro estável; mudar default documentado; paginar o que era lista completa.

### API-028 — Prefira evolução aditiva a versão nova **[RECOMENDADA]**

Versão nova dobra superfície e congela a antiga. Use versão nova quando o modelo mental mudou, não
quando faltou um campo.

### API-029 — Duas versões simultâneas no máximo, salvo contrato de parceiro **[RECOMENDADA]**

Três versões é sinal de depreciação que não termina.

### API-030 — Campo novo opcional não quebra; campo novo usado sem default no servidor pode quebrar escrita **[OBRIGATÓRIA]**

POST que passa a exigir campo sem default é incompatível na prática mesmo "aditivo" na aparência.

---

## Capítulo 15.7 — Depreciação

### API-031 — Depreciação anuncia, mede, remove — nessa ordem **[OBRIGATÓRIA]**

`BAK-036`. Anúncio sem medição é teatro. Remoção sem uso zero (ou exceção nomeada) é breaking
surpresa.

### API-032 — Cabeçalho e documentação marcam o depreciado **[OBRIGATÓRIA]**

`Deprecation` / `Sunset` quando aplicável; campo marcado no schema; changelog. Cliente precisa
descobrir sem ler o Slack da sua empresa.

### API-033 — Prazo de sunset publicado e cumprido **[OBRIGATÓRIA]**

Prazo no perfil ou política (`[perfil]`). Cumprir inclui contatar consumidores restantes com evidência
de uso.

### API-034 — Medição de uso por campo/endpoint antes de remover **[OBRIGATÓRIA]**

Sem telemetria de uso, "ninguém usa" é fé. Em GraphQL, `BAK-065`.

### API-035 — Exceção de remoção antecipada só com aceitação de risco nomeada **[OBRIGATÓRIA]**

Segurança (`S0`), obrigação legal, ou acordo bilateral. Registro com nome (`CON-042`).

### API-036 — Código de erro e valor de enum depreciados seguem o mesmo rito **[OBRIGATÓRIA]**

Não só paths e campos.

---

## Capítulo 15.8 — Limite de taxa e autenticação do consumidor

### API-037 — Limite de taxa é publicado: cota, janela, resposta, cabeçalhos **[OBRIGATÓRIA]**

`BAK-035` no servidor. No contrato: `X-RateLimit-*` (ou equivalente), `Retry-After`, corpo de erro
estável. Limite secreto produz clientes que martelam.

### API-038 — Limite por sujeito autenticado, não só por IP **[OBRIGATÓRIA]**

`ESC-034`. IP compartilhado (NAT, móvel) pune inocentes; IP único de atacante com muitas chaves
contorna.

### API-039 — Autenticação de API documentada no nível do consumidor **[OBRIGATÓRIA]**

Chave, Bearer, OAuth2 — escopos, rotação, revogação, ambiente (test vs live). Segredo nunca no
query string de URLs logáveis.

### API-040 — Escopos mínimos por operação **[OBRIGATÓRIA]**

Chave com "acesso total" para ler catálogo viola menor privilégio (`SEC-036`). Documente escopos por
grupo de rotas.

### API-041 — Ambiente de teste isolado com dados de teste **[RECOMENDADA]**

Chave de test que aponta para produção é incidente. Contratos e URLs distintos.

---

## Capítulo 15.9 — Documentação e SDK

### API-042 — Documentação executável deriva do contrato, não de wiki paralela **[OBRIGATÓRIA]**

OpenAPI/AsyncAPI/GraphQL SDL como fonte. Wiki que diverge é mentira com formatação (`ARC-011`
aplicado a docs).

### API-043 — Exemplos na documentação são válidos e testados no CI **[OBRIGATÓRIA]**

Exemplo que falha é pior que ausência: é copiado por todos.

### API-044 — Documente autenticação, erros, paginação e limites na primeira página útil **[OBRIGATÓRIA]**

Não enterre o que todo cliente precisa atrás de "referência avançada".

### API-045 — SDK oficial, se existir, versiona junto com a política da API **[RECOMENDADA]**

SDK que quebra em patch da API, ou API que quebra SDK sem major, destrói a confiança nos dois.

### API-046 — Cliente gerado a partir do schema; não mantenha modelos à mão em paralelo **[RECOMENDADA]**

Duplicação diverge. Se gerar, o schema é a verdade.

### API-047 — Changelog de API legível por humanos e por máquina **[RECOMENDADA]**

O que mudou, compatível ou não, prazo de sunset.

---

## Capítulo 15.10 — Webhooks como produto

### API-048 — Webhook de saída tem contrato: eventos, payload, assinatura, reentrega **[OBRIGATÓRIA]**

Implementação em `BAK-054`–`BAK-059`. Aqui: catálogo de eventos versionado; payload mínimo;
verificação para o assinante; política de retry publicada.

### API-049 — Evento novo é aditivo; mudança de payload de evento existente é versionada **[OBRIGATÓRIA]**

Mesma disciplina de campo de API. Payload que muda de forma quebra assinantes silenciosos.

### API-050 — Assinante consegue verificar, inspecionar entregas e reenviar **[RECOMENDADA]**

`BAK-059`. Sem isso, todo incidente vira ticket manual.

### API-051 — Documente ordem não garantida e at-least-once **[OBRIGATÓRIA]**

`BAK-052`, `BAK-050` no receptor. Contrato que mente "exactly once" produz sistemas frágeis.

---

## Capítulo 15.11 — Teste de contrato

### API-052 — Teste de contrato tem dono e roda no CI do provedor e do consumidor quando possível **[OBRIGATÓRIA]**

Provedor garante que não quebrou o schema publicado. Consumidor garante que não depende do não
documentado (pacto/consumer-driven onde couber).

### API-053 — Contrato testa o que é publicado, não o comportamento interno completo **[OBRIGATÓRIA]**

Status, forma, campos obrigatórios, erros estáveis. Regra de negócio profunda permanece nos testes
de domínio (`QAT`).

### API-054 — Breaking change detectada no CI bloqueia o merge **[OBRIGATÓRIA]**

Teatro é publicar OpenAPI e não diffar. Ferramenta de breaking-change no pipeline (`OPS-028`
inverso).

### API-055 — Ambientes de contrato (mock/sandbox) refletem o schema atual **[RECOMENDADA]**

Sandbox atrasado ensina clientes a integrar com o passado.

---

## Capítulo 15.12 — Observabilidade e operação do contrato

### API-056 — Métricas por rota e por código de erro estável **[OBRIGATÓRIA]**

`OPS-018`. Sem isso, depreciação não tem medição (`API-034`) e incidente não tem corte.

### API-057 — Compatibilidade durante deploy: cliente antigo e novo contra servidor novo **[OBRIGATÓRIA]**

`OPS-010`, `ARC-027`. O contrato aditivo precisa ser verdadeiro com as duas versões de código no ar.

### API-058 — Idempotência documentada onde o cliente retenta **[OBRIGATÓRIA]**

`BAK-042`. Cabeçalho de chave de idempotência, se usado, é contrato: TTL, escopo, resposta na
replay.

---

## Padrões reutilizáveis

**Padrão: envelope de lista.** `{ "data": [...], "pagination": { "next_cursor", "has_more" } }` em
todas as coleções.

**Padrão: error code namespaced.** `domain.reason` — estável, pesquisável, traduzível na UI.

**Padrão: expand/include allowlisted.** Em vez de GraphQL prematuro, `?include=items,customer` com
lista fechada.

**Padrão: sunset calendar.** Página única com endpoints depreciados e datas; gerada do mesmo manifesto
que o CI usa.

**Padrão: versão na URL + aditivo dentro da versão.** `/v1` só quebra em `/v2`; dentro de v1, só
aditivo.

---

## Matrizes de decisão

| Pergunta | Prefira | Evite se |
| --- | --- | --- |
| REST vs GraphQL | REST para recursos estáveis e poucos clientes | GraphQL sem limite de custo |
| Offset vs cursor | Cursor em feed/alta escrita | Offset em timeline quente |
| Versão URL vs header | URL para API pública | Header se precisa cache CDN simples |
| Campo novo vs vN | Campo opcional | vN para um campo |
| Webhook vs polling | Webhook para evento de negócio | Polling agressivo sem cota |

| Mudança | Compatível? |
| --- | --- |
| Adicionar campo opcional na resposta | Sim |
| Remover campo | Não |
| Adicionar valor de enum | Condicional (cliente deve tolerar) |
| Mudar significado de campo | Não |
| Passar a paginar | Não, se antes retornava tudo |
| Apertar validação | Não |

---

## Fluxo de trabalho

```
1. Nomear consumidores e tipo de API (pública/parceiro/interna)
2. Modelar recursos (não tabelas); invariantes de ID e erro
3. Escrever OpenAPI/SDL antes do código de borda (ou no mesmo PR)
4. Definir paginação, sort, filtro allowlisted
5. Publicar auth, rate limit, política de versão
6. Implementar no Volume 03 (validação, auth, idempotência)
7. Teste de contrato no CI + exemplos da doc
8. Telemetria de uso por rota/campo
9. Depreciação: anunciar → medir → remover
```

---

## Exemplos de implementação

```
# Ruim — breaking silencioso
# v1: GET /orders → [ {...}, ... ]  (array completo)
# v2 mesmo path: { "data": [...], "next_cursor": "..." }

# Bom — API-019, API-027
# GET /v1/orders já nasceu paginado; ou
# GET /v1/orders mantém array; GET /v2/orders introduz envelope
```

```json
// Ruim — código de erro instável
{ "message": "Something went wrong" }

// Bom — API-015
{
  "error": {
    "code": "invoice.already_paid",
    "message": "Fatura já está paga",
    "trace_id": "01HZX..."
  }
}
```

```
# Ruim — filtro livre
GET /orders?query=status=open;drop table

# Bom — API-023
GET /orders?status=open&created_after=2026-01-01
# status ∈ {open,paid,cancelled}; datas ISO-8601
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Serializar entidade/tabela | Acopla schema; vaza campo (`BAK-033`) |
| Ação por parâmetro `action=` | Auth e métrica impossíveis |
| Paginação depois do primeiro cliente | Breaking (`API-019`) |
| Remover campo "que ninguém usa" sem medir | Quebra silenciosa (`API-034`) |
| Documentação wiki divergente | Clientes integram o fantasma (`API-042`) |
| Rate limit secreto | Martelada e 429 opaco (`API-037`) |
| GraphQL sem limite de custo | DoS de uma query (`BAK-061`) |
| Webhook "exactly once" | Mentira; assinante duplica efeito |
| Três versões eternas | Custo permanente (`API-029`) |
| Sandbox desatualizado | Integração contra o passado (`API-055`) |

---

## Checklist

- [ ] Tipo de API e dono declarados. (`API-001`, `API-002`)
- [ ] Recursos ≠ tabelas; IDs estáveis. (`API-003`, `API-004`)
- [ ] Métodos e status semânticos. (`API-007`, `BAK-031`)
- [ ] Erro com code estável + trace_id. (`API-015`)
- [ ] Coleções paginadas; sort/filtro allowlisted. (`API-019`–`API-023`)
- [ ] Política de versão publicada. (`API-025`)
- [ ] Compatível vs breaking classificado. (`API-026`, `API-027`)
- [ ] Depreciação: anúncio + medição. (`API-031`, `API-034`)
- [ ] Rate limit documentado. (`API-037`)
- [ ] Auth e escopos documentados. (`API-039`, `API-040`)
- [ ] OpenAPI/SDL fonte da doc; exemplos no CI. (`API-042`, `API-043`)
- [ ] Webhooks: eventos, assinatura, at-least-once. (`API-048`, `API-051`)
- [ ] Breaking change bloqueia CI. (`API-054`)
- [ ] Métricas por rota e código. (`API-056`)

---

## Prompt do volume

```
You are designing or reviewing a published API contract under EOS Volume 15 (API).

Load: core-contract, output-schemas, 00-constituicao, 15-apis.md, 03-backend.md
(for BAK implementation rules), and 06-seguranca.md if auth surfaces change.

Sequence:
1. Classify API type (public / partner / internal) and list known consumers.
2. Model resources in business language — not tables.
3. Define error contract, pagination, sort/filter allowlists.
4. State versioning policy and classify each proposed change as compatible or breaking.
5. Require OpenAPI/SDL as source of truth; examples must be CI-tested.
6. Rate limit, auth, and deprecation must be publishable, not tribal knowledge.
7. Cite BAK for server-side enforcement; do not restate BAK rules.
8. Output: contract decisions, breaking-change list, open questions, ADR need.

Stop if a breaking change lacks migration path for consumers or measurement of usage.
```

---

## Critérios de aceite

1. Contrato (OpenAPI/SDL) é a fonte da documentação (`API-042`).
2. Nenhuma coleção pública sem paginação e limite de servidor (`API-019`).
3. Erros com código estável e correlação (`API-015`).
4. Política de versão e depreciação publicadas (`API-025`, `API-031`).
5. CI detecta breaking change (`API-054`).
6. Rate limit e auth documentados para o consumidor (`API-037`, `API-039`).
7. Telemetria permite medir uso antes de remover (`API-034`, `API-056`).

---

## Verificação obrigatória de saída

```
## API
Nome/superfície: <...>
Tipo: <pública | parceiro | interna>
Dono: <...>
Consumidores conhecidos: <...>

## Contrato
Fonte: <OpenAPI | SDL | ...>
Paginação: <offset | cursor | N/A> | Sort/filtro allowlisted: <sim/não>
Erros: código estável <sim/não> | Catálogo <sim/não>

## Versão e depreciação
Política: <...>
Mudanças neste PR: | item | compatível? | evidência |

## Operação
Rate limit documentado: <> | Auth/escopos: <>
Teste de contrato no CI: <> | Breaking gate: <>
Métricas por rota/código: <>

## Não verificado
| Item | Motivo |
```
