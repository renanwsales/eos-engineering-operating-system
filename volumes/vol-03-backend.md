# 📙 Volume 3 — Framework Backend

Prefixo: `BAK` · Regras: BAK-001 a BAK-048 · Papel: [Backend](../agents/02-backend.md)

Camadas cobertas: **2 (domínio)**, **3 (segurança, em conjunto com o Vol 5)**.

Missão do volume: garantir que **o servidor faz a coisa certa sob toda entrada, toda falha e toda execução
concorrente**. Os achados de maior valor aqui não são arquiteturais — são os casos concretos e baratos de
corrigir em que o código simplesmente está errado para uma entrada que ele certamente vai receber.

---

## Capítulo 3.1 — Regras de negócio

### BAK-001 — Enuncie cada regra em linguagem clara **[OBRIGATÓRIA]**

Antes de julgar o código, escreva as regras em escopo em português. **Se você não consegue enunciar uma
regra com clareza a partir do código, isso já é um achado.**

### BAK-002 — Mapeie todos os caminhos que devem aplicar a regra **[OBRIGATÓRIA]**

Para cada regra: API, job em background, admin, importação, webhook, comando de terminal, migração.
Verifique cada um.

> Regra aplicada em um caminho só é o `S1` mais comum em código de backend.

### BAK-003 — Percorra o ponto de entrada ponta a ponta **[OBRIGATÓRIA]**

`entrada → validação → autorização → regra de negócio → persistência → resposta → caminhos de erro`.
Achados aparecem nas transições, não no meio de cada etapa.

### BAK-004 — Falha de negócio previsível não é exceção **[RECOMENDADA]**

Saldo insuficiente, cupom expirado e estoque indisponível são **resultados**, não exceções. Exceção é para
o inesperado. Isso mantém o fluxo de negócio visível no tipo de retorno, em vez de escondido num
`catch` distante.

### BAK-005 — Cálculo é função pura **[RECOMENDADA]**

Preço, imposto, desconto, frete e prazo: mesma entrada, mesma saída, sem efeito. Empurre o efeito para as
bordas. Regra pura é testável sem estrutura complexa — é o que torna a cobertura de negócio viável.

### BAK-006 — Arredondamento é decisão explícita **[OBRIGATÓRIA]**

Onde arredondar, para quantas casas, e em que direção. Arredondar em pontos diferentes do fluxo produz
divergência de centavos impossível de reconciliar. Teste o arredondamento explicitamente.

### BAK-007 — Dinheiro em inteiro ou decimal exato **[OBRIGATÓRIA]**

Ponto flutuante para dinheiro é `S1`, sempre, sem exceção por "funciona hoje".

### BAK-008 — Transições de estado são explícitas e verificadas **[OBRIGATÓRIA]**

Declare as transições válidas. Uma operação sobre recurso em estado final (pedido cancelado, assinatura
encerrada) deve falhar com erro de domínio claro, não seguir adiante.

---

## Capítulo 3.2 — Entrada e validação

### BAK-009 — Validação no servidor, sempre **[OBRIGATÓRIA]**

Validação no cliente é experiência do usuário; validação no servidor é correção. Nenhuma exceção,
inclusive para endpoints "internos".

### BAK-010 — Rejeite campos desconhecidos **[OBRIGATÓRIA]**

Campo ignorado silenciosamente esconde bug de integração por meses — o cliente acredita que enviou algo
que o servidor descartou.

### BAK-011 — Nunca aceite campo privilegiado do cliente **[OBRIGATÓRIA]**

Papel, plano, preço, status, `id` de dono, tenant, permissões: explicitamente ignorados ou rejeitados,
mesmo que a interface não os envie hoje. `S0` se aceito.

### BAK-012 — Validação por lista de permitidos **[OBRIGATÓRIA]**

Lista de proibidos sempre tem um caso a mais. Vale para tipo de arquivo, destino de redirecionamento,
campo de ordenação e valor de enumeração.

### BAK-013 — Limite de tamanho em toda entrada **[OBRIGATÓRIA]**

Corpo da requisição, tamanho de arquivo, comprimento de texto, quantidade de itens em lote. Ausência é
vetor de indisponibilidade trivialmente explorável.

