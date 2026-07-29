# 📕 Volume 13 — Revisão de Código

Prefixo: `REV` · Regras: REV-001 a REV-058 · Papel: [Auditor Final](agents/10-final-auditor.md)

Este volume trata de **um pull request concreto**. Não é auditoria de módulo
([Volume 12](12-auditoria.md)) nem o portão final ([Volume 24](24-auditoria-final.md)). É a disciplina
diária: como ler um diff, o que comentar, quando bloquear, e como não transformar revisão em teatro ou
em reescrita.

O [Volume 12](12-auditoria.md) já define orçamento de mudança (`AUD-004`), ordem de níveis (`AUD-006`),
força de comentário (`AUD-008`) e a falha simétrica por excesso e omissão (`AUD-001`). Este volume
**cita** essas regras e cobre o que só aparece quando o objeto da revisão é um PR: tamanho e ritmo,
leitura do arquivo inteiro vs do diff, revisão de teste e migração, código gerado por IA, pressão de
prazo, e o comportamento do revisor.

**Fronteira.** Revisão de um PR e o checklist operacional em [`checklists/code-review.md`](checklists/code-review.md).
Não cobre: auditoria de módulo do zero (`AUD`); veredito de nota 10 (→ [24](24-auditoria-final.md));
norma técnica de domínio (fica no volume do domínio); preferência de estilo sem norma (`CON-013`).

---

## Fundamentos

Revisão de código existe para encontrar **defeitos que o autor não viu** e para transferir contexto.
Ela não existe para provar que o revisor leu, para impor gosto, nem para reescrever o PR no estilo do
revisor.

A capacidade humana de encontrar defeitos cai rápido com o tamanho do diff (`AUD-004`). Por isso a
ordem importa mais que a exaustividade: um `MUST` de escopo cedo vale mais que vinte notas de
nomenclatura depois. E ruído tem custo simétrico à omissão (`AUD-001`): treina o autor a ignorar a
próxima revisão.

Código gerado por IA mudou a economia da revisão. O volume de diff sobe, a plausibilidade sobe, a
intenção do autor cai. O revisor precisa assumir que texto correto e fluido pode estar errado no
domínio — exatamente o inverso do viés antigo ("se está mal escrito, está errado").

---

## Capítulo 13.1 — O que a revisão encontra e o que ela não encontra

### REV-001 — A revisão de PR não substitui teste, medição nem auditoria de módulo **[IMUTÁVEL]**

Um PR aprovado prova que **duas pessoas** olharam o diff sob as regras deste volume. Não prova que o
módulo está correto, que a performance cabe no limiar, nem que a autorização cobre todos os caminhos.
Tratar aprovação de PR como DoE é o antipadrão que esvazia os portões G4 e G5.

### REV-002 — O que a revisão encontra bem **[OBRIGATÓRIA]**

Escopo errado; abordagem que não resolve o problema; contrato público alterado sem intenção; teste
ausente ou frágil; migração irreversível; autorização por papel em vez de por objeto; campo sensível
exposto; N+1 óbvio no diff; "enquanto eu estava lá"; segredo em código.

### REV-003 — O que a revisão comprovadamente não encontra **[OBRIGATÓRIA]**

Corrida sob carga; vazamento entre inquilinos em caminho não tocado pelo diff; regressão de
performance sem medição; falha de acessibilidade sem percorrer a tela; inconsistência de domínio
espalhada em arquivos que o PR não abriu. Esses achados exigem teste, medição ou auditoria de módulo
— e o revisor que finge encontrá-los no diff produz falsa segurança.

### REV-004 — Todo PR declara o que **não** foi verificado **[RECOMENDADA]**

Na descrição ou no comentário de aprovação: "não percorri a tela com teclado", "não medi p95", "não
testeie o job irmão". Omissão silenciosa vira confiança falsa no próximo leitor.

---

## Capítulo 13.2 — Ordem de leitura

### REV-005 — Não leia o diff de cima para baixo como padrão **[OBRIGATÓRIA]**

