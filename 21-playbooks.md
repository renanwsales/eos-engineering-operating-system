# 📕 Volume 21 — Playbooks

Prefixo: `PLB` · Regras: PLB-001 a PLB-058 · Papel: qualquer, conforme a tarefa

Os outros volumes dizem o que é certo. Este diz **em que ordem fazer**, para as tarefas que se repetem toda
semana. É a camada que transforma 500 regras em trabalho executável.

A diferença em relação a [`runbooks/`](runbooks/): runbook coordena **papéis** numa rodada de revisão;
playbook executa **uma tarefa** de construção, normalmente por um papel só.

Índice operacional das tarefas: [`playbooks/README.md`](playbooks/README.md) — aponta para os capítulos
deste volume; não duplica os passos.

**Fronteira.** É deste volume: a **ordem** de execução das tarefas recorrentes (CRUD, endpoint, tela,
schema, integração externa, correção de bug) e as regras `PLB` que tornam essa ordem citável. O
índice em [`playbooks/README.md`](playbooks/README.md) lista as tarefas e o passo que mais se erra;
a substância mora aqui.

**Não é deste volume:** as **normas** que os passos aplicam. Autorização, schema, contrato, UX,
teste, deploy — ficam nos volumes de domínio (`SEC`, `DAT`, `API`, `UXI`, `QAT`, `OPS`, …). Playbook
**referencia por ID**, nunca reafirma (`A-001`). Coordenação multi-papel de revisão
(→ [`runbooks/`](runbooks/)). Doutrina de checklist (→ [22](22-checklists.md)).

---

## Fundamentos

Um playbook não é atalho para pular G0–G2 (`PLB-001`). É a trilha de G3: implementação na ordem que
impede o modelo anêmico. Começar pela tela ou pelo endpoint empurra a regra para a borda (`ARC-020`)
e deixa a integridade fora do banco (`DAT-001`).

A ordem compartilhada — **invariante → dado → regra → contrato → borda → interface → teste →
observabilidade** — é a substância (`PLB-002`), não cerimônia. Pular passo em silêncio torna o
esquecido indistinguível do dispensado (`PLB-003`). Passo que não cabe no projeto por convenção
local é lacuna no [perfil](templates/perfil-do-projeto.md), não exceção informal (`PLB-004`).

G4 nunca é comprimido (`CON-061`). Fechar o playbook sem Definition of Done é entregar intenção.

---

## Capítulo 21.1 — Como usar um playbook

### PLB-001 — Playbook não substitui os portões **[IMUTÁVEL]**

Ele é a trilha de G3 (implementação). G0 a G2 continuam valendo: você precisa saber o que existe, ter um
achado ou requisito, e ter decidido entre alternativas. G4 é obrigatório e nunca comprimido (`CON-061`).

### PLB-002 — A ordem dos passos é a substância, não a formalidade **[OBRIGATÓRIA]**

Todo playbook aqui é ordenado do mais interno para o mais externo: **invariante → dado → regra → contrato →
borda → interface → teste → observabilidade**.

Essa ordem existe porque o oposto — começar pela tela ou pelo endpoint — produz um sistema em que a regra
vive na borda (`ARC-020`) e a integridade não existe no banco (`DAT-001`). Começar por fora é como se produz
o modelo anêmico.

### PLB-003 — Pule passo declarando que pulou **[OBRIGATÓRIA]**

Passo irrelevante para a tarefa é `N/A` com uma frase de justificativa. Pular em silêncio é como um passo
esquecido se torna indistinguível de um passo dispensado — e viola a regra de evidência (`CON-009`):
sem justificativa, o “feito” não é verificável.

### PLB-004 — Playbook divergente da realidade é achado **[OBRIGATÓRIA]**

Se o passo não se aplica ao projeto por causa de uma convenção local, o achado é a lacuna no
[perfil do projeto](templates/perfil-do-projeto.md), não uma exceção informal. Achado não corrigido
entra no backlog na mesma sessão (`CON-019`).

---

## Capítulo 21.2 — Playbook: criar um CRUD

O caso mais frequente e o mais frequentemente feito ao contrário. "CRUD" sugere quatro operações
simétricas sobre uma tabela; **é a suposição que produz a maioria dos defeitos** desta tarefa, porque as
quatro operações têm regras, autorizações e invariantes diferentes.

