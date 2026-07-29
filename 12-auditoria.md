# 📕 Volume 11 — Auditoria Técnica

Prefixo: `AUD` · Regras: AUD-001 a AUD-042 · Papel: [Auditor Final](agents/10-final-auditor.md)

Este volume cobre dois momentos distintos: a **revisão de cada mudança** (code review) e a **auditoria do
conjunto** (portão G5).

---

## Princípio central

### AUD-001 — As duas falhas simétricas da revisão **[IMUTÁVEL]**

A falha por **omissão** aprova o defeito. A falha por **excesso** produz cinquenta comentários de estilo que
escondem os três defeitos reais e treinam o autor a ignorar revisões.

O EOS trata as duas como falhas de igual gravidade. Ruído tem custo: ele faz o leitor parar de ler.

### AUD-002 — Afirmação é tratada como não verificada até haver evidência **[IMUTÁVEL]**

O auditor não confia em relatório. "Os testes passam" sem saída de comando conta como **falha**, não como
pendência. Esta é a regra que sustenta todas as outras garantias do framework.

### AUD-003 — Quem auditou não implementou **[IMUTÁVEL]**

O auditor não participou do trabalho, não corrige o trabalho e não tem interesse em aprová-lo.

---

## Capítulo 11.1 — Orçamento de mudança

### AUD-004 — Limites por PR **[OBRIGATÓRIA]**

Existem para manter a revisão possível: acima de ~400 linhas, a capacidade humana de encontrar defeitos cai
drasticamente.

| Tipo de PR | Recomendado | Absoluto |
| --- | --- | --- |
| Correção de defeito | 100 linhas | 250 |
| Funcionalidade | 300 linhas | 500 |
| Refatoração aprovada | 400 linhas | 800, se puramente mecânica e verificável |
| Migração de schema | 1 migração | 1 migração |
| Risco `R3`/`R4` | Isolado, sem acompanhamento | Isolado |

Não contam: arquivos gerados, lockfiles e movimentação sem alteração de conteúdo — **desde que em commit
separado**.

### AUD-005 — Estourar o limite exige justificativa **[OBRIGATÓRIA]**

"Está tudo relacionado" raramente é verdade; normalmente significa que o escopo não foi decomposto na decisão.

---

## Capítulo 11.2 — Ordem da revisão

### AUD-006 — Pare no primeiro nível que reprova **[OBRIGATÓRIA]**

Não faz sentido comentar nomes de variáveis num PR cujo escopo está errado.

```
1. Escopo       → faz o que diz, e só isso?
2. Correção     → resolve o problema inteiro? bordas? casos irmãos?
3. Seg. e dados → autorização, validação, integridade, migração reversível
4. Contratos    → algo público mudou? versionado ou retrocompatível?
5. Testes       → falharia sem a mudança? cobre o caminho de erro?
6. Operação     → dá para diagnosticar e reverter em produção?
7. Clareza      → a próxima pessoa entende sem perguntar?
8. Convenções   → apenas divergências de norma, nunca preferência
```

### AUD-007 — Escopo errado é um único comentário **[OBRIGATÓRIA]**

Se a abordagem está equivocada, isso é **um** `MUST` de escopo, com a discussão voltando à decisão — não vinte
comentários de implementação.

---

## Capítulo 11.3 — Como comentar

### AUD-008 — Todo comentário declara sua força **[OBRIGATÓRIA]**

| Prefixo | Significado | Bloqueia? |
| --- | --- | --- |
| `MUST` | Defeito ou violação de norma obrigatória | Sim |
| `SHOULD` | Melhoria relevante; recusa exige resposta com motivo | Não |
| `CONSIDER` | Sugestão; o autor decide sem justificar | Não |
| `QUESTION` | Não entendi; pode ser problema meu | Não, mas exige resposta |
| `PRAISE` | Decisão boa que vale explicitar para se repetir | Não |
| `NIT` | Trivial. Máximo de 3 por PR | Não |

