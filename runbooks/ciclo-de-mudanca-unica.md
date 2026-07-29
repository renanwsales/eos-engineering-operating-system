# Runbook — Ciclo de mudança única

Para o trabalho do dia a dia: um bug, uma funcionalidade pequena, um ajuste pontual. É o caminho
usado em 90% dos casos.

Se a mudança toca três ou mais áreas, use
[revisão completa de módulo](revisao-completa-de-modulo.md) em vez deste.

---

## Passo 1 — Enquadrar (2 minutos, sempre)

- [ ] Li o [perfil do projeto](../templates/perfil-do-projeto.md), especialmente os comandos e as
      armadilhas conhecidas.
- [ ] Declarei qual papel estou adotando.
- [ ] Enunciei o problema como **restrição**, não como solução.
- [ ] Verifiquei o estado inicial: testes, tipos e lint. Sem isso é impossível distinguir o que eu
      quebrei do que já estava quebrado.

Classifique a mudança:

| Tipo | Caminho |
| --- | --- |
| **Trivial** (texto, erro de digitação, config reversível por flag, correção com teste já falhando) | Passo 2 comprimido |
| **Normal** | Todos os passos |
| **Sensível** (auth, autorização, pagamento, dado pessoal, schema, migração) | Todos os passos + faixa de risco `R3`/`R4` |

---

## Passo 2 — Diagnosticar

- [ ] Encontrei a causa, não o sintoma. Tenho `arquivo:linha`.
- [ ] Verifiquei se o defeito tem **irmãos**: o mesmo padrão em outros pontos do código.
- [ ] Verifiquei se a regra é aplicada em **todos** os caminhos: API, job, admin, importação, webhook.
- [ ] Li o histórico do trecho antes de mudá-lo. O código existente tem razões.

**Compressão permitida** para mudanças triviais: um parágrafo, declarando "portões G0–G2 comprimidos
porque `<motivo>`".

Se aparecer qualquer surpresa — o teste falha por outro motivo, o arquivo tem mais dependências do que
parecia — o processo volta ao início. Surpresa é sinal de que o entendimento estava errado.

---

## Passo 3 — Decidir

Para qualquer coisa não trivial:

- [ ] Duas alternativas reais, mais "não fazer nada".
- [ ] Escolhi a mais reversível que resolve o problema **inteiro**.
- [ ] Declarei a troca aceita.
- [ ] Verifiquei a faixa de [risco](../manual/07-matriz-de-risco.md) e a mitigação obrigatória dela.
- [ ] Se `R4`: **parei e pedi aprovação humana** antes de implementar.
- [ ] Se muda contrato público ou é custoso de reverter: escrevi [ADR](../templates/adr.md).

Pergunta de sanidade: eu estou mudando isto porque há um defeito, um risco ou uma métrica — ou porque
eu faria diferente? Se é a segunda, **pare**: é cosmético, e vai ao backlog.

---

## Passo 4 — Implementar

- [ ] Menor mudança reversível que resolve o problema inteiro.
- [ ] Um concern por commit.
- [ ] Nenhum "enquanto eu estava lá". O que eu vi de passagem vai ao backlog, não ao diff.
- [ ] Dentro do orçamento de mudança.
- [ ] Se a abordagem se revelou errada, voltei ao passo 3 em vez de improvisar uma terceira.

---

## Passo 5 — Validar (nunca comprimido)

**Uma mudança não validada não existe.** Registre a saída literal.

- [ ] Teste que **falha** sem a mudança — verifiquei que falha.
- [ ] Verificação estreita: `<comando>` → `<resultado>`
- [ ] Tipos e lint sem erro novo; nenhuma regra silenciada.
- [ ] Regressão do escopo afetado.
- [ ] Se performance: antes e depois, mesmo método.
- [ ] Se segurança: caminho de exploração demonstrado como fechado.
- [ ] O que não pude validar está declarado, com o comando exato para um humano rodar.

---

## Passo 6 — Fechar

- [ ] [Pré-merge](../checklists/pre-merge.md) executado, incluindo ler o próprio diff inteiro.
- [ ] [Definition of Done](../manual/08-definition-of-done.md) item por item, com `N/A` justificados.
- [ ] Mensagem de commit explica o **porquê**.
- [ ] **Tudo que encontrei e não corrigi está no backlog com ID.**
- [ ] Rollback declarado.

---

## O relatório final

```
<O que mudou e por quê, em 1–3 frases>

Validação
- <comando> → <resultado>
- <suíte> → <n passaram>

Risco: R<n> | Raio: <n arquivos> | Rollback: <como>

MUST-FIX restante
<nenhum, ou lista>

OPPORTUNITY registrada
[EOS-NNN] <título> — <severidade>

Não verificado
<o que, e o comando para verificar>
```

---

## Pare e pergunte quando

- A mudança altera contrato público sem ADR que a cubra.
- Toca autenticação, autorização, pagamento ou dado pessoal e o comportamento pretendido é ambíguo.
- Exige exclusão ou migração de dados.
- Você falhou **três** vezes no mesmo problema. Reporte o que estabeleceu, o que descartou, e os dois
  próximos passos mais prováveis.
- A correção correta custa mais de 3× o orçamento de mudança. Proponha como item de backlog em vez de
  fazer em silêncio.