### PLB-005 — Comece pelas invariantes, não pela tabela **[OBRIGATÓRIA]**

Escreva em linguagem de negócio o que precisa ser sempre verdade. Só então desenhe o schema. Ver `ARC-009` e
`DAT-002`.

### PLB-006 — Enumere os estados e as transições válidas **[OBRIGATÓRIA]**

Antes de escrever `update`. Quase nenhuma entidade real aceita "alterar qualquer campo a qualquer momento" —
e `update` genérico é o que permite alterar um pedido pago. Ver `BAK-008`.

### PLB-007 — Modele com as constraints desde a primeira migração **[OBRIGATÓRIA]**

`NOT NULL`, `UNIQUE`, chave estrangeira com comportamento, `CHECK`. Adicionar depois exige lidar com dado que
já viola (`DAT-032`), o que é sempre mais caro.

### PLB-008 — Escreva a regra de negócio antes de qualquer borda **[OBRIGATÓRIA]**

Pura e testável sem banco (`CON-074`, `QAT-024`). Se você não consegue testá-la sem infraestrutura, pare: a
dependência está invertida.

### PLB-009 — Trate as quatro operações como quatro decisões **[OBRIGATÓRIA]**

| Operação | Perguntas que precisam de resposta explícita |
| --- | --- |
| **Criar** | Quem pode? Que campos o cliente **não** pode enviar (`BAK-011`)? É idempotente? Que unicidade se aplica? |
| **Ler** | Autorização por objeto (`SEC-004`)? Filtro de inquilino (`ESC-038`)? Que campos **não** saem (`BAK-033`)? Paginação com limite do servidor (`BAK-032`)? |
| **Atualizar** | Que transições são válidas? Que campos são imutáveis após criar? Como se trata escrita concorrente (`DAT-027`)? Parcial ou total? |
| **Excluir** | Físico ou marcação de inativo (`DAT-011`)? O que acontece com os dependentes? É reversível? Exige confirmação (`UXI-021`)? |

Um endpoint único que faz tudo conforme um parâmetro de ação é antipadrão: impossível autorizar, versionar e
monitorar separadamente.

### PLB-010 — Autorize por objeto em todas as quatro **[OBRIGATÓRIA]** · `S0`

Inclusive na leitura em lote e na exportação (`SEC-008`).

### PLB-011 — Valide no servidor com lista de permitidos e rejeite campo desconhecido **[OBRIGATÓRIA]**

`BAK-009`, `BAK-010`, `BAK-012`.

### PLB-012 — Índice para cada filtro e ordenação que a listagem oferece **[OBRIGATÓRIA]**

Verifique o plano (`DAT-016`). Uma listagem com filtro sem índice funciona na revisão e falha no crescimento.

### PLB-013 — Conte as consultas com 1 e com 50 itens **[OBRIGATÓRIA]**

Antes de considerar pronto. É a medição mais barata que existe (`PRF-008`).

### PLB-014 — Interface com os oito estados **[OBRIGATÓRIA]**

`FRT-001`. Vazio, erro e sem permissão são os esquecidos.

### PLB-015 — Impeça envio duplicado no formulário **[OBRIGATÓRIA]** · `S1`

`UXI-007`.

### PLB-016 — Teste os casos de negócio e os caminhos de erro **[OBRIGATÓRIA]**

Não os getters. Cada invariante de `PLB-005` tem um teste que falha sem a regra (`QAT-004`).

### PLB-017 — Registre a operação sensível **[OBRIGATÓRIA]**

Exclusão e alteração de dado relevante, com quem e o que mudou (`SEC-011`, `DAT-013`).

---

## Capítulo 21.3 — Playbook: criar um endpoint

### PLB-018 — Comece pelo contrato, e pelo que ele **não** expõe **[OBRIGATÓRIA]**

Método, caminho, entrada, saída, códigos de erro. A saída é construída campo por campo, nunca serializando a
entidade (`BAK-033`) — é o que evita vazar a coluna sensível que alguém adicionar no futuro.

### PLB-019 — Método e status corretos desde o início **[OBRIGATÓRIA]**

`BAK-031`. `GET` não altera estado. Erro de entrada nunca é 5xx.

### PLB-020 — Autenticação e autorização antes da lógica **[OBRIGATÓRIA]**

Nasce inacessível até a autorização ser declarada (`SEC-005`).

### PLB-021 — Paginação com limite do servidor desde a primeira versão **[OBRIGATÓRIA]**

