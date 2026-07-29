# Runbook — Revisão completa de módulo

O pipeline multiagente completo. Use quando um módulo precisa de revisão profunda em várias áreas.

**Não use** para mudança pontual — nesse caso, use
[ciclo de mudança única](ciclo-de-mudanca-unica.md). Rodar onze papéis para corrigir um botão é
desperdício de contexto, e desperdício de contexto degrada o julgamento.

Duração típica: uma sessão longa, ou várias com estado registrado em arquivos.

---

## Etapa 0 — Preparação (humano)

- [ ] O [perfil do projeto](../templates/perfil-do-projeto.md) está preenchido, incluindo os comandos.
- [ ] O módulo alvo está definido, com fronteiras claras.
- [ ] O objetivo está escrito, com critério de sucesso mensurável.
- [ ] Está definido quem aceita risco `R4` e quem aprova ADR.
- [ ] Existe um lugar para o backlog ([`backlog/BACKLOG.md`](../backlog/BACKLOG.md) ou o rastreador).

Sem o perfil, pare aqui. Todo julgamento técnico depende dele.

---

## Etapa 1 — G0 Descoberta (orquestrador)

Papel: [`00-orchestrator`](../agents/00-orchestrator.md) ·
Checklist: [`pre-analise`](../checklists/pre-analise.md)

O orquestrador executa a descoberta **pessoalmente**. Delegar a descoberta significa não ter como
julgar os relatórios que vão chegar.

Saída: mapa do sistema, zonas de risco, estado inicial (testes, tipos, lint), perguntas abertas,
escopo da rodada com camadas incluídas e excluídas.

Proibido nesta etapa: apontar problemas.

---

## Etapa 2 — G1 Diagnóstico (especialistas)

Despacho com o schema `HANDOFF`, uma pergunta específica por papel, e uma lista explícita de fora de
escopo.

### Onda 1 — sequencial, porque a saída de um é entrada do outro

| Ordem | Papel | Pergunta típica |
| --- | --- | --- |
| 1 | [`01-architect`](../agents/01-architect.md) | As fronteiras estão certas e o domínio permite estado inválido? |
| 2 | [`04-database`](../agents/04-database.md) | O schema garante as invariantes por si mesmo? |

Rode nessa ordem: se o modelo de domínio está errado, tudo depois é construído sobre areia. Um `S0`
ou `S1` de modelagem **interrompe** a rodada e volta para decisão.

### Onda 2 — paralela

| Papel | Pergunta típica |
| --- | --- |
| [`02-backend`](../agents/02-backend.md) | As regras são aplicadas em **todos** os caminhos, sob todas as entradas e concorrência? |
| [`05-security`](../agents/05-security.md) | Onde alguém faz algo que não deveria? Comece por autorização por objeto |
| [`03-frontend`](../agents/03-frontend.md) | A interface diz a verdade sobre o estado, inclusive quando falha? |

Segurança é despachada **sempre** que houver autenticação, autorização, dado pessoal, dinheiro ou
upload — independentemente do tamanho da mudança.

### Onda 3 — paralela, depende das anteriores

| Papel | Pergunta típica |
| --- | --- |
| [`06-performance`](../agents/06-performance.md) | Onde está o gargalo **medido**, e ele viola um limiar declarado? |
| [`07-qa`](../agents/07-qa.md) | Os testes existentes pegariam as falhas que importam? |
| [`08-devops-sre`](../agents/08-devops-sre.md) | Quanto tempo até sabermos, e quanto até voltarmos? |
| [`09-product-ux`](../agents/09-product-ux.md) | Os fluxos fazem o que o usuário quer, e são consistentes? |

Performance só é despachado quando há **medição possível**. Sem acesso a medição, o entregável dele é o
plano de medição, declarado como tal — nunca hipótese apresentada como achado (ORC-013).

---

## Etapa 3 — Integração (orquestrador)