Ler o patch na ordem do Git produz revisão rasa: o revisor reage a cada hunk sem modelo mental do
objetivo. A ordem correta é a de `AUD-006`, aplicada ao artefato:

```
1. Descrição e escopo do PR
2. Testes adicionados ou alterados
3. Migração de schema (se houver)
4. Domínio / regra de negócio
5. Borda (API, fila, webhook, job)
6. Interface
7. Infra / config / dependência
8. Convenções e nit — só se os níveis acima passaram
```

### REV-006 — Comece pela descrição; se ela for vaga, pare **[OBRIGATÓRIA]**

"Corrige bug" e "melhorias" não são descrição. Sem problema, escopo e risco declarados, a revisão
não tem critério. Um único `MUST`: reescreva a descrição antes de continuar.

### REV-007 — Leia os testes antes do código de produção **[OBRIGATÓRIA]**

O teste revela a intenção. Se o teste não falharia sem a mudança (`QAT-004`), o PR não tem prova.
Ler produção primeiro faz o revisor "entender" o código e depois aceitar teste decorativo.

### REV-008 — Migração antes do código que a assume **[OBRIGATÓRIA]**

Schema e aplicação coexistem durante o deploy (`OPS-010`, `DAT-031`). Revisor que só olha o código
novo perde a incompatibilidade com a versão antiga ainda no ar.

### REV-009 — O que só se vê no diff **[OBRIGATÓRIA]**

Linha removida que era a única proteção; rename que muda comportamento; import novo de caminho
interno de outro módulo; constante alterada sem teste; permissão ampliada num enum.

### REV-010 — O que só se vê no arquivo inteiro **[OBRIGATÓRIA]**

Invariante quebrada em método vizinho; estado inválido ainda representável; autorização no controller
e não no caso de uso; duplicação da mesma regra três pastas acima. Abra o arquivo. Diff sozinho
mente por omissão.

### REV-011 — Abra os arquivos irmãos quando o PR toca regra de negócio **[RECOMENDADA]**

O bug irmão (`BAK-002`, `PLB-057`) quase nunca está no hunk. Está no job, no admin, na importação.

---

## Capítulo 13.3 — Tamanho, ritmo e composição do PR

### REV-012 — Respeite o orçamento de `AUD-004`; acima dele, peça decomposição **[OBRIGATÓRIA]**

Não "revise mais rápido". Capacidade humana não escala com o tamanho do PR. Estouro sem justificativa
é `MUST` de escopo (`AUD-005`).

### REV-013 — Formatação e comportamento nunca no mesmo commit **[IMUTÁVEL]**

É `CON-013` e `AUD` aplicados ao PR. Diff cosmético esconde a mudança real e torna o `git blame` e o
bisect inúteis. Peça split; não aprove misturado.

### REV-014 — Refatoração mecânica e mudança de comportamento são PRs separados **[OBRIGATÓRIA]**

Juntas, o revisor não sabe o que validar e o rollback reverte as duas. Se o autor insiste em um PR,
o risco sobe para o próximo nível da matriz (`CON-041`) por construção.

### REV-015 — Dependência nova exige justificativa no PR **[OBRIGATÓRIA]**

O que 30 linhas não resolvem; custo (bytes, superfície, manutenção); quem mantém; caminho de saída
(`SEL-030`, `SEC-043`). Sem isso, um `MUST` — não um nit sobre a versão.

### REV-016 — Arquivos gerados e lockfiles não contam no orçamento **se** estão sozinhos no commit **[RECOMENDADA]**

Misturados com lógica, voltam a contar: o revisor não consegue filtrar.

### REV-017 — PR que "só move arquivos" ainda precisa de revisão de fronteira **[OBRIGATÓRIA]**

Movimentação muda o grafo de dependência. Verifique se algum import atravessou a fronteira de módulo
(`ARC-019`).

---

## Capítulo 13.4 — Comentário útil

### REV-018 — Todo comentário declara a força **[OBRIGATÓRIA]**

Prefixos de [`checklists/code-review.md`](checklists/code-review.md) e `AUD-008`:

| Prefixo | Significado |
| --- | --- |
| `MUST` | Bloqueia merge até resolvido ou aceito com risco registrado |
| `SHOULD` | Esperado; divergir exige justificativa no thread |
| `CONSIDER` | Alternativa; o autor decide |
| `QUESTION` | O revisor não entendeu; resposta pode fechar ou virar `MUST` |
| `PRAISE` | Sinaliza o que manter; raro e específico |
| `NIT` | Preferência menor; máximo 3 por PR |

Comentário sem prefixo é ruído: o autor não sabe se bloqueia.

### REV-019 — `MUST` cita a regra ou o defeito concreto **[OBRIGATÓRIA]**

```
Ruim:  Isso está errado.
Bom:   MUST: autorização por objeto ausente em GET /orders/:id (`SEC-004`).
       Qualquer membro autenticado lê o pedido de outro.
```

Sem ID ou sem caminho de exploração, o `MUST` é opinião com maiúscula.

### REV-020 — Não discuta decisão já registrada no ADR no thread do PR **[OBRIGATÓRIA]**

Se o PR executa um ADR, o lugar de discordar é o ADR — não vinte comentários de implementação.
Um `QUESTION` apontando a tensão basta; reabrir a arquitetura no diff viola `AUD-007`.

### REV-021 — Sugestão de código no comentário é `CONSIDER` ou patch anexado, nunca reescrita silenciosa **[OBRIGATÓRIA]**

O revisor não é coautor oculto. Se a mudança é grande o bastante para reescrever, o achado é de
abordagem (`MUST` de escopo), não um comentário de 40 linhas.

### REV-022 — Máximo de 3 `NIT` por PR **[OBRIGATÓRIA]**

O quarto nit é sintoma de revisão sem defeito real ou de revisor que só olha estilo. Pare. Se só há
nits, aprove.

### REV-023 — Discordar com alternativa e custo **[OBRIGATÓRIA]**

"Eu faria diferente" sem alternativa e sem custo de mudar agora é preferência (`CON-013`). Formato:

```
MUST/SHOULD: <defeito>
Alternativa: <o que fazer>
Custo de mudar agora: <...>
Custo de não mudar: <...>
```

### REV-024 — Ceder também se registra **[RECOMENDADA]**

Quando o autor convence, feche com uma frase do aprendizado. Thread que some sem resolução ensina
ninguém e reaparece no próximo PR.

### REV-025 — Elogio específico ou nenhum **[RECOMENDADA]**

"Bom trabalho" não informa. "O teste de corrida em `reserveStock` pega o caso que o bug reportou" —
informa o que repetir.

---

## Capítulo 13.5 — Revisão de teste

### REV-026 — O teste falharia se a regra fosse removida? **[OBRIGATÓRIA]**

É `QAT-004` aplicado ao PR. Se a resposta é não, o teste é documentação cara, não proteção. `MUST`.

### REV-027 — Teste que só cobre o caminho feliz em mudança de regra é incompleto **[OBRIGATÓRIA]**

Caminho de erro, autorização negada e entrada inválida são o mínimo quando o PR toca regra
(`QAT-019`).

### REV-028 — Não aprove teste que congela comportamento sem o revisor saber se está certo **[IMUTÁVEL]**

É o antipadrão de `QAT-008`: o bug vira especificação. Se o revisor não entende o comportamento
esperado, `QUESTION` até entender — nunca "os testes passam".

### REV-029 — Snapshot e golden file exigem justificativa **[RECOMENDADA]**

Eles passam com quase qualquer mudança cosmética e escondem regressão semântica. Aceitáveis para
saída serializada estável; suspeitos para regra de negócio.

### REV-030 — Teste flaky no PR é `MUST`, não "vamos ver no CI" **[OBRIGATÓRIA]**

Entrar flaky é aceitar ruído permanente no pipeline (`QAT` sobre estabilidade). Peça isolamento ou
remoção da causa (tempo real, ordem, rede).

---

## Capítulo 13.6 — Revisão de migração e de dados

