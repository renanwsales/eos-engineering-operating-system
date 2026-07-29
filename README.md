# EOS — Engineering Operating System

Especificação operacional de engenharia para agentes de IA e times humanos. **735 regras técnicas
numeradas** em **15 volumes**, mais uma cadeia de **11 papéis especializados** que trabalham juntos.

Não é um prompt. É o manual interno que define **como se pensa, decide, revisa, implementa e valida** —
reutilizável em qualquer módulo, de qualquer projeto.

---

## Por que não um prompt único

Um prompt longo mistura instruções, objetivos e critérios num só texto. Três consequências práticas:

1. **Diluição.** Quanto mais itens no mesmo bloco, menos peso cada um recebe. A regra 47 é ignorada.
2. **Sem verificação.** Não existe "terminei" verificável: só uma sensação de ter atendido ao pedido.
3. **Impossível de manter.** Mudar uma regra exige reler o texto inteiro e torcer para não contradizer outra.

O EOS separa em camadas, cada uma respondendo a uma pergunta diferente:

| Camada | Pergunta que responde | Onde vive |
| --- | --- | --- |
| **Constituição** | Como pensamos? Em que ordem? O que nunca fazemos? | [`volumes/vol-01`](00-constituicao-da-engenharia.md) |
| **Normas técnicas** | O que é certo e errado neste domínio? | [`volumes/vol-02` a `vol-11`](volumes/) |
| **Escolhas** | Qual abordagem, entre alternativas legítimas? | [`vol-13`](02-arquitetura.md), [`vol-14`](14-escalabilidade.md) |
| **Execução** | Em que ordem eu faço esta tarefa? | [`vol-15`](21-playbooks.md) |
| **Papéis** | Quem analisa o quê, com que profundidade? | [`agents/`](agents/) |
| **Coordenação** | Quem é despachado, em que ordem, com que pergunta? | [`volumes/vol-12`](01-orquestrador.md) |
| **Portões e provas** | Como sei que terminei? | [`checklists/`](checklists/) |
| **Artefatos** | Como registro o que foi decidido? | [`templates/`](templates/), [`backlog/`](backlog/) |
| **Índice** | Onde está a regra `SEC-004`? | [`RULES-INDEX.md`](RULES-INDEX.md) |

Cada regra tem **ID estável** (`CON-013`, `SEC-004`, `DAT-019`) e **nível de obrigatoriedade**. Isso permite
citar em revisão, rastrear em relatório, e discutir a divergência de uma regra específica sem renegociar o
framework inteiro.

---

## Os 15 volumes

| Vol | Título | Prefixo | Regras | Cobre |
| --- | --- | --- | --- | --- |
| 📘 01 | [Constituição da Engenharia](00-constituicao-da-engenharia.md) | `CON` | 86 | Princípios, seis portões, ordem de análise, decisão, severidade, priorização, risco, DoD, DoE, métricas, ofício |
| 📗 02 | [Arquitetura](02-arquitetura.md) | `ARC` | 40 | Clean Architecture, DDD, modularização, integração entre módulos |
| 📙 03 | [Backend](03-backend.md) | `BAK` | 73 | APIs, regras de negócio, autorização, erros, webhooks, GraphQL, trabalho agendado |
| 📕 04 | [Frontend](04-frontend.md) | `FRT` | 42 | Estados, gerenciamento de estado, componentes, design system |
| 📓 05 | [Segurança e DevSecOps](06-seguranca.md) | `SEC` | 66 | OWASP Top 10, segredos, criptografia, permissões, dados pessoais, níveis de verificação |
| 📒 06 | [Banco de Dados](05-banco-de-dados.md) | `DAT` | 40 | Modelagem, integridade, índices, transações, migrações |
| 📔 07 | [Performance](07-performance.md) | `PRF` | 38 | Medição, acesso a dados, cache, renderização, limiares |
| 📘 08 | [UX/UI Premium](08-ux-premium.md) | `UXI` | 55 | Estados, microinterações, erros, consistência, fluxos, WCAG 2.2 AA |
| 📗 09 | [QA e Testes](11-qa.md) | `QAT` | 40 | Qualidade do teste, cobertura de negócio, regressão, aceite |
| 📙 10 | [DevOps e SRE](10-devops.md) | `OPS` | 48 | Rollback, compatibilidade de deploy, observabilidade, CI/CD, backups, HA |
| 📕 11 | [Auditoria Técnica](12-auditoria.md) | `AUD` | 42 | Code review, regressões, notas, veredito, backlog |
| 📓 12 | [Orquestrador Mestre](01-orquestrador.md) | `ORC` | 32 | Cadeia de agentes, despacho, integração, aprovação |
| 📔 13 | [Seleção de Arquitetura](02-arquitetura.md) | `SEL` | 33 | Estilos, monólito vs serviços, CQRS, síncrono vs assíncrono, renderização, comprar vs construir |
| 📒 14 | [Escala e Multi-Inquilino](14-escalabilidade.md) | `ESC` | 42 | Normalização, réplicas, particionamento, sharding, contrapressão, isolamento de inquilino |
| 📕 15 | [Playbooks](21-playbooks.md) | `PLB` | 58 | CRUD, endpoint, tela, schema, integração externa, correção de bug |

Os volumes 01 a 12 dizem **o que é certo**. Os volumes 13 e 14 tratam de **escolher entre alternativas
legítimas** — a pergunta que uma norma não responde. O volume 15 diz **em que ordem executar** as tarefas que
se repetem toda semana.

Índice completo pesquisável: [`RULES-INDEX.md`](RULES-INDEX.md).

---

## A cadeia de 11 papéis

