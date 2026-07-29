# 📓 Volume 17 — Observabilidade

Prefixo: `OBS` · Regras: OBS-001 a OBS-070 · Papel: [DevOps/SRE](agents/08-devops-sre.md)

Camada coberta: **8 (entrega)**, no eixo da detecção.

Existe uma classe de sistema que passa em todos os testes, tem cobertura alta, arquitetura defensável, e que
ninguém consegue explicar quando quebra. O incidente acontece, o time abre trinta painéis, todos verdes,
e a resposta chega por reclamação de cliente três horas depois. O código estava correto segundo tudo que
se sabia perguntar. O problema é que o cliente fez uma pergunta que o sistema não sabia responder: *por que
a cobrança do inquilino 4417 falhou às 02h14 e não falhou às 02h15?*

Esse é o erro caro que este volume previne, e ele custa duas coisas ao mesmo tempo. Custa tempo de
indisponibilidade, porque o tempo até entender domina o tempo até corrigir em quase todo incidente real.
E custa dinheiro em silêncio: o time que não consegue responder perguntas compensa gerando volume — mais
log, mais painel, mais alerta — até a conta de telemetria passar a de computação, sem que a capacidade de
responder tenha melhorado. Volume não é observabilidade. É o sintoma de que ela falhou.

O que muda no trabalho de quem lê este volume: instrumentação deixa de ser um passo posterior à
implementação e passa a ser parte do desenho da mudança, derivada de perguntas escritas antes do código.
O entregável não é "temos logs". É "estas nove perguntas têm resposta em menos de dois minutos, e esta é
a consulta que responde cada uma".

**Fronteira.** É deste volume: a diferença entre monitorar e observar e o que ela obriga a instrumentar;
os três sinais e o que cada um responde; log estruturado em profundidade — schema, cardinalidade,
amostragem, custo e vida útil; correlação atravessando processo, fila e trabalho agendado; tracing
distribuído; tipos de métrica, cardinalidade de rótulo e agregação; as métricas mínimas por tipo de
componente; painéis; SLI, SLO e orçamento de erro; alerta acionável e fadiga; depuração em produção;
observabilidade de frontend; custo e retenção de telemetria.

**Não é deste volume:** o núcleo de detecção — log correlacionável (`OPS-013`), log estruturado em campos
(`OPS-014`), níveis com significado (`OPS-015`), as quatro métricas mínimas por serviço (`OPS-018`),
métrica de negócio (`OPS-019`), alerta acionável com runbook e dono (`OPS-023`, `OPS-025`, `OPS-027`) —
mora no [Volume 10](10-devops.md) e é a fundação sobre a qual este volume opera; pipeline, deploy,
rollback e resposta a incidente também (→ [10](10-devops.md)). Medição de gargalo e limiares de
performance (→ [07](07-performance.md)). Contrapressão e capacidade (→ [14](14-escalabilidade.md)).
Métricas de qualidade da engenharia, que medem o time e não o produto (→ [23](23-metricas.md)).
Classificação de achado de dado sensível em telemetria (→ [06](06-seguranca.md)).

---

## Fundamentos

**Monitorar é verificar hipóteses que você já tem. Observar é responder a hipóteses que você não tinha.**
A distinção não é acadêmica: ela decide o que se instrumenta. Monitoramento é um conjunto fechado de
perguntas — "a taxa de erro passou de 2%?", "a fila cresceu?" — e para responder a um conjunto fechado
bastam agregados baratos. Observabilidade é a capacidade de fatiar o comportamento por dimensões que
ninguém escolheu de antemão: por inquilino, por plano, por versão do aplicativo móvel, por método de
pagamento, pela combinação dos quatro. Isso exige que o contexto tenha sido gravado no momento do
evento, porque ele não pode ser reconstruído depois.

Daí sai a assimetria que governa o volume inteiro. **Agregado é barato e responde pouco; contexto por
evento é caro e responde muito.** A engenharia de observabilidade é a alocação desse orçamento: métricas
agregadas para o que precisa ser vigiado continuamente, contexto por evento para o que precisa ser
explicado eventualmente. Errar a alocação nas duas direções é comum. Quem só tem agregados sabe que algo
piorou e nunca por quê. Quem só tem log detalhado paga por linha e não consegue montar um alerta que
dispare em dez segundos.

O terceiro elemento é a **cardinalidade** — o número de valores distintos que um campo pode assumir.
Identificador de pedido tem cardinalidade praticamente infinita; código de status HTTP tem sete valores
úteis. Cardinalidade é grátis em log e em trace, porque o custo lá é por evento armazenado. Em métrica
ela é multiplicativa e destrutiva: cada combinação de rótulos cria uma série temporal própria, e o custo
do sistema de métricas é linear no número de séries. A maior parte dos desastres de custo de telemetria
é uma única linha de código que colocou um identificador num rótulo de métrica.

O quarto é **correlação**. Um sistema SaaS moderno atende uma ação do usuário atravessando um processo
web, uma fila, um worker, um job noturno e dois fornecedores. Sem um identificador que atravesse todas
essas fronteiras, cada peça produz um relato verdadeiro e inútil, e a investigação passa a depender de
comparar carimbos de tempo à mão. A correlação é o que transforma seis relatos em uma narrativa.

O quinto, e o que mais decisão prática governa, é **custo**. Telemetria compete por orçamento com o
produto. Um serviço cuja telemetria custa mais do que a computação que ele consome não é um serviço bem
instrumentado: é um serviço que está pagando para guardar respostas a perguntas que ninguém faz. O corte
correto não é percentual — é por pergunta.

---

## Capítulo 17.1 — Monitorar e observar

### OBS-001 — Observabilidade é a capacidade de responder à pergunta que ninguém previu **[IMUTÁVEL]**

O critério de aceite de um sistema instrumentado não é a existência de log, métrica ou painel. É esta
pergunta, feita sobre um incidente que já aconteceu: **as perguntas surgidas durante o incidente foram
respondidas com o que já estava gravado, ou exigiram um deploy para descobrir?**

Se exigiram deploy, o sistema é monitorado e não é observável, e a consequência é o tempo de
indisponibilidade: cada rodada de "adicionar um log e subir" custa o ciclo completo de deploy, no pior
momento possível. O objetivo declarado é que a próxima investigação não precise de código novo.

### OBS-002 — Toda instrumentação nasce de uma pergunta escrita **[OBRIGATÓRIA]**

Antes de adicionar log, métrica ou span, escreva a pergunta que ele responde e quem a fará. Instrumentação
sem pergunta é a origem de todo o volume inútil: ela parece prudente na hora e produz, em dois anos, um
sistema onde a busca por um erro real retorna quarenta mil linhas irrelevantes.

```
Ruim:  log.info('processando assinatura', { assinatura })
Bom:   pergunta: "quantas renovações falharam por cartão expirado, por plano, nas últimas 24h?"
       → evento assinatura.renovacao.falhou com campos plano, motivo, tentativa
```

A pergunta também é o teste de suficiência: se o campo não aparece em nenhuma pergunta, ele não entra.

### OBS-003 — Contexto de alta cardinalidade é o que separa observar de monitorar **[OBRIGATÓRIA]**

Todo evento relevante grava os identificadores que permitem fatiar depois: inquilino, usuário, assinatura,
pedido, versão do artefato, região, plano, canal de origem. Esses campos não cabem em métrica (`OBS-036`)
e é exatamente por isso que precisam existir em log ou em trace.

A consequência de omiti-los é específica e recorrente: o painel mostra que 0,4% das cobranças falham, e
não existe nenhuma forma de descobrir que 100% delas são de um único inquilino grande, em um único plano,
desde uma única versão. O agregado esconde a estrutura do problema, e a estrutura é a correção.

### OBS-004 — Telemetria nunca está no caminho crítico da requisição **[OBRIGATÓRIA]**

Escrita de log, envio de métrica e exportação de trace são assíncronos, com buffer limitado, e falham
descartando dados — nunca propagando erro nem bloqueando. Coletor indisponível não pode virar
indisponibilidade do produto.

O modo de falha é conhecido: exportador síncrono sem timeout contra um coletor lento adiciona a latência
dele a cada requisição, esgota o pool de conexões e derruba o serviço que ele existia para vigiar. Vale
aqui a mesma exigência de `BAK-043` para qualquer chamada externa, e o descarte é declarado com
contador próprio, para que a perda de telemetria seja visível.

### OBS-005 — Instrumentação entra na mesma mudança, não em uma rodada posterior **[OBRIGATÓRIA]**

O fluxo novo chega instrumentado. Deixar para depois falha de forma previsível: a instrumentação é
priorizada contra funcionalidade e perde, até o primeiro incidente nesse fluxo — que é justamente quando
não há tempo de instrumentar. É a aplicação de `OPS-022` no momento em que ela custa menos, e o revisor
verifica isso no PR (`REV-006`).