### BAK-014 — Distinga ausência de vazio e de zero **[OBRIGATÓRIA]**

Usar `0`, `""` ou `-1` como sentinela de ausência é `S2`. "Não informado", "vazio" e "zero" são três
estados de negócio diferentes.

### BAK-015 — Tabela de bordas obrigatória **[OBRIGATÓRIA]**

Para cada entrada relevante, verifique e cite a linha que trata — ou reporte a ausência:

| Categoria | Casos |
| --- | --- |
| Ausência | nulo, campo faltando, string vazia, apenas espaços |
| Quantidade | 0, 1, muitos, o limite, o limite + 1 |
| Sinal | negativo onde deve ser rejeitado |
| Texto | muito longo, caractere especial, unicode combinado, emoji, payload de injeção |
| Número | precisão decimal, arredondamento, estouro |
| Tempo | fuso, horário de verão, virada de dia/mês/ano, fim antes do início |
| Duplicidade | requisição repetida, requisição concorrente idêntica |
| Estado | transição inválida, operação em recurso finalizado |
| Autorização | dono, não dono, outro tenant, não autenticado |
| Dependência | fora do ar, lenta, resposta malformada, sucesso parcial |

---

## Capítulo 3.3 — Autenticação e autorização

Aprofundado no [Volume 5](vol-05-seguranca.md). Aqui, o que o backend precisa garantir em cada endpoint.

### BAK-016 — Autorização por objeto, não por rota **[OBRIGATÓRIA]**

Verificar o papel do usuário não basta: verifique se **este** sujeito pode agir sobre **este** recurso.
`GET /pedidos/{id}` que só checa autenticação é `S0`.

### BAK-017 — Negar por omissão **[OBRIGATÓRIA]**

Rota, campo ou operação nova nasce inacessível até que a autorização seja declarada. Lista de exceções
públicas é mais segura do que lista de proteções.

### BAK-018 — Autorização centralizada e obrigatória por construção **[RECOMENDADA]**

Repetir a verificação em cada handler garante que um dia alguém esquecerá. Prefira o mecanismo que falha
fechado quando a declaração falta.

### BAK-019 — Filtro de tenant na camada de dados **[OBRIGATÓRIA]**

Em sistema multi-inquilino, o isolamento é aplicado no ponto mais interno possível — política no banco ou
camada de acesso obrigatória — não na disciplina de cada desenvolvedor. Consulta sem filtro é `S0`.

### BAK-020 — Autorização em lote, exportação e recurso aninhado **[OBRIGATÓRIA]**

Endpoint de lote autoriza **cada** item. Relatório e exportação seguem as mesmas regras da leitura
individual. Em `/pedidos/{a}/itens/{b}`, verifique que `b` pertence a `a`.

### BAK-021 — Reautenticação em operação sensível **[OBRIGATÓRIA]**

Troca de senha, de e-mail, de meio de pagamento e de permissões exige reautenticação.

### BAK-022 — Job herda autoridade explícita **[OBRIGATÓRIA]**

Trabalho em background executado "em nome de" um usuário precisa declarar com que autoridade roda. Job com
privilégio total processando pedido de usuário comum é escalada de privilégio esperando um bug.

---

## Capítulo 3.4 — Tratamento de erros

### BAK-023 — Nunca engula erro **[OBRIGATÓRIA]**

`catch` vazio, ou que apenas registra log e segue, é `S2`. Trate, converta em erro de domínio, ou propague
— deliberadamente.

### BAK-024 — Erro carrega contexto **[OBRIGATÓRIA]**

O que falhou, com qual entrada (sem dado sensível) e o que fazer. `Error: falhou` é inútil no incidente às
3h.

### BAK-025 — Separe erro de usuário de erro de sistema **[OBRIGATÓRIA]**

Usuário recebe mensagem acionável; o sistema registra o detalhe técnico. **Nunca** exponha stack trace,
SQL, caminho de arquivo ou nome de tabela na resposta.

### BAK-026 — Formato único de erro em toda a API **[OBRIGATÓRIA]**

```json
{
  "code": "ESTOQUE_INSUFICIENTE",
  "message": "Restam 2 unidades de SKU-1234.",
  "details": [{ "field": "itens[0].quantidade", "issue": "max", "max": 2 }],
  "traceId": "01HF3..."
}
```

