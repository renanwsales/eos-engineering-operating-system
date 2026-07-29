# 08 — Definition of Done

O mínimo aceitável. Não é o alvo — é o piso abaixo do qual a mudança **não existe**.

Regras de uso:
- Todo item é marcado explicitamente: `OK`, `N/A + justificativa`, ou `PENDENTE`.
- Um único `PENDENTE` significa `PARTIAL`, nunca `DONE`.
- `N/A` sem justificativa é tratado como `PENDENTE`.
- Marcar sem verificar é a falha mais grave possível neste framework, porque corrompe todos os
  relatórios subsequentes.

---

## A. Correção

- [ ] O problema declarado está resolvido **por inteiro**, não apenas no caso reportado.
- [ ] A classe do problema foi considerada: casos irmãos no mesmo código foram verificados e
      tratados ou explicitamente listados.
- [ ] Casos de borda cobertos: nulo/ausente, vazio, zero, valor limite, duplicata, valor
      negativo, string muito longa, caractere especial.
- [ ] Caminhos de erro tratados, com comportamento definido para falha de dependência externa.
- [ ] Nenhum estado inválido novo passou a ser representável.
- [ ] Nenhum comportamento existente mudou sem intenção declarada.

## B. Validação executada

- [ ] Verificação estreita executada (teste ou chamada específica), com o resultado literal
      registrado.
- [ ] Type check sem erro novo.
- [ ] Lint sem erro novo. Nenhuma regra foi silenciada para passar.
- [ ] Suíte de regressão do escopo afetado executada e verde.
- [ ] Se algo não pôde ser validado no ambiente, isso está declarado com o comando exato que
      um humano deve rodar.

## C. Testes

- [ ] Regra de negócio nova ou alterada tem teste que **falha** sem a mudança.
- [ ] Bug corrigido tem teste de regressão que reproduz o defeito original.
- [ ] Nenhum teste novo depende de tempo real, ordem de execução, rede externa ou estado
      compartilhado.
- [ ] Nenhum teste foi desabilitado, marcado como `skip` ou afrouxado para passar.
- [ ] Os testes verificam comportamento observável, não detalhe de implementação.

## D. Segurança

- [ ] Toda entrada nova é validada no servidor.
- [ ] Autorização verificada **por objeto**, não apenas por rota ou papel.
- [ ] Nenhum segredo em código, log, mensagem de erro ou bundle de cliente.
- [ ] Nenhum dado pessoal novo em log.
- [ ] Nenhuma dependência nova com vulnerabilidade conhecida.
- [ ] Se o fluxo é sensível (auth, pagamento, dado pessoal), o caminho de exploração foi
      demonstrado como fechado — não apenas "os testes passam".

## E. Dados

- [ ] Invariantes garantidas no banco quando possível, não só na aplicação.
- [ ] Migração é reversível, e a reversa foi executada em teste.
- [ ] Migração testada contra dados existentes que violariam a nova regra.
- [ ] Consulta nova usa índice; o plano de execução foi verificado quando o volume justifica.
- [ ] Escopo de transação correto para a invariante que protege.

## F. Interface e experiência

- [ ] Estados presentes: carregando, vazio, erro, sucesso, sem permissão.
- [ ] Mensagem de erro diz ao usuário o que fazer, sem expor detalhe técnico.
- [ ] Ação destrutiva tem confirmação ou desfazer.
- [ ] Operável por teclado, com foco visível.
- [ ] Elementos interativos têm rótulo acessível; imagens significativas têm alternativa
      textual.
- [ ] Nada quebra em tela pequena.
- [ ] Nenhum trabalho do usuário é perdido por navegação, erro ou revalidação.

## G. Observabilidade

- [ ] Falha nova é registrada com contexto correlacionável (id de requisição, usuário/tenant,
      operação).
- [ ] Nenhum erro é engolido silenciosamente.
- [ ] Se a mudança pode falhar de forma silenciosa, existe métrica ou alerta que a revelaria.

## H. Rastreabilidade

- [ ] O commit explica **por que**, não o que — o diff já mostra o que.
- [ ] Achados endereçados estão referenciados por ID.
- [ ] Decisão com alternativa não óbvia está registrada (comentário, PR ou ADR).
- [ ] Mudança de contrato público tem ADR.
- [ ] Tudo que foi encontrado e não corrigido está no backlog com ID.

## I. Higiene do diff

- [ ] Um concern por commit.
- [ ] Nenhuma alteração cosmética misturada com alteração de comportamento.
- [ ] Nenhum arquivo tocado sem necessidade (incluindo lockfile e formatação em massa).
- [ ] Nenhum código comentado, `console.log`, `TODO` sem ID de backlog, ou artefato de debug.
- [ ] Nenhuma dependência nova sem justificativa registrada.

---

## Ajuste por severidade

Para correções de `S0` em produção, a DoD pode ser reduzida ao **caminho crítico** — seções A,
B, D e o mínimo de G — para reduzir o tempo de exposição. Nesse caso:

- A redução deve ser declarada no `CHANGE REPORT`.
- Um item de backlog `S1` é criado imediatamente para completar a DoD.
- O prazo desse item é **a rodada seguinte**, não "quando der".

Nenhuma outra situação autoriza reduzir a DoD.

---

## O teste final da DoD

Antes de declarar `DONE`, responda:

> Se esta mudança causar um incidente às 3h da manhã, alguém que nunca a viu consegue
> entender o que ela fez, descobrir que ela é a causa, e revertê-la sem me perguntar nada?

Se a resposta é não, algum item acima está marcado incorretamente.
