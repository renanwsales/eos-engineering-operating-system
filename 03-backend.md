# 📙 Volume 3 — Framework Backend

Prefixo: `BAK` · Regras: BAK-001 a BAK-073 · Papel: [Backend](agents/02-backend.md)

Camadas cobertas: **2 (domínio)**, **3 (segurança, em conjunto com o Vol 5)**.

Inclui webhooks, GraphQL e trabalho agendado. Contrato de API e regras de negócio são os capítulos centrais;
os três últimos capítulos aplicam-se conforme a superfície do projeto.

Missão do volume: garantir que **o servidor faz a coisa certa sob toda entrada, toda falha e toda execução
concorrente**. Os achados de maior valor aqui não são arquiteturais — são os casos concretos e baratos de
corrigir em que o código simplesmente está errado para uma entrada que ele certamente vai receber.

**Fronteira.** É deste volume: casos de uso, entidades, repositórios, serviços, DTOs, validação,
erros, autorização aplicada, concorrência, idempotência, transações, filas, workers, trabalho
agendado, webhooks de entrada e saída, GraphQL.
Não é o design do contrato REST/GraphQL como produto público — versionamento, paginação, limite de
taxa, depreciação e documentação vão para [15](15-apis.md). O Volume 3 é o **lado de dentro**; o 15
é o **contrato**. Isolamento de inquilino em profundidade: [16](16-multi-tenant.md).

---

## Fundamentos

Backend correto é o que sobrevive a entrada adversária, falha de fornecedor e duas requisições no
mesmo milissegundo. A missão do volume não é elegância de camadas: é **enunciar a regra, percorrer
cada entrada, e provar o caso de borda** (`BAK-001`–`BAK-003`, `BAK-015`).

Três assimetrias. **Cliente versus servidor:** validação de UI é UX; o atacante fala com a API
(`BAK-009`). **Rota versus objeto:** autorizar o endpoint e esquecer o registro é o vazamento
clássico (`BAK-016`). **Sucesso local versus efeito externo:** sem idempotência e sem timeout, o
retry vira cobrança duplicada ou pool esgotado (`BAK-042`, `BAK-043`).

Contrato publicado e versionamento de API como produto vivem em [15](15-apis.md); aqui o contrato
declarado ainda é fonte de verdade da implementação (`BAK-029`), sem reabrir o volume 15.


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

Aprofundado no [Volume 5](06-seguranca.md). Aqui, o que o backend precisa garantir em cada endpoint.

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

## Capítulo 3.8 — Webhooks

### BAK-049 — Webhook de entrada verifica a origem **[OBRIGATÓRIA]** · `S0`

Assinatura do payload conferida em tempo constante (`SEC-017`), ou autenticação mútua. Endpoint público que
confia no corpo da requisição é uma API de escrita sem autenticação — e normalmente numa área sensível, porque
webhook costuma carregar confirmação de pagamento.

Verifique também o **carimbo de tempo**, para recusar replay de uma requisição legítima capturada.

### BAK-050 — Webhook de entrada é idempotente **[OBRIGATÓRIA]**

Todo provedor reentrega. Processar duas vezes a confirmação de pagamento é `S0`. Guarde o identificador do
evento e descarte repetição.

### BAK-051 — Responda rápido, processe fora do ciclo da requisição **[OBRIGATÓRIA]**

Aceite, persista, enfileire, responda. Processar de forma síncrona faz o provedor expirar e reentregar — o que
multiplica o trabalho exatamente quando ele já está lento.

### BAK-052 — Ordem de chegada não é garantida **[OBRIGATÓRIA]**

Eventos chegam fora de ordem. Use o carimbo do provedor ou o número de sequência para descartar o estado mais
antigo, em vez de aplicar o último que chegou. É a causa do bug em que um pedido cancelado volta a `pago`.

### BAK-053 — Evento desconhecido é ignorado, não é erro **[RECOMENDADA]**

Provedores adicionam tipos de evento. Responder erro para o que você não trata faz o provedor reentregar
indefinidamente e, em alguns casos, desativar o endpoint.

### BAK-054 — Webhook de saída é assinado, com segredo por assinante **[OBRIGATÓRIA]**

O assinante precisa poder verificar que a mensagem é sua. Segredo compartilhado entre todos os assinantes
significa que qualquer um pode falsificar mensagem para outro.

### BAK-055 — URL de destino validada contra faixas internas **[OBRIGATÓRIA]** · `S1`

Webhook de saída com URL configurável pelo cliente é o vetor clássico de SSRF: ele pede que **você** faça a
requisição. Ver `SEC-049`.

### BAK-056 — Reentrega com espera crescente, limite e destino final **[OBRIGATÓRIA]**

