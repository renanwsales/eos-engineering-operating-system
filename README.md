# EOS — Engineering Operating System

**Manual Operacional de Engenharia para Desenvolvimento Assistido por IA de Sistemas SaaS de Classe Mundial**

Um livro técnico versionado em **25 volumes**, com regras numeradas e citáveis por ID, mais uma cadeia de
**papéis especializados** que trabalham juntos. Não é um prompt: é o manual interno que define como se pensa,
decide, revisa, implementa e valida.

Sumário e fronteiras: [`SUMARIO.md`](SUMARIO.md) · Índice de regras: [`RULES-INDEX.md`](RULES-INDEX.md) ·
Como se escreve neste livro: [`AUTHORING.md`](AUTHORING.md) · Entrada para agentes: [`AGENTS.md`](AGENTS.md)

---

## Por que um livro, e não um prompt

Um prompt longo mistura instruções, objetivos e critérios num só texto. Três consequências práticas:

1. **Diluição.** Quanto mais itens no mesmo bloco, menos peso cada um recebe. A regra 47 é ignorada.
2. **Sem verificação.** Não existe "terminei" verificável: só uma sensação de ter atendido ao pedido.
3. **Impossível de manter.** Mudar uma regra exige reler o texto inteiro e torcer para não contradizer outra.

O EOS separa em camadas, cada uma respondendo a uma pergunta diferente:

| Camada | Pergunta que responde | Onde vive |
| --- | --- | --- |
| **Constituição** | Como pensamos? Em que ordem? O que nunca fazemos? | [`00`](00-constituicao-da-engenharia.md) |
| **Coordenação** | Quem é despachado, em que ordem, com que pergunta? | [`01`](01-orquestrador.md) |
| **Normas técnicas** | O que é certo e errado neste domínio? | volumes `02` a `12`, `17` |
| **Escolhas** | Qual abordagem, entre alternativas legítimas? | [`02` Parte II](02-arquitetura.md), [`14`](14-escalabilidade.md), [`16`](16-multi-tenant.md) |
| **Contratos** | O que prometemos a quem consome? | [`15`](15-apis.md) |
| **Produto** | Isto deveria existir? | [`18`](18-produto.md) |
| **Execução** | Em que ordem eu faço esta tarefa? | [`21`](21-playbooks.md), [`playbooks/`](playbooks/) |
| **Verificação** | Como sei que terminei, e quem assina? | [`13`](13-revisao-de-codigo.md), [`22`](22-checklists.md), [`23`](23-metricas.md), [`24`](24-auditoria-final.md) |
| **Papéis** | Quem analisa o quê, com que profundidade? | [`agents/`](agents/), [`prompts/`](prompts/) |
| **Artefatos** | Como registro o que foi decidido? | [`templates/`](templates/), [`backlog/`](backlog/) |

Cada regra tem **ID estável** (`CON-013`, `SEC-004`, `DAT-019`) e **nível de obrigatoriedade**. Isso permite
citar em revisão, rastrear em relatório, e discutir a divergência de uma regra específica sem renegociar o
framework inteiro. IDs nunca são renumerados nem reciclados (`A-007`).

---

## Os 25 volumes

