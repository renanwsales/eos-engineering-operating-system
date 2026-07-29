# 📕 Volume 24 — Auditoria Final

Prefixo: `FIN` · Regras: FIN-001 a FIN-052 · Papel: [Auditor Final](agents/10-final-auditor.md)

Este volume é o **portão que não negocia teatro**. A revisão de PR (`REV`) aprova um diff. A auditoria
de módulo (`AUD`) investiga, pontua e caça regressão. Aqui decide-se se o conjunto da rodada — ou o
módulo sob DoE — **merece sair**: se as afirmações foram de fato verificadas, se cada volume aplicável
foi aplicado de verdade, se a nota 10 é excelência ou ausência de reclamação, e o que fica registrado
quando o veredito não é aprovação limpa.

O erro caro que este volume previne: relatório convincente, checklist todo verde, merge autorizado —
e o defeito que ninguém confrontou com evidência. É `AUD-002` no instante em que ainda dá para parar.

**Fronteira.** Portão final (G5 ampliado a veredito de nota, cobertura de volumes, anti-teatro,
discordância com o orquestrador, aprovação parcial com dívida nomeada, auditoria da auditoria). Não
é: como conduzir a investigação do zero (`AUD`, → [12](12-auditoria.md)); revisão de um PR
(`REV`, → [13](13-revisao-de-codigo.md)); doutrina de checklist (`CHK`, → [22](22-checklists.md));
pesos e DoD/DoE (`CON-043`, `CON-046`–`CON-052`); correção do trabalho (o auditor não implementa,
`AUD-003`).

---

## Fundamentos

G5 (`CON-062`) olha o conjunto, não a peça. O auditor final herda essa obrigação e adiciona uma
segunda: **desconfiar do próprio processo de auditoria**. Relatórios de agentes são fluentes por
construção (`AUD-042`). Checklists longos são marcados sem leitura (`CHK-011`). Orquestradores
otimizam por fechamento de rodada. Sem portão anti-teatro, o framework vira cerimônia.

Três distinções sustentam o volume:

1. **Report OK ≠ verificado.** Texto que afirma validação sem artefato conta como falha (`AUD-002`).
2. **Pronto ≠ excelente.** DoD é piso; DoE é teto deliberado (`CON-046`). Ausência de achados não é
   nota 10 (`AUD-029`).
3. **Aprovar parcial ≠ empurrar com a barriga.** Condições e dívidas têm nome, gatilho e dono humano
   (`AUD-037`); sem isso, é `REJECTED` disfarçado.

O auditor não redesenha a solução (`AUD-034`). Ele verifica contra normas, DoD e DoE; defeito novo
genuíno fora do escopo da rodada vai para a próxima, não expande esta em silêncio — salvo bloqueante
de segurança ou regressão introduzida agora.

---

## Capítulo 24.1 — Portão anti-teatro

### FIN-001 — O veredito final trata afirmação sem evidência como falha **[IMUTÁVEL]**

Não como pendência educada. "Os testes passam", "validei localmente", "a IA confirmou" sem saída de
comando ou artefato equivalente → item falho. É `AUD-002` aplicado sem exceção de simpatia.

### FIN-002 — Teatro de processo é motivo suficiente para `REJECTED` **[IMUTÁVEL]**

Escopo não aprovado, backlog não atualizado, DoD carimbada, checklist marcado em bloco: rejeição por
processo é legítima (`AUD-033`). Não é burocracia; é o que mantém as outras garantias reais.

### FIN-003 — O auditor não participa da implementação da rodada que julga **[IMUTÁVEL]**

`AUD-003`. Se o mesmo agente implementou e "auditou", o portão não ocorreu. Declare conflito e
reassine com outro papel ou humano.

### FIN-004 — Pressão de prazo não rebaixa bloqueante **[IMUTÁVEL]**

Alinhado a `REV-048` e `CON-044`: só `S0` de produção autoriza DoD reduzida, com dívida imediata.
"O cliente espera" não autoriza `APPROVED` com `S1` aberto.

### FIN-005 — Primeira linha do entregável é o veredito **[OBRIGATÓRIA]**

`AUD-032`. Tudo depois é justificativa. Relatório que enterra o veredito no parágrafo quinze treina
o leitor a não ler.

### FIN-006 — Anti-teatro amostral é obrigatório em toda rodada não trivial **[OBRIGATÓRIA]**