---

## Capítulo 17.2 — Os três sinais

### OBS-006 — Cada sinal responde bem a uma pergunta e mal às outras **[OBRIGATÓRIA]**

| Sinal | Responde bem | Responde mal | Custo dominante |
| --- | --- | --- | --- |
| Métrica | Está acontecendo agora? Está pior que ontem? Qual a tendência? | Por que aconteceu com este pedido | Número de séries (cardinalidade) |
| Log | O que aconteceu neste caso concreto, com todo o contexto | Qual a taxa disso ao longo de 90 dias | Volume ingerido e retido |
| Trace | Onde foi o tempo, e em qual salto entre serviços | Frequência agregada; comportamento de baixa amostragem | Volume e taxa de amostragem |

Usar o sinal errado é caro nas duas direções: contar eventos varrendo log é lento e caro sob pressão de
incidente; gravar contexto por pedido em rótulo de métrica destrói o sistema de métricas (`OBS-036`).

### OBS-007 — A ordem de consulta em incidente é métrica, trace, log **[RECOMENDADA]**

Métrica delimita *quando começou e o que está afetado*; trace localiza *onde o tempo ou o erro nasce*;
log explica *o que exatamente aconteceu naquele caso*. Começar pelo log é o erro mais comum, e produz
uma hora de leitura de linhas sem saber ainda se o problema começou às 02h ou às 14h.

### OBS-008 — Os três sinais compartilham um vocabulário de campo único **[OBRIGATÓRIA]**

O mesmo conceito tem o mesmo nome em log, em atributo de span e em rótulo de métrica: `inquilinoId` não
convive com `tenant_id` e `idDoTenant`. É `CON-066` aplicado à telemetria.

Sem isso, a junção entre sinais é manual e falha justamente sob pressão: você tem o trace, tem o log, e
não consegue pular de um para o outro porque o campo que os liga tem nomes diferentes.

---

## Capítulo 17.3 — Log estruturado em profundidade

`OPS-014` estabelece que log é estruturado em campos e `OPS-013` que ele é correlacionável. Este capítulo
trata do que isso exige na prática: qual é o schema, o que nunca entra, quanto custa, e o que fazer com
o log que ninguém leu.

### OBS-009 — O schema de log é declarado e verificado, não emergente **[OBRIGATÓRIA]**

Existe um conjunto de campos obrigatórios em todo registro, escrito em um lugar, e um construtor
compartilhado que os aplica. Campos mínimos, além do contexto de `OPS-013`: carimbo de tempo em UTC com
fuso explícito, nome do serviço, versão do artefato implantado, ambiente, e nome do evento.

A versão do artefato é o campo mais esquecido e o mais valioso: sem ela, não é possível responder "isso
começou com o último deploy?", que é a primeira pergunta de metade dos incidentes.

Schema emergente — cada chamada decide seus campos — produz o resultado previsível de que nenhuma consulta
funciona sobre todo o conjunto, porque cada serviço nomeou o inquilino de um jeito diferente.

### OBS-010 — Nome de evento é fato no passado, de conjunto enumerável **[OBRIGATÓRIA]**

`assinatura.renovacao.falhou`, `pedido.pago`, `nota_fiscal.emitida`. Hierárquico, estável, e listável: é
possível saber quais eventos existem sem varrer o código. É `ARC-018` aplicado ao log.

Nome interpolado (`"falha no inquilino " + id`) não é nome: é texto único por ocorrência, impossível de
agrupar e de contar. A consequência é que a pergunta "com que frequência isso acontece?" deixa de ter
resposta.

### OBS-011 — Uma linha canônica por unidade de trabalho **[RECOMENDADA]**

Ao fim de cada requisição, mensagem consumida ou execução de job, emita um registro único que resume o
trabalho inteiro: rota ou evento, sujeito, resultado, duração, número de consultas, chamadas externas,
bytes de resposta, e as decisões de negócio tomadas.

Essa linha responde sozinha a maior parte das perguntas operacionais, com um registro por unidade em vez
de doze. Ela não substitui o registro de erro em ponto específico (`OPS-017`); substitui a dezena de
registros de progresso que existem para o caso de alguém querer acompanhar.

### OBS-012 — O que nunca entra no log **[OBRIGATÓRIA]**

Além de dado sensível, que é `S0` por `OPS-016` e `SEC-050`:

| Nunca | Motivo |
| --- | --- |
| Corpo inteiro de requisição ou resposta | Custo por linha, e é o vetor mais comum de dado pessoal acidental |
| Mensagem interpolada que repete campos já estruturados | Dobra o custo e não acrescenta consulta possível |
| Pilha de exceção em nível informativo | Ocupa o espaço onde o erro real seria visto |
| Sucesso de leitura em caminho de alto volume | Cresce com o tráfego e nunca é consultado |
| URL completa com parâmetros de consulta | Segredo em parâmetro vaza para o log e para o coletor |
| Conteúdo binário ou codificado em base64 | Custo alto, valor de investigação nulo |

A consequência de violar é dupla e ambas doem: a conta cresce proporcionalmente ao tráfego, e o sinal
real fica sepultado — o time aprende que a busca no log não ajuda, e para de usá-la.

### OBS-013 — Nome e tipo de campo são estáveis para sempre **[OBRIGATÓRIA]**

Um campo que era número passa a ser texto, e todo painel e alerta construído sobre ele silenciosamente
para de casar. O sistema de telemetria não valida tipos, e a falha é silenciosa: a consulta retorna zero
resultados e parece que o problema desapareceu.

Mudança de nome ou de tipo é tratada como mudança incompatível de contrato: campo novo em paralelo,
migração das consultas, remoção depois — o mesmo padrão de `OPS-011`.

### OBS-014 — Amostragem é declarada por classe de evento **[OBRIGATÓRIA]**

Log de alto volume e baixo valor individual pode ser amostrado, com a taxa registrada no próprio evento
para que a contagem seja reconstituível. **Nunca são amostrados:** erro, evento de negócio, evento de
segurança (`SEC-051`) e operação sensível registrada em auditoria (`SEC-011`).

Amostragem não declarada é pior que ausência de log: o investigador conta 400 falhas onde havia 40 mil, e
decide com base num número errado por duas ordens de magnitude.

### OBS-015 — Todo tipo de registro tem consumidor nomeado **[RECOMENDADA]**

Painel, alerta, consulta de investigação recorrente ou obrigação de auditoria. Um tipo de evento cuja
única resposta é "pode ser útil algum dia" tem um consumidor real: a fatura.

Revisão periódica declarada no [perfil do projeto](templates/perfil-do-projeto.md): eventos sem nenhuma
consulta em 90 dias são removidos ou movidos para retenção fria, com item de backlog (`CON-019`). O
argumento de que "um dia alguém pode precisar" já foi testado — o log que ninguém leu em dois anos não
foi lido no incidente seguinte, porque ninguém sabia que ele existia.

### OBS-016 — Volume de log é medido por serviço e por evento, e o crescimento é achado **[OBRIGATÓRIA]**

Existe uma métrica de linhas e bytes emitidos, quebrada por serviço e por nome de evento. Sem ela, a
descoberta de que um serviço decuplicou a emissão acontece na fatura, um mês depois, e a causa já se
perdeu entre trinta deploys.

Crescimento desproporcional ao tráfego é defeito, não uso: quase sempre é um log dentro de laço, um
retry que registra cada tentativa, ou uma exceção esperada tratada como erro.

### OBS-017 — Nível não é controle de custo **[OBRIGATÓRIA]**

Rebaixar `ERROR` para `WARN` ou desligar `INFO` em produção para reduzir a conta não reduz o problema:
esconde. `OPS-015` define o significado de cada nível pela ação que ele exige, e o nível segue esse
significado independentemente do custo.

Quando o custo é o problema real, as alavancas legítimas são reduzir o que se emite (`OBS-012`), amostrar
o que pode ser amostrado (`OBS-014`), e encurtar retenção (`OBS-069`). Todas preservam a semântica do
nível; mexer no nível a destrói, e o próximo incidente é diagnosticado com informação enganosa.

---

## Capítulo 17.4 — Correlação além da requisição

`OPS-013` exige que o log seja correlacionável atravessando serviços, filas e jobs. As regras seguintes
tratam de como isso se sustenta nas fronteiras onde ele normalmente se rompe.

### OBS-018 — A propagação atravessa a fila pelo envelope, nunca pelo corpo **[OBRIGATÓRIA]**

