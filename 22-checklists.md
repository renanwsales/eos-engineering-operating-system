# 📙 Volume 22 — Checklists

Prefixo: `CHK` · Regras: CHK-001 a CHK-048 · Papel: [Auditor Final](agents/10-final-auditor.md)

Checklist não é documentação. É **memória externa sob pressão**: a ferramenta que impede o profissional
competente de pular o passo que ele já "sabe" e que, justamente por isso, esquece quando o prazo aperta.
Sem doutrina, o checklist vira teatro — mil caixas marcadas, zero verificação — e produz
afirmação não verificada em escala industrial (`AUD-002`, decisão `EOS-005`).

Este volume não lista as verificações de segurança, performance ou merge. Essas listas vivem nos arquivos
de [`checklists/`](checklists/) e nos volumes de domínio. Aqui mora o mecanismo: o que faz um item
funcionar, quando a lista deve encolher, quem assina cada caixa, e quando a verificação sai do checklist
e entra no pipeline.

**Fronteira.** Doutrina de verificação por checklist: leitura vs confirmação, limite de tamanho, redação
de item, estados `OK` / `N/A` / `PENDENTE`, assinatura, automação e índice canônico em
[`checklists/`](checklists/). Não é: o conteúdo das listas de domínio (fica no volume dono e nos arquivos
citados); a auditoria de módulo (`AUD`, → [12](12-auditoria.md)); o portão de nota 10
(`FIN`, → [24](24-auditoria-final.md)); revisão de um PR concreto (`REV`, → [13](13-revisao-de-codigo.md));
a DoD em si (`CON-043`).

---

## Fundamentos

A mente humana sob carga segura cerca de sete itens e perde o oitavo. Em incidente, em merge às 18h, ou
num PR de 400 linhas, o oitavo item é quase sempre o que importa: autorização por objeto, contagem de
linhas existentes, rollback testado. O checklist existe porque **competência não substitui atenção
dividida**.

Há duas falhas simétricas (`AUD-001`). Omissão: não verificar. Excesso: lista tão longa que ninguém lê —
e então a omissão volta disfarçada de conformidade. Listas de 500 ou 1.000 itens (`EOS-005`) não são
rigor; são a forma mais barata de produzir `AUD-002` sem parecer negligente. As regras com ID do EOS já
são a lista granular e citável. O checklist operacional é o subconjunto **executável em minutos** no
momento certo.

