# SUMÁRIO — Engineering Operating System

**Manual Operacional de Engenharia para Desenvolvimento Assistido por IA de Sistemas SaaS de Classe Mundial**

25 volumes. Este arquivo é o contrato de fronteiras entre eles: define o que cada volume cobre, o que ele
**não** cobre, e qual prefixo de regra é dele. Quem escreve um volume lê a fronteira dos vizinhos primeiro
(`A-002`).

Contrato de autoria: [`AUTHORING.md`](AUTHORING.md) · Índice de regras: [`RULES-INDEX.md`](RULES-INDEX.md)

---

## Mapa

| # | Volume | Prefixo | Estado | Papel dono |
| --- | --- | --- | --- | --- |
| 00 | [Constituição da Engenharia](00-constituicao-da-engenharia.md) | `CON` | escrito | todos |
| 01 | [Orquestrador](01-orquestrador.md) | `ORC` | escrito | [Orquestrador](agents/00-orchestrator.md) |
| 02 | [Arquitetura](02-arquitetura.md) | `ARC` `SEL` | escrito | [Arquiteto](agents/01-architect.md) |
| 03 | [Backend](03-backend.md) | `BAK` | escrito | [Backend](agents/02-backend.md) |
| 04 | [Frontend](04-frontend.md) | `FRT` | escrito | [Frontend](agents/03-frontend.md) |
| 05 | [Banco de Dados](05-banco-de-dados.md) | `DAT` | escrito | [Database](agents/04-database.md) |
| 06 | [Segurança](06-seguranca.md) | `SEC` | escrito | [Security](agents/05-security.md) |
| 07 | [Performance](07-performance.md) | `PRF` | escrito | [Performance](agents/06-performance.md) |
| 08 | [UX Premium](08-ux-premium.md) | `UXI` | escrito | [Product/UX](agents/09-product-ux.md) |
| 09 | [Design System](09-design-system.md) | `DSY` | escrito | [Frontend](agents/03-frontend.md) |
| 10 | [DevOps](10-devops.md) | `OPS` | escrito | [DevOps/SRE](agents/08-devops-sre.md) |
| 11 | [QA](11-qa.md) | `QAT` | escrito | [QA](agents/07-qa.md) |
| 12 | [Auditoria](12-auditoria.md) | `AUD` | escrito | [Auditor Final](agents/10-final-auditor.md) |
| 13 | [Revisão de Código](13-revisao-de-codigo.md) | `REV` | escrito | [Auditor Final](agents/10-final-auditor.md) |
| 14 | [Escalabilidade](14-escalabilidade.md) | `ESC` | escrito | [Performance](agents/06-performance.md) |
| 15 | [APIs](15-apis.md) | `API` | pendente | [Backend](agents/02-backend.md) |
| 16 | [Multi-Tenant](16-multi-tenant.md) | `MTN` | pendente | [Arquiteto](agents/01-architect.md) |
| 17 | [Observabilidade](17-observabilidade.md) | `OBS` | escrito | [DevOps/SRE](agents/08-devops-sre.md) |
| 18 | [Produto](18-produto.md) | `PRD` | pendente | [Product/UX](agents/09-product-ux.md) |
| 19 | [IA no Produto](19-ia-no-produto.md) | `IAX` | escrito | [Arquiteto](agents/01-architect.md) |
| 20 | [Prompt Engineering](20-prompt-engineering.md) | `PRM` | pendente | [Orquestrador](agents/00-orchestrator.md) |
| 21 | [Playbooks](21-playbooks.md) | `PLB` | escrito | qualquer |
| 22 | [Checklists](22-checklists.md) | `CHK` | pendente | [Auditor Final](agents/10-final-auditor.md) |
| 23 | [Métricas](23-metricas.md) | `MET` | pendente | [Orquestrador](agents/00-orchestrator.md) |
| 24 | [Auditoria Final](24-auditoria-final.md) | `FIN` | pendente | [Auditor Final](agents/10-final-auditor.md) |

Diretórios de apoio: [`prompts/`](prompts/) · [`checklists/`](checklists/) · [`playbooks/`](playbooks/) ·
[`templates/`](templates/) · [`examples/`](examples/) · [`diagrams/`](diagrams/) · [`agents/`](agents/) ·
[`runbooks/`](runbooks/) · [`backlog/`](backlog/) · [`scripts/`](scripts/)

---

## Fronteiras

Cada entrada abaixo é normativa. Quando dois volumes parecem reivindicar o mesmo tema, esta seção decide.