Escolha no mínimo três afirmações `OK` (validação, item de checklist, ou achado "ausente") e
reconstrua a evidência. Se a amostra falha, trate o relatório inteiro como não confiável até nova
passagem — não "corrija só os três".

---

## Capítulo 24.2 — Report OK versus realmente verificou

### FIN-007 — Tabela de verificação de afirmações é seção obrigatória **[OBRIGATÓRIA]**

Para cada `CHANGE REPORT` da rodada:

| Mudança | Validação declarada | Evidência encontrada | Veredito |

Veredito por linha: `verified` | `failed` | `not_run`. Qualquer `failed`/`not_run` em validação
obrigatória da DoD bloqueia `APPROVED`.

### FIN-008 — "Melhorou performance" sem antes/depois pelo mesmo método é falha **[OBRIGATÓRIA]**

Não é `OPPORTUNITY`. É afirmação inválida (`PRF` / `CON-054`). Remova a afirmação ou produza o
número; não aprove a narrativa.

### FIN-009 — Correção de segurança não se valida só com "testes passam" **[OBRIGATÓRIA]**

Exija o caminho de exploração demonstrado como fechado (`CON-061`). Teste verde sem o exploit path
é teatro de segurança.

### FIN-010 — O auditor reexecuta a suíte relevante, types e lint no escopo **[OBRIGATÓRIA]**

Delegar ao relatório do implementador viola `FIN-001`. Reexecução pode ser o job de CI cujo log o
auditor abre e confere — desde que o log seja desta revisão, não de uma run antiga "parecida".

### FIN-011 — Evidência de outrem exige rastreio até o artefato bruto **[OBRIGATÓRIA]**

Link para comentário "passou" ≠ log. Abra o log. Confira o comando, o exit code, o escopo dos testes.
Resumo gerado por agente é narrativa (`AUD-042`).

### FIN-012 — Declaração de "não pude validar" só vale com comando exato para humano **[OBRIGATÓRIA]**

`CON-061`. Sem o comando, é omissão. Com o comando, o item fica `PENDENTE`/`PARTIAL` até execução —
não vira `OK` por honestidade.

---

## Capítulo 24.3 — Ordem de leitura do portão final

### FIN-013 — Ordem fixa; não comece pelas notas **[OBRIGATÓRIA]**

```
1. Diff completo da rodada (conjunto)
2. Propostas aprovadas vs arquivos tocados (escopo)
3. Verificação de afirmações / evidências
4. Testes alterados (asserção afrouxada?)
5. DoD item a item por mudança
6. Regressões e interações (AUD-019)
7. Backlog: reportadas vs registradas
8. Cobertura de volumes aplicáveis
9. Notas por dimensão
10. Veredito e risco residual
```

Começar pelas notas ancora o auditor no número que deseja justificar. A ordem acima ancora na
evidência.

### FIN-014 — Leia o diff do conjunto antes dos relatórios parciais **[OBRIGATÓRIA]**

`AUD-018`. Relatórios por mudança escondem contradição entre mudanças. O portão final existe para
ver o que só o conjunto mostra.

### FIN-015 — Pare no primeiro bloqueante estrutural **[OBRIGATÓRIA]**

Escopo infiltrado, `S0`, afirmação central sem evidência: registre `REJECTED` (ou o bloqueante) e
não gaste páginas em nomenclatura. Economia simétrica a `AUD-006`.

### FIN-016 — Checklist operacional deste portão é `modulo-concluido.md` **[OBRIGATÓRIA]**

[`checklists/modulo-concluido.md`](checklists/modulo-concluido.md), executado sob doutrina `CHK`,
não carimbado. Este volume interpreta o veredito; o arquivo lista as caixas.

---

## Capítulo 24.4 — Cobertura de volumes

### FIN-017 — Declare quais volumes eram aplicáveis e quais foram de fato aplicados **[OBRIGATÓRIA]**

Tabela obrigatória:

| Volume | Aplicável? | Aplicado? | Evidência | Risco se não |

"Não olhamos segurança porque o PR era pequeno" em caminho que toca auth é falha, não N/A.

### FIN-018 — Camadas de análise omitidas são risco nomeado, não silêncio **[OBRIGATÓRIA]**

