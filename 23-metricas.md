# 📗 Volume 23 — Métricas

Prefixo: `MET` · Regras: MET-001 a MET-058 · Papel: [Orquestrador](agents/00-orchestrator.md)

Um time pode ter cobertura alta, pipeline verde e um painel com vinte gráficos — e ainda assim não
saber se a engenharia está melhorando. O número existe; a decisão não. Alguém sobe cobertura
apagando asserções. Outro reduz cycle time abrindo PRs incompletos. Um terceiro reporta MTTR baixo
porque conta só o tempo de hotfix, não o tempo até o cliente voltar a operar. Todos os números
melhoraram. O produto piorou.

Esse é o erro caro que este volume previne: **confundir instrumento de gestão com decoração de
status, e confundir proxy fácil de medir com a qualidade que o proxy deveria representar.** A
constituição já exige limiar, reação e antipadrão (`CON-050`), separa o que bloqueia do que apenas
aponta (`CON-051`), e fixa os pesos da nota (`CON-052`, `AUD-027`). Este volume não os repete: ele
ensina a desenhar, defender e matar métricas de engenharia sem cair em Goodhart, vigilância ou no
painel que ninguém abre.

O que muda no trabalho de quem lê: toda métrica nova nasce com quatro campos preenchidos; toda
métrica viva tem dono e data da última reação; toda métrica morta é removida; e nenhum número isolado
justifica ranquear pessoas ou refatorar código.

**Fronteira.** É deste volume: a anatomia de uma métrica útil de qualidade de engenharia; Goodhart e
gamificação; tendência versus absoluto e baseline; o que métricas de código medem e o que
explicitamente não medem; métricas de processo (cycle time, tamanho de PR, tempo de revisão,
frequência de deploy, CFR, MTTR) e de defeito; produto que a engenharia precisa para decidir; limiares
de a11y e performance como portões de qualidade; nota por dimensão e o perigo da agregação que
esconde; vigilância versus instrumentação; o que nunca coletar; higiene de painéis de engenharia.

**Não é deste volume:** telemetria de produção do sistema — log, trace, métrica de serviço, SLI/SLO,
alerta e custo de telemetria (→ [17](17-observabilidade.md), fundação em [10](10-devops.md)). Como
medir gargalo e limiares de latência no código (→ [07](07-performance.md)). Como escrever e cobrir
testes (→ [11](11-qa.md)). Como atribuir nota e veredito numa auditoria (→ [12](12-auditoria.md)).
Como decidir *se* construir uma funcionalidade (→ [18](18-produto.md), quando existir). Os limiares
canônicos da tabela de `CON-050` vivem na constituição; aqui se aprofunda o *como* operar com eles.

---

## Fundamentos

**Uma métrica é um contrato de decisão, não um número.** O número sem definição operacional é
ambíguo. Sem limiar é ruído. Sem reação é decoração (`CON-050`). Sem dono é órfão: quando estoura,
ninguém age e o estouro vira normalidade. Os quatro campos — definição, limiar, reação, dono — são
a unidade mínima. Menos que isso não entra no painel.

**Goodhart não é exceção; é o estado estacionário.** Toda métrica usada como meta deixa de ser boa
medida do que pretendia. Cobertura vira meta e nasce teste sem asserção (`QAT-002`, `QAT-040`).
Velocidade vira meta e nasce ponto inflado. Deploy frequente vira meta e nasce deploy vazio. O
desenho correto assume a corrupção e escolhe proxies difíceis de jogar, ou combina sinais que se
anulam quando alguém otimiza um só.

**Tendência sem baseline é conversa; absoluto sem contexto é pânico.** Um cycle time de quatro dias
é excelente para um módulo regulado e péssimo para um ajuste de copy. A pergunta útil quase sempre é
"melhorou ou piorou na mesma definição, na mesma janela?", não "qual o número mágico universal?".

**Instrumentação do processo não é vigilância do indivíduo.** Medir o sistema (fila de PRs, taxa de
escape, tempo até recuperação) melhora o fluxo. Medir a pessoa (LOC/dia, commits/semana, horas online)
produz teatro e esconde o defeito estrutural. A linha divisória é: o número muda uma prática do
sistema, ou muda o comportamento de quem sabe que está sendo ranqueado?

**Agregação é a ferramenta favorita de quem quer esconder.** Uma nota 8,5 composta de segurança 3 e
UX 10 é fraude estatística. Os pesos (`CON-052`, `AUD-027`) e as travas (`AUD-030`) existem porque a
média mente. Este volume trata a nota como vetor de dimensões com travas — nunca como um único
escalar de marketing interno.

**O programa de métricas compete com o produto pelo tempo do time.** Cada série temporal que ninguém
consulta, cada OKR de proxy fácil e cada leaderboard de commits custa atenção que não vai para
defeito real. Por isso matar métrica é trabalho de primeira classe — não higiene opcional de fim de
trimestre. Um programa menor e obedecido supera um programa completo e ignorado: o segundo treina
todos a tratar vermelho como papel de parede.

---

## Capítulo 23.1 — Anatomia de uma métrica útil

### MET-001 — Uma métrica útil tem definição, limiar, reação e dono **[IMUTÁVEL]**

Os quatro campos são obrigatórios na criação. Ausência de qualquer um invalida a métrica: ela não
pode aparecer em painel, relatório ou meta de time. Isso aprofunda `CON-050` — a constituição exige
limiar, reação e antipadrão; aqui o contrato completo inclui definição operacional e dono nomeado,
porque sem eles a reação não tem sujeito e o limiar não tem fórmula.

```
Ruim:  "acompanhamos cycle time"
Bom:   Cycle time = tempo entre primeiro commit da branch e deploy em produção (excluindo
       branches abandonadas > 14 dias). Limiar: p50 < [perfil] e p90 < [perfil]. Reação:
       se p90 sobe > 20% em 14 dias, o dono do fluxo abre post-mortem de fluxo em 5 dias úteis.
       Dono: lead de entrega do domínio Pedidos.
```

