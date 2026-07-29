# RULES-INDEX — índice de regras do EOS

**735 regras** em 15 volumes. Este arquivo é **gerado** por
`scripts/build-rules-index.py`; não edite à mão. Se um volume e este índice divergirem,
**o volume** é a fonte de verdade.

## Como citar uma regra

Sempre pelo ID: `SEC-004`, `CON-013`, `DAT-019`. IDs são **estáveis** — uma regra removida
deixa o número aposentado, nunca reaproveitado, para que relatórios antigos continuem legíveis.

## Obrigatoriedade

| Nível | Significado | Divergir exige |
| --- | --- | --- |
| `[IMUTÁVEL]` | Núcleo do framework | Decisão do dono do produto + ADR. É mudança `MAJOR` do EOS |
| `[OBRIGATÓRIA]` | Violação é achado, com severidade | ADR registrando a divergência (ARC-037) |
| `[RECOMENDADA]` | Padrão esperado; exceção é normal | Justificativa no momento, sem ADR |

Distribuição: **69 imutáveis** · **531 obrigatórias** · **135 recomendadas**.

## Volumes

| Vol | Título | Prefixo | Regras |
| --- | --- | --- | --- |
| 01 | [Constituição da Engenharia](volumes/vol-01-constituicao.md) | `CON` | 86 |
| 02 | [Framework de Arquitetura](volumes/vol-02-arquitetura.md) | `ARC` | 40 |
| 03 | [Framework Backend](volumes/vol-03-backend.md) | `BAK` | 73 |
| 04 | [Framework Frontend](volumes/vol-04-frontend.md) | `FRT` | 42 |
| 05 | [Segurança e DevSecOps](volumes/vol-05-seguranca.md) | `SEC` | 66 |
| 06 | [Framework de Banco de Dados](volumes/vol-06-banco-de-dados.md) | `DAT` | 40 |
| 07 | [Framework de Performance](volumes/vol-07-performance.md) | `PRF` | 38 |
| 08 | [UX/UI Premium](volumes/vol-08-ux-ui.md) | `UXI` | 55 |
| 09 | [QA e Testes](volumes/vol-09-qa-testes.md) | `QAT` | 40 |
| 10 | [DevOps e SRE](volumes/vol-10-devops-sre.md) | `OPS` | 48 |
| 11 | [Auditoria Técnica](volumes/vol-11-auditoria.md) | `AUD` | 42 |
| 12 | [Orquestrador Mestre](volumes/vol-12-orquestrador.md) | `ORC` | 32 |
| 13 | [Seleção de Arquitetura](volumes/vol-13-selecao-de-arquitetura.md) | `SEL` | 33 |
| 14 | [Escala e Multi-Inquilino](volumes/vol-14-escala-e-multi-inquilino.md) | `ESC` | 42 |
| 15 | [Playbooks](volumes/vol-15-playbooks.md) | `PLB` | 58 |
| | **Total** | | **735** |

---

## 📘 Volume 1 — Constituição da Engenharia

Arquivo: [`volumes/vol-01-constituicao.md`](volumes/vol-01-constituicao.md) · 86 regras

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

## 📗 Volume 2 — Framework de Arquitetura

Arquivo: [`volumes/vol-02-arquitetura.md`](volumes/vol-02-arquitetura.md) · 40 regras

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

## 📙 Volume 3 — Framework Backend

Arquivo: [`volumes/vol-03-backend.md`](volumes/vol-03-backend.md) · 73 regras

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

Arquivo: [`volumes/vol-04-frontend.md`](volumes/vol-04-frontend.md) · 42 regras

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

## 📓 Volume 5 — Segurança e DevSecOps

Arquivo: [`volumes/vol-05-seguranca.md`](volumes/vol-05-seguranca.md) · 66 regras

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

## 📒 Volume 6 — Framework de Banco de Dados

Arquivo: [`volumes/vol-06-banco-de-dados.md`](volumes/vol-06-banco-de-dados.md) · 40 regras

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

## 📔 Volume 7 — Framework de Performance

Arquivo: [`volumes/vol-07-performance.md`](volumes/vol-07-performance.md) · 38 regras

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

Arquivo: [`volumes/vol-08-ux-ui.md`](volumes/vol-08-ux-ui.md) · 55 regras

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

## 📗 Volume 9 — QA e Testes

Arquivo: [`volumes/vol-09-qa-testes.md`](volumes/vol-09-qa-testes.md) · 40 regras

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

## 📙 Volume 10 — DevOps e SRE

Arquivo: [`volumes/vol-10-devops-sre.md`](volumes/vol-10-devops-sre.md) · 48 regras

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

## 📕 Volume 11 — Auditoria Técnica

Arquivo: [`volumes/vol-11-auditoria.md`](volumes/vol-11-auditoria.md) · 42 regras

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

## 📓 Volume 12 — Orquestrador Mestre

Arquivo: [`volumes/vol-12-orquestrador.md`](volumes/vol-12-orquestrador.md) · 32 regras

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

## 📔 Volume 13 — Seleção de Arquitetura

Arquivo: [`volumes/vol-13-selecao-de-arquitetura.md`](volumes/vol-13-selecao-de-arquitetura.md) · 33 regras

| ID | Regra | Nível | Sev. | Capítulo |
| --- | --- | --- | --- | --- |
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

## 📒 Volume 14 — Escala e Multi-Inquilino

Arquivo: [`volumes/vol-14-escala-e-multi-inquilino.md`](volumes/vol-14-escala-e-multi-inquilino.md) · 42 regras

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

## 📕 Volume 15 — Playbooks

Arquivo: [`volumes/vol-15-playbooks.md`](volumes/vol-15-playbooks.md) · 58 regras

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

