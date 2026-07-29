# EOS — Engineering Operating System

Um **manual operacional de engenharia** executável por IA. Não é um prompt: é uma
especificação de como pensar, decidir, mudar e validar software.

A premissa do EOS é que prompts longos falham porque misturam instruções, objetivos e
critérios num único texto. O EOS separa essas três coisas:

| Camada | Pergunta que responde | Onde vive |
| --- | --- | --- |
| **Filosofia e processo** | Como pensamos? Em que ordem? | [`manual/`](manual/) |
| **Normas técnicas** | O que é certo e errado neste código? | [`standards/`](standards/) |
| **Papéis** | Quem analisa o quê, com que profundidade? | [`agents/`](agents/) |
| **Portões e provas** | Como sei que terminei? | [`checklists/`](checklists/) |
| **Artefatos** | Como registro o que foi decidido? | [`templates/`](templates/), [`backlog/`](backlog/) |

Idioma: o **manual e as normas estão em português** (para a equipe ler e discutir); os
**prompts dos agentes estão em inglês** (melhor aderência dos modelos e reuso).

---

## Por que isso funciona melhor do que um prompt gigante

Um prompt único diz "melhore tudo". O EOS impõe cinco restrições que mudam o
comportamento do modelo:

1. **Ordem obrigatória de análise.** Arquitetura → domínio → segurança → dados →
   performance → UX/A11y → testes → deploy. Ninguém opina sobre nomes de variáveis antes
   de entender o domínio.
2. **Regra da evidência.** Nenhuma afirmação sem `arquivo:linha` ou saída de comando.
   Suspeita sem prova é registrada como hipótese, não como achado.
3. **Protocolo de decisão.** Toda mudança não trivial exige ≥2 alternativas comparadas
   por custo, risco, reversibilidade e retorno — antes de editar qualquer arquivo.
4. **Proibição de refatoração cosmética.** Mudança sem defeito, risco ou métrica
   associada é rejeitada, não importa quão "mais limpa" seja.
5. **Portão de validação.** Cada alteração é validada isoladamente antes da próxima.
   Sem validação, a mudança não existe.

E duas separações que evitam o maior desperdício de tempo em revisões:

- **`MUST-FIX` vs `OPPORTUNITY`** — o que bloqueia entrega versus o que entra no backlog.
- **Definition of Done vs Definition of Excellence** — o mínimo aceitável versus o alvo.

---

## Como usar

### Opção A — Como repositório de contexto (recomendado)

Copie a pasta para dentro do seu projeto (ou adicione como submódulo) em `.eos/`. O
arquivo [`AGENTS.md`](AGENTS.md) é lido automaticamente por Cursor e agentes compatíveis
e funciona como roteador: ele diz ao agente quais documentos carregar para cada tipo de
tarefa.

```bash
git submodule add <url-deste-repo> .eos
cp .eos/AGENTS.md ./AGENTS.md   # ajuste os caminhos para .eos/
```

Primeiro passo obrigatório em um projeto novo: preencher
[`templates/perfil-do-projeto.md`](templates/perfil-do-projeto.md). O EOS é agnóstico de
stack; o perfil é onde a stack real entra.

### Opção B — Prompt único compilado

Para ferramentas que aceitam apenas um system prompt, use
[`dist/system-prompt.md`](dist/system-prompt.md). É a versão condensada do núcleo —
perde a profundidade das normas, mantém o processo e os portões.

### Opção C — Pipeline multiagente

Para revisão completa de um módulo, siga
[`runbooks/revisao-completa-de-modulo.md`](runbooks/revisao-completa-de-modulo.md): o
orquestrador distribui o trabalho para os 9 especialistas e o auditor final atribui notas
e detecta regressões.

---

## Mapa dos documentos

### Manual — como pensamos (PT)

