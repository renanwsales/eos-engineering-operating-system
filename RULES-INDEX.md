# RULES-INDEX — índice de regras do EOS

**1391 regras** em 25 volumes. Este arquivo é **gerado** por
`scripts/build-rules-index.py`; não edite à mão. Se um volume e este índice divergirem,
**o volume** é a fonte de verdade.

Sumário e fronteiras dos volumes: [`SUMARIO.md`](SUMARIO.md) ·
contrato de autoria: [`AUTHORING.md`](AUTHORING.md)

## Como citar uma regra

Sempre pelo ID: `SEC-004`, `CON-013`, `DAT-019`. IDs são **estáveis** — uma regra removida
deixa o número aposentado, nunca reaproveitado, para que relatórios antigos continuem legíveis.

## Obrigatoriedade

| Nível | Significado | Divergir exige |
| --- | --- | --- |
| `[IMUTÁVEL]` | Núcleo do framework | Decisão do dono do produto + ADR. É mudança `MAJOR` do EOS |
| `[OBRIGATÓRIA]` | Violação é achado, com severidade | ADR registrando a divergência (ARC-037) |
| `[RECOMENDADA]` | Padrão esperado; exceção é normal | Justificativa no momento, sem ADR |
| `[REVOGADA]` | Não vale mais; o número fica aposentado | — |

Distribuição: **133 imutáveis** · **1051 obrigatórias** · **207 recomendadas**.

## Volumes

| Vol | Título | Prefixo | Regras |
| --- | --- | --- | --- |
| 00 | [Constituição da Engenharia](00-constituicao-da-engenharia.md) | `CON` | 86 |
| 01 | [Orquestrador Mestre](01-orquestrador.md) | `ORC` | 32 |
| 02 | [Framework de Arquitetura](02-arquitetura.md) | `ARC` `SEL` | 73 |
| 03 | [Framework Backend](03-backend.md) | `BAK` | 73 |
| 04 | [Framework Frontend](04-frontend.md) | `FRT` | 42 |
| 05 | [Framework de Banco de Dados](05-banco-de-dados.md) | `DAT` | 40 |
| 06 | [Segurança e DevSecOps](06-seguranca.md) | `SEC` | 66 |
| 07 | [Framework de Performance](07-performance.md) | `PRF` | 38 |
| 08 | [UX/UI Premium](08-ux-premium.md) | `UXI` | 55 |
| 09 | [Design System](09-design-system.md) | `DSY` | 69 |
| 10 | [DevOps e SRE](10-devops.md) | `OPS` | 48 |
| 11 | [QA e Testes](11-qa.md) | `QAT` | 40 |
| 12 | [Auditoria Técnica](12-auditoria.md) | `AUD` | 42 |
| 13 | [Revisão de Código](13-revisao-de-codigo.md) | `REV` | 58 |
| 14 | [Escala e Multi-Inquilino](14-escalabilidade.md) | `ESC` | 42 |
| 15 | [APIs](15-apis.md) | `API` | 58 |
| 16 | [Multi-Tenant](16-multi-tenant.md) | `MTN` | 58 |
| 17 | [Observabilidade](17-observabilidade.md) | `OBS` | 70 |
| 18 | [Produto](18-produto.md) | `PRD` | 58 |
| 19 | [IA no Produto](19-ia-no-produto.md) | `IAX` | 69 |
| 20 | [Prompt Engineering](20-prompt-engineering.md) | `PRM` | 58 |
| 21 | [Playbooks](21-playbooks.md) | `PLB` | 58 |
| 22 | [Checklists](22-checklists.md) | `CHK` | 48 |
| 23 | [Métricas](23-metricas.md) | `MET` | 58 |
| 24 | [Auditoria Final](24-auditoria-final.md) | `FIN` | 52 |
| | **Total** | | **1391** |

---

## 📘 Volume 00 — Constituição da Engenharia

Arquivo: [`00-constituicao-da-engenharia.md`](00-constituicao-da-engenharia.md) · 86 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `CON-001` | Correção antes de elegância | IMUT | — | Princípios |
| `CON-002` | O código existente tem razões | IMUT | — | Princípios |
| `CON-003` | Mudança é custo, não progresso | IMUT | — | Princípios |
| `CON-004` | Duplicação é mais barata que a abstração errada | IMUT | — | Princípios |
| `CON-005` | Explícito vence esperto | IMUT | — | Princípios |
| `CON-006` | Sem medição não há performance | IMUT | — | Princípios |
| `CON-007` | Segurança e dados não têm zona cinzenta | IMUT | — | Princípios |
| `CON-008` | O produto está vivo | IMUT | — | Princípios |
| `CON-009` | Regra da evidência | IMUT | — | Regras imutáveis de conduta |
| `CON-010` | Confiança declarada | IMUT | — | Regras imutáveis de conduta |
| `CON-011` | Ordem obrigatória de análise | IMUT | — | Regras imutáveis de conduta |
| `CON-012` | Protocolo de decisão | IMUT | — | Regras imutáveis de conduta |
| `CON-013` | Proibição de refatoração cosmética | IMUT | — | Regras imutáveis de conduta |
| `CON-014` | Portão de validação | IMUT | — | Regras imutáveis de conduta |
| `CON-015` | Um concern por commit | IMUT | — | Regras imutáveis de conduta |
| `CON-016` | Menor mudança reversível | IMUT | — | Regras imutáveis de conduta |
| `CON-017` | Justificativa de quatro campos | IMUT | — | Regras imutáveis de conduta |
| `CON-018` | Separação obrigatória de listas | IMUT | — | Regras imutáveis de conduta |
| `CON-019` | Nada morre no chat | IMUT | — | Regras imutáveis de conduta |
| `CON-020` | Declare o não verificado | IMUT | — | Regras imutáveis de conduta |
| `CON-021` | Ordem lexicográfica de prioridade | IMUT | — | Regra de desempate |
| `CON-022` | O que rejeitamos explicitamente | IMUT | — | Regra de desempate |
| `CON-056` | O trabalho avança por portões | IMUT | — | Processo: os seis portões |
| `CON-057` | G0 Descoberta: entender antes de julgar | OBRIG | — | Processo: os seis portões |
| `CON-058` | G1 Diagnóstico: achados com evidência | OBRIG | — | Processo: os seis portões |
| `CON-059` | G2 Decisão: alternativa descartada registrada | OBRIG | — | Processo: os seis portões |
| `CON-060` | G3 Implementação: a menor mudança reversível | OBRIG | — | Processo: os seis portões |
| `CON-061` | G4 Validação: nunca comprimida | IMUT | — | Processo: os seis portões |
| `CON-062` | G5 Auditoria: o conjunto, não a peça | OBRIG | — | Processo: os seis portões |
| `CON-063` | Compressão de portões | OBRIG | — | Processo: os seis portões |
| `CON-064` | Voltar atrás é o comportamento correto | OBRIG | — | Processo: os seis portões |
| `CON-023` | As oito camadas | IMUT | — | Ordem de análise |
| `CON-024` | Regra de avanço | OBRIG | — | Ordem de análise |
| `CON-025` | Regra de parada | OBRIG | — | Ordem de análise |
| `CON-026` | O que procurar em cada camada | OBRIG | — | Ordem de análise |
| `CON-027` | Registro do percurso | OBRIG | — | Ordem de análise |
| `CON-028` | Enuncie o problema como restrição | OBRIG | — | Tomada de decisão |
| `CON-029` | A opção zero é obrigatória | OBRIG | — | Tomada de decisão |
| `CON-030` | Alternativas reais | OBRIG | — | Tomada de decisão |
| `CON-031` | Seis dimensões de comparação | OBRIG | — | Tomada de decisão |
| `CON-032` | Declare a troca aceita | OBRIG | — | Tomada de decisão |
| `CON-033` | Declare a condição de invalidação | OBRIG | — | Tomada de decisão |
| `CON-034` | Registre no nível adequado | OBRIG | — | Tomada de decisão |
| `CON-035` | Postergar é decisão, e se registra | OBRIG | — | Tomada de decisão |
| `CON-036` | Severidade mede consequência | IMUT | — | Classificação e priorização |
| `CON-037` | Esforço e risco de correção | OBRIG | — | Classificação e priorização |
| `CON-038` | `MUST-FIX` versus `OPPORTUNITY` | IMUT | — | Classificação e priorização |
| `CON-039` | Score de prioridade | OBRIG | — | Classificação e priorização |
| `CON-040` | Orçamento da rodada | OBRIG | — | Classificação e priorização |
| `CON-041` | Faixas e mitigação obrigatória | IMUT | — | Matriz de risco de execução |
| `CON-042` | Riscos que não aparecem no diff | OBRIG | — | Matriz de risco de execução |
| `CON-043` | DoD é obrigatória e verificada item a item | IMUT | — | Definition of Done |
| `CON-044` | Redução de DoD apenas em `S0` de produção | OBRIG | — | Definition of Done |
| `CON-045` | O teste das 3h da manhã | OBRIG | — | Definition of Done |
| `CON-046` | Excelência é deliberada e por módulo | OBRIG | — | Definition of Excellence |
| `CON-047` | As oito marcas de excelência | OBRIG | — | Definition of Excellence |
| `CON-048` | Suba um degrau por rodada | OBRIG | — | Definition of Excellence |
| `CON-049` | O critério único de excelência | IMUT | — | Definition of Excellence |
| `CON-050` | Métrica sem reação é decoração | OBRIG | — | Métricas e limiares |
| `CON-051` | Métricas de manutenibilidade não justificam mudança | IMUT | — | Métricas e limiares |
| `CON-052` | Pesos da nota final | OBRIG | — | Métricas e limiares |
| `CON-053` | Pare e escale | IMUT | — | Condições de parada |
| `CON-054` | Antipadrões proibidos | IMUT | — | Condições de parada |
| `CON-065` | O nome diz a intenção, não o tipo | OBRIG | — | Ofício: nomes, código e commits |
| `CON-066` | Vocabulário único, do banco à interface | OBRIG | — | Ofício: nomes, código e commits |
| `CON-067` | Sufixos com significado fixo | RECOM | — | Ofício: nomes, código e commits |
| `CON-068` | Booleano afirmativo | OBRIG | — | Ofício: nomes, código e commits |
| `CON-069` | Funções são verbos, e o nome revela o efeito | OBRIG | — | Ofício: nomes, código e commits |
| `CON-070` | Sem abreviação não estabelecida | RECOM | — | Ofício: nomes, código e commits |
| `CON-071` | Uma responsabilidade por unidade | RECOM | — | Ofício: nomes, código e commits |
| `CON-072` | Retorno antecipado | RECOM | — | Ofício: nomes, código e commits |
| `CON-073` | Sem número ou texto mágico | OBRIG | — | Ofício: nomes, código e commits |
| `CON-074` | Funções puras onde é possível | RECOM | — | Ofício: nomes, código e commits |
| `CON-075` | Sem código morto | OBRIG | — | Ofício: nomes, código e commits |
| `CON-076` | Imutabilidade por padrão | RECOM | — | Ofício: nomes, código e commits |
| `CON-077` | Sem escape do sistema de tipos | OBRIG | — | Ofício: nomes, código e commits |
| `CON-078` | Tipos de domínio, não primitivos | RECOM | — | Ofício: nomes, código e commits |
| `CON-079` | Ausência explícita | OBRIG | — | Ofício: nomes, código e commits |
| `CON-080` | Nunca engula erro | OBRIG | — | Ofício: nomes, código e commits |
| `CON-081` | Erro carrega contexto e separa usuário de sistema | OBRIG | — | Ofício: nomes, código e commits |
| `CON-082` | Comente o porquê, nunca o quê | OBRIG | — | Ofício: nomes, código e commits |
| `CON-083` | `TODO` exige identificador de backlog | OBRIG | — | Ofício: nomes, código e commits |
| `CON-084` | Documente o não óbvio, o perigoso e o contraintuitivo | RECOM | — | Ofício: nomes, código e commits |
| `CON-085` | A mensagem de commit explica o porquê | OBRIG | — | Ofício: nomes, código e commits |
| `CON-086` | Formatação em massa em commit separado | OBRIG | — | Ofício: nomes, código e commits |
| `CON-055` | A frase que resume o volume | IMUT | — | Ofício: nomes, código e commits |

## 📓 Volume 01 — Orquestrador Mestre

Arquivo: [`01-orquestrador.md`](01-orquestrador.md) · 32 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `ORC-001` | Os onze papéis | OBRIG | — | A cadeia de agentes |
| `ORC-002` | Todos herdam o mesmo contrato | IMUT | — | A cadeia de agentes |
| `ORC-003` | Orquestrador e Auditor estão em toda combinação | OBRIG | — | A cadeia de agentes |
| `ORC-004` | Nem toda tarefa merece a cadeia completa | IMUT | — | Escolha do caminho |
| `ORC-005` | Carregue só os volumes que a tarefa exige | OBRIG | — | Escolha do caminho |
| `ORC-006` | Descoberta é feita pelo orquestrador, pessoalmente | OBRIG | — | Despacho |
| `ORC-007` | Objetivo mensurável e não objetivos declarados | OBRIG | — | Despacho |
| `ORC-008` | Uma pergunta específica por papel | OBRIG | — | Despacho |
| `ORC-009` | Lista explícita de fora de escopo em cada despacho | OBRIG | — | Despacho |
| `ORC-010` | Ondas: sequencial onde há dependência, paralelo onde não há | OBRIG | — | Despacho |
| `ORC-011` | `S0`/`S1` de modelagem interrompe a rodada | OBRIG | — | Despacho |
| `ORC-012` | Security é despachado sempre que houver caminho sensível | OBRIG | — | Despacho |
| `ORC-013` | Performance só entra com medição possível | OBRIG | — | Despacho |
| `ORC-014` | Deduplicar | OBRIG | — | Integração |
| `ORC-015` | Rejeitar achado sem evidência | OBRIG | — | Integração |
| `ORC-016` | Deflacionar severidade inflada, com motivo escrito | OBRIG | — | Integração |
| `ORC-017` | `S0` e achado de segurança em caminho sensível não são rebaixáveis | IMUT | — | Integração |
| `ORC-018` | Resolver conflito pela regra de desempate, nunca pela média | OBRIG | — | Integração |
| `ORC-019` | Discussão que passa de dois turnos sem informação nova é encerrada por decisão | OBRIG | — | Integração |
| `ORC-020` | Aceitação de risco não é resolvida pelo orquestrador | IMUT | — | Integração |
| `ORC-021` | Compor a rodada em 70/20/10 | OBRIG | — | Integração |
| `ORC-022` | `MUST-FIX` acima da capacidade é o achado principal | OBRIG | — | Integração |
| `ORC-023` | Os oito critérios | OBRIG | — | Portão de aprovação |
| `ORC-024` | Rejeição com uma razão específica | OBRIG | — | Portão de aprovação |
| `ORC-025` | Não reescreva a proposta do papel | OBRIG | — | Portão de aprovação |
| `ORC-026` | Definir ordem de execução | OBRIG | — | Portão de aprovação |
| `ORC-027` | Proposta inviável durante a implementação volta à decisão | OBRIG | — | Portão de aprovação |
| `ORC-028` | O orquestrador não audita a própria rodada | IMUT | — | Encerramento |
| `ORC-029` | Registrar camadas não analisadas | OBRIG | — | Encerramento |
| `ORC-030` | Conferir o backlog | OBRIG | — | Encerramento |
| `ORC-031` | Registrar as notas para comparação | RECOM | — | Encerramento |
| `ORC-032` | Recomendar o próximo item de maior valor | OBRIG | — | Encerramento |

## 📗 Volume 2 — Framework de Arquitetura

Arquivo: [`02-arquitetura.md`](02-arquitetura.md) · 73 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `ARC-001` | Dependências apontam para dentro | OBRIG | — | Clean Architecture: direção das dependências |
| `ARC-002` | O domínio não conhece infraestrutura | OBRIG | — | Clean Architecture: direção das dependências |
| `ARC-003` | Inversão só onde há fronteira real | OBRIG | — | Clean Architecture: direção das dependências |
| `ARC-004` | Casos de uso orquestram, não decidem | OBRIG | — | Clean Architecture: direção das dependências |
| `ARC-005` | Zero dependências circulares | OBRIG | — | Clean Architecture: direção das dependências |
| `ARC-006` | Interface pública explícita por módulo | OBRIG | — | Clean Architecture: direção das dependências |
| `ARC-007` | Sem abstração especulativa | OBRIG | — | Clean Architecture: direção das dependências |
| `ARC-008` | Sem camada de passagem | RECOM | — | Clean Architecture: direção das dependências |
| `ARC-009` | Estados inválidos não são representáveis | OBRIG | — | Domain-Driven Design: o modelo |
| `ARC-010` | Invariantes aplicadas em todos os caminhos | OBRIG | — | Domain-Driven Design: o modelo |
| `ARC-011` | Uma fonte de verdade por decisão | OBRIG | — | Domain-Driven Design: o modelo |
| `ARC-012` | Tipos de domínio, não primitivos | OBRIG | — | Domain-Driven Design: o modelo |
| `ARC-013` | Agregado com fronteira de consistência | RECOM | — | Domain-Driven Design: o modelo |
| `ARC-014` | Sem modelo anêmico | RECOM | — | Domain-Driven Design: o modelo |
| `ARC-015` | Vocabulário único (linguagem ubíqua) | OBRIG | — | Domain-Driven Design: o modelo |
| `ARC-016` | Conceito de domínio ausente | RECOM | — | Domain-Driven Design: o modelo |
| `ARC-017` | Serviço de domínio só para o que não pertence a uma entidade | RECOM | — | Domain-Driven Design: o modelo |
| `ARC-018` | Evento de domínio é fato, no passado | RECOM | — | Domain-Driven Design: o modelo |
| `ARC-019` | Fronteiras alinhadas ao domínio | RECOM | — | Modularização |
| `ARC-020` | Regra de negócio fora das bordas | OBRIG | — | Modularização |
| `ARC-021` | Sem módulo Deus | OBRIG | — | Modularização |
| `ARC-022` | Estado compartilhado explícito | OBRIG | — | Modularização |
| `ARC-023` | Sem vazamento de ORM | OBRIG | — | Modularização |
| `ARC-024` | Divisão só com autonomia real | RECOM | — | Modularização |
| `ARC-025` | Falha declarada em toda fronteira | OBRIG | — | Integração entre módulos |
| `ARC-026` | Contratos versionados | OBRIG | — | Integração entre módulos |
| `ARC-027` | Compatibilidade durante o deploy | OBRIG | — | Integração entre módulos |
| `ARC-028` | Anticorrupção na borda de terceiros | RECOM | — | Integração entre módulos |
| `ARC-029` | Escolha entre síncrono e assíncrono é decisão registrada | RECOM | — | Integração entre módulos |
| `ARC-030` | Consumidor idempotente | OBRIG | — | Integração entre módulos |
| `ARC-031` | Consistência eventual é declarada ao usuário | RECOM | — | Integração entre módulos |
| `ARC-032` | Configuração fora do código | OBRIG | — | Configuração e ambiente |
| `ARC-033` | Sem ramificação por ambiente espalhada | OBRIG | — | Configuração e ambiente |
| `ARC-034` | Flags têm prazo | RECOM | — | Configuração e ambiente |
| `ARC-035` | O mapa, não o código | RECOM | — | Documentação da arquitetura |
| `ARC-036` | Decisão relevante tem ADR | OBRIG | — | Documentação da arquitetura |
| `ARC-037` | Divergência registrada, nunca silenciosa | OBRIG | — | Documentação da arquitetura |
| `ARC-038` | Trace uma mudança real | OBRIG | — | Heurísticas de diagnóstico |
| `ARC-039` | Tabela de sinais | OBRIG | — | Heurísticas de diagnóstico |
| `ARC-040` | Achado arquitetural exige custo e caminho incremental | OBRIG | — | Heurísticas de diagnóstico |
| `SEL-001` | O padrão é o mais simples que resolve | IMUT | — | A regra que governa toda escolha |
| `SEL-002` | Toda escolha declara o gatilho de mudança | OBRIG | — | A regra que governa toda escolha |
| `SEL-003` | Escolha por restrição observada, nunca por escala hipotética | IMUT | — | A regra que governa toda escolha |
| `SEL-004` | Nenhuma escolha de estilo sem ADR | OBRIG | — | A regra que governa toda escolha |
| `SEL-005` | Clean, Hexagonal e Onion: escolha o vocabulário, não a arquitetura | OBRIG | — | Estilos de organização interna |
| `SEL-006` | Camadas técnicas versus fatia vertical | RECOM | — | Estilos de organização interna |
| `SEL-007` | Feature First não dispensa fronteira de domínio | OBRIG | — | Estilos de organização interna |
| `SEL-008` | Monólito modular é o padrão para produto em evolução | RECOM | — | Monólito, monólito modular e serviços |
| `SEL-009` | Separar em serviço exige autonomia real em três eixos | OBRIG | — | Monólito, monólito modular e serviços |
| `SEL-010` | Dois serviços que sempre sobem juntos são um serviço com custo de rede | IMUT | — | Monólito, monólito modular e serviços |
| `SEL-011` | Separar exige a infraestrutura da separação, antes | OBRIG | — | Monólito, monólito modular e serviços |
| `SEL-012` | Extraia um serviço por vez, pela fronteira mais clara | OBRIG | — | Monólito, monólito modular e serviços |
| `SEL-013` | Banco compartilhado entre serviços anula a separação | OBRIG | — | Monólito, monólito modular e serviços |
| `SEL-014` | BFF só com clientes de necessidades divergentes | RECOM | — | Monólito, monólito modular e serviços |
| `SEL-015` | CQRS é resposta a uma assimetria medida | RECOM | — | CQRS e event sourcing |
| `SEL-016` | CQRS assíncrono cria consistência eventual visível ao usuário | OBRIG | — | CQRS e event sourcing |
| `SEL-017` | Event sourcing exige compromisso permanente | OBRIG | — | CQRS e event sourcing |
| `SEL-018` | Evento de domínio não é event sourcing | OBRIG | — | CQRS e event sourcing |
| `SEL-019` | Nenhum dos dois é padrão; a escolha é registrada | OBRIG | — | Síncrono e assíncrono |
| `SEL-020` | Assíncrono para o que o usuário não espera | RECOM | — | Síncrono e assíncrono |
| `SEL-021` | Assíncrono exige consumidor idempotente, sem exceção | OBRIG | — | Síncrono e assíncrono |
| `SEL-022` | Fila não conserta dependência instável | OBRIG | — | Síncrono e assíncrono |
| `SEL-023` | Escolha o modelo de entrega conscientemente | RECOM | — | Síncrono e assíncrono |
| `SEL-024` | Escolha por natureza do conteúdo, não por moda de framework | OBRIG | — | Estratégia de renderização |
| `SEL-025` | Dado por usuário nunca em resposta cacheada publicamente | OBRIG | `S0` | Estratégia de renderização |
| `SEL-026` | A fronteira servidor/cliente é uma fronteira de segurança | OBRIG | — | Estratégia de renderização |
| `SEL-027` | Streaming exige espaço reservado | OBRIG | — | Estratégia de renderização |
| `SEL-028` | Misturar estratégias é normal; misturar sem critério declarado não é | RECOM | — | Estratégia de renderização |
| `SEL-029` | Construir o que é diferencial; comprar o resto | RECOM | — | Comprar, usar ou construir |
| `SEL-030` | Dependência é decisão com quatro perguntas | OBRIG | — | Comprar, usar ou construir |
| `SEL-031` | Fornecedor entra pela borda, com tradução | OBRIG | — | Comprar, usar ou construir |
| `SEL-032` | Fornecedor crítico exige comportamento em falha declarado | OBRIG | — | Comprar, usar ou construir |
| `SEL-033` | Construir para evitar custo de assinatura exige o cálculo completo | RECOM | — | Comprar, usar ou construir |

