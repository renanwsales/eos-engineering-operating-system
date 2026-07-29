# Norma — Código e nomenclatura

Esta norma existe para eliminar discussão, não para criar mais. Ela **não** trata de formatação:
formatação é responsabilidade da ferramenta (formatter), configurada uma vez, aplicada
automaticamente, e nunca comentada em revisão.

Convenções de caixa (`camelCase`, `snake_case`, `PascalCase`) seguem o idioma da linguagem e são
definidas no [perfil do projeto](../templates/perfil-do-projeto.md). O que segue vale para
qualquer linguagem.

---

## Nomenclatura

### N1. O nome diz a intenção, não o tipo **[OBRIGATÓRIA]**

| Ruim | Bom | Por quê |
| --- | --- | --- |
| `data`, `info`, `obj`, `item` | `pedidoPendente`, `precoTotal` | Não informa nada |
| `userArray`, `strNome` | `usuarios`, `nome` | O tipo já está no tipo |
| `handleClick2` | `confirmarPagamento` | Numeração revela ausência de conceito |
| `flag`, `temp`, `aux` | `estoqueReservado`, `precoOriginal` | Nomes de rascunho em código definitivo |

### N2. Vocabulário único **[OBRIGATÓRIA]**

Um conceito tem um nome, do banco à interface. Se a entidade é `pedido`, ela não é `order` no
código, `venda` no banco e "compra" na tela. Sinônimo é ambiguidade permanente e a principal
fonte de bug de integração.

Mantenha um glossário no perfil do projeto. Termo novo é decisão, não improviso.

### N3. Sufixos com significado fixo **[RECOMENDADA]**

| Sufixo | Significado |
| --- | --- |
| `...At` | Instante (`criadoAt`, `expiraAt`) |
| `...Count` | Quantidade inteira |
| `...Id` | Identificador de referência |
| `...Cents` / `...Amount` | Valor monetário em unidade inteira |
| `is...` / `has...` / `can...` | Booleano |
| `...Total` | Resultado agregado |

Nunca use um sufixo com significado divergente. `precoAt` é ruído; `pagoCount` não é booleano.

### N4. Booleano afirmativo **[OBRIGATÓRIA]**

`isAtivo`, não `isNaoInativo`. Negação dupla em condicional é fonte real de defeito, não questão
de estilo.

### N5. Funções são verbos; nomes revelam efeito **[OBRIGATÓRIA]**

- `calcularTotal` — puro, retorna valor.
- `salvarPedido` — tem efeito colateral, e o nome diz isso.
- `getUsuario` **não pode** criar, alterar ou enviar nada. Nome que esconde efeito é `S2`.

### N6. Sem abreviação não estabelecida **[RECOMENDADA]**

`quantidade`, não `qtd`. Exceções: abreviações universais do domínio (`id`, `url`, `cpf`, `sku`)
e o índice de laço (`i`).

---

## Estrutura do código

### C1. Uma responsabilidade por unidade **[RECOMENDADA]**

Se você precisa de "e" para descrever o que uma função faz, provavelmente são duas. Isto é um
indicador, não uma regra de tamanho: fatiar função para cumprir número de linhas produz o mesmo
código, mais espalhado — e é explicitamente proibido pelo veto cosmético.

### C2. Retorno antecipado **[RECOMENDADA]**

Trate erro e caso trivial no início; deixe o caminho principal sem aninhamento. Aninhamento acima
de 4 níveis é indicador de investigação.

### C3. Sem número ou texto mágico **[OBRIGATÓRIA]**

Valor com significado de negócio é constante nomeada: `LIMITE_TENTATIVAS_LOGIN = 5`, não `5`
espalhado. Vale para status, códigos de erro e chaves.

### C4. Funções puras onde é possível **[RECOMENDADA]**

Cálculo, transformação e decisão devem ser puros: mesma entrada, mesma saída, sem efeito. Empurre
o efeito para as bordas. Regra pura é testável sem estrutura de teste complexa — é o que torna
cobertura de negócio viável.