- `code` estável e legível por máquina — clientes não devem interpretar `message`.
- `message` acionável, sem detalhe interno.
- `traceId` correlaciona com o log do servidor. É o que torna o suporte possível.

### BAK-027 — Erro de fornecedor mapeado para erro de domínio **[OBRIGATÓRIA]**

Nunca repasse o erro bruto do terceiro ao cliente: vaza detalhe de implementação e cria acoplamento com o
formato de erro de outra empresa.

### BAK-028 — Mensagem de erro não revela existência **[OBRIGATÓRIA]**

Erro de login não diz se o e-mail está cadastrado. 404 é a resposta correta para "existe, mas você não pode
saber".

---

## Capítulo 3.5 — Contrato de API

### BAK-029 — Contrato declarado é a fonte de verdade **[OBRIGATÓRIA]**

OpenAPI, schema GraphQL ou tipos compartilhados, versionados. Documentação escrita à mão que divirja do
comportamento real é pior do que nenhuma.

### BAK-030 — Mudança incompatível exige versão **[OBRIGATÓRIA]**

| Incompatível | Compatível |
| --- | --- |
| Remover ou renomear campo | Adicionar campo opcional na entrada |
| Tornar campo opcional em obrigatório | Adicionar campo na saída (se os consumidores toleram extras) |
| Mudar tipo ou significado | Adicionar endpoint |
| Restringir valores aceitos | Relaxar validação |
| Mudar código de status ou semântica de erro | — |

Com cliente que você não controla, **não existe** mudança incompatível sem período de convivência.

### BAK-031 — Métodos e status corretos **[OBRIGATÓRIA]**

`GET` nunca altera estado. `PUT` e `DELETE` são idempotentes.

| Status | Uso |
| --- | --- |
| 200 / 201 / 204 | Sucesso com corpo / criado / sem corpo |
| 400 | Entrada malformada |
| 401 | Não autenticado |
| 403 | Autenticado, sem permissão |
| 404 | Não existe — ou existe e você não pode saber |
| 409 | Conflito de estado (versão, duplicata) |
| 422 | Sintaxe válida, regra de negócio violada |
| 429 | Limite de taxa |
| 5xx | Falha nossa. **Nunca** para erro de entrada |

Retornar 200 com `{"erro": ...}` no corpo é violação: quebra todo cliente e todo monitoramento.

### BAK-032 — Coleções são paginadas com limite do servidor **[OBRIGATÓRIA]**

Toda listagem tem paginação com **máximo imposto pelo servidor**. Endpoint que retorna "todos" é um
incidente esperando volume. Prefira cursor a offset quando os dados mudam durante a navegação.

A resposta inclui o mecanismo de continuação desde o início — adicionar paginação depois é mudança
incompatível.

### BAK-033 — Não serialize a entidade inteira **[OBRIGATÓRIA]**

Retorne o necessário para o caso de uso. Serializar a entidade vaza campo interno hoje e, pior, no futuro:
quando alguém adicionar uma coluna sensível, ela aparece na API sem que ninguém perceba.

### BAK-034 — Padrão de nomes consistente **[OBRIGATÓRIA]**

Uma convenção declarada no perfil do projeto, aplicada em toda a superfície. Duas convenções obrigam todo
consumidor a manter um mapa mental de exceções.

### BAK-035 — Limite de taxa em toda API pública **[OBRIGATÓRIA]**

Por sujeito e por endpoint custoso. Ausência é vetor de indisponibilidade.

### BAK-036 — Deprecação anunciada e medida **[OBRIGATÓRIA]**

Marque no contrato, comunique, **meça o uso real**, e remova quando o uso chegar a zero ou o prazo vencer.
Remover porque "parece que ninguém usa" é `S1`.

### BAK-037 — Identificador não sequencial em recurso exposto **[RECOMENDADA]**

Identificador sequencial permite enumerar dados e inferir volume de negócio.

---

## Capítulo 3.6 — Concorrência

Este capítulo encontra bugs reais que quase nunca têm teste.

### BAK-038 — Recurso escasso tem proteção explícita **[OBRIGATÓRIA]**