### MET-002 — Definição é fórmula, unidade e denominador **[OBRIGATÓRIA]**

"Taxa de erro", "cobertura" e "MTTR" sem fórmula são rótulos. A definição declara: numerador,
denominador, unidade, o que entra e o que fica de fora. Dois times com o mesmo rótulo e denominadores
diferentes não estão medindo a mesma coisa — e qualquer comparação entre eles é inválida.

A consequência de omitir o denominador é clássica: "reduzimos bugs em 40%" porque o time lançou
menos features, não porque a qualidade subiu. Sem denominador estável (releases, PRs, sessões,
requisições), o numerador é teatro.

### MET-003 — Limiar declara valor, janela e direção **[OBRIGATÓRIA]**

Limiar sem janela ("p95 < 300 ms") não diz se vale para a última hora, o último deploy ou o último
mês. Limiar sem direção não diz se subir é bom ou ruim. Todo limiar neste volume usa o formato:
valor · janela · direção · se bloqueia.

Valores marcados `[perfil]` vêm do perfil do projeto; na ausência de perfil preenchido, valem os
padrões de `CON-050` até alguém ajustar por escrito. Ajustar limiar para caber o status atual, sem
aceitação de risco, é fraude — não calibração.

### MET-004 — Reação nomeia ação, prazo e gatilho **[OBRIGATÓRIA]**

"Investigar" não é reação. Reação é: quem faz o quê até quando, quando o limiar é cruzado. Sem prazo,
a métrica estoura e o estouro vira o novo normal. Sem ação concreta, o alerta de engenharia sofre a
mesma fadiga que o alerta de produção (`OBS-060` no domínio vizinho).

| Gatilho | Reação mínima aceitável |
| --- | --- |
| Limiar de bloqueio cruzado | Impede merge/deploy até correção ou aceitação `CON-042` |
| Limiar de investigação | Item com dono e prazo ≤ [perfil, padrão 5 dias úteis] |
| Tendência adversa > [perfil, padrão 20%] | Análise escrita; não "vamos olhar" |

### MET-005 — Toda métrica tem dono humano nomeado **[OBRIGATÓRIA]**

Dono é pessoa ou papel com autoridade para agir sobre a reação — não um canal Slack. Métrica sem
dono é a que aparece no relatório trimestral e some do backlog na segunda-feira. Quando o dono muda
de time, a transferência é explícita; métrica órfã por mais de um ciclo de relatório é candidata a
remoção (`MET-058`).

### MET-006 — Antipadrão de uso é declarado na criação **[OBRIGATÓRIA]**

Toda métrica nova responde, no registro: "como alguém vai jogar este jogo?". Se a resposta for
"inflar o denominador", "omitir casos", "dividir o PR em dez commits vazios", o desenho muda antes da
coleta — ou a métrica não nasce como meta, só como indicador de tendência (`MET-009`).

---

## Capítulo 23.2 — Goodhart e gamificação

### MET-007 — Toda métrica usada como meta se corrompe; desenhe sabendo disso **[IMUTÁVEL]**

Goodhart não é risco residual: é previsível. Se a métrica é meta de avaliação individual ou de
bônus, assuma que o comportamento vai otimizar o número, não o resultado. A mitigação não é moral —
é desenho: proxies difíceis de falsear, combinação de sinais opostos, e proibição de meta única.

A constituição já separa o que bloqueia do que apenas aponta (`CON-051`) precisamente por isso. Este
volume estende: **mesmo métricas de correção se corrompem** se virarem ranking de pessoa. Bloquear
merge por `S0` aberto é controle. Ranquear engenheiros por "bugs fechados/semana" é jogo.

### MET-008 — Meta composta de um único proxy fácil é proibida **[OBRIGATÓRIA]**

Proibido: "meta do trimestre = cobertura ≥ 80%". Proibido: "meta = story points". Proibido: "meta =
número de PRs". Proxy único e barato de falsear garante falseamento. Meta legítima combina pelo
menos dois sinais que se tensionam — por exemplo, frequência de deploy **e** CFR; cycle time **e**
taxa de escape; cobertura de casos de negócio (`QAT-017`) **e** reincidência zero (`QAT-031`).

### MET-009 — Indicador de tendência não vira meta individual **[OBRIGATÓRIA]**

Complexidade, arquivos por mudança, LOC, churn de arquivo e "saúde" de repositório são indicadores
de onde olhar. Transformá-los em meta de pessoa ou de squad produz o pior tipo de refatoração: a que
move o número e não o risco (`CON-013`, `CON-051`).

### MET-010 — Gamificação detectada invalida o período **[OBRIGATÓRIA]**

Se a investigação mostra que o número melhorou por jogo (teste sem asserção, PR cosmétique, deploy
vazio, reclassificação de severidade), o período é marcado inválido no relatório e a métrica é
redesenhada ou rebaixada a indicador. Continuar reportando o número como sucesso é `AUD-002`:
afirmação sem evidência do que a métrica pretendia medir.

---

## Capítulo 23.3 — Tendência, absoluto e baseline

### MET-011 — Tendência supera absoluto até existir baseline estável **[OBRIGATÓRIA]**

Antes de baseline, o entregável é a série e o método — não o julgamento "bom/ruim". Absolutos
copiados de outro produto ou de blog de DORA sem calibração local viram limiar fictício e geram
pânico ou complacência falsa.

### MET-012 — Baseline declara método, janela e data de congelamento **[OBRIGATÓRIA]**

Baseline não é "a média de sempre". É: janela ≥ [perfil, padrão 4 semanas úteis] · definição
congelada · exclusões documentadas (feriados, incidente maior, migração) · data em que passou a
valer. Mudar a definição reinicia a baseline; comparar séries com definições diferentes é achado
de método, não de performance.

### MET-013 — Divergência entre tendência e absoluto força investigação **[OBRIGATÓRIA]**

