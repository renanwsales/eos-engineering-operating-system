# 📒 Volume 6 — Framework de Banco de Dados

Prefixo: `DAT` · Regras: DAT-001 a DAT-040 · Papel: [Database Architect](agents/04-database.md)

Camada coberta: **4 (dados)**.

Este volume trata de integridade, consulta correta e migração segura. As decisões **estruturais** de
crescimento — normalizar ou desnormalizar, réplicas, particionamento, sharding, isolamento de inquilino —
estão no [Volume 14](14-escalabilidade.md).

---

## Princípio central do volume

### DAT-001 — O banco é a última linha de defesa da integridade **[IMUTÁVEL]**

A aplicação tem bugs, é reescrita, ganha novos pontos de escrita, recebe scripts pontuais e importações
manuais. **O que o banco garante está garantido para sempre; o que só a aplicação verifica será
contornado.**

Consequência: integridade delegada exclusivamente à aplicação é `S2`, e `S1` em dado crítico (financeiro,
pessoal, de acesso).

---

## Capítulo 6.1 — Modelagem e integridade

### DAT-002 — Auditoria de invariantes é o primeiro entregável **[OBRIGATÓRIA]**

Para cada invariante do negócio, responda onde ela vive:

```
| Invariante (linguagem de negócio) | Tipo | Constraint | App | Veredito |
| Total do pedido deve ser > 0       | não  | nenhuma    | API | S1: importação contorna |
| Um carrinho ativo por usuário      | não  | nenhuma    | não | S1 |
| Estoque não pode ficar negativo    | não  | nenhuma    | API | S1 + risco de concorrência |
```

É o output de maior valor do volume, porque torna a lacuna visível.

### DAT-003 — `NOT NULL` em tudo que é obrigatório **[OBRIGATÓRIA]**

Coluna anulável é uma pergunta: "o que significa nulo aqui?". Sem resposta de negócio, é erro de modelagem
— e cada leitura passa a tratar um caso que ninguém definiu. `S2`.

### DAT-004 — `UNIQUE` no que é único **[OBRIGATÓRIA]**

Incluindo unicidade composta e unicidade parcial (por exemplo, "um endereço padrão por usuário").

### DAT-005 — Chave estrangeira com comportamento explícito **[OBRIGATÓRIA]**

`ON DELETE` declarado deliberadamente. Cascata acidental apaga dado que ninguém queria apagar; ausência de
chave deixa registro órfão.

### DAT-006 — `CHECK` para faixas e combinações válidas **[OBRIGATÓRIA]**

`quantidade > 0`, `total >= 0`, `fim > inicio`, e combinações condicionais.

### DAT-007 — Estado inválido não representável no schema **[RECOMENDADA]**

Se um pedido `pago` exige `pago_em` e `total`, o schema deve impedir a combinação impossível — com `CHECK`
condicional ou tabela dedicada. É o que distingue integridade real de esperança.

### DAT-008 — Valor padrão válido no domínio **[OBRIGATÓRIA]**

Nunca um valor "neutro" que crie estado inválido. Um padrão `0` em coluna de preço transforma erro de
inserção em produto de graça.

### DAT-009 — Tipos corretos **[OBRIGATÓRIA]**

| Dado | Correto | Errado |
| --- | --- | --- |
| Dinheiro | Inteiro na menor unidade, ou decimal exato | Ponto flutuante — `S1` |
| Data/hora | Tipo temporal com fuso explícito (UTC) | Texto, ou fuso implícito |
| Enumeração | Enum nativo, ou texto com `CHECK` | Texto livre |
| Identificador | Tipo dedicado (UUID, inteiro) | Texto genérico |
| Booleano | Booleano | `0/1` em texto, `S/N` |
| JSON | Tipo JSON, para dado realmente sem forma | JSON para fugir de modelagem |

### DAT-010 — JSON não é atalho para não modelar **[OBRIGATÓRIA]**

Dado que se consulta, filtra, ordena ou valida merece coluna. JSON perde tipo, integridade e desempenho de
uma só vez.

### DAT-011 — Sem exclusão física de histórico **[RECOMENDADA]**