E desativação do assinante após falha persistente, com notificação. Sem limite, um assinante morto consome
capacidade indefinidamente.

### BAK-057 — Carga útil mínima, sem dado sensível **[OBRIGATÓRIA]**

Prefira enviar o identificador e deixar o assinante buscar o recurso com a própria autorização. Webhook é
enviado para um endpoint que você não controla, e frequentemente sem TLS verificado do outro lado.

### BAK-058 — Falha de assinante não afeta o fluxo principal **[OBRIGATÓRIA]**

Entrega de webhook é assíncrona e isolada. Se o envio é síncrono no fluxo de checkout, o assinante lento
derruba a sua venda.

### BAK-059 — O assinante tem visibilidade das entregas **[RECOMENDADA]**

Histórico com resultado e possibilidade de reenviar. Sem isso, todo problema de integração vira um pedido de
suporte que você investiga manualmente.

---

## Capítulo 3.9 — GraphQL

Aplicável somente quando a API usa GraphQL. As regras dos capítulos anteriores continuam valendo; estas
tratam do que muda.

### BAK-060 — Resolver não faz uma consulta por item **[OBRIGATÓRIA]**

GraphQL torna o N+1 o comportamento **padrão**: cada campo de cada item resolve isoladamente. Sem carregamento
em lote por requisição, uma consulta de 50 itens com 3 relações faz 151 consultas. `S1` em fluxo principal.

Verifique contando consultas (`PRF-008`), nunca lendo o resolver.

### BAK-061 — Profundidade e complexidade limitadas **[OBRIGATÓRIA]** · `S1`

Sem limite, uma única consulta aninhada é um ataque de indisponibilidade de uma linha. Imponha profundidade
máxima, custo máximo calculado antes de executar, e limite de tempo.

### BAK-062 — Autorização por campo e por objeto, não na raiz **[OBRIGATÓRIA]** · `S0`

O grafo permite alcançar um recurso por caminhos que ninguém previu — por exemplo, o e-mail do dono através de
um pedido público. Autorizar apenas a consulta de entrada é insuficiente por construção.

### BAK-063 — Erro parcial é decisão explícita **[OBRIGATÓRIA]**

GraphQL responde 200 com dados parciais e uma lista de erros. Defina o que o cliente faz nesse caso — e
garanta que o monitoramento conta esses erros, porque por status HTTP eles são invisíveis (`OPS-018`).

### BAK-064 — Introspecção e campos internos controlados em produção **[RECOMENDADA]**

O schema é a documentação completa da sua superfície de ataque.

### BAK-065 — Deprecação de campo é medida antes da remoção **[OBRIGATÓRIA]**

Marque, meça o uso real, remova quando chegar a zero (`BAK-036`).

---

## Capítulo 3.10 — Trabalho agendado e workers

### BAK-066 — Agendamento roda uma vez, não uma vez por instância **[OBRIGATÓRIA]** · `S0` com efeito externo

Ao escalar de uma para três instâncias, todo agendamento em processo passa a executar três vezes. Se o
trabalho cobra, envia ou provisiona, isso é `S0`. Ver `ESC-024`.

### BAK-067 — Todo job é idempotente e retomável **[OBRIGATÓRIA]**

Ele vai ser interrompido no meio — por deploy, por reciclagem de instância, por falha. Job que ao ser
reexecutado duplica efeito, ou que perde todo o progresso, é defeito de projeto.

### BAK-068 — Job declara com que autoridade roda **[OBRIGATÓRIA]**

E qual o escopo de dados que alcança. Job com privilégio total processando pedido de usuário comum é escalada
de privilégio esperando um bug (`BAK-022`).

### BAK-069 — Sobreposição de execução é tratada **[OBRIGATÓRIA]**

Se a execução de hoje ainda roda quando a de amanhã começa, o comportamento precisa estar definido: pular,
enfileirar ou executar em paralelo com segurança. Sem definição, o padrão é corrida.

### BAK-070 — Timeout por execução **[OBRIGATÓRIA]**

Job sem limite de tempo trava recurso indefinidamente e não aparece como falha.

### BAK-071 — Falha de job é visível e alertada **[OBRIGATÓRIA]**

Job que falha em silêncio é a forma mais comum de perda de dado que ninguém percebe por semanas. Registre
início, fim, volume processado e resultado. Alerte para falha e para **ausência de execução** — job que parou
de rodar não emite erro nenhum.

### BAK-072 — Fuso do agendamento é explícito **[OBRIGATÓRIA]**

Agendamento em fuso local muda de hora com horário de verão, e duplica ou pula execução na virada. Agende em
UTC e converta para exibir.

### BAK-073 — Job de volume processa em lotes, com progresso registrado **[RECOMENDADA]**