Cada papel tem missão, sequência obrigatória, normas próprias, `overrides` declarados do contrato comum,
formato de saída, e uma seção explícita de **o que não é da sua conta** — que é o que evita relatórios
redundantes e inflação de escopo.

| # | Papel | Pergunta que ele responde | Volume |
| --- | --- | --- | --- |
| 00 | [Orquestrador](agents/00-orchestrator.md) | O que importa agora, quem faz, e isso está aprovado? | 12 |
| 01 | [Arquiteto](agents/01-architect.md) | As fronteiras estão certas e o domínio permite estado inválido? | 2 |
| 02 | [Backend](agents/02-backend.md) | As regras valem em **todos** os caminhos, sob toda entrada e concorrência? | 3 |
| 03 | [Frontend](agents/03-frontend.md) | A interface diz a verdade sobre o estado, inclusive quando falha? | 4 |
| 04 | [Database](agents/04-database.md) | O schema garante as invariantes por si mesmo? | 6 |
| 05 | [Security](agents/05-security.md) | Onde alguém faz algo que não deveria? | 5 |
| 06 | [Performance](agents/06-performance.md) | Onde está o gargalo **medido**, e ele viola um limiar? | 7 |
| 07 | [QA](agents/07-qa.md) | Os testes existentes pegariam as falhas que importam? | 9 |
| 08 | [DevOps/SRE](agents/08-devops-sre.md) | Quanto tempo até sabermos, e quanto até voltarmos? | 10 |
| 09 | [Product/UX](agents/09-product-ux.md) | Os fluxos fazem o que o usuário quer, e são consistentes? | 8 |
| 10 | [Auditor Final](agents/10-final-auditor.md) | O que foi afirmado é verdade, e o que regrediu? | 11 |

Contrato herdado por todos: [`agents/_shared/core-contract.md`](agents/_shared/core-contract.md) ·
[`agents/_shared/output-schemas.md`](agents/_shared/output-schemas.md).

---

## Como usar

### 1. Repositório de contexto (recomendado)

Aponte o agente para [`AGENTS.md`](AGENTS.md). Ele é o roteador: define os não negociáveis e a ordem de
carga por tipo de tarefa. O agente carrega **só** os volumes que a tarefa exige — carregar os doze para
tudo dilui as instruções que importam (ORC-005).

### 2. Prompt único compilado

Quando a ferramenta aceita apenas um system prompt: [`dist/system-prompt.md`](dist/system-prompt.md).
Mantém processo, portões e classificação; **omite** as normas detalhadas por domínio. É a versão reduzida,
e sabê-lo importa.

### 3. Pipeline multiagente

Um papel por chamada, com o orquestrador integrando. É o modo de maior qualidade e maior custo. Runbooks:

- [Revisão completa de módulo](runbooks/revisao-completa-de-modulo.md) — a cadeia inteira, em três ondas.
- [Ciclo de mudança única](runbooks/ciclo-de-mudanca-unica.md) — o dia a dia, um papel, portões comprimidos.

---

## Primeiro passo obrigatório

Preencher [`templates/perfil-do-projeto.md`](templates/perfil-do-projeto.md).

O núcleo do EOS é **agnóstico de stack**. O perfil é onde vivem os comandos reais, as convenções, o
glossário do domínio, a classificação de criticidade por módulo, os limiares de métrica e a tolerância a
risco. Sem ele, o agente aplica limiares padrão que podem não fazer sentido no seu contexto — e recomenda
o que já existe.

Está registrado como [`EOS-001`](backlog/BACKLOG.md), severidade `S1`.

---

## Estrutura

```
AGENTS.md                  Roteador para agentes: não negociáveis e ordem de carga
RULES-INDEX.md             Índice gerado das 735 regras, com nível e severidade

volumes/                   Os 15 volumes (PT) — fonte de verdade das normas
agents/                    11 prompts de papel (EN) + contrato e schemas compartilhados
checklists/                Portões acionáveis (PT): pré-análise, review, pré-merge, OWASP,
                           performance, acessibilidade, módulo concluído
templates/                 Perfil do projeto, ADR, proposta de mudança, relatório de
                           auditoria, entrada de backlog
runbooks/                  Fluxos operacionais multiagente
backlog/                   BACKLOG.md + adr/ (decisões registradas)
scripts/                   build-rules-index.py, check-links.py — verificação automatizada
dist/                      system-prompt.md (versão compilada, reduzida)
```

**Idioma:** volumes, checklists e templates em português; prompts de papel e schemas de saída em inglês.
Os schemas são contratos consumidos por máquina e ficam em inglês para casar com a terminologia das
ferramentas.

---

## Verificação

O próprio repositório é verificável — coerente com a regra de que métrica sem reação é decoração (CON-050):

```bash
python3 scripts/build-rules-index.py --check   # numeração contínua, índice em dia
python3 scripts/check-links.py                 # links, âncoras e IDs de regra citados
```

`check-links.py` valida também as **referências cruzadas entre regras**: citar um ID que não existe em nenhum
volume falha o check, o que impede que uma renumeração deixe referências mortas espalhadas.

---

## Versionamento

Versionamento semântico. Mudança em regra `[IMUTÁVEL]` é `MAJOR` e exige ADR. Adição de regra é `MINOR`.
Correção de texto é `PATCH`.

IDs de regra são **estáveis**: uma regra removida deixa o número aposentado, nunca reaproveitado, para que
relatórios antigos continuem legíveis.

Versão atual: **2.1.0** — volumes 13 a 15 (seleção, escala, playbooks) e capítulos de webhooks,
GraphQL, trabalho agendado e níveis de verificação de segurança.
Decisão de adoção: [`ADR-0001`](backlog/adr/0001-adocao-do-eos.md).