- [ ] Deduplicar: o mesmo defeito reportado por três papéis é **um** achado, com a maior severidade e
      a melhor evidência.
- [ ] Rejeitar achados sem evidência — voltam como hipótese.
- [ ] Deflacionar severidade inflada, com motivo escrito.
- [ ] Resolver conflitos entre papéis pela [regra de desempate](../volumes/vol-01-constituicao.md),
      nunca pela média das opiniões.
- [ ] Aplicar a [matriz de priorização](../volumes/vol-01-constituicao.md).
- [ ] Compor a rodada em 70% `MUST-FIX` / 20% risco estrutural / 10% ferramental.
- [ ] Registrar **toda** `OPPORTUNITY` no backlog.

Se `MUST-FIX` excede a capacidade, **esse é o achado principal**: o módulo está em dívida crítica e
precisa de decisão de produto, não de mais revisão.

---

## Etapa 4 — G2 Decisão

Para cada item do escopo, o papel responsável escreve uma
[proposta de mudança](../templates/proposta-de-mudanca.md) com ≥2 alternativas reais mais a opção
zero.

O orquestrador aprova ou rejeita pelos oito critérios do
[portão de aprovação](../agents/00-orchestrator.md#approval-gate). Rejeição vem com **uma** razão
específica; o orquestrador não reescreve a proposta.

- [ ] Itens `R4` param para aprovação humana **antes** da implementação.
- [ ] ADRs escritos onde exigido.
- [ ] Ordem de execução definida: dependências primeiro, risco alto isolado.

---

## Etapa 5 — G3/G4 Implementação e validação

Uma proposta por vez, na ordem definida.

Para cada uma:

1. Implementar, um concern por commit.
2. Validar isoladamente — [pré-merge](../checklists/pre-merge.md).
3. Produzir `CHANGE REPORT` com a saída literal das verificações.
4. **Só então** começar a seguinte.

- [ ] Mudanças de risco `R3`/`R4` entram isoladas.
- [ ] Se uma proposta se revelar inviável durante a implementação, volta para G2 — não improvise uma
      terceira solução no caminho.

---

## Etapa 6 — G5 Auditoria

Papel: [`09-final-auditor`](../agents/10-final-auditor.md) ·
Checklist: [`modulo-concluido`](../checklists/modulo-concluido.md)

O auditor **não** participou da implementação e trata cada afirmação de validação como não verificada
até ver a evidência.

Saída: [relatório de auditoria](../templates/relatorio-de-auditoria.md) com veredito, notas por
dimensão, regressões, integridade de escopo e risco residual com nome de quem aceitou.

- [ ] `REJECTED` → volta para G1 com as regressões como entrada.
- [ ] `APPROVED WITH CONDITIONS` → condições cumpridas e verificadas, sem nova rodada completa.

---

## Etapa 7 — Encerramento

- [ ] Backlog atualizado e conferido: reportadas versus registradas.
- [ ] ADRs em [`backlog/adr/`](../backlog/adr/).
- [ ] Camadas não analisadas registradas como risco conhecido.
- [ ] Notas registradas, para comparar com a próxima rodada.
- [ ] Recomendação do próximo item de maior valor.

---

## Adaptação por tamanho

| Situação | Papéis |
| --- | --- |
| Módulo crítico, revisão completa | Todos os 10 |
| Módulo padrão | Orquestrador, arquiteto, backend, banco, segurança, QA, auditor |
| Área de interface | Orquestrador, frontend, product/UX, QA, auditor |
| Área de dados | Orquestrador, banco, backend, DevOps, auditor |
| Auditoria de segurança | Orquestrador, segurança, backend, banco, auditor |

O auditor final e o orquestrador estão em **todas** as combinações. Sem orquestrador não há
priorização; sem auditor não há verificação independente — e sem verificação independente, o
framework inteiro depende da palavra de quem fez o trabalho.