Exemplos que exigem análise escrita, não slide: absoluto dentro do limiar mas tendência piorando
três janelas seguidas; absoluto fora do limiar mas tendência melhorando após mudança conhecida;
um percentil estável e outro explodindo. Agregar tudo numa média única esconde exatamente esses
casos (`MET-041`).

### MET-014 — Comparação entre times exige denominador e contexto idênticos **[OBRIGATÓRIA]**

Comparar cycle time de "plataforma" com "growth" sem normalizar por tipo de mudança, criticidade e
tamanho de PR produz ranking político. Se a comparação não sobrevive a `MET-002`, ela não entra em
relatório executivo.

---

## Capítulo 23.4 — Métricas de código — o que não dizem

### MET-015 — Cobertura de linhas não mede qualidade **[IMUTÁVEL]**

A constituição já fixa: cobertura de linhas ≥ 60% `[perfil]` **nunca** bloqueia (`CON-050`);
perseguir percentual é antipadrão (`QAT-002`); não se bloqueia por percentual (`QAT-040`). Este
volume adiciona a consequência operacional: **nenhum relatório de qualidade de engenharia usa
cobertura de linhas como evidência de correção.** Evidência legítima é cobertura de casos de
negócio declarados (`QAT-016`, `QAT-017`) e reincidência (`QAT-031`).

```
Ruim:  "módulo aprovado — cobertura 92%"
Bom:  "módulo aprovado — 14/14 casos de cobrança cobertos; 0 reincidência em 90 dias;
       cobertura de linhas 71% (indicador, não portão)"
```

### MET-016 — Complexidade e cheiros estáticos apontam; não justificam mudança sozinhos **[OBRIGATÓRIA]**

É `CON-051` aplicado: métrica de manutenibilidade não autoriza diff. Complexidade alta + defeito
recorrente + área de mudança frequente = hipótese com evidência. Complexidade alta sozinha =
`OPPORTUNITY` no backlog com gatilho (`AUD-036`), não PR de "limpeza".

### MET-017 — Dívida estática sem defeito, risco ou norma ligada é decoração **[OBRIGATÓRIA]**

Contagem de "code smells", TODOs e avisos de linter só entram no sistema de métricas se cada classe
tiver limiar, dono e ligação a falha real ou a norma citável. Caso contrário, o painel treina o time
a ignorar vermelho — a mesma falha de alerta inútil (`OPS-026`).

### MET-018 — Métricas de código respondem a perguntas de risco, não a ranking **[OBRIGATÓRIA]**

Perguntas legítimas: "quais módulos concentram escape de defeitos?", "quais arquivos mudam em todo
incidente?", "onde a suíte é lenta demais para ser usada (`QAT-027`)?" Perguntas ilegítimas: "quem
escreveu mais linhas?", "quem tem mais avisos?". As ilegítimas violam `MET-048`.

---

## Capítulo 23.5 — Métricas de processo

### MET-019 — Cycle time mede fluxo de valor, não esforço individual **[OBRIGATÓRIA]**

Cycle time = tempo entre início observável do trabalho (primeiro commit da branch ou ticket
"em progresso", escolha uma e congele) e valor disponível em produção. Não inclui "horas digitando".
Otimizar cycle time sem olhar CFR e escape rate produz atalho: PR menor que não termina o trabalho,
feature flag eterna, deploy de no-op (`MET-008`).

Limiar típico: p50 e p90 por classe de mudança (hotfix / feature / mudança de schema), valores
`[perfil]`. Uma única meta para todas as classes é inválida.

Exclua explicitamente branches abandonadas após [perfil, padrão 14 dias] e trabalho pausado por
dependência externa nomeada — senão o p90 é dominado por zumbis e a reação ataca o time errado.
A exclusão entra na definição congelada (`MET-012`), não num filtro ad hoc do relatório.

### MET-020 — Lead time inclui fila; omitir fila falseia o diagnóstico **[OBRIGATÓRIA]**

Se a maior parte do tempo está em "aguardando revisão" ou "aguardando janela de deploy", acelerar
coding é otimizar o trecho errado. Lead time / cycle time devem expor estágios: coding · review ·
CI · waiting for release · production. Sem estágio, a reação ataca o sintoma favorito do time, não
a fila real.

### MET-021 — Tamanho de PR tem limiar alinhado ao orçamento de mudança **[OBRIGATÓRIA]**

O orçamento de PR vive em `AUD-004` / `REV-012`. A métrica de engenharia acompanha a distribuição
(p50/p90 de arquivos e de linhas líquidas) e reage a tendência, não a um PR isolado. Time que vive
acima do orçamento não tem "produtividade alta": tem revisão rasa e regressão (`AUD-018`).

### MET-022 — Tempo de revisão é métrica de fluxo, não de virtude do revisor **[OBRIGATÓRIA]**

Aprofunda `REV-050`: mede-se tempo até primeira resposta humana e tempo até decisão (approve /
changes). Limiar `[perfil]`. Usar a métrica para punir revisores individualmente empurra approve
cego — o jogo clássico. A reação correta ataca fila (WIP de PRs, donos ausentes, PRs acima do
orçamento), não a pessoa.

### MET-023 — Frequência de deploy é sinal de capacidade, não objetivo isolado **[OBRIGATÓRIA]**

Deploy frequente e rotineiro é o alvo de `OPS-037`. Como métrica de engenharia, só vale **em
conjunto** com CFR e MTTR (`MET-026`). Meta de "N deploys/dia" sem os outros dois produz deploy
cerimonial: artefato sobe, comportamento não muda, risco de verdade acumula em releases raras
escondidas atrás de flags sem prazo (`OPS-038`).

### MET-024 — Change failure rate exige definição escrita de falha **[OBRIGATÓRIA]**

CFR = deploys que causam incidente, rollback, hotfix ou feature flag de emergência ÷ deploys no
período — **com a definição de cada termo no perfil**. Sem definição, times reclassificam falha
como "ajuste" e o CFR cai no PowerPoint. Limiar `[perfil]`; cruzar limiar obriga análise de causa
dos falhos do período, não "vamos deployar menos".