### REV-031 — Migração sem reversa executada é incompleta **[OBRIGATÓRIA]**

`DAT-030`. "Tem down" não basta — foi rodada em ambiente com dado?

### REV-032 — Conte registros que violam a nova regra **[OBRIGATÓRIA]**

`PLB-040`, `DAT-032`. Migração que assume dado limpo falha em produção ou preenche padrão mentiroso.

### REV-033 — Aditivo primeiro; destrutivo em fase própria **[OBRIGATÓRIA]**

`DAT-031`, `PLB-041`. Remover coluna no mesmo PR que para de escrever nela, sem a fase de leitura
dupla, é `MUST` de risco `R3`/`R4`.

### REV-034 — Migração de dados é `R4` até prova em contrário **[OBRIGATÓRIA]**

`CON-041`, `PLB-045`. Backup, lotes, contagem, abort criterion. Se falta, bloqueie — não "aprove com
cuidado".

### REV-035 — Verifique bloqueio de tabela na versão do banco em uso **[OBRIGATÓRIA]**

`DAT-033`. O revisor confirma a versão no perfil do projeto; não presume Postgres "moderno".

---

## Capítulo 13.7 — Segurança, contrato e operação no PR

### REV-036 — Qualquer superfície nova nasce inacessível até autorização declarada **[OBRIGATÓRIA]** · `S0`

`SEC-005`, `PLB-020`. Endpoint, job, tela admin, exportação.

### REV-037 — Diff que toca dado de usuário, dinheiro ou permissão exige revisor de segurança ou checklist OWASP **[OBRIGATÓRIA]**

Não basta o revisor de domínio. `ORC-012`.

### REV-038 — Mudança de contrato público sem versão ou compatibilidade é `MUST` **[OBRIGATÓRIA]**

Campo removido, significado alterado, erro que muda de formato, paginação que quebra cliente.
Cite `BAK-036` / Volume 15 quando existir; até lá, trate como alteração incompatível.

### REV-039 — O PR declara como se detecta falha em produção e como se reverte **[OBRIGATÓRIA]**

Sem métrica, log correlacionável ou flag, a mudança é opaca (`OPS-013`, `OPS-018`). Para `R3`/`R4`,
é bloqueante (`CON-041`).

### REV-040 — Feature flag sem plano de remoção é dívida disfarçada **[RECOMENDADA]**

Entre no backlog com gatilho, ou o flag vira permanente e dobra os caminhos de teste.

---

## Capítulo 13.8 — Código gerado por IA

### REV-041 — Trate saída de IA como entrada não confiável de alta plausibilidade **[IMUTÁVEL]**

Não é rascunho amador. É texto fluente que pode estar errado no domínio, inventar API, omitir
autorização e copiar padrão vizinho sem a invariante. O ônus da prova é o mesmo de qualquer PR —
com atenção extra a omissões.

### REV-042 — Volume alto de PR gerado não reduz o padrão de revisão **[OBRIGATÓRIA]**

Aprovar mais rápido porque "a IA escreveu muito" é exatamente como defeitos entram em massa.
Decomponha (`AUD-004`) ou rejeite por tamanho.

### REV-043 — Exija que o autor explique a intenção em linguagem de negócio **[OBRIGATÓRIA]**

Se o autor não consegue explicar sem reler o diff, ele não revisou a saída da IA. `MUST` na
descrição: problema, abordagem, o que não cobre.

### REV-044 — Procure o padrão colado sem a proteção do original **[OBRIGATÓRIA]**

IA copia o happy path do arquivo vizinho e esquece o filtro de inquilino, o limite, o timeout.
Diff "parecido com o resto" é sinal de alerta, não de qualidade.

### REV-045 — Testes gerados por IA passam no mesmo crivo `REV-026` **[OBRIGATÓRIA]**

Teste que espelha a implementação linha a linha não protege. Peça caso de negócio e caso de falha.

---

## Capítulo 13.9 — Quando bloquear, quando aprovar, pressão

### REV-046 — Bloqueie por defeito, contrato, segurança, dado ou teste que não prova **[OBRIGATÓRIA]**