| Documento | Conteúdo |
| --- | --- |
| [01 — Filosofia de engenharia](manual/01-filosofia-de-engenharia.md) | Princípios não negociáveis e o que fazer quando eles colidem |
| [02 — Processo de engenharia](manual/02-processo-de-engenharia.md) | Os 6 portões: G0 descoberta → G5 auditoria |
| [03 — Ordem de análise](manual/03-ordem-de-analise.md) | As 8 camadas, o que procurar em cada uma e quando parar |
| [04 — Tomada de decisão](manual/04-tomada-de-decisao.md) | Comparação de alternativas, reversibilidade, quando não decidir |
| [05 — Classificação de problemas](manual/05-classificacao-de-problemas.md) | Severidade S0–S3, confiança, esforço, `MUST-FIX` vs `OPPORTUNITY` |
| [06 — Matriz de priorização](manual/06-matriz-de-priorizacao.md) | Score de prioridade e regras de desempate |
| [07 — Matriz de risco](manual/07-matriz-de-risco.md) | Probabilidade × impacto e mitigação obrigatória por faixa |
| [08 — Definition of Done](manual/08-definition-of-done.md) | O mínimo para uma mudança existir |
| [09 — Definition of Excellence](manual/09-definition-of-excellence.md) | O alvo para um módulo ser considerado maduro |
| [10 — Métricas de qualidade](manual/10-metricas-de-qualidade.md) | O que medimos, limiares e como reagimos |
| [11 — Processo de revisão](manual/11-processo-de-revisao.md) | Code review, tamanho de PR, orçamento de mudança |
| [12 — Gestão de backlog](manual/12-gestao-de-backlog.md) | Como o produto continua vivo entre entregas |

### Standards — o que é certo e errado (PT)

[Arquitetura](standards/arquitetura.md) · [Código e nomenclatura](standards/codigo-e-nomenclatura.md) ·
[API](standards/api.md) · [Banco de dados](standards/banco-de-dados.md) ·
[Segurança](standards/seguranca.md) · [Performance](standards/performance.md) ·
[Acessibilidade](standards/acessibilidade.md) · [UX/UI](standards/ux-ui.md) ·
[Testes](standards/testes.md) · [Observabilidade](standards/observabilidade.md)

### Agentes — quem faz o quê (EN)

O [contrato compartilhado](agents/_shared/core-contract.md) e os
[schemas de saída](agents/_shared/output-schemas.md) são herdados por todos.

| # | Papel | Escopo |
| --- | --- | --- |
| 00 | [Orchestrator](agents/00-orchestrator.md) | Prioriza, distribui, aprova e integra |
| 01 | [Architect](agents/01-architect.md) | Fronteiras, acoplamento, modelagem de domínio |
| 02 | [Backend](agents/02-backend.md) | APIs, regras de negócio, autenticação, resiliência |
| 03 | [Frontend](agents/03-frontend.md) | Componentes, estado, renderização, bundle |
| 04 | [Database](agents/04-database.md) | Modelagem, índices, migrações, consultas |
| 05 | [Security](agents/05-security.md) | OWASP Top 10, autorização, segredos, supply chain |
| 06 | [QA](agents/06-qa.md) | Estratégia de testes, casos de borda, regressão |
| 07 | [DevOps/SRE](agents/07-devops-sre.md) | CI/CD, observabilidade, deploy, recuperação |
| 08 | [Product/UX](agents/08-product-ux.md) | Fluxos, consistência, acessibilidade, conteúdo |
| 09 | [Final Auditor](agents/09-final-auditor.md) | Regressões, notas, veto de entrega |

### Checklists e templates

[Pré-análise](checklists/pre-analise.md) · [Code review](checklists/code-review.md) ·
[Pré-merge](checklists/pre-merge.md) · [Performance](checklists/performance.md) ·
[Acessibilidade](checklists/acessibilidade.md) · [Segurança OWASP](checklists/seguranca-owasp.md) ·
[Módulo concluído](checklists/modulo-concluido.md)

[ADR](templates/adr.md) · [Proposta de mudança](templates/proposta-de-mudanca.md) ·
[Relatório de auditoria](templates/relatorio-de-auditoria.md) ·
[Entrada de backlog](templates/entrada-de-backlog.md) ·
[Perfil do projeto](templates/perfil-do-projeto.md)

---

## Princípio que resume tudo

> Nenhuma linha de código muda sem um motivo declarado, uma alternativa descartada e uma
> prova de que funcionou.

---

## Versionamento

O EOS é versionado semanticamente. Mudanças em normas que invalidam código existente são
**MAJOR** e exigem ADR em [`backlog/adr/`](backlog/adr/). Versão atual: **1.0.0**.