## 📙 Volume 3 — Framework Backend

Arquivo: [`03-backend.md`](03-backend.md) · 73 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `BAK-001` | Enuncie cada regra em linguagem clara | OBRIG | — | Regras de negócio |
| `BAK-002` | Mapeie todos os caminhos que devem aplicar a regra | OBRIG | — | Regras de negócio |
| `BAK-003` | Percorra o ponto de entrada ponta a ponta | OBRIG | — | Regras de negócio |
| `BAK-004` | Falha de negócio previsível não é exceção | RECOM | — | Regras de negócio |
| `BAK-005` | Cálculo é função pura | RECOM | — | Regras de negócio |
| `BAK-006` | Arredondamento é decisão explícita | OBRIG | — | Regras de negócio |
| `BAK-007` | Dinheiro em inteiro ou decimal exato | OBRIG | — | Regras de negócio |
| `BAK-008` | Transições de estado são explícitas e verificadas | OBRIG | — | Regras de negócio |
| `BAK-009` | Validação no servidor, sempre | OBRIG | — | Entrada e validação |
| `BAK-010` | Rejeite campos desconhecidos | OBRIG | — | Entrada e validação |
| `BAK-011` | Nunca aceite campo privilegiado do cliente | OBRIG | — | Entrada e validação |
| `BAK-012` | Validação por lista de permitidos | OBRIG | — | Entrada e validação |
| `BAK-013` | Limite de tamanho em toda entrada | OBRIG | — | Entrada e validação |
| `BAK-014` | Distinga ausência de vazio e de zero | OBRIG | — | Entrada e validação |
| `BAK-015` | Tabela de bordas obrigatória | OBRIG | — | Entrada e validação |
| `BAK-016` | Autorização por objeto, não por rota | OBRIG | — | Autenticação e autorização |
| `BAK-017` | Negar por omissão | OBRIG | — | Autenticação e autorização |
| `BAK-018` | Autorização centralizada e obrigatória por construção | RECOM | — | Autenticação e autorização |
| `BAK-019` | Filtro de tenant na camada de dados | OBRIG | — | Autenticação e autorização |
| `BAK-020` | Autorização em lote, exportação e recurso aninhado | OBRIG | — | Autenticação e autorização |
| `BAK-021` | Reautenticação em operação sensível | OBRIG | — | Autenticação e autorização |
| `BAK-022` | Job herda autoridade explícita | OBRIG | — | Autenticação e autorização |
| `BAK-023` | Nunca engula erro | OBRIG | — | Tratamento de erros |
| `BAK-024` | Erro carrega contexto | OBRIG | — | Tratamento de erros |
| `BAK-025` | Separe erro de usuário de erro de sistema | OBRIG | — | Tratamento de erros |
| `BAK-026` | Formato único de erro em toda a API | OBRIG | — | Tratamento de erros |
| `BAK-027` | Erro de fornecedor mapeado para erro de domínio | OBRIG | — | Tratamento de erros |
| `BAK-028` | Mensagem de erro não revela existência | OBRIG | — | Tratamento de erros |
| `BAK-029` | Contrato declarado é a fonte de verdade | OBRIG | — | Contrato de API |
| `BAK-030` | Mudança incompatível exige versão | OBRIG | — | Contrato de API |
| `BAK-031` | Métodos e status corretos | OBRIG | — | Contrato de API |
| `BAK-032` | Coleções são paginadas com limite do servidor | OBRIG | — | Contrato de API |
| `BAK-033` | Não serialize a entidade inteira | OBRIG | — | Contrato de API |
| `BAK-034` | Padrão de nomes consistente | OBRIG | — | Contrato de API |
| `BAK-035` | Limite de taxa em toda API pública | OBRIG | — | Contrato de API |
| `BAK-036` | Deprecação anunciada e medida | OBRIG | — | Contrato de API |
| `BAK-037` | Identificador não sequencial em recurso exposto | RECOM | — | Contrato de API |
| `BAK-038` | Recurso escasso tem proteção explícita | OBRIG | — | Concorrência |
| `BAK-039` | Escopo de transação pela invariante | OBRIG | — | Concorrência |
| `BAK-040` | Nada externo dentro da transação | OBRIG | — | Concorrência |
| `BAK-041` | Ordem consistente de bloqueio | RECOM | — | Concorrência |
| `BAK-042` | Idempotência em operação com efeito externo | OBRIG | — | Concorrência |
| `BAK-043` | Toda chamada externa tem timeout | OBRIG | — | Resiliência |
| `BAK-044` | Retry com espera crescente, limite e idempotência | OBRIG | — | Resiliência |
| `BAK-045` | Comportamento em falha é decidido, não acidental | OBRIG | — | Resiliência |
| `BAK-046` | Sucesso parcial é tratado | OBRIG | — | Resiliência |
| `BAK-047` | Fila com destino final definido | OBRIG | — | Resiliência |
| `BAK-048` | Trabalho em volume é processado em lotes e retomável | RECOM | — | Resiliência |
| `BAK-049` | Webhook de entrada verifica a origem | OBRIG | `S0` | Webhooks |
| `BAK-050` | Webhook de entrada é idempotente | OBRIG | — | Webhooks |
| `BAK-051` | Responda rápido, processe fora do ciclo da requisição | OBRIG | — | Webhooks |
| `BAK-052` | Ordem de chegada não é garantida | OBRIG | — | Webhooks |
| `BAK-053` | Evento desconhecido é ignorado, não é erro | RECOM | — | Webhooks |
| `BAK-054` | Webhook de saída é assinado, com segredo por assinante | OBRIG | — | Webhooks |
| `BAK-055` | URL de destino validada contra faixas internas | OBRIG | `S1` | Webhooks |
| `BAK-056` | Reentrega com espera crescente, limite e destino final | OBRIG | — | Webhooks |
| `BAK-057` | Carga útil mínima, sem dado sensível | OBRIG | — | Webhooks |
| `BAK-058` | Falha de assinante não afeta o fluxo principal | OBRIG | — | Webhooks |
| `BAK-059` | O assinante tem visibilidade das entregas | RECOM | — | Webhooks |
| `BAK-060` | Resolver não faz uma consulta por item | OBRIG | — | GraphQL |
| `BAK-061` | Profundidade e complexidade limitadas | OBRIG | `S1` | GraphQL |
| `BAK-062` | Autorização por campo e por objeto, não na raiz | OBRIG | `S0` | GraphQL |
| `BAK-063` | Erro parcial é decisão explícita | OBRIG | — | GraphQL |
| `BAK-064` | Introspecção e campos internos controlados em produção | RECOM | — | GraphQL |
| `BAK-065` | Deprecação de campo é medida antes da remoção | OBRIG | — | GraphQL |
| `BAK-066` | Agendamento roda uma vez, não uma vez por instância | OBRIG | `S0` com efeito externo | Trabalho agendado e workers |
| `BAK-067` | Todo job é idempotente e retomável | OBRIG | — | Trabalho agendado e workers |
| `BAK-068` | Job declara com que autoridade roda | OBRIG | — | Trabalho agendado e workers |
| `BAK-069` | Sobreposição de execução é tratada | OBRIG | — | Trabalho agendado e workers |
| `BAK-070` | Timeout por execução | OBRIG | — | Trabalho agendado e workers |
| `BAK-071` | Falha de job é visível e alertada | OBRIG | — | Trabalho agendado e workers |
| `BAK-072` | Fuso do agendamento é explícito | OBRIG | — | Trabalho agendado e workers |
| `BAK-073` | Job de volume processa em lotes, com progresso registrado | RECOM | — | Trabalho agendado e workers |

## 📕 Volume 4 — Framework Frontend

Arquivo: [`04-frontend.md`](04-frontend.md) · 42 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `FRT-001` | Os oito estados de toda tela | OBRIG | — | Cobertura de estados |
| `FRT-002` | Vazio não é erro | OBRIG | — | Cobertura de estados |
| `FRT-003` | Impedir envio duplicado | OBRIG | — | Cobertura de estados |
| `FRT-004` | Nunca exponha erro bruto do servidor | OBRIG | — | Cobertura de estados |
| `FRT-005` | Percorra os caminhos de falha | OBRIG | — | Cobertura de estados |
| `FRT-006` | Separe dado do servidor de estado do cliente | OBRIG | — | Gerenciamento de estado |
| `FRT-007` | Derive, não duplique | OBRIG | — | Gerenciamento de estado |
| `FRT-008` | Estado no menor escopo possível | RECOM | — | Gerenciamento de estado |
| `FRT-009` | Invalidação declarada após mutação | OBRIG | — | Gerenciamento de estado |
| `FRT-010` | Corrida entre requisições tratada | OBRIG | — | Gerenciamento de estado |
| `FRT-011` | Atualização otimista tem rollback | OBRIG | — | Gerenciamento de estado |
| `FRT-012` | Nenhum efeito colateral em renderização | OBRIG | — | Gerenciamento de estado |
| `FRT-013` | Nada de estado derivado de props copiado na inicialização | RECOM | — | Gerenciamento de estado |
| `FRT-014` | Componente tem uma responsabilidade | RECOM | — | Componentes |
| `FRT-015` | Separe apresentação de orquestração | RECOM | — | Componentes |
| `FRT-016` | Nenhuma regra de negócio no componente | OBRIG | — | Componentes |
| `FRT-017` | Componente controlado ou não controlado, nunca ambos | RECOM | — | Componentes |
| `FRT-018` | Chave estável em lista | OBRIG | — | Componentes |
| `FRT-019` | Limite de erro na fronteira de tela | OBRIG | — | Componentes |
| `FRT-020` | Elemento nativo antes de recriar comportamento | OBRIG | — | Componentes |
| `FRT-021` | Um token, não um valor literal | OBRIG | — | Design system |
| `FRT-022` | Um componente por padrão de interação | OBRIG | — | Design system |
| `FRT-023` | Variante declarada, não improvisada | RECOM | — | Design system |
| `FRT-024` | Estado visual completo em cada componente do sistema | OBRIG | — | Design system |
| `FRT-025` | Acessibilidade embutida no componente | OBRIG | — | Design system |
| `FRT-026` | Contraste verificado no token, não na tela | OBRIG | — | Design system |
| `FRT-027` | Componente do sistema não conhece o domínio | RECOM | — | Design system |
| `FRT-028` | Orçamento de bundle declarado e verificado no pipeline | OBRIG | — | Performance de interface |
| `FRT-029` | Dependência é decisão de performance | OBRIG | — | Performance de interface |
| `FRT-030` | Divisão de código por rota | RECOM | — | Performance de interface |
| `FRT-031` | Nenhum re-render desnecessário por identidade instável | RECOM | — | Performance de interface |
| `FRT-032` | Lista longa é virtualizada | OBRIG | — | Performance de interface |
| `FRT-033` | Nenhum trabalho pesado na thread principal | OBRIG | — | Performance de interface |
| `FRT-034` | Reserve espaço para conteúdo assíncrono | OBRIG | — | Performance de interface |
| `FRT-035` | Imagem otimizada por padrão | OBRIG | — | Performance de interface |
| `FRT-036` | Animação em propriedade que não recalcula layout | RECOM | — | Performance de interface |
| `FRT-037` | Fonte não bloqueia a primeira pintura | RECOM | — | Performance de interface |
| `FRT-038` | Nenhum segredo no cliente | OBRIG | — | Segurança no cliente |
| `FRT-039` | Nenhuma decisão de segurança no cliente | OBRIG | — | Segurança no cliente |
| `FRT-040` | Nenhuma inserção de HTML não confiável | OBRIG | — | Segurança no cliente |
| `FRT-041` | Armazenamento local não guarda dado sensível | OBRIG | — | Segurança no cliente |
| `FRT-042` | Destino de redirecionamento validado | OBRIG | — | Segurança no cliente |

## 📒 Volume 05 — Framework de Banco de Dados

Arquivo: [`05-banco-de-dados.md`](05-banco-de-dados.md) · 40 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `DAT-001` | O banco é a última linha de defesa da integridade | IMUT | — | - |
| `DAT-002` | Auditoria de invariantes é o primeiro entregável | OBRIG | — | Modelagem e integridade |
| `DAT-003` | `NOT NULL` em tudo que é obrigatório | OBRIG | — | Modelagem e integridade |
| `DAT-004` | `UNIQUE` no que é único | OBRIG | — | Modelagem e integridade |
| `DAT-005` | Chave estrangeira com comportamento explícito | OBRIG | — | Modelagem e integridade |
| `DAT-006` | `CHECK` para faixas e combinações válidas | OBRIG | — | Modelagem e integridade |
| `DAT-007` | Estado inválido não representável no schema | RECOM | — | Modelagem e integridade |
| `DAT-008` | Valor padrão válido no domínio | OBRIG | — | Modelagem e integridade |
| `DAT-009` | Tipos corretos | OBRIG | — | Modelagem e integridade |
| `DAT-010` | JSON não é atalho para não modelar | OBRIG | — | Modelagem e integridade |
| `DAT-011` | Sem exclusão física de histórico | RECOM | — | Modelagem e integridade |
| `DAT-012` | Carimbos mantidos pelo banco | RECOM | — | Modelagem e integridade |
| `DAT-013` | Auditoria do que importa | RECOM | — | Modelagem e integridade |
| `DAT-014` | Sem modelo genérico de entidade-atributo-valor | RECOM | — | Modelagem e integridade |
| `DAT-015` | Toda consulta frequente usa índice | OBRIG | — | Índices e consultas |
| `DAT-016` | Verifique o plano de execução | OBRIG | — | Índices e consultas |
| `DAT-017` | Ordem de colunas do índice composto corresponde às consultas reais | OBRIG | — | Índices e consultas |
| `DAT-018` | Índice não utilizado é problema | RECOM | — | Índices e consultas |
| `DAT-019` | Zero N+1 | OBRIG | — | Índices e consultas |
| `DAT-020` | Nenhuma consulta em laço | OBRIG | — | Índices e consultas |
| `DAT-021` | Limite obrigatório em caminho de requisição | OBRIG | — | Índices e consultas |
| `DAT-022` | Selecione o que precisa | RECOM | — | Índices e consultas |
| `DAT-023` | Agregação no banco | RECOM | — | Índices e consultas |
| `DAT-024` | Declare o volume assumido | OBRIG | — | Índices e consultas |
| `DAT-025` | Escopo pela invariante | OBRIG | — | Transações e concorrência |
| `DAT-026` | Nada externo dentro da transação | OBRIG | — | Transações e concorrência |
| `DAT-027` | Recurso escasso tem proteção declarada | OBRIG | — | Transações e concorrência |
| `DAT-028` | Nível de isolamento é decisão consciente | RECOM | — | Transações e concorrência |
| `DAT-029` | Ordem consistente de bloqueio | RECOM | — | Transações e concorrência |
| `DAT-030` | Versionadas, reversíveis e com reversa executada | OBRIG | — | Migrações |
| `DAT-031` | Duas fases para mudança incompatível | OBRIG | — | Migrações |
| `DAT-032` | Conte os registros que violam a nova regra | OBRIG | — | Migrações |
| `DAT-033` | Não bloqueie tabela grande | OBRIG | — | Migrações |
| `DAT-034` | Migração de dados é `R4` | OBRIG | — | Migrações |
| `DAT-035` | Migração destrutiva separada da mudança de comportamento | OBRIG | — | Migrações |
| `DAT-036` | Migração é testada contra volume representativo | RECOM | — | Migrações |
| `DAT-037` | Backup com restauração testada | OBRIG | — | Operação |
| `DAT-038` | Credencial da aplicação com privilégio mínimo | OBRIG | — | Operação |
| `DAT-039` | Retenção definida por tabela sensível ou volumosa | RECOM | — | Operação |
| `DAT-040` | Isolamento de tenant garantido no banco quando possível | OBRIG | — | Operação |

## 📓 Volume 06 — Segurança e DevSecOps