Registro com valor histórico ou financeiro é marcado como inativo. Exclusão real apenas para atender a
direito de eliminação de dado pessoal — deliberadamente, documentada, com todos os locais mapeados.

### DAT-012 — Carimbos mantidos pelo banco **[RECOMENDADA]**

`criado_em` e `atualizado_em` mantidos por padrão ou gatilho. Mantidos pela aplicação, sempre haverá um
caminho que esquece.

### DAT-013 — Auditoria do que importa **[RECOMENDADA]**

Operação sensível registra quem, quando, o que mudou, de qual valor para qual.

### DAT-014 — Sem modelo genérico de entidade-atributo-valor **[RECOMENDADA]**

Tabela genérica de "chave e valor para qualquer coisa" abandona tipo, integridade e índice
simultaneamente. Se a necessidade é real, ela é a exceção documentada, não o padrão.

---

## Capítulo 6.2 — Índices e consultas

### DAT-015 — Toda consulta frequente usa índice **[OBRIGATÓRIA]**

Coluna usada em filtro, junção ou ordenação frequente precisa de índice.

### DAT-016 — Verifique o plano de execução **[OBRIGATÓRIA]**

Nunca presuma que o índice é usado. Achado de índice sem plano verificado é `HYPOTHESIS`, não `FINDING`.

### DAT-017 — Ordem de colunas do índice composto corresponde às consultas reais **[OBRIGATÓRIA]**

Índice composto na ordem errada não serve à consulta. Ele existe, custa escrita, e não é usado.

### DAT-018 — Índice não utilizado é problema **[RECOMENDADA]**

Custa em cada escrita e em cada backup, sem retorno. Reporte-os.

### DAT-019 — Zero N+1 **[OBRIGATÓRIA]**

O número de consultas não pode crescer com o tamanho do resultado.

- **Detecção objetiva:** conte as consultas de uma requisição que retorna 1 item e de outra que retorna 50.
- **Severidade:** `S2`; em fluxo principal, `S1`.

### DAT-020 — Nenhuma consulta em laço **[OBRIGATÓRIA]**

A origem mais comum de N+1. Carregue em lote.

### DAT-021 — Limite obrigatório em caminho de requisição **[OBRIGATÓRIA]**

O que funciona com mil registros derruba o serviço com um milhão, e o crescimento é garantido.

### DAT-022 — Selecione o que precisa **[RECOMENDADA]**

`SELECT *` em tabela larga transfere colunas não usadas, impede índice de cobertura, e muda de comportamento
silenciosamente quando alguém adiciona uma coluna.

### DAT-023 — Agregação no banco **[RECOMENDADA]**

Somar, contar e agrupar na aplicação transfere volume desnecessário e é ordens de magnitude mais lento.

### DAT-024 — Declare o volume assumido **[OBRIGATÓRIA]**

Toda conclusão de desempenho declara o volume de dados considerado. Conclusão sem volume não é conclusão.

---

## Capítulo 6.3 — Transações e concorrência

### DAT-025 — Escopo pela invariante **[OBRIGATÓRIA]**

Exatamente o conjunto de escritas que precisa ser atômico. Ampla demais gera contenção; estreita demais
gera inconsistência.

### DAT-026 — Nada externo dentro da transação **[OBRIGATÓRIA]**

Chamada HTTP, e-mail ou publicação em fila mantêm a transação aberta pela duração da rede, e o efeito
externo não pode ser desfeito pelo rollback. `S2`.

### DAT-027 — Recurso escasso tem proteção declarada **[OBRIGATÓRIA]**

"Leia, verifique, escreva" sem proteção é `S1`: produz estoque negativo e cupom usado duas vezes, de forma
confiável, sob carga. Declare qual proteção usou: bloqueio, versão ou constraint.

### DAT-028 — Nível de isolamento é decisão consciente **[RECOMENDADA]**

O padrão do banco em uso pode não ser suficiente para a invariante que você acredita estar protegendo.

### DAT-029 — Ordem consistente de bloqueio **[RECOMENDADA]**

Caminhos que bloqueiam os mesmos recursos em ordens diferentes produzem deadlock intermitente.

---

## Capítulo 6.4 — Migrações

### DAT-030 — Versionadas, reversíveis e com reversa executada **[OBRIGATÓRIA]**