| # | Volume | Prefixo | Cobre |
| --- | --- | --- | --- |
| 00 | [Constituição da Engenharia](00-constituicao-da-engenharia.md) | `CON` | Princípios, seis portões, ordem de análise, decisão, severidade, priorização, risco, DoD, DoE, ofício |
| 01 | [Orquestrador](01-orquestrador.md) | `ORC` | Como a IA pensa, decide, prioriza, despacha e recusa |
| 02 | [Arquitetura](02-arquitetura.md) | `ARC` `SEL` | Regra de dependência, fronteiras, DDD, integração · **Parte II:** escolha de estilo, síncrono vs assíncrono, renderização, comprar vs construir |
| 03 | [Backend](03-backend.md) | `BAK` | Casos de uso, validação, erros, concorrência, idempotência, filas, workers, webhooks, GraphQL |
| 04 | [Frontend](04-frontend.md) | `FRT` | Oito estados, gerenciamento de estado, cache de cliente, composição, formulários |
| 05 | [Banco de Dados](05-banco-de-dados.md) | `DAT` | Modelagem, integridade declarativa, índices, transações, migrações |
| 06 | [Segurança](06-seguranca.md) | `SEC` | OWASP Top 10, criptografia, sessão, segredos, dados pessoais, níveis de verificação |
| 07 | [Performance](07-performance.md) | `PRF` | Medição, acesso a dados, cache, renderização, limiares |
| 08 | [UX Premium](08-ux-premium.md) | `UXI` | Usabilidade, microinterações, erros, fluxos, caminhos infelizes, WCAG 2.2 AA |
| 09 | [Design System](09-design-system.md) | `DSY` | Tokens, cor, espaçamento, tipografia, movimento, catálogo de componentes, governança |
| 10 | [DevOps](10-devops.md) | `OPS` | CI/CD, deploy, rollback, flags, backups, alta disponibilidade, incidente |
| 11 | [QA](11-qa.md) | `QAT` | Qualidade do teste, unidade, integração, contrato, E2E, regressão, aceite |
| 12 | [Auditoria](12-auditoria.md) | `AUD` | Como revisar um módulo, evidência, regressão, notas, backlog e dívida |
| 13 | [Revisão de Código](13-revisao-de-codigo.md) | `REV` | Revisão de um PR: ordem de leitura, tamanho, comentário útil, quando bloquear |
| 14 | [Escalabilidade](14-escalabilidade.md) | `ESC` | Ordem de intervenção, réplicas, particionamento, sharding, contrapressão, capacidade |
| 15 | [APIs](15-apis.md) | `API` | Contrato como produto: recursos, erros, paginação, versionamento, depreciação, limites |
| 16 | [Multi-Tenant](16-multi-tenant.md) | `MTN` | Isolamento, identificação, cotas, customização, operações e faturamento por inquilino |
| 17 | [Observabilidade](17-observabilidade.md) | `OBS` | Log, correlação, tracing, métricas, SLO, alerta acionável, custo de telemetria |
| 18 | [Produto](18-produto.md) | `PRD` | Enquadrar problema, decidir o que não construir, critério de sucesso, requisito sem ambiguidade |
| 19 | [IA no Produto](19-ia-no-produto.md) | `IAX` | Quando IA é a solução errada, RAG, memória, ferramentas, avaliação, injeção de prompt |
| 20 | [Prompt Engineering](20-prompt-engineering.md) | `PRM` | Anatomia de prompt, camadas, formato de saída, versionamento e teste de prompt |
| 21 | [Playbooks](21-playbooks.md) | `PLB` | CRUD, endpoint, tela, schema, integração externa, correção de bug |
| 22 | [Checklists](22-checklists.md) | `CHK` | Doutrina de verificação: por que listas longas falham, item bem escrito, quem assina |
| 23 | [Métricas](23-metricas.md) | `MET` | Como medir qualidade, limiar e reação, lei de Goodhart, nota por dimensão |
| 24 | [Auditoria Final](24-auditoria-final.md) | `FIN` | O portão final, verificação anti-teatro, o que separa 8 de 10, o veredito |

A contagem exata de regras por volume está em [`RULES-INDEX.md`](RULES-INDEX.md), que é gerado por script.
Se um volume e o índice divergirem, **o volume** é a fonte de verdade.

### Como os volumes se relacionam

Seis regras de fronteira governam o livro inteiro e estão em [`SUMARIO.md`](SUMARIO.md). As duas que mais
importam no dia a dia:

- **Dentro vs contrato.** Implementação de endpoint é o Volume 03; o contrato publicado é o Volume 15.
- **Hoje vs estrutura.** O gargalo medido agora é o Volume 07; a decisão de crescimento é o Volume 14.

---

## A cadeia de papéis

Cada papel tem missão, sequência obrigatória, normas próprias, `overrides` declarados do contrato comum,
formato de saída, e uma seção explícita de **o que não é da sua conta** — que é o que evita relatórios
redundantes e inflação de escopo.

| # | Papel | Pergunta que ele responde | Volumes |
| --- | --- | --- | --- |
| 00 | [Orquestrador](agents/00-orchestrator.md) | O que importa agora, quem faz, e isso está aprovado? | 01, 00 |
| 01 | [Arquiteto](agents/01-architect.md) | As fronteiras estão certas e o domínio permite estado inválido? | 02, 16 |
| 02 | [Backend](agents/02-backend.md) | As regras valem em **todos** os caminhos, sob toda entrada e concorrência? | 03, 15 |
| 03 | [Frontend](agents/03-frontend.md) | A interface diz a verdade sobre o estado, inclusive quando falha? | 04, 09 |
| 04 | [Database](agents/04-database.md) | O schema garante as invariantes por si mesmo? | 05, 14 |
| 05 | [Security](agents/05-security.md) | Onde alguém faz algo que não deveria? | 06, 16 |
| 06 | [Performance](agents/06-performance.md) | Onde está o gargalo **medido**, e ele viola um limiar? | 07, 14 |
| 07 | [QA](agents/07-qa.md) | Os testes existentes pegariam as falhas que importam? | 11 |
| 08 | [DevOps/SRE](agents/08-devops-sre.md) | Quanto tempo até sabermos, e quanto até voltarmos? | 10, 17 |
| 09 | [Product/UX](agents/09-product-ux.md) | Os fluxos fazem o que o usuário quer, e são consistentes? | 08, 18 |
| 10 | [Auditor Final](agents/10-final-auditor.md) | O que foi afirmado é verdade, e o que regrediu? | 12, 13, 24 |