### 00 — Constituição da Engenharia · `CON`

**É deste volume:** princípios inegociáveis, definições de excelência, qualidade, pronto e arquitetura; os seis
portões; a ordem de análise em oito camadas; protocolo de decisão; classificação de severidade; matriz de
priorização; matriz de risco; DoD e DoE; convenções de nome, código e commit.

**Não é:** norma técnica de nenhum domínio. A Constituição diz *como se decide*; os volumes técnicos dizem *o
que é certo*.

### 01 — Orquestrador · `ORC`

**É deste volume:** como a IA pensa, decide, prioriza, despacha papéis, integra achados conflitantes, gerencia
contexto e recusa mudanças ruins. Composição de rodada. Escalada.

**Não é:** o conteúdo das análises. Cada papel tem seu volume.

### 02 — Arquitetura · `ARC` `SEL`

**É deste volume:** `ARC` — regra de dependência, fronteiras de módulo, modelagem de domínio, integração entre
módulos, eventos, versionamento de contrato interno. `SEL` — escolha entre estilos (Clean, Hexagonal, Onion,
monólito modular, microsserviços, event driven, CQRS, vertical slice, feature first, BFF, API first), síncrono
vs assíncrono, estratégia de renderização, comprar vs construir.

**Não é:** contrato de API externa (→ [15](15-apis.md)). Isolamento de inquilino
(→ [16](16-multi-tenant.md)). Decisões de crescimento de dados (→ [14](14-escalabilidade.md)).

### 03 — Backend · `BAK`

**É deste volume:** casos de uso, entidades, repositórios, serviços, DTOs, validação, erros, autorização
aplicada, concorrência, idempotência, transações, filas, workers, trabalho agendado, webhooks de entrada e
saída, GraphQL.

**Não é:** design do contrato REST/GraphQL como produto público — versionamento, paginação, limite de taxa,
depreciação e documentação vão para [15](15-apis.md). O Volume 3 é o **lado de dentro**; o 15 é o **contrato**.

### 04 — Frontend · `FRT`

**É deste volume:** os oito estados de tela, gerenciamento de estado, cache de cliente e invalidação,
composição de componentes, fronteira servidor/cliente, code splitting, carregamento tardio, formulários,
segurança de cliente.

**Não é:** tokens, escalas, tipografia, movimento e catálogo de componentes (→ [09](09-design-system.md)).
Princípios de usabilidade e fluxo (→ [08](08-ux-premium.md)). Escolha de estratégia de renderização
(→ [02](02-arquitetura.md), `SEL`).

### 05 — Banco de Dados · `DAT`

**É deste volume:** modelagem, integridade declarativa, constraints, chaves, índices, planos de execução,
transações, isolamento, migrações, retenção.

**Não é:** normalizar vs desnormalizar como decisão de escala, réplicas, particionamento, sharding
(→ [14](14-escalabilidade.md)). Isolamento por inquilino (→ [16](16-multi-tenant.md)).

### 06 — Segurança · `SEC`

**É deste volume:** OWASP Top 10 completo, criptografia, autenticação e sessão, segredos, dados pessoais,
cadeia de suprimentos, SSRF, níveis progressivos de verificação.

**Não é:** infraestrutura de deploy e política de acesso operacional (→ [10](10-devops.md)). Isolamento de
inquilino, que é decisão de arquitetura com consequência de segurança (→ [16](16-multi-tenant.md), com achados
classificados por este volume).

### 07 — Performance · `PRF`

**É deste volume:** disciplina de medição, o gargalo de hoje, acesso a dados, cache com invalidação declarada,
custo de renderização, limiares, orçamento de performance.

**Não é:** decisões estruturais de crescimento e contrapressão (→ [14](14-escalabilidade.md)). Instrumentação e
dashboards (→ [17](17-observabilidade.md)).

### 08 — UX Premium · `UXI`

**É deste volume:** princípios de usabilidade que produtos de referência aplicam, estados e microinterações,
redação de erro, consistência, fluxos, caminhos infelizes, acessibilidade WCAG 2.2 AA, proteção do trabalho do
usuário.

**Não é:** tokens e componentes concretos (→ [09](09-design-system.md)). Decidir *o que* construir e para quem
(→ [18](18-produto.md)).

### 09 — Design System · `DSY`