A migração vive no repositório, é aplicada em ordem, e a reversa é **escrita e executada** em ambiente de
teste. "É só um ALTER" é a frase que antecede a indisponibilidade.

### DAT-031 — Duas fases para mudança incompatível **[OBRIGATÓRIA]**

```
Fase 1: adicionar o novo (coluna/tabela) — aditivo
Fase 2: aplicação escreve nos dois
Fase 3: migrar o dado existente, em lotes
Fase 4: aplicação lê do novo
Fase 5: remover o antigo — após confirmar que nada mais o usa
```

Cada fase é um deploy separado. Renomear coluna em um passo derruba a aplicação durante o rollout, porque as
duas versões coexistem (ARC-027).

### DAT-032 — Conte os registros que violam a nova regra **[OBRIGATÓRIA]**

Antes de adicionar `NOT NULL`, `UNIQUE` ou `CHECK`. Reporte a contagem. É a verificação que evita migração
falhando em produção — ou, pior, aplicada com um valor padrão que corrompe o significado do dado.

### DAT-033 — Não bloqueie tabela grande **[OBRIGATÓRIA]**

Criação de índice e alteração de tipo podem bloquear escritas. Use as opções concorrentes do banco ou uma
janela acordada. Verifique o comportamento na **versão específica** em uso — isso varia.

### DAT-034 — Migração de dados é `R4` **[OBRIGATÓRIA]**

Backup verificado (restauração testada), execução em lotes, retomável, contagem antes e depois, aprovação
humana prévia. Ver CON-041.

### DAT-035 — Migração destrutiva separada da mudança de comportamento **[OBRIGATÓRIA]**

Nunca no mesmo deploy. Juntas, o rollback se torna impossível.

### DAT-036 — Migração é testada contra volume representativo **[RECOMENDADA]**

Migração que roda em 2 segundos com dados de teste pode levar horas em produção e bloquear a tabela.

---

## Capítulo 6.5 — Operação

### DAT-037 — Backup com restauração testada **[OBRIGATÓRIA]**

Backup nunca testado não é backup: é uma suposição. Teste em calendário, com o **tempo de restauração
medido** e conhecido.

### DAT-038 — Credencial da aplicação com privilégio mínimo **[OBRIGATÓRIA]**

Nunca administrador. Migração usa credencial distinta. Isso limita o dano de uma injeção bem-sucedida.

### DAT-039 — Retenção definida por tabela sensível ou volumosa **[RECOMENDADA]**

Sem política, o banco cresce indefinidamente e a exposição em caso de vazamento cresce com ele.

### DAT-040 — Isolamento de tenant garantido no banco quando possível **[OBRIGATÓRIA]**

Política de linha ou equivalente é mais forte do que confiar em cada consulta. Ver SEC-006.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Integridade só na aplicação | A primeira importação manual corrompe |
| Dinheiro em ponto flutuante | Divergência de centavos, impossível de reconciliar |
| Coluna anulável sem significado | Cada leitura trata um caso não definido |
| `updated_at` mantido pela aplicação | Sempre haverá um caminho que esquece |
| Índice em tudo | Escrita lenta, sem ganho de leitura |
| Índice composto na ordem errada | Custo sem uso |
| Migração sem reversa | Rollback impossível durante incidente |
| Consulta em laço | N+1 garantido |
| JSON para fugir de modelagem | Perde tipo, integridade e índice |
| `EAV` genérico | Abandona as três garantias de uma vez |
| Renomear coluna em um passo | Derruba a aplicação durante o deploy |

---

## Verificação obrigatória de saída

```
## Auditoria de integridade
| Invariante | Tipo | Constraint | App | Veredito |

## Índices
| Consulta (local) | Colunas filtradas/ordenadas | Índice usado? | Plano verificado? | Veredito |

## Contagem de consultas
| Endpoint | Consultas @1 item | Consultas @50 itens | N+1? |

## Transações
| Local | Escopo | Chamada externa dentro? | Proteção de concorrência |

## Migrações
| Migração | Reversível? | Reversa testada? | Registros violando? | Risco de bloqueio |

## Volume assumido
<qual volume de dados embasou as conclusões>
```
