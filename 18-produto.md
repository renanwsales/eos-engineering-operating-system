# 📘 Volume 18 — Produto

Prefixo: `PRD` · Regras: PRD-001 a PRD-058 · Papel: [Product/UX](agents/09-product-ux.md)

Há uma falha que passa em todo teste de engenharia e ainda assim destrói o trimestre: construir a
coisa certa do jeito certo para o problema errado. O código compila, a cobertura sobe, a revisão
aprova, e seis semanas depois o time descobre que o usuário resolvia o problema com uma planilha —
ou que o problema era de outro papel — ou que não havia problema mensurável, só um pedido de um
cliente grande. Engenheiros competentes gastam capacidade em solução sem restrição. Isso não é
defeito de código. É falha de produto.

O erro caro que este volume previne é a **entrega correta de trabalho desnecessário**. Cada feature
que entra no produto tem custo permanente: superfície de suporte, caminho de regressão, carga
cognitiva na interface, ramo de autorização, migração futura. Construir sem critério de sucesso é
assumir esse custo sem saber o retorno. Cortar escopo depois do código escrito custa o dobro do
corte feito na especificação. Recusar um pedido ruim antes do primeiro commit é a intervenção mais
barata que existe neste livro.

O que muda no trabalho de quem lê: pedido deixa de ser fila de implementação e passa a ser hipótese
com dono, restrição, critério e exclusões. Engenheiro deixa de "só executar" e passa a poder — e
dever — recusar com evidência. Product owner deixa de priorizar por quem falou mais alto e passa a
ordenar por valor, risco e capacidade real.

**Fronteira.** É deste volume: enquadrar problema de produto versus solução disfarçada; identificar
quem sofre o problema; decidir o que **não** construir; escopo mínimo honesto; critério de sucesso
antes de construir; priorização de produto versus priorização técnica; descoberta proporcional ao
risco; requisito sem ambiguidade; trade-off prazo/escopo/dívida; custo de manutenção na decisão;
feature de um cliente só; comunicação de mudança; encerramento de funcionalidade; dívida de
produto; recusa fundamentada de pedido.

**Não é deste volume:** como desenhar a interface, estados, acessibilidade e redação de erro
(→ [08](08-ux-premium.md) `UXI`). Priorização e severidade de achados técnicos
(→ [00](00-constituicao-da-engenharia.md) `CON`). Depreciação de contrato de API
(→ [15](15-apis.md) `API`). Customização por inquilino no schema
(→ [16](16-multi-tenant.md) `MTN`). Quando IA é a solução correta
(→ [19](19-ia-no-produto.md) `IAX`). Métricas de qualidade da engenharia como disciplina
(→ [23](23-metricas.md)).

---

## Fundamentos

Produto, neste livro, é a disciplina de **escolher o que o sistema fará pelo usuário** — e o que
deixará de fazer. Não é roadmap colorido. Não é backlog infinito. É a sequência de decisões que
determina se a capacidade de engenharia produz valor ou superfície.

Três assimetrias governam o volume.

**Problema versus solução.** A Constituição já exige restrição em vez de tecnologia (`CON-028`).
Em produto a mesma falha aparece com outra roupagem: o pedido chega como tela, integração ou
"preciso de um dashboard", e o time discute implementação antes de saber quem perde tempo ou
dinheiro hoje. Enquanto a restrição não estiver escrita sem nomear a solução, nenhuma alternativa
real existe (`CON-030`), inclusive a de não fazer (`CON-029`).

**Valor versus correção.** Uma implementação correta de feature desnecessária ainda é desperdício.
A auditoria técnica mede se o módulo está bem feito; este volume mede se deveria existir. São
veredictos ortogonais. Confundi-los produz o antipadrão clássico: o time defende a feature porque
o código está limpo.

**Descoberta versus risco.** Investir semanas em pesquisa para um toggle de preferência é teatro.
Lançar sem validação uma mudança que altera cobrança ou fluxo principal de onboarding é imprudência.
A proporção correta escala com irreversibilidade e raio de alcance (`CON-041`), não com o entusiasmo
de quem pediu.

O papel [Product/UX](agents/09-product-ux.md) é o desempate de intenção: quando o comportamento
desejado é ambíguo, ninguém inventa regra de negócio — escala-se. Este volume dá as regras que
tornam essa escalada operacional, e que permitem ao engenheiro dizer "não" sem parecer obstáculo.

---

## Capítulo 18.1 — Problema antes de solução

### PRD-001 — Problema de produto é restrição de valor, não de tecnologia **[IMUTÁVEL]**

Enuncie o que precisa ser verdade para o usuário ou o negócio, sem nomear tela, API, fornecedor ou
padrão. A forma é a de `CON-028` aplicada ao valor: restrição descreve o resultado; solução descreve
o caminho.

```
Ruim:  "Precisamos de um dashboard de churn com gráficos"
Bom:   "O CS precisa identificar, em menos de cinco minutos, quais inquilinos do plano Pro
        não renovaram nos últimos 30 dias e qual foi a última ação de suporte"
```

Se o enunciado ainda contém a solução, o trabalho de produto não começou. Começar pela solução
elimina alternativas — inclusive a de configurar um relatório existente — antes de considerá-las.

### PRD-002 — Solução disfarçada de pedido é rejeitada até reescrita **[OBRIGATÓRIA]**

