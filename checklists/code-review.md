# Checklist — Code review

Revise nesta ordem e **pare no primeiro nível que reprova**. Comentar nomes de variáveis num PR cujo
escopo está errado é desperdício e ruído.

Prefixos obrigatórios de comentário: `MUST` · `SHOULD` · `CONSIDER` · `QUESTION` · `PRAISE` · `NIT`
(máximo 3). Ver [processo de revisão](../12-auditoria.md).

---

## Nível 1 — Escopo (reprova cedo)

- [ ] O PR faz o que a descrição diz, e **só** isso.
- [ ] Nenhuma mudança não relacionada entrou de carona.
- [ ] Formatação e comportamento não estão no mesmo commit.
- [ ] Está dentro do orçamento de mudança, ou o excesso está justificado.
- [ ] Nenhuma alteração cosmética sem defeito, métrica ou norma associada.
- [ ] Nenhuma dependência nova sem justificativa.

**Reprovou?** Um único `MUST` de escopo. Não comente o resto.

## Nível 2 — Correção

- [ ] Resolve o problema por inteiro, não só o caso reportado.
- [ ] Casos irmãos no mesmo código foram verificados.
- [ ] Bordas: nulo, vazio, zero, limite, negativo, duplicata, texto longo, caractere especial.
- [ ] Tempo: fuso, virada de dia/mês, ordem invertida de datas.
- [ ] Dinheiro: sem ponto flutuante, arredondamento explícito.
- [ ] Caminhos de erro tratados, com comportamento definido para falha externa.
- [ ] Nenhum estado inválido novo se tornou representável.
- [ ] Concorrência: recurso escasso tem proteção explícita.
- [ ] Nenhum comportamento existente mudou sem intenção declarada.

## Nível 3 — Segurança e dados

- [ ] Autorização verificada **por objeto**, não só por rota.
- [ ] Filtro de tenant presente em toda consulta multi-inquilino.
- [ ] Entrada validada no servidor.
- [ ] Consulta parametrizada; nenhuma concatenação de entrada. (`SEC-019`)
- [ ] SQL dinâmico / sort / filtro DSL sem texto cru; service role valida IDs. (`SEC-067`–`SEC-070`)
- [ ] Nenhum segredo em código, log ou bundle de cliente.
- [ ] Nenhum dado pessoal novo em log.
- [ ] Integridade garantida no banco onde é possível.
- [ ] Migração reversível, com reversa testada.
- [ ] Dado existente verificado contra a nova regra.
- [ ] Nenhuma chamada externa dentro de transação.

## Nível 4 — Contratos

- [ ] Nada público mudou de forma incompatível sem versionamento.
- [ ] Cliente que não controlamos (app móvel) continua funcionando.
- [ ] Código antigo e novo coexistem durante o deploy — nos dois sentidos.
- [ ] Formato em cache e mensagens em trânsito continuam legíveis.

## Nível 5 — Testes

- [ ] O teste novo **falha** sem a mudança (peça a evidência).
- [ ] Bug corrigido tem teste que reproduz o defeito original.
- [ ] Caminho de erro testado.
- [ ] Nenhuma asserção foi afrouxada para acomodar a mudança. **Verifique cada teste alterado.**
- [ ] Nenhum teste desabilitado, `skip` sem ID, ou `retry` novo.
- [ ] Determinístico: sem tempo real, ordem, rede ou estado compartilhado.
- [ ] Testa comportamento, não implementação.

## Nível 6 — Operação

- [ ] Falha nova é registrada com contexto correlacionável.
- [ ] Nenhum erro engolido (`catch` vazio ou que só faz log).
- [ ] Se pode falhar em silêncio, há métrica ou alerta que revelaria.
- [ ] Rollback existe e está declarado.
- [ ] Chamada externa tem timeout; retry só onde é idempotente.

## Nível 7 — Clareza

- [ ] A próxima pessoa entende sem perguntar.
- [ ] Nomes dizem intenção; nome de função revela efeito colateral.
- [ ] Nenhum número ou texto mágico com significado de negócio.
- [ ] Comentário explica o **porquê**, não o quê.
- [ ] `TODO` tem ID de backlog.
- [ ] Nenhum código morto, comentado ou artefato de debug.
- [ ] Mensagem de commit explica o porquê.

## Nível 8 — Convenções

Somente divergências de norma registrada nos [volumes](../RULES-INDEX.md). Preferência pessoal não entra.

- [ ] Nomenclatura conforme a norma.
- [ ] Vocabulário do domínio consistente entre código, banco, API e interface.
- [ ] Nenhum escape do sistema de tipos sem comentário justificando.

---

## Antes de enviar os comentários

- [ ] Todo `MUST` tem: onde, qual consequência, como corrigir.
- [ ] Nenhum `MUST` é preferência pessoal disfarçada.
- [ ] No máximo 3 `NIT`.
- [ ] Não estou pedindo que este PR resolva dívida histórica do arquivo — isso vai ao backlog.
- [ ] Elogiei o que quero ver repetido.
- [ ] O veredito está explícito: `APPROVED` · `APPROVED WITH CONDITIONS` · `CHANGES REQUESTED` ·
      `REJECTED`.

---

## Específico para código gerado por IA

- [ ] API inventada: função, opção ou pacote que não existe na versão em uso.
- [ ] Padrão correto em geral, errado para esta arquitetura.
- [ ] Simetria falsa: ramos que parecem iguais e divergem sutilmente.
- [ ] Teste tautológico, que afirma o que a implementação faz — inclusive o defeito.
- [ ] Escopo inflado com melhorias não solicitadas.
- [ ] "Validei" sem saída de comando. **Exija a evidência.**
- [ ] Dependência nova para algo que a biblioteca padrão resolve.