Adicionar depois é mudança incompatível (`BAK-032`).

### PLB-022 — Idempotência se houver efeito externo **[OBRIGATÓRIA]**

`BAK-042`. A rede vai falhar e o cliente vai repetir.

### PLB-023 — Limite de taxa e limite de tamanho de entrada **[OBRIGATÓRIA]**

`BAK-035`, `BAK-013`.

### PLB-024 — Formato de erro igual ao do resto da API, com identificador de rastreamento **[OBRIGATÓRIA]**

`BAK-026`.

### PLB-025 — Declare timeout e comportamento em falha de cada chamada externa **[OBRIGATÓRIA]**

`BAK-043`, `BAK-045`.

### PLB-026 — Atualize o contrato declarado e teste o caminho de erro **[OBRIGATÓRIA]**

`BAK-029`, `QAT-019`.

### PLB-027 — Log com contexto correlacionável e métrica de erro **[OBRIGATÓRIA]**

`OPS-013`, `OPS-018`.

---

## Capítulo 21.4 — Playbook: criar uma tela

### PLB-028 — Comece pelo objetivo do usuário e pelo critério de sucesso dele **[OBRIGATÓRIA]**

`UXI-036`. Tela sem objetivo declarado não pode ser avaliada.

### PLB-029 — Liste os oito estados antes de escrever componente **[OBRIGATÓRIA]**

`FRT-001`. Projetar o estado de erro depois é como ele deixa de existir.

### PLB-030 — Use componentes do design system; variante antes de sobreposição **[OBRIGATÓRIA]**

`FRT-022`, `FRT-023`. Se o padrão não existe no sistema, criá-lo lá é parte da tarefa.

### PLB-031 — Nenhum valor literal de cor, espaçamento ou tipografia **[OBRIGATÓRIA]**

`FRT-021`.

### PLB-032 — Nenhuma regra de negócio na tela **[OBRIGATÓRIA]**

`FRT-016`. A tela formata e exibe; não decide.

### PLB-033 — Declare a invalidação de cada mutação **[OBRIGATÓRIA]**

`FRT-009`. Sem isso o usuário vê o valor antigo e repete a ação.

### PLB-034 — Proteja o trabalho do usuário **[OBRIGATÓRIA]** · `S1` em formulário longo

Erro de validação, falha de rede, navegação acidental e sessão expirada não apagam o que foi preenchido
(`UXI-023`).

### PLB-035 — Percorra a tela inteira pelo teclado antes de considerar pronta **[OBRIGATÓRIA]**

Com foco visível (`UXI-044`, `UXI-045`). Leva dois minutos e encontra o que a ferramenta automática não pega.

### PLB-036 — Todo controle com nome acessível; estado comunicado programaticamente **[OBRIGATÓRIA]**

`UXI-049`, `UXI-050`. Placeholder não é rótulo.

### PLB-037 — Reserve espaço para conteúdo assíncrono **[OBRIGATÓRIA]**

`FRT-034`.

### PLB-038 — Verifique em tela pequena e em zoom 200% **[OBRIGATÓRIA]**

`UXI-054`.

### PLB-039 — Percorra os caminhos infelizes na tela real **[OBRIGATÓRIA]**

`UXI-039`. Requisição falhando, 403, sessão expirando no meio do preenchimento.

---

## Capítulo 21.5 — Playbook: alterar o schema

### PLB-040 — Conte os registros que violam a nova regra, primeiro **[OBRIGATÓRIA]**

Antes de escrever a migração. Reporte a contagem (`DAT-032`). É o passo que evita a migração que falha em
produção — ou que "funciona" preenchendo um padrão que corrompe o significado do dado.

### PLB-041 — Aditivo primeiro, sempre **[OBRIGATÓRIA]**

Adicionar coluna anulável ou tabela nova é seguro. Tornar obrigatório, renomear e remover são fases
posteriores (`DAT-031`).

### PLB-042 — Verifique a compatibilidade nos dois sentidos **[OBRIGATÓRIA]**

Durante o rollout, código antigo e novo coexistem (`ARC-027`, `OPS-010`). O código antigo funciona contra o
schema novo?

### PLB-043 — Escreva a reversa e **execute-a** **[OBRIGATÓRIA]**

Em ambiente de teste, com dado (`DAT-030`). Reversa não executada não é reversa.