Arquivo: [`06-seguranca.md`](06-seguranca.md) · 66 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `SEC-001` | O ônus da prova é invertido | IMUT | — | - |
| `SEC-002` | Pense como atacante autenticado | OBRIG | — | - |
| `SEC-003` | Ordem de análise dentro da segurança | OBRIG | — | - |
| `SEC-004` | Autorização por objeto | OBRIG | `S0` | Controle de acesso (OWASP A01) |
| `SEC-005` | Negar por omissão | OBRIG | — | Controle de acesso (OWASP A01) |
| `SEC-006` | Isolamento de tenant na camada de dados | OBRIG | `S0` | Controle de acesso (OWASP A01) |
| `SEC-007` | As quatro perguntas por ponto de entrada | OBRIG | — | Controle de acesso (OWASP A01) |
| `SEC-008` | Os caminhos que a revisão esquece | OBRIG | — | Controle de acesso (OWASP A01) |
| `SEC-009` | Campo privilegiado do cliente é ignorado | OBRIG | `S0` | Controle de acesso (OWASP A01) |
| `SEC-010` | Autorização centralizada por construção | RECOM | — | Controle de acesso (OWASP A01) |
| `SEC-011` | Registro de auditoria em operação sensível | RECOM | — | Controle de acesso (OWASP A01) |
| `SEC-012` | Senha com hash lento e específico | OBRIG | `S0` | Criptografia (OWASP A02) |
| `SEC-013` | TLS em trânsito, sem exceção interna | OBRIG | — | Criptografia (OWASP A02) |
| `SEC-014` | Dado sensível criptografado em repouso | OBRIG | — | Criptografia (OWASP A02) |
| `SEC-015` | Nenhum algoritmo obsoleto e nenhuma criptografia caseira | OBRIG | — | Criptografia (OWASP A02) |
| `SEC-016` | Aleatoriedade criptográfica para token | OBRIG | — | Criptografia (OWASP A02) |
| `SEC-017` | Comparação de segredo em tempo constante | OBRIG | — | Criptografia (OWASP A02) |
| `SEC-018` | Hash não é criptografia, e codificação não é nenhum dos dois | OBRIG | — | Criptografia (OWASP A02) |
| `SEC-019` | Consulta parametrizada, sempre | OBRIG | `S0` | Injeção (OWASP A03) |
| `SEC-020` | Nunca execute entrada | OBRIG | `S0` | Injeção (OWASP A03) |
| `SEC-021` | Escape na saída por contexto | OBRIG | — | Injeção (OWASP A03) |
| `SEC-022` | Nenhuma inserção de HTML não confiável | OBRIG | `S1` | Injeção (OWASP A03) |
| `SEC-023` | Upload de arquivo tratado como hostil | OBRIG | — | Injeção (OWASP A03) |
| `SEC-024` | Nome de arquivo, cabeçalho e caminho validados | OBRIG | — | Injeção (OWASP A03) |
| `SEC-025` | Reautenticação em fluxo sensível | OBRIG | — | Design inseguro (OWASP A04) |
| `SEC-026` | Limite de tentativas com bloqueio progressivo | OBRIG | — | Design inseguro (OWASP A04) |
| `SEC-027` | Não revele existência | OBRIG | — | Design inseguro (OWASP A04) |
| `SEC-028` | Operação irreversível é confirmada e registrada | OBRIG | — | Design inseguro (OWASP A04) |
| `SEC-029` | Modele o abuso, não só o uso | OBRIG | — | Design inseguro (OWASP A04) |
| `SEC-030` | Controle de segurança que empurra para contorno é falha | RECOM | — | Design inseguro (OWASP A04) |
| `SEC-031` | Nenhuma credencial padrão em produção | OBRIG | `S0` | Configuração (OWASP A05) |
| `SEC-032` | Depuração e erro detalhado desligados em produção | OBRIG | — | Configuração (OWASP A05) |
| `SEC-033` | CORS restrito a origens conhecidas | OBRIG | — | Configuração (OWASP A05) |
| `SEC-034` | Cabeçalhos de segurança presentes | OBRIG | — | Configuração (OWASP A05) |
| `SEC-035` | Armazenamento privado por padrão | OBRIG | — | Configuração (OWASP A05) |
| `SEC-036` | Menor privilégio em toda credencial de serviço | OBRIG | — | Configuração (OWASP A05) |
| `SEC-037` | Superfície mínima | OBRIG | — | Configuração (OWASP A05) |
| `SEC-038` | Varredura automatizada que bloqueia | OBRIG | — | Dependências e cadeia de suprimentos (OWASP A06 e A08) |
| `SEC-039` | Supressão exige análise de explorabilidade escrita | OBRIG | — | Dependências e cadeia de suprimentos (OWASP A06 e A08) |
| `SEC-040` | Dependência abandonada é risco registrado | RECOM | — | Dependências e cadeia de suprimentos (OWASP A06 e A08) |
| `SEC-041` | Integridade verificada em tudo que executa | OBRIG | — | Dependências e cadeia de suprimentos (OWASP A06 e A08) |
| `SEC-042` | Pipeline é código revisado | OBRIG | — | Dependências e cadeia de suprimentos (OWASP A06 e A08) |
| `SEC-043` | Cuidado com typosquatting e script de instalação | RECOM | — | Dependências e cadeia de suprimentos (OWASP A06 e A08) |
| `SEC-044` | Sessão expira, renova com segurança e é invalidada | OBRIG | — | Autenticação e sessão (OWASP A07) |
| `SEC-045` | Identificador de sessão regenerado após autenticar | OBRIG | — | Autenticação e sessão (OWASP A07) |
| `SEC-046` | Token com escopo, vida curta e revogação possível | OBRIG | — | Autenticação e sessão (OWASP A07) |
| `SEC-047` | MFA disponível em conta e operação sensível | RECOM | — | Autenticação e sessão (OWASP A07) |
| `SEC-048` | Proteção contra requisição forjada em fluxo com cookie | OBRIG | — | Autenticação e sessão (OWASP A07) |
| `SEC-049` | URL fornecida pelo usuário passa por lista de permitidos | OBRIG | — | SSRF (OWASP A10) |
| `SEC-050` | Nenhum dado sensível em log | OBRIG | `S0` | Registro e monitoramento (OWASP A09) |
| `SEC-051` | Eventos de segurança registrados e alertados | OBRIG | — | Registro e monitoramento (OWASP A09) |
| `SEC-052` | Ordem correta ao encontrar segredo exposto | IMUT | — | Segredos |
| `SEC-053` | Inventário obrigatório | OBRIG | — | Dados pessoais |
| `SEC-054` | Minimização | OBRIG | — | Dados pessoais |
| `SEC-055` | Retenção declarada e eliminação automatizada | OBRIG | — | Dados pessoais |
| `SEC-056` | Direitos do titular tecnicamente possíveis | OBRIG | — | Dados pessoais |
| `SEC-057` | Nenhum dado pessoal em desenvolvimento ou em fixture | OBRIG | — | Dados pessoais |
| `SEC-058` | Compartilhamento com terceiro é decisão registrada | OBRIG | — | Dados pessoais |
| `SEC-059` | Três níveis, escolhidos por criticidade do módulo | OBRIG | — | Níveis de verificação |
| `SEC-060` | O nível é declarado no relatório, sempre | OBRIG | — | Níveis de verificação |
| `SEC-061` | Subir de nível é decisão registrada; descer também | OBRIG | — | Níveis de verificação |
| `SEC-062` | V3 nunca é executado só por agente | IMUT | — | Níveis de verificação |
| `SEC-063` | Nível não substitui as regras de bloqueio | IMUT | — | Níveis de verificação |
| `SEC-064` | Testes passando não é prova | OBRIG | — | Níveis de verificação |
| `SEC-065` | Descreva o caminho de exploração concretamente | OBRIG | — | Níveis de verificação |
| `SEC-066` | `S0` de segurança não é rebaixável por agente | IMUT | — | Níveis de verificação |

## 📔 Volume 7 — Framework de Performance

Arquivo: [`07-performance.md`](07-performance.md) · 38 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `PRF-001` | Sem medição, não há achado | IMUT | — | - |
| `PRF-002` | Toda medição declara o método | OBRIG | — | - |
| `PRF-003` | Use p95, nunca média | OBRIG | — | - |
| `PRF-004` | Meça no volume real, atual e projetado | OBRIG | — | - |
| `PRF-005` | Ataque o gargalo, não o suspeito | OBRIG | — | - |
| `PRF-006` | Prove o ganho, ou não houve ganho | OBRIG | — | - |
| `PRF-007` | Siga a ordem de maior impacto típico | OBRIG | — | Ordem de investigação |
| `PRF-008` | Conte as consultas por requisição | OBRIG | — | Acesso a dados |
| `PRF-009` | Plano de execução verificado antes de afirmar falta de índice | OBRIG | — | Acesso a dados |
| `PRF-010` | Paginação com limite do servidor em toda listagem | OBRIG | — | Acesso a dados |
| `PRF-011` | Agregação no banco, não na aplicação | RECOM | — | Acesso a dados |
| `PRF-012` | Transação curta para evitar contenção | RECOM | — | Acesso a dados |
| `PRF-013` | Chamadas independentes em paralelo | RECOM | — | Rede e integrações |
| `PRF-014` | Toda chamada externa tem timeout | OBRIG | — | Rede e integrações |
| `PRF-015` | Paralelismo com limite | OBRIG | — | Rede e integrações |
| `PRF-016` | Retry com espera crescente e variação aleatória | OBRIG | — | Rede e integrações |
| `PRF-017` | Conexões reutilizadas | RECOM | — | Rede e integrações |
| `PRF-018` | Degradação em vez de queda | RECOM | — | Rede e integrações |
| `PRF-019` | Cache é decisão, com quatro respostas obrigatórias | OBRIG | — | Cache |
| `PRF-020` | A chave inclui tudo que altera a resposta | OBRIG | `S0` | Cache |
| `PRF-021` | Invalidação definida por mutação | OBRIG | — | Cache |
| `PRF-022` | Cache não esconde N+1 | OBRIG | — | Cache |
| `PRF-023` | Suba um nível de cache por vez, com medição | RECOM | — | Cache |
| `PRF-024` | Cache de dado sensível é decisão registrada | OBRIG | — | Cache |
| `PRF-025` | Prevenir avalanche de recomputação | RECOM | — | Cache |
| `PRF-026` | Nenhuma recomputação de valor estável na mesma requisição | RECOM | — | Trabalho repetido e carga útil |
| `PRF-027` | Resposta sem campos não usados | RECOM | — | Trabalho repetido e carga útil |
| `PRF-028` | Compressão habilitada nas respostas | OBRIG | — | Trabalho repetido e carga útil |
| `PRF-029` | Nenhuma serialização redundante | RECOM | — | Trabalho repetido e carga útil |
| `PRF-030` | Orçamento de bundle verificado no pipeline | OBRIG | — | Renderização e interface |
| `PRF-031` | Lista longa virtualizada | OBRIG | — | Renderização e interface |
| `PRF-032` | Nenhum trabalho pesado na thread principal | OBRIG | — | Renderização e interface |
| `PRF-033` | Espaço reservado para conteúdo assíncrono | OBRIG | — | Renderização e interface |
| `PRF-034` | Percepção de velocidade é tratada | RECOM | — | Renderização e interface |
| `PRF-035` | Complexidade adequada ao volume real | OBRIG | — | Algoritmo e volume |
| `PRF-036` | Estrutura de dados adequada ao padrão de acesso | RECOM | — | Algoritmo e volume |
| `PRF-037` | Trabalho em volume processado em lotes e retomável | RECOM | — | Algoritmo e volume |
| `PRF-038` | Limiares declarados e protegidos por verificação automática | OBRIG | — | Limiares e regressão |

## 📘 Volume 8 — UX/UI Premium