### MET-025 — MTTR conta até recuperação do usuário, não até o merge do hotfix **[OBRIGATÓRIA]**

MTTR de engenharia alinha-se ao espírito operacional de `CON-050` (MTTR < 30 min `[perfil]` como
indicador): o relógio para quando o sintoma do usuário cessa — mitigação em produção efetiva — não
quando o PR do fix é aprovado. Contar só até o merge produz MTTR heroico e cliente ainda quebrado.

MTTD (tempo até detectar) é métrica irmã: se MTTD domina, o problema é detecção (`OPS-022`, volume
17), não velocidade de digitação.

### MET-026 — As métricas de processo se leem em conjunto **[OBRIGATÓRIA]**

O conjunto mínimo de processo para um domínio de entrega:

| Métrica | Lê-se com |
| --- | --- |
| Cycle / lead time | Tamanho de PR, tempo de revisão |
| Frequência de deploy | CFR, MTTR |
| CFR | Escape rate, reincidência |
| WIP / idade de PR | Cycle time |

Otimizar uma coluna sem olhar a linha é Goodhart institucional (`MET-007`). Relatório que mostra
só uma delas é incompleto por construção.

### MET-027 — WIP e idade do trabalho expõem gargalo melhor que vazão **[RECOMENDADA]**

Contar itens em progresso e idade do mais velho revela fila sem precisar de estimativa de pontos.
Vazão alta com WIP alto e idade crescente é mentira de produtividade: o time empurra muito e
termina pouco.

---

## Capítulo 23.6 — Defeito e escape

### MET-028 — Escape rate mede defeito que passou dos portões **[OBRIGATÓRIA]**

Escape = defeitos encontrados em produção (ou por cliente) que deveriam ter sido pegos por teste,
revisão ou portão de pipeline, ÷ mudanças no período. A classificação "deveria ter sido pego"
exige critério escrito — senão vira disputa. Reincidência tem regra própria: o achado é o teste
ausente (`QAT-031`), e bloqueia (`CON-050`).

### MET-029 — Densidade de defeito é por módulo ou fluxo, nunca por pessoa **[OBRIGATÓRIA]**

Agregar defeitos por autor produz caça às bruxas e esconde módulo podre tocado por muita gente.
Agregar por módulo, serviço ou fluxo crítico revela onde o sistema sangra — e alimenta priorização
de auditoria (`AUD-006`), não de RH.

### MET-030 — Severidade classifica impacto; volume sozinho não prioriza **[OBRIGATÓRIA]**

Cem `S3` não pesam como um `S0`. Relatórios de "bugs abertos" sem fatia por severidade e idade são
inválidos para decisão. A matriz de severidade é da constituição (`CON-036`); este volume só exige
que a métrica a respeite no denominador e no limiar (0 `S0`/`S1` em aberto como portão — `CON-050`).

---

## Capítulo 23.7 — Fronteira com observabilidade

### MET-031 — Telemetria do produto não é métrica de engenharia **[IMUTÁVEL]**

Latência de endpoint, taxa de erro HTTP, saturação, SLI/SLO, cardinalidade de rótulo e painel de
incidente pertencem a [17](17-observabilidade.md) e à fundação em [10](10-devops.md) (`OPS-018`,
`OBS-048`). Este volume **cita** esses sinais quando a qualidade da engenharia depende deles (CFR,
MTTR, regressão de p95), mas não redefine tipo de métrica, histograma ou alerta.

Se a pergunta é "o serviço está quebrado agora?", é OBS. Se a pergunta é "nosso processo de entrega
está piorando?", é MET.

### MET-032 — Métrica de engenharia não substitui SLI **[OBRIGATÓRIA]**

Cycle time ótimo com SLI estourado é fracasso. É ilegítimo reportar "engenharia saudável" com base
só em MET quando os SLOs do fluxo crítico estão sem orçamento (`OBS-051`) ou sem consequência
(`OBS-053`). O relatório de engenharia declara a fatia OBS relevante ou marca "não verificado"
(`CON-020`, `CON-027`).

### MET-033 — Quando MET consome dado de OBS, a definição aponta a consulta **[OBRIGATÓRIA]**

Exemplo: "regressão de p95 > 20% bloqueia" (`CON-050`, `PRF-038`) — a métrica de engenharia no
pipeline aponta a query/painel OBS que a alimenta. Número colado à mão no PR não é evidência
(`CON-009`).

---

## Capítulo 23.8 — Produto que a engenharia precisa

### MET-034 — Engenharia exige sinais de resultado de produto para fechar o ciclo **[OBRIGATÓRIA]**

Sem taxa de conclusão do fluxo crítico, abandono no passo de pagamento, erro visto pelo usuário e
adoção da feature após release, a engenharia otimiza proxy interno. O mínimo que este volume exige
exposto ao time de entrega — não necessariamente desenhado por ele:

| Sinal | Por que engenharia precisa |
| --- | --- |
| Conclusão do fluxo crítico | Detecta deploy "verde" que quebra negócio (`OPS-019`) |
| Erro de cliente com versão | Amarra defeito a artefato (`OBS-061`) |
| Adoção / abandono pós-release | Diz se a mudança gerou valor ou só código |
| Volume por inquilino no fluxo | Expõe blast radius real |

A definição de *o que* medir como sucesso de produto pode viver no volume de produto; a obrigação
aqui é: **mudança de risco médio ou alto sem sinal de resultado associado não declara sucesso.**

### MET-035 — Critério de sucesso da mudança é mensurável antes do merge **[OBRIGATÓRIA]**

Toda mudança que alega "melhorar X" declara X, método e limiar de verificação — alinhado a
`PRF-006` quando X é performance, e a `CON-014` sempre. "Melhoramos a UX" sem métrica ou critério
observável é narrativa, não entrega.

### MET-036 — Feature flag sem métrica de adoção é dívida disfarçada **[RECOMENDADA]**