`CON-027` / declaração de cobertura. Omissão silenciosa vira confiança falsa no próximo leitor
(`REV-004` no nível módulo).

### FIN-019 — Segurança é sempre aplicável quando auth, PII, dinheiro ou upload entram no diff **[IMUTÁVEL]**

`ORC-012`. Nessa condição, [`seguranca-owasp.md`](checklists/seguranca-owasp.md) ou revisão
equivalente não é opcional. Nota de segurança < 6 limita o veredito (`AUD-030`).

### FIN-020 — Performance só "aplicada" com medição ou com N/A justificado por ausência de caminho quente **[OBRIGATÓRIA]**

Hipótese sem número não conta como cobertura `PRF` (`PRF-001` / checklist de performance).

### FIN-021 — Multi-tenant aplicável exige evidência de isolamento no ponto interno **[OBRIGATÓRIA]**

Citar `MTN` / `SEC` no relatório sem mostrar filtro de inquilino no caminho tocado é cobertura
teatral.

### FIN-022 — Volume aplicável não aplicado bloqueia `APPROVED` limpo **[OBRIGATÓRIA]**

Máximo: `APPROVED WITH CONDITIONS` se a lacuna é trivial e verificável; senão `REJECTED` ou
`CHANGES REQUESTED` conforme `AUD-031`. Lacuna de DoE em módulo não crítico pode ser `OPPORTUNITY`
registrada — lacuna de DoD não.

---

## Capítulo 24.5 — Bloqueantes

### FIN-023 — Bloqueantes sem negociação **[IMUTÁVEL]**

| Condição | Efeito |
| --- | --- |
| Qualquer `S0` | Total ≤ 4, `REJECTED` |
| Qualquer `S1` não corrigido | Total ≤ 4, `REJECTED` |
| Escopo não aprovado | `REJECTED` (`AUD-023`) |
| Afirmação de validação obrigatória sem evidência | Trata como falha; bloqueia `APPROVED` |
| Backlog: reportadas ≠ registradas | Bloqueia (`AUD-035`, `CON-019`) |
| Regressão introduzida na rodada | `REJECTED` / volta a G1 (`CON-064`) |
| Implementador = auditor | Portão inválido (`FIN-003`) |

Travas alinhadas a `AUD-030` e `CON-052`; este volume as aplica no fechamento.

### FIN-024 — Teste afrouxado sem justificativa de correção do comportamento antigo é `S1` **[OBRIGATÓRIA]**

`AUD-020`, `QAT-008`. Inspeção obrigatória de **cada** teste modificado no diff do conjunto.

### FIN-025 — Dependência nova não prevista na proposta é bloqueante de escopo **[OBRIGATÓRIA]**

`AUD-025`. Não é nit de estilo.

### FIN-026 — Remoção de código sem justificativa é mudança de comportamento não proposta **[OBRIGATÓRIA]**

`AUD-024`. Trate como escopo infiltrado.

### FIN-027 — Segurança < 6 → no máximo `APPROVED WITH CONDITIONS` **[IMUTÁVEL]**

Mesmo sem `S0`/`S1` abertos. Condições devem fechar o caminho até a nota mínima acordada, com prazo.

---

## Capítulo 24.6 — Nota 8 versus nota 10

### FIN-028 — Nota 10 exige DoE na dimensão; ausência de problemas não basta **[IMUTÁVEL]**

`CON-046`, `AUD-029`. Módulo sem achados, sem testes, sem observabilidade e sem ADR fica em torno de
5: **não se sabe se funciona**.

### FIN-029 — Faixa 8–9: DoD folgada; lacunas de DoE conhecidas e registradas **[OBRIGATÓRIA]**

`AUD-028`. Se a lacuna de DoE não está no backlog com gatilho, a nota correta é ≤7 (há `S2`
não registrado → 4–5).

### FIN-030 — Não negocie nota para "motivar o time" **[OBRIGATÓRIA]**

Nota inflada corrompe tendência e priorização (`CON-050`). O portão final otimiza verdade operacional,
não moral.

### FIN-031 — Justificativa por dimensão cita evidência, não impressão **[OBRIGATÓRIA]**

"Arquitetura 9 porque está limpa" é inválido. "Arquitetura 8: fronteiras ok em `billing/`; ciclo
evitado; lacuna DoE: estados inválidos ainda representáveis — `EOS-…`" é válido.