Não bloqueie por gosto, por "eu faria diferente" sem custo, nem por nit.

### REV-047 — Aprovar com comentários abertos só se nenhum for `MUST` **[OBRIGATÓRIA]**

`SHOULD` aberto vira item de backlog com dono e prazo, ou é resolvido. Aprovar com `MUST` aberto é
fraude de processo.

### REV-048 — Pressão de prazo não rebaixa `S0`/`S1` nem `R4` **[IMUTÁVEL]**

`SEC-066`, `CON-042`. A saída honesta é: reduzir escopo, feature flag off, ou aceitação de risco
**com nome de pessoa**. "Aprova aí que a gente corrige depois" sem registro é o incidente futuro.

### REV-049 — Autoaprovação só com regra explícita no perfil do projeto **[OBRIGATÓRIA]**

Equipe de um ou dois precisa de regra escrita (o que pode autoaprovar, o que exige segundo olhar).
Sem regra, autoaprovação de `R3`/`R4` e de segurança é proibida.

### REV-050 — Tempo de resposta de revisão é métrica de fluxo, não de virtude **[RECOMENDADA]**

PR parado três dias ensina a pular revisão ou a abrir PRs enormes. Limiar no perfil (`[perfil]`);
orquestrador age quando estoura — não o revisor individual como herói.

### REV-051 — Quando o código está certo e a abordagem está errada, um `MUST` de escopo **[OBRIGATÓRIA]**

`AUD-007`. Não comente a implementação. Volte à decisão. Implementação impecável da abordagem
errada é desperdício total.

### REV-052 — Segunda revisão após mudança substancial **[OBRIGATÓRIA]**

"LGTM" no primeiro round não cobre um push que reescreveu a migração. Peça re-review explícito; não
assumir.

---

## Capítulo 13.10 — O revisor

### REV-053 — Quem implementou não aprova o próprio PR em mudança `R3`/`R4` **[IMUTÁVEL]**

`AUD-003` aplicado ao PR. Em `R1`/`R2`, siga o perfil do projeto (`REV-049`).

### REV-054 — Revisor declara o que não olhou **[OBRIGATÓRIA]**

Mesma lógica de `REV-004`. Aprovação sem fronteira de cobertura é teatro (`AUD-002`).

### REV-055 — Bikeshedding é falha do revisor, não do autor **[OBRIGATÓRIA]**

Discussão longa sobre nome de variável enquanto autorização está aberta viola `AUD-001` por excesso
no lugar errado. Pare, abra o `MUST` real, feche os nits.

### REV-056 — Revisão que só olha estilo é revisão não feita **[OBRIGATÓRIA]**

Aproveitar o PR para formatar não conta como níveis 1–6 de `AUD-006`. Se só há estilo, ou não há
defeito (aprove) ou o revisor não leu (releia).

### REV-057 — Não use o PR para ensinar carreira **[RECOMENDADA]**

Mentoria fora do thread. No PR, só o que afeta este merge. Thread pedagógico alonga o ciclo e mistura
bloqueio com aula.

### REV-058 — Checklist marcado sem evidência não conta **[IMUTÁVEL]**

`AUD-002`. Item de [`checklists/code-review.md`](checklists/code-review.md) exige `OK` com nota, ou
`N/A` com motivo. Marcação em bloco é `MUST` de processo — reabra a revisão.

---

## Padrões reutilizáveis

**Padrão: comentário em três linhas.** Força · defeito com ID · alternativa/custo. Cabe no celular do
autor e força o revisor a ser preciso.

**Padrão: split checklist no topo do PR.** Autor cola o que o revisor deve olhar primeiro (migração,
auth, contrato). Reduz ida e volta; não substitui a ordem de `REV-005`.

**Padrão: "re-review needed" label.** Depois de push que toca migração, auth ou contrato, o autor
remove a aprovação anterior. Evita merge de round 1 com código de round 3.

**Padrão: par de revisão para IA.** Autor cola o prompt ou a origem da geração na descrição. O
revisor sabe onde desconfiar (geração vs edição humana).