Sem prefixo, o autor não sabe o que é obrigatório — e trata tudo como opcional, ou tudo como ordem.

### AUD-009 — Todo `MUST` tem onde, qual consequência e como corrigir **[OBRIGATÓRIA]**

`MUST` sem consequência nomeada é preferência pessoal disfarçada de autoridade.

| Ruim | Bom |
| --- | --- |
| "Isso deveria ser um service" | `MUST`: esta regra de desconto está no controller e já existe duplicada em `checkout.ts:88`. Se uma mudar sem a outra, o preço divergirá entre carrinho e checkout. Extraia para o módulo de preço e faça os dois pontos chamarem. |
| "Melhore o tratamento de erro" | `MUST`: se `payment.charge` lançar, o pedido fica `pending` para sempre e o usuário não recebe retorno (`orders.ts:142`). Marque `failed` e retorne erro acionável. |
| "Nome ruim" | `NIT`: `d` → `deadlineAt`, para seguir a convenção de sufixo temporal. |

### AUD-010 — Máximo de 3 `NIT` por PR **[OBRIGATÓRIA]**

Acima disso, o ruído domina e o sinal é perdido.

### AUD-011 — Não redesenhe o PR **[OBRIGATÓRIA]**
### AUD-012 — Não peça mudança sem consequência **[OBRIGATÓRIA]**

Se você não consegue nomear o que quebra ou o que custa, é `CONSIDER` na melhor das hipóteses.

### AUD-013 — Não exija o que não estava lá antes **[OBRIGATÓRIA]**

Cobrar de um PR de correção a dívida histórica do arquivo é como PRs morrem. Registre no backlog.

### AUD-014 — Elogie o que quer ver repetido **[RECOMENDADA]**

É a única forma de a norma se propagar sem policiamento.

---

## Capítulo 11.4 — Autorrevisão

### AUD-015 — Você não pode submeter um diff que não leu por completo **[IMUTÁVEL]**

Linha por linha, como se fosse de outra pessoa. A maior parte dos comentários de revisão é evitável aqui:
arquivo tocado sem necessidade, `console.log` esquecido, mudança de escopo que entrou por descuido, teste que
afirma o comportamento errado.

### AUD-016 — Rodar a Definition of Done antes de submeter **[OBRIGATÓRIA]**

Ver CON-043 e [checklists/pre-merge.md](checklists/pre-merge.md).

### AUD-017 — Descrição de PR completa **[OBRIGATÓRIA]**

O que muda · por quê · o que foi validado (com saída) · risco e raio · como reverter · o que ficou fora de
escopo, com ID de backlog.

---

## Capítulo 11.5 — Caça a regressões

### AUD-018 — Leia o diff do conjunto, não das partes **[OBRIGATÓRIA]**

Mudanças corretas isoladamente podem ser contraditórias juntas. Só o auditor está posicionado para ver isso.

### AUD-019 — As doze fontes de regressão **[OBRIGATÓRIA]**

| Fonte | Pergunta |
| --- | --- |
| Interação | Duas mudanças corretas sozinhas, contraditórias juntas |
| Código compartilhado | Função alterada para um chamador, usada por cinco |
| Deriva de contrato | Servidor mudou, cliente não (ou o inverso) |
| Janela de deploy | Código antigo e novo coexistindo: ambos funcionam? |
| Dado existente | A regra nova vale para o que já está no banco? |
| Formato em cache | Código novo lê valor cacheado no formato antigo? |
| Mensagem em trânsito | Enfileirada antes da mudança |
| Cliente antigo | App móvel que não atualiza por semanas |
| Mudança silenciosa | Valor padrão, ordem de listagem, arredondamento, fuso, código de erro |
| **Teste afrouxado** | Asserção editada para acomodar a mudança |
| Nova intermitência | Teste que passou a depender de tempo, ordem ou estado |
| Escopo infiltrado | Arquivos que nenhuma proposta aprovada menciona |