Flag com prazo (`OPS-038`) e sem sinal de quem a usa vira ramo eterno. A métrica mínima é exposição
(quantos inquilinos/usuários no tratamento) e resultado (conversão ou erro no tratamento vs
controle), mesmo que o experimento seja tosco.

---

## Capítulo 23.9 — A11y e performance com limiar

### MET-037 — Acessibilidade automatizada zero erros é portão; manual tem amostra **[OBRIGATÓRIA]**

Conforme `CON-050`: erros automatizados de a11y = 0 (bloqueia); tarefas críticas por teclado =
100% (bloqueia). A métrica de engenharia no pipeline falha o build nesses portões. Complemento
manual: amostra das tarefas críticas do módulo, rastreável a `UXI-044` e afins — não "rodamos o
axe uma vez".

Relatório que cita só o score do Lighthouse como prova de a11y é rejeitado: score agrega e esconde
falha de teclado.

### MET-038 — Performance de qualidade usa limiar declarado e regressão **[OBRIGATÓRIA]**

Os números canônicos estão em `CON-050` e `PRF-038` (API p95, LCP/INP/CLS, bundle, regressão >
20%). Este volume exige: (1) limiar no perfil; (2) verificação automática no pipeline onde a
constituição marca bloqueio; (3) registro do método (`PRF-002`); (4) proibição de "ficou mais
rápido" sem número (`PRF-001`).

Performance sem medição não gera achado de performance — gera `não verificado`.

### MET-039 — Bundle e regressão bloqueiam; p95 de API investiga **[OBRIGATÓRIA]**

Respeitar a coluna "Bloqueia?" de `CON-050`. Tratar p95 acima do limiar como bloqueio de merge sem
aceitação de risco é inventar norma. Tratar bundle acima do limiar como "só aviso" é enfraquecer
portão existente. A métrica de engenharia espelha a política; não a renegocia no dashboard.

---

## Capítulo 23.10 — Nota por dimensão e agregação

### MET-040 — Nota é vetor de dimensões; o escalar sozinho não decide **[OBRIGATÓRIA]**

Pesos e escala vivem em `CON-052`, `AUD-027`, `AUD-028`. Quem reporta qualidade de módulo publica
as notas por dimensão **e** o total. Publicar só o total é achado: permite esconder segurança 4
atrás de testes 10.

O total ponderado só é legítimo depois das travas. Ordem obrigatória: notas por dimensão → aplicar
`AUD-030` → só então calcular o agregado e o veredito (`AUD-031`). Inverter a ordem — agregar
primeiro e "lembrar" da trava depois — é o caminho pelo qual módulos perigosos ganham slide verde.

### MET-041 — Agregação que mascara trava é proibida **[IMUTÁVEL]**

Qualquer fórmula, gráfico ou "health score" que permita `S0`/`S1` abertos ou segurança < 6 aparecer
como verde viola `AUD-030` e este volume. A trava limita o total e força veredito; a métrica de
engenharia não pode ter um caminho paralelo mais generoso.

### MET-042 — Ausência de achados não produz excelência **[OBRIGATÓRIA]**

Aprofunda `AUD-029`: módulo sem inspeção, sem testes, sem telemetria e sem decisão registrada não
tira 9 por "estar quieto". Métrica de "zero bugs abertos" em módulo nunca exercitado é viés de
amostra, não qualidade.

### MET-043 — Nota 10 exige DoE na dimensão, não marketing **[OBRIGATÓRIA]**

Escala em `AUD-028` e excelência em `CON-047`. Relatório de engenharia que distribui 10s sem
rastrear as marcas de excelência é teatro de métrica — o mesmo crime de cobertura inflada.

### MET-044 — Health score proprietário declara fórmula ou é rejeitado **[OBRIGATÓRIA]**

Ferramenta que devolve "78% healthy" sem fórmula auditável não entra em decisão. Se a ferramenta
não exporta a composição, o time calcula as dimensões EOS e ignora o score opaco.

---

## Capítulo 23.11 — Vigilância versus instrumentação

### MET-045 — Instrumentação mede o sistema; vigilância mede a pessoa **[IMUTÁVEL]**

Instrumentação legítima: idade de PRs, taxa de falha de deploy, tempo de suíte, escape por módulo,
fila de revisão. Vigilância ilegítima: keystrokes, horas de IDE, LOC/pessoa, commits/pessoa,
ranking de "produtividade" individual a partir de telemetria de editor.

A consequência da vigilância não é só ética: é epistemológica. O número deixa de medir o sistema
no instante em que o indivíduo otimiza a aparência (`MET-007`).

### MET-046 — LOC por pessoa e commits por pessoa nunca são coletados como desempenho **[IMUTÁVEL]**

Proibido em relatório, OKR, avaliação e painel. LOC e commits podem aparecer em análises de
churn de *arquivo/módulo* para risco — sem dimensão de autor na visualização executiva. Quebrar
esta regra invalida o programa de métricas do período (`MET-010`).

### MET-047 — Coleta de processo é transparente ao time medido **[OBRIGATÓRIA]**

O que se coleta, com qual definição, quem vê e qual reação existe fica publicado internamente.
Métrica secreta sobre o processo é vigilância mesmo quando o agregado é de time. Transparência não
exige consenso universal; exige que ninguém descubra o placar depois do fato.

### MET-048 — Não compare pessoas; compare sistemas e filas **[IMUTÁVEL]**

Leaderboard de engenheiros por qualquer proxy deste volume é antipadrão. Comparações legítimas:
módulos, fluxos, classes de mudança, equipes apenas quando o denominador e o contexto são idênticos
(`MET-014`) e o objetivo é desenho de sistema, não avaliação individual.

---

## Capítulo 23.12 — Baseline, painéis e o que matar

### MET-049 — Painel de engenharia sem consumidor nomeado é removido **[OBRIGATÓRIA]**