---

## Matrizes de decisão

| Situação | Ação |
| --- | --- |
| Escopo errado | Um `MUST`; pare o resto (`AUD-007`) |
| Abordagem errada, código limpo | `MUST` de escopo; sem nits de implementação |
| Só nits | Aprove; no máximo 3 (`REV-022`) |
| `MUST` de segurança | Bloqueia; sem rebaixamento por prazo (`REV-048`) |
| PR > orçamento sem justificativa | Peça split (`REV-012`) |
| Formatação + comportamento | Peça commits separados (`REV-013`) |
| Autor não explica intenção (IA) | `MUST` na descrição (`REV-043`) |
| Teste não falharia sem a mudança | `MUST` (`REV-026`) |
| Discorda do ADR | Leve ao ADR; um `QUESTION` no PR (`REV-020`) |

| Prefixo | Bloqueia merge? | Exige citação de regra? |
| --- | --- | --- |
| `MUST` | Sim | Sim (`REV-019`) |
| `SHOULD` | Não, se justificado | Recomendado |
| `CONSIDER` | Não | Não |
| `QUESTION` | Até resposta | Não |
| `NIT` | Não | Não |

---

## Fluxo de trabalho

```
1. Ler descrição → vaga? MUST e pare
2. Classificar risco (R1–R4) e se toca auth/dado/dinheiro
3. Ler testes → migração → domínio → borda → UI
4. Abrir arquivo inteiro nos pontos de regra e auth
5. Percorrer checklist/code-review.md nível a nível; parar no primeiro que reprova
6. Comentar com prefixo; ≤3 NIT
7. Declarar o que não foi olhado
8. Aprovar / pedir mudanças / MUST de escopo
9. Se push substancial → re-review (REV-052)
```

Playbook relacionado: correção de bug (`PLB-055`–`PLB-058`) — o PR de bug sem teste que falha antes
é incompleto por construção.

---

## Exemplos de implementação

```
// Ruim — comentário sem força nem regra
// "Acho melhor extrair isso."

// Bom — REV-018, REV-019
// MUST: GET /invoices/:id autoriza só por papel (`SEC-004`).
// Qualquer membro lê fatura de outro inquilino se adivinhar o id.
// Alternativa: authorize(invoice, actor) no caso de uso, como em GET /orders/:id.
```

```
# Ruim — descrição de PR gerado por IA
"Update orders module"

# Bom — REV-043
Problema: cancelamento após pagamento parcial deixava saldo inconsistente.
Abordagem: transição explícita Paid → PartiallyRefunded no agregado; job de estorno idempotente.
Não cobre: estorno parcial multi-moeda (backlog).
Teste: orders/cancel.test.ts falha se a transição ilegal for permitida.
Risco: R2. Rollback: reverter PR; flag refund_v2 off.
```