### PLB-044 — Verifique o risco de bloqueio de tabela na versão em uso **[OBRIGATÓRIA]**

`DAT-033`. O comportamento varia entre versões do banco; não presuma.

### PLB-045 — Migração de dados é `R4` **[OBRIGATÓRIA]**

Backup com restauração testada, aprovação humana prévia, lotes, retomável, contagem antes e depois
(`DAT-034`, `CON-041`).

### PLB-046 — Nunca junte migração destrutiva com mudança de comportamento **[OBRIGATÓRIA]**

`DAT-035`, `OPS-007`. Juntas, o rollback é impossível.

### PLB-047 — Cinco fases, cinco deploys **[OBRIGATÓRIA]**

Adicionar → escrever nos dois → migrar em lotes → ler do novo → remover o antigo. Um deploy por fase, com
confirmação de que nada mais usa o antigo antes de remover. É a expansão operacional de `DAT-031`;
fase destrutiva nunca no mesmo deploy que mudança de comportamento (`OPS-007`, `DAT-035`).

---

## Capítulo 21.6 — Playbook: integrar um serviço externo

### PLB-048 — Traduza na borda; o modelo do fornecedor não entra no domínio **[OBRIGATÓRIA]**

`ARC-028`, `SEL-031`.

### PLB-049 — Declare timeout, retry, idempotência e comportamento em falha **[OBRIGATÓRIA]**

Os quatro, antes da primeira chamada em produção (`BAK-043`, `BAK-044`, `BAK-045`).

### PLB-050 — Segredo no gerenciador, rotacionável sem deploy **[OBRIGATÓRIA]**

`SEC-052`.

### PLB-051 — Erro do fornecedor mapeado para erro de domínio **[OBRIGATÓRIA]**

Nunca repassado ao cliente (`BAK-027`).

### PLB-052 — Nenhuma chamada externa dentro de transação **[OBRIGATÓRIA]**

Persista a intenção, execute o efeito depois (`BAK-040`).

### PLB-053 — Webhook de entrada: verifique origem, seja idempotente, responda rápido **[OBRIGATÓRIA]**

`BAK-049`, `BAK-050`. Aceite, enfileire, processe fora do ciclo da requisição.

### PLB-054 — Registre a chamada com correlação e monitore a taxa de falha **[OBRIGATÓRIA]**

`OPS-013`, `OPS-018`. Integração sem métrica falha em silêncio.

---

## Capítulo 21.7 — Playbook: corrigir um bug

O playbook mais curto e o mais violado, porque a pressa é maior.

### PLB-055 — Reproduza antes de corrigir **[IMUTÁVEL]**

Sem reprodução você não sabe se corrigiu — sabe apenas que o sintoma não apareceu na sua tentativa. Se não
consegue reproduzir, isso é o achado, e o próximo passo é instrumentar, não editar. O teste que falha
antes da correção (`QAT-004`, `QAT-030`) é a forma verificável dessa reprodução.

### PLB-056 — Escreva o teste que falha, antes da correção **[OBRIGATÓRIA]**

`QAT-030`. Ele prova a reprodução e impede a reincidência de uma vez.

### PLB-057 — Corrija a classe, não só a instância reportada **[OBRIGATÓRIA]**

Procure os casos irmãos: o mesmo defeito no job, na importação, no admin (`BAK-002`). Correção parcial que
deixa o defeito alcançável não é mudança menor: é incompleta (`CON-016`).

### PLB-058 — Nada de "enquanto eu estava lá" **[IMUTÁVEL]**

O commit de correção contém a correção. Toda melhoria adjacente percebida vai ao backlog (`CON-019`). É o
antipadrão que mais infla diff de correção e o que mais dificulta bissecar a próxima regressão.

Se a reincidência for de um bug já corrigido antes, **o achado é o teste de regressão ausente**, não o código
(`QAT-031`).

---

## Padrões reutilizáveis

**Tabela de passos com status.** Uma linha por passo do playbook: `feito` · evidência path:line · ou
`N/A` com frase (`PLB-003`). É o artefato que prova que a ordem foi seguida.

**Invariantes antes do schema.** Frases de negócio que precisam ser sempre verdade, depois constraints
(`PLB-005`, `PLB-007`). *Use* em todo CRUD novo.

**Quatro operações, quatro decisões.** Create/Read/Update/Delete com autorização e invariantes
próprias (`PLB-009`, `PLB-010`). *Não trate* como simétricas.