O identificador de correlação viaja em metadado da mensagem, separado da carga útil de domínio. Colocá-lo
no corpo o transforma em campo de contrato: consumidores passam a depender dele, e mudar o formato de
telemetria vira mudança incompatível de contrato de mensagem.

Sem propagação, a cadeia se rompe exatamente no ponto mais difícil de investigar: a ação do usuário
termina com sucesso, o worker falha três minutos depois, e não há nada que ligue os dois relatos.

### OBS-019 — Trabalho agendado abre a própria correlação e a expõe **[OBRIGATÓRIA]**

Todo job registra um identificador de execução, e cada item processado carrega esse identificador mais o
seu próprio. Isso torna respondível a pergunta que aparece toda semana: "esta cobrança foi gerada por
qual execução do job de faturamento, e o que mais aquela execução fez?"

Sem identificador de execução, um job que processou 12 mil assinaturas produz 12 mil registros sem
nenhuma forma de saber quais pertencem à mesma rodada — e quando duas rodadas se sobrepõem (`BAK-069`),
não há como distingui-las.

### OBS-020 — Retentativa preserva a correlação de origem e numera a tentativa **[OBRIGATÓRIA]**

O identificador original acompanha todas as tentativas; um campo separado diz qual tentativa é esta e por
que a anterior falhou. Gerar correlação nova a cada tentativa produz o efeito de contar cinco incidentes
onde houve um, e inflar a taxa de erro por um fator igual ao número de tentativas.

Vale igualmente para reprocessamento manual e para mensagem retirada do destino final (`BAK-047`): o
registro precisa dizer que aquilo é reprocessamento, ou a métrica de negócio conta o mesmo pedido duas
vezes.

### OBS-021 — Chamada a fornecedor registra o identificador dele **[OBRIGATÓRIA]**

Toda chamada externa grava o identificador de requisição devolvido pelo fornecedor, junto do seu próprio.
É o único elemento que torna possível abrir um caso de suporte com evidência, em vez de descrever o
problema em prosa e aguardar.

A consequência de omitir aparece no pior cenário: a operadora de pagamento afirma que não recebeu a
requisição, você afirma que enviou, e nenhum dos dois tem o identificador que resolveria a disputa em
trinta segundos.

### OBS-022 — Falha de sistema devolve ao usuário um identificador de suporte **[RECOMENDADA]**

Erro de sistema — nunca erro de validação — apresenta um identificador curto que localiza a requisição na
telemetria. Sem detalhe técnico na interface (`UXI-017`) e sem revelar estrutura interna.

Isso transforma "não funcionou ontem à tarde" em uma busca de um segundo, e é o que faz o suporte deixar
de pedir print de tela.

---

## Capítulo 17.5 — Tracing distribuído

### OBS-023 — Span é unidade de trabalho com início, fim e resultado declarado **[OBRIGATÓRIA]**

Um span cobre um trabalho que pode falhar ou demorar: a requisição HTTP, a consulta ao banco, a chamada
ao fornecedor, o consumo de uma mensagem, uma etapa de cálculo custosa. Ele declara o resultado — sucesso
ou erro — e não apenas a duração.

Span sem resultado produz o trace que mostra onde o tempo foi e não mostra onde a falha nasceu, o que
resolve metade do problema e é frequentemente a metade menos urgente.

### OBS-024 — Atributo de span carrega o que muda a interpretação da duração **[OBRIGATÓRIA]**

Uma consulta de 900 ms é defeito ou normal dependendo de quantas linhas ela retornou, de qual inquilino
é, e se o cache foi usado. Sem esses atributos, o trace informa o número e nega o significado.

Atributos úteis por natureza de span: tamanho do conjunto de resultados, tamanho do lote, se houve acerto
de cache, qual índice, qual versão de contrato, qual inquilino. Atributos inúteis: os que repetem
informação já presente no nome do span.

### OBS-025 — Erro é marcado no span, não descrito em texto **[OBRIGATÓRIA]**

O span erro usa o mecanismo de estado de erro do formato, com o tipo do erro em campo próprio. Descrever
a falha apenas em mensagem livre impede filtrar traces com erro, que é a consulta mais usada em
investigação de latência: os casos lentos e os casos com erro são populações diferentes e precisam ser
separáveis.

### OBS-026 — Amostragem de trace preserva o anômalo **[OBRIGATÓRIA]**

Amostragem uniforme baixa descarta exatamente o que interessa, porque o caso patológico é raro por
definição. A política mínima aceitável: manter 100% dos traces com erro e dos que excedem o limiar de
latência declarado (`PRF-038`), amostrar o restante.

Com amostragem uniforme de 1%, um erro que atinge um em cada mil pedidos tem chance de dez por cento de
aparecer em um único trace por dia. A investigação vira espera.

### OBS-027 — Tracing paga onde há fronteira e é caro onde não há **[RECOMENDADA]**

| Situação | Tracing distribuído | Alternativa mais barata |
| --- | --- | --- |
| Requisição atravessa três serviços ou mais | Paga; é a única forma de localizar o salto lento | — |
| Monólito com um banco e dois fornecedores | Raramente paga | Linha canônica com duração por etapa (`OBS-011`) |
| Fluxo assíncrono com fila e worker | Paga, se a propagação existir (`OBS-018`) | Correlação em log, se o fluxo tem duas etapas |
| Trabalho em lote noturno | Não paga; a granularidade é a execução | Métrica de duração e progresso do job |
| Depurar latência de função interna | Não paga | Perfilamento (`PRF-005`) |

Adotar tracing em monólito de duas dependências produz custo de instrumentação, custo de ingestão e uma
resposta que a linha canônica já dava. Recusar tracing em arquitetura de cinco serviços produz o
incidente em que cada equipe prova que o problema é da outra.

### OBS-028 — Instrumentação manual só na fronteira que a automática não vê **[RECOMENDADA]**

Bibliotecas de instrumentação automática cobrem HTTP, banco e fila. O span escrito à mão existe para a
fronteira de **domínio**: cálculo de imposto, aplicação de regra de preço, decisão de aprovação de
crédito. Envolver cada função em span produz trace com trezentos nós, no qual nada se acha, e um custo de
ingestão proporcional ao ruído.

### OBS-029 — Trace não é fonte de alerta **[OBRIGATÓRIA]**

Alerta se constrói sobre métrica, que é completa e agregada. Trace é amostrado por construção
(`OBS-026`), e alertar sobre dado amostrado produz disparo dependente de sorte estatística: o mesmo
problema alerta hoje e não alerta amanhã, o que treina o time a desconfiar do alerta.

O caminho correto é derivar métrica a partir de spans no coletor, com contagem completa antes da
amostragem, e alertar sobre a métrica.

---

## Capítulo 17.6 — Métricas

### OBS-030 — O tipo da métrica sai da pergunta **[OBRIGATÓRIA]**

| Tipo | O que é | Pergunta que responde | Erro comum |
| --- | --- | --- | --- |
| Contador | Valor que só cresce | Quantas vezes, e a que taxa | Usar para valor que pode diminuir |
| Medidor | Valor instantâneo | Quanto há agora | Usar onde a taxa importa; o pico entre coletas é perdido |
| Histograma | Distribuição em faixas | Qual a distribuição, e o percentil | Usar medidor de latência e perder a distribuição |

Escolher o tipo errado não degrada a métrica: invalida a pergunta. Latência em medidor responde "qual foi
a última latência", que não interessa a ninguém.

### OBS-031 — Contador é monotônico, e a consulta é sobre a taxa **[OBRIGATÓRIA]**

O contador nunca é zerado pela aplicação; a reinicialização do processo é tratada pelo sistema de
métricas. Zerar à meia-noite, ou por decisão da aplicação, quebra o cálculo de taxa e produz picos
artificiais que disparam alerta.

### OBS-032 — Latência e tamanho são histograma, com faixas escolhidas **[OBRIGATÓRIA]**

As faixas são definidas em torno do limiar que interessa: se o objetivo é 300 ms (`PRF-038`), há faixas
em 200, 300 e 500 ms. Faixas padrão da biblioteca costumam ser logarítmicas e largas, e produzem um p95
com margem de erro maior do que a diferença que se quer detectar.

Consequência concreta: com faixas em 100 ms e 1 s, um p95 que subiu de 320 ms para 780 ms aparece como
"entre 100 ms e 1 s" nas duas medições. A regressão é invisível.

### OBS-033 — Percentil não se agrega por média **[OBRIGATÓRIA]**

A média dos p95 de dez instâncias não é o p95 do conjunto, e o erro não é pequeno: ele apaga a instância
patológica, que é a que está causando o problema. Percentil sobre o conjunto se calcula a partir das
faixas do histograma somadas, nunca a partir dos percentis já calculados.