Arquivo: [`08-ux-premium.md`](08-ux-premium.md) · 55 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `UXI-001` | Gosto visual não é achado | IMUT | — | - |
| `UXI-002` | Os oito estados são projetados | OBRIG | — | Estados |
| `UXI-003` | Três vazios diferentes | OBRIG | — | Estados |
| `UXI-004` | Estado vazio diz o que fazer | OBRIG | — | Estados |
| `UXI-005` | Toda ação tem resposta imediata | OBRIG | — | Feedback e microinterações |
| `UXI-006` | Feedback proporcional à espera | RECOM | — | Feedback e microinterações |
| `UXI-007` | Impedir envio duplicado | OBRIG | `S1` | Feedback e microinterações |
| `UXI-008` | Sucesso confirmado sem ambiguidade | OBRIG | — | Feedback e microinterações |
| `UXI-009` | Microinteração informa, não decora | RECOM | — | Feedback e microinterações |
| `UXI-010` | Transição preserva a continuidade | RECOM | — | Feedback e microinterações |
| `UXI-011` | Duração curta e curva natural | RECOM | — | Feedback e microinterações |
| `UXI-012` | Respeite a redução de movimento | OBRIG | — | Feedback e microinterações |
| `UXI-013` | Nenhuma animação bloqueia a interação | OBRIG | — | Feedback e microinterações |
| `UXI-014` | Estado de foco e sobreposição são microinterações obrigatórias | OBRIG | — | Feedback e microinterações |
| `UXI-015` | Erro no vocabulário do usuário | OBRIG | — | Mensagens de erro |
| `UXI-016` | Todo erro diz o que fazer | OBRIG | — | Mensagens de erro |
| `UXI-017` | Nenhum detalhe técnico na interface | OBRIG | — | Mensagens de erro |
| `UXI-018` | Ofereça caminho de saída | RECOM | — | Mensagens de erro |
| `UXI-019` | Nenhum jargão interno | OBRIG | — | Mensagens de erro |
| `UXI-020` | Prefira desfazer a confirmar | RECOM | — | Prevenção de erro e proteção do trabalho |
| `UXI-021` | Confirmação nomeia o que será destruído | OBRIG | — | Prevenção de erro e proteção do trabalho |
| `UXI-022` | Ação destrutiva sem confirmação nem desfazer é `S1` | OBRIG | — | Prevenção de erro e proteção do trabalho |
| `UXI-023` | Nunca perca o trabalho do usuário | OBRIG | `S1` em formulário longo | Prevenção de erro e proteção do trabalho |
| `UXI-024` | Valide no momento certo | RECOM | — | Prevenção de erro e proteção do trabalho |
| `UXI-025` | Ação destrutiva longe da ação comum | RECOM | — | Prevenção de erro e proteção do trabalho |
| `UXI-026` | Limite de tempo avisado e extensível | OBRIG | — | Prevenção de erro e proteção do trabalho |
| `UXI-027` | Nenhum beco sem saída | OBRIG | — | Prevenção de erro e proteção do trabalho |
| `UXI-028` | Um padrão por problema | OBRIG | — | Consistência |
| `UXI-029` | Vocabulário único na interface | OBRIG | — | Consistência |
| `UXI-030` | Mesmas regras de validação para o mesmo campo | OBRIG | — | Consistência |
| `UXI-031` | Mesmo padrão de ação destrutiva em todo o produto | OBRIG | — | Consistência |
| `UXI-032` | Formato local consistente | OBRIG | — | Consistência |
| `UXI-033` | Estado de navegação preservado | RECOM | — | Consistência |
| `UXI-034` | Uma ação primária por tela | RECOM | — | Consistência |
| `UXI-035` | Números com contexto | RECOM | — | Consistência |
| `UXI-036` | O objetivo do usuário está declarado | OBRIG | — | Fluxos |
| `UXI-037` | O usuário sabe onde está e quanto falta | RECOM | — | Fluxos |
| `UXI-038` | Não bloqueie o que pode ser postergado | RECOM | — | Fluxos |
| `UXI-039` | Percorra os caminhos infelizes | OBRIG | — | Fluxos |
| `UXI-040` | Degradação aceitável para o usuário, não só para o engenheiro | OBRIG | — | Fluxos |
| `UXI-041` | Semântica antes de ARIA | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-042` | Estrutura significativa | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-043` | Idioma declarado | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-044` | Toda tarefa completável por teclado | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-045` | Foco sempre visível | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-046` | Ordem de foco lógica | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-047` | Foco gerenciado em conteúdo dinâmico | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-048` | Sem armadilha de foco | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-049` | Todo controle tem nome acessível | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-050` | Estado comunicado programaticamente | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-051` | Mudança dinâmica anunciada | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-052` | Erro identificado, descrito e associado ao campo | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-053` | Contraste conforme AA | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-054` | Zoom 200% e viewport estreita sem perda | OBRIG | — | Acessibilidade (WCAG 2.2 AA) |
| `UXI-055` | Alvo de toque adequado | RECOM | — | Acessibilidade (WCAG 2.2 AA) |

## 📗 Volume 09 — Design System

Arquivo: [`09-design-system.md`](09-design-system.md) · 69 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `DSY-001` | Um design system existe para eliminar decisão repetida, não para padronizar gosto | IMUT | — | O sistema, seu dono e sua fronteira |
| `DSY-002` | Uma biblioteca de componentes sem tokens, documentação e governança não é o sistema | OBRIG | — | O sistema, seu dono e sua fronteira |
| `DSY-003` | O sistema tem dono nomeado e uma fonte única | OBRIG | — | O sistema, seu dono e sua fronteira |
| `DSY-004` | A promoção de uma peça ao sistema tem limiar declarado | OBRIG | — | O sistema, seu dono e sua fronteira |
| `DSY-005` | O sistema é consumido como artefato versionado, nunca copiado | OBRIG | — | O sistema, seu dono e sua fronteira |
| `DSY-006` | Três níveis de token, com o consumidor declarado por nível | OBRIG | — | Tokens |
| `DSY-007` | Componente e tela consomem token semântico, nunca primitivo | OBRIG | — | Tokens |
| `DSY-008` | O nome do token semântico descreve papel, nunca aparência | OBRIG | — | Tokens |
| `DSY-009` | Token de componente existe só quando o semântico não basta | RECOM | — | Tokens |
| `DSY-010` | Nenhum valor bruto atravessa a camada semântica | OBRIG | — | Tokens |
| `DSY-011` | Os tokens têm uma fonte única, e cada plataforma é gerada dela | OBRIG | — | Tokens |
| `DSY-012` | Todo token semântico tem valor em todos os temas declarados | OBRIG | — | Tokens |
| `DSY-013` | Nenhum valor tem dois nomes semânticos | OBRIG | — | Tokens |
| `DSY-014` | Token removido ou renomeado passa por depreciação, nunca por substituição direta | OBRIG | — | Tokens |
| `DSY-015` | Cor vive em escala com passos fixos | OBRIG | — | Cor |
| `DSY-016` | O contraste é garantido pela construção da escala, não verificado depois | OBRIG | — | Cor |
| `DSY-017` | Os pares de cor permitidos são declarados; combinação livre é proibida | OBRIG | — | Cor |
| `DSY-018` | O conjunto de cores de estado é fechado e semântico | OBRIG | — | Cor |
| `DSY-019` | Cada cor de estado é entregue com um portador não cromático | OBRIG | — | Cor |
| `DSY-020` | Tema é a troca da camada semântica, nunca a inversão do primitivo | OBRIG | — | Cor |
| `DSY-021` | Tema escuro não é o tema claro invertido | OBRIG | — | Cor |
| `DSY-022` | Superfície e elevação formam uma escala única de profundidade | OBRIG | — | Cor |
| `DSY-023` | O tema inicial respeita a preferência do sistema, e a escolha do usuário persiste | OBRIG | — | Cor |
| `DSY-024` | A escala de espaçamento tem base única e passos nomeados | OBRIG | — | Espaçamento e densidade |
| `DSY-025` | Proximidade codifica relação, e é por isso que espaço arbitrário destrói a leitura | OBRIG | — | Espaçamento e densidade |
| `DSY-026` | O espaçamento externo é responsabilidade do contêiner | RECOM | — | Espaçamento e densidade |
| `DSY-027` | Densidade é variante declarada do sistema | OBRIG | — | Espaçamento e densidade |
| `DSY-028` | A variante densa preserva o alvo de toque | OBRIG | — | Espaçamento e densidade |
| `DSY-029` | A escala tipográfica é fechada, com papel declarado por passo | OBRIG | — | Tipografia |
| `DSY-030` | Papel tipográfico e nível de cabeçalho são independentes | OBRIG | — | Tipografia |
| `DSY-031` | Altura de linha é proporcional ao tamanho, não fixa | OBRIG | — | Tipografia |
| `DSY-032` | A medida de linha é limitada | RECOM | — | Tipografia |
| `DSY-033` | O conjunto de pesos é fechado e efetivamente carregado | OBRIG | — | Tipografia |
| `DSY-034` | O texto escala com a preferência do usuário | OBRIG | — | Tipografia |
| `DSY-035` | Tamanho responsivo é interpolação declarada, não salto por ponto de quebra | RECOM | — | Tipografia |
| `DSY-036` | A fonte tem orçamento, e o texto é legível antes de ela chegar | OBRIG | — | Tipografia |
| `DSY-037` | O layout vem de grade declarada, não de posição arbitrária | OBRIG | — | Grade, contêiner e pontos de quebra |
| `DSY-038` | O ponto de quebra nomeia a necessidade do conteúdo, não o dispositivo | OBRIG | — | Grade, contêiner e pontos de quebra |
| `DSY-039` | O componente reage ao espaço que recebeu, não à largura da janela | RECOM | — | Grade, contêiner e pontos de quebra |
| `DSY-040` | Nenhuma primitiva de layout reordena o visual sem reordenar o documento | OBRIG | — | Grade, contêiner e pontos de quebra |
| `DSY-041` | Conjunto único, com grade e traço únicos | OBRIG | — | Ícones |
| `DSY-042` | O tamanho de ícone vem de uma escala alinhada à tipografia | OBRIG | — | Ícones |
| `DSY-043` | Ícone sozinho não identifica ação fora do conjunto convencional | OBRIG | — | Ícones |
| `DSY-044` | Um significado, um ícone, em todo o produto | OBRIG | — | Ícones |
| `DSY-045` | O raio é escala, e o passo carrega hierarquia | RECOM | — | Raio, borda e elevação |
| `DSY-046` | Sombra codifica distância do plano, e o separador tem mecanismo único por superfície | OBRIG | — | Raio, borda e elevação |
| `DSY-047` | Elevação e ordem de empilhamento saem da mesma tabela | OBRIG | — | Raio, borda e elevação |
| `DSY-048` | Duração e curva são tokens, com papel declarado | OBRIG | — | Movimento |
| `DSY-049` | A lista do que anima é fechada | OBRIG | — | Movimento |
| `DSY-050` | Nada anima entre a ação e a primeira evidência de resposta | OBRIG | — | Movimento |
| `DSY-051` | Movimento reduzido é uma variante completa do sistema, não a ausência de animação | OBRIG | — | Movimento |
| `DSY-052` | O esqueleto reproduz a forma real do conteúdo | RECOM | — | Movimento |
| `DSY-053` | Cada mecanismo de feedback tem critério de uso declarado | OBRIG | — | Feedback: a hierarquia dos mecanismos |
| `DSY-054` | Erro de campo é inline e permanente | OBRIG | `S2` | Feedback: a hierarquia dos mecanismos |
| `DSY-055` | Notificação transitória não carrega o que precisa ser relido | OBRIG | — | Feedback: a hierarquia dos mecanismos |
| `DSY-056` | Modal só para o que impede prosseguir | OBRIG | — | Feedback: a hierarquia dos mecanismos |
| `DSY-057` | Um mecanismo por evento, e a fila é limitada | RECOM | — | Feedback: a hierarquia dos mecanismos |
| `DSY-058` | Todo componente do catálogo tem anatomia declarada | OBRIG | — | Catálogo de componentes |
| `DSY-059` | A matriz variante × estado é enumerada e verificada | OBRIG | — | Catálogo de componentes |
| `DSY-060` | Nenhuma variante nasce sem regra de quando usar | OBRIG | — | Catálogo de componentes |
| `DSY-061` | Composição por padrão; configuração para o que é fechado | RECOM | — | Catálogo de componentes |
| `DSY-062` | Propriedade de escape é nomeada, rara e medida | OBRIG | — | Catálogo de componentes |
| `DSY-063` | Componente que envolve elemento nativo repassa propriedades e referência | OBRIG | — | Catálogo de componentes |
| `DSY-064` | Um caminho único de contribuição, com revisor nomeado | OBRIG | — | Governança |
| `DSY-065` | O que o produto precisa e o sistema não tem nasce local, com dono e prazo | OBRIG | — | Governança |
| `DSY-066` | Mudança de aparência é mudança incompatível | OBRIG | — | Governança |
| `DSY-067` | Depreciação tem substituto, prazo e uso medido | OBRIG | — | Governança |
| `DSY-068` | A divergência entre o sistema e a produção é medida, não presumida | OBRIG | — | Governança |
| `DSY-069` | O catálogo é executável e é a fonte de verdade da documentação | RECOM | — | Governança |

## 📙 Volume 10 — DevOps e SRE

Arquivo: [`10-devops.md`](10-devops.md) · 48 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `OPS-001` | Quando isso falhar, quanto tempo até sabermos e até voltarmos? | IMUT | — | - |
| `OPS-002` | Ordem de análise | OBRIG | — | - |
| `OPS-003` | Rollback é um comando documentado | OBRIG | — | Rollback |
| `OPS-004` | Rollback foi executado ao menos uma vez | OBRIG | — | Rollback |
| `OPS-005` | Qualquer pessoa do time consegue reverter | OBRIG | — | Rollback |
| `OPS-006` | Rollback inclui o caminho de dados | OBRIG | — | Rollback |
| `OPS-007` | Migração destrutiva nunca no mesmo deploy que mudança de comportamento | OBRIG | — | Rollback |
| `OPS-008` | Tempo de rollback é conhecido | RECOM | — | Rollback |
| `OPS-009` | Flag onde a faixa de risco exige | OBRIG | — | Rollback |
| `OPS-010` | Versões antiga e nova coexistem | OBRIG | — | Compatibilidade de deploy |
| `OPS-011` | Aditivo primeiro, remoção depois | OBRIG | — | Compatibilidade de deploy |
| `OPS-012` | Cliente que você não controla nunca é atualizado pelo seu deploy | OBRIG | — | Compatibilidade de deploy |
| `OPS-013` | Log correlacionável | OBRIG | — | Detecção e observabilidade |
| `OPS-014` | Log estruturado em campos | OBRIG | — | Detecção e observabilidade |
| `OPS-015` | Nível com significado | OBRIG | — | Detecção e observabilidade |
| `OPS-016` | Nenhum dado sensível em log | OBRIG | `S0` | Detecção e observabilidade |
| `OPS-017` | Erro registrado uma vez, onde há contexto | OBRIG | — | Detecção e observabilidade |
| `OPS-018` | As quatro métricas mínimas por serviço | OBRIG | — | Detecção e observabilidade |
| `OPS-019` | Métrica de negócio, não só técnica | OBRIG | — | Detecção e observabilidade |
| `OPS-020` | Rastreamento em fluxo distribuído | RECOM | — | Detecção e observabilidade |
| `OPS-021` | Um painel que responde "está tudo bem?" em dez segundos | RECOM | — | Detecção e observabilidade |
| `OPS-022` | Se a mudança pode falhar em silêncio, existe detecção | OBRIG | — | Detecção e observabilidade |
| `OPS-023` | Alerta é acionável ou não existe | OBRIG | — | Alertas |
| `OPS-024` | Alerte por sintoma, não por causa | RECOM | — | Alertas |
| `OPS-025` | Todo alerta tem runbook | OBRIG | — | Alertas |
| `OPS-026` | Ruído é falha de configuração | OBRIG | — | Alertas |
| `OPS-027` | Alerta tem responsável nomeado | OBRIG | — | Alertas |
| `OPS-028` | O pipeline bloqueia | OBRIG | — | CI/CD |
| `OPS-029` | Build reproduzível | OBRIG | — | CI/CD |
| `OPS-030` | Um artefato, vários ambientes | RECOM | — | CI/CD |
| `OPS-031` | Pipeline é código revisado | OBRIG | — | CI/CD |
| `OPS-032` | Nenhum segredo em log de pipeline | OBRIG | — | CI/CD |
| `OPS-033` | Pipeline rápido o suficiente para não ser contornado | RECOM | — | CI/CD |
| `OPS-034` | Varredura de dependências e de segredos automatizada | OBRIG | — | CI/CD |
| `OPS-035` | Verificação de saúde real | OBRIG | — | Deploy |
| `OPS-036` | Gradual quando o risco justifica | RECOM | — | Deploy |
| `OPS-037` | Deploy é rotina e frequente | RECOM | — | Deploy |
| `OPS-038` | Flags têm prazo e item de backlog | RECOM | — | Deploy |
| `OPS-039` | Validada na inicialização | OBRIG | — | Configuração |
| `OPS-040` | Toda diferença entre ambientes é documentada | OBRIG | — | Configuração |
| `OPS-041` | Segredos gerenciados e rotacionáveis sem deploy | OBRIG | — | Configuração |
| `OPS-042` | Restauração de backup testada em calendário | OBRIG | — | Recuperação e alta disponibilidade |
| `OPS-043` | Objetivos de recuperação declarados | OBRIG | — | Recuperação e alta disponibilidade |
| `OPS-044` | Modo degradado definido por dependência | RECOM | — | Recuperação e alta disponibilidade |
| `OPS-045` | Nenhum ponto único de falha não declarado | RECOM | — | Recuperação e alta disponibilidade |
| `OPS-046` | Capacidade conhecida sob volume de produção | RECOM | — | Recuperação e alta disponibilidade |
| `OPS-047` | Incidente gera aprendizado registrado | RECOM | — | Recuperação e alta disponibilidade |
| `OPS-048` | Incidente ativo interrompe a rodada | OBRIG | — | Recuperação e alta disponibilidade |

## 📗 Volume 11 — QA e Testes

Arquivo: [`11-qa.md`](11-qa.md) · 40 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `QAT-001` | Um teste existe para detectar que algo importante quebrou | IMUT | — | - |
| `QAT-002` | Perseguir percentual de cobertura é antipadrão | IMUT | — | - |
| `QAT-003` | Teste comportamento, não implementação | OBRIG | — | Qualidade do teste |
| `QAT-004` | Todo teste novo deve falhar antes | OBRIG | — | Qualidade do teste |
| `QAT-005` | Determinístico | OBRIG | — | Qualidade do teste |
| `QAT-006` | Teste intermitente é pior do que teste ausente | OBRIG | — | Qualidade do teste |
| `QAT-007` | `retry` não é correção | OBRIG | — | Qualidade do teste |
| `QAT-008` | Nunca afrouxe a asserção para passar | OBRIG | `S1` | Qualidade do teste |
| `QAT-009` | Nome descreve o cenário | OBRIG | — | Qualidade do teste |
| `QAT-010` | Um motivo de falha por teste | RECOM | — | Qualidade do teste |
| `QAT-011` | Sem lógica no teste | RECOM | — | Qualidade do teste |
| `QAT-012` | Mensagem de falha no vocabulário do domínio | RECOM | — | Qualidade do teste |
| `QAT-013` | Simule fronteiras, não o próprio código | RECOM | — | Qualidade do teste |
| `QAT-014` | Dados de teste explícitos | RECOM | — | Qualidade do teste |
| `QAT-015` | Snapshot lido, nunca aprovado em massa | OBRIG | — | Qualidade do teste |
| `QAT-016` | Mapeie o que não pode quebrar | OBRIG | — | Cobertura que importa |
| `QAT-017` | Cobertura por casos declarados de cada regra | OBRIG | — | Cobertura que importa |
| `QAT-018` | Regra de negócio crítica sem teste é `S1` | OBRIG | — | Cobertura que importa |
| `QAT-019` | Caminho de erro é testado | OBRIG | — | Cobertura que importa |
| `QAT-020` | Bordas obrigatórias | OBRIG | — | Cobertura que importa |
| `QAT-021` | Arredondamento de dinheiro testado explicitamente | OBRIG | — | Cobertura que importa |
| `QAT-022` | Bordas por tabela ou propriedade, não por exemplos avulsos | RECOM | — | Cobertura que importa |
| `QAT-023` | Proporção é orientação, risco é o que decide | RECOM | — | Estrutura da suíte |
| `QAT-024` | Regra de negócio testável sem infraestrutura | OBRIG | — | Estrutura da suíte |
| `QAT-025` | Pelo menos um teste do caminho crítico ponta a ponta | RECOM | — | Estrutura da suíte |
| `QAT-026` | Teste de contrato onde há consumidor externo | RECOM | — | Estrutura da suíte |
| `QAT-027` | Suíte rápida o suficiente para ser usada | RECOM | — | Estrutura da suíte |
| `QAT-028` | Teste de concorrência onde há recurso escasso | OBRIG | — | Estrutura da suíte |
| `QAT-029` | Teste que conta consultas onde N+1 foi corrigido | RECOM | — | Estrutura da suíte |
| `QAT-030` | Bug corrigido ganha teste que reproduz o defeito | OBRIG | — | Regressão |
| `QAT-031` | Reincidência de defeito: o achado é o teste ausente | OBRIG | — | Regressão |
| `QAT-032` | Nenhum teste desabilitado sem ID de backlog | OBRIG | — | Regressão |
| `QAT-033` | Teste de regressão antes da mudança de risco `R3`/`R4` | OBRIG | — | Regressão |
| `QAT-034` | Critério de aceite é verificável | OBRIG | — | Critérios de aceite |
| `QAT-035` | Critério de aceite inclui os caminhos infelizes | OBRIG | — | Critérios de aceite |
| `QAT-036` | Critério de aceite inclui o que **não** deve acontecer | RECOM | — | Critérios de aceite |
| `QAT-037` | Aceite não passa sem a Definition of Done | OBRIG | — | Critérios de aceite |
| `QAT-038` | Nunca escreva asserção para comportamento não confirmado | IMUT | — | Limites do papel |
| `QAT-039` | Não exija teste de código trivial | OBRIG | — | Limites do papel |
| `QAT-040` | Não bloqueie por percentual | IMUT | — | Limites do papel |

## 📕 Volume 12 — Auditoria Técnica

Arquivo: [`12-auditoria.md`](12-auditoria.md) · 42 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `AUD-001` | As duas falhas simétricas da revisão | IMUT | — | - |
| `AUD-002` | Afirmação é tratada como não verificada até haver evidência | IMUT | — | - |
| `AUD-003` | Quem auditou não implementou | IMUT | — | - |
| `AUD-004` | Limites por PR | OBRIG | — | Orçamento de mudança |
| `AUD-005` | Estourar o limite exige justificativa | OBRIG | — | Orçamento de mudança |
| `AUD-006` | Pare no primeiro nível que reprova | OBRIG | — | Ordem da revisão |
| `AUD-007` | Escopo errado é um único comentário | OBRIG | — | Ordem da revisão |
| `AUD-008` | Todo comentário declara sua força | OBRIG | — | Como comentar |
| `AUD-009` | Todo `MUST` tem onde, qual consequência e como corrigir | OBRIG | — | Como comentar |
| `AUD-010` | Máximo de 3 `NIT` por PR | OBRIG | — | Como comentar |
| `AUD-011` | Não redesenhe o PR | OBRIG | — | Como comentar |
| `AUD-012` | Não peça mudança sem consequência | OBRIG | — | Como comentar |
| `AUD-013` | Não exija o que não estava lá antes | OBRIG | — | Como comentar |
| `AUD-014` | Elogie o que quer ver repetido | RECOM | — | Como comentar |
| `AUD-015` | Você não pode submeter um diff que não leu por completo | IMUT | — | Autorrevisão |
| `AUD-016` | Rodar a Definition of Done antes de submeter | OBRIG | — | Autorrevisão |
| `AUD-017` | Descrição de PR completa | OBRIG | — | Autorrevisão |
| `AUD-018` | Leia o diff do conjunto, não das partes | OBRIG | — | Caça a regressões |
| `AUD-019` | As doze fontes de regressão | OBRIG | — | Caça a regressões |
| `AUD-020` | A inspeção de maior rendimento é o teste alterado | OBRIG | — | Caça a regressões |
| `AUD-021` | Verifique dado existente contra regra nova | OBRIG | — | Caça a regressões |
| `AUD-022` | Cada arquivo do diff corresponde a uma proposta aprovada | OBRIG | — | Integridade do escopo |
| `AUD-023` | Escopo não aprovado não é queixa de processo | IMUT | — | Integridade do escopo |
| `AUD-024` | Verifique também as remoções | OBRIG | — | Integridade do escopo |
| `AUD-025` | Nenhuma dependência nova não prevista | OBRIG | — | Integridade do escopo |
| `AUD-026` | Nenhuma formatação em massa dentro de commit de lógica | OBRIG | — | Integridade do escopo |
| `AUD-027` | Pesos por dimensão | OBRIG | — | Notas |
| `AUD-028` | Escala | OBRIG | — | Notas |
| `AUD-029` | Ausência de problemas não é excelência | IMUT | — | Notas |
| `AUD-030` | Travas obrigatórias | IMUT | — | Notas |
| `AUD-031` | Os quatro vereditos | OBRIG | — | Veredito |
| `AUD-032` | O veredito vem na primeira linha | OBRIG | — | Veredito |
| `AUD-033` | Rejeição por violação de processo é legítima | IMUT | — | Veredito |
| `AUD-034` | O auditor não adiciona achados de preferência própria | OBRIG | — | Veredito |
| `AUD-035` | Conferência obrigatória: reportadas versus registradas | OBRIG | — | Backlog |
| `AUD-036` | Toda entrada tem gatilho de promoção | OBRIG | — | Backlog |
| `AUD-037` | Dívida deliberada tem os cinco campos | OBRIG | — | Backlog |
| `AUD-038` | Regra das três postergações | OBRIG | — | Backlog |
| `AUD-039` | `não faremos` é estado saudável | RECOM | — | Backlog |
| `AUD-040` | Higiene periódica | OBRIG | — | Backlog |
| `AUD-041` | Riscos específicos verificados explicitamente | OBRIG | — | Código gerado por IA |
| `AUD-042` | Exija a evidência, não a narrativa | IMUT | — | Código gerado por IA |

## 📕 Volume 13 — Revisão de Código

Arquivo: [`13-revisao-de-codigo.md`](13-revisao-de-codigo.md) · 58 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `REV-001` | A revisão de PR não substitui teste, medição nem auditoria de módulo | IMUT | — | O que a revisão encontra e o que ela não encontra |
| `REV-002` | O que a revisão encontra bem | OBRIG | — | O que a revisão encontra e o que ela não encontra |
| `REV-003` | O que a revisão comprovadamente não encontra | OBRIG | — | O que a revisão encontra e o que ela não encontra |
| `REV-004` | Todo PR declara o que **não** foi verificado | RECOM | — | O que a revisão encontra e o que ela não encontra |
| `REV-005` | Não leia o diff de cima para baixo como padrão | OBRIG | — | Ordem de leitura |
| `REV-006` | Comece pela descrição; se ela for vaga, pare | OBRIG | — | Ordem de leitura |
| `REV-007` | Leia os testes antes do código de produção | OBRIG | — | Ordem de leitura |
| `REV-008` | Migração antes do código que a assume | OBRIG | — | Ordem de leitura |
| `REV-009` | O que só se vê no diff | OBRIG | — | Ordem de leitura |
| `REV-010` | O que só se vê no arquivo inteiro | OBRIG | — | Ordem de leitura |
| `REV-011` | Abra os arquivos irmãos quando o PR toca regra de negócio | RECOM | — | Ordem de leitura |
| `REV-012` | Respeite o orçamento de `AUD-004`; acima dele, peça decomposição | OBRIG | — | Tamanho, ritmo e composição do PR |
| `REV-013` | Formatação e comportamento nunca no mesmo commit | IMUT | — | Tamanho, ritmo e composição do PR |
| `REV-014` | Refatoração mecânica e mudança de comportamento são PRs separados | OBRIG | — | Tamanho, ritmo e composição do PR |
| `REV-015` | Dependência nova exige justificativa no PR | OBRIG | — | Tamanho, ritmo e composição do PR |
| `REV-016` | Arquivos gerados e lockfiles não contam no orçamento **se** estão sozinhos no commit | RECOM | — | Tamanho, ritmo e composição do PR |
| `REV-017` | PR que "só move arquivos" ainda precisa de revisão de fronteira | OBRIG | — | Tamanho, ritmo e composição do PR |
| `REV-018` | Todo comentário declara a força | OBRIG | — | Comentário útil |
| `REV-019` | `MUST` cita a regra ou o defeito concreto | OBRIG | — | Comentário útil |
| `REV-020` | Não discuta decisão já registrada no ADR no thread do PR | OBRIG | — | Comentário útil |
| `REV-021` | Sugestão de código no comentário é `CONSIDER` ou patch anexado, nunca reescrita silenciosa | OBRIG | — | Comentário útil |
| `REV-022` | Máximo de 3 `NIT` por PR | OBRIG | — | Comentário útil |
| `REV-023` | Discordar com alternativa e custo | OBRIG | — | Comentário útil |
| `REV-024` | Ceder também se registra | RECOM | — | Comentário útil |
| `REV-025` | Elogio específico ou nenhum | RECOM | — | Comentário útil |
| `REV-026` | O teste falharia se a regra fosse removida? | OBRIG | — | Revisão de teste |
| `REV-027` | Teste que só cobre o caminho feliz em mudança de regra é incompleto | OBRIG | — | Revisão de teste |
| `REV-028` | Não aprove teste que congela comportamento sem o revisor saber se está certo | IMUT | — | Revisão de teste |
| `REV-029` | Snapshot e golden file exigem justificativa | RECOM | — | Revisão de teste |
| `REV-030` | Teste flaky no PR é `MUST`, não "vamos ver no CI" | OBRIG | — | Revisão de teste |
| `REV-031` | Migração sem reversa executada é incompleta | OBRIG | — | Revisão de migração e de dados |
| `REV-032` | Conte registros que violam a nova regra | OBRIG | — | Revisão de migração e de dados |
| `REV-033` | Aditivo primeiro; destrutivo em fase própria | OBRIG | — | Revisão de migração e de dados |
| `REV-034` | Migração de dados é `R4` até prova em contrário | OBRIG | — | Revisão de migração e de dados |
| `REV-035` | Verifique bloqueio de tabela na versão do banco em uso | OBRIG | — | Revisão de migração e de dados |
| `REV-036` | Qualquer superfície nova nasce inacessível até autorização declarada | OBRIG | `S0` | Segurança, contrato e operação no PR |
| `REV-037` | Diff que toca dado de usuário, dinheiro ou permissão exige revisor de segurança ou checklist OWASP | OBRIG | — | Segurança, contrato e operação no PR |
| `REV-038` | Mudança de contrato público sem versão ou compatibilidade é `MUST` | OBRIG | — | Segurança, contrato e operação no PR |
| `REV-039` | O PR declara como se detecta falha em produção e como se reverte | OBRIG | — | Segurança, contrato e operação no PR |
| `REV-040` | Feature flag sem plano de remoção é dívida disfarçada | RECOM | — | Segurança, contrato e operação no PR |
| `REV-041` | Trate saída de IA como entrada não confiável de alta plausibilidade | IMUT | — | Código gerado por IA |
| `REV-042` | Volume alto de PR gerado não reduz o padrão de revisão | OBRIG | — | Código gerado por IA |
| `REV-043` | Exija que o autor explique a intenção em linguagem de negócio | OBRIG | — | Código gerado por IA |
| `REV-044` | Procure o padrão colado sem a proteção do original | OBRIG | — | Código gerado por IA |
| `REV-045` | Testes gerados por IA passam no mesmo crivo `REV-026` | OBRIG | — | Código gerado por IA |
| `REV-046` | Bloqueie por defeito, contrato, segurança, dado ou teste que não prova | OBRIG | — | Quando bloquear, quando aprovar, pressão |
| `REV-047` | Aprovar com comentários abertos só se nenhum for `MUST` | OBRIG | — | Quando bloquear, quando aprovar, pressão |
| `REV-048` | Pressão de prazo não rebaixa `S0`/`S1` nem `R4` | IMUT | — | Quando bloquear, quando aprovar, pressão |
| `REV-049` | Autoaprovação só com regra explícita no perfil do projeto | OBRIG | — | Quando bloquear, quando aprovar, pressão |
| `REV-050` | Tempo de resposta de revisão é métrica de fluxo, não de virtude | RECOM | — | Quando bloquear, quando aprovar, pressão |
| `REV-051` | Quando o código está certo e a abordagem está errada, um `MUST` de escopo | OBRIG | — | Quando bloquear, quando aprovar, pressão |
| `REV-052` | Segunda revisão após mudança substancial | OBRIG | — | Quando bloquear, quando aprovar, pressão |
| `REV-053` | Quem implementou não aprova o próprio PR em mudança `R3`/`R4` | IMUT | — | O revisor |
| `REV-054` | Revisor declara o que não olhou | OBRIG | — | O revisor |
| `REV-055` | Bikeshedding é falha do revisor, não do autor | OBRIG | — | O revisor |
| `REV-056` | Revisão que só olha estilo é revisão não feita | OBRIG | — | O revisor |
| `REV-057` | Não use o PR para ensinar carreira | RECOM | — | O revisor |
| `REV-058` | Checklist marcado sem evidência não conta | IMUT | — | O revisor |

## 📒 Volume 14 — Escala e Multi-Inquilino

Arquivo: [`14-escalabilidade.md`](14-escalabilidade.md) · 42 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `ESC-001` | Escala é sempre resposta a um número, nunca a uma ambição | IMUT | — | A disciplina de escalar |
| `ESC-002` | A ordem de intervenção é fixa | OBRIG | — | A disciplina de escalar |
| `ESC-003` | Aumentar infraestrutura não é correção | OBRIG | — | A disciplina de escalar |
| `ESC-004` | Toda decisão estrutural declara a condição de invalidação | OBRIG | — | A disciplina de escalar |
| `ESC-005` | Normalize por padrão | OBRIG | — | Normalizar e desnormalizar |
| `ESC-006` | Desnormalizar é decisão com quatro respostas obrigatórias | OBRIG | — | Normalizar e desnormalizar |
| `ESC-007` | Desnormalização exige detecção de divergência | OBRIG | — | Normalizar e desnormalizar |
| `ESC-008` | Dado histórico é cópia legítima, não desnormalização | RECOM | — | Normalizar e desnormalizar |
| `ESC-009` | Contador agregado precisa de estratégia de concorrência | OBRIG | — | Normalizar e desnormalizar |
| `ESC-010` | Visão materializada declara a janela de obsolescência | RECOM | — | Normalizar e desnormalizar |
| `ESC-011` | Réplica introduz atraso, e o atraso é visível | OBRIG | — | Réplicas de leitura |
| `ESC-012` | Classifique cada leitura por tolerância a atraso | OBRIG | — | Réplicas de leitura |
| `ESC-013` | Atraso de replicação é monitorado com alerta | OBRIG | — | Réplicas de leitura |
| `ESC-014` | Réplica não é backup | OBRIG | — | Réplicas de leitura |
| `ESC-015` | Roteamento de leitura é explícito, nunca implícito | RECOM | — | Réplicas de leitura |
| `ESC-016` | Particione quando o problema é o conjunto quente, não o total | RECOM | — | Particionamento e sharding |
| `ESC-017` | A chave de partição precisa aparecer nas consultas | OBRIG | — | Particionamento e sharding |
| `ESC-018` | Retenção e arquivamento antes de particionar | RECOM | — | Particionamento e sharding |
| `ESC-019` | Sharding é o último recurso, e exige as cinco respostas | OBRIG | — | Particionamento e sharding |
| `ESC-020` | Chave de fragmentação errada é praticamente irreversível | IMUT | — | Particionamento e sharding |
| `ESC-021` | Sharding e integridade referencial não coexistem bem | OBRIG | — | Particionamento e sharding |
| `ESC-022` | Sem estado em memória do processo | OBRIG | — | Estado e escala horizontal |
| `ESC-023` | Nenhuma afinidade de sessão como requisito | RECOM | — | Estado e escala horizontal |
| `ESC-024` | Trabalho agendado roda uma vez, não uma vez por instância | OBRIG | — | Estado e escala horizontal |
| `ESC-025` | Trava distribuída tem expiração e trata perda | OBRIG | — | Estado e escala horizontal |
| `ESC-026` | Arquivo em disco local não sobrevive | OBRIG | — | Estado e escala horizontal |
| `ESC-027` | Pool de conexões dimensionado pelo total, não por instância | OBRIG | — | Estado e escala horizontal |
| `ESC-028` | Todo recurso tem limite explícito | OBRIG | — | Contrapressão e descarte de carga |
| `ESC-029` | Rejeitar rápido é melhor que aceitar e morrer | OBRIG | — | Contrapressão e descarte de carga |
| `ESC-030` | Fila com limite e política de descarte declarada | OBRIG | — | Contrapressão e descarte de carga |
| `ESC-031` | Interromper trabalho abandonado | RECOM | — | Contrapressão e descarte de carga |
| `ESC-032` | Disjuntor em dependência que pode ficar lenta | RECOM | — | Contrapressão e descarte de carga |
| `ESC-033` | Priorize tráfego quando saturado | RECOM | — | Contrapressão e descarte de carga |
| `ESC-034` | Limite de taxa por sujeito, não global | OBRIG | — | Contrapressão e descarte de carga |
| `ESC-035` | Capacidade conhecida por teste, não por inferência | RECOM | — | Contrapressão e descarte de carga |
| `ESC-036` | Escolha o modelo de isolamento com critério declarado | OBRIG | — | Multi-inquilino |
| `ESC-037` | Mudar de modelo depois é migração de dados | OBRIG | — | Multi-inquilino |
| `ESC-038` | Isolamento aplicado no ponto mais interno possível | OBRIG | `S0` | Multi-inquilino |
| `ESC-039` | O inquilino vem do contexto autenticado, nunca da requisição | OBRIG | `S0` | Multi-inquilino |
| `ESC-040` | Toda chave de cache e de busca inclui o inquilino | OBRIG | `S0` | Multi-inquilino |
| `ESC-041` | Vizinho ruidoso é contido por cota | OBRIG | — | Multi-inquilino |
| `ESC-042` | Operações por inquilino precisam existir desde cedo | RECOM | — | Multi-inquilino |

## 📙 Volume 15 — APIs

Arquivo: [`15-apis.md`](15-apis.md) · 58 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `API-001` | Toda API pública tem dono, consumidores conhecidos e política de compatibilidade | OBRIG | — | API como produto |
| `API-002` | Distinga API pública, parceiro e interna — por escrito | OBRIG | — | API como produto |
| `API-003` | O modelo de recurso não é o modelo de tabela | OBRIG | — | API como produto |
| `API-004` | Estabilidade do identificador é parte do contrato | OBRIG | — | API como produto |
| `API-005` | Erros de projeto que só aparecem com consumidores | OBRIG | — | API como produto |
| `API-006` | Recurso é substantivo; ação arriscada vira sub-recurso ou comando explícito | OBRIG | — | REST e recursos |
| `API-007` | Semântica de método é parte do contrato | OBRIG | — | REST e recursos |
| `API-008` | Coleções têm forma estável | OBRIG | — | REST e recursos |
| `API-009` | Hipermídia é opcional; links documentados para ações principais são recomendados | RECOM | — | REST e recursos |
| `API-010` | Quando não usar REST puro | RECOM | — | REST e recursos |
| `API-011` | GraphQL é contrato de schema, não "REST flexível" | OBRIG | — | GraphQL no contrato |
| `API-012` | Escolha GraphQL por necessidade de forma de leitura divergente, não por moda | RECOM | — | GraphQL no contrato |
| `API-013` | Nullability e depreciação no schema são decisões irreversíveis na prática | OBRIG | — | GraphQL no contrato |
| `API-014` | Limite de profundidade e custo faz parte do contrato publicado | OBRIG | — | GraphQL no contrato |
| `API-015` | Erro é contrato: código estável, mensagem, campo, correlação | OBRIG | — | Formato de erro |
| `API-016` | Status HTTP alinhado à classe de erro, nunca 200 com falha escondida em REST | OBRIG | — | Formato de erro |
| `API-017` | Não vaze detalhe interno na mensagem pública | OBRIG | — | Formato de erro |
| `API-018` | Catálogo de códigos de erro versionado com a API | RECOM | — | Formato de erro |
| `API-019` | Toda coleção listável é paginada com limite do servidor | OBRIG | — | Paginação, filtro e ordenação |
| `API-020` | Escolha offset vs cursor com critério declarado | OBRIG | — | Paginação, filtro e ordenação |
| `API-021` | Cursor é opaco para o cliente | OBRIG | — | Paginação, filtro e ordenação |
| `API-022` | Ordenação só por campos allowlisted | OBRIG | — | Paginação, filtro e ordenação |
| `API-023` | Filtro é allowlist de campos e operadores | OBRIG | — | Paginação, filtro e ordenação |
| `API-024` | Resposta declara a paginação de forma consistente | OBRIG | — | Paginação, filtro e ordenação |
| `API-025` | Política de versionamento publicada antes do segundo consumidor | OBRIG | — | Versionamento e evolução |
| `API-026` | O que é mudança compatível | OBRIG | — | Versionamento e evolução |
| `API-027` | O que é mudança incompatível | OBRIG | — | Versionamento e evolução |
| `API-028` | Prefira evolução aditiva a versão nova | RECOM | — | Versionamento e evolução |
| `API-029` | Duas versões simultâneas no máximo, salvo contrato de parceiro | RECOM | — | Versionamento e evolução |
| `API-030` | Campo novo opcional não quebra; campo novo usado sem default no servidor pode quebrar escrita | OBRIG | — | Versionamento e evolução |
| `API-031` | Depreciação anuncia, mede, remove — nessa ordem | OBRIG | — | Depreciação |
| `API-032` | Cabeçalho e documentação marcam o depreciado | OBRIG | — | Depreciação |
| `API-033` | Prazo de sunset publicado e cumprido | OBRIG | — | Depreciação |
| `API-034` | Medição de uso por campo/endpoint antes de remover | OBRIG | — | Depreciação |
| `API-035` | Exceção de remoção antecipada só com aceitação de risco nomeada | OBRIG | — | Depreciação |
| `API-036` | Código de erro e valor de enum depreciados seguem o mesmo rito | OBRIG | — | Depreciação |
| `API-037` | Limite de taxa é publicado: cota, janela, resposta, cabeçalhos | OBRIG | — | Limite de taxa e autenticação do consumidor |
| `API-038` | Limite por sujeito autenticado, não só por IP | OBRIG | — | Limite de taxa e autenticação do consumidor |
| `API-039` | Autenticação de API documentada no nível do consumidor | OBRIG | — | Limite de taxa e autenticação do consumidor |
| `API-040` | Escopos mínimos por operação | OBRIG | — | Limite de taxa e autenticação do consumidor |
| `API-041` | Ambiente de teste isolado com dados de teste | RECOM | — | Limite de taxa e autenticação do consumidor |
| `API-042` | Documentação executável deriva do contrato, não de wiki paralela | OBRIG | — | Documentação e SDK |
| `API-043` | Exemplos na documentação são válidos e testados no CI | OBRIG | — | Documentação e SDK |
| `API-044` | Documente autenticação, erros, paginação e limites na primeira página útil | OBRIG | — | Documentação e SDK |
| `API-045` | SDK oficial, se existir, versiona junto com a política da API | RECOM | — | Documentação e SDK |
| `API-046` | Cliente gerado a partir do schema; não mantenha modelos à mão em paralelo | RECOM | — | Documentação e SDK |
| `API-047` | Changelog de API legível por humanos e por máquina | RECOM | — | Documentação e SDK |
| `API-048` | Webhook de saída tem contrato: eventos, payload, assinatura, reentrega | OBRIG | — | Webhooks como produto |
| `API-049` | Evento novo é aditivo; mudança de payload de evento existente é versionada | OBRIG | — | Webhooks como produto |
| `API-050` | Assinante consegue verificar, inspecionar entregas e reenviar | RECOM | — | Webhooks como produto |
| `API-051` | Documente ordem não garantida e at-least-once | OBRIG | — | Webhooks como produto |
| `API-052` | Teste de contrato tem dono e roda no CI do provedor e do consumidor quando possível | OBRIG | — | Teste de contrato |
| `API-053` | Contrato testa o que é publicado, não o comportamento interno completo | OBRIG | — | Teste de contrato |
| `API-054` | Breaking change detectada no CI bloqueia o merge | OBRIG | — | Teste de contrato |
| `API-055` | Ambientes de contrato (mock/sandbox) refletem o schema atual | RECOM | — | Teste de contrato |
| `API-056` | Métricas por rota e por código de erro estável | OBRIG | — | Observabilidade e operação do contrato |
| `API-057` | Compatibilidade durante deploy: cliente antigo e novo contra servidor novo | OBRIG | — | Observabilidade e operação do contrato |
| `API-058` | Idempotência documentada onde o cliente retenta | OBRIG | — | Observabilidade e operação do contrato |

## 📒 Volume 16 — Multi-Tenant

Arquivo: [`16-multi-tenant.md`](16-multi-tenant.md) · 58 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `MTN-001` | Defina inquilino em linguagem de produto antes do schema | IMUT | — | O que é um inquilino |
| `MTN-002` | Separe organização, faturamento e workspace quando os ciclos de vida divergem | OBRIG | — | O que é um inquilino |
| `MTN-003` | Hierarquia entre inquilinos é explícita ou inexistente | OBRIG | — | O que é um inquilino |
| `MTN-004` | Ambiente sandbox não é o inquilino de produção com flag | OBRIG | — | O que é um inquilino |
| `MTN-005` | O identificador de inquilino é estável e não reutilizado | OBRIG | — | O que é um inquilino |
| `MTN-006` | Escolha o modelo com ADR e critério de promoção | OBRIG | — | Modelo de isolamento |
| `MTN-007` | Schema compartilhado exige política no banco ou camada de acesso obrigatória | OBRIG | `S0` | Modelo de isolamento |
| `MTN-008` | Schema por inquilino: migração é frota | OBRIG | — | Modelo de isolamento |
| `MTN-009` | Banco por inquilino: restore e compliance individuais são o benefício que se compra | RECOM | — | Modelo de isolamento |
| `MTN-010` | Híbrido (shared + dedicated) declara o critério de upgrade | OBRIG | — | Modelo de isolamento |
| `MTN-011` | Mudança de modelo entre isolamentos é projeto, não tarefa | OBRIG | — | Modelo de isolamento |
| `MTN-012` | Inquilino ativo vem do contexto autenticado, nunca do body/query livre | IMUT | `S0` | Identidade e contexto |
| `MTN-013` | Usuário multi-inquilino tem membership explícito e troca de contexto auditada | OBRIG | — | Identidade e contexto |
| `MTN-014` | Token e sessão amarram o inquilino atual | OBRIG | — | Identidade e contexto |
| `MTN-015` | Convenções de subdomínio/domínio customizado resolvem para tenant no edge, com prova | OBRIG | — | Identidade e contexto |
| `MTN-016` | Impersonação de suporte é privilegiada, temporária e registrada | OBRIG | `S1` | Identidade e contexto |
| `MTN-017` | Inventário obrigatório dos caminhos fora da query | OBRIG | — | Onde o isolamento vaza |
| `MTN-018` | Busca full-text e embeddings filtram por tenant na recuperação | OBRIG | `S0` | Onde o isolamento vaza |
| `MTN-019` | Objeto em storage: path ou metadata com tenant + URL assinada | OBRIG | `S0` | Onde o isolamento vaza |
| `MTN-020` | Mensagem de fila carrega tenant_id e o consumidor não aceita override | OBRIG | — | Onde o isolamento vaza |
| `MTN-021` | E-mail e notificação não cruzam dado de outro tenant no template | OBRIG | — | Onde o isolamento vaza |
| `MTN-022` | Log e suporte: query por tenant sem expor outros no mesmo painel por default | OBRIG | — | Onde o isolamento vaza |
| `MTN-023` | Relatório e export assíncronos herdam o tenant do solicitante no momento da criação | OBRIG | — | Onde o isolamento vaza |
| `MTN-024` | Papéis são por membership, não globais por padrão | OBRIG | — | Autorização dentro e entre inquilinos |
| `MTN-025` | Autorização por objeto continua obrigatória dentro do tenant | OBRIG | `S0` | Autorização dentro e entre inquilinos |
| `MTN-026` | Endpoints de plataforma (super-admin) são superfície separada | OBRIG | — | Autorização dentro e entre inquilinos |
| `MTN-027` | Convite cria membership com expiração e papel mínimo | OBRIG | — | Autorização dentro e entre inquilinos |
| `MTN-028` | Provisionar é uma transação de produto com estados | OBRIG | — | Provisionamento e desprovisionamento |
| `MTN-029` | Suspensão bloqueia escrita e efeitos externos, não só o login | OBRIG | — | Provisionamento e desprovisionamento |
| `MTN-030` | Eliminação é processo, não DELETE cascade na raiva | OBRIG | — | Provisionamento e desprovisionamento |
| `MTN-031` | Desprovisionamento verifica resíduos nos caminhos do inventário `MTN-017` | OBRIG | — | Provisionamento e desprovisionamento |
| `MTN-032` | Reativação após suspensão é explícita; após hard delete, é novo tenant | OBRIG | — | Provisionamento e desprovisionamento |
| `MTN-033` | Customização por configuração, não por fork de código por tenant | OBRIG | — | Customização |
| `MTN-034` | Campo customizado tem tipo, validação e cota | OBRIG | — | Customização |
| `MTN-035` | Domínio customizado: TLS, verificação de posse, rollback | OBRIG | — | Customização |
| `MTN-036` | Tema/branding não remove contraste nem estados de foco | OBRIG | — | Customização |
| `MTN-037` | Limite: customização que exige regra de negócio divergente é produto separado ou recusa | RECOM | — | Customização |
| `MTN-038` | Cotas por tenant em API, jobs, storage e busca | OBRIG | — | Vizinho ruidoso e inquilino grande |
| `MTN-039` | Fair scheduling em filas multi-tenant | RECOM | — | Vizinho ruidoso e inquilino grande |
| `MTN-040` | Detecte o tenant grande antes que ele force sharding de pânico | OBRIG | — | Vizinho ruidoso e inquilino grande |
| `MTN-041` | Hot key de tenant: plano de mitigação declarado | OBRIG | — | Vizinho ruidoso e inquilino grande |
| `MTN-042` | Teste de carga multi-tenant inclui vizinho ruidoso | RECOM | — | Vizinho ruidoso e inquilino grande |
| `MTN-043` | Exportação completa por tenant é requisito desde cedo | OBRIG | — | Dados, exportação e faturamento |
| `MTN-044` | Restauração de um tenant não reescreve os outros | OBRIG | — | Dados, exportação e faturamento |
| `MTN-045` | Medição de uso para billing é append-only e reconciliável | OBRIG | — | Dados, exportação e faturamento |
| `MTN-046` | Fatura e uso são do tenant de faturamento, não do workspace filho sem regra | OBRIG | — | Dados, exportação e faturamento |
| `MTN-047` | Inadimplência: degradação controlada, não delete imediato | OBRIG | — | Dados, exportação e faturamento |
| `MTN-048` | Todo teste de feature multi-tenant usa pelo menos dois tenants | OBRIG | — | Testes e operação |
| `MTN-049` | Teste de regressão de isolamento para cache e busca | OBRIG | — | Testes e operação |
| `MTN-050` | Proibido tenant de teste permanente em produção com dado real misturado | OBRIG | — | Testes e operação |
| `MTN-051` | Runbook: vazamento entre tenants | OBRIG | — | Testes e operação |
| `MTN-052` | Migração de schema em frota (schema-por-tenant) tem canário e progresso | OBRIG | — | Testes e operação |
| `MTN-053` | Backup prova restore de um tenant no modelo escolhido | OBRIG | — | Testes e operação |
| `MTN-054` | Todo log e métrica de request carregam tenant_id quando houver contexto | OBRIG | — | Observabilidade multi-tenant |
| `MTN-055` | Alertas de saturação por tenant, não só globais | RECOM | — | Observabilidade multi-tenant |
| `MTN-056` | Painel de uso por tenant para suporte e success | RECOM | — | Observabilidade multi-tenant |
| `MTN-057` | Onboarding declara o que o tenant isola e o que é compartilhado (catálogo global, etc.) | RECOM | — | Produto e limites |
| `MTN-058` | Recusar requisito que quebra isolamento em nome de conveniência | OBRIG | — | Produto e limites |

## 📓 Volume 17 — Observabilidade

Arquivo: [`17-observabilidade.md`](17-observabilidade.md) · 70 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `OBS-001` | Observabilidade é a capacidade de responder à pergunta que ninguém previu | IMUT | — | Monitorar e observar |
| `OBS-002` | Toda instrumentação nasce de uma pergunta escrita | OBRIG | — | Monitorar e observar |
| `OBS-003` | Contexto de alta cardinalidade é o que separa observar de monitorar | OBRIG | — | Monitorar e observar |
| `OBS-004` | Telemetria nunca está no caminho crítico da requisição | OBRIG | — | Monitorar e observar |
| `OBS-005` | Instrumentação entra na mesma mudança, não em uma rodada posterior | OBRIG | — | Monitorar e observar |
| `OBS-006` | Cada sinal responde bem a uma pergunta e mal às outras | OBRIG | — | Os três sinais |
| `OBS-007` | A ordem de consulta em incidente é métrica, trace, log | RECOM | — | Os três sinais |
| `OBS-008` | Os três sinais compartilham um vocabulário de campo único | OBRIG | — | Os três sinais |
| `OBS-009` | O schema de log é declarado e verificado, não emergente | OBRIG | — | Log estruturado em profundidade |
| `OBS-010` | Nome de evento é fato no passado, de conjunto enumerável | OBRIG | — | Log estruturado em profundidade |
| `OBS-011` | Uma linha canônica por unidade de trabalho | RECOM | — | Log estruturado em profundidade |
| `OBS-012` | O que nunca entra no log | OBRIG | — | Log estruturado em profundidade |
| `OBS-013` | Nome e tipo de campo são estáveis para sempre | OBRIG | — | Log estruturado em profundidade |
| `OBS-014` | Amostragem é declarada por classe de evento | OBRIG | — | Log estruturado em profundidade |
| `OBS-015` | Todo tipo de registro tem consumidor nomeado | RECOM | — | Log estruturado em profundidade |
| `OBS-016` | Volume de log é medido por serviço e por evento, e o crescimento é achado | OBRIG | — | Log estruturado em profundidade |
| `OBS-017` | Nível não é controle de custo | OBRIG | — | Log estruturado em profundidade |
| `OBS-018` | A propagação atravessa a fila pelo envelope, nunca pelo corpo | OBRIG | — | Correlação além da requisição |
| `OBS-019` | Trabalho agendado abre a própria correlação e a expõe | OBRIG | — | Correlação além da requisição |
| `OBS-020` | Retentativa preserva a correlação de origem e numera a tentativa | OBRIG | — | Correlação além da requisição |
| `OBS-021` | Chamada a fornecedor registra o identificador dele | OBRIG | — | Correlação além da requisição |
| `OBS-022` | Falha de sistema devolve ao usuário um identificador de suporte | RECOM | — | Correlação além da requisição |
| `OBS-023` | Span é unidade de trabalho com início, fim e resultado declarado | OBRIG | — | Tracing distribuído |
| `OBS-024` | Atributo de span carrega o que muda a interpretação da duração | OBRIG | — | Tracing distribuído |
| `OBS-025` | Erro é marcado no span, não descrito em texto | OBRIG | — | Tracing distribuído |
| `OBS-026` | Amostragem de trace preserva o anômalo | OBRIG | — | Tracing distribuído |
| `OBS-027` | Tracing paga onde há fronteira e é caro onde não há | RECOM | — | Tracing distribuído |
| `OBS-028` | Instrumentação manual só na fronteira que a automática não vê | RECOM | — | Tracing distribuído |
| `OBS-029` | Trace não é fonte de alerta | OBRIG | — | Tracing distribuído |
| `OBS-030` | O tipo da métrica sai da pergunta | OBRIG | — | Métricas |
| `OBS-031` | Contador é monotônico, e a consulta é sobre a taxa | OBRIG | — | Métricas |
| `OBS-032` | Latência e tamanho são histograma, com faixas escolhidas | OBRIG | — | Métricas |
| `OBS-033` | Percentil não se agrega por média | OBRIG | — | Métricas |
| `OBS-034` | Cardinalidade de rótulo é orçada por métrica | OBRIG | — | Métricas |
| `OBS-035` | Nenhum identificador de entidade como rótulo de métrica | OBRIG | — | Métricas |
| `OBS-036` | Nome, unidade e sufixo seguem convenção declarada | RECOM | — | Métricas |
| `OBS-037` | Erro é contado por classe, com o total derivável | OBRIG | — | Métricas |
| `OBS-038` | Métrica nova declara o painel ou o alerta que a consome | OBRIG | — | Métricas |
| `OBS-039` | Cada tipo de componente tem um conjunto mínimo próprio | OBRIG | — | As métricas mínimas por tipo de componente |
| `OBS-040` | Em fila, a idade da mensagem mais antiga é a métrica que revela atraso | OBRIG | — | As métricas mínimas por tipo de componente |
| `OBS-041` | Em job, a última conclusão com sucesso é a métrica que revela ausência | OBRIG | — | As métricas mínimas por tipo de componente |
| `OBS-042` | Em integração externa, quem mede é você | OBRIG | — | As métricas mínimas por tipo de componente |
| `OBS-043` | Em banco, meça contenção e atraso, não só latência de consulta | OBRIG | — | As métricas mínimas por tipo de componente |
| `OBS-044` | Destino final de mensagens tem contagem alertada em zero | OBRIG | — | As métricas mínimas por tipo de componente |
| `OBS-045` | Painel responde a uma pergunta declarada no próprio título | OBRIG | — | Painéis |
| `OBS-046` | Todo gráfico tem unidade, escala e a linha do objetivo | OBRIG | — | Painéis |
| `OBS-047` | Um painel por público e por pergunta, não um painel para todos | RECOM | — | Painéis |
| `OBS-048` | SLI mede um evento do usuário, não a saúde de um processo | OBRIG | — | SLI, SLO e orçamento de erro |
| `OBS-049` | SLO é número, janela e público, os três | OBRIG | — | SLI, SLO e orçamento de erro |
| `OBS-050` | Cem por cento não é objetivo | IMUT | — | SLI, SLO e orçamento de erro |
| `OBS-051` | O orçamento de erro é a unidade de decisão de lançamento | OBRIG | — | SLI, SLO e orçamento de erro |
| `OBS-052` | Velocidade de consumo alerta antes do esgotamento | OBRIG | — | SLI, SLO e orçamento de erro |
| `OBS-053` | SLO sem consequência declarada não existe | OBRIG | — | SLI, SLO e orçamento de erro |
| `OBS-054` | Escolha os fluxos com SLO pela consequência da falha | RECOM | — | SLI, SLO e orçamento de erro |
| `OBS-055` | Todo alerta declara a consequência de ser ignorado | OBRIG | — | Alerta acionável |
| `OBS-056` | Interromper uma pessoa exige ação humana imediata e útil | OBRIG | — | Alerta acionável |
| `OBS-057` | O limiar do alerta vem do objetivo, não do palpite | OBRIG | — | Alerta acionável |
| `OBS-058` | Alerta tem duração mínima e histerese | RECOM | — | Alerta acionável |
| `OBS-059` | O que nunca deve alertar | OBRIG | — | Alerta acionável |
| `OBS-060` | Fadiga de alerta é medida, e o número é responsabilidade da engenharia | OBRIG | — | Alerta acionável |
| `OBS-061` | Erro de cliente carrega versão do artefato e contexto de sessão | OBRIG | — | Observabilidade de frontend |
| `OBS-062` | Métrica de usuário real, não apenas sintética | OBRIG | — | Observabilidade de frontend |
| `OBS-063` | Telemetria vinda do cliente é entrada não confiável | OBRIG | — | Observabilidade de frontend |
| `OBS-064` | Falha de rede do cliente é sinal de produto, não ruído | RECOM | — | Observabilidade de frontend |
| `OBS-065` | Aumentar verbosidade é operação com escopo, prazo e reversão | OBRIG | — | Depuração em produção |
| `OBS-066` | Nenhuma coleta que altere o comportamento observado | OBRIG | — | Depuração em produção |
| `OBS-067` | Consulta de investigação repetida vira painel ou campo | RECOM | — | Depuração em produção |
| `OBS-068` | Telemetria tem orçamento declarado por serviço, e ele é medido | OBRIG | — | Custo e retenção |
| `OBS-069` | Retenção é declarada por sinal e por camada | OBRIG | — | Custo e retenção |
| `OBS-070` | Corte de custo é por pergunta, nunca por percentual | OBRIG | — | Custo e retenção |

## 📘 Volume 18 — Produto

Arquivo: [`18-produto.md`](18-produto.md) · 58 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `PRD-001` | Problema de produto é restrição de valor, não de tecnologia | IMUT | — | Problema antes de solução |
| `PRD-002` | Solução disfarçada de pedido é rejeitada até reescrita | OBRIG | — | Problema antes de solução |
| `PRD-003` | Nomeie quem sofre o problema | OBRIG | — | Problema antes de solução |
| `PRD-004` | Frequência e custo do problema são números ou hipóteses rotuladas | OBRIG | — | Problema antes de solução |
| `PRD-005` | Problema de um papel não é problema de todos | OBRIG | — | Problema antes de solução |
| `PRD-006` | Sintoma relatado não é diagnóstico | OBRIG | — | Problema antes de solução |
| `PRD-007` | Toda proposta declara o que fica de fora | OBRIG | — | O que não construir |
| `PRD-008` | Escopo mínimo é o menor conjunto que prova o critério de sucesso | OBRIG | — | O que não construir |
| `PRD-009` | "Também seria bom" não entra no escopo da entrega | OBRIG | — | O que não construir |
| `PRD-010` | Opção zero é legítima em produto | OBRIG | — | O que não construir |
| `PRD-011` | Feature para um cliente só exige contrato de custo e generalização | OBRIG | — | O que não construir |
| `PRD-012` | Preferir configuração a fork de produto | RECOM | — | O que não construir |
| `PRD-013` | Comprar o que não é diferencial | RECOM | — | O que não construir |
| `PRD-014` | Critério de sucesso escrito antes do primeiro commit | IMUT | — | Critério de sucesso antes de construir |
| `PRD-015` | Critério é observável por terceiro sem perguntar ao autor | OBRIG | — | Critério de sucesso antes de construir |
| `PRD-016` | Métrica de sucesso distingue adoção de valor | OBRIG | — | Critério de sucesso antes de construir |
| `PRD-017` | Horizonte de medição declarado com a entrega | OBRIG | — | Critério de sucesso antes de construir |
| `PRD-018` | Sem critério, a entrega é experimento rotulado | OBRIG | — | Critério de sucesso antes de construir |
| `PRD-019` | Prioridade de produto ordena valor e risco de negócio | OBRIG | — | Priorização de produto versus técnica |
| `PRD-020` | Achado técnico S0 e S1 não entra em disputa com roadmap | IMUT | — | Priorização de produto versus técnica |
| `PRD-021` | Capacidade da engenharia é restrição do plano | OBRIG | — | Priorização de produto versus técnica |
| `PRD-022` | Fórmula de score de produto é declarada no perfil | RECOM | — | Priorização de produto versus técnica |
| `PRD-023` | Trabalho que reduz custo operacional conta como produto | RECOM | — | Priorização de produto versus técnica |
| `PRD-024` | Roadmap sem capacidade comprometida é lista de desejo | OBRIG | — | Priorização de produto versus técnica |
| `PRD-025` | Investimento em descoberta escala com irreversibilidade | OBRIG | — | Descoberta proporcional ao risco |
| `PRD-026` | Entrevista sem decisão pendente é teatro | OBRIG | — | Descoberta proporcional ao risco |
| `PRD-027` | Protótipo responde uma pergunta, não antecipa a implementação | OBRIG | — | Descoberta proporcional ao risco |
| `PRD-028` | Distinga o que o usuário diz do que o usuário faz | OBRIG | — | Descoberta proporcional ao risco |
| `PRD-029` | Validação com N=1 não generaliza sem declaração | OBRIG | — | Descoberta proporcional ao risco |
| `PRD-030` | Pare de descobrir quando a próxima informação não muda a decisão | OBRIG | — | Descoberta proporcional ao risco |
| `PRD-031` | Requisito ambíguo bloqueia implementação | IMUT | — | Requisito sem ambiguidade |
| `PRD-032` | Cada requisito tem ator, ação, condição e resultado | OBRIG | — | Requisito sem ambiguidade |
| `PRD-033` | Casos de borda nomeados ou declarados fora de escopo | OBRIG | — | Requisito sem ambiguidade |
| `PRD-034` | Um conceito, um nome, no glossário do domínio | OBRIG | — | Requisito sem ambiguidade |
| `PRD-035` | Aceite é comportamental, não cosmética | OBRIG | — | Requisito sem ambiguidade |
| `PRD-036` | Conflito com fluxo existente é escalada, não merge silencioso | OBRIG | — | Requisito sem ambiguidade |
| `PRD-037` | "Obviamente" e "como sempre" marcam ambiguidade | OBRIG | — | Requisito sem ambiguidade |
| `PRD-038` | Trade-off prazo/escopo/dívida é explícito e assinado | OBRIG | — | Prazo, escopo, dívida e manutenção |
| `PRD-039` | Cortar escopo antes de cortar qualidade estrutural | OBRIG | — | Prazo, escopo, dívida e manutenção |
| `PRD-040` | Dívida de produto registra-se como dívida, não como "v2" | OBRIG | — | Prazo, escopo, dívida e manutenção |
| `PRD-041` | Custo de manutenção entra na decisão de construir | OBRIG | — | Prazo, escopo, dívida e manutenção |
| `PRD-042` | Flag não autoriza escopo indefinido | OBRIG | — | Prazo, escopo, dívida e manutenção |
| `PRD-043` | Prazo fixo sem escopo negociável é recusado | OBRIG | — | Prazo, escopo, dívida e manutenção |
| `PRD-044` | Mudança visível ao usuário tem comunicação antes do corte | OBRIG | — | Comunicar mudança e encerrar funcionalidade |
| `PRD-045` | Comunique o que muda para o usuário, não a implementação | OBRIG | — | Comunicar mudança e encerrar funcionalidade |
| `PRD-046` | Encerrar funcionalidade exige medição de uso e alternativa | OBRIG | — | Comunicar mudança e encerrar funcionalidade |
| `PRD-047` | Sunset tem data, dono e caminho de migração | OBRIG | — | Comunicar mudança e encerrar funcionalidade |
| `PRD-048` | Remoção antecipada só com aceitação de risco nomeada | OBRIG | — | Comunicar mudança e encerrar funcionalidade |
| `PRD-049` | Dívida de produto é lacuna entre promessa e capacidade | OBRIG | — | Dívida de produto e recusa com evidência |
| `PRD-050` | Acúmulo de exceções por cliente é dívida estrutural | OBRIG | — | Dívida de produto e recusa com evidência |
| `PRD-051` | Engenheiro recusa pedido com evidência, não com opinião | OBRIG | — | Dívida de produto e recusa com evidência |
| `PRD-052` | Recusa cita o impacto de aceitar | OBRIG | — | Dívida de produto e recusa com evidência |
| `PRD-053` | Pedido sensível sem comportamento definido para a implementação | OBRIG | — | Dívida de produto e recusa com evidência |
| `PRD-054` | Implementação correta do pedido errado ainda é desperdício | IMUT | — | Dívida de produto e recusa com evidência |
| `PRD-055` | Reabrir escopo após aceite exige novo critério | OBRIG | — | Dívida de produto e recusa com evidência |
| `PRD-056` | Métrica de vaidade não justifica continuidade | OBRIG | — | Dívida de produto e recusa com evidência |
| `PRD-057` | Toda decisão de produto tem dono nomeado | OBRIG | — | Dívida de produto e recusa com evidência |
| `PRD-058` | Decisão de produto registra-se no nível adequado | OBRIG | — | Dívida de produto e recusa com evidência |

## 📓 Volume 19 — IA no Produto

Arquivo: [`19-ia-no-produto.md`](19-ia-no-produto.md) · 69 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `IAX-001` | Se uma regra determinística resolve, o modelo está proibido | IMUT | — | - |
| `IAX-002` | A saída do modelo é entrada não confiável | IMUT | `S0` | - |
| `IAX-003` | Ordem de análise dentro de uma funcionalidade com IA | OBRIG | — | - |
| `IAX-004` | O critério de sucesso é declarado antes da escolha do modelo | OBRIG | — | Quando IA é a solução correta, e quando é a errada |
| `IAX-005` | Declare a taxa de erro aceitável e quem paga por ela | OBRIG | — | Quando IA é a solução correta, e quando é a errada |
| `IAX-006` | Efeito irreversível não é executado por saída de modelo | IMUT | — | Quando IA é a solução correta, e quando é a errada |
| `IAX-007` | A linha de base sem modelo é medida, não estimada | OBRIG | — | Quando IA é a solução correta, e quando é a errada |
| `IAX-008` | Toda funcionalidade com IA tem dono humano nomeado | OBRIG | — | Quando IA é a solução correta, e quando é a errada |
| `IAX-009` | Não determinismo é característica do produto, não detalhe de implementação | OBRIG | — | O que muda quando a funcionalidade é não determinística |
| `IAX-010` | Fixe tudo que pode ser fixado, e declare o que não pode | OBRIG | — | O que muda quando a funcionalidade é não determinística |
| `IAX-011` | Teste determinístico em tudo que envolve o modelo | OBRIG | — | O que muda quando a funcionalidade é não determinística |
| `IAX-012` | Registre o suficiente para reproduzir a investigação | OBRIG | — | O que muda quando a funcionalidade é não determinística |
| `IAX-013` | Troca de versão de modelo é mudança de comportamento | OBRIG | — | O que muda quando a funcionalidade é não determinística |
| `IAX-014` | "Qual é o melhor modelo" é a pergunta errada | OBRIG | — | Escolha de modelo |
| `IAX-015` | Decomponha a funcionalidade em tarefas e escolha por tarefa | OBRIG | — | Escolha de modelo |
| `IAX-016` | Escolha por avaliação no seu conjunto, nunca por ranking público | OBRIG | — | Escolha de modelo |
| `IAX-017` | O modelo entra pela borda, atrás de uma interface própria | OBRIG | — | Escolha de modelo |
| `IAX-018` | Três camadas separadas: montagem, invocação, validação | OBRIG | — | Arquitetura de uma funcionalidade com IA |
| `IAX-019` | O prompt é artefato versionado, fora do código de orquestração | OBRIG | — | Arquitetura de uma funcionalidade com IA |
| `IAX-020` | Nenhuma chamada de modelo dentro de transação | OBRIG | — | Arquitetura de uma funcionalidade com IA |
| `IAX-021` | Timeout, retry e comportamento em falha declarados por chamada | OBRIG | — | Arquitetura de uma funcionalidade com IA |
| `IAX-022` | Streaming não dispensa validação; o efeito espera | OBRIG | — | Arquitetura de uma funcionalidade com IA |
| `IAX-023` | Toda saída consumida por código é estruturada e validada por schema | OBRIG | — | Saída estruturada e a fronteira de confiança |
| `IAX-024` | Validação de schema não é validação de negócio | OBRIG | — | Saída estruturada e a fronteira de confiança |
| `IAX-025` | Todo identificador vindo do modelo é reconsultado e reautorizado | OBRIG | `S0` | Saída estruturada e a fronteira de confiança |
| `IAX-026` | Falha de validação tem caminho definido, e ele não é o retry infinito | OBRIG | — | Saída estruturada e a fronteira de confiança |
| `IAX-027` | Nunca conserte silenciosamente uma saída inválida | OBRIG | — | Saída estruturada e a fronteira de confiança |
| `IAX-028` | Alucinação não se corrige; se contém | IMUT | — | Alucinação como requisito de projeto |
| `IAX-029` | Afirmação verificável é ancorada em fonte do sistema | OBRIG | — | Alucinação como requisito de projeto |
| `IAX-030` | Abstenção é resultado válido, e precisa ser possível | OBRIG | — | Alucinação como requisito de projeto |
| `IAX-031` | A taxa de invenção é medida, não estimada | OBRIG | — | Alucinação como requisito de projeto |
| `IAX-032` | A permissão do usuário é aplicada na recuperação | OBRIG | `S0` | Recuperação (RAG) |
| `IAX-033` | Documento removido ou revogado sai do índice no mesmo fluxo | OBRIG | — | Recuperação (RAG) |
| `IAX-034` | Recuperação e geração são avaliadas separadamente | OBRIG | — | Recuperação (RAG) |
| `IAX-035` | Recuperação errada com confiança alta é o modo de falha dominante | OBRIG | — | Recuperação (RAG) |
| `IAX-036` | Fragmentação é decisão declarada e medida | OBRIG | — | Recuperação (RAG) |
| `IAX-037` | Existe limiar de relevância, e um comportamento quando nada o atinge | OBRIG | — | Recuperação (RAG) |
| `IAX-038` | Toda resposta cita a fonte, e a citação é verificável pelo usuário | OBRIG | — | Recuperação (RAG) |
| `IAX-039` | Contexto crescente é custo e latência crescentes, com teto declarado | OBRIG | — | Memória e estado de conversa |
| `IAX-040` | Truncar ou resumir é perda de informação declarada | OBRIG | — | Memória e estado de conversa |
| `IAX-041` | Memória entre sessões é dado pessoal | OBRIG | — | Memória e estado de conversa |
| `IAX-042` | O usuário vê e apaga o que o sistema lembra dele | RECOM | — | Memória e estado de conversa |
| `IAX-043` | A ferramenta roda com a autoridade do usuário, nunca com a do sistema | OBRIG | `S0` | Ferramentas e chamada de função |
| `IAX-044` | Argumento de ferramenta é entrada não confiável | OBRIG | — | Ferramentas e chamada de função |
| `IAX-045` | Ferramenta com efeito irreversível exige confirmação humana explícita | OBRIG | — | Ferramentas e chamada de função |
| `IAX-046` | Ferramenta é idempotente ou protegida por chave de idempotência | OBRIG | — | Ferramentas e chamada de função |
| `IAX-047` | O catálogo de ferramentas é mínimo por tarefa | RECOM | — | Ferramentas e chamada de função |
| `IAX-048` | Todo laço tem teto de passos, de tempo e de custo | OBRIG | — | Agentes e seus limites |
| `IAX-049` | "Não convergiu" é um resultado, com tratamento definido | OBRIG | — | Agentes e seus limites |
| `IAX-050` | O agente não amplia o próprio escopo de permissão | IMUT | — | Agentes e seus limites |
| `IAX-051` | Tarefa longa tem estado durável e retomável | RECOM | — | Agentes e seus limites |
| `IAX-052` | O conjunto de casos existe antes da primeira linha de prompt | OBRIG | — | Avaliação sistemática |
| `IAX-053` | A avaliação roda no pipeline e bloqueia | OBRIG | — | Avaliação sistemática |
| `IAX-054` | Regressão de qualidade é queda medida no conjunto, com margem declarada | OBRIG | — | Avaliação sistemática |
| `IAX-055` | Modelo usado como avaliador é calibrado contra rótulo humano | RECOM | — | Avaliação sistemática |
| `IAX-056` | Caso real que falhou entra no conjunto no mesmo ciclo | OBRIG | — | Avaliação sistemática |
| `IAX-057` | Custo por interação é requisito de primeira classe, com teto | OBRIG | — | Custo, latência e degradação |
| `IAX-058` | Limite de gasto por usuário e por inquilino | OBRIG | — | Custo, latência e degradação |
| `IAX-059` | Latência é orçada em p95 e inclui a cadeia inteira | OBRIG | — | Custo, latência e degradação |
| `IAX-060` | O comportamento sem o modelo é projetado, não improvisado | OBRIG | — | Custo, latência e degradação |
| `IAX-061` | Conteúdo não confiável no contexto é dado, nunca instrução | OBRIG | `S0` | Segurança específica de funcionalidades com IA |
| `IAX-062` | A saída é um canal de exfiltração | OBRIG | — | Segurança específica de funcionalidades com IA |
| `IAX-063` | Dado enviado a modelo de terceiro é compartilhamento com terceiro | OBRIG | — | Segurança específica de funcionalidades com IA |
| `IAX-064` | Envie o mínimo necessário ao contexto | OBRIG | — | Segurança específica de funcionalidades com IA |
| `IAX-065` | Registro da conversa segue as regras de dado sensível | OBRIG | `S0` | Segurança específica de funcionalidades com IA |
| `IAX-066` | A interface distingue o que é gerado do que é dado do sistema | OBRIG | — | Experiência de uma resposta não determinística |
| `IAX-067` | Comunique incerteza sem simulá-la | OBRIG | — | Experiência de uma resposta não determinística |
| `IAX-068` | O usuário corrige, edita e rejeita a saída | OBRIG | — | Experiência de uma resposta não determinística |
| `IAX-069` | A correção do usuário alimenta a avaliação | RECOM | — | Experiência de uma resposta não determinística |

## 📔 Volume 20 — Prompt Engineering

Arquivo: [`20-prompt-engineering.md`](20-prompt-engineering.md) · 58 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `PRM-001` | Prompt que copia norma é segunda fonte de verdade | IMUT | — | Por que o prompt monolítico degrada |
| `PRM-002` | Norma vive no volume; prompt opera por referência | IMUT | — | Por que o prompt monolítico degrada |
| `PRM-003` | Cada token compete com os outros por atenção | OBRIG | — | Por que o prompt monolítico degrada |
| `PRM-004` | Um prompt, uma missão | OBRIG | — | Por que o prompt monolítico degrada |
| `PRM-005` | Monólito proibido quando a composição resolve | OBRIG | — | Por que o prompt monolítico degrada |
| `PRM-006` | Todo prompt operacional tem os sete blocos | IMUT | — | Anatomia do prompt operacional |
| `PRM-007` | Identidade declara responsabilidade por consequência, não por volume | OBRIG | — | Anatomia do prompt operacional |
| `PRM-008` | Missão é resultado mensurável, não lista de tarefas | OBRIG | — | Anatomia do prompt operacional |
| `PRM-009` | Sequência obrigatória é ordenada e proibida de reordenar | OBRIG | — | Anatomia do prompt operacional |
| `PRM-010` | Normas entram só por ID, com uma cláusula de contexto | IMUT | — | Anatomia do prompt operacional |
| `PRM-011` | Formato de saída é schema fechado | OBRIG | — | Anatomia do prompt operacional |
| `PRM-012` | Condições de parada são enumeradas e concretas | OBRIG | — | Anatomia do prompt operacional |
| `PRM-013` | "Not your job" é lista positiva de exclusões | OBRIG | — | Anatomia do prompt operacional |
| `PRM-014` | Separe visualmente instrução, contexto e exemplo | OBRIG | — | Instrução, contexto e exemplo |
| `PRM-015` | Instrução é estável; contexto é por invocação | OBRIG | — | Instrução, contexto e exemplo |
| `PRM-016` | Exemplo demonstra o schema, não ensina a norma | OBRIG | — | Instrução, contexto e exemplo |
| `PRM-017` | Exemplo sem contraste ensina o defeito se o defeito for o único mostrado | OBRIG | — | Instrução, contexto e exemplo |
| `PRM-018` | Conteúdo não confiável no contexto é dado, nunca instrução | OBRIG | `S0` | Instrução, contexto e exemplo |
| `PRM-019` | FINDING exige `path:line` ou saída de comando executado | IMUT | — | Ancoragem em evidência |
| `PRM-020` | Confiança HIGH | MEDIUM | LOW acompanha todo achado | OBRIG | — | Ancoragem em evidência |
| `PRM-021` | Declare o não verificado em lista própria | OBRIG | — | Ancoragem em evidência |
| `PRM-022` | Afirmação de qualidade sem medição é HYPOTHESIS | OBRIG | — | Ancoragem em evidência |
| `PRM-023` | Evidência insuficiente dispara BLOCKED, não achado inventado | OBRIG | — | Ancoragem em evidência |
| `PRM-024` | Schema de saída é o contrato entre papéis | OBRIG | — | Formato estruturado e sequência |
| `PRM-025` | Campo obrigatório ausente vira `n/a` com motivo, nunca some | OBRIG | — | Formato estruturado e sequência |
| `PRM-026` | MUST-FIX e OPPORTUNITY nunca na mesma lista | IMUT | — | Formato estruturado e sequência |
| `PRM-027` | A sequência começa pelo modo de falha mais caro do domínio | OBRIG | — | Formato estruturado e sequência |
| `PRM-028` | Ordem de análise do EOS, quando a tarefa é revisão, não se inverte | OBRIG | — | Formato estruturado e sequência |
| `PRM-029` | Fora de escopo é explícito em toda tarefa | OBRIG | — | Guardas de escopo e calibração de recusa |
| `PRM-030` | O prompt não amplia o próprio escopo de permissão | IMUT | — | Guardas de escopo e calibração de recusa |
| `PRM-031` | Recusa é calibrada por condição concreta | OBRIG | — | Guardas de escopo e calibração de recusa |
| `PRM-032` | Recusa reporta o estabelecido, o descartado e a decisão necessária | OBRIG | — | Guardas de escopo e calibração de recusa |
| `PRM-033` | Pedido que viola CON-013 é recusado, não negociado em silêncio | OBRIG | — | Guardas de escopo e calibração de recusa |
| `PRM-034` | Três camadas distintas: sistema, papel, tarefa | OBRIG | — | Sistema, tarefa, papel e composição |
| `PRM-035` | Contrato compartilhado é herdado, nunca reescrito no papel | IMUT | — | Sistema, tarefa, papel e composição |
| `PRM-036` | Composição na ordem core → schemas → papel → tarefa | OBRIG | — | Sistema, tarefa, papel e composição |
| `PRM-037` | Prompt de volume não substitui prompt de papel quando há julgamento e priorização | RECOM | — | Sistema, tarefa, papel e composição |
| `PRM-038` | Papel declara Overrides em seção nomeada, e só os permitidos | OBRIG | — | Sistema, tarefa, papel e composição |
| `PRM-039` | Prompt é artefato versionado com o volume ou o papel | OBRIG | — | Versionamento, teste e regressão |
| `PRM-040` | Prompt e norma referenciada mudam na mesma entrega | OBRIG | — | Versionamento, teste e regressão |
| `PRM-041` | Conjunto de regressão existe antes da edição | OBRIG | — | Versionamento, teste e regressão |
| `PRM-042` | Mudança de prompt é mudança de comportamento | OBRIG | — | Versionamento, teste e regressão |
| `PRM-043` | Teste mede aderência ao schema e às regras de engajamento | OBRIG | — | Versionamento, teste e regressão |
| `PRM-044` | Caso que falhou em produção ou em revisão entra no conjunto no mesmo ciclo | OBRIG | — | Versionamento, teste e regressão |
| `PRM-045` | Diff de prompt é revisado com o mesmo rigor de código | OBRIG | — | Versionamento, teste e regressão |
| `PRM-046` | Aderência é taxa medida no conjunto, não impressão | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-047` | Limiar de aderência e margem são declarados | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-048` | Custo de contexto é orçado por tipo de tarefa | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-049` | Carregue só volumes e arquivos que a tarefa exige | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-050` | Contexto longo sem ranking degrada a instrução | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-051` | Prompt em inglês; normas e volumes em português | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-052` | Proibido no texto do prompt: hedging, metalinguagem, superlativo vazio | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-053` | Justificativa de edição de prompt tem os quatro campos | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-054` | Parâmetros de amostragem que afetam reprodutibilidade são fixados e versionados | RECOM | — | Medição de aderência e custo de contexto |
| `PRM-055` | Prompt de produto e prompt de engenharia não se misturam | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-056` | Exemplos no prompt usam domínio SaaS real | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-057` | Biblioteca em `prompts/` indexa; não duplica | OBRIG | — | Medição de aderência e custo de contexto |
| `PRM-058` | Checklist operacional de prompt tem no máximo 25 itens | OBRIG | — | Medição de aderência e custo de contexto |

## 📕 Volume 21 — Playbooks

Arquivo: [`21-playbooks.md`](21-playbooks.md) · 58 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `PLB-001` | Playbook não substitui os portões | IMUT | — | Como usar um playbook |
| `PLB-002` | A ordem dos passos é a substância, não a formalidade | OBRIG | — | Como usar um playbook |
| `PLB-003` | Pule passo declarando que pulou | OBRIG | — | Como usar um playbook |
| `PLB-004` | Playbook divergente da realidade é achado | OBRIG | — | Como usar um playbook |
| `PLB-005` | Comece pelas invariantes, não pela tabela | OBRIG | — | Playbook: criar um CRUD |
| `PLB-006` | Enumere os estados e as transições válidas | OBRIG | — | Playbook: criar um CRUD |
| `PLB-007` | Modele com as constraints desde a primeira migração | OBRIG | — | Playbook: criar um CRUD |
| `PLB-008` | Escreva a regra de negócio antes de qualquer borda | OBRIG | — | Playbook: criar um CRUD |
| `PLB-009` | Trate as quatro operações como quatro decisões | OBRIG | — | Playbook: criar um CRUD |
| `PLB-010` | Autorize por objeto em todas as quatro | OBRIG | `S0` | Playbook: criar um CRUD |
| `PLB-011` | Valide no servidor com lista de permitidos e rejeite campo desconhecido | OBRIG | — | Playbook: criar um CRUD |
| `PLB-012` | Índice para cada filtro e ordenação que a listagem oferece | OBRIG | — | Playbook: criar um CRUD |
| `PLB-013` | Conte as consultas com 1 e com 50 itens | OBRIG | — | Playbook: criar um CRUD |
| `PLB-014` | Interface com os oito estados | OBRIG | — | Playbook: criar um CRUD |
| `PLB-015` | Impeça envio duplicado no formulário | OBRIG | `S1` | Playbook: criar um CRUD |
| `PLB-016` | Teste os casos de negócio e os caminhos de erro | OBRIG | — | Playbook: criar um CRUD |
| `PLB-017` | Registre a operação sensível | OBRIG | — | Playbook: criar um CRUD |
| `PLB-018` | Comece pelo contrato, e pelo que ele **não** expõe | OBRIG | — | Playbook: criar um endpoint |
| `PLB-019` | Método e status corretos desde o início | OBRIG | — | Playbook: criar um endpoint |
| `PLB-020` | Autenticação e autorização antes da lógica | OBRIG | — | Playbook: criar um endpoint |
| `PLB-021` | Paginação com limite do servidor desde a primeira versão | OBRIG | — | Playbook: criar um endpoint |
| `PLB-022` | Idempotência se houver efeito externo | OBRIG | — | Playbook: criar um endpoint |
| `PLB-023` | Limite de taxa e limite de tamanho de entrada | OBRIG | — | Playbook: criar um endpoint |
| `PLB-024` | Formato de erro igual ao do resto da API, com identificador de rastreamento | OBRIG | — | Playbook: criar um endpoint |
| `PLB-025` | Declare timeout e comportamento em falha de cada chamada externa | OBRIG | — | Playbook: criar um endpoint |
| `PLB-026` | Atualize o contrato declarado e teste o caminho de erro | OBRIG | — | Playbook: criar um endpoint |
| `PLB-027` | Log com contexto correlacionável e métrica de erro | OBRIG | — | Playbook: criar um endpoint |
| `PLB-028` | Comece pelo objetivo do usuário e pelo critério de sucesso dele | OBRIG | — | Playbook: criar uma tela |
| `PLB-029` | Liste os oito estados antes de escrever componente | OBRIG | — | Playbook: criar uma tela |
| `PLB-030` | Use componentes do design system; variante antes de sobreposição | OBRIG | — | Playbook: criar uma tela |
| `PLB-031` | Nenhum valor literal de cor, espaçamento ou tipografia | OBRIG | — | Playbook: criar uma tela |
| `PLB-032` | Nenhuma regra de negócio na tela | OBRIG | — | Playbook: criar uma tela |
| `PLB-033` | Declare a invalidação de cada mutação | OBRIG | — | Playbook: criar uma tela |
| `PLB-034` | Proteja o trabalho do usuário | OBRIG | `S1` em formulário longo | Playbook: criar uma tela |
| `PLB-035` | Percorra a tela inteira pelo teclado antes de considerar pronta | OBRIG | — | Playbook: criar uma tela |
| `PLB-036` | Todo controle com nome acessível; estado comunicado programaticamente | OBRIG | — | Playbook: criar uma tela |
| `PLB-037` | Reserve espaço para conteúdo assíncrono | OBRIG | — | Playbook: criar uma tela |
| `PLB-038` | Verifique em tela pequena e em zoom 200% | OBRIG | — | Playbook: criar uma tela |
| `PLB-039` | Percorra os caminhos infelizes na tela real | OBRIG | — | Playbook: criar uma tela |
| `PLB-040` | Conte os registros que violam a nova regra, primeiro | OBRIG | — | Playbook: alterar o schema |
| `PLB-041` | Aditivo primeiro, sempre | OBRIG | — | Playbook: alterar o schema |
| `PLB-042` | Verifique a compatibilidade nos dois sentidos | OBRIG | — | Playbook: alterar o schema |
| `PLB-043` | Escreva a reversa e **execute-a** | OBRIG | — | Playbook: alterar o schema |
| `PLB-044` | Verifique o risco de bloqueio de tabela na versão em uso | OBRIG | — | Playbook: alterar o schema |
| `PLB-045` | Migração de dados é `R4` | OBRIG | — | Playbook: alterar o schema |
| `PLB-046` | Nunca junte migração destrutiva com mudança de comportamento | OBRIG | — | Playbook: alterar o schema |
| `PLB-047` | Cinco fases, cinco deploys | OBRIG | — | Playbook: alterar o schema |
| `PLB-048` | Traduza na borda; o modelo do fornecedor não entra no domínio | OBRIG | — | Playbook: integrar um serviço externo |
| `PLB-049` | Declare timeout, retry, idempotência e comportamento em falha | OBRIG | — | Playbook: integrar um serviço externo |
| `PLB-050` | Segredo no gerenciador, rotacionável sem deploy | OBRIG | — | Playbook: integrar um serviço externo |
| `PLB-051` | Erro do fornecedor mapeado para erro de domínio | OBRIG | — | Playbook: integrar um serviço externo |
| `PLB-052` | Nenhuma chamada externa dentro de transação | OBRIG | — | Playbook: integrar um serviço externo |
| `PLB-053` | Webhook de entrada: verifique origem, seja idempotente, responda rápido | OBRIG | — | Playbook: integrar um serviço externo |
| `PLB-054` | Registre a chamada com correlação e monitore a taxa de falha | OBRIG | — | Playbook: integrar um serviço externo |
| `PLB-055` | Reproduza antes de corrigir | IMUT | — | Playbook: corrigir um bug |
| `PLB-056` | Escreva o teste que falha, antes da correção | OBRIG | — | Playbook: corrigir um bug |
| `PLB-057` | Corrija a classe, não só a instância reportada | OBRIG | — | Playbook: corrigir um bug |
| `PLB-058` | Nada de "enquanto eu estava lá" | IMUT | — | Playbook: corrigir um bug |

## 📙 Volume 22 — Checklists

Arquivo: [`22-checklists.md`](22-checklists.md) · 48 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `CHK-001` | Checklist existe para o momento em que a memória falha | IMUT | — | Memória sob pressão |
| `CHK-002` | Competência não autoriza pular o checklist | IMUT | — | Memória sob pressão |
| `CHK-003` | Um checklist serve a um momento, não a um domínio inteiro | OBRIG | — | Memória sob pressão |
| `CHK-004` | O checklist não substitui a norma | IMUT | — | Memória sob pressão |
| `CHK-005` | Sob pressão de prazo, o checklist encolhe por prioridade declarada — nunca some | OBRIG | — | Memória sob pressão |
| `CHK-006` | Declare o tipo da lista no cabeçalho | OBRIG | — | Leitura versus confirmação |
| `CHK-007` | Checklist de leitura proíbe veredito | OBRIG | — | Leitura versus confirmação |
| `CHK-008` | Checklist de confirmação exige evidência anexável | IMUT | — | Leitura versus confirmação |
| `CHK-009` | Não converta leitura em confirmação por pressão social | OBRIG | — | Leitura versus confirmação |
| `CHK-010` | Um item não pode ser ao mesmo tempo "explore" e "prove" | OBRIG | — | Leitura versus confirmação |
| `CHK-011` | Lista longa falha por economia de atenção, não por falta de virtude | IMUT | — | Por que listas longas falham |
| `CHK-012` | Marcar sem ler é a falha mais grave do framework aplicado a checklists | IMUT | — | Por que listas longas falham |
| `CHK-013` | As 735 regras com ID não são um checklist operacional | OBRIG | — | Por que listas longas falham |
| `CHK-014` | Acúmulo é o inimigo; contexto de uso é a divisão correta | OBRIG | — | Por que listas longas falham |
| `CHK-015` | Cada item além do limite reduz a taxa de leitura real | RECOM | — | Por que listas longas falham |
| `CHK-016` | Checklist de volume: no máximo 25 itens | OBRIG | — | Limite e divisão |
| `CHK-017` | Checklist operacional em `checklists/` divide por nível ou bloco com parada | OBRIG | — | Limite e divisão |
| `CHK-018` | Ao crescer, fatie por momento ou por superfície — nunca por "capítulo do livro" | OBRIG | — | Limite e divisão |
| `CHK-019` | Item que ninguém consegue verificar em cinco minutos não entra | OBRIG | — | Limite e divisão |
| `CHK-020` | Remova item que o pipeline já bloqueia de forma confiável | OBRIG | — | Limite e divisão |
| `CHK-021` | Enunciado no passado verificável ou na primeira pessoa da ação | OBRIG | — | Item bem escrito |
| `CHK-022` | Todo item de confirmação cita a regra ou o artefato mínimo | OBRIG | — | Item bem escrito |
| `CHK-023` | Item negativo explícito quando a falha é omissão | RECOM | — | Item bem escrito |
| `CHK-024` | Um item, um veredito | OBRIG | — | Item bem escrito |
| `CHK-025` | Escreva a consequência no item quando o custo de pular não for óbvio | RECOM | — | Item bem escrito |
| `CHK-026` | Só três estados legítimos | IMUT | — | Estados: OK, N/A, PENDENTE |
| `CHK-027` | `OK` exige verificação nesta execução | IMUT | — | Estados: OK, N/A, PENDENTE |
| `CHK-028` | `N/A` sem justificativa conta como `PENDENTE` | IMUT | — | Estados: OK, N/A, PENDENTE |
| `CHK-029` | Um único `PENDENTE` impede `DONE` | IMUT | — | Estados: OK, N/A, PENDENTE |
| `CHK-030` | Não use `N/A` para esconder o que não deu tempo | OBRIG | — | Estados: OK, N/A, PENDENTE |
| `CHK-031` | Toda execução de checklist declara executor e papel | OBRIG | — | Quem assina |
| `CHK-032` | Autor assina pré-merge; revisor assina code-review; auditor assina módulo concluído | IMUT | — | Quem assina |
| `CHK-033` | Assinatura em bloco de seção inteira é inválida | OBRIG | — | Quem assina |
| `CHK-034` | Agente que marca checklist anexa a mesma evidência que um humano | IMUT | — | Quem assina |
| `CHK-035` | Segundo assinante quando o risco é `R3`/`R4` ou toca auth/dado/dinheiro | OBRIG | — | Quem assina |
| `CHK-036` | O que o CI bloqueia com sinal claro sai do checklist humano | OBRIG | — | Automatizar e sair do checklist |
| `CHK-037` | Automação que só reporta sem bloquear não remove o item humano | OBRIG | — | Automatizar e sair do checklist |
| `CHK-038` | Ao automatizar, registre a remoção e o gate substituto | RECOM | — | Automatizar e sair do checklist |
| `CHK-039` | Nunca automatize o julgamento de escopo ou de intenção | IMUT | — | Automatizar e sair do checklist |
| `CHK-040` | Preferir um teste que falha a um item eterno no checklist | RECOM | — | Automatizar e sair do checklist |
| `CHK-041` | Os sete arquivos em `checklists/` são a lista operacional canônica | OBRIG | — | Índice canônico dos checklists |
| `CHK-042` | Não forkue checklist canônico por time sem motivo registrado | OBRIG | — | Índice canônico dos checklists |
| `CHK-043` | Checklist de volume aponta para o arquivo operacional; não o duplica | OBRIG | — | Índice canônico dos checklists |
| `CHK-044` | Ordem de uso na rodada é a dos portões | OBRIG | — | Índice canônico dos checklists |
| `CHK-045` | Item obsoleto é removido ou marcado com data e substituto | OBRIG | — | Ciclo de vida e higiene |
| `CHK-046` | Mudança de checklist canônico é mudança de processo — com dono | OBRIG | — | Ciclo de vida e higiene |
| `CHK-047` | Meça aderência pela evidência, não pela taxa de caixas marcadas | OBRIG | — | Ciclo de vida e higiene |
| `CHK-048` | Em dúvida entre item novo e regra nova, prefira a regra no volume dono | RECOM | — | Ciclo de vida e higiene |

## 📗 Volume 23 — Métricas

Arquivo: [`23-metricas.md`](23-metricas.md) · 58 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `MET-001` | Uma métrica útil tem definição, limiar, reação e dono | IMUT | — | Anatomia de uma métrica útil |
| `MET-002` | Definição é fórmula, unidade e denominador | OBRIG | — | Anatomia de uma métrica útil |
| `MET-003` | Limiar declara valor, janela e direção | OBRIG | — | Anatomia de uma métrica útil |
| `MET-004` | Reação nomeia ação, prazo e gatilho | OBRIG | — | Anatomia de uma métrica útil |
| `MET-005` | Toda métrica tem dono humano nomeado | OBRIG | — | Anatomia de uma métrica útil |
| `MET-006` | Antipadrão de uso é declarado na criação | OBRIG | — | Anatomia de uma métrica útil |
| `MET-007` | Toda métrica usada como meta se corrompe; desenhe sabendo disso | IMUT | — | Goodhart e gamificação |
| `MET-008` | Meta composta de um único proxy fácil é proibida | OBRIG | — | Goodhart e gamificação |
| `MET-009` | Indicador de tendência não vira meta individual | OBRIG | — | Goodhart e gamificação |
| `MET-010` | Gamificação detectada invalida o período | OBRIG | — | Goodhart e gamificação |
| `MET-011` | Tendência supera absoluto até existir baseline estável | OBRIG | — | Tendência, absoluto e baseline |
| `MET-012` | Baseline declara método, janela e data de congelamento | OBRIG | — | Tendência, absoluto e baseline |
| `MET-013` | Divergência entre tendência e absoluto força investigação | OBRIG | — | Tendência, absoluto e baseline |
| `MET-014` | Comparação entre times exige denominador e contexto idênticos | OBRIG | — | Tendência, absoluto e baseline |
| `MET-015` | Cobertura de linhas não mede qualidade | IMUT | — | Métricas de código — o que não dizem |
| `MET-016` | Complexidade e cheiros estáticos apontam; não justificam mudança sozinhos | OBRIG | — | Métricas de código — o que não dizem |
| `MET-017` | Dívida estática sem defeito, risco ou norma ligada é decoração | OBRIG | — | Métricas de código — o que não dizem |
| `MET-018` | Métricas de código respondem a perguntas de risco, não a ranking | OBRIG | — | Métricas de código — o que não dizem |
| `MET-019` | Cycle time mede fluxo de valor, não esforço individual | OBRIG | — | Métricas de processo |
| `MET-020` | Lead time inclui fila; omitir fila falseia o diagnóstico | OBRIG | — | Métricas de processo |
| `MET-021` | Tamanho de PR tem limiar alinhado ao orçamento de mudança | OBRIG | — | Métricas de processo |
| `MET-022` | Tempo de revisão é métrica de fluxo, não de virtude do revisor | OBRIG | — | Métricas de processo |
| `MET-023` | Frequência de deploy é sinal de capacidade, não objetivo isolado | OBRIG | — | Métricas de processo |
| `MET-024` | Change failure rate exige definição escrita de falha | OBRIG | — | Métricas de processo |
| `MET-025` | MTTR conta até recuperação do usuário, não até o merge do hotfix | OBRIG | — | Métricas de processo |
| `MET-026` | As métricas de processo se leem em conjunto | OBRIG | — | Métricas de processo |
| `MET-027` | WIP e idade do trabalho expõem gargalo melhor que vazão | RECOM | — | Métricas de processo |
| `MET-028` | Escape rate mede defeito que passou dos portões | OBRIG | — | Defeito e escape |
| `MET-029` | Densidade de defeito é por módulo ou fluxo, nunca por pessoa | OBRIG | — | Defeito e escape |
| `MET-030` | Severidade classifica impacto; volume sozinho não prioriza | OBRIG | — | Defeito e escape |
| `MET-031` | Telemetria do produto não é métrica de engenharia | IMUT | — | Fronteira com observabilidade |
| `MET-032` | Métrica de engenharia não substitui SLI | OBRIG | — | Fronteira com observabilidade |
| `MET-033` | Quando MET consome dado de OBS, a definição aponta a consulta | OBRIG | — | Fronteira com observabilidade |
| `MET-034` | Engenharia exige sinais de resultado de produto para fechar o ciclo | OBRIG | — | Produto que a engenharia precisa |
| `MET-035` | Critério de sucesso da mudança é mensurável antes do merge | OBRIG | — | Produto que a engenharia precisa |
| `MET-036` | Feature flag sem métrica de adoção é dívida disfarçada | RECOM | — | Produto que a engenharia precisa |
| `MET-037` | Acessibilidade automatizada zero erros é portão; manual tem amostra | OBRIG | — | A11y e performance com limiar |
| `MET-038` | Performance de qualidade usa limiar declarado e regressão | OBRIG | — | A11y e performance com limiar |
| `MET-039` | Bundle e regressão bloqueiam; p95 de API investiga | OBRIG | — | A11y e performance com limiar |
| `MET-040` | Nota é vetor de dimensões; o escalar sozinho não decide | OBRIG | — | Nota por dimensão e agregação |
| `MET-041` | Agregação que mascara trava é proibida | IMUT | — | Nota por dimensão e agregação |
| `MET-042` | Ausência de achados não produz excelência | OBRIG | — | Nota por dimensão e agregação |
| `MET-043` | Nota 10 exige DoE na dimensão, não marketing | OBRIG | — | Nota por dimensão e agregação |
| `MET-044` | Health score proprietário declara fórmula ou é rejeitado | OBRIG | — | Nota por dimensão e agregação |
| `MET-045` | Instrumentação mede o sistema; vigilância mede a pessoa | IMUT | — | Vigilância versus instrumentação |
| `MET-046` | LOC por pessoa e commits por pessoa nunca são coletados como desempenho | IMUT | — | Vigilância versus instrumentação |
| `MET-047` | Coleta de processo é transparente ao time medido | OBRIG | — | Vigilância versus instrumentação |
| `MET-048` | Não compare pessoas; compare sistemas e filas | IMUT | — | Vigilância versus instrumentação |
| `MET-049` | Painel de engenharia sem consumidor nomeado é removido | OBRIG | — | Baseline, painéis e o que matar |
| `MET-050` | Painel sem consulta no período é morto | OBRIG | — | Baseline, painéis e o que matar |
| `MET-051` | Uma pergunta por vista; vistas de ego são proibidas | OBRIG | — | Baseline, painéis e o que matar |
| `MET-052` | Métrica nova passa por revisão de Goodhart antes de virar meta | OBRIG | — | Baseline, painéis e o que matar |
| `MET-053` | Limiares `[perfil]` vivem no perfil do projeto | OBRIG | — | Baseline, painéis e o que matar |
| `MET-054` | Relatório periódico tem dono, cadência e decisão explícita | OBRIG | — | Baseline, painéis e o que matar |
| `MET-055` | Mudança justificada só por mover métrica de manutenibilidade é rejeitada | IMUT | — | Baseline, painéis e o que matar |
| `MET-056` | Tempo de suíte e flakiness são métricas de processo de qualidade | OBRIG | — | Baseline, painéis e o que matar |
| `MET-057` | Custo de coleta de métricas de engenharia é orçado | RECOM | — | Baseline, painéis e o que matar |
| `MET-058` | Toda métrica morta é removida no mesmo ciclo em que é reconhecida | OBRIG | — | Baseline, painéis e o que matar |

## 📕 Volume 24 — Auditoria Final

Arquivo: [`24-auditoria-final.md`](24-auditoria-final.md) · 52 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
| `FIN-001` | O veredito final trata afirmação sem evidência como falha | IMUT | — | Portão anti-teatro |
| `FIN-002` | Teatro de processo é motivo suficiente para `REJECTED` | IMUT | — | Portão anti-teatro |
| `FIN-003` | O auditor não participa da implementação da rodada que julga | IMUT | — | Portão anti-teatro |
| `FIN-004` | Pressão de prazo não rebaixa bloqueante | IMUT | — | Portão anti-teatro |
| `FIN-005` | Primeira linha do entregável é o veredito | OBRIG | — | Portão anti-teatro |
| `FIN-006` | Anti-teatro amostral é obrigatório em toda rodada não trivial | OBRIG | — | Portão anti-teatro |
| `FIN-007` | Tabela de verificação de afirmações é seção obrigatória | OBRIG | — | Report OK versus realmente verificou |
| `FIN-008` | "Melhorou performance" sem antes/depois pelo mesmo método é falha | OBRIG | — | Report OK versus realmente verificou |
| `FIN-009` | Correção de segurança não se valida só com "testes passam" | OBRIG | — | Report OK versus realmente verificou |
| `FIN-010` | O auditor reexecuta a suíte relevante, types e lint no escopo | OBRIG | — | Report OK versus realmente verificou |
| `FIN-011` | Evidência de outrem exige rastreio até o artefato bruto | OBRIG | — | Report OK versus realmente verificou |
| `FIN-012` | Declaração de "não pude validar" só vale com comando exato para humano | OBRIG | — | Report OK versus realmente verificou |
| `FIN-013` | Ordem fixa; não comece pelas notas | OBRIG | — | Ordem de leitura do portão final |
| `FIN-014` | Leia o diff do conjunto antes dos relatórios parciais | OBRIG | — | Ordem de leitura do portão final |
| `FIN-015` | Pare no primeiro bloqueante estrutural | OBRIG | — | Ordem de leitura do portão final |
| `FIN-016` | Checklist operacional deste portão é `modulo-concluido.md` | OBRIG | — | Ordem de leitura do portão final |
| `FIN-017` | Declare quais volumes eram aplicáveis e quais foram de fato aplicados | OBRIG | — | Cobertura de volumes |
| `FIN-018` | Camadas de análise omitidas são risco nomeado, não silêncio | OBRIG | — | Cobertura de volumes |
| `FIN-019` | Segurança é sempre aplicável quando auth, PII, dinheiro ou upload entram no diff | IMUT | — | Cobertura de volumes |
| `FIN-020` | Performance só "aplicada" com medição ou com N/A justificado por ausência de caminho quente | OBRIG | — | Cobertura de volumes |
| `FIN-021` | Multi-tenant aplicável exige evidência de isolamento no ponto interno | OBRIG | — | Cobertura de volumes |
| `FIN-022` | Volume aplicável não aplicado bloqueia `APPROVED` limpo | OBRIG | — | Cobertura de volumes |
| `FIN-023` | Bloqueantes sem negociação | IMUT | — | Bloqueantes |
| `FIN-024` | Teste afrouxado sem justificativa de correção do comportamento antigo é `S1` | OBRIG | — | Bloqueantes |
| `FIN-025` | Dependência nova não prevista na proposta é bloqueante de escopo | OBRIG | — | Bloqueantes |
| `FIN-026` | Remoção de código sem justificativa é mudança de comportamento não proposta | OBRIG | — | Bloqueantes |
| `FIN-027` | Segurança < 6 → no máximo `APPROVED WITH CONDITIONS` | IMUT | — | Bloqueantes |
| `FIN-028` | Nota 10 exige DoE na dimensão; ausência de problemas não basta | IMUT | — | Nota 8 versus nota 10 |
| `FIN-029` | Faixa 8–9: DoD folgada; lacunas de DoE conhecidas e registradas | OBRIG | — | Nota 8 versus nota 10 |
| `FIN-030` | Não negocie nota para "motivar o time" | OBRIG | — | Nota 8 versus nota 10 |
| `FIN-031` | Justificativa por dimensão cita evidência, não impressão | OBRIG | — | Nota 8 versus nota 10 |
| `FIN-032` | Peso das dimensões é o de `CON-052` / `AUD-027` — sem remanejo ad hoc | IMUT | — | Nota 8 versus nota 10 |
| `FIN-033` | Meta razoável entre rodadas é +1 na dimensão mais fraca, não 10 universal | RECOM | — | Nota 8 versus nota 10 |
| `FIN-034` | `APPROVED` exige DoD completa no escopo da rodada, não DoE | OBRIG | — | Pronto versus excelente |
| `FIN-035` | Módulo crítico no perfil sem caminho a DoE não recebe nota 10 | OBRIG | — | Pronto versus excelente |
| `FIN-036` | Pronto com dívida só com os cinco campos de dívida deliberada | OBRIG | — | Pronto versus excelente |
| `FIN-037` | A pergunta final do módulo concluído é critério de aceite narrativo | RECOM | — | Pronto versus excelente |
| `FIN-038` | Veredito do auditor final prevalece na rodada sobre o desejo de fechar do orquestrador | IMUT | — | Discordar do orquestrador |
| `FIN-039` | Discordância cita evidência e regra, não preferência | OBRIG | — | Discordar do orquestrador |
| `FIN-040` | Orquestrador pode pedir reabertura de G1/G2; não pode pedir "aprova assim" | OBRIG | — | Discordar do orquestrador |
| `FIN-041` | Empate entre papéis especialistas resolve-se por evidência e `CON-021`, não por média de notas | OBRIG | — | Discordar do orquestrador |
| `FIN-042` | Registro da discordância fica no `AUDIT REPORT` | OBRIG | — | Discordar do orquestrador |
| `FIN-043` | `APPROVED WITH CONDITIONS` só para itens triviais e verificáveis | OBRIG | — | Aprovação parcial com dívida nomeada |
| `FIN-044` | Lista de condições é numerada e fechável sem nova auditoria completa | OBRIG | — | Aprovação parcial com dívida nomeada |
| `FIN-045` | Dívida que bloqueava DoD não pode ser rebaixada a condição cosmética | IMUT | — | Aprovação parcial com dívida nomeada |
| `FIN-046` | Risco residual declara monitoramento e aceitante humano | OBRIG | — | Aprovação parcial com dívida nomeada |
| `FIN-047` | Condições não cumpridas na rodada seguinte viram `S1` de processo | OBRIG | — | Aprovação parcial com dívida nomeada |
| `FIN-048` | Ao fechar, audite o próprio relatório contra esta lista | OBRIG | — | Auditoria da auditoria |
| `FIN-049` | Se a amostra anti-teatro falha, o veredito não é "corrigir a amostra" | OBRIG | — | Auditoria da auditoria |
| `FIN-050` | Achado novo fora do escopo: registre para a próxima rodada, não expanda esta | OBRIG | — | Auditoria da auditoria |
| `FIN-051` | Guarde o artefato do portão onde a próxima pessoa o encontra sem perguntar | OBRIG | — | Auditoria da auditoria |
| `FIN-052` | O critério final remete a `CON-055` | IMUT | — | Auditoria da auditoria |