### FIN-032 — Peso das dimensões é o de `CON-052` / `AUD-027` — sem remanejo ad hoc **[IMUTÁVEL]**

Remanejar peso para salvar a nota total é fraude de métrica.

### FIN-033 — Meta razoável entre rodadas é +1 na dimensão mais fraca, não 10 universal **[RECOMENDADA]**

`CON-048`. Exigir DoE em módulo periférico é erro de priorização, não rigor.

---

## Capítulo 24.7 — Pronto versus excelente

### FIN-034 — `APPROVED` exige DoD completa no escopo da rodada, não DoE **[OBRIGATÓRIA]**

Pronto = DoD (`CON-043`) + travas de `FIN-023`. Excelente = DoE (`CON-047`) nas dimensões do módulo
crítico. Confundir os dois ou atrasa entrega eternamente ou entrega "excelência" teatral.

### FIN-035 — Módulo crítico no perfil sem caminho a DoE não recebe nota 10 **[OBRIGATÓRIA]**

Classificação `crítico` / `padrão` / `periférico` vive no
[perfil do projeto](templates/perfil-do-projeto.md). Crítico aprovado no piso deve ter `OPPORTUNITY`
de DoE com gatilho — senão a excelência nunca entra na fila.

### FIN-036 — Pronto com dívida só com os cinco campos de dívida deliberada **[OBRIGATÓRIA]**

`AUD-037`: quando/por quê · custo de manter · custo de pagar · gatilho · aceito por **nome de
pessoa**. Sem nome, não há dívida: há defeito omitido.

### FIN-037 — A pergunta final do módulo concluído é critério de aceite narrativo **[RECOMENDADA]**

> Se o time sair amanhã, o módulo opera e um novo dev corrige um bug na primeira semana?

Resposta negativa obriga nomear a lacuna no backlog antes de `APPROVED` limpo — alinhado a
`CON-055`.

---

## Capítulo 24.8 — Discordar do orquestrador

### FIN-038 — Veredito do auditor final prevalece na rodada sobre o desejo de fechar do orquestrador **[IMUTÁVEL]**

O orquestrador integra e despacha (`ORC`); não anula evidência. Aceitação de risco residual pertence
a humano nomeado (`CON-042`), não ao orquestrador "para seguir".

### FIN-039 — Discordância cita evidência e regra, não preferência **[OBRIGATÓRIA]**

Formato: achado · `arquivo:linha` ou log · ID da norma · efeito no veredito. Discordância sem
evidência é `AUD-034` invertido (opinião do auditor) e também é inválida.

### FIN-040 — Orquestrador pode pedir reabertura de G1/G2; não pode pedir "aprova assim" **[OBRIGATÓRIA]**

Caminhos legítimos: voltar portão (`CON-064`), decompor escopo, produzir evidência faltante. Caminho
ilegítimo: negociar o significado de `S1`.

### FIN-041 — Empate entre papéis especialistas resolve-se por evidência e `CON-021`, não por média de notas **[OBRIGATÓRIA]**

Média entre "seguro" e "inseguro" é absurdo. O auditor escolhe o lado com prova; o outro vira
`HYPOTHESIS` ou item de backlog.

### FIN-042 — Registro da discordância fica no `AUDIT REPORT` **[OBRIGATÓRIA]**

Seção `Disagreement`: posição do orquestrador · posição do auditor · evidência · decisão · se risco
foi aceito, por quem. Sem registro, a próxima rodada repete o conflito às cegas.

---

## Capítulo 24.9 — Aprovação parcial com dívida nomeada

### FIN-043 — `APPROVED WITH CONDITIONS` só para itens triviais e verificáveis **[OBRIGATÓRIA]**

`AUD-031`. Condição: ação concreta, evidência esperada, responsável, prazo ≤ rodada seguinte.
Condição vaga ("melhorar testes") é inválida — use `CHANGES REQUESTED`.

### FIN-044 — Lista de condições é numerada e fechável sem nova auditoria completa **[OBRIGATÓRIA]**

Exemplo válido: "1. Anexar log de `pnpm test -- billing` nesta PR; 2. Registrar `EOS-…` para S2 de
índice em `invoices.due_at`". Reauditoria aponta só às condições.

### FIN-045 — Dívida que bloqueava DoD não pode ser rebaixada a condição cosmética **[IMUTÁVEL]**