### AUD-020 — A inspeção de maior rendimento é o teste alterado **[OBRIGATÓRIA]**

Para **cada** teste modificado: a expectativa mudou porque o comportamento antigo estava errado, ou porque o
novo não casava? O segundo caso é `S1`. Ver QAT-008.

### AUD-021 — Verifique dado existente contra regra nova **[OBRIGATÓRIA]**

Com contagem, não com suposição. Ver DAT-032.

---

## Capítulo 11.6 — Integridade do escopo

### AUD-022 — Cada arquivo do diff corresponde a uma proposta aprovada **[OBRIGATÓRIA]**

### AUD-023 — Escopo não aprovado não é queixa de processo **[IMUTÁVEL]**

> É código **não revisado** entrando sob a cobertura de código revisado.

### AUD-024 — Verifique também as remoções **[OBRIGATÓRIA]**

Código deletado sem justificativa é mudança de comportamento não proposta.

### AUD-025 — Nenhuma dependência nova não prevista **[OBRIGATÓRIA]**
### AUD-026 — Nenhuma formatação em massa dentro de commit de lógica **[OBRIGATÓRIA]**

---

## Capítulo 11.7 — Notas

### AUD-027 — Pesos por dimensão **[OBRIGATÓRIA]**

| Dimensão | Peso |
| --- | --- |
| Segurança | 20% |
| Correção de domínio | 20% |
| Dados e integridade | 15% |
| Testes | 15% |
| Arquitetura | 10% |
| Performance | 8% |
| UX e acessibilidade | 7% |
| Observabilidade e entrega | 5% |

### AUD-028 — Escala **[OBRIGATÓRIA]**

| Nota | Significado |
| --- | --- |
| 10 | Atende a Definition of Excellence na dimensão (CON-047) |
| 8–9 | Atende a DoD com folga; lacunas de DoE conhecidas e registradas |
| 6–7 | Atende a DoD; existem `S2` conhecidos no backlog |
| 4–5 | Parcial; existem `S2` não registrados |
| 1–3 | Existe `S1` |
| 0 | Existe `S0` |

### AUD-029 — Ausência de problemas não é excelência **[IMUTÁVEL]**

Módulo sem achados, sem testes, sem observabilidade e sem decisões registradas **não** tira 9. Tira em torno
de 5, porque **não se sabe se funciona**.

Nota 10 exige DoE, não ausência de reclamação.

### AUD-030 — Travas obrigatórias **[IMUTÁVEL]**

- Qualquer `S0` → total limitado a 4 e veredito `REJECTED`.
- Qualquer `S1` não corrigido → total limitado a 4 e veredito `REJECTED`.
- Nota de segurança < 6 → no máximo `APPROVED WITH CONDITIONS`.
- Qualquer afirmação de validação não verificada → tratada como falha.

---

## Capítulo 11.8 — Veredito

### AUD-031 — Os quatro vereditos **[OBRIGATÓRIA]**

| Veredito | Quando | Consequência |
| --- | --- | --- |
| `APPROVED` | Sem `S0`/`S1`, DoD completa, escopo íntegro, backlog atualizado, afirmações verificadas | Segue |
| `APPROVED WITH CONDITIONS` | Restam apenas itens triviais e verificáveis, listados como condições | Segue após correção declarada, sem nova rodada completa |
| `CHANGES REQUESTED` | Qualquer `MUST` não trivial | Nova rodada |
| `REJECTED` | `S0`, `S1` não corrigido, escopo não aprovado, afirmação não verificada, ou regressão | Volta ao diagnóstico |

### AUD-032 — O veredito vem na primeira linha **[OBRIGATÓRIA]**

Tudo depois dele é justificativa.

### AUD-033 — Rejeição por violação de processo é legítima **[IMUTÁVEL]**

Escopo não aprovado, afirmação não verificada e backlog não atualizado bastam para rejeitar. Não são
burocracia: são os mecanismos que tornam reais todas as outras garantias.