Vale também no tempo: o p95 da hora não é a média dos p95 dos minutos. É a extensão de `PRF-003` ao lado
da agregação — usar média onde se precisa de percentil, e usar percentil de percentil, são o mesmo erro
com duas caras.

### OBS-034 — Cardinalidade de rótulo é orçada por métrica **[OBRIGATÓRIA]**

Antes de adicionar um rótulo, multiplique: o número de séries é o produto das cardinalidades de todos os
rótulos. Rota (40) × status (8) × método (5) × versão de artefato (30 em uma semana) são 48 mil séries
para uma única métrica.

Cada série custa memória no processo, custo de ingestão e custo de consulta. A explosão não degrada
graciosamente: o sistema de métricas atinge o limite e passa a descartar séries — inclusive as que
sustentam alertas — no momento de maior tráfego, que é quando a cardinalidade é maior.

### OBS-035 — Nenhum identificador de entidade como rótulo de métrica **[OBRIGATÓRIA]**

Identificador de pedido, de usuário, de sessão, de requisição, mensagem de erro livre, URL com parâmetro,
endereço de rede. Todos têm cardinalidade ilimitada e todos aparecem regularmente em código de produção.

Inquilino é o caso de fronteira e a resposta depende do número: com 50 inquilinos, rótulo de inquilino é
legítimo e valioso; com 50 mil, é a mesma falha com outro nome. A regra prática é rotular por **classe**
— plano, região, faixa de tamanho — e deixar o identificador para log e trace (`OBS-003`).

### OBS-036 — Nome, unidade e sufixo seguem convenção declarada **[RECOMENDADA]**

Unidade no nome, sempre em unidade base: `cobranca_duracao_segundos`, `resposta_bytes`,
`fila_mensagens_total`. Métrica sem unidade explícita produz o painel em que ninguém sabe se o eixo está
em milissegundos ou segundos, e a decisão de escala é tomada com fator mil de erro.

### OBS-037 — Erro é contado por classe, com o total derivável **[OBRIGATÓRIA]**

Um contador de erros com rótulo de classe — `expirado`, `saldo_insuficiente`, `fornecedor_indisponivel`,
`timeout` — em vez de um contador por tipo de erro ou de um contador único. A classe é enumerável e vem
do domínio (`BAK-025`).

Sem classificação, a taxa de erro sobe e não se sabe se é o fornecedor caindo ou o cliente digitando
cartão vencido. As duas exigem ações opostas: a primeira é incidente, a segunda é produto.

### OBS-038 — Métrica nova declara o painel ou o alerta que a consome **[OBRIGATÓRIA]**

É `CON-050` no plano da telemetria: métrica sem reação declarada é decoração com custo recorrente.
Métrica emitida e nunca consultada é a forma mais silenciosa de desperdício, porque nada falha e a conta
sobe mês a mês.

---

## Capítulo 17.7 — As métricas mínimas por tipo de componente

`OPS-018` estabelece as quatro por serviço — taxa, erro, latência, saturação — e `OPS-019` exige métrica
de negócio. Este capítulo diz o que **cada tipo de componente** exige além disso, porque as quatro são
suficientes para uma API e insuficientes para tudo o mais.

### OBS-039 — Cada tipo de componente tem um conjunto mínimo próprio **[OBRIGATÓRIA]**

| Componente | Além das quatro de `OPS-018` |
| --- | --- |
| API | Taxa por rota, status e versão de contrato; tamanho de resposta; uso de cota por cliente |
| Worker de fila | Idade da mensagem mais antiga; profundidade; taxa de reentrega; profundidade do destino final |
| Job agendado | Carimbo da última conclusão com sucesso; duração; registros processados; execuções sobrepostas |
| Banco | Conexões em uso e em espera; tempo de espera por bloqueio; consultas acima do limiar; atraso de réplica |
| Integração externa | Latência e taxa de erro medidas por você; taxa de timeout; consumo de cota do fornecedor |
| Frontend | Erros de cliente por versão de artefato; métricas de usuário real; falha de requisição por rota |

Ausência de um item deste conjunto no componente correspondente é achado, com a severidade saindo da
consequência (`CON-036`): banco sem métrica de espera por bloqueio significa que contenção se manifesta
como "está lento" sem nenhuma pista.

### OBS-040 — Em fila, a idade da mensagem mais antiga é a métrica que revela atraso **[OBRIGATÓRIA]**

Profundidade de fila engana: mil mensagens processadas em dez segundos é saudável, e dez mensagens
paradas há duas horas é incidente. A profundidade não distingue os dois casos; a idade da mensagem mais
antiga distingue, e é ela que se alerta.

O modo de falha que só a idade revela: consumidor vivo, processando normalmente as mensagens novas, com
um punhado de mensagens envenenadas em retentativa infinita no fundo da fila. Todos os painéis verdes,
e um cliente esperando desde ontem. Ver `ESC-030` para o limite da fila.

### OBS-041 — Em job, a última conclusão com sucesso é a métrica que revela ausência **[OBRIGATÓRIA]**

Métrica de falha só existe quando o job executa. O modo de falha mais comum de trabalho agendado não é
falhar: é **não rodar** — agendador reconfigurado, container que não subiu, fuso alterado (`BAK-072`).
Nesse caso, a taxa de erro é zero e tudo parece bem.

O que se alerta é o tempo desde a última conclusão com sucesso, contra o intervalo esperado mais uma
folga. `BAK-071` exige que a falha seja visível; esta regra cobre a ausência, que é o caso que a falha
não cobre.

### OBS-042 — Em integração externa, quem mede é você **[OBRIGATÓRIA]**

Latência e disponibilidade do fornecedor são medidas do seu lado, na sua borda, incluindo rede, DNS e
tempo de fila do seu pool. A página de status do fornecedor mede o data center dele e é atualizada por
humanos, com atraso.

A consequência de confiar no painel alheio: o fornecedor está "operacional", suas chamadas levam oito
segundos, e a discussão interna gira em torno de quem está errado em vez de acionar o comportamento
degradado (`SEL-032`).

### OBS-043 — Em banco, meça contenção e atraso, não só latência de consulta **[OBRIGATÓRIA]**

Conexões em espera, tempo de espera por bloqueio, transações longas abertas e atraso de replicação
(`ESC-013`). Sob concorrência, o tempo de resposta cresce sem que nenhuma consulta individual fique
lenta — o tempo está na fila, não na execução, e a métrica de latência de consulta não o vê.

### OBS-044 — Destino final de mensagens tem contagem alertada em zero **[OBRIGATÓRIA]**

`BAK-047` exige que a fila tenha destino final. Aqui o requisito é que a chegada de qualquer mensagem
nele dispare alerta com dono. Destino final que acumula sem alerta é uma pasta de perdidos: os pedidos
estão lá, tecnicamente não foram perdidos, e ninguém sabe que estão esperando.

---

## Capítulo 17.8 — Painéis

### OBS-045 — Painel responde a uma pergunta declarada no próprio título **[OBRIGATÓRIA]**

"Saúde do checkout: estamos aceitando pagamentos na taxa esperada?" é um painel. "Métricas do serviço de
pagamento" é uma galeria de gráficos.

O teste é operacional e barato: entregue o painel a alguém que não o construiu e peça a resposta. Se essa
pessoa precisa interpretar oito gráficos para formar uma opinião, o painel não responde — ele exibe. É a
extensão de `OPS-021`, que exige um painel capaz de responder "está tudo bem?" em dez segundos; esta
regra estende o critério a todos os outros painéis.

O antipadrão tem forma reconhecível: vinte gráficos bonitos, eixos sem unidade, nenhuma linha de
referência, nenhum limiar marcado, e nenhuma pergunta escrita em lugar nenhum. Ele consome semanas para
construir e não é aberto durante o incidente, porque ninguém sabe o que procurar nele.

### OBS-046 — Todo gráfico tem unidade, escala e a linha do objetivo **[OBRIGATÓRIA]**

Sem o limiar desenhado, o leitor não sabe se 340 ms é bom. Um gráfico sem referência exige conhecimento
prévio para ser lido, e conhecimento prévio é exatamente o que falta a quem foi acionado às 3h da manhã
(`CON-045`).

### OBS-047 — Um painel por público e por pergunta, não um painel para todos **[RECOMENDADA]**

Três públicos com necessidades diferentes: quem está de plantão precisa de "o que está quebrado agora";
quem investiga precisa de fatiar por dimensão; quem decide precisa de tendência semanal. Um painel único
que tenta servir aos três serve mal aos três, e é abandonado pelos três.

---

## Capítulo 17.9 — SLI, SLO e orçamento de erro

### OBS-048 — SLI mede um evento do usuário, não a saúde de um processo **[OBRIGATÓRIA]**