Contrato herdado por todos: [`agents/_shared/core-contract.md`](agents/_shared/core-contract.md) ·
[`agents/_shared/output-schemas.md`](agents/_shared/output-schemas.md). Biblioteca completa de prompts,
incluindo os prompts por volume: [`prompts/`](prompts/).

---

## Como usar

### 1. Repositório de contexto (recomendado)

Aponte o agente para [`AGENTS.md`](AGENTS.md). Ele é o roteador: define os não negociáveis e a ordem de carga
por tipo de tarefa. O agente carrega **só** os volumes que a tarefa exige — carregar os vinte e cinco para
tudo dilui as instruções que importam (`ORC-005`).

### 2. Prompt único compilado

Quando a ferramenta aceita apenas um system prompt: [`dist/system-prompt.md`](dist/system-prompt.md). Mantém
processo, portões e classificação; **omite** as normas detalhadas por domínio. É a versão reduzida, e sabê-lo
importa.

### 3. Pipeline multiagente

Um papel por chamada, com o orquestrador integrando. É o modo de maior qualidade e maior custo. Runbooks:

- [Revisão completa de módulo](runbooks/revisao-completa-de-modulo.md) — a cadeia inteira, em três ondas.
- [Ciclo de mudança única](runbooks/ciclo-de-mudanca-unica.md) — o dia a dia, um papel, portões comprimidos.

---

## Primeiro passo obrigatório

Preencher [`templates/perfil-do-projeto.md`](templates/perfil-do-projeto.md).

O núcleo do EOS é **agnóstico de stack**. O perfil é onde vivem os comandos reais, as convenções, o glossário
do domínio, a classificação de criticidade por módulo, os limiares de métrica e a tolerância a risco. Sem ele,
o agente aplica limiares padrão que podem não fazer sentido no seu contexto — e recomenda o que já existe.

Está registrado como [`EOS-001`](backlog/BACKLOG.md), severidade `S1`.

---

## Estrutura

```
SUMARIO.md                 Sumário e fronteira normativa de cada volume
AUTHORING.md               Contrato de autoria: como se escreve e revisa um volume
AGENTS.md                  Roteador para agentes: não negociáveis e ordem de carga
RULES-INDEX.md             Índice gerado de todas as regras, com nível e severidade

00-*.md a 24-*.md          Os 25 volumes (PT) — fonte de verdade das normas
agents/                    Prompts de papel (EN) + contrato e schemas compartilhados
prompts/                   Biblioteca de prompts: por papel e por volume
playbooks/                 Índice das tarefas recorrentes (o conteúdo vive no Volume 21)
checklists/                Portões acionáveis (PT)
templates/                 Perfil do projeto, ADR, proposta de mudança, relatório, backlog
examples/                  Exemplos de implementação citados pelos volumes
diagrams/                  Diagramas referenciados pelos volumes
runbooks/                  Fluxos operacionais multiagente
backlog/                   BACKLOG.md + adr/ (decisões registradas, incluindo as recusadas)
scripts/                   build-rules-index.py, check-links.py — verificação automatizada
dist/                      system-prompt.md (versão compilada, reduzida)
```

**Idioma:** volumes, checklists e templates em português; prompts e schemas de saída em inglês (`A-015`).

---

## Verificação

O próprio repositório é verificável — coerente com a regra de que métrica sem reação é decoração (`CON-050`):

```bash
python3 scripts/build-rules-index.py --check   # numeração contínua por prefixo, índice em dia
python3 scripts/check-links.py                 # links, âncoras e IDs de regra citados
```

`check-links.py` valida as **referências cruzadas entre regras**: citar um ID que não existe em nenhum volume
falha o check, o que impede referências mortas espalhadas. O que ele não valida é se o ID citado *significa* o
que o texto afirma — isso é responsabilidade do autor (`A-013`).

---

## Versionamento

Versionamento semântico, com as regras completas em [`AUTHORING.md`](AUTHORING.md) seção 7. Mudança em regra
`[IMUTÁVEL]` é `MAJOR` e exige ADR. Adição de regra ou volume é `MINOR`. Correção de texto é `PATCH`.

IDs de regra são **estáveis**: uma regra revogada deixa o número aposentado, nunca reaproveitado, para que
relatórios e ADRs antigos continuem legíveis.

Versão atual: **3.0.0** — reestruturação como livro de 25 volumes, com contrato de autoria e sumário de
fronteiras. Histórico das decisões em [`backlog/adr/`](backlog/adr/).