### C5. Sem código morto **[OBRIGATÓRIA]**

Código comentado, função nunca chamada, flag que nunca muda, import não usado: remova. O git é o
histórico. Código morto engana o leitor e infla a área de busca durante um incidente.

### C6. Imutabilidade por padrão **[RECOMENDADA]**

Prefira criar novo valor a mutar existente, especialmente em objeto compartilhado ou parâmetro de
função. Mutação de parâmetro é `S2`: é efeito invisível para o chamador.

---

## Tipos

### T1. Sem escape do sistema de tipos **[OBRIGATÓRIA]**

`any`, cast forçado, supressão de erro de tipo e `!` não nulo são proibidos sem comentário que
explique a garantia externa que justifica. Cada escape é uma verificação desligada em silêncio.

### T2. Tipos de domínio, não primitivos **[RECOMENDADA]**

Dinheiro, identificador, e-mail, CPF, quantidade e período merecem tipo próprio. Isso impede a
classe inteira de erros de argumento trocado — `transferir(destino, origem)` deixa de compilar.

**Dinheiro em ponto flutuante é `S1`, sempre.** Use inteiro na menor unidade, ou tipo decimal.

### T3. Ausência explícita **[OBRIGATÓRIA]**

Distinga "não informado", "vazio" e "zero". Usar `0`, `""` ou `-1` como sentinela de ausência é
`S2`.

---

## Erros

### E1. Nunca engula erro **[OBRIGATÓRIA]**

`catch` vazio, ou que apenas registra log e segue, é `S2`. Trate, converta em erro de domínio, ou
propague — decida deliberadamente.

### E2. Erro carrega contexto **[OBRIGATÓRIA]**

Um erro deve dizer o que falhou, com qual entrada (sem dado sensível) e o que fazer. `Error:
falhou` é inútil no incidente às 3h.

### E3. Erro esperado não é exceção **[RECOMENDADA]**

Falha previsível de regra de negócio (saldo insuficiente, cupom expirado) é resultado, não
exceção. Exceção é para o inesperado. Isso mantém o fluxo de negócio visível no tipo de retorno.

### E4. Erro de usuário separado de erro de sistema **[OBRIGATÓRIA]**

Usuário recebe mensagem acionável; o sistema registra o detalhe técnico. Nunca exponha stack
trace, SQL ou caminho interno para o usuário.

---

## Comentários

### K1. Comente o porquê **[OBRIGATÓRIA]**

```
// Ruim: incrementa o contador
contador++

// Bom: o fornecedor cobra em lotes de 100; abaixo disso a chamada é rejeitada
if (itens.length < TAMANHO_MINIMO_LOTE) { ... }
```

Comentário que narra o código é ruído que envelhece e passa a mentir.

### K2. `TODO` com identificador **[OBRIGATÓRIA]**

`// TODO(EOS-042): remover quando a migração de preço concluir`. Sem ID de backlog, o `TODO` é
proibido — é dívida sem registro.

### K3. Documente o não óbvio, o perigoso e o contra-intuitivo **[RECOMENDADA]**

Ordem de operação que importa, restrição externa, workaround de bug de terceiro, e o motivo de
algo *não* ter sido feito da forma esperada. Especialmente o último: é o que evita que alguém
"corrija" para a forma quebrada.

---

## Commits

### G1. Um concern por commit **[OBRIGATÓRIA]**
### G2. A mensagem explica o porquê **[OBRIGATÓRIA]**

```
Ruim:  "fix bug"  |  "ajustes"  |  "atualiza checkout.ts"
Bom:   "impede pedido pago sem valor confirmado

        A transição para `pago` não verificava o retorno do provedor, permitindo
        pedido com total zero quando a cobrança falhava silenciosamente.
        Resolve EOS-031."
```

### G3. Formatação em massa em commit separado **[OBRIGATÓRIA]**

Misturar reformatação com comportamento inutiliza a revisão e o bisect.