Um indicador de nível de serviço é uma razão entre eventos bons e eventos válidos, definida da perspectiva
de quem usa: proporção de tentativas de checkout que terminam em confirmação em menos de 3 segundos.
Disponibilidade de processo, uso de CPU e resultado de verificação de saúde não são SLI.

O erro que isto previne é o mais comum de todos: 99,98% de disponibilidade do serviço enquanto o
percentual de checkouts concluídos caiu de 94% para 61%, porque o serviço responde HTTP 200 com um erro
de negócio dentro. É o mesmo ponto cego de `OPS-019`, agora no plano do objetivo declarado.

### OBS-049 — SLO é número, janela e público, os três **[OBRIGATÓRIA]**

"99,9% em 30 dias corridos, para todos os inquilinos do plano empresarial." Sem janela, o número não é
verificável — 99,9% em um dia permite 86 segundos de falha, em 30 dias permite 43 minutos, e a diferença
muda o desenho da arquitetura.

Sem público declarado, o objetivo é medido no agregado e um inquilino grande esconde o desastre de cem
pequenos.

### OBS-050 — Cem por cento não é objetivo **[IMUTÁVEL]**

Objetivo de 100% proíbe deploy, proíbe manutenção e é falso na primeira falha de rede que não está sob
seu controle. Pior: um objetivo impossível é descumprido sempre, e um objetivo sempre descumprido é
ignorado — o que remove o único mecanismo que fazia o número influenciar decisão.

O número correto é o menor que os usuários não percebem como problema, porque cada nove adicional
multiplica o custo de arquitetura e reduz a velocidade de entrega.

### OBS-051 — O orçamento de erro é a unidade de decisão de lançamento **[OBRIGATÓRIA]**

O orçamento é o complemento do SLO: 99,9% em 30 dias autoriza 43 minutos de falha. Enquanto sobra
orçamento, entrega-se com risco normal. Quando o orçamento se esgota, a política declarada entra em
vigor — e ela precisa estar escrita antes, porque escrita durante é negociação.

| Orçamento restante | Consequência declarada |
| --- | --- |
| Acima de 50% | Entrega normal; risco `R3` aceito com mitigação padrão |
| Entre 10% e 50% | Mudança `R3`/`R4` exige liberação gradual (`OPS-036`); nada de migração de dados |
| Abaixo de 10% | Só correção de defeito e redução de risco; funcionalidade nova espera |
| Esgotado | Congelamento de funcionalidade até a janela renovar, com dono nomeado da decisão |

Isso é o que transforma confiabilidade de opinião em restrição. Sem orçamento, a conversa "podemos
lançar?" é resolvida por quem fala mais alto; com orçamento, é resolvida por um número que ninguém
controla sozinho.

### OBS-052 — Velocidade de consumo alerta antes do esgotamento **[OBRIGATÓRIA]**

Alertar quando o orçamento acabou é alertar depois do dano. O que se vigia é a **velocidade de consumo**:
gastar em uma hora o que a janela reservava para um dia é incidente em andamento, mesmo que o total
mensal ainda esteja confortável.

Duas velocidades, com destinos diferentes: consumo rápido em janela curta interrompe pessoa; consumo
lento e persistente em janela longa abre item de trabalho. Alertar as duas no mesmo canal produz a fadiga
que `OPS-026` trata como falha de configuração.

### OBS-053 — SLO sem consequência declarada não existe **[OBRIGATÓRIA]**

Se descumprir o objetivo não muda nenhuma decisão, o objetivo é decoração — `CON-050` aplicado a
confiabilidade. A consequência é escrita junto com o número: o que congela, quem decide, e o que é
revisto.

### OBS-054 — Escolha os fluxos com SLO pela consequência da falha **[RECOMENDADA]**

Definir SLO para tudo dilui a atenção e produz dezenas de números que ninguém acompanha. Comece pelos
fluxos onde a falha custa dinheiro ou confiança de forma imediata: autenticar, concluir compra, receber
webhook de pagamento, emitir documento fiscal. Relatório e exportação raramente merecem SLO formal —
merecem limiar (`PRF-038`).

---

## Capítulo 17.10 — Alerta acionável

`OPS-023` exige que o alerta seja acionável, `OPS-025` que tenha runbook, `OPS-027` que tenha dono, e
`OPS-024` que prefira sintoma a causa. Este capítulo trata do que sustenta essas quatro exigências ao
longo do tempo, que é onde elas normalmente se degradam.

### OBS-055 — Todo alerta declara a consequência de ser ignorado **[OBRIGATÓRIA]**

Três campos, escritos junto com o alerta: o que acontece se ninguém agir em 5 minutos, em 1 hora, em 1
dia. Um alerta cuja resposta às três é "nada de importante" não é alerta: é informação, e informação
mora em painel.

Esse campo é o que permite decidir, sem debate, se o alerta interrompe uma pessoa ou abre um item de
trabalho. Sem ele, todo alerta é configurado como urgente por precaução, e a precaução produz o
silenciamento do canal.

### OBS-056 — Interromper uma pessoa exige ação humana imediata e útil **[OBRIGATÓRIA]**

Só acorda alguém o alerta que satisfaz as três condições: existe dano em curso, existe ação humana que o
reduz, e essa ação não pode esperar o horário comercial. Falhando qualquer uma, o destino é item de
trabalho.

O caso mais comum de violação é o alerta de coisa que se resolve sozinha: um retry que vai funcionar, um
pico que vai passar, um nó que o orquestrador vai substituir. Ele acorda alguém para assistir ao sistema
se recuperar, e o custo é real — a pessoa acordada às 3h decide pior no dia seguinte, e o alerta seguinte
recebe menos atenção.

### OBS-057 — O limiar do alerta vem do objetivo, não do palpite **[OBRIGATÓRIA]**

O limiar deriva do SLO e da velocidade de consumo (`OBS-052`), ou do limiar declarado de performance
(`PRF-038`). Número escolhido por intuição erra nas duas direções, e as duas são conhecidas: alto demais
não detecta, baixo demais dispara toda semana até alguém silenciar a regra — e ninguém lembra de
reativá-la.

### OBS-058 — Alerta tem duração mínima e histerese **[RECOMENDADA]**

A condição precisa persistir por uma janela antes de disparar, e cair abaixo de um limiar menor antes de
resolver. Sem isso, uma métrica oscilando em torno do limiar produz uma sequência de disparos e
resoluções que é indistinguível de ruído e treina o time a esperar antes de olhar.

### OBS-059 — O que nunca deve alertar **[OBRIGATÓRIA]**

| Nunca alerte | Por quê | Onde isso mora |
| --- | --- | --- |
| Uso de CPU ou memória em si | Pode ser saudável; alta utilização é o objetivo de quem paga | Painel de saturação |
| Reinício isolado de instância substituível | Já é o comportamento correto do orquestrador | Métrica de taxa de reinício |
| Falha única que o retry resolve | Nenhuma ação humana é necessária | Métrica de taxa de retry |
| Deploy concluído, job concluído, fila esvaziada | É informação, não anomalia | Registro e painel |
| Erro de validação do usuário | É produto funcionando; alertar é confundir usuário com defeito | Métrica de produto |
| Limiar de disco em ambiente efêmero | Alerta que nunca exige ação treina a ignorar | Automatizar a limpeza |
| Qualquer condição sem runbook | Quem for acionado não terá o que fazer (`OPS-025`) | Corrigir ou remover |

Taxa de reinício, taxa de retry e taxa de erro de validação **são** métricas legítimas, e a mudança de
padrão nelas pode alertar. O que não alerta é a ocorrência individual.

### OBS-060 — Fadiga de alerta é medida, e o número é responsabilidade da engenharia **[OBRIGATÓRIA]**

Duas métricas, revisadas em calendário: número de alertas por turno de plantão e proporção dos que
exigiram ação humana. Limiar padrão `[perfil]`: mais de dois alertas por turno noturno, ou menos de 70%
de alertas acionáveis, é achado com correção obrigatória na rodada.

**Fadiga não é falha de disciplina do time.** Ela é a resposta racional e previsível a um sistema de
alertas com baixa precisão: quem recebe cinquenta alertas por semana e age em três aprende, corretamente,
que o custo esperado de olhar é maior que o benefício. Tratar isso como problema de atitude mantém a
causa intacta. `OPS-026` já classifica ruído como falha de configuração; esta regra fornece o número que
torna a falha visível antes do incidente perdido, e o registro alimenta o aprendizado de `OPS-047`.

---

## Capítulo 17.11 — Observabilidade de frontend

### OBS-061 — Erro de cliente carrega versão do artefato e contexto de sessão **[OBRIGATÓRIA]**