Pedido que nomeia implementação ("adicionar filtro na listagem de assinaturas", "integrar com o
CRM X", "criar role de auditor") volta ao autor com a pergunta: qual restrição isso satisfaz, para
quem, com que frequência. Aceitar o pedido na forma dada congela a solução e transforma a
engenharia em escriba.

Consequência de aceitar: o time gasta o orçamento da sprint na primeira ideia verbalizada, e a
alternativa barata — se existia — nunca entra na comparação (`CON-031`).

### PRD-003 — Nomeie quem sofre o problema **[OBRIGATÓRIA]**

Todo problema de produto declara o sujeito: papel, segmento, plano, ou tipo de inquilino. "Os
usuários" não é sujeito. "O admin financeiro do plano Enterprise que fecha a fatura mensal" é.

Sem sujeito, não há como medir sucesso, não há como amostrar descoberta, e não há como saber se o
pedido de um cliente representa a base ou um outlier. Feature construída para sujeito fantasma
vira custo de manutenção pago por quem nunca pediu.

### PRD-004 — Frequência e custo do problema são números ou hipóteses rotuladas **[OBRIGATÓRIA]**

Declare: quantas vezes por semana o sujeito encontra o problema; quanto tempo ou dinheiro perde;
qual a evidência. Se o número é estimativa, rotule `HIPÓTESE`. Se não há número, o entregável é o
plano de medição, não a feature.

```
Ruim:  "O onboarding está ruim, muita gente reclama"
Bom:   "HIPÓTESE: 40% dos trials abandonam no passo de importar catálogo (fonte: funil das
        últimas 8 semanas). Custo estimado: 12 trials/semana × ticket médio R$ 180"
```

Afirmação sem evidência não vira prioridade. Vira `HYPOTHESIS` até alguém medir (`CON-009`).

### PRD-005 — Problema de um papel não é problema de todos **[OBRIGATÓRIA]**

Otimizar o fluxo do operador de suporte às custas do fluxo do comprador — ou o inverso — é troca,
não melhoria. Declare quem ganha e quem paga o custo cognitivo ou operacional da mudança.

Consequência de omitir: o time "melhora" uma tela medindo satisfação de um papel e descobre
queda de conversão no outro. A regressão era previsível; faltava o enunciado do trade-off
(`CON-032`).

### PRD-006 — Sintoma relatado não é diagnóstico **[OBRIGATÓRIA]**

"A tela de pedidos está lenta", "ninguém usa o relatório", "precisamos de mais campos" são
sintomas. O diagnóstico pode ser dado faltando, permissão errada, vocabulário confuso, ou
problema que o produto não deveria resolver.

Antes de abrir escopo de construção, pergunte: o usuário está pedindo alívio do sintoma ou a
remoção da causa. Construir sobre sintoma empilha paliativos; a causa continua gerando tickets.

---

## Capítulo 18.2 — O que não construir

### PRD-007 — Toda proposta declara o que fica de fora **[OBRIGATÓRIA]**

Escopo sem exclusões não é escopo: é autorização em branco. A proposta lista, em linguagem de
comportamento, o que **não** entra nesta entrega: papéis não cobertos, integrações adiadas, casos
de borda conscientes, plataformas fora.

Sem exclusões, cada stakeholder completa o pedido com a própria imaginação, e a "pequena adição"
aparece no meio da implementação — fora do orçamento de `AUD-004`.

### PRD-008 — Escopo mínimo é o menor conjunto que prova o critério de sucesso **[OBRIGATÓRIA]**

Não é o menor conjunto que impressiona numa demo. É o menor conjunto observável que permite
aceitar ou rejeitar a hipótese de valor. Tudo além disso é antecipação.

Se o critério é "o operador consegue emitir a segunda via em menos de dois minutos sem abrir
ticket", o mínimo pode ser um atalho no detalhe da fatura — não um portal de self-service completo.

### PRD-009 — "Também seria bom" não entra no escopo da entrega **[OBRIGATÓRIA]**

Itens de desejo adjacentes vão ao backlog com severidade de produto e gatilho de promoção
(`AUD-036`, `CON-019`). Misturá-los à entrega corrente transforma cada feature numa árvore de
dependências não orçadas.

Consequência: a entrega atrasa, o critério de sucesso dilui, e ninguém sabe se a hipótese original
foi validada ou ofuscada pelo excesso.

### PRD-010 — Opção zero é legítima em produto **[OBRIGATÓRIA]**

Não construir é alternativa real (`CON-029`). É a escolha correta quando o custo de manutenção
excede o valor esperado, quando o problema é raro e tem contorno manual aceitável, quando falta
evidência e o risco de errar é alto, ou quando a capacidade está consumida por `MUST-FIX`
técnico (`CON-038`).

Registrar "não faremos" com motivo é estado saudável de backlog — não fracasso.

### PRD-011 — Feature para um cliente só exige contrato de custo e generalização **[OBRIGATÓRIA]**

Antes de aceitar: o cliente paga o custo de construção e o de manutenção contínua; existe data ou
critério em que a feature generaliza ou é removida; o desvio não quebra invariantes do produto
para os demais inquilinos.

Sem esses três, a feature é fork disfarçado. Em multi-inquilino, regra de negócio divergente por
cliente já tem limiar em `MTN-037`: produto separado ou recusa.

### PRD-012 — Preferir configuração a fork de produto **[RECOMENDADA]**

Quando a variação entre clientes cabe em parâmetro, política ou campo tipado, use configuração —
não ramo de código por inquilino (`MTN-033`). Fork de produto multiplica o custo de cada mudança
futura pelo número de ramos vivos.

Exceção legítima: regulamentação que exige comportamento estruturalmente incompatível. Aí o
enunciado é produto distinto, não "flag escondida".

### PRD-013 — Comprar o que não é diferencial **[RECOMENDADA]**

Autenticação genérica, e-mail transacional, cobrança de cartão, helpdesk: construa só o que é
vantagem competitiva do domínio (`SEL-029`). Construir commodity para "ter controle" sem calcular
custo total de posse é vaidade de engenharia disfarçada de estratégia.

A decisão ainda passa pelas quatro perguntas de dependência (`SEL-030`) e pelo comportamento em
falha (`SEL-032`).

---

## Capítulo 18.3 — Critério de sucesso antes de construir

### PRD-014 — Critério de sucesso escrito antes do primeiro commit **[IMUTÁVEL]**

Nenhuma implementação de feature de produto começa sem critério observável escrito e aceito pelo
dono. "Fica melhor" e "o cliente pediu" não são critérios.

Sem critério prévio, qualquer resultado pode ser narrado como sucesso. Isso torna aprendizado
impossível e torna o corte de escopo político em vez de técnico.

Paralelo em IA no produto: o critério antecede a escolha do modelo (`IAX-004`). Aqui antecede a
escolha de qualquer caminho.

### PRD-015 — Critério é observável por terceiro sem perguntar ao autor **[OBRIGATÓRIA]**

Duas pessoas competentes, lendo só o critério, chegam ao mesmo veredito pass/fail sobre um caso
concreto. Se precisam interpretar intenção, o critério ainda é ambíguo (`A-003` aplicado a
produto).

```
Ruim:  "Melhorar a ativação do trial"
Bom:   "Em 30 dias após o lançamento, ≥ 55% dos trials novos completam a importação do primeiro
        catálogo em ≤ 10 minutos (mediana), medido no funil existente evento catalog.imported"
```

### PRD-016 — Métrica de sucesso distingue adoção de valor **[OBRIGATÓRIA]**

Abrir a tela não é sucesso. Sucesso é o resultado que o sujeito obtém. Contar cliques, pageviews
ou "usuários que viram o banner" como prova de valor é métrica de vaidade: guia o time a otimizar
exposição, não resultado.

Declare a métrica de resultado e, se útil, a de adoção como indicador intermediário — nunca como
substituto.

### PRD-017 — Horizonte de medição declarado com a entrega **[OBRIGATÓRIA]**

Todo critério traz a janela: 7 dias, 30 dias, um ciclo de cobrança. Sem horizonte, o time declara
sucesso no dia do lançamento com amostra irrelevante, ou nunca fecha o experimento.

Na data do horizonte: aceitar, iterar com novo critério, ou encerrar (`PRD-046`). Omitir o fechamento
é deixar feature zumbi no produto.

### PRD-018 — Sem critério, a entrega é experimento rotulado **[OBRIGATÓRIA]**

Há casos em que o critério ainda não pode ser escrito com honestidade — mercado novo, hipótese
fraca. Nesse caso o trabalho se chama **experimento**, tem orçamento curto, flag com prazo
(`OPS-038`, `ARC-034`), e critério de aprendizado (o que vamos saber ao terminar), não de
sucesso de produto.

Chamar experimento de feature é fraude de priorização: consome capacidade como se o valor já
estivesse demonstrado.

---

## Capítulo 18.4 — Priorização de produto versus técnica

### PRD-019 — Prioridade de produto ordena valor e risco de negócio **[OBRIGATÓRIA]**

A fila de produto responde: quanto valor esperado, para quem, com que incerteza, e o que acontece
se não fizermos. Não responde elegância de código, desejo de reescrever módulo, nem preferência
estética (`UXI-001`, `CON-013`).

Usar priorização técnica (`CON-036`, `CON-038`) para ordenar o roadmap de features confunde
camadas: um `S3` de nomenclatura não compete com uma hipótese de retenção; um `S0` de vazamento
não espera a próxima janela de roadmap.

### PRD-020 — Achado técnico S0 e S1 não entra em disputa com roadmap **[IMUTÁVEL]**

`S0` para tudo. `S1` bloqueia entrega (`CON-036`, `CON-038`). Nenhum argumento de "o cliente
espera a feature X" autoriza adiar correção de perda de dado, falha de autorização ou erro de
cobrança.

Consequência de negociar: o time acelera receita sobre fundação podre e paga em incidente, churn
e retrabalho. Produto maduro trata segurança e integridade como pré-condição, não como item do
backlog de inovação.

### PRD-021 — Capacidade da engenharia é restrição do plano **[OBRIGATÓRIA]**

Roadmap que ignora capacidade real — feriados, incidentes, dívida com gatilho vencido, onboarding
de gente nova — é ficção. Planeje com a capacidade líquida, não com a bruta.

Quando `MUST-FIX` consome a maior parte da capacidade por duas rodadas, o plano de produto
encolhe. Negar o fato produz prazo mentiroso e dívida escondida.

### PRD-022 — Fórmula de score de produto é declarada no perfil **[RECOMENDADA]**

Se o time usa score (alcance × impacto × confiança / esforço, ou variante), a fórmula vive no
[`perfil-do-projeto`](templates/perfil-do-projeto.md) e não muda a cada reunião. Mudar a fórmula
para fazer um item "ganhar" invalida o histórico de decisões.

Score ordena dentro da mesma classe de risco. Não autoriza pular `PRD-020`.

### PRD-023 — Trabalho que reduz custo operacional conta como produto **[RECOMENDADA]**

Automatizar um processo manual que consome 20 h/semana do CS é entrega de produto se o critério
for redução medida desse custo. Tratar só "features visíveis ao comprador" como produto enviesa o
roadmap contra a operação que sustenta o NPS.

O trabalho ainda precisa de restrição, critério e exclusões — não é licença para refatoração
cosmética (`CON-013`).

### PRD-024 — Roadmap sem capacidade comprometida é lista de desejo **[OBRIGATÓRIA]**

Itens sem trimestre, dono e fatia de capacidade alocada não são compromisso. Podem existir como
horizonte, desde que rotulados como tal. Misturar desejo e compromisso na mesma lista faz o time
parecer inadimplente o ano inteiro.

---

## Capítulo 18.5 — Descoberta proporcional ao risco

### PRD-025 — Investimento em descoberta escala com irreversibilidade **[OBRIGATÓRIA]**

| Risco da decisão | Descoberta mínima |
| --- | --- |
| Reversível, baixo blast (copy, filtro, atalho) | Evidência existente ou smoke com 3–5 usuários |
| Médio (fluxo novo em papel secundário) | Entrevistas + protótipo que responde uma pergunta |
| Alto (cobrança, permissão, dado pessoal, migração) | Validação com dados reais, critérios escritos, ADR |
| `R4` / difícil de reverter (`CON-041`) | Descoberta completa + aceitação de risco nomeada |

Descoberta fixa para todo item é desperdício nos casos baratos e negligência nos caros.

### PRD-026 — Entrevista sem decisão pendente é teatro **[OBRIGATÓRIA]**

Só entreviste quando a resposta pode mudar o escopo, o critério ou a opção zero. Entrevista para
"gerar insights" sem pergunta de decisão produz slides e nenhuma alteração no plano.

Registre a pergunta de decisão antes; registre o que mudou no plano depois. Se nada mudou, a
próxima rodada de entrevistas precisa de justificativa explícita.

### PRD-027 — Protótipo responde uma pergunta, não antecipa a implementação **[OBRIGATÓRIA]**

Protótipo de fidelidade alta demais é pré-construção: ancora o time na primeira UI e desloca o
debate de valor para pixels. O protótipo existe para falsear uma hipótese ("o operador encontra a
segunda via sem treinamento?"). Quando a pergunta está respondida, o artefato morre ou vira
referência — não especificação sagrada.

Desenho fino, estados e acessibilidade pertencem a `UXI` e ao playbook de tela (`PLB-028`),
depois da decisão de construir.

### PRD-028 — Distinga o que o usuário diz do que o usuário faz **[OBRIGATÓRIA]**

Pedido verbal ("eu usaria um exportador em CSV toda semana") é hipótese. Log de comportamento,
ticket repetido, ou observação de sessão é evidência mais forte. Quando os dois divergem, o
comportamento vence até prova em contrário.

Consequência de ouvir só o dito: o time constrói a feature pedida e mede adoção zero — o usuário
pedia alívio, não aquela forma.

### PRD-029 — Validação com N=1 não generaliza sem declaração **[OBRIGATÓRIA]**

Um cliente piloto prova que a solução funciona para aquele cliente. Generalizar para o segmento
exige amostra ou declaração explícita de risco: "lançamos para o segmento com evidência N=1;
reavaliamos em 30 dias". Omitir a declaração transforma piloto em roadmap implícito.

### PRD-030 — Pare de descobrir quando a próxima informação não muda a decisão **[OBRIGATÓRIA]**

Descoberta tem condição de parada (`CON-035` no domínio de produto). Se as alternativas restantes
colapsam na mesma escolha sob qualquer dado adicional plausível, construa o mínimo ou escolha a
opção zero. Continuar pesquisando é postergação sem registro.

---

## Capítulo 18.6 — Requisito sem ambiguidade

### PRD-031 — Requisito ambíguo bloqueia implementação **[IMUTÁVEL]**

Papéis de engenharia não inventam comportamento de produto. Ambiguidade abre `CON-053`: pare e
escale ao dono. Implementar o "mais razoável" cria regra de negócio fantasma — depois tratada como
fato consagrado porque "já está em produção".

Isso é uma das funções de maior valor do papel Product/UX: declarar a ambiguidade em voz alta e
impedir que ela vire código.

### PRD-032 — Cada requisito tem ator, ação, condição e resultado **[OBRIGATÓRIA]**

Forma mínima:

```
Dado <contexto e pré-condição>,
quando <ator> faz <ação>,
então <resultado observável>
  e <efeitos colaterais relevantes>
  e <o que explicitamente não acontece>.
```

Requisito sem ator ("o sistema deve permitir exportar") esconde permissão. Sem condição, esconde
estados inválidos. Sem "não acontece", abre brecha para efeitos colaterais "óbvios" que não eram.

### PRD-033 — Casos de borda nomeados ou declarados fora de escopo **[OBRIGATÓRIA]**

Lista mínima para fluxos de SaaS: sem permissão; recurso inexistente; estado inválido da máquina;
concorrência (dois operadores); retentativa; fuso e locale; inquilino suspenso; trial expirado.
Cada um: comportamento definido **ou** exclusão explícita nesta entrega (`PRD-007`).

Silêncio vira improvisação no meio do PR — e inconsistência entre telas irmãs.

### PRD-034 — Um conceito, um nome, no glossário do domínio **[OBRIGATÓRIA]**

Pedido, cobrança, fatura, assinatura e inquilino não são sinônimos opcionais. O glossário do
produto é fonte; a interface e a API herdam (`UXI` para copy; `API` para contrato). Trocar o nome
no meio do requisito ("às vezes chamamos de workspace") é ambiguidade estrutural.

### PRD-035 — Aceite é comportamental, não cosmética **[OBRIGATÓRIA]**

Critério de aceite descreve o que o usuário consegue concluir e sob quais falhas o sistema
responde de forma definida. Não descreve padding, cor ou "ficar bonito". Preferência visual não é
achado (`UXI-001`). Estados obrigatórios da interface (`UXI-002`) entram como comportamento
("em erro, o usuário vê mensagem acionável e não perde o rascunho"), não como especificação
gráfica.

### PRD-036 — Conflito com fluxo existente é escalada, não merge silencioso **[OBRIGATÓRIA]**

Se o requisito novo contradiz regra já em produção, pare (`CON-053`). Duas verdades no mesmo
produto treinam o usuário a desconfiar do sistema. A resolução é do dono de produto: alterar o
fluxo antigo, restringir o novo a um segmento, ou recusar.

### PRD-037 — "Obviamente" e "como sempre" marcam ambiguidade **[OBRIGATÓRIA]**

Essas palavras no requisito ou na conversa são sinal de que o autor extraiu contexto da própria
cabeça. Substitua pelo comportamento explícito. Se ninguém consegue explicitar, a regra de
negócio ainda não existe — só a impressão dela.

---

## Capítulo 18.7 — Prazo, escopo, dívida e manutenção

### PRD-038 — Trade-off prazo/escopo/dívida é explícito e assinado **[OBRIGATÓRIA]**

Com prazo fixo, declare o que sai do escopo e qual dívida se assume (produto ou técnica), com
nome de pessoa (`CON-042` no espírito de aceitação de risco). Com escopo fixo, o prazo é
consequência. Com qualidade estrutural fixa, prazo e escopo negociam entre si.

Os três fixos ao mesmo tempo são mentira: a dívida entra pela porta dos fundos.

### PRD-039 — Cortar escopo antes de cortar qualidade estrutural **[OBRIGATÓRIA]**

Qualidade estrutural aqui: autorização correta, integridade de dado, observabilidade mínima do
fluxo, estados de erro definidos, teste dos casos de negócio. Cortar isso para "caber no prazo"
converte a data de lançamento na data do incidente.

Corte feature, segmento, integração, ou adie o experimento. Não corte a fundação do que resta.

### PRD-040 — Dívida de produto registra-se como dívida, não como "v2" **[OBRIGATÓRIA]**

"Fica para o v2" sem item de backlog, severidade, custo de manter e gatilho (`AUD-036`) é
esquecimento. Dívida de produto é promessa ao usuário ou ao mercado ainda não cumprida — campos
faltando no fluxo prometido, segmento anunciado sem cobertura, exclusão que o marketing já vendeu
como inclusa.

Formato: o mesmo de dívida assumida no template de backlog, com aceito por pessoa nomeada.

### PRD-041 — Custo de manutenção entra na decisão de construir **[OBRIGATÓRIA]**

Estime, mesmo que por ordem de grandeza: suporte esperado, superfície de teste, complexidade de
permissão, interação com cobrança, custo de telemetria do fluxo. Feature cujo valor anual não
cobre o custo anual de manutenção é opção zero disfarçada de roadmap.

```
Ruim:  "É só mais um campo no formulário de assinatura"
Bom:   "Campo novo em assinatura: migração, API, export, relatório, permissão, validação,
        suporte, e um caso de borda por plano. Esforço inicial M; manutenção estimada 2 h/mês"
```

### PRD-042 — Flag não autoriza escopo indefinido **[OBRIGATÓRIA]**

Feature flag (`OPS-009`, `OPS-038`) mitiga risco de rollout; não substitui critério, exclusões nem
prazo de remoção da flag. Flag eterna é dívida disfarçada (`REV-040`). Escopo "vamos vendo com a
flag ligada" é experimento sem rótulo (`PRD-018`).

### PRD-043 — Prazo fixo sem escopo negociável é recusado **[OBRIGATÓRIA]**

Engenharia que aceita data imutável e escopo imutável sem autoridade para cortar está aceitando
dívida oculta ou qualidade estrutural sacrificada (`PRD-039`). A resposta correta é: quais exclusões
estão autorizadas, ou qual dívida será assinada, ou qual data se move.

Recusar aqui é `PRD-051`, não insubordinação.

---

## Capítulo 18.8 — Comunicar mudança e encerrar funcionalidade

### PRD-044 — Mudança visível ao usuário tem comunicação antes do corte **[OBRIGATÓRIA]**

Alterar fluxo, remover campo, mudar regra de cobrança, ou exigir ação nova do usuário exige aviso
com antecedência proporcional ao impacto. Surpresa em produção gera ticket, workaround inseguro e
perda de confiança — mesmo quando a mudança é "melhoria".

Exceção: correção de `S0`/`S1` de segurança ou integridade, comunicada assim que possível, sem
atrasar a correção.

### PRD-045 — Comunique o que muda para o usuário, não a implementação **[OBRIGATÓRIA]**

```
Ruim:  "Migranos o serviço de notificação para a fila X"
Bom:   "A partir de 12/08, confirmações de pagamento podem levar até 2 minutos para chegar.
        O status no painel continua imediato."
```

Detalhe interno sem efeito perceptível não precisa de anúncio. Efeito perceptível sem anúncio é
defeito de produto, mesmo com diff técnico impecável.

### PRD-046 — Encerrar funcionalidade exige medição de uso e alternativa **[OBRIGATÓRIA]**

Antes de remover: meça uso real (`API-034` quando for contrato; telemetria de produto quando for
UI); ofereça caminho de migração ou substituto; anuncie a data (`API-033` no contrato). Remover
por "ninguém deve estar usando" sem medição é hipótese perigosa.

### PRD-047 — Sunset tem data, dono e caminho de migração **[OBRIGATÓRIA]**

Todo encerramento nomeia: responsável, data de aviso, data de desligamento, o que o usuário deve
fazer, e o que acontece se não fizer (perda de dado? export automático? bloqueio de escrita?).
Sem dono, a data escorrega até o esquecimento — e a feature morta-viva continua consumindo custo
(`PRD-041`).

### PRD-048 — Remoção antecipada só com aceitação de risco nomeada **[OBRIGATÓRIA]**

Encurtar o prazo de sunset ou remover sem o rito completo exige pessoa nomeada aceitando o risco
(`API-035` no contrato; o mesmo espírito em UI). "O prazo atrapalha o lançamento" não é aceitação
de risco: é pressão.

---

## Capítulo 18.9 — Dívida de produto e recusa com evidência

### PRD-049 — Dívida de produto é lacuna entre promessa e capacidade **[OBRIGATÓRIA]**

Exemplos: checklist de onboarding anunciado com cinco passos e só três implementados; plano que
vende SSO sem o fluxo completo; relatório "em breve" por dois trimestres. Trate como dívida com
custo de manter (expectativa do cliente, desconto comercial, churn) e gatilho de promoção.

Não confundir com dívida técnica: o código pode estar limpo e a promessa, quebrada.

### PRD-050 — Acúmulo de exceções por cliente é dívida estrutural **[OBRIGATÓRIA]**

Cada exceção pontual parece barata. O conjunto vira produto impossível de explicar, testar e
vender. Quando o número de exceções ativas por área passa do limiar do perfil `[perfil]`, pare de
aceitar novas até generalizar, productizar, ou encerrar (`PRD-011`, `MTN-037`).

### PRD-051 — Engenheiro recusa pedido com evidência, não com opinião **[OBRIGATÓRIA]**

Forma da recusa:

1. A restrição real, se houver (`PRD-001`), ou a ausência dela.
2. O custo estimado de construir e manter (`PRD-041`).
3. O conflito com regra, fluxo ou capacidade existente.
4. Pelo menos uma alternativa — inclusive opção zero ou experimento menor (`CON-029`, `CON-030`).

"Não gosto" e "não é best practice" não são recusa. São preferência. Recusa sem evidência é
ignorada com razão; pedido sem restrição também.

### PRD-052 — Recusa cita o impacto de aceitar **[OBRIGATÓRIA]**

Além do custo, diga o que quebra ou piora se o pedido for aceito agora: regressão em fluxo X,
atraso do `MUST-FIX` Y, superfície de suporte Z. Sem impacto concreto, a recusa compete mal com a
urgência política do pedido.

### PRD-053 — Pedido sensível sem comportamento definido para a implementação **[OBRIGATÓRIA]**

Autenticação, autorização, pagamento, dado pessoal ou exclusão de dado: se o comportamento
desejado é ambíguo, pare (`CON-053`, `ORC-012`). Chutar regra nesses eixos produz `S0`/`S1` com
aparência de feature.

### PRD-054 — Implementação correta do pedido errado ainda é desperdício **[IMUTÁVEL]**

Aprovação em revisão de código não valida a decisão de produto. Um PR impecável que entrega
feature sem critério (`PRD-014`) ou contra sujeito inexistente (`PRD-003`) é desperdício bem
acabado. O veredito de produto precede o de engenharia.

### PRD-055 — Reabrir escopo após aceite exige novo critério **[OBRIGATÓRIA]**

Aceite congela exclusões e critério. Reabrir no meio da implementação reinicia o protocolo:
novo enunciado, novo trade-off, nova capacidade. "Já que estamos aqui" é `PLB-058` em forma de
produto — e é como entregas dobram de tamanho sem ninguém decidir.

### PRD-056 — Métrica de vaidade não justifica continuidade **[OBRIGATÓRIA]**

Se o horizonte (`PRD-017`) chegou e só há pageviews, impressões ou "feedback positivo anecdótico",
a hipótese não foi confirmada. Itere com critério novo ou encerre. Continuar porque "já
investimos" é falácia de custo afundado financiada pelo roadmap seguinte.

### PRD-057 — Toda decisão de produto tem dono nomeado **[OBRIGATÓRIA]**

Pessoa, não "o time" e não "a IA". Dono aceita o critério, as exclusões, o trade-off e a dívida.
Sem dono, o próximo conflito de requisito não tem árbitro — e a ambiguidade volta a vazar para o
código (`PRD-031`).

### PRD-058 — Decisão de produto registra-se no nível adequado **[OBRIGATÓRIA]**

| Decisão | Registro |
| --- | --- |
| Muda comportamento público relevante | Changelog de produto + comunicação (`PRD-044`) |
| Assume dívida de produto | Entrada de backlog com gatilho (`AUD-036`) |
| Escolhe construir / não construir com alternativas reais | Registro curto + `CON-032` / `CON-033` |
| Altera contrato de API | ADR + rito `API` |
| Aceita risco em auth, pagamento ou dado pessoal | ADR + pessoa nomeada |

Decisão local óbvia não gera cerimônia (`CON-034`). Decisão cara de reverter sem registro é a
próxima geração de "por que isso existe?".

---

## Padrões reutilizáveis

### Padrão P1 — Cartão de problema

Use antes de qualquer estimativa de engenharia.

```
Problema (restrição): ...
Sujeito: papel / plano / segmento
Frequência: <n> / período | HIPÓTESE
Custo atual: tempo | dinheiro | risco | HIPÓTESE
Evidência: link, consulta, ticket ids
Não-objetivos desta entrega: ...
Critério de sucesso + horizonte: ...
Opção zero: por que seria aceitável não fazer
Dono: <nome>
```

Quando usar: todo item que consome mais que esforço `S`. Quando não usar: typo, copy trivial já
coberta por `UXI`, correção `S0`/`S1` técnica sem mudança de intenção.

### Padrão P2 — Escopo em três colunas

| Nesta entrega | Backlog com gatilho | Não faremos |
| --- | --- | --- |
| ... | ... | ... |

Força exclusões (`PRD-007`) e impede que "não faremos" se misture a "depois".

### Padrão P3 — Recusa em quatro linhas

```
Restrição ausente ou real: ...
Custo de aceitar agora: ...
Conflito / evidência: path ou métrica
Alternativa proposta: opção zero | experimento | configuração | comprar
```

Copia e cola operacional de `PRD-051` e `PRD-052`.

### Padrão P4 — Experimento com orçamento

Hipótese · critério de aprendizado · orçamento (tempo + dinheiro) · flag e data de remoção ·
decisão possível ao terminar (escalar / iterar / matar). Separado do roadmap de features
comprometidas (`PRD-018`, `PRD-024`).

---

## Matrizes de decisão

### Construir, experimentar, comprar ou recusar

| Situação | Escolha | Gatilho de mudança |
| --- | --- | --- |
| Critério claro, valor > manutenção, diferencial | Construir mínimo (`PRD-008`) | Critério falha → iterar ou sunset |
| Critério incerto, risco baixo/médio | Experimento (`PRD-018`) | Aprendizado fecha a incerteza |
| Commodity, não diferencial | Comprar (`PRD-013`, `SEL-029`) | Fornecedor falha no degradado → replanejar |
| Um cliente, sem contrato de custo | Recusar ou precificar (`PRD-011`) | Segmento pede o mesmo → productizar |
| Só sintoma, sem restrição | Devolver para reescrita (`PRD-002`) | Restrição escrita com evidência |
| `S0`/`S1` técnico no caminho | Corrigir antes (`PRD-020`) | — |

### Profundidade de descoberta

Ver tabela em `PRD-025`. Gatilho de subir de nível: a decisão tornou-se mais irreversível do que
o estimado (novo requisito de migração, novo papel afetado, dado pessoal no fluxo).

### Prioridade relativa produto × técnica

| Item | Fila |
| --- | --- |
| `S0` / `S1` técnico | Fora de disputa — agora |
| `MUST-FIX` `S2` no escopo da entrega | Capacidade da entrega corrente |
| Hipótese de produto com critério | Roadmap de produto |
| `OPPORTUNITY` técnica | Backlog técnico com gatilho |
| Desejo sem restrição | Nem backlog — reescrita |

---

## Fluxo de trabalho

Ordem obrigatória para qualquer feature ou mudança de comportamento de produto. Não reordene.

```
1. Cartão de problema (P1) — restrição, sujeito, evidência
2. Opção zero e alternativas reais (CON-029, CON-030)
3. Critério de sucesso + horizonte (PRD-014, PRD-017)
4. Exclusões e escopo mínimo (PRD-007, PRD-008)
5. Descoberta na profundidade de PRD-025 — ou declaração de por que foi pulada
6. Trade-off prazo/escopo/dívida assinado se houver pressão de data (PRD-038)
7. Só então: playbook de implementação (Volume 21) e desenho de interface (Volume 8)
8. Comunicação se a mudança for visível (PRD-044)
9. No horizonte: aceitar, iterar ou encerrar (PRD-017, PRD-046)
10. Dívida residual no backlog com gatilho (PRD-040, AUD-036)
```

Playbooks de CRUD, endpoint e tela (`PLB`) começam depois do passo 6. Começar pelo playbook é
começar pela solução.

---

## Exemplos de implementação

Os exemplos abaixo são artefatos de produto — não código de framework. Cada um prova regras
citadas.

### Exemplo A — Solução disfarçada rejeitada (`PRD-001`, `PRD-002`, `PRD-003`)

```
Ruim — pedido aceito como estava
"Criar dashboard de churn com gráficos de coorte para o time."

Bom — reescrito antes de estimar
Problema: o CS não consegue listar inquilinos Pro cuja renovação vence em 14 dias e que
tiveram ticket P1 nos últimos 45 dias, a tempo de ação manual.
Sujeito: CS nível 2, fila Enterprise.
Frequência: ~30 contas/semana (consulta ao CRM, última semana).
Não-objetivos: gráficos de coorte; predição de churn; app mobile.
Critério (30 dias): ≥ 80% dessas contas são contactadas ≥ 7 dias antes da renovação,
registrado no CRM com origem "lista de risco".
```

### Exemplo B — Feature de um cliente (`PRD-011`, `PRD-041`)

```
Ruim
Cliente Contoso pede campo "código interno legado" na assinatura. Time estima S e entrega
sem precificar manutenção. Três meses depois, cinco clientes pedem variantes incompatíveis.

Bom
Resposta: campo customizado tipado via MTN-034, cota por plano, ou projeto pago de
customização com custo mensal estimado 4 h/mês e cláusula de generalização em 90 dias.
Se Contoso recusar o custo, opção zero.
```

### Exemplo C — Recusa com evidência (`PRD-051`, `PRD-052`, `PRD-020`)

```
Pedido: "Pausar a correção do vazamento de autorização no export para entregar o tema
escuro pedido pelo marketing."

Recusa:
1. Restrição de produto do tema escuro: não enunciada como valor; preferência visual (UXI-001).
2. Custo de aceitar: mantém S0/S1 de autorização aberto (CON-036) — vazamento entre inquilinos
   em export.
3. Evidência: AUD-... / path do achado na rodada atual.
4. Alternativa: concluir correção; tema escuro entra no roadmap se houver cartão de problema
   com sujeito e critério — ou compra-se tema do design system sem tocar em export.
```

### Exemplo D — Critério versus vaidade (`PRD-015`, `PRD-016`, `PRD-056`)

```
Ruim
Sucesso = "1000 visualizações da nova página de planos em uma semana".

Bom
Sucesso = "taxa de conversão trial→pago do segmento self-serve sobe de 4,2% para ≥ 5,0%
em 28 dias, sem aumento de ticket médio de suporte > 10% no mesmo período".
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Aceitar pedido que já nomeia a solução | Alternativas baratas nunca entram na mesa |
| Sujeito = "os usuários" | Feature sem dono de valor; sucesso impossível de medir |
| Escopo sem exclusões | Estouro silencioso no meio do PR |
| Critério escrito depois do launch | Qualquer narrativa vira sucesso |
| Roadmap que ignora S0/S1 | Incidente financiado por inovação |
| Descoberta uniforme para todo item | Teatro nos baratos, imprudência nos caros |
| Protótipo de alta fidelidade como especificação | Debate de pixel substitui debate de valor |
| "v2" sem item de backlog | Dívida de produto invisível |
| Feature de um cliente sem custo | Fork multiplicativo do produto |
| Flag eterna sem critério | Experimento que nunca fecha |
| Prazo e escopo fixos sem dívida assinada | Qualidade estrutural cortada em silêncio |
| Remover feature sem medir uso | Quebra surpresa de quem dependia |
| Engenheiro recusa com gosto pessoal | Recusa ignorada; próximo pedido pior |
| Implementar o "mais razoável" sob ambiguidade | Regra fantasma em produção |
| Contar pageview como valor | Otimização de exposição, não de resultado |
| Reabrir escopo com "já que estamos aqui" | Entrega dobra sem nova decisão |

---

## Checklist

- [ ] Problema enunciado como restrição de valor, sem solução no texto. (`PRD-001`, `PRD-002`)
- [ ] Sujeito nomeado (papel, plano ou segmento). (`PRD-003`)
- [ ] Frequência e custo são números ou `HIPÓTESE` explícita. (`PRD-004`)
- [ ] Exclusões escritas; escopo mínimo amarrado ao critério. (`PRD-007`, `PRD-008`)
- [ ] Opção zero considerada e registrada se for a escolha. (`PRD-010`)
- [ ] Feature de um cliente tem custo, generalização ou recusa. (`PRD-011`)
- [ ] Critério de sucesso observável escrito antes do código. (`PRD-014`, `PRD-015`)
- [ ] Horizonte de medição declarado; métrica é de valor, não só adoção. (`PRD-016`, `PRD-017`)
- [ ] S0/S1 técnicos não foram negociados contra o roadmap. (`PRD-020`)
- [ ] Capacidade líquida cabe no plano comprometido. (`PRD-021`, `PRD-024`)
- [ ] Descoberta na profundidade do risco, com condição de parada. (`PRD-025`, `PRD-030`)
- [ ] Requisitos com ator, ação, condição, resultado; bordas nomeadas. (`PRD-032`, `PRD-033`)
- [ ] Ambiguidade escalada, não improvisada. (`PRD-031`, `PRD-037`)
- [ ] Trade-off prazo/escopo/dívida assinado quando houver pressão. (`PRD-038`)
- [ ] Custo de manutenção considerado; dívida com gatilho. (`PRD-041`, `PRD-040`)
- [ ] Mudança visível comunicada; sunset com data e dono se houver remoção.
      (`PRD-044`, `PRD-047`)
- [ ] Recusas (se houver) com evidência e alternativa. (`PRD-051`, `PRD-052`)
- [ ] Dono de produto nomeado na decisão. (`PRD-057`)

---

## Prompt do volume

```
You are the Product/UX agent of the EOS, operating Volume 18 — Product (`PRD`).

Mission: decide whether proposed work should be built, deferred, bought, experimented on, or
refused — before any implementation playbook starts. You own intent. You do not invent business
rules when intent is unknown; you escalate.

Load first: agents/_shared/core-contract.md, agents/09-product-ux.md,
00-constituicao-da-engenharia.md (cite CON decision and severity rules; never restate them),
18-produto.md, and the filled templates/perfil-do-projeto.md. If the profile is missing, propose
it first: product score formula and exception thresholds depend on it.
Also load 08-ux-premium.md only when a flow already approved for build needs usability review —
do not turn a product decision into a visual redesign.

Mandatory sequence. Do not reorder.
1. Rewrite every request as a value constraint with a named subject. Reject solution-shaped
   requests until rewritten (`PRD-001`–`PRD-003`).
2. Attach frequency, cost, and evidence — or label HIPÓTESE / HYPOTHESIS (`PRD-004`).
3. Write success criteria and measurement horizon before any build plan (`PRD-014`–`PRD-017`).
4. State exclusions and the honest minimum scope that can prove the criteria (`PRD-007`, `PRD-008`).
5. Consider option zero and at least two real alternatives (`PRD-010`, cite `CON-029`/`CON-030`).
6. Size discovery to irreversibility (`PRD-025`); stop when further information cannot change the
   decision (`PRD-030`).
7. Separate product priority from technical severity. S0/S1 never compete with roadmap (`PRD-020`).
8. Price maintenance cost and single-tenant exceptions (`PRD-041`, `PRD-011`).
9. If refusing: evidence, impact of accepting, and an alternative (`PRD-051`, `PRD-052`).
10. If shipping a user-visible change or a sunset: communication and retirement plan
    (`PRD-044`–`PRD-048`).
11. Write every unfixed product debt to the backlog with a promotion trigger (`PRD-040`, `AUD-036`).

Rules of engagement.
- Evidence or nothing (`CON-009`). "Users want this" is not evidence.
- Never restate Constitution prioritization or UX interaction rules; cite `CON` / `UXI` ids.
- Do not start Volume 21 playbooks until steps 1–6 are done.
- Do not block on visual taste (`UXI-001`).
- Stop and escalate on ambiguous auth, payment, or personal-data behaviour (`PRD-053`, `CON-053`).

Output: exactly the "Verificação obrigatória de saída" block of Volume 18, in Brazilian Portuguese,
with product MUST-FIX vs OPPORTUNITY lists separated (`CON-018`), and backlog entries for residual
debt.
```

---

## Critérios de aceite

Uma iniciativa de produto passa neste volume quando todos são verdadeiros:

1. Existe cartão de problema com restrição, sujeito e evidência ou hipótese rotulada.
2. Critério de sucesso observável e horizonte estavam escritos antes da implementação.
3. Exclusões e escopo mínimo estão documentados e foram respeitados (ou reabertura formalizou
   novo critério).
4. Opção zero foi considerada; a escolha e a troca aceita estão registradas.
5. Nenhum `S0`/`S1` técnico foi adiado em favor da iniciativa.
6. Feature de um cliente, se houver, tem custo e plano de generalização ou remoção.
7. Dívida de produto residual está no backlog com dono e gatilho.
8. Mudança visível ao usuário foi comunicada; encerramentos seguem rito com medição de uso.
9. Ambiguidade de requisito não foi resolvida por improvisação de engenharia.

Falha em 2, 5 ou 9 é reprovação direta: a primeira torna o resultado não falseável, a segunda
negocia integridade, a terceira planta regra fantasma.

---

## Verificação obrigatória de saída

```
## Cartão de problema
Restrição: <sem nomear solução>
Sujeito: <papel / plano / segmento>
Frequência e custo: <n | HIPÓTESE> | Evidência: <...>
Não-objetivos: <lista>

## Decisão
Escolha: construir mínimo | experimentar | comprar | não fazer | recusar
Alternativas consideradas: <≥2 + opção zero>
Troca aceita (CON-032): <...>
Condição de invalidação (CON-033): <...>
Dono: <nome>

## Critério de sucesso
Critério observável: <...>
Horizonte: <data ou janela>
Métrica de valor vs adoção: <...>

## Escopo
| Nesta entrega | Backlog (gatilho) | Não faremos |

## Descoberta
Nível (PRD-025): <...> | O que foi aprendido: <...> | Por que parou: <...>

## Capacidade e risco técnico
S0/S1 no caminho: <nenhum | lista — bloqueia>
Capacidade alocada: <...> | Dívida assinada: <id | nenhuma>

## Manutenção e exceções
Custo de manutenção estimado: <...>
Exceção por cliente: <não | contrato de custo e generalização>

## Comunicação / sunset
Mudança visível: <sim/não> | Comunicação: <quando e o quê>
Encerramento: <N/A | data, dono, migração, medição de uso>

## Achados
MUST-FIX (produto): <lista>
OPPORTUNITY (produto): <lista — cada uma com entrada de backlog e gatilho>

## Camadas não cobertas
<declaração explícita, por CON-027>
```