Espelho de `OBS-038` / `OBS-045` no domínio MET: todo gráfico declara a pergunta no título e o
papel que a faz na cadência (daily de entrega, semanal de qualidade, mensal executivo). Painel sem
consumidor em um ciclo completo é deletado, não "arquivado para depois".

"Consumidor" não é "qualquer um com acesso". É o papel que, na cadência declarada, toma uma decisão
com base na vista — priorizar, abrir post-mortem, ajustar WIP, bloquear release. Se a única ação
observada for "abrir e fechar", o painel não tem consumidor: tem plateia.

### MET-050 — Painel sem consulta no período é morto **[OBRIGATÓRIA]**

Se ninguém abriu ou consultou a fonte em [perfil, padrão 30 dias], o painel ou a métrica entra em
quarentena e some no ciclo seguinte, salvo dono que renove com nova pergunta. Painel que ninguém
olha treina o time a achar que medição aconteceu.

### MET-051 — Uma pergunta por vista; vistas de ego são proibidas **[OBRIGATÓRIA]**

"Overview de engenharia" com vinte widgets sem pergunta é wallpaper. Quebre por pergunta: "a fila
de revisão está piorando?", "o último mês teve mais escape no checkout?", "a suíte ainda roda em
menos de [perfil]?".

### MET-052 — Métrica nova passa por revisão de Goodhart antes de virar meta **[OBRIGATÓRIA]**

Checklist mínimo de criação: quatro campos (`MET-001`) · antipadrão (`MET-006`) · se é meta ou
indicador (`MET-009`) · sinais companheiros (`MET-008`, `MET-026`) · custo de coleta · dono. Sem
esse registro, a métrica não pode ser meta de OKR nem portão.

### MET-053 — Limiares `[perfil]` vivem no perfil do projeto **[OBRIGATÓRIA]**

O perfil confirma ou ajusta os padrões de `CON-050` e os limiares de processo deste volume. Ausência
de perfil: o primeiro entregável é propô-lo (como em todo volume EOS), usando os padrões até a
confirmação. Limiar só no slide do QBR não conta.

### MET-054 — Relatório periódico tem dono, cadência e decisão explícita **[OBRIGATÓRIA]**

Relatório sem "o que mudou na prática por causa dele" no ciclo anterior é candidato a cancelamento.
Métrica que nunca alterou prioridade, portão ou desenho de fluxo é decoração (`CON-050`) — mate-a
(`MET-058`).

### MET-055 — Mudança justificada só por mover métrica de manutenibilidade é rejeitada **[IMUTÁVEL]**

Restatement operacional de `CON-051` + `CON-013` no fluxo de métricas: PR, ADR ou item de backlog
cuja única justificativa é "melhorar o score / reduzir complexidade / subir cobertura de linhas"
não passa em revisão de escopo. Exija defeito, risco, norma ou regressão medida.

### MET-056 — Tempo de suíte e flakiness são métricas de processo de qualidade **[OBRIGATÓRIA]**

Suíte relevante < [perfil, padrão 5 min] (`CON-050`); testes intermitentes = 0 (`QAT-006`). A
reação a flakiness não é retry no CI (`QAT-007`): é correção ou quarentena com item de backlog
(`QAT-032`). Suíte lenta demais para rodar localmente produz o mesmo efeito de cobertura falsa —
o portão existe e ninguém confia nele.

### MET-057 — Custo de coleta de métricas de engenharia é orçado **[RECOMENDADA]**

Ferramentas, exports e jobs que alimentam MET competem por tempo de manutenção. Se o custo de
manter o placar supera o valor das decisões que ele produziu no último trimestre, corte por
pergunta — o análogo de `OBS-070` para o domínio de engenharia.

### MET-058 — Toda métrica morta é removida no mesmo ciclo em que é reconhecida **[OBRIGATÓRIA]**

Métrica morta: sem dono, sem consulta, sem reação cumprida, ou corrompida por jogo sem redesenho.
Manter morta "porque um dia alguém olha" viola `CON-050` de forma permanente e polui o restante do
programa. Remoção é o entregável; arquivo histórico pode existir, vista viva não.

---

## Padrões reutilizáveis

**Padrão: cartão de métrica.** Um registro por métrica com os campos de `MET-001` + antipadrão +
sinais companheiros + consulta/fonte + data da última reação. Sem cartão, não há métrica.

**Padrão: par tensionado.** Toda meta de processo nasce em par (deploy freq ↔ CFR; cycle time ↔
escape; velocidade de revisão ↔ defeitos pós-merge). O par é o antídoto a `MET-008`.

**Padrão: série antes de meta.** Quatro semanas de baseline (`MET-012`) antes de qualquer OKR
baseado no número. Meta sem série é chute calibrado com gravata.

**Padrão: vetor de nota.** Template de relatório de módulo: oito dimensões (`AUD-027`) · travas
(`AUD-030`) · veredito (`AUD-031`) · total por último. Nunca o inverso.

**Padrão: quarentena de painel.** 30 dias `[perfil]` sem consulta → banner de morte → remoção.
Recriação exige nova pergunta, não "restaurar o antigo".

**Padrão: definição congelada no perfil.** YAML ou seção do `perfil-do-projeto` com fórmulas de
CFR, cycle time, escape e limiares. Mudança de fórmula = versão nova + reinício de baseline.

---

## Matrizes de decisão

| Pergunta | Domínio | Volume |
| --- | --- | --- |
| O checkout falhou para o inquilino X agora? | Telemetria de produto | [17](17-observabilidade.md) |
| Nosso CFR do mês piorou? | Qualidade de entrega | este volume |
| p95 da API passou do limiar? | Performance + OBS | [07](07-performance.md), [17](17-observabilidade.md) |
| Este módulo merece nota 8 em testes? | Auditoria | [12](12-auditoria.md) |
| Devemos construir a feature? | Produto | [18](18-produto.md) |
| A suíte está confiável? | QA + MET | [11](11-qa.md), `MET-056` |