**Contrato antes do handler.** Campos expostos e omitidos escritos antes do código da borda
(`PLB-018`). *Não serialize* a entidade inteira.

**Oito estados antes do componente.** Empty, loading, error, success, partial, forbidden, offline,
skeleton — listados (`PLB-029`). *Não deixe* erro "para depois".

**Contar violadores antes de migrar.** `SELECT` que conta registros que quebram a regra nova
(`PLB-040`). *Antes* de escrever a migração.

**Reproduzir → teste que falha → corrigir a classe.** Ordem de bug (`PLB-055`–`PLB-057`). Commit só
com a correção (`PLB-058`).

---

## Matrizes de decisão

**Qual playbook**

| Tarefa | Capítulo | Faixa |
| --- | --- | --- |
| CRUD de entidade | 15.2 | `PLB-005`–`017` |
| Endpoint / rota | 15.3 | `PLB-018`–`027` |
| Tela | 15.4 | `PLB-028`–`039` |
| Schema / migração | 15.5 | `PLB-040`–`047` |
| Integração externa | 15.6 | `PLB-048`–`054` |
| Bug | 15.7 | `PLB-055`–`058` |

Índice: [`playbooks/README.md`](playbooks/README.md).

**Passo vs norma**

| O playbook faz | A norma mora em |
| --- | --- |
| Ordena "autorize por objeto" | `SEC-004` / `BAK` |
| Ordena constraints na 1ª migração | `DAT-001` / `DAT-002` |
| Ordena oito estados de tela | `FRT` / `UXI` |
| Ordena aditivo primeiro | `DAT-031` / `OPS-011` |
| Ordena timeout/retry/idempotência | `BAK` / `OPS` |

**Pular passo**

| Situação | Ação |
| --- | --- |
| Passo irrelevante de verdade | `N/A` + uma frase (`PLB-003`) |
| "Não temos tempo" | Não é N/A — é risco aceito ou dívida (`AUD-037`) |
| Convenção local diverge | Lacuna no perfil (`PLB-004`) |
| Quer pular G0–G2 | Proibido (`PLB-001`) |

---

## Fluxo de trabalho

```
1. Identificar a tarefa em playbooks/README.md
2. Confirmar G0–G2 feitos (ou comprimir só se trivial e declarado) — PLB-001
3. Percorrer os passos PLB na ordem do capítulo
4. Cada pulo = N/A justificado (PLB-003)
5. Se passo não cabe no projeto → achar no perfil (PLB-004)
6. Fechar com DoD (CON-043) e bloco de verificação deste volume
7. G4: validar em isolamento (CON-061) — nunca comprimir
```

Ordem interna compartilhada: invariante → dado → regra → contrato → borda → interface → teste →
observabilidade (`PLB-002`).

---

## Exemplos de implementação

**CRUD ao contrário (`PLB-005`, `PLB-009`)**

```
# Ruim — tabela primeiro, update genérico depois
CREATE TABLE pedidos (...);
app.put('/pedidos/:id', (body) => repo.update(id, body)) // altera pedido pago

# Bom — invariantes e transições antes
# Invariante: pedido pago não muda itens.
# Transições: rascunho→enviado→pago→cancelado (subset).
# Update: casos de uso explícitos, não patch genérico (PLB-009).
```

**Schema sem contagem (`PLB-040`)**

```sql
-- Ruim: ADD NOT NULL direto
ALTER TABLE clientes ALTER COLUMN documento SET NOT NULL;

-- Bom: contar violadores primeiro
SELECT count(*) FROM clientes WHERE documento IS NULL;
-- depois: backfill / fases (PLB-047), só então NOT NULL
```

**Bug com "enquanto eu estava lá" (`PLB-058`)**