Erro capturado no navegador registra: versão do pacote implantado, rota, ação do usuário que o precedeu,
navegador e versão, e o identificador de correlação da última requisição. Sem a versão do artefato, o
erro é irreprodutível — o mapa de código-fonte que o traduz corresponde a um build específico, e sem
saber qual, a pilha é ilegível.

Sem limite de erro na fronteira de tela (`FRT-019`), o que se coleta é a tela branca sem nenhum contexto
do que o usuário estava fazendo.

### OBS-062 — Métrica de usuário real, não apenas sintética **[OBRIGATÓRIA]**

Medição em laboratório mede a sua máquina e a sua rede. O que decide se o produto é lento é a
distribuição no campo, por rota, por dispositivo e por região — e ela é regularmente duas a quatro vezes
pior que a sintética. Os limiares de `PRF-038` são verificados contra o campo; a medição sintética serve
para bloquear regressão no pipeline, não para afirmar que o produto está rápido.

### OBS-063 — Telemetria vinda do cliente é entrada não confiável **[OBRIGATÓRIA]**

O endpoint que recebe telemetria de navegador é uma API pública: valida schema, limita tamanho, limita
taxa por origem, e nunca deriva identidade a partir do que o cliente afirma (`ESC-039`). Qualquer pessoa
pode enviar mil eventos por segundo dizendo ser outro inquilino.

Duas consequências, ambas registradas em produção real: distorção de métrica de negócio por dado
fabricado, e conta de ingestão inflada por tráfego que não é seu.

### OBS-064 — Falha de rede do cliente é sinal de produto, não ruído **[RECOMENDADA]**

Requisição que nunca chegou ao servidor é invisível na telemetria de servidor por definição. É ela que
explica a diferença entre "97% de sucesso" no servidor e a percepção do usuário em conexão instável, e é
o que justifica trabalho de resiliência no cliente em vez de discussão sobre se o problema existe.

---

## Capítulo 17.12 — Depuração em produção

### OBS-065 — Aumentar verbosidade é operação com escopo, prazo e reversão **[OBRIGATÓRIA]**

Elevar o nível de log é feito por escopo — um serviço, um inquilino, uma rota — com prazo de expiração
automático, sem deploy. Verbosidade global ativada durante um incidente e esquecida depois é a origem
clássica do salto de fatura, e frequentemente da inclusão acidental de dado sensível em log
(`OPS-016`).

Sem expiração automática, a reversão depende de alguém lembrar, e ninguém lembra depois de um incidente
resolvido às 4h.

### OBS-066 — Nenhuma coleta que altere o comportamento observado **[OBRIGATÓRIA]**

Depuração em produção não para o mundo: nada de ponto de parada, nada de perfilamento de alocação que
pausa o processo, nada de despejo de memória em instância que atende tráfego. A alternativa é sempre
alguma forma de amostragem contínua de baixo impacto, ou reproduzir com o tráfego espelhado.

A consequência de violar é o incidente causado pela investigação, que é a pior categoria de incidente
porque destrói a confiança na própria ferramenta de investigação.

### OBS-067 — Consulta de investigação repetida vira painel ou campo **[RECOMENDADA]**

Uma consulta improvisada duas vezes é uma pergunta recorrente disfarçada de acidente. Na terceira, ela se
torna painel, alerta, ou — se foi necessário extrair informação de texto livre para respondê-la — um
campo estruturado no log (`OBS-009`). Registre o item com gatilho de promoção (`AUD-036`).

---

## Capítulo 17.13 — Custo e retenção

### OBS-068 — Telemetria tem orçamento declarado por serviço, e ele é medido **[OBRIGATÓRIA]**

O orçamento é expresso como fração do custo de infraestrutura do serviço, declarado no
[perfil do projeto](templates/perfil-do-projeto.md). Faixa de referência `[perfil]`: 5% a 15%. Passar
disso não é automaticamente errado — é automaticamente uma decisão que precisa de dono.

Sem orçamento, o crescimento é invisível porque é gradual: cada PR adiciona três campos, e a conta dobra
em um ano sem que nenhuma decisão tenha sido tomada.

### OBS-069 — Retenção é declarada por sinal e por camada **[OBRIGATÓRIA]**

| Sinal | Consulta quente `[perfil]` | Frio ou arquivo | Motivo |
| --- | --- | --- | --- |
| Log de aplicação | 7 a 15 dias | 90 dias comprimido | Investigação real ocorre em dias |
| Log de auditoria e segurança | 90 dias | 1 a 5 anos, conforme obrigação | Exigência legal, não operacional (`SEC-011`) |
| Métrica de resolução fina | 15 dias | agregada por hora, 13 meses | Comparação ano a ano precisa de agregado, não de detalhe |
| Trace | 3 a 7 dias | amostra representativa, 30 dias | Trace antigo raramente responde algo |

Retenção de log de auditoria segue a mesma disciplina de dado pessoal de `SEC-055` e a retenção por
tabela de `DAT-039`: prazo declarado e eliminação automatizada, não "para sempre por segurança".

Retenção indefinida é a decisão padrão quando ninguém decide, e é a mais cara de todas.

### OBS-070 — Corte de custo é por pergunta, nunca por percentual **[OBRIGATÓRIA]**

Quando a telemetria custa mais que o serviço, a redução linear — "cortar 40% do log" — é a pior opção
disponível: ela remove aleatoriamente, e o que se perde só é descoberto no incidente seguinte, quando a
pergunta não tem mais resposta.

A ordem correta de corte, do mais barato ao mais doloroso:

```
1. Remover eventos sem consumidor nomeado (OBS-015)     ← quase sempre resolve, e não perde resposta
2. Remover campos que nenhuma pergunta usa (OBS-002)
3. Encurtar retenção quente, mantendo arquivo frio (OBS-069)
4. Amostrar o que pode ser amostrado, com taxa registrada (OBS-014)
5. Reduzir cardinalidade de rótulo por classe (OBS-035)
6. Desligar tracing onde ele não paga (OBS-027)
7. Aceitar perder uma pergunta — e declarar qual, por escrito
```

O passo 7 é uma decisão de risco com dono nomeado (`CON-042`), não um efeito colateral de configuração.
Times que pulam direto para o passo 4 costumam descobrir, meses depois, que os passos 1 e 2 sozinhos
resolveriam o problema sem custo nenhum de capacidade.

---

## Padrões reutilizáveis

**Linha canônica de requisição.** Um registro por unidade de trabalho, emitido no encerramento, com
resultado, duração, contagem de consultas, chamadas externas e as decisões de negócio (`OBS-011`).
*Use quando* o sistema é um monólito ou tem poucas fronteiras. *Não use como substituto* de trace em
arquitetura de cinco serviços — ela não mostra o salto entre eles.

**Contexto acumulado por requisição.** Uma estrutura criada na borda que acumula campos ao longo do
processamento e é despejada na linha canônica. *Use quando* os campos interessantes são descobertos em
camadas diferentes. *Não use* como sacola de tudo: ela herda o limite de `OBS-002`.

**Envelope de mensagem com metadado de rastreio.** Toda mensagem publicada carrega correlação, tentativa
e carimbo de origem em metadado separado da carga útil (`OBS-018`). *Use sempre* que houver fila.

**Métrica derivada de span no coletor.** Contagem e histograma calculados antes da amostragem, para que
o alerta seja completo e o trace amostrado (`OBS-029`). *Use quando* já existe tracing e você quer
métrica por operação sem instrumentar duas vezes.

**Sentinela de ausência.** Métrica de "segundos desde a última conclusão com sucesso" para todo processo
periódico (`OBS-041`). *Use sempre* que houver job, sincronização ou exportação agendada.

**Interruptor de verbosidade por escopo, com expiração.** Elevação de nível por inquilino ou rota,
ativável sem deploy, com desligamento automático (`OBS-065`). *Use* quando houver mais de um inquilino.

**Alerta de velocidade de consumo em duas janelas.** Janela curta interrompe pessoa; janela longa abre
item de trabalho (`OBS-052`). *Use* quando existir SLO. *Não use* sem SLO — sem orçamento, não há
velocidade a medir.

---

## Matrizes de decisão

**Onde gravar um dado que você quer poder consultar depois**

| Natureza do dado | Cardinalidade | Destino | Motivo |
| --- | --- | --- | --- |
| Contagem de ocorrências | baixa | Métrica com rótulo de classe | Barato, completo, serve a alerta |
| Identificador de entidade | ilimitada | Log e atributo de span | Só ali o custo é por evento (`OBS-035`) |
| Duração de operação | — | Histograma e span | Percentil exige distribuição (`OBS-032`) |
| Decisão de negócio tomada | média | Log estruturado, evento nomeado | Precisa ser explicável caso a caso |
| Estado atual de um recurso | baixa | Medidor | A pergunta é "quanto há agora" |
| Conteúdo de entrada do usuário | — | Nenhum | `OPS-016` e `OBS-012` |