Ver `BAK-048`. Processamento único e gigante bloqueia, estoura memória e, ao falhar, não deixa progresso.

---

---

## Padrões reutilizáveis

**Tabela de regra → caminhos.** Enuncie a regra em português; liste todo ponto de entrada que deve
aplicá-la (HTTP, job, webhook, GraphQL) (`BAK-001`, `BAK-002`). Lacuna = achado.

**Matriz de bordas por entrada.** Para cada entrada: ausência, limite, tipo, permissão, concorrência
(`BAK-015`). É o artefato que transforma "validamos" em verificação.

**Autorização por objeto no centro.** Filtro de tenant na camada de dados; negar por omissão;
lote/export/aninhado cobertos (`BAK-016`–`BAK-020`). Job declara autoridade (`BAK-022`, `BAK-068`).

**Transação pela invariante.** Escopo mínimo; nada externo dentro; ordem de bloqueio consistente
(`BAK-039`–`BAK-041`). Efeito externo com chave de idempotência (`BAK-042`).

**Webhook: verificar → ACK rápido → processar idempotente.** Assinatura na entrada; resposta fora
do ciclo longo; ordem não garantida (`BAK-049`–`BAK-052`). Saída assinada, URL validada, DLQ
(`BAK-054`–`BAK-056`).

---

## Matrizes de decisão

**Onde a regra deve viver**

| Situação | Lugar | Por quê |
| --- | --- | --- |
| Cálculo determinístico | Função pura (`BAK-005`) | Testável sem infra |
| Transição de estado | Máquina explícita (`BAK-008`) | Impede estado fantasma |
| Autorização | Por objeto, centralizada (`BAK-016`, `BAK-018`) | Rota sozinha vaza |
| Efeito em provedor externo | Fora da transação + idempotência (`BAK-040`, `BAK-042`) | Evita double-charge |
| Trabalho longo / volume | Fila ou job em lotes (`BAK-047`, `BAK-048`) | Não bloqueia request |

**Falha de dependência (`BAK-045`)**

| Papel da dependência | Comportamento |
| --- | --- |
| Crítica para a invariante | Falhar fechado; não mentir sucesso |
| Secundária (recomendação, enrich) | Degradar com comportamento declarado |
| Webhook de assinante | Isolar do fluxo principal (`BAK-058`) |

---

## Fluxo de trabalho

1. Enunciar regras em escopo e mapear caminhos (`BAK-001`, `BAK-002`).
2. Percorrer cada entrada ponta a ponta; preencher matriz de bordas (`BAK-003`, `BAK-015`).
3. Validação no servidor; lista de permitidos; sem campo privilegiado do cliente
   (`BAK-009`–`BAK-012`).
4. Autorização por objeto + tenant; reauth se sensível (`BAK-016`–`BAK-021`).
5. Erros com contexto, formato único, sem revelar existência indevida (`BAK-023`–`BAK-028`).
6. Concorrência e idempotência nos recursos escassos e efeitos externos (`BAK-038`, `BAK-042`).
7. Timeouts, retry e comportamento em falha em toda chamada externa (`BAK-043`–`BAK-045`).
8. Se houver webhook/GraphQL/jobs: capítulos 3.8–3.10 antes de declarar pronto.
9. Contrato: não serializar entidade; paginar; mudança incompatível versionada — e citar
   [15](15-apis.md) para o contrato público (`BAK-029`–`BAK-033`).

Playbooks de endpoint/CRUD em [21](21-playbooks.md) depois dos passos 1–5.

---

## Exemplos de implementação

**Campo privilegiado do cliente (`BAK-011`)**

```ts
// Ruim — BAK-011: cliente define o próprio papel
const user = await createUser({ ...body, role: body.role });

// Bom
const user = await createUser({ ...body, role: "member" });
// elevação só em caso de uso admin autenticado e autorizado por objeto
```

**Autorização só na rota (`BAK-016`)**

```ts
// Ruim — BAK-016: "está autenticado" ≠ "é dono do pedido"
app.get("/pedidos/:id", auth, async (req, res) => {
  res.json(await pedidos.findById(req.params.id));
});

// Bom
app.get("/pedidos/:id", auth, async (req, res) => {
  const pedido = await pedidos.findByIdForUser(req.params.id, req.user.id);
  if (!pedido) return res.status(404).json(erroNotFound()); // BAK-028
  res.json(toPedidoDto(pedido)); // BAK-033
});
```

**Retry sem idempotência (`BAK-042`, `BAK-044`)**

```ts
// Ruim — reentrega do provedor cobra duas vezes
await provedor.cobrar({ pedidoId, valor });

// Bom
await provedor.cobrar({
  pedidoId,
  valor,
  idempotencyKey: `cobranca:${pedidoId}:${tentativa}`,
});
```


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

---