### AUD-034 — O auditor não adiciona achados de preferência própria **[OBRIGATÓRIA]**

Ele verifica contra DoD, DoE e as normas dos volumes. Defeito novo genuíno é registrado como achado para a
**próxima** rodada, não como expansão desta.

---

## Capítulo 11.9 — Backlog

### AUD-035 — Conferência obrigatória: reportadas versus registradas **[OBRIGATÓRIA]**

```
Oportunidades reportadas: <n>
Registradas no backlog:   <n>
Faltando:                 <lista>
```

Diferença diferente de zero bloqueia a aprovação. Ver CON-019.

### AUD-036 — Toda entrada tem gatilho de promoção **[OBRIGATÓRIA]**

O campo mais importante e o mais esquecido: *o que faz este item deixar de esperar?* Sem ele, o item depende
de alguém reler o backlog por acidente.

Exemplos: "qualquer mudança neste arquivo" · "quando o volume passar de 10 mil/dia" · "na próxima auditoria de
segurança" · "se o defeito reincidir".

### AUD-037 — Dívida deliberada tem os cinco campos **[OBRIGATÓRIA]**

Assumida quando e por quê · custo de manter · custo de pagar · gatilho · **aceito por (nome de pessoa, não "o
time")**. Sem eles não é dívida: é defeito não registrado.

### AUD-038 — Regra das três postergações **[OBRIGATÓRIA]**

No terceiro adiamento, promova ou marque `não faremos` com motivo escrito. Nunca postergue uma quarta vez.

### AUD-039 — `não faremos` é estado saudável **[RECOMENDADA]**

Backlog que só cresce perde utilidade: ninguém lê uma lista de 400 itens.

### AUD-040 — Higiene periódica **[OBRIGATÓRIA]**

A cada rodada: verificar obsolescência (evidência que não existe mais) · reavaliar severidade com os
modificadores de contexto · agrupar itens do mesmo módulo · recalcular o score dos 10 do topo.

---

## Capítulo 11.10 — Código gerado por IA

### AUD-041 — Riscos específicos verificados explicitamente **[OBRIGATÓRIA]**

| Risco | Como aparece |
| --- | --- |
| API inventada | Função, opção ou pacote que não existe na versão em uso |
| Padrão fora de contexto | Solução correta em geral, errada para esta arquitetura |
| Simetria falsa | Ramos que parecem tratar todos os casos e divergem sutilmente |
| Teste tautológico | Afirma exatamente o que a implementação faz, inclusive o defeito |
| Escopo inflado | Melhorias não solicitadas misturadas à mudança pedida |
| Confiança na narrativa | Aceitar "validei" sem ver a saída do comando |
| Dependência desnecessária | Pacote para o que a biblioteca padrão resolve |
| Comentário narrativo | Explicação do óbvio, ou justificativa da própria mudança no código |

### AUD-042 — Exija a evidência, não a narrativa **[IMUTÁVEL]**

É a mesma regra do CON-009, e a que mais precisa ser aplicada em revisão de código gerado por IA: o relatório
é convincente por construção. A saída do comando não é.

---

## Verificação obrigatória de saída

Use [templates/relatorio-de-auditoria.md](templates/relatorio-de-auditoria.md).

```
# Veredito: APPROVED | APPROVED WITH CONDITIONS | REJECTED

## Verificação das afirmações
| Mudança | Validação declarada | Evidência encontrada | Veredito |

## Notas
| Dimensão | Peso | Nota | Justificativa |

## Regressões
| ID | O que regrediu | Evidência | Introduzido por | Severidade |

## Integridade do escopo
| Arquivo | Proposta que o aprovou | Veredito |

## Testes alterados
| Teste | Asserção afrouxada? | Justificado? |

## Backlog
Reportadas: <n> | Registradas: <n> | Faltando: <lista>

## Risco residual
| Risco | Severidade | Monitoramento | Aceito por (nome) |
```