**Destino de um sinal de anomalia**

| Situação | Destino | Critério |
| --- | --- | --- |
| Dano em curso, ação humana existe, não pode esperar | Interrompe pessoa | `OBS-056` |
| Dano em curso, ação é automática | Métrica e painel | Nada a fazer manualmente |
| Degradação lenta com dias de margem | Item de trabalho com dono | `OBS-052`, janela longa |
| Condição sem runbook | Nenhum destino: corrigir ou remover | `OPS-025` |
| Anomalia que interessa só em investigação | Painel | `OBS-045` |

**Quanto instrumentar, por criticidade do fluxo**

| Criticidade do fluxo | Log | Métrica | Trace | SLO |
| --- | --- | --- | --- | --- |
| Dinheiro, identidade, documento fiscal | Linha canônica e evento por decisão | Completa, com classe de erro | Sim, 100% dos erros | Sim |
| Fluxo principal de produto | Linha canônica | Completa | Amostrado | Sim |
| Funcionalidade secundária | Linha canônica | As quatro de `OPS-018` | Herdado | Não; limiar |
| Ferramenta interna | Erro apenas | Erro e latência | Não | Não |

---

## Fluxo de trabalho

```
1. Escreva as perguntas          → o que precisará ser respondido em produção, e por quem (OBS-002)
2. Classifique cada pergunta     → agregado contínuo (métrica) ou explicação de caso (log/trace)
3. Defina o SLI do fluxo         → evento do usuário, não saúde de processo (OBS-048)
4. Instrumente na mesma mudança  → schema de log, métricas do componente, spans de fronteira (OBS-005)
5. Verifique a resposta          → execute a consulta antes de considerar pronto; sem consulta rodada,
                                   a instrumentação é HIPÓTESE (CON-009)
6. Construa o painel da pergunta → título é a pergunta; limiar desenhado (OBS-045, OBS-046)
7. Derive o alerta do objetivo   → limiar do SLO, com consequência de ignorar escrita (OBS-055, OBS-057)
8. Declare custo e retenção      → orçamento do serviço e prazo por sinal (OBS-068, OBS-069)
9. Feche o ciclo no incidente    → cada pergunta sem resposta durante o incidente é item de backlog
                                   com gatilho (AUD-036), e entra no aprendizado de OPS-047
```

O passo 5 é o que separa instrumentação real de intenção. Log escrito e nunca consultado costuma estar
com campo faltando, tipo errado ou nome divergente, e a descoberta acontece durante o incidente.

---

## Exemplos de implementação

**Cardinalidade de rótulo (`OBS-035`)**

```js
// Ruim — OBS-035: pedidoId e a mensagem livre criam uma série por pedido e por texto de erro.
// Em produção isso passou de 2 milhões de séries em uma semana e o coletor começou a
// descartar séries, inclusive as que sustentavam o alerta de taxa de erro do checkout.
metricas.contador('checkout_falhas', 1, {
  pedidoId: pedido.id,
  inquilinoId: pedido.inquilinoId,
  erro: erro.message,
})

// Bom
metricas.contador('checkout_falhas_total', 1, {
  plano: pedido.plano,              // 4 valores
  classe: classificar(erro),        // enumerável: 'saldo_insuficiente' | 'fornecedor_timeout' | ...
  gateway: pedido.gateway,          // 3 valores
})
log.warn('checkout.falhou', {
  pedidoId: pedido.id,              // cardinalidade alta mora aqui (OBS-003)
  inquilinoId: pedido.inquilinoId,
  classe: classificar(erro),
  gateway: pedido.gateway,
  tentativa: pedido.tentativas,
})
```

**Correlação atravessando a fila (`OBS-018`, `OBS-020`)**

```js
// Ruim — OBS-018: a correlação vai dentro da carga útil, virando parte do contrato da mensagem,
// e a tentativa não é registrada, então três retentativas contam como três falhas distintas.
await fila.publicar('nota-fiscal.emitir', {
  pedidoId, correlacaoId: contexto.correlacaoId,
})

// Bom
await fila.publicar(
  'nota-fiscal.emitir',
  { pedidoId },
  { metadados: {
      correlacaoId: contexto.correlacaoId,   // origem preservada em todas as tentativas
      tentativa: 1,
      publicadoEm: agora(),
      versaoArtefato: processo.versao,
  } },
)
```

**Sentinela de ausência em job agendado (`OBS-041`)**

```js
// Ruim — OBS-041: só existe métrica quando o job roda. O agendador foi reconfigurado num
// domingo, o job de faturamento não executou por seis dias, a taxa de erro permaneceu zero,
// e a descoberta foi por um cliente perguntando pela fatura.
try { await faturarAssinaturas() } catch (erro) { metricas.contador('faturamento_erros', 1) }

// Bom
try {
  const resultado = await faturarAssinaturas({ execucaoId })
  metricas.medidor('faturamento_ultima_conclusao_timestamp', agora())
  metricas.medidor('faturamento_assinaturas_processadas', resultado.total)
} catch (erro) {
  metricas.contador('faturamento_erros_total', 1, { classe: classificar(erro) })
  throw erro
}
// Alerta: agora() - faturamento_ultima_conclusao_timestamp > intervalo esperado + folga
```

**SLI de evento de usuário (`OBS-048`)**

```
Ruim — OBS-048: mede o processo, não a pessoa.
  SLI = requisições com status 5xx / total de requisições
  Resultado observado: 99,98%. Enquanto isso, 39% dos checkouts terminavam em HTTP 200
  com erro de negócio do gateway, e o objetivo permanecia cumprido.

Bom
  Eventos válidos = tentativas de checkout com carrinho não vazio e pagamento submetido
  Eventos bons    = tentativas confirmadas em menos de 3 s, sem erro de sistema
  SLI = bons / válidos     SLO = 99,5% em 30 dias corridos, por inquilino do plano empresarial
  Orçamento = 0,5% das tentativas; consequência de esgotar: congelamento (OBS-051)
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Instrumentar sem escrever a pergunta | Volume alto e nenhuma resposta; custo cresce, capacidade não |
| Identificador de entidade em rótulo de métrica | Explosão de séries; o coletor descarta as séries do alerta |
| Média de percentis entre instâncias | A instância patológica desaparece exatamente na conta |
| Medidor para latência | Perde a distribuição; o p95 deixa de existir |
| Faixas de histograma longe do limiar | Regressão de 320 ms para 780 ms fica invisível |
| Amostragem uniforme de trace | O caso raro, que é o que interessa, quase nunca é capturado |
| Alertar sobre trace amostrado | Disparo por sorte estatística; o time deixa de confiar no alerta |
| Painel bonito sem pergunta no título | Semanas de construção, e não é aborto durante o incidente |
| Gráfico sem unidade nem linha de objetivo | Quem foi acionado às 3h não sabe se o número é bom |
| Profundidade de fila como métrica de atraso | Dez mensagens paradas há duas horas não aparecem |
| Job sem sentinela de ausência | Não rodar é indistinguível de estar tudo bem |
| Confiar na página de status do fornecedor | Discussão sobre culpa em vez de acionar o modo degradado |
| Exportador de telemetria síncrono | Coletor lento vira indisponibilidade do produto |
| Rebaixar nível de log para reduzir custo | Esconde o problema e degrada o diagnóstico seguinte |
| SLO de 100% | Descumprido sempre, logo ignorado sempre |
| SLO sem consequência escrita | "Podemos lançar?" volta a ser decidido por quem fala mais alto |
| Alertar no esgotamento do orçamento | Alerta depois do dano |
| Alertar CPU, reinício isolado e retry único | Fadiga, silenciamento do canal, alerta real perdido |
| Tratar fadiga como falta de disciplina | A causa permanece e o próximo incidente também passa |
| Verbosidade global ativada e esquecida | Salto de fatura e dado sensível em log |
| Corte linear de telemetria por percentual | Perde-se aleatoriamente; descobre-se no incidente seguinte |
| Retenção indefinida por precaução | A decisão mais cara, tomada por omissão |

---

## Checklist

- [ ] Cada instrumentação nova tem uma pergunta escrita e um consumidor. (`OBS-002`, `OBS-015`)
- [ ] Todo evento carrega inquilino, sujeito e versão do artefato. (`OBS-003`, `OBS-009`)
- [ ] Exportação de telemetria é assíncrona, com timeout e descarte contado. (`OBS-004`)
- [ ] Nomes de evento são fatos no passado, enumeráveis, não interpolados. (`OBS-010`)
- [ ] Nenhum corpo de requisição, URL com parâmetros ou pilha em nível informativo. (`OBS-012`)
- [ ] Amostragem declarada; erro, negócio e segurança não amostrados. (`OBS-014`)
- [ ] Volume de log medido por serviço e por evento. (`OBS-016`)
- [ ] Correlação atravessa fila em metadado e sobrevive à retentativa. (`OBS-018`, `OBS-020`)
- [ ] Job tem identificador de execução; chamada externa registra o identificador do fornecedor.
      (`OBS-019`, `OBS-021`)
- [ ] Spans declaram resultado e marcam erro no mecanismo do formato. (`OBS-023`, `OBS-025`)
- [ ] Amostragem de trace mantém 100% dos erros e dos lentos. (`OBS-026`)
- [ ] Tipo de métrica corresponde à pergunta; latência é histograma. (`OBS-030`, `OBS-032`)
- [ ] Nenhum percentil agregado por média. (`OBS-033`)
- [ ] Cardinalidade de rótulo calculada; nenhum identificador de entidade. (`OBS-034`, `OBS-035`)
- [ ] Erros contados por classe de domínio. (`OBS-037`)
- [ ] Conjunto mínimo do tipo de componente presente. (`OBS-039`)
- [ ] Fila tem idade da mensagem mais antiga; job tem sentinela de ausência. (`OBS-040`, `OBS-041`)
- [ ] Integração externa medida na sua borda; banco com métrica de contenção. (`OBS-042`, `OBS-043`)
- [ ] Destino final de mensagens alerta em qualquer chegada. (`OBS-044`)
- [ ] Painel tem a pergunta no título e limiar desenhado. (`OBS-045`, `OBS-046`)
- [ ] SLI é evento de usuário; SLO tem número, janela e público. (`OBS-048`, `OBS-049`)
- [ ] Orçamento de erro com consequência escrita e alerta de velocidade. (`OBS-051`, `OBS-052`)
- [ ] Todo alerta declara a consequência de ser ignorado e só interrompe se houver ação.
      (`OBS-055`, `OBS-056`)
- [ ] Taxa de alerta acionável medida no período. (`OBS-060`)
- [ ] Orçamento e retenção de telemetria declarados por sinal. (`OBS-068`, `OBS-069`)

---

## Prompt do volume

```
You are the DevOps/SRE agent of the EOS, operating Volume 17 — Observability (`OBS`).