Dois tipos de lista não se misturam. Checklist de **leitura** orienta descoberta ("o que mapear antes de
julgar"). Checklist de **confirmação** exige prova ("rodei o comando; a saída está aqui"). Marcar o
segundo como se fosse o primeiro é fraude de processo: a caixa preenchida mente sobre o que aconteceu.

---

## Capítulo 22.1 — Memória sob pressão

### CHK-001 — Checklist existe para o momento em que a memória falha **[IMUTÁVEL]**

Use checklist quando o custo de esquecer um passo supera o custo de percorrer a lista: merge, deploy,
resposta a incidente, auditoria G5, revisão de auth/dado/dinheiro. Não use para "lembrar de escrever
código limpo" — isso não é verificável em minutos e falha `A-003`.

Consequência de não ter lista no momento certo: o passo crítico depende de sorte e de quem está de plantão.

### CHK-002 — Competência não autoriza pular o checklist **[IMUTÁVEL]**

O autor sênior que "já sabe" é exatamente quem marca sem olhar. Experiência reduz o tempo por item; não
elimina a obrigação de evidência (`AUD-002`).

### CHK-003 — Um checklist serve a um momento, não a um domínio inteiro **[OBRIGATÓRIA]**

"Checklist de backend" é domínio demais. Momentos válidos: pré-análise (G0), pré-merge do autor, code
review, módulo concluído (G5), segurança OWASP no caminho tocado, performance com medição,
acessibilidade da tela alterada. Se a lista tenta cobrir "tudo de backend", ela será ignorada ou
marcada em bloco.

### CHK-004 — O checklist não substitui a norma **[IMUTÁVEL]**

Item sem ID de regra rastreável é preferência. A norma mora no volume (`A-001`); o checklist só aponta
o momento em que ela deve ser confrontada com evidência. Duplicar o texto da regra no item cria segunda
fonte de verdade que envelhece sozinha.

### CHK-005 — Sob pressão de prazo, o checklist encolhe por prioridade declarada — nunca some **[OBRIGATÓRIA]**

Redução legítima: só seções A/B/D da DoD em `S0` de produção (`CON-044`), com backlog imediato. Sumir
com a lista "porque urgência" é o mecanismo clássico do incidente às 3h (`CON-045`).

---

## Capítulo 22.2 — Leitura versus confirmação

### CHK-006 — Declare o tipo da lista no cabeçalho **[OBRIGATÓRIA]**

| Tipo | Pergunta que responde | Evidência esperada |
| --- | --- | --- |
| Leitura | O que preciso entender antes de julgar? | Mapa, lista de zonas, perguntas abertas |
| Confirmação | Isto foi verificado agora? | Saída de comando, contagem, percurso nomeado |

Misturar os dois no mesmo bloco sem rótulo faz o executor tratar descoberta como prova.

### CHK-007 — Checklist de leitura proíbe veredito **[OBRIGATÓRIA]**

Em G0 (`CON-057`, [`pre-analise.md`](checklists/pre-analise.md)), marcar item não autoriza propor
mudança. Opinar cedo produz achado superficial. Se o item convida a "listar problemas", está no tipo
errado.

### CHK-008 — Checklist de confirmação exige evidência anexável **[IMUTÁVEL]**

"Testes passam" sem saída é falha (`AUD-002`). O item de confirmação nomeia o artefato: comando,
screenshot de plano de execução, trecho de log, ID do job no CI. Sem artefato, o estado correto é
`PENDENTE`, não `OK`.

### CHK-009 — Não converta leitura em confirmação por pressão social **[OBRIGATÓRIA]**

"Já mapeamos o terreno" não vira `OK` de "autorização por objeto verificada". São momentos diferentes.
Converter um no outro encurta a rodada e fura G4 (`CON-061`).

### CHK-010 — Um item não pode ser ao mesmo tempo "explore" e "prove" **[OBRIGATÓRIA]**

Se o enunciado pede descoberta e prova, divida em dois itens ou em duas listas. Item híbrido é marcado
como prova sem exploração — ou explorado sem prova.

---

## Capítulo 22.3 — Por que listas longas falham

### CHK-011 — Lista longa falha por economia de atenção, não por falta de virtude **[IMUTÁVEL]**

Com dezenas de itens sob prazo, o custo marginal de ler o próximo item supera o benefício percebido.
O executor otimiza: marca o bloco. O relatório fica verde. A garantia morreu. Esta é a falha que
`EOS-005` recusou institucionalizar: checklist de 500–1.000 itens como produto.

### CHK-012 — Marcar sem ler é a falha mais grave do framework aplicado a checklists **[IMUTÁVEL]**

É `CON-043` e `AUD-002` no instrumento: a caixa mentirosa corrompe todo relatório que a cita. Prefira
lista curta com três `PENDENTE` honestos a lista longa toda `OK` sem evidência.

### CHK-013 — As 735 regras com ID não são um checklist operacional **[OBRIGATÓRIA]**

O índice ([`RULES-INDEX.md`](RULES-INDEX.md)) é citável e pesquisável. Operar "marque se cumpriu cada
regra do livro" recria a lista de mil itens. Operação usa o subconjunto do momento; auditoria cita a
regra pelo ID quando encontra violação.

### CHK-014 — Acúmulo é o inimigo; contexto de uso é a divisão correta **[OBRIGATÓRIA]**

Se o domínio "parece" exigir mais de 25 itens no checklist do volume (`A-011`), o domínio tem
submomentos. Divida por contexto (pré-merge vs G5 vs OWASP), não por acúmulo alfabético de preocupações.

### CHK-015 — Cada item além do limite reduz a taxa de leitura real **[RECOMENDADA]**

Trate 25 como teto duro por artefato de checklist de volume; nos arquivos de [`checklists/`](checklists/),
prefira seções com cabeçalho de parada ("reprovou? pare") a uma parede única. Seção com critério de
parada precoce protege atenção (`AUD-006`).

---

## Capítulo 22.4 — Limite e divisão

### CHK-016 — Checklist de volume: no máximo 25 itens **[OBRIGATÓRIA]**

Cada item verificável em minutos e rastreável a uma regra por ID (`A-011`). Estouro sem divisão é
defeito de autoria, não de disciplina do leitor.

### CHK-017 — Checklist operacional em `checklists/` divide por nível ou bloco com parada **[OBRIGATÓRIA]**

Modelo: [`code-review.md`](checklists/code-review.md) — níveis; pare no primeiro que reprova.
Modelo: [`acessibilidade.md`](checklists/acessibilidade.md) — automático / teclado / leitor.
Não publique uma única lista plana de 80 caixas sem critério de parada.

### CHK-018 — Ao crescer, fatie por momento ou por superfície — nunca por "capítulo do livro" **[OBRIGATÓRIA]**

Fatiar "como o sumário do volume 6" reproduz a norma inteira. Fatiar "tela alterada", "caminho de
pagamento", "migração desta rodada" produz lista executável.

### CHK-019 — Item que ninguém consegue verificar em cinco minutos não entra **[OBRIGATÓRIA]**

"Arquitetura está limpa" falha `A-003`. Ou vira pergunta concreta com evidência (`arquivo:linha`,
diagrama, ADR), ou sai da lista e vira trabalho de G1.

### CHK-020 — Remova item que o pipeline já bloqueia de forma confiável **[OBRIGATÓRIA]**

Ver `CHK-036`. Checklist que repete o que o CI já falha com sinal claro treina o hábito de marcar sem
olhar o restante.

---

## Capítulo 22.5 — Item bem escrito

### CHK-021 — Enunciado no passado verificável ou na primeira pessoa da ação **[OBRIGATÓRIA]**

| Ruim | Bom |
| --- | --- |
| "Autorização ok" | "Verifiquei autorização por objeto em cada endpoint tocado (`SEC-004`)" |
| "Performance" | "Medi p95 antes/depois com o mesmo método; números no relatório" |
| "Testes" | "Rodei `<comando>`; N passaram / M falharam; saída anexada" |

O ruim convida carimbo. O bom descreve o ato e o artefato.

### CHK-022 — Todo item de confirmação cita a regra ou o artefato mínimo **[OBRIGATÓRIA]**

Citação por ID (`A-012`) ou comando literal. Sem os dois, o item não é auditável por terceiro.

### CHK-023 — Item negativo explícito quando a falha é omissão **[RECOMENDADA]**

"Nenhum segredo no diff" · "Nenhuma asserção afrouxada sem justificativa" · "Nenhum `N/A` sem
motivo". Omissão é o defeito mais comum; enunciado só positivo esconde o buraco.

### CHK-024 — Um item, um veredito **[OBRIGATÓRIA]**

"Auth e tenant e SQL" são três verificações. Item composto recebe um `OK` que mascara dois
`PENDENTE`.

### CHK-025 — Escreva a consequência no item quando o custo de pular não for óbvio **[RECOMENDADA]**

"Contei linhas que violam a nova constraint — senão a migração falha em produção com dado legado"
obedece `A-004`. Item sem consequência é o primeiro a ser pulado sob pressão.

---

## Capítulo 22.6 — Estados: OK, N/A, PENDENTE

### CHK-026 — Só três estados legítimos **[IMUTÁVEL]**

`OK` · `N/A` + justificativa · `PENDENTE`. Inventar "quase", "ok com ressalvas" ou "delegado ao CI"
sem evidência reintroduz ambiguidade que `CON-043` eliminou.

### CHK-027 — `OK` exige verificação nesta execução **[IMUTÁVEL]**

Marcar `OK` porque "passou na sprint passada" ou "o autor disse que validou" é `AUD-002`. Confirmação
é no agora, com evidência desta rodada.

### CHK-028 — `N/A` sem justificativa conta como `PENDENTE` **[IMUTÁVEL]**

Justificativa nomeia por que a verificação não se aplica *neste* escopo ("não há migração neste PR";
"módulo sem UI"). "N/A" sozinho é caixa mentirosa.

### CHK-029 — Um único `PENDENTE` impede `DONE` **[IMUTÁVEL]**

O conjunto fica `PARTIAL` (`CON-043`). Relatório que declara módulo pronto com `PENDENTE` aberto é
rejeitado no portão final (`FIN`).

### CHK-030 — Não use `N/A` para esconder o que não deu tempo **[OBRIGATÓRIA]**

Falta de tempo é `PENDENTE` ou redução declarada com backlog (`CON-044`). `N/A` por preguiça é fraude
de classificação.

---

## Capítulo 22.7 — Quem assina

### CHK-031 — Toda execução de checklist declara executor e papel **[OBRIGATÓRIA]**

Nome (ou identidade do agente) + papel (autor, revisor, auditor final). Sem assinatura, a lista não
tem dono quando o defeito aparece em produção.

### CHK-032 — Autor assina pré-merge; revisor assina code-review; auditor assina módulo concluído **[IMUTÁVEL]**

Separação de papéis (`AUD-003`). Quem implementou não assina G5 como se fosse terceiro. Quem só
revisou o PR não assina DoE do módulo.

### CHK-033 — Assinatura em bloco de seção inteira é inválida **[OBRIGATÓRIA]**

"Tudo OK na seção 3" sem percorrer itens é o padrão que `REV-058` e este volume proíbem. Assine item
a item, ou declare a seção `PENDENTE`.

### CHK-034 — Agente que marca checklist anexa a mesma evidência que um humano **[IMUTÁVEL]**

Narrativa fluida do modelo não é evidência (`AUD-042`). Saída de comando, path:line, contagem.

### CHK-035 — Segundo assinante quando o risco é `R3`/`R4` ou toca auth/dado/dinheiro **[OBRIGATÓRIA]**

Alinhado a revisão de alto risco (`REV-053`). Uma única assinatura de autor em caminho de pagamento é
insuficiente mesmo com checklist verde.

---

## Capítulo 22.8 — Automatizar e sair do checklist

### CHK-036 — O que o CI bloqueia com sinal claro sai do checklist humano **[OBRIGATÓRIA]**

Lint que falha o build, typecheck, teste de contrato no pipeline, axe no CI que bloqueia merge: o
humano não precisa "lembrar" de marcar. O checklist humano fica com o que a máquina não vê —
autorização por objeto no caminho certo, contagem de dado legado, percurso de teclado, intenção do
diff.

### CHK-037 — Automação que só reporta sem bloquear não remove o item humano **[OBRIGATÓRIA]**

Aviso amarelo no CI é decoração (`CON-050` aplicado a gate). Enquanto não bloqueia, o item permanece
no checklist de confirmação.

### CHK-038 — Ao automatizar, registre a remoção e o gate substituto **[RECOMENDADA]**

Nota no cabeçalho do arquivo: "contraste de tokens: agora no job `design-tokens`; removido do
checklist em AAAA-MM-DD". Sem registro, alguém recoloca o item e a lista incha de novo.

### CHK-039 — Nunca automatize o julgamento de escopo ou de intenção **[IMUTÁVEL]**

"O PR faz só o que a descrição diz" e "a asserção foi afrouxada por motivo legítimo" são julgamento.
Script que marca isso automaticamente produz falsa segurança.

### CHK-040 — Preferir um teste que falha a um item eterno no checklist **[RECOMENDADA]**

Regressão que já quebrou produção merece teste nomeado (`QAT`), não eterna caixa "não esquecer o
caso X". Checklist é memória; teste é trava.

---

## Capítulo 22.9 — Índice canônico dos checklists

### CHK-041 — Os sete arquivos em `checklists/` são a lista operacional canônica **[OBRIGATÓRIA]**

| Arquivo | Momento | Tipo | Norma âncora |
| --- | --- | --- | --- |
| [`pre-analise.md`](checklists/pre-analise.md) | G0 | Leitura | `CON-057` |
| [`pre-merge.md`](checklists/pre-merge.md) | Autor antes do PR | Confirmação | `AUD-015`, `CON-043` |
| [`code-review.md`](checklists/code-review.md) | Revisão de PR | Confirmação + parada | `AUD-006`, `REV` |
| [`modulo-concluido.md`](checklists/modulo-concluido.md) | G5 | Confirmação | `CON-062`, `AUD`, `FIN` |
| [`seguranca-owasp.md`](checklists/seguranca-owasp.md) | Caminho com risco | Confirmação | `SEC` |
| [`performance.md`](checklists/performance.md) | Mudança com custo | Confirmação | `PRF` |
| [`acessibilidade.md`](checklists/acessibilidade.md) | UI alterada | Misto (auto + manual) | `UXI` |

Novos checklists operacionais entram neste diretório com cabeçalho de tipo e momento — não como
apêndice de mil linhas num volume.

### CHK-042 — Não forkue checklist canônico por time sem motivo registrado **[OBRIGATÓRIA]**

Cópia "nossa versão" diverge na primeira semana. Extensão legítima: bloco adicional no perfil do
projeto ou item `[perfil]` com limiar local. Fork silencioso produz duas verdades (`A-001`).

### CHK-043 — Checklist de volume aponta para o arquivo operacional; não o duplica **[OBRIGATÓRIA]**

O checklist curto no fim deste volume e dos volumes de domínio rastreia doutrina local. A execução
diária usa [`checklists/`](checklists/). Duplicar os 100 itens de OWASP dentro do volume 6 e do arquivo
garante divergência.

### CHK-044 — Ordem de uso na rodada é a dos portões **[OBRIGATÓRIA]**

```
pre-analise → (trabalho) → pre-merge → code-review → [domínio: SEC/PRF/UXI se tocado] → modulo-concluido
```

Pular `pre-merge` e ir direto a `modulo-concluido` empurra defeito evitável para o auditor e viola a
economia de `AUD-015`.

---

## Capítulo 22.10 — Ciclo de vida e higiene

### CHK-045 — Item obsoleto é removido ou marcado com data e substituto **[OBRIGATÓRIA]**

Checklist que acumula itens mortos ensina a ignorar a lista inteira. Higiene alinhada a `AUD-040`.

### CHK-046 — Mudança de checklist canônico é mudança de processo — com dono **[OBRIGATÓRIA]**

Quem altera [`modulo-concluido.md`](checklists/modulo-concluido.md) altera o portão G5. Diff revisado;
motivo no commit; se altera critério de passagem, mencione no relatório da rodada.

### CHK-047 — Meça aderência pela evidência, não pela taxa de caixas marcadas **[OBRIGATÓRIA]**

100% de `OK` com zero anexos é sinal de falha (`CHK-012`), não de maturidade. Métrica útil: amostragem
de itens `OK` confrontados com artefato; divergência é achado de processo.

### CHK-048 — Em dúvida entre item novo e regra nova, prefira a regra no volume dono **[RECOMENDADA]**

Checklist não é lugar para nascer norma (`A-001`). Se a verificação não tem lar, abra regra no volume
correto e só então aponte o item para o ID.

---

## Padrões reutilizáveis

### Padrão C1 — Cabeçalho mínimo de checklist

```
# Checklist — <Nome>
Tipo: leitura | confirmação
Momento: <portão ou evento>
Executor esperado: <papel>
Norma: <volume ou IDs>
Regra que governa: <uma frase — ex.: sem número, não há achado>
```

Use em todo arquivo novo em [`checklists/`](checklists/).

### Padrão C2 — Parada precoce por nível

Como em [`code-review.md`](checklists/code-review.md): ao reprovar o nível N, um único `MUST` e pare.
Evita `AUD-001` por excesso.

### Padrão C3 — Evidência inline no item

```
- [ ] Typecheck: `pnpm tsc --noEmit` → saída: <colar ou link CI #1234>
```

O formulário força `CHK-008`.

### Padrão C4 — Saída do checklist para o gate

Tabela no README do CI: item removido → job → desde quando. Satisfaz `CHK-038`.

### Padrão C5 — Amostragem anti-teatro

Em G5, o auditor escolhe 3 itens `OK` ao acaso e exige o artefato (`FIN` aplica; doutrina nasce aqui).

---

## Matrizes de decisão

| Situação | Ação |
| --- | --- |
| Precisa lembrar passos sob pressão | Checklist de confirmação do momento |
| Precisa entender antes de julgar | Checklist de leitura (G0) |
| Mais de 25 itens no mesmo artefato | Dividir por momento/superfície (`CHK-014`) |
| CI já bloqueia com sinal claro | Remover item humano (`CHK-036`) |
| CI só avisa | Manter item (`CHK-037`) |
| Tentação de lista "completa" do domínio | Citar `RULES-INDEX`; operar o subconjunto (`CHK-013`) |
| "Não deu tempo" | `PENDENTE` ou `CON-044` — nunca `N/A` falso (`CHK-030`) |
| Autor quer assinar G5 | Recusar (`CHK-032`, `AUD-003`) |
| Item sem ID nem comando | Reescrever ou excluir (`CHK-022`) |
| Proposta de checklist de 500 itens | Recusar (`EOS-005`, `CHK-011`) |

---

## Fluxo de trabalho

1. Identifique o momento (portão ou evento).
2. Abra o arquivo canônico correspondente (`CHK-041`).
3. Declare tipo e executor.
4. Percorra item a item; pare cedo se o modelo do arquivo exigir.
5. Para cada item: `OK` com evidência, `N/A` justificado, ou `PENDENTE`.
6. Assine.
7. Se houver `PENDENTE`, o entregável não é `DONE` (`CHK-029`).
8. Em G5, o auditor confronta amostragem de `OK` com artefato (→ [24](24-auditoria-final.md)).

Playbooks de construção citam checklists; não os reescrevem ([21](21-playbooks.md)).

---

## Exemplos de implementação

```
# Ruim — CHK-021, CHK-012: carimbo
- [x] Segurança
- [x] Testes
- [x] Performance

# Bom — CHK-021, CHK-008
- [x] OWASP controle de acesso: percorri POST /invoices e GET /invoices/:id;
      authorize(invoice, actor) em invoices/create.ts:41 e invoices/get.ts:28 (`SEC-004`)
- [x] `pnpm test -- invoices` → 14 passed, 0 failed (CI #8841)
- [ ] Performance: PENDENTE — sem medição antes; comando: `k6 run scripts/invoice-p95.js`
```

```
# Ruim — CHK-007: veredito dentro de G0
- [x] Problemas encontrados: N+1 em listagem (já propor índice)

# Bom — leitura pura
- [x] Fluxo do pedido: checkout → payment.charge → outbox → worker de fiscal
- [x] Zona de risco: payment.charge, PII em Customer.email
- Perguntas abertas: job fiscal usa a mesma autorização do solicitante?
```

```
# Ruim — CHK-028
- [x] Migração: N/A

# Bom
- [x] Migração: N/A — este PR não altera schema (diff sem /migrations)
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Checklist de 500–1.000 itens | `AUD-002` em massa (`EOS-005`, `CHK-011`) |
| Marcar seção inteira de uma vez | Caixas mentirosas (`CHK-033`) |
| Misturar leitura e confirmação | Falsa prova (`CHK-006`) |
| `N/A` por falta de tempo | Fraude (`CHK-030`) |
| Duplicar OWASP no volume e no arquivo | Duas verdades (`CHK-043`) |
| Autor assina G5 | Viola `AUD-003` / `CHK-032` |
| Manter item que o CI já bloqueia | Fadiga e marcação cega (`CHK-020`) |
| "OK" porque o relatório do agente disse | `AUD-042` |
| Enunciado vago ("qualidade ok") | Falha `A-003` / `CHK-019` |
| Fork silencioso por time | Divergência (`CHK-042`) |
| Taxa de caixas como KPI | Incentiva mentira (`CHK-047`) |
| Norma nascendo só no checklist | Viola `A-001` / `CHK-048` |

---

## Checklist

- [ ] Tipo (leitura/confirmação) declarado no cabeçalho. (`CHK-006`)
- [ ] Momento único; não "domínio inteiro". (`CHK-003`)
- [ ] ≤25 itens no checklist de volume; operacionais com níveis/parada. (`CHK-016`, `CHK-017`)
- [ ] Cada item de confirmação com regra ou comando. (`CHK-022`)
- [ ] Um item, um veredito. (`CHK-024`)
- [ ] Estados só `OK` / `N/A`+motivo / `PENDENTE`. (`CHK-026`)
- [ ] `OK` com evidência desta execução. (`CHK-027`, `CHK-008`)
- [ ] Nenhum `DONE` com `PENDENTE`. (`CHK-029`)
- [ ] Executor e papel assinados; G5 ≠ implementador. (`CHK-031`, `CHK-032`)
- [ ] Sem assinatura em bloco. (`CHK-033`)
- [ ] Itens cobertos por CI bloqueante removidos e registrados. (`CHK-036`, `CHK-038`)
- [ ] Arquivo canônico usado; sem fork silencioso. (`CHK-041`, `CHK-042`)
- [ ] Ordem dos portões respeitada. (`CHK-044`)
- [ ] Sem lista "todas as regras do índice". (`CHK-013`)
- [ ] Amostragem anti-teatro preparada para G5. (`CHK-047`, padrão C5)

---

## Prompt do volume

```
You are applying EOS Volume 22 (CHK) — checklist doctrine.

Load: AUTHORING.md (A-011), 22-checklists.md, 00-constituicao-da-engenharia.md (CON-043),
12-auditoria.md (AUD-002), and the relevant file under checklists/.

Sequence (mandatory):
1. Identify the moment (G0, pre-merge, PR review, domain check, G5).
2. Open the canonical checklist for that moment; declare type: reading vs confirmation.
3. Walk items one by one. Do not batch-tick a section.
4. For each confirmation item: attach evidence (command output, path:line, count) or mark PENDENTE.
5. N/A only with scope justification — never for "no time".
6. Record executor identity and role. Implementer must not sign G5.
7. If any PENDENTE remains, status is PARTIAL — not DONE.
8. If asked to create a 100+ item mega-checklist, refuse (EOS-005 / CHK-011) and propose a split by moment.

Do not: restate domain norms; duplicate OWASP into a new file; treat agent narrative as evidence;
use checkbox completion rate as a quality metric.

Output: checklist execution log (item → state → evidence), signer, and DONE|PARTIAL verdict.
```

---

## Critérios de aceite

Uma execução de checklist só conta sob este volume quando:

1. O arquivo canônico do momento foi usado (`CHK-041`).
2. O tipo estava claro e respeitado (`CHK-006`–`CHK-010`).
3. Todo `OK` de confirmação tem evidência desta execução (`CHK-027`, `CHK-008`).
4. Todo `N/A` tem justificativa de escopo (`CHK-028`).
5. Não há `DONE` com `PENDENTE` (`CHK-029`).
6. Assinatura separa papéis (`CHK-032`).
7. Nenhum carimbo em bloco (`CHK-033`).

---

## Verificação obrigatória de saída

```
## Checklist execution
Arquivo: checklists/<nome>.md
Tipo: leitura | confirmação
Momento: <G0|pre-merge|review|domínio|G5>
Executor: <nome/agente> · Papel: <autor|revisor|auditor>

## Itens
| ID/seção | Estado (OK|N/A|PENDENTE) | Evidência ou justificativa |

## Resumo
OK: <n> | N/A: <n> | PENDENTE: <n>
Veredito do conjunto: DONE | PARTIAL

## Anti-teatro
Amostra de OK reverificada: <lista> | Artefatos ok: <sim/não>
```