Se era `S1` ou item DoD `PENDENTE` obrigatório, o veredito correto não é parcial elegante: é
`REJECTED` / `CHANGES REQUESTED`.

### FIN-046 — Risco residual declara monitoramento e aceitante humano **[OBRIGATÓRIA]**

Tabela: risco · severidade · como detecta · aceito por. Aceite "o time" é inválido (`AUD-037`).

### FIN-047 — Condições não cumpridas na rodada seguinte viram `S1` de processo **[OBRIGATÓRIA]**

Promessa quebrada corrói o instrumento. Terceira postergação: promover ou `não faremos`
(`AUD-038`) — nunca quarta.

---

## Capítulo 24.10 — Auditoria da auditoria

### FIN-048 — Ao fechar, audite o próprio relatório contra esta lista **[OBRIGATÓRIA]**

| Pergunta | Se não |
| --- | --- |
| Afirmações amostradas com artefato? | Relatório não confiável |
| Escopo batido arquivo a arquivo? | Possível código não revisado |
| Testes alterados inspecionados? | `QAT-008` oculto |
| Backlog contado (n vs n)? | Viola `CON-019` |
| Volumes aplicáveis declarados? | Cobertura teatral |
| Notas com evidência? | Número decorativo |
| Veredito na primeira linha? | Viola `FIN-005` |
| Implementador ≠ auditor? | Portão inválido |

### FIN-049 — Se a amostra anti-teatro falha, o veredito não é "corrigir a amostra" **[OBRIGATÓRIA]**

É `REJECTED` ou reabertura: o processo de evidência da rodada falhou. Corrigir três links e manter
quarenta `OK` não verificados reproduz o defeito.

### FIN-050 — Achado novo fora do escopo: registre para a próxima rodada, não expanda esta **[OBRIGATÓRIA]**

`AUD-034`. Exceção: bloqueante de segurança ou regressão causada pela rodada atual — aí entra no
veredito agora (`FIN-023`).

### FIN-051 — Guarde o artefato do portão onde a próxima pessoa o encontra sem perguntar **[OBRIGATÓRIA]**

Relatório no lugar canônico do repositório (PR de auditoria, `backlog/`, ou pasta acordada no perfil).
Chat não é arquivo (`CON-019`).

### FIN-052 — O critério final remete a `CON-055` **[IMUTÁVEL]**

Se a próxima pessoa não consegue operar e mudar o módulo com segurança sem perguntar a quem auditou,
o portão aprovou cedo demais — nomeie o que falta antes do próximo `APPROVED`.

---

## Padrões reutilizáveis

### Padrão F1 — Cabeçalho de veredito

```
# Veredito: APPROVED | APPROVED WITH CONDITIONS | CHANGES REQUESTED | REJECTED
Rodada: <id> · Auditor: <nome> · Implementadores: <lista> · Conflito de papel: não
```

### Padrão F2 — Amostra anti-teatro

Sorteie 3 IDs de mudança ou 3 itens `OK` do checklist G5. Para cada um, cole comando + saída ou
`path:line`. Se 1 falhar → `FIN-049`.

### Padrão F3 — Matriz de cobertura de volumes

Preencha `FIN-017` antes das notas. Impede nota alta com camada nunca olhada.

### Padrão F4 — Condição fechável

```
COND-1: <ação> · Evidência: <artefato> · Dono: <nome> · Prazo: <data/rodada>
Critério de fechamento: auditor confirma só COND-* sem reabrir G0–G3
```

### Padrão F5 — Discordância mínima

```
## Disagreement
Orquestrador: <posição>
Auditor: <posição>
Evidência: <path:line | log>
Norma: <ID>
Decisão: <prevalece auditor | risco aceito por <humano>>
```

---

## Matrizes de decisão

| Situação | Veredito |
| --- | --- |
| DoD ok, evidências ok, sem S0/S1, backlog batendo | `APPROVED` |
| Só faltam anexos/triviais fecháveis | `APPROVED WITH CONDITIONS` |
| MUST/DoD não trivial aberto | `CHANGES REQUESTED` |
| S0/S1, escopo infiltrado, regressão, teatro de evidência | `REJECTED` |
| Segurança 5 com resto 9 | no máx. `APPROVED WITH CONDITIONS` (`FIN-027`) |
| Sem achados, sem testes, sem OBS | notas ~5; não 9 (`FIN-028`) |
| Orquestrador pede merge com S1 | recusar (`FIN-038`) |
| Amostra anti-teatro falha | `REJECTED` / reabrir (`FIN-049`) |
| DoE incompleta em módulo periférico | `APPROVED` + `OPPORTUNITY` |
| DoE incompleta exigida como se fosse DoD | erro de enquadramento (`FIN-034`) |