Mission: determine whether this system can answer, from telemetry that already exists, the questions
that a real incident will raise — and report every place where it cannot.

Load first: agents/_shared/core-contract.md, 00-constituicao-da-engenharia.md, 17-observabilidade.md,
10-devops.md chapter 10.3 and 10.4 (the detection and alerting foundation you must cite, never restate),
and the filled templates/perfil-do-projeto.md. If the profile does not exist, your first deliverable is
to propose it: retention windows, cost budget and criticality thresholds all depend on it.

Mandatory sequence. Do not reorder.
1. Enumerate the questions this module must answer in production. Write them down before reading any
   instrumentation code. Include at least: is it broken now; did the last deploy cause it; which tenant
   is affected; where did the time go; did the scheduled work run.
2. Inventory the existing telemetry with evidence — path:line for emission sites, and the actual query
   or dashboard for consumption. Emission without a named consumer is a finding, not an asset.
3. Answer each question from step 1 using only what exists. Run the query. A question you cannot answer
   without a deploy is the primary finding of this analysis.
4. Audit log discipline: declared schema, event naming, forbidden content, field type stability,
   sampling policy, measured volume per service.
5. Audit correlation across every asynchronous boundary: queue, scheduled job, retry, reprocessing,
   external vendor call. Name the boundary where the chain breaks.
6. Audit metrics: type versus question, histogram buckets against the declared threshold, label
   cardinality computed as a product, error classification.
7. Audit the minimum metric set for each component type present (API, worker, job, database, external
   integration, frontend). Report absences, not opinions.
8. Audit SLI/SLO: is the SLI a user event; does the SLO have number, window and audience; is there an
   error budget with a written consequence and a burn-rate alert.
9. Audit alerts: consequence of being ignored, human action available, threshold derived from the
   objective, and the measured actionable-alert ratio.
10. Audit cost and retention against the declared budget, per signal.

Rules of engagement.
- Evidence or nothing (`CON-009`). "There is no metric for this" requires the search you ran.
- Never restate a rule from Volume 10. Cite the `OPS` id and build on top of it.
- Every proposed instrumentation states the question it answers and its recurring cost.
- Proposing more telemetry while the module already emits unconsumed events is a rejected finding:
  removal comes before addition.
- Do not propose a dashboard without writing the question that titles it.
- Stop and escalate if telemetry currently carries personal or sensitive data: that is a security
  finding, classified by Volume 6, and it interrupts this analysis.

Output: exactly the "Verificação obrigatória de saída" block of Volume 17, in Brazilian Portuguese,
with `MUST-FIX` and `OPPORTUNITY` in separate lists (`CON-018`), and every unfixed opportunity written
to the backlog with a promotion trigger (`AUD-036`).
```

---

## Critérios de aceite

Um módulo passa em observabilidade quando todos são verdadeiros:

1. As perguntas operacionais do módulo estão escritas, e cada uma tem uma consulta que a responde — com
   a consulta tendo sido executada, não presumida.
2. Nenhuma pergunta da lista exige deploy para ser respondida (`OBS-001`).
3. O schema de log é declarado e aplicado por construção; versão do artefato presente em todo registro.
4. A correlação sobrevive a todas as fronteiras assíncronas do módulo, verificada seguindo um caso real
   de ponta a ponta.
5. O conjunto mínimo de métricas do tipo de componente está presente, e nenhuma métrica usa
   identificador de entidade como rótulo.
6. Todo fluxo de criticidade alta tem SLI de evento de usuário, SLO com janela e público, orçamento de
   erro com consequência escrita.
7. Todo alerta tem dono, runbook, ação humana disponível e consequência de ser ignorado declarada; a
   taxa de alertas acionáveis do último período está acima do limiar do perfil.
8. Orçamento e retenção de telemetria declarados, medidos, e dentro da faixa do perfil — ou fora dela
   com aceitação de risco assinada por pessoa nomeada.
9. Nenhum dado sensível na telemetria, verificado por amostragem de registros reais de produção.

Falha em 2, 5 ou 9 é reprovação direta: o primeiro significa que o módulo não é observável, o segundo
que a telemetria pode derrubar o sistema de métricas, e o terceiro é achado de segurança.

---

## Verificação obrigatória de saída

```
## Perguntas e respostas
| Pergunta operacional | Sinal que responde | Consulta executada | Respondida? |

Perguntas sem resposta sem deploy: <n>   ← se > 0, este é o achado principal (OBS-001)

## Log
Schema declarado: <onde> | Versão do artefato presente: <sim/não>
| Evento | Volume/dia | Consumidor nomeado | Amostragem | Veredito |
Campos proibidos encontrados: <lista com path:line>

## Correlação
| Fronteira (processo, fila, job, retry, fornecedor) | Propaga? | Evidência | Lacuna |

## Métricas
| Métrica | Tipo | Rótulos | Séries estimadas | Consumidor | Veredito |
Rótulos de cardinalidade ilimitada: <lista>
Percentis agregados por média: <lista>

## Conjunto mínimo por componente
| Componente | Métricas exigidas ausentes | Consequência da ausência | Severidade |

## Tracing
Adotado: <sim/não/parcial> | Paga aqui? <justificativa por OBS-027>
Política de amostragem: <...> | Preserva erro e lento: <sim/não>

## Painéis
| Painel | Pergunta declarada no título | Limiar desenhado | Última consulta |

## SLI / SLO
| Fluxo | SLI (evento) | SLO (número, janela, público) | Orçamento | Consequência escrita |
Velocidade de consumo alertada: <sim/não>

## Alertas
| Alerta | Sintoma ou causa | Dono | Runbook | Ação humana | Consequência se ignorado |
Alertas do período: <n> | Acionáveis: <n> | Taxa: <%> | Limiar do perfil: <%>
Alertas a remover ou corrigir: <lista>

## Frontend
Erro de cliente com versão do artefato: <sim/não> | Métrica de usuário real: <sim/não>
Endpoint de telemetria validado e limitado: <sim/não>

## Custo e retenção
| Sinal | Volume/mês | Custo/mês | Retenção quente | Retenção fria | Dentro do orçamento |
Custo de telemetria / custo de infraestrutura: <%> | Faixa do perfil: <%>
Ordem de corte proposta (OBS-070): <passos, com a pergunta perdida em cada um>

## Camadas não cobertas
<declaração explícita, por CON-027>
```
