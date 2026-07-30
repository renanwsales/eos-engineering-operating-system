# 📒 Volume 05 — Framework de Banco de Dados

Prefixo: `DAT` · Regras: DAT-001 a DAT-040 · Papel: [Database Architect](agents/04-database.md)

Camada coberta: **4 (dados)**.

Este volume trata de integridade, consulta correta e migração segura. As decisões **estruturais** de
crescimento — normalizar ou desnormalizar, réplicas, particionamento, sharding, isolamento de inquilino —
estão no [Volume 14](14-escalabilidade.md).

**Fronteira.** Modelagem, integridade declarativa, constraints, chaves, índices, planos de
execução, transações, isolamento, migrações, retenção. Não cobre: normalizar vs desnormalizar como
decisão de escala, réplicas, particionamento, sharding (→ [14](14-escalabilidade.md)); isolamento
por inquilino como produto (→ [16](16-multi-tenant.md)) — quando aplicável, cite `DAT-040` /
`SEC-006` sem reabrir o modelo de tenant.

---

## Fundamentos

A aplicação tem bugs, é reescrita e recebe scripts pontuais. **O que o banco garante está
garantido; o que só a aplicação verifica será contornado** (`DAT-001`). Por isso a auditoria de
invariantes — onde cada regra de negócio vive no schema — é o primeiro entregável (`DAT-002`), não
um apêndice.

Consulta correta sem plano de execução é hipótese (`DAT-016`). Migração sem reversa e sem contagem
de violadores transforma deploy em incidente (`DAT-030`, `DAT-032`). Escala estrutural (réplica,
shard) não substitui índice e limite (`DAT-015`, `DAT-021`); isso é [14](14-escalabilidade.md).

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

## Padrões reutilizáveis

**Padrão: auditoria de invariantes.** Tabela invariante → tipo → constraint → app → veredito
(`DAT-002`) como primeiro artefato da revisão.

**Padrão: constraint antes de convenção.** `NOT NULL`, `UNIQUE`, `FK`, `CHECK` no schema
(`DAT-003`–`DAT-006`).

**Padrão: 1 vs 50.** Contar consultas em resposta com 1 item e com 50 para detectar N+1
(`DAT-019`).

**Padrão: migração em duas fases.** Expand → migrate data → contract (`DAT-031`); nunca
renomear/dropar em um passo com app antiga no ar.

**Padrão: nada externo na transação.** HTTP/fila/e-mail fora do `BEGIN`/`COMMIT` (`DAT-026`).

---

## Matrizes de decisão

| Pergunta | Prefira | Evite se |
| --- | --- | --- |
| Onde vive a invariante | Constraint no banco (`DAT-001`) | Só validação na API |
| JSON vs colunas | Colunas tipadas (`DAT-009`, `DAT-010`) | JSON para fugir de modelagem |
| Índice novo | Plano prova uso (`DAT-016`) | Índice "por precaução" |
| Transação larga | Escopo pela invariante (`DAT-025`) | Chamada externa dentro (`DAT-026`) |
| Mudança incompatível | Duas fases (`DAT-031`) | Drop/rename em um deploy |
| Escala (réplica/shard) | [14](14-escalabilidade.md) | Decidir sharding neste volume |

---

## Fluxo de trabalho

```
1. Auditoria de invariantes (DAT-002)
2. Schema: nullability, unique, FK, check, tipos (DAT-003–014)
3. Consultas quentes: índice + plano (DAT-015–018)
4. Contagem 1 vs 50; eliminar N+1 e laço (DAT-019–021)
5. Transações: escopo, isolamento, concorrência (DAT-025–029)
6. Migração: reversível, violadores, bloqueio, R4 se dados (DAT-030–036)
7. Operação: backup testado, privilégio mínimo, retenção (DAT-037–039)
8. Tenant no banco quando o produto exige (DAT-040) — cite 16/SEC
```

Playbook de schema: [21](21-playbooks.md) (alterar o schema).

---

## Exemplos de implementação

```sql
-- Ruim — DAT-001: integridade só na app
-- app: if (qty < 0) throw
CREATE TABLE stock (sku text, qty int);

-- Bom
CREATE TABLE stock (
  sku text PRIMARY KEY,
  qty int NOT NULL CHECK (qty >= 0)
);
```

```
# Ruim — DAT-019: N+1
for order in orders:
    order.items = db.query("SELECT * FROM items WHERE order_id=?", order.id)

# Bom — lote
items = db.query("SELECT * FROM items WHERE order_id = ANY(?)", order_ids)
# agrupar em memória
```

```sql
-- Ruim — DAT-031: rename em um passo
ALTER TABLE orders RENAME COLUMN total TO amount;

-- Bom — expand/contract
ALTER TABLE orders ADD COLUMN amount ...;
-- backfill + app lê/escreve ambos
-- depois drop total em migração separada
```

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

## Checklist

- [ ] Auditoria de invariantes preenchida. (`DAT-002`)
- [ ] `NOT NULL` / `UNIQUE` / FK / `CHECK` onde o domínio exige. (`DAT-003`–`DAT-006`)
- [ ] Tipos corretos; dinheiro sem float. (`DAT-009`)
- [ ] Consultas frequentes com índice e plano. (`DAT-015`, `DAT-016`)
- [ ] Zero N+1; limite em caminho de request. (`DAT-019`, `DAT-021`)
- [ ] Transação sem I/O externo; concorrência declarada. (`DAT-026`, `DAT-027`)
- [ ] Migrações versionadas e reversíveis; violadores contados. (`DAT-030`, `DAT-032`)
- [ ] Mudança incompatível em fases. (`DAT-031`)
- [ ] Backup com restore testado; privilégio mínimo. (`DAT-037`, `DAT-038`)
- [ ] Volume de dados assumido declarado. (`DAT-024`)

---

## Prompt do volume

```
You are reviewing or changing the database under EOS Volume 05 (DAT).

Load: core-contract, output-schemas, 00-constituicao, 05-banco-de-dados.md.
Cite 14-escalabilidade.md for replicas/partition/shard; 16-multi-tenant.md /
06-seguranca.md for tenant isolation — do not restate ESC/MTN/SEC norms.

Sequence:
1. Produce invariant audit table (DAT-002) before debating indexes.
2. Check declarative integrity: null, unique, FK, check, types (DAT-003–014).
3. Hot queries: index + execution plan evidence (DAT-015–018).
4. Count queries at 1 vs 50 items; ban loops (DAT-019–021).
5. Transactions: scope, no external I/O, concurrency control (DAT-025–029).
6. Migrations: reversible, violator count, two-phase for breaking (DAT-030–036).
7. Ops: backup restore, least privilege, retention (DAT-037–039).

Output: integrity audit, index/plan findings, migration risk, assumed volume.
Hypothesis without plan = HYPOTHESIS, not FINDING (DAT-016).
```

---

## Critérios de aceite

1. Invariantes críticas têm constraint (ou veredito explícito de risco) (`DAT-001`, `DAT-002`).
2. Consultas frequentes em escopo têm índice com plano verificado (`DAT-015`, `DAT-016`).
3. Sem N+1 no caminho revisado (`DAT-019`).
4. Migrações reversíveis; incompatíveis em fases (`DAT-030`, `DAT-031`).
5. Transações sem chamada externa (`DAT-026`).
6. Backup com restauração testada quando operação está em escopo (`DAT-037`).
7. Volume de dados assumido declarado (`DAT-024`).

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