---

## Fluxo de trabalho

1. Confirme que você não implementou (`FIN-003`).
2. Execute a ordem de `FIN-013`.
3. Percorra [`modulo-concluido.md`](checklists/modulo-concluido.md) item a item (`CHK`).
4. Aplique amostra anti-teatro (`FIN-006`).
5. Preencha cobertura de volumes (`FIN-017`).
6. Aplique travas (`FIN-023`).
7. Note dimensões com evidência (`FIN-031`).
8. Emita veredito na primeira linha; condições/dívidas se houver.
9. Audite o próprio relatório (`FIN-048`).
10. Publique o artefato fora do chat (`FIN-051`).

Papel: [`agents/10-final-auditor.md`](agents/10-final-auditor.md).

---

## Exemplos de implementação

```
# Ruim — FIN-001, FIN-005
"No geral o módulo está maduro e os testes passam. Sugiro aprovar."

# Bom
# Veredito: REJECTED
## Claim verification
| change-12 | pnpm test -- billing | log CI #8841 não encontrado; autor colou resumo |
| | | failed |
Motivo: validação obrigatória sem artefato (AUD-002, FIN-001).
```

```
# Ruim — FIN-043: condição não fechável
APPROVED WITH CONDITIONS: melhorar a qualidade dos testes e olhar performance depois.

# Bom
APPROVED WITH CONDITIONS
COND-1: Anexar saída de `pnpm test -- invoices` na descrição da PR #412 · Dono: Ana · Prazo: 24h
COND-2: Registrar EOS-014 (p95 listagem sem índice) com gatilho "quando volume > 10k/dia" · Dono: Ana
```

```
# Ruim — FIN-028
Segurança 10 — nenhum achado de segurança nesta rodada.

# Bom
Segurança 6 — DoD de auth no diff ok (authorize por objeto em invoices/*);
DoE incompleta: inventário de PII ausente; S2 no backlog EOS-015.
Sem pentest desta superfície — declarado em cobertura (FIN-017).
```

```
## Disagreement — FIN-042
Orquestrador: aprovar; S2 de log pode esperar.
Auditor: log de pagamento sem correlation id impede o teste das 3h (CON-045); classificado S1 operacional.
Evidência: workers/charge.ts:88 — erro engolido sem request_id.
Decisão: REJECTED até S1 corrigido ou aceito por <nome do dono de risco>.
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Confiar no relatório do implementador | Teatro (`FIN-001`) |
| Começar pelas notas | Número justificado a posteriori (`FIN-013`) |
| Nota 10 por "ninguém reclamou" | Viola `AUD-029` / `FIN-028` |
| Aprovar com S1 "combinado no Slack" | Bloqueante (`FIN-023`) |
| Condição vaga | Falsa parcial (`FIN-043`) |
| Auditor = implementador | Portão inválido (`FIN-003`) |
| Cobertura de volume só no nome | Lacuna silenciosa (`FIN-017`) |
| Corrigir só a amostra anti-teatro | Relatório ainda podre (`FIN-049`) |
| Orquestrador anula veredito | Viola `FIN-038` |
| Aceite de risco "pelo time" | Sem dono (`FIN-046`) |
| Expandir rodada com preferências | Viola `AUD-034` / `FIN-050` |
| Artefato só no chat | Viola `CON-019` / `FIN-051` |

---

## Checklist

- [ ] Veredito na primeira linha. (`FIN-005`)
- [ ] Auditor ≠ implementador. (`FIN-003`)
- [ ] Ordem de leitura respeitada. (`FIN-013`)
- [ ] Tabela de afirmações preenchida; falhas tratadas como falha. (`FIN-007`, `FIN-001`)
- [ ] Amostra anti-teatro (≥3) com artefato. (`FIN-006`)
- [ ] Diff do conjunto vs propostas (escopo). (`FIN-014`, `AUD-022`)
- [ ] Todo teste alterado inspecionado. (`FIN-024`)
- [ ] DoD item a item; sem PENDENTE em APPROVED. (`CON-043`)
- [ ] Cobertura de volumes declarada. (`FIN-017`)
- [ ] Travas S0/S1/escopo/backlog aplicadas. (`FIN-023`)
- [ ] Notas com evidência; 10 só com DoE. (`FIN-028`, `FIN-031`)
- [ ] Backlog: n reportadas = n registradas. (`AUD-035`)
- [ ] Condições fecháveis ou dívida com cinco campos. (`FIN-043`, `FIN-036`)
- [ ] Discordância registrada se houve. (`FIN-042`)
- [ ] Autoauditoria `FIN-048` passada; artefato publicado. (`FIN-051`)

---

## Prompt do volume

```
You are the EOS Final Auditor for Volume 24 (FIN). You did not implement this round.