**É deste volume:** tokens e sua hierarquia; escalas de cor com contraste garantido; escala de espaçamento;
tipografia; grade; ícones; elevação; raio; movimento e duração; catálogo de componentes com anatomia, variantes
e estados; densidade; tema claro e escuro; versionamento e depreciação de componente; governança de contribuição.

**Não é:** princípios de usabilidade (→ [08](08-ux-premium.md)). Implementação de estado e cache no cliente
(→ [04](04-frontend.md)).

### 10 — DevOps · `OPS`

**É deste volume:** empacotamento, ambientes, CI, CD, estratégias de deploy, compatibilidade durante rollout,
rollback, feature flags, backups e restauração testada, alta disponibilidade, gestão de configuração e
segredos em runtime, resposta a incidente, plantão.

**Não é:** instrumentação, tracing, métricas e dashboards (→ [17](17-observabilidade.md)). Capacidade e
contrapressão (→ [14](14-escalabilidade.md)).

### 11 — QA · `QAT`

**É deste volume:** qualidade do teste, o que merece teste, unidade, integração, contrato, ponta a ponta,
carga, teste de segurança, dados de teste, dublês, testes instáveis, regressão, critérios de aceite.

**Não é:** o veredito de um módulo (→ [12](12-auditoria.md) e [24](24-auditoria-final.md)).

### 12 — Auditoria · `AUD`

**É deste volume:** como revisar um projeto ou módulo do zero, ordem de investigação aplicada, evidência,
detecção de regressão, notas por dimensão, veredito, gestão de backlog e dívida.

**Não é:** revisão de um pull request específico (→ [13](13-revisao-de-codigo.md)). A decisão final de nota 10
(→ [24](24-auditoria-final.md)).

### 13 — Revisão de Código · `REV`

**É deste volume:** revisão de um pull request concreto — o que ler primeiro, como ler um diff, o que só se vê
no diff, tamanho de PR, comentário útil vs ruído, revisão de teste, revisão de migração, revisão de dependência
nova, quando bloquear, como discordar, revisão assistida por IA e seus limites.

**Não é:** auditoria de módulo inteiro (→ [12](12-auditoria.md)).

### 14 — Escalabilidade · `ESC`

**É deste volume:** ordem de intervenção, normalizar vs desnormalizar, réplicas de leitura, particionamento,
sharding, estado que impede escala horizontal, limites de recurso, contrapressão, descarte de carga, disjuntor,
capacidade, custo por unidade.

**Não é:** o gargalo pontual medido hoje (→ [07](07-performance.md)). Isolamento de inquilino
(→ [16](16-multi-tenant.md)).

### 15 — APIs · `API`

**É deste volume:** desenho de contrato como produto — REST, GraphQL, recursos e verbos, formato de erro,
paginação e ordenação, filtragem, versionamento e evolução compatível, depreciação com medição, limite de taxa
publicado, documentação executável, contratos de webhook, SDK e cliente, teste de contrato, política de
compatibilidade.

**Não é:** implementação interna do endpoint, validação e autorização em código (→ [03](03-backend.md)).

### 16 — Multi-Tenant · `MTN`

**É deste volume:** modelos de isolamento e critério de escolha, identificação de inquilino, aplicação do
isolamento no ponto mais interno, migração entre modelos, vizinho ruidoso e cotas, customização por inquilino,
operações por inquilino (exportar, eliminar, restaurar, medir), inquilino grande, provisionamento e
desprovisionamento, faturamento por uso.

**Não é:** as regras genéricas de controle de acesso (→ [06](06-seguranca.md)). Sharding como técnica
(→ [14](14-escalabilidade.md)).

### 17 — Observabilidade · `OBS`

**És deste volume:** log estruturado e níveis, correlação, tracing distribuído, métricas e cardinalidade, as
métricas mínimas por tipo de serviço, SLI, SLO e orçamento de erro, dashboards que respondem perguntas,
alertas acionáveis, ruído de alerta, depuração em produção, retenção e custo de telemetria.

**Não é:** pipeline, deploy e rollback (→ [10](10-devops.md)). Métricas de qualidade de engenharia
(→ [23](23-metricas.md)).

### 18 — Produto · `PRD`

**É deste volume:** enquadrar problema antes de solução, decidir o que **não** construir, escopo mínimo
honesto, critério de sucesso mensurável, priorização de produto, descoberta e validação, escrita de requisito
sem ambiguidade, trade-off entre prazo e dívida, comunicação de mudança ao usuário, encerramento de
funcionalidade.