```
// Ruim — teste que espelha a implementação (REV-045, REV-026)
expect(calculateTotal(items)).toBe(items.reduce((s, i) => s + i.price * i.qty, 0))

// Bom — caso de negócio
it("does not allow total to include items removed before checkout", ...)
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Aprovar sem ler | Teatro; `AUD-002` |
| Ler só o diff, nunca o arquivo | Perde invariante vizinha (`REV-010`) |
| Diff de cima para baixo | Revisão rasa (`REV-005`) |
| Bikeshedding de nome com auth aberta | `AUD-001` por excesso no lugar errado |
| Reescrever o PR no comentário | Vira coautoria oculta; use `MUST` de escopo |
| Aprovar com `MUST` aberto | Fraude de processo (`REV-047`) |
| "LGTM" sob pressão em `S0` | Incidente com nome (`REV-048`) |
| Congelar bug em teste | `QAT-008` |
| Formatação + lógica no mesmo commit | Bisect e blame inutilizáveis (`REV-013`) |
| Revisar código de IA mais rápido | Defeitos em massa (`REV-042`) |
| Autoaprovação de `R4` sem regra | Viola `AUD-003` / `REV-053` |
| Checklist marcado em bloco | Revisão não feita (`REV-058`) |

---

## Checklist

- [ ] Descrição clara; senão, `MUST` e pare. (`REV-006`)
- [ ] Ordem: testes → migração → domínio → borda → UI. (`REV-005`)
- [ ] Arquivo inteiro aberto nos pontos de regra/auth. (`REV-010`)
- [ ] Orçamento `AUD-004` ou justificativa. (`REV-012`)
- [ ] Sem mistura formatação/comportamento. (`REV-013`)
- [ ] Comentários com prefixo; `MUST` cita regra. (`REV-018`, `REV-019`)
- [ ] ≤3 `NIT`. (`REV-022`)
- [ ] Teste falharia sem a mudança. (`REV-026`)
- [ ] Migração: reversa, contagem, fases. (`REV-031`–`REV-034`)
- [ ] Superfície nova com auth. (`REV-036`)
- [ ] Contrato público compatível ou versionado. (`REV-038`)
- [ ] Detecção e rollback declarados se `R3`+. (`REV-039`)
- [ ] Se IA: intenção do autor explícita. (`REV-043`)
- [ ] Nenhum `MUST` aberto na aprovação. (`REV-047`)
- [ ] Declarado o que não foi olhado. (`REV-054`)
- [ ] Checklist de code-review com evidência, não bloco. (`REV-058`)

---

## Prompt do volume

```
You are reviewing one pull request under EOS Volume 13 (REV).

Load: agents/_shared/core-contract.md, agents/_shared/output-schemas.md,
00-constituicao-da-engenharia.md, 13-revisao-de-codigo.md,
checklists/code-review.md, and the domain volumes touched by the diff.

Sequence (mandatory):
1. Read the PR description. If vague, emit one MUST and stop.
2. Classify risk R1–R4 and whether auth, money, or personal data is touched.
3. Read in order: tests → migrations → domain → edges → UI.
4. Open full files at rule and authorization points; do not trust the diff alone.
5. Walk checklists/code-review.md; stop at the first failing level.
6. Comment with MUST/SHOULD/CONSIDER/QUESTION/PRAISE/NIT (max 3 NIT).
7. Every MUST cites a rule ID or a concrete exploit path.
8. Declare what you did not verify.
9. Verdict: approve / request changes / scope MUST.

Do not: bikeshed names while auth is open; rewrite the PR in comments;
approve with open MUST; lower S0/S1 or R4 for deadline pressure; rubber-stamp
AI-generated volume.

Output: list of comments (prefix, file:line, rule ID, cost), coverage declaration,
and merge verdict.
```

---

## Critérios de aceite

Um PR só é aprovado sob este volume quando:

1. Passou pelos níveis aplicáveis de [`checklists/code-review.md`](checklists/code-review.md) com
   evidência (`REV-058`).
2. Nenhum `MUST` permanece aberto (`REV-047`).
3. Testes novos ou alterados falhariam sem a mudança (`REV-026`).
4. Se há migração, reversa e contagem foram verificadas (`REV-031`, `REV-032`).
5. Se toca auth/dado/dinheiro, o nível de verificação de segurança foi declarado (`REV-037`).
6. O revisor registrou o que não olhou (`REV-054`).
7. Quem aprova não é quem implementou, quando `R3`/`R4` (`REV-053`).

---

## Verificação obrigatória de saída

```
## PR
Título/ID: <...>
Risco: R<1-4> | Auth/dado/dinheiro: <sim/não>
Autor usou IA: <sim/não/desconhecido>

## Cobertura da revisão
| Nível (AUD-006 / checklist) | Veredito | Evidência |
| Escopo | | |
| Correção | | |
| Seg. e dados | | |
| Contratos | | |
| Testes | | |
| Operação | | |
| Clareza | | |
| Convenções | | |

## Comentários
| Prefixo | Arquivo:linha | Regra | Resumo |

## Não verificado
| Item | Motivo |

## Veredito
<approve | changes requested | scope MUST>
MUST abertos: <0 ou lista>
Re-review necessário após push? <sim/não>
```