```
# Ruim — um commit: corrige NPE + renomeia módulo + ajusta lint do arquivo vizinho

# Bom
commit 1: teste que falha + correção do NPE (PLB-055–057)
backlog: renomear módulo (CON-019)
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Playbook no lugar de G0–G2 | Implementa a solução errada (`PLB-001`) |
| Começar pela tela/endpoint | Regra na borda; modelo anêmico (`PLB-002`) |
| Pular passo em silêncio | Esquecido = dispensado (`PLB-003`) |
| Exceção informal ao playbook | Perfil desatualizado (`PLB-004`) |
| CRUD com update genérico | Quebra invariante de estado (`PLB-009`) |
| Serializar entidade no endpoint | Vaza campo; acopla contrato (`PLB-018`) |
| Estado de erro "depois" | Erro nunca existe na UI (`PLB-029`) |
| Migrar antes de contar violadores | Deploy quebra em produção (`PLB-040`) |
| Chamada externa dentro de transação | Lock longo; falha parcial (`PLB-052`) |
| Corrigir sem reproduzir | Correção cosmética (`PLB-055`) |
| Commit de bug com melhoria adjacente | Diff impossível de bisectar (`PLB-058`) |
| Reafirmar `SEC`/`DAT` no playbook | Segunda fonte de verdade (`A-001`) |

---

## Checklist

- [ ] Playbook certo identificado; G0–G2 não foram substituídos. (`PLB-001`)
- [ ] Passos na ordem interna (invariante→…→observabilidade). (`PLB-002`)
- [ ] Todo pulo tem `N/A` justificado. (`PLB-003`)
- [ ] Divergência local registrada no perfil, não como exceção informal. (`PLB-004`)
- [ ] CRUD: invariantes, transições, auth por objeto nas quatro operações. (`PLB-005`–`010`)
- [ ] Endpoint: contrato, auth, paginação, idempotência se efeito externo. (`PLB-018`–`022`)
- [ ] Tela: oito estados, tokens do DS, teclado, zoom. (`PLB-029`–`038`)
- [ ] Schema: contagem de violadores, aditivo, reversa executada. (`PLB-040`–`043`)
- [ ] Integração: timeout/retry/idempotência; sem call em transação. (`PLB-049`, `PLB-052`)
- [ ] Bug: reproduzido, teste que falha, classe corrigida, commit limpo. (`PLB-055`–`058`)
- [ ] DoD (`CON-043`) e G4 executados. (`PLB-001`, `CON-061`)

---

## Prompt do volume

```
You are executing an EOS playbook from Volume 21 (PLB).

Mission: implement or review a recurring build task in the mandatory step order. You order work;
you do not invent or restate domain norms — cite SEC, DAT, BAK, API, FRT, UXI, QAT, OPS, etc. by ID
(A-001).

Load: agents/_shared/core-contract.md, 00-constituicao-da-engenharia.md, 21-playbooks.md,
playbooks/README.md, templates/perfil-do-projeto.md, and the domain volumes cited by the chosen
playbook's steps.

Mandatory sequence:
1. Pick the playbook from playbooks/README.md (CRUD, endpoint, screen, schema, integration, bug).
2. Confirm G0–G2 are done or explicitly compressed as trivial (PLB-001). Never skip G4 (CON-061).
3. Walk every PLB step in order. For each: done with path:line evidence, or N/A with one sentence
   (PLB-003).
4. If a step conflicts with local convention, file a profile gap (PLB-004) — do not silently skip.
5. Cite domain rule IDs; do not rephrase them as new PLB norms.
6. Close with Definition of Done (CON-043) and the Volume 21 verification block.

Do not: start from UI or endpoint when the playbook says invariants first; mix adjacent cleanups into
a bugfix (PLB-058); duplicate playbook steps into playbooks/README.md.

Output: the "Verificação obrigatória de saída" block of Volume 21, in Brazilian Portuguese.
```

---

## Critérios de aceite

Uma entrega via playbook só é aceita quando:

1. O playbook correto foi aplicado e G0–G2 não foram substituídos por ele (`PLB-001`).
2. A ordem dos passos foi respeitada; pulos são `N/A` justificados (`PLB-002`, `PLB-003`).
3. Cada passo obrigatório cita evidência (`path:line` ou comando), não narrativa.
4. Normas de domínio foram cumpridas por citação aos volumes donos — o playbook não as reescreveu
   (`A-001`).
5. Definition of Done (`CON-043`) completa no escopo; G4 executado (`CON-061`).
6. Em bug: teste que falhava antes da correção existe (`PLB-056`); commit sem "enquanto eu estava lá"
   (`PLB-058`).

---

## Verificação obrigatória de saída

Para qualquer playbook:

```
## Playbook aplicado: <nome>
| Passo | Status | Evidência ou justificativa de N/A |

## Passos pulados
| Passo | Por quê |

## Definition of Done
<checklist de CON-043, item a item>
```