**Não é:** desenho da interface (→ [08](08-ux-premium.md)). Priorização técnica de achados
(→ [00](00-constituicao-da-engenharia.md)).

### 19 — IA no Produto · `IAX`

**É deste volume:** quando IA é a solução correta e quando é a errada, escolha de modelo, arquitetura de
funcionalidade com IA, RAG e suas falhas, memória e estado de conversa, ferramentas e chamada de função,
agentes e seus limites, avaliação sistemática, alucinação como requisito de projeto, custo e latência, segurança
específica (injeção de prompt, exfiltração), dado do usuário em modelo de terceiro, degradação e fallback,
experiência de usuário de resposta não determinística.

**Não é:** como escrever prompts (→ [20](20-prompt-engineering.md)). Uso de IA para desenvolver o software
(→ [01](01-orquestrador.md) e [20](20-prompt-engineering.md)).

> Este volume é material de referência para a Vire hoje: a decisão registrada em `EOS-004` é que a IA é
> ferramenta de desenvolvimento, não funcionalidade entregue ao usuário. Ele existe para o livro ser completo e
> para o dia em que essa decisão mudar.

### 20 — Prompt Engineering · `PRM`

**É deste volume:** anatomia de um prompt operacional, instrução vs contexto vs exemplo, decomposição em
camadas, por que prompt monolítico degrada, ancoragem em evidência, formato de saída estruturado, sequência
obrigatória, guardas contra deriva de escopo, calibração de recusa, prompts de sistema vs de tarefa,
versionamento e teste de prompt, medição de aderência, antipadrões de prompt.

**Não é:** funcionalidade de IA no produto (→ [19](19-ia-no-produto.md)). Coordenação entre papéis
(→ [01](01-orquestrador.md)).

### 21 — Playbooks · `PLB`

**É deste volume:** a ordem de execução das tarefas recorrentes — CRUD, endpoint, tela, alteração de schema,
integração externa, correção de bug, e os que vierem.

**Não é:** as normas que os passos citam. Playbook referencia, nunca reafirma (`A-001`).

### 22 — Checklists · `CHK`

**É deste volume:** a doutrina de verificação — o que faz um checklist funcionar, por que checklists longos
falham, checklist de leitura vs de confirmação, quando usar, quem assina, e o índice canônico dos checklists
em [`checklists/`](checklists/).

**Não é:** o conteúdo dos checklists de cada domínio, que vive no volume do domínio e em
[`checklists/`](checklists/).

### 23 — Métricas · `MET`

**É deste volume:** como medir qualidade de engenharia, métricas de produto, de código, de processo e de
operação; limiar e reação declarada; métricas que se corrompem ao virar meta; instrumentação da própria
engenharia; nota por dimensão e sua fórmula; tendência vs valor absoluto.

**Não é:** telemetria de produção do sistema (→ [17](17-observabilidade.md)).

### 24 — Auditoria Final · `FIN`

**É deste volume:** o portão final — como decidir se um módulo merece nota 10, quais achados são bloqueantes
sem negociação, verificação de que cada volume aplicável foi de fato aplicado, verificação anti-teatro, o
veredito e sua justificativa, o que fazer quando o auditor discorda do orquestrador, e o registro que fica.

**Não é:** a auditoria em si (→ [12](12-auditoria.md)). Revisão de PR (→ [13](13-revisao-de-codigo.md)).

---

## Regras de fronteira que se aplicam ao livro inteiro

1. **Dentro vs contrato.** Implementação em código fica no volume do domínio; contrato publicado fica no volume
   de contrato. Vale para [03](03-backend.md) vs [15](15-apis.md).
2. **Hoje vs estrutura.** Problema medido agora fica em [07](07-performance.md); decisão estrutural de
   crescimento fica em [14](14-escalabilidade.md).
3. **Princípio vs peça.** Princípio de usabilidade fica em [08](08-ux-premium.md); token e componente ficam em
   [09](09-design-system.md).
4. **Sistema vs engenharia.** Telemetria do produto fica em [17](17-observabilidade.md); medição da qualidade
   do trabalho fica em [23](23-metricas.md).
5. **Escopo de revisão.** PR fica em [13](13-revisao-de-codigo.md); módulo fica em [12](12-auditoria.md);
   veredito final fica em [24](24-auditoria-final.md).
6. **Segurança é transversal.** Qualquer volume pode encontrar achado de segurança, e todos os classificam
   pelas regras de [06](06-seguranca.md). Nenhum outro volume cria norma de segurança própria.
