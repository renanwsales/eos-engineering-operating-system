# Proposta de mudança `<ID>` — `<o que muda>`

Obrigatória antes de editar qualquer coisa não trivial. Sem proposta aprovada, a implementação não
começa. Ver [portão G2](../manual/02-processo-de-engenharia.md).

| Campo | Valor |
| --- | --- |
| Resolve | `<IDs dos achados>` |
| Papel proponente | `<architect | backend | frontend | database | security | qa | devops | product>` |
| Faixa de risco | `R1` \| `R2` \| `R3` \| `R4` |
| Esforço | `XS` \| `S` \| `M` \| `L` \| `XL` |
| Status | `proposta` \| `aprovada` \| `rejeitada` \| `implementada` |

---

## 1. Problema como restrição

Uma frase, sem nomear solução.

> `<preencher>`

## 2. Evidência

O achado que força esta mudança. `arquivo:linha` ou saída de comando.

```
<preencher>
```

Consequência se não mudarmos: `<o que quebra, para quem, em que condição>`

## 3. Alternativas

| # | Abordagem | Custo | Risco | Reversibilidade | Retorno |
| --- | --- | --- | --- | --- | --- |
| A | `<preencher>` | | | | |
| B | `<preencher>` | | | | |
| C | Não fazer nada / aceitar o risco | 0 | | total | |

A opção C é obrigatória. Alternativa que existe só para preencher a tabela invalida o processo — se
só há um caminho viável, declare isso e explique por quê.

## 4. Decisão

Escolhida: **`<A | B | C>`**

Troca aceita: `<o que estou pagando em troca do quê>`

Invalidada se: `<a condição que mudaria esta escolha>`

Precisa de ADR? `<não | sim — porquê>`

## 5. Raio de alcance

| Item | Valor |
| --- | --- |
| Arquivos | `<n>` |
| Módulos | `<lista>` |
| Contratos públicos tocados | `<nenhum | lista>` |
| Clientes que não controlamos afetados | `<nenhum | lista>` |
| Migração necessária | `<não | sim — aditiva ou destrutiva>` |
| Dentro do orçamento de mudança | `<sim | não — justificativa>` |

## 6. Riscos que não aparecem no diff

Verificar todos antes de aprovar (ver [matriz de risco](../manual/07-matriz-de-risco.md)):

- [ ] Dado existente viola a regra nova?
- [ ] Cliente antigo continua funcionando?
- [ ] Código antigo e novo coexistem durante o deploy, nos dois sentidos?
- [ ] Valor em cache no formato antigo será lido pelo código novo?
- [ ] Mensagem já enfileirada no formato antigo será processada?
- [ ] Integração externa depende do comportamento exato que muda?
- [ ] Comportamento muda conforme fuso, moeda ou idioma?
- [ ] Funciona no volume de produção, não só no de teste?
- [ ] Migração bloqueia tabela durante a execução?

## 7. Mitigação exigida pela faixa

- [ ] `<itens de R2/R3/R4 conforme a faixa declarada>`
- [ ] Aprovação humana antes da implementação (obrigatório em `R4`)

## 8. Plano de verificação

1. Verificação estreita: `<comando exato>`
2. Regressão: `<escopo e comando>`
3. Métrica, se performance: `<antes → esperado depois, método>`
4. Prova, se segurança: `<caminho de exploração fechado>`

## 9. Rollback

`<como desfazer>` — tempo estimado: `<n>`

Inclui caminho de dados? `<n/a | sim — como>`

## 10. Fora de escopo

O que **não** será feito nesta mudança, e onde foi registrado.

| Item | Severidade | ID de backlog |
| --- | --- | --- |
| `<preencher>` | | |

---

## Decisão do orquestrador

| Campo | Valor |
| --- | --- |
| Veredito | `aprovada` \| `rejeitada` \| `precisa de ajuste` |
| Motivo | `<uma razão específica>` |
| Condições | `<se aprovada com condições>` |
| Data | `<AAAA-MM-DD>` |

Critérios de aprovação (todos obrigatórios):

- [ ] Resolve um achado com evidência
- [ ] Duas alternativas reais comparadas, incluindo não fazer nada
- [ ] Raio dentro do orçamento, ou excesso justificado
- [ ] Plano de verificação concreto e executável
- [ ] Rollback declarado
- [ ] Mitigação da faixa de risco satisfeita
- [ ] `R4` com aprovação humana prévia
- [ ] Não é cosmética