## Checklist

- [ ] Regras enunciadas e caminhos mapeados. (`BAK-001`, `BAK-002`)
- [ ] Matriz de bordas preenchida por entrada. (`BAK-015`)
- [ ] Validação no servidor; campos desconhecidos rejeitados. (`BAK-009`, `BAK-010`)
- [ ] Nenhum campo privilegiado aceito do cliente. (`BAK-011`)
- [ ] Autorização por objeto; negar por omissão; tenant na dados.
      (`BAK-016`, `BAK-017`, `BAK-019`)
- [ ] Lote, export e aninhado autorizados. (`BAK-020`)
- [ ] Erros com contexto; formato único; sem engolir. (`BAK-023`, `BAK-024`,
      `BAK-026`)
- [ ] Dinheiro em tipo exato; arredondamento explícito. (`BAK-006`, `BAK-007`)
- [ ] Transições de estado verificadas. (`BAK-008`)
- [ ] Recurso escasso protegido; idempotência em efeito externo.
      (`BAK-038`, `BAK-042`)
- [ ] Nada externo dentro da transação. (`BAK-040`)
- [ ] Timeout e comportamento em falha em toda chamada externa.
      (`BAK-043`, `BAK-045`)
- [ ] DTO explícito; listagens paginadas com limite. (`BAK-033`, `BAK-032`)
- [ ] Webhook de entrada: origem, idempotência, ACK rápido.
      (`BAK-049`–`BAK-051`) — se aplicável
- [ ] Job: uma vez por cluster, idempotente, autoridade, overlap tratado.
      (`BAK-066`–`BAK-069`) — se aplicável
- [ ] GraphQL: sem N+1 de resolver; auth por campo/objeto.
      (`BAK-060`, `BAK-062`) — se aplicável

---

## Prompt do volume

```
ROLE: Backend engineer under EOS Volume 03 (`BAK`). You own use cases, validation, applied
authorization, concurrency, resilience, webhooks, GraphQL resolvers, and workers.

MISSION
Prove the server does the right thing under every input, every dependency failure, and every
concurrent execution. Highest-value findings are concrete edge cases, not architectural taste.

LOAD
- `AGENTS.md`, `agents/_shared/core-contract.md`, `agents/_shared/output-schemas.md`
- `00-constituicao-da-engenharia.md`, `03-backend.md`, `agents/02-backend.md`
- Cite `15-apis.md` for public contract shape; do not restate API product rules here
- Cite `06-seguranca.md` / `16-multi-tenant.md` by ID for crypto and tenant isolation depth
- Filled project profile

MANDATORY SEQUENCE
1. Write business rules in plain language; map every entry path (`BAK-001`, `BAK-002`).
2. Walk each path end-to-end; fill the edge matrix (`BAK-003`, `BAK-015`).
3. Server-side validation; allow-list; reject privileged client fields (`BAK-009`–`BAK-012`).
4. Object-level authorization + tenant filter (`BAK-016`–`BAK-020`).
5. Errors: never swallow; context; stable format (`BAK-023`–`BAK-026`).
6. Scarce resources, transaction scope, idempotency (`BAK-038`–`BAK-042`).
7. External calls: timeout, bounded retry, declared failure mode (`BAK-043`–`BAK-045`).
8. Apply webhook / GraphQL / job chapters only when that surface exists.

EVIDENCE
Every FINDING cites `path:line` or command output. Separate MUST-FIX from OPPORTUNITY.

NOT YOUR JOB
Public API product decisions (Volume 15). Deep tenant architecture (Volume 16). UX copy
(Volume 08). Inventing business rules under ambiguity — escalate (`CON-053`).

OUTPUT
Use the "Verificação obrigatória de saída" block of `03-backend.md` verbatim.
```

---

## Critérios de aceite

Um módulo backend passa neste volume quando:

1. Toda regra em escopo tem caminhos mapeados e bordas tratadas. (`BAK-002`, `BAK-015`)
2. Validação e autorização estão no servidor por objeto. (`BAK-009`, `BAK-016`)
3. Nenhum campo privilegiado é aceito do cliente. (`BAK-011`)
4. Recursos escassos e efeitos externos têm proteção e idempotência. (`BAK-038`, `BAK-042`)
5. Chamadas externas têm timeout e comportamento de falha declarado. (`BAK-043`, `BAK-045`)
6. Erros não são engolidos; formato único; DTO não vaza entidade. (`BAK-023`, `BAK-026`,
   `BAK-033`)
7. Superfícies presentes (webhook, GraphQL, job) cumprem seus capítulos.
8. Lacunas residuais estão no backlog com gatilho (`CON-019`).

Falha em 2, 3 ou 4 é reprovação: são as classes que viram incidente de dados ou dinheiro.


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