Para estoque, saldo, assento, cupom de uso único, slug único e cota:

O padrão "leia, verifique, escreva" sem proteção é `S1`. Não é falha teórica: é o que produz estoque
negativo e cupom usado duas vezes, de forma confiável, sob carga.

Proteções válidas: bloqueio pessimista · controle de versão otimista · constraint que faça o segundo
escritor falhar. Declare qual você usou.

### BAK-039 — Escopo de transação pela invariante **[OBRIGATÓRIA]**

Exatamente o conjunto de escritas que precisa ser atômico. Ampla demais gera contenção; estreita demais
gera inconsistência.

### BAK-040 — Nada externo dentro da transação **[OBRIGATÓRIA]**

Nenhuma chamada HTTP, envio de e-mail ou publicação em fila dentro de uma transação: ela fica aberta pela
duração da rede, e o efeito externo não pode ser desfeito pelo rollback.

Padrão correto: persista a intenção na mesma transação, execute o efeito depois.

### BAK-041 — Ordem consistente de bloqueio **[RECOMENDADA]**

Caminhos diferentes que bloqueiam os mesmos recursos em ordens diferentes produzem deadlock intermitente.

### BAK-042 — Idempotência em operação com efeito externo **[OBRIGATÓRIA]**

Cobrança, envio, emissão e provisionamento aceitam chave de idempotência. Rede falha, cliente repete, e
cobrar duas vezes é `S0`.

---

## Capítulo 3.7 — Resiliência

### BAK-043 — Toda chamada externa tem timeout **[OBRIGATÓRIA]**

Sem timeout, uma dependência lenta esgota o pool de conexões e derruba tudo. Ausência é `S2`; em caminho
crítico, `S1`.

### BAK-044 — Retry com espera crescente, limite e idempotência **[OBRIGATÓRIA]**

Retry imediato em massa amplifica a falha da dependência que já está sofrendo. Espera crescente com
variação aleatória, número máximo de tentativas, e apenas em operação idempotente.

### BAK-045 — Comportamento em falha é decidido, não acidental **[OBRIGATÓRIA]**

Para cada dependência: falhar, degradar ou enfileirar. Declare qual. Falha em recurso secundário
(recomendação, avaliação, banner) não deve impedir o fluxo principal.

### BAK-046 — Sucesso parcial é tratado **[OBRIGATÓRIA]**

Se duas de três chamadas funcionaram, qual é o estado do sistema? Sem resposta, o sistema tem estado
inconsistente silencioso.

### BAK-047 — Fila com destino final definido **[OBRIGATÓRIA]**

Número de tentativas, espera entre elas e destino da mensagem que não pode ser processada. Mensagem perdida
em silêncio é perda de dado.

### BAK-048 — Trabalho em volume é processado em lotes e retomável **[RECOMENDADA]**

Com limite de tempo por bloco e possibilidade de retomar. Um processamento único e gigante bloqueia,
estoura memória e, ao falhar, não deixa progresso.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Endpoint que faz tudo conforme um parâmetro `acao` | Impossível autorizar, versionar e monitorar |
| 200 com erro no corpo | Quebra cliente e monitoramento |
| Retornar entidade do banco diretamente | Vaza campo interno no futuro |
| Listagem sem limite | Incidente proporcional ao crescimento |
| "Algo deu errado" genérico | Suporte impossível |
| Verbo na URL (`/criarPedido`) | Perde semântica de método e cache |
| Mudança silenciosa de significado de campo | O pior tipo de quebra: os testes passam |
| Retry sem idempotência | Efeito duplicado |
| Validar só no cliente | Correção depende de quem chama |
| Regra de negócio no controller | Impossível reusar; divergirá do job |

---

## Verificação obrigatória de saída

```
## Regras de negócio em escopo
| Regra (linguagem clara) | Aplicada em | Faltando em | Severidade |

## Matriz de bordas
| Ponto de entrada | Caso | Tratado? | Evidência |

## Concorrência
| Recurso | Padrão atual | Proteção | Severidade |

## Chamadas externas
| Chamada | Timeout | Retry | Idempotente | Comportamento em falha |

## Contrato
| Endpoint | Problema | Incompatível? | Consumidores afetados |
```