| Tipo de número | Pode ser meta? | Pode bloquear merge? |
| --- | --- | --- |
| `S0`/`S1` abertos, segredos, a11y auto, casos de negócio | Sim (portão) | Sim (`CON-050`) |
| Cobertura de linhas, complexidade, LOC | Não | Não (`CON-051`, `MET-015`) |
| Cycle time, deploy freq | Só em par tensionado | Não, salvo política local escrita |
| CFR, escape, reincidência | Sim, com definição | Reincidência sim; CFR conforme perfil |
| Score opaco de ferramenta | Não | Não (`MET-044`) |

| Sintoma | Hipótese preferida | Não faça |
| --- | --- | --- |
| Cycle time sobe | Fila de review ou PR grande | Cobrar "mais commits" |
| Deploy freq sobe e CFR sobe | Qualidade do portão | Celebrar velocidade |
| Cobertura sobe e escape sobe | Testes teatrais | Subir a meta de cobertura |
| Bugs abertos caem e `S1` sobe | Reclassificação | Premiar "zero bugs" |
| MTTR cai e reclamações sobem | Relógio no merge, não na recuperação | Premiar heróis de hotfix |

---

## Fluxo de trabalho

```
1. Inventariar métricas existentes (painel, OKR, CI gates, planilhas)
2. Classificar: MET vs OBS vs inexistente; matar mortas (MET-058)
3. Para cada métrica viva: completar cartão MET-001 ou remover
4. Separar portões (CON-050) de indicadores (CON-051)
5. Estabelecer baseline onde faltar (MET-012)
6. Montar pares tensionados de processo (MET-026)
7. Publicar vetor de nota do módulo sob revisão (MET-040)
8. Agendar cadência de relatório com decisão explícita (MET-054)
9. Revisar Goodhart a cada ciclo (MET-010, MET-052)
```

Playbooks de construção de feature/endpoint não duplicam este fluxo: ao fechar a mudança, o
critério de sucesso mensurável (`MET-035`) e a instrumentação OBS necessária são checados nos
playbooks de [21](21-playbooks.md).

---

## Exemplos de implementação

```
# Ruim — MET-001 / MET-015: rótulo sem contrato; cobertura como prova
quality:
  coverage: 92%
  status: healthy

# Bom — cartão mínimo
metric_id: checkout_escape_rate
definition: >
  defeitos de produção no fluxo checkout classificados como "pegáveis
  por teste/revisão" / deploys que tocaram checkout, janela 30d
threshold: "<= 5% [perfil]"; direction: lower_is_better; window: 30d
reaction: >
  se > limiar: dono do domínio Checkout abre análise em 5 dias úteis
  com os casos e o portão que falhou
owner: "lead-checkout"
antipattern: "reclassificar escape como melhoria"
companions: [checkout_cfr, checkout_reincidence]
```

```
# Ruim — MET-024: CFR sem definição
cfr = incidents / deploys

# Bom
cfr = (
  deploys_with (rollback OR sev<=S1_incident OR emergency_flag)
) / deploys_to_production
# "emergency_flag" e "sev" definidos no perfil; mudanças de definição
# reiniciam baseline (MET-012)
```

```
# Ruim — MET-040 / MET-041: escalar que esconde
health_score = average(all_dimensions)  # segurança 3 + UX 10 = 6.5 "ok"

# Bom — vetor + travas
scores = { security: 3, domain: 8, data: 7, tests: 8,
           architecture: 7, performance: 7, ux: 9, observability: 6 }
if open_s0_or_s1:
    total = min(weighted(scores), 4)
    verdict = "REJECTED"  # AUD-030
elif scores["security"] < 6:
    verdict = "APPROVED WITH CONDITIONS"
```

```
# Ruim — MET-046: vigilância
leaderboard = commits_per_author_this_week.sort(desc)

# Bom — risco de sistema
hotspots = files.rank_by(change_frequency * production_defects)
# sem dimensão de autor na vista executiva
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Métrica sem os quatro campos | Decoração; estouro sem dono (`MET-001`) |
| Meta = cobertura de linhas | Testes teatrais; escape sobe (`MET-015`) |
| Leaderboard individual | Jogo e esconde defeito de sistema (`MET-048`) |
| Health score opaco | Decisão irreproduzível (`MET-044`) |
| Otimizar uma métrica DORA sozinha | Goodhart clássico (`MET-026`) |
| MTTR até o merge | Cliente quebrado com placar verde (`MET-025`) |
| Comparar times sem denominador | Política disfarçada de dado (`MET-014`) |
| Painel sem consulta por meses | Falsa sensação de controle (`MET-050`) |
| PR só para mover complexidade | Viola `CON-051` / `MET-055` |
| Coletar LOC/pessoa "só para curiosidade" | Vira avaliação; corrompe o programa (`MET-046`) |
| Ajustar limiar para caber o status | Fraude de calibração (`MET-003`) |
| Reportar só o total da nota | Esconde dimensão crítica (`MET-040`) |

---

## Checklist

- [ ] Toda métrica viva tem definição, limiar, reação e dono (`MET-001`)
- [ ] Antipadrão de uso declarado (`MET-006`)
- [ ] Nenhuma meta de proxy único fácil (`MET-008`)
- [ ] Baseline com método e data, ou tendência sem julgamento absoluto (`MET-011`, `MET-012`)
- [ ] Cobertura de linhas não usada como evidência de qualidade (`MET-015`)
- [ ] Process metrics lidas em conjunto (`MET-026`)
- [ ] CFR e escape com definição escrita (`MET-024`, `MET-028`)
- [ ] MTTR até recuperação do usuário (`MET-025`)
- [ ] Fronteira OBS respeitada; SLI não substituído (`MET-031`, `MET-032`)
- [ ] Sinais de resultado de produto amarrados a mudanças relevantes (`MET-034`)
- [ ] Portões a11y/perf alinhados a `CON-050` (`MET-037`, `MET-038`)
- [ ] Nota publicada como vetor; travas aplicadas (`MET-040`, `MET-041`)
- [ ] Nenhuma métrica de vigilância individual (`MET-045`, `MET-046`)
- [ ] Painéis com consumidor e consulta recente (`MET-049`, `MET-050`)
- [ ] Métricas mortas removidas (`MET-058`)
- [ ] Limiares `[perfil]` no perfil do projeto (`MET-053`)
- [ ] Nenhuma mudança só para mover manutenibilidade (`MET-055`)
- [ ] Flakiness e tempo de suíte tratados como métricas de processo (`MET-056`)

---

## Prompt do volume

```
You are the Orchestrator agent of the EOS, operating Volume 23 — Metrics (`MET`).

