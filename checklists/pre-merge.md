# Checklist — Pré-merge (autorrevisão)

Executado pelo **autor** — humano ou agente — antes de submeter. A maior parte dos comentários de
revisão é evitável aqui.

Regra que governa este checklist: **você não pode submeter um diff que não leu por completo.**

---

## 1. Leia o próprio diff, inteiro

- [ ] Li **cada linha** do diff, como se fosse de outra pessoa.
- [ ] Cada arquivo tocado tem motivo. Nenhum entrou por descuido.
- [ ] Nenhum arquivo gerado, lockfile ou formatação em massa misturado com lógica.
- [ ] Se o lockfile mudou: cada pacote novo tem prova no registry (`SEC-043`); install
      local/CI continua frozen (`SEC-094`); não reabilitei lifecycle scripts.
- [ ] Nenhum `console.log`, `print`, código comentado ou artefato de debug.
- [ ] Nenhum `TODO` sem ID de backlog.
- [ ] Nenhum segredo, token, URL interna ou dado real de pessoa.
- [ ] Nenhum trecho que eu não saiba explicar.

## 2. Escopo

- [ ] O diff corresponde à proposta aprovada. Diferenças estão declaradas.
- [ ] Um concern por commit.
- [ ] Nada de "enquanto eu estava lá".
- [ ] Dentro do orçamento de mudança, ou o excesso está justificado.

## 3. Validação executada — com evidência

Registre a saída literal. "Deve funcionar" não é validação.

- [ ] Verificação estreita: `<comando>` → `<resultado>`
- [ ] Verificação de tipos: `<comando>` → sem erro novo
- [ ] Lint: `<comando>` → sem erro novo, nenhuma regra silenciada
- [ ] Suíte de regressão do escopo: `<comando>` → `<n passaram / n falharam>`
- [ ] Se performance: antes `<n>`, depois `<n>`, mesmo método
- [ ] Se segurança: caminho de exploração demonstrado como fechado
- [ ] O que não pôde ser validado está declarado, com o comando exato para um humano rodar

## 4. Testes

- [ ] Teste novo **falha** sem a mudança — verifiquei.
- [ ] Bug corrigido tem teste de regressão.
- [ ] Nenhuma asserção existente foi afrouxada. Se foi, confirmei que o novo comportamento é o correto
      e expliquei no PR.
- [ ] Nenhum teste desabilitado, `skip` ou `retry` novo.
- [ ] Nada depende de tempo real, ordem, rede ou estado compartilhado.

## 5. Definition of Done

- [ ] Rodei a [Definition of Done](../00-constituicao-da-engenharia.md) item por item.
- [ ] Cada `N/A` tem justificativa.
- [ ] Nenhum item `PENDENTE`. Se há, o status é `PARTIAL`, não `DONE`.

## 6. Contratos e deploy

- [ ] Nada público mudou de forma incompatível sem versionamento.
- [ ] Cliente que não controlo continua funcionando.
- [ ] Código antigo e novo coexistem durante o deploy, nos dois sentidos.
- [ ] Migração: reversa escrita e executada; dado existente verificado.
- [ ] Rollback declarado, com tempo estimado.

## 7. Rastreabilidade

- [ ] Mensagem de commit explica o **porquê**.
- [ ] Achados endereçados referenciados por ID.
- [ ] ADR escrito, se houve mudança de contrato ou decisão custosa de reverter.
- [ ] **Tudo que encontrei e não corrigi está no backlog com ID.**
- [ ] Descrição do PR diz: o que muda, por quê, o que foi validado, qual o risco, como reverter.

## 8. O teste das 3h da manhã

- [ ] Se isto causar um incidente de madrugada, alguém que nunca viu esta mudança consegue entender o
      que ela fez, descobrir que ela é a causa, e revertê-la sem me perguntar nada.

Se a resposta é não, volte ao item correspondente.

---

## Modelo de descrição de PR

```markdown
## O que muda
<uma ou duas frases>

## Por quê
Resolve: [ID do achado]  |  Proposta: [ID]

## Validação
- <comando> → <resultado>
- <suíte> → <n passaram>
- <métrica antes → depois, se aplicável>

## Risco
Faixa: R1|R2|R3|R4  |  Raio: <n arquivos, m módulos>
Contratos públicos: <nenhum|lista>
Migração: <não|sim + reversa testada>

## Rollback
<comando> — <tempo estimado>

## Fora de escopo (registrado no backlog)
[ID] <título>
```