Load: agents/10-final-auditor.md, agents/_shared/core-contract.md,
agents/_shared/output-schemas.md, 00-constituicao-da-engenharia.md,
12-auditoria.md, 22-checklists.md, 24-auditoria-final.md,
checklists/modulo-concluido.md, and the CHANGE REPORTs / diff for the round.

Sequence (mandatory):
1. Confirm you are not an implementer of this round; if you are, stop (FIN-003).
2. Read the full round diff before partial reports (FIN-014).
3. Verify every validation claim against raw evidence (FIN-007, AUD-002).
4. Draw an anti-theater sample of ≥3 OK claims and reconstruct artifacts (FIN-006).
5. Walk modulo-concluido.md item by item; no section batch-ticks.
6. Inspect every modified test for weakened assertions (FIN-024).
7. Fill applicable-volumes coverage table (FIN-017).
8. Apply hard locks (FIN-023). Score dimensions with evidence (FIN-031).
9. Issue verdict on line 1. Conditions must be closable (FIN-043).
10. Self-check against FIN-048. Publish the report outside chat.

Do not: fix the code; redesign the solution; lower S0/S1 for schedule pressure;
average contradictory specialist opinions; grant score 10 for "no complaints";
negotiate away evidence failures.

Output: AUDIT REPORT schema plus claim verification, coverage table, conditions/debt,
disagreement (if any), residual risk with named acceptor, and DONE|PARTIAL gate status.
```

---

## Critérios de aceite

O portão final só emite `APPROVED` quando:

1. Afirmações obrigatórias verificadas com artefato (`FIN-001`, `FIN-007`).
2. Amostra anti-teatro passou (`FIN-006`).
3. Escopo íntegro; sem S0/S1 abertos (`FIN-023`).
4. DoD completa no escopo (`CON-043`).
5. Backlog batendo e com gatilhos (`AUD-035`, `AUD-036`).
6. Cobertura de volumes aplicáveis honesta (`FIN-017`).
7. Auditor ≠ implementador (`FIN-003`).
8. Artefato publicado (`FIN-051`).

`APPROVED WITH CONDITIONS` exige condições que passam `FIN-043`–`FIN-044`.
Nota 10 em qualquer dimensão exige DoE (`FIN-028`).

---

## Verificação obrigatória de saída

```
# Veredito: APPROVED | APPROVED WITH CONDITIONS | CHANGES REQUESTED | REJECTED
Auditor: <nome> · Implementadores: <lista> · Conflito: <não|sim→abort>

## Claim verification
| Mudança | Validação declarada | Evidência encontrada | Veredito |

## Anti-teatro sample
| Item OK amostrado | Artefato | Passou? |

## Scope integrity
| Arquivo | Proposta | Veredito |

## Test diff review
| Teste | Asserção afrouxada? | Justificado? |

## Volume coverage
| Volume | Aplicável | Aplicado | Evidência | Risco residual |

## Definition of Done
| Mudança | Itens PENDENTE | N/A justificados |

## Scores
| Dimensão | Peso | Nota | Evidência |

## Backlog
Reportadas: <n> | Registradas: <n> | Faltando: <lista>

## Conditions / debt
| ID | Ação | Evidência | Dono | Prazo | Gatilho |

## Disagreement
| Tema | Orquestrador | Auditor | Norma | Decisão |

## Residual risk
| Risco | Severidade | Monitoramento | Aceito por |

## Self-audit (FIN-048)
| Pergunta | OK? |
```