Mission: determine whether this team’s engineering-quality measurement system produces decisions —
or decoration — and report every metric that is incomplete, corrupted, surveilling individuals, or
crossing into product telemetry territory.

Load first: agents/_shared/core-contract.md, 00-constituicao-da-engenharia.md (cite CON-050, CON-051,
CON-052 — never restate them), 23-metricas.md, 12-auditoria.md (scoring and verdicts),
17-observabilidade.md (boundary only), and the filled templates/perfil-do-projeto.md. If the profile
does not exist, your first deliverable is to propose the metric thresholds section.

Mandatory sequence. Do not reorder.
1. Inventory every engineering metric in use: CI gates, dashboards, OKRs, spreadsheets, audit
   scorecards. Classify each as MET, OBS, or neither. Evidence: where it is defined and who consumes it.
2. For each MET metric, verify the four fields (definition, threshold, reaction, owner). Incomplete
   cards are findings — not “to be improved later”.
3. Separate blocking gates (CON-050) from maintainability indicators (CON-051). Flag any change or
   OKR justified only by moving a maintainability number.
4. Audit Goodhart risk: single-proxy goals, individual leaderboards, LOC/commits-per-person,
   coverage-as-quality. Invalidate periods that improved by gaming.
5. Audit process set as a system: cycle/lead time, PR size, review time, deploy frequency, CFR, MTTR,
   escape/reincidence. Report isolated optimization.
6. Audit scoring: dimension vector present, weights cited (CON-052 / AUD-027), clamps applied
   (AUD-030), no opaque health score.
7. Audit boundary with Volume 17: product telemetry mistaken for engineering metrics, or engineering
   reports that ignore SLO/error-budget state.
8. Kill list: metrics/dashboards with no named consumer or no query in the profile window.

Rules of engagement.
- Evidence or nothing (CON-009). “We track cycle time” requires the formula and the query.
- Cite CON-050/051/052, AUD-027–032, QAT-002/040, PRF-001/038, OPS-018/037 — do not restate them.
- Never propose individual productivity rankings.
- Never treat line coverage as evidence of correctness.
- Stop and escalate if the request is to build surveillance of individuals (keystrokes, LOC/person)
  presented as engineering quality.

Output: exactly the “Verificação obrigatória de saída” block of Volume 23, in Brazilian Portuguese,
with MUST-FIX and OPPORTUNITY in separate lists (CON-018), and every unfixed opportunity written to
the backlog with a promotion trigger (AUD-036).
```

---

## Critérios de aceite

Um programa de métricas de engenharia (ou a fatia sob revisão) passa quando todos são verdadeiros:

1. Toda métrica viva tem cartão completo (`MET-001`) e antipadrão (`MET-006`).
2. Nenhuma meta de proxy único fácil (`MET-008`); processo lido em conjunto (`MET-026`).
3. Cobertura de linhas não aparece como evidência de qualidade (`MET-015`).
4. Nenhuma coleta de LOC/pessoa, commits/pessoa ou leaderboard individual (`MET-046`, `MET-048`).
5. CFR, escape e cycle time têm definição no perfil; baselines datadas ou tendência sem absoluto
   precipitado (`MET-012`, `MET-024`, `MET-028`).
6. Notas de módulo publicadas por dimensão com travas (`MET-040`, `MET-041`).
7. Fronteira com OBS respeitada; relatório não substitui SLI (`MET-031`, `MET-032`).
8. Portões a11y/perf alinhados a `CON-050` (`MET-037`–`MET-039`).
9. Painéis com consumidor e consulta recente; mortas removidas (`MET-049`, `MET-050`, `MET-058`).
10. Nenhuma mudança no escopo justificada só por manutenibilidade (`MET-055`).

Falha em 3, 4 ou 6 é reprovação direta: corrompe o restante do programa.

---

## Verificação obrigatória de saída

```
## Inventário
| Métrica / painel | Domínio (MET/OBS/outro) | Definição | Limiar | Reação | Dono | Veredito |

## Portões vs indicadores
| Sinal | Porta (CON-050) ou indicador (CON-051)? | Uso atual | Achado |

## Goodhart e vigilância
Jogos detectados: <lista> | Períodos invalidados: <lista>
Vigilância individual: <sim/não + evidência>   ← se sim, MUST-FIX

## Processo (conjunto)
| Cycle/Lead | PR size | Review time | Deploy freq | CFR | MTTR | Escape |
Pares tensionados presentes: <sim/não>
Otimização isolada: <lista>

## Código e qualidade
Cobertura de linhas usada como prova: <sim/não>
Casos de negócio / reincidência reportados: <sim/não>
Suíte: tempo=<...> flaky=<...>

## Nota / agregação
| Dimensão | Nota | Peso | Evidência |
Travas aplicadas: <sim/não> | Score opaco: <sim/não>
Veredito coerente com AUD-031: <...>

## Fronteira OBS / produto
Sinais OBS citados sem redefinição: <lista>
SLI/SLO considerados: <sim/não/não verificado>
Sinais de resultado de produto: <lista ou lacuna>

## Painéis
| Vista | Pergunta | Consumidor | Última consulta | Manter/Matar |

## MUST-FIX
<lista separada>

## OPPORTUNITY
<lista separada; cada uma com gatilho AUD-036>

## Camadas não cobertas
<declaração explícita, CON-027>
```
