# 11 — Processo de revisão

Revisão tem duas falhas simétricas. A falha por omissão aprova o defeito. A falha por excesso
produz cinquenta comentários de estilo que escondem os três defeitos reais e treinam o autor a
ignorar revisões. O EOS trata as duas como falhas de igual gravidade.

---

## Orçamento de mudança

Limites por PR. Existem para manter a revisão possível: acima de ~400 linhas, a capacidade
humana de encontrar defeitos cai drasticamente.

| Tipo de PR | Limite recomendado | Limite absoluto |
| --- | --- | --- |
| Correção de defeito | 100 linhas | 250 |
| Funcionalidade | 300 linhas | 500 |
| Refatoração aprovada | 400 linhas | 800, se puramente mecânica e verificável |
| Migração de schema | 1 migração | 1 migração |
| Risco `R3`/`R4` | Isolado, sem acompanhamento | Isolado |

Não contam para o limite: arquivos gerados, lockfiles, e movimentação de arquivo sem alteração
de conteúdo — desde que estejam em **commit separado**.

Estourar o limite exige declarar o motivo e por que dividir seria pior. "Está tudo relacionado"
raramente é verdade; normalmente significa que o escopo não foi decomposto em G2.

---

## Ordem de revisão

Revise nesta ordem e **pare no primeiro nível que reprova**. Não faz sentido comentar nomes de
variáveis num PR cujo escopo está errado.

1. **Escopo** — o PR faz o que diz e só isso? Se há mudança não relacionada, devolva.
2. **Correção** — resolve o problema por inteiro? Casos de borda? Casos irmãos?
3. **Segurança e dados** — autorização, validação, integridade, migração reversível.
4. **Contratos** — algo público mudou? Está versionado ou é retrocompatível?
5. **Testes** — o teste falharia sem a mudança? Cobre o caminho de erro?
6. **Operação** — dá para diagnosticar e reverter isso em produção?
7. **Clareza** — a próxima pessoa entende sem perguntar?
8. **Convenções** — apenas divergências de `standards/`, nunca preferência pessoal.

---

## Como escrever um comentário de revisão

Todo comentário declara sua força. Sem isso, o autor não sabe o que é obrigatório.

| Prefixo | Significado | Bloqueia? |
| --- | --- | --- |
| `MUST` | Defeito ou violação de norma obrigatória | Sim |
| `SHOULD` | Melhoria relevante; se recusada, exige resposta com motivo | Não |
| `CONSIDER` | Sugestão; o autor decide e não precisa justificar | Não |
| `QUESTION` | Não entendi; pode ser problema meu | Não, mas exige resposta |
| `PRAISE` | Decisão boa que vale explicitar para se repetir | Não |
| `NIT` | Trivial. Máximo de 3 por PR | Não |

Todo `MUST` precisa de três coisas: **onde**, **qual consequência** e **como corrigir**. Um
`MUST` sem consequência nomeada é preferência pessoal disfarçada de autoridade.

| Comentário ruim | Comentário bom |
| --- | --- |
| "Isso deveria ser um service" | `MUST`: esta regra de desconto está no controller e já existe duplicada em `checkout.ts:88`. Se uma mudar sem a outra, o preço divergirá entre carrinho e checkout. Extraia para o módulo de preço e faça os dois pontos chamarem. |
| "Melhore o tratamento de erro" | `MUST`: se `payment.charge` lançar, o pedido fica `pending` para sempre e o usuário não recebe retorno (`orders.ts:142`). Trate a falha marcando `failed` e retornando erro acionável. |
| "Nome ruim" | `NIT`: `d` → `deadlineAt`, para seguir a convenção de sufixo temporal das normas. |

---

## Limites do revisor

- **Máximo de 3 `NIT` por PR.** Acima disso, o ruído domina e o sinal é perdido.
- **Não redesenhe o PR.** Se a abordagem está errada, isso é um único `MUST` de escopo, com a
  discussão voltando a G2 — não vinte comentários de implementação.
- **Não peça mudança sem consequência.** Se você não consegue nomear o que quebra ou o que
  custa, é `CONSIDER` na melhor das hipóteses.
- **Não peça o que não estava lá antes.** Exigir que um PR de correção resolva a dívida
  histórica do arquivo é como PRs morrem. Registre no backlog.
- **Elogie o que quer ver repetido.** É a única forma de a norma se propagar sem policiamento.

---

## Autorrevisão obrigatória

Antes de submeter, o autor (humano ou agente) executa
[`checklists/pre-merge.md`](../checklists/pre-merge.md) e lê o próprio diff **inteiro**, linha
por linha, como se fosse de outra pessoa.

A maior parte dos comentários de revisão é evitável nesta etapa: arquivo tocado sem
necessidade, `console.log` esquecido, mudança de escopo que entrou por descuido, teste que
afirma o comportamento errado.

Regra: **você não pode submeter um diff que não leu por completo.**

---

## Veredito

| Veredito | Quando | Consequência |
| --- | --- | --- |
| `APPROVED` | Nenhum `MUST` | Segue |
| `APPROVED WITH CONDITIONS` | `MUST` triviais e verificáveis, ou `SHOULD` relevantes | Segue após a correção declarada, sem nova rodada completa |
| `CHANGES REQUESTED` | Qualquer `MUST` não trivial | Nova rodada |
| `REJECTED` | Escopo errado, ou abordagem inviável | Volta a G2 |

---

## Resolução de discordância

1. Quem discorda apresenta **evidência**, não opinião: caso de teste, medição, trecho de
   código, norma citada.
2. Se ambos os lados têm evidência, decide-se pela [regra de desempate](01-filosofia-de-engenharia.md#regra-de-desempate).
3. Se o desempate não resolve, o [orquestrador](../agents/00-orchestrator.md) decide.
4. Se envolve aceitação de risco, decide o dono humano — e a aceitação é registrada com nome.
5. Discussão que passa de dois turnos sem informação nova é encerrada por decisão, com ADR se
   houver consequência estrutural.

Nunca resolva discordância por antiguidade, autoridade, ou por citar "best practice" sem
argumento contextual.

---

## Revisão de código gerado por IA

Riscos específicos, verificados explicitamente:

- **Invenção de API:** funções, opções ou pacotes que não existem na versão em uso.
- **Padrão fora de contexto:** solução correta em geral, errada para esta arquitetura.
- **Simetria falsa:** código que parece tratar todos os casos, mas cujos ramos divergem
  sutilmente.
- **Teste tautológico:** teste que afirma exatamente o que a implementação faz, inclusive o
  defeito.
- **Escopo inflado:** melhorias não solicitadas misturadas com a mudança pedida.
- **Confiança na narrativa:** aceitar "validei" sem ver a saída do comando. Exija a evidência.
- **Dependência desnecessária:** pacote adicionado para algo que a biblioteca padrão resolve.
