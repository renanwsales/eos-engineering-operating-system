# 📗 Volume 2 — Framework de Arquitetura

Prefixos: `ARC` (Parte I — normas) · `SEL` (Parte II — seleção) · Regras: ARC-001 a ARC-040, SEL-001 a SEL-033 · Papel: [Arquiteto](agents/01-architect.md)

Camadas de análise cobertas: **1 (arquitetura)** e **2 (domínio)**.

Este volume trata de **como fazer certo** dentro da abordagem escolhida. A escolha da abordagem — estilo
arquitetural, monólito ou serviços, síncrono ou assíncrono, comprar ou construir — está no
[Volume 13](02-arquitetura.md).

Aviso de calibragem: este é o volume com maior risco de gerar trabalho caro e de baixo valor. Achados
arquiteturais costumam ter esforço `L`/`XL` sem defeito ativo, o que os coloca em prioridade baixa apesar
de parecerem importantes. O valor deste volume está nas **poucas** fronteiras erradas que causam defeitos
reais — não em redesenhar o sistema.

---

## Capítulo 2.1 — Clean Architecture: direção das dependências

### ARC-001 — Dependências apontam para dentro **[OBRIGATÓRIA]**

```
UI / API / CLI  ──▶  Aplicação (casos de uso)  ──▶  Domínio (regras)
                              │
                              ▼
                    Infraestrutura (banco, HTTP, fila, SDK)
                    — implementa interfaces definidas pelo domínio
```

- **Viola:** entidade de domínio importando o ORM; regra de negócio recebendo objeto de requisição HTTP;
  domínio chamando SDK de fornecedor diretamente.
- **Teste da regra:** é possível testar a regra de negócio sem banco, sem rede e sem framework? Se não, a
  dependência está invertida.
- **Severidade:** `S2`, ou `S1` quando impede testar regra crítica.

### ARC-002 — O domínio não conhece infraestrutura **[OBRIGATÓRIA]**

Nenhum import de framework, ORM, cliente HTTP, SDK de nuvem ou biblioteca de serialização dentro do
domínio. O domínio **declara** a interface que precisa; a infraestrutura a implementa.

### ARC-003 — Inversão só onde há fronteira real **[OBRIGATÓRIA]**

Inverter dependência tem custo: uma indireção a mais para o leitor seguir. Justifica-se em fronteira de
fornecedor, de persistência, de tempo, de aleatoriedade e de I/O. **Não** se justifica entre dois módulos
de domínio que sempre mudam juntos.

### ARC-004 — Casos de uso orquestram, não decidem **[OBRIGATÓRIA]**

A camada de aplicação coordena: carrega, chama o domínio, persiste, publica evento. A **decisão** de
negócio pertence ao domínio. Caso de uso com condicional de regra de negócio é sinal de modelo anêmico
(ARC-014).

### ARC-005 — Zero dependências circulares **[OBRIGATÓRIA]**

Ciclo entre módulos significa que as duas partes são, na prática, um módulo só — e que nenhuma pode ser
entendida, testada ou substituída isoladamente.

- **Correções, em ordem:** mover o conceito compartilhado para um terceiro módulo · inverter a dependência
  com interface · emitir evento em vez de chamar.
- **Atenção:** ciclo disfarçado via um terceiro módulo é o mesmo problema, mais difícil de ver.
- **Severidade:** `S2` estrutural.

### ARC-006 — Interface pública explícita por módulo **[OBRIGATÓRIA]**

Um ponto de entrada por módulo. O que é interno é inacessível de fora. Import que alcança arquivo interno
de outro módulo é violação. O que é público é **contrato**: mudá-lo exige avaliar os chamadores.

### ARC-007 — Sem abstração especulativa **[OBRIGATÓRIA]**

Interface com uma única implementação, sem necessidade de teste ou de troca real, é rejeitada.

Abstraia quando: existem duas implementações reais · é fronteira de teste necessária · é fronteira de
fornecedor que se pretende trocar. **Nunca** "porque pode ser útil depois".

### ARC-008 — Sem camada de passagem **[RECOMENDADA]**

Serviço que apenas repassa a chamada para o repositório, sem decidir nada, é custo sem benefício. Remova
ou dê-lhe responsabilidade real.

---

## Capítulo 2.2 — Domain-Driven Design: o modelo

Este capítulo concentra os achados de maior valor do volume. Eles são tipicamente `S1` e baratos de
corrigir.

### ARC-009 — Estados inválidos não são representáveis **[OBRIGATÓRIA]**

Para cada entidade, liste os estados que o sistema de tipos ou o schema permitem e o negócio proíbe.

- **Exemplos de violação:** pedido `pago` com total nulo; usuário sem tenant; assinatura `ativa` com meio
  de pagamento expirado; período com fim antes do início.
- **Ordem de garantia:** tipo > constraint de banco > validação de aplicação > validação de cliente.
  Prefira sempre a mais interna disponível.
- **Severidade:** `S1` quando alcançável no fluxo normal.

### ARC-010 — Invariantes aplicadas em todos os caminhos **[OBRIGATÓRIA]**

Uma regra verificada na API mas não no job, no admin, na importação ou no script de migração não está
aplicada. **A inconsistência é o defeito**, não a ausência.

### ARC-011 — Uma fonte de verdade por decisão **[OBRIGATÓRIA]**

Cada regra de negócio tem **uma** implementação. Duas implementações é `S2` mesmo quando idênticas hoje: o
defeito é a divergência futura, que é inevitável.

Ao encontrar duplicação, compare linha por linha e reporte onde elas **já** divergem — essa divergência é
quase sempre um bug ativo.

Aplica-se a: cálculo, validação, transição de estado, autorização e formatação com significado de negócio.

### ARC-012 — Tipos de domínio, não primitivos **[OBRIGATÓRIA]**

Dinheiro, identificador, e-mail, documento, quantidade, período e percentual merecem tipo próprio. Isso
elimina a classe inteira de erros de argumento trocado — `transferir(destino, origem)` deixa de compilar.

**Dinheiro em ponto flutuante é `S1`, sempre.** Use inteiro na menor unidade ou tipo decimal exato.

### ARC-013 — Agregado com fronteira de consistência **[RECOMENDADA]**

Um agregado é a menor unidade que precisa ser consistente numa transação. Regras práticas:

- A invariante que exige atomicidade define a fronteira do agregado — não o diagrama de entidades.
- Referencie outros agregados por **identificador**, não por objeto carregado.
- Uma transação altera **um** agregado. Precisar de dois na mesma transação é sinal de que a fronteira
  está errada, ou de que o caso é de consistência eventual.

### ARC-014 — Sem modelo anêmico **[RECOMENDADA]**

Entidades que só carregam dados, com todas as regras espalhadas em serviços, não garantem invariante
alguma: qualquer caminho pode montar um objeto inválido. Coloque a regra junto do dado que ela protege.

### ARC-015 — Vocabulário único (linguagem ubíqua) **[OBRIGATÓRIA]**

Um conceito, um nome, do banco à interface. Se a entidade é `pedido`, ela não é `order` no código,
`venda` no banco e "compra" na tela.

Mantenha o glossário no [perfil do projeto](templates/perfil-do-projeto.md). Termo novo é decisão, não
improviso. Divergência de vocabulário é a principal fonte de bug de integração.

### ARC-016 — Conceito de domínio ausente **[RECOMENDADA]**

Regra espalhada por cinco lugares normalmente indica que o conceito que a possui **não existe ainda**.
Este é o achado arquitetural de maior alavancagem: criar o conceito elimina a duplicação, a divergência e
a dificuldade de teste de uma só vez.

Sinais: nome composto repetido em várias funções (`calcularFreteComDesconto`); conjunto de parâmetros que
sempre viajam juntos; comentário explicando a relação entre dois campos.

### ARC-017 — Serviço de domínio só para o que não pertence a uma entidade **[RECOMENDADA]**

Regra que envolve dois agregados, ou que depende de política externa, vive em serviço de domínio — ainda
sem infraestrutura. Serviço de domínio não é depósito para tudo que não se quis modelar.

### ARC-018 — Evento de domínio é fato, no passado **[RECOMENDADA]**

`PedidoPago`, não `PagarPedido`. Evento descreve o que aconteceu; comando pede que aconteça. Confundi-los
acopla produtor e consumidor.

---

## Capítulo 2.3 — Modularização

### ARC-019 — Fronteiras alinhadas ao domínio **[RECOMENDADA]**

Organize por capacidade de negócio (`pedidos/`, `catalogo/`, `pagamentos/`), não por tipo técnico
(`controllers/`, `services/`, `models/`).

- **Critério objetivo:** uma mudança de requisito típica deve tocar **um** diretório. Se toca cinco, a
  organização está por camada técnica e o custo de cada mudança é multiplicado.

### ARC-020 — Regra de negócio fora das bordas **[OBRIGATÓRIA]**

Controllers, handlers, componentes de UI e jobs **orquestram**; não decidem.

- **Bordas podem:** validar formato, autenticar, traduzir formato, chamar caso de uso, mapear erro para
  resposta.
- **Bordas não podem:** calcular preço, desconto, imposto ou frete; decidir permissão de negócio; validar
  invariante de domínio.

### ARC-021 — Sem módulo Deus **[OBRIGATÓRIA]**

Arquivo ou pasta que toda mudança precisa tocar serializa todo o trabalho do time.

- **Detecção:** arquivo presente em mais de 60% dos commits recentes.
- **Correção:** identifique as responsabilidades distintas dentro dele e extraia a que tem a fronteira mais
  clara — uma por vez, não todas de uma vez.

### ARC-022 — Estado compartilhado explícito **[OBRIGATÓRIA]**

Estado mutável global, singleton com estado e cache implícito precisam ser declarados e justificados. Cada
um é ponto de acoplamento invisível e fonte de teste intermitente.

### ARC-023 — Sem vazamento de ORM **[OBRIGATÓRIA]**

Entidade do ORM circulando por toda a aplicação torna impossível mudar a persistência e provoca
carregamento acidental de relações (origem silenciosa de N+1). Converta na fronteira.

### ARC-024 — Divisão só com autonomia real **[RECOMENDADA]**

Separar em serviço, pacote ou repositório distinto só se justifica quando as partes têm ciclos de mudança,
de deploy ou de escala **independentes**. Dois serviços que sempre mudam e sobem juntos são um serviço com
custo de rede — o pior dos dois mundos.

---

## Capítulo 2.4 — Integração entre módulos

### ARC-025 — Falha declarada em toda fronteira **[OBRIGATÓRIA]**

Toda chamada externa (rede, banco, fornecedor, fila) declara: **timeout**, **comportamento em falha** e se
pode ser **repetida com segurança**.

- Timeout ausente é `S2`; em dependência crítica, `S1`.
- Retry sem idempotência é `S1`: duplica efeito.
- Falha silenciosa (`catch` vazio ou que só registra log) é `S2`.

### ARC-026 — Contratos versionados **[OBRIGATÓRIA]**

Mudança incompatível em contrato consumido por outro sistema ou por cliente que você não controla exige
versionamento ou período de convivência. **Não existe "deploy simultâneo"** com app instalado no
dispositivo do usuário.

### ARC-027 — Compatibilidade durante o deploy **[OBRIGATÓRIA]**

Durante o rollout, código antigo e novo coexistem contra o mesmo banco, a mesma fila e o mesmo cache. Toda
mudança precisa funcionar nos **dois** sentidos, o que força mudanças aditivas primeiro.

### ARC-028 — Anticorrupção na borda de terceiros **[RECOMENDADA]**

Modelo de fornecedor externo não entra no domínio. Traduza na borda, ainda que a tradução pareça
redundante hoje: é o que permite trocar o fornecedor sem reescrever regras de negócio.

### ARC-029 — Escolha entre síncrono e assíncrono é decisão registrada **[RECOMENDADA]**

Síncrono acopla disponibilidade; assíncrono acopla ordem e exige idempotência. Nenhum é padrão. Registre a
escolha e a consequência aceita.

### ARC-030 — Consumidor idempotente **[OBRIGATÓRIA]**

Toda entrega pode ocorrer mais de uma vez. Consumidor não idempotente vai duplicar efeito — não é questão
de se, mas de quando.

### ARC-031 — Consistência eventual é declarada ao usuário **[RECOMENDADA]**

Se o dado leva tempo para refletir, a interface diz isso. Consistência eventual escondida produz o bug
mais confuso possível: o usuário age sobre informação que ele acredita ser atual.

---

## Capítulo 2.5 — Configuração e ambiente

### ARC-032 — Configuração fora do código **[OBRIGATÓRIA]**

Endpoint, credencial, limite e flag vêm de configuração validada na inicialização. Falhar no start com
mensagem clara é melhor do que falhar na primeira requisição do usuário.

### ARC-033 — Sem ramificação por ambiente espalhada **[OBRIGATÓRIA]**

`if (ambiente === 'prod')` disperso pelo código produz comportamento imprevisível e impossível de testar.
Injete a diferença como configuração ou implementação, num único ponto.

### ARC-034 — Flags têm prazo **[RECOMENDADA]**

Toda flag temporária tem data e item de backlog para remoção. Flags eternas multiplicam exponencialmente
os caminhos possíveis, e ninguém testa todas as combinações.

---

## Capítulo 2.6 — Documentação da arquitetura

### ARC-035 — O mapa, não o código **[RECOMENDADA]**

Um diagrama de uma página com módulos, responsabilidades e dependências, atualizado quando a **fronteira**
muda — não a cada commit. Documentação de arquitetura que não corresponde à realidade é pior do que
ausência de documentação.

### ARC-036 — Decisão relevante tem ADR **[OBRIGATÓRIA]**

Ver CON-034. ADR obrigatório para: contrato público, escolha de tecnologia ou padrão que outros seguirão,
aceitação de risco, decisão custosa de reverter, divergência deliberada de norma, esforço `XL`.

### ARC-037 — Divergência registrada, nunca silenciosa **[OBRIGATÓRIA]**

Romper uma norma deste volume é legítimo quando o custo de cumprir excede o benefício **neste** contexto —
com ADR declarando qual regra, por quê, o risco aceito e o que faria reverter.

Divergência silenciosa é erosão: em seis meses ninguém sabe qual é a regra real, e a norma deixa de
existir.

---

## Capítulo 2.7 — Heurísticas de diagnóstico

### ARC-038 — Trace uma mudança real **[OBRIGATÓRIA]**

Antes de julgar a estrutura, escolha um requisito de negócio plausível e trace quais arquivos ele tocaria.
**Este exercício encontra mais problemas de fronteira do que ler a estrutura.**

```
Requisito traçado: "cobrar frete diferente por região"
Arquivos tocados: 11 em 4 módulos
Veredito: fronteiras mal posicionadas — a regra de frete está em 3 lugares
```

### ARC-039 — Tabela de sinais **[OBRIGATÓRIA]**

| Sinal observado | Problema provável | Regra |
| --- | --- | --- |
| Mudança típica toca > 5 arquivos em > 3 módulos | Fronteiras por camada técnica | ARC-019 |
| Um arquivo aparece na maioria dos commits | Módulo Deus | ARC-021 |
| Módulo A importa interno de B | Sem interface pública | ARC-006 |
| Regra de negócio em controller ou componente | Lógica na borda | ARC-020 |
| Interface com uma implementação, sem teste que a exija | Abstração especulativa | ARC-007 |
| Serviço que só repassa ao repositório | Camada de passagem | ARC-008 |
| Dois serviços sempre implantados juntos | Divisão sem autonomia | ARC-024 |
| Domínio importa ORM, HTTP ou SDK | Dependência invertida | ARC-002 |
| Não consigo testar a regra sem banco | Dependência invertida, confirmada | ARC-001 |
| Entidades só com dados, regras em serviços | Modelo anêmico | ARC-014 |
| Mesmo conceito com nomes diferentes por camada | Vocabulário divergente | ARC-015 |
| Parâmetros que sempre viajam juntos | Conceito de domínio ausente | ARC-016 |

### ARC-040 — Achado arquitetural exige custo e caminho incremental **[OBRIGATÓRIA]**

Todo achado deste volume carrega estimativa de esforço. Achado arquitetural sem custo não é acionável e
será ignorado.

Para proposta acima de esforço `M`: ADR obrigatório **com caminho incremental**. Propostas de
reestruturação de uma vez ("big bang") são rejeitadas por padrão — elas concentram todo o risco num único
momento, violando CON-016.

Elevar achado arquitetural a `S1` exige nomear um **defeito ativo** ou uma **mudança concretamente
bloqueada**. Desconforto estrutural sozinho é `S2`, no máximo.

---

# Parte II — Seleção de Arquitetura

Prefixo: `SEL` · Regras: SEL-001 a SEL-033

A Parte I deste volume diz **como fazer certo** depois que a abordagem foi escolhida. Este
volume trata da escolha em si: qual estilo, qual estratégia de renderização, síncrono ou assíncrono,
comprar ou construir.

Existe porque a lacuna mais cara de um framework de engenharia não é ignorar a norma — é aplicar
corretamente a norma de uma abordagem que não deveria ter sido escolhida. Um agente que sabe inverter
dependências mas não sabe que aquele módulo não precisava ser um serviço separado produz trabalho
impecável e inútil.

---

## Capítulo 2.1 — A regra que governa toda escolha

### SEL-001 — O padrão é o mais simples que resolve **[IMUTÁVEL]**

Toda escolha de arquitetura começa na opção mais simples e sobe **um degrau por vez**, com gatilho nomeado.
O ônus da prova é de quem propõe subir.

```
função → módulo → módulo com fronteira explícita → monólito modular
      → monólito modular com deploy independente → serviço separado
```

Pular degraus é a forma mais comum e mais cara de erro arquitetural, porque o custo aparece meses depois,
distribuído, e nunca é atribuído à decisão que o causou.

### SEL-002 — Toda escolha declara o gatilho de mudança **[OBRIGATÓRIA]**

Não basta escolher: declare **o que faria você escolher diferente**. É `CON-033` aplicado à arquitetura, e é
o que permite revisitar a decisão sem refazer a análise.

```
Escolhido: monólito modular
Gatilho para separar pagamentos: quando pagamentos precisar de janela de deploy
  própria, ou quando a equipe passar de 12 pessoas em um repositório
```

### SEL-003 — Escolha por restrição observada, nunca por escala hipotética **[IMUTÁVEL]**

"Vamos precisar escalar" não é restrição; é previsão. Arquitetura para um volume que você não tem cobra o
custo hoje e entrega o benefício talvez.

A pergunta correta não é "isso escala?", e sim: **"quando isso deixar de escalar, quanto custa mudar?"** Se
a resposta é "pouco", escolha o simples agora.

### SEL-004 — Nenhuma escolha de estilo sem ADR **[OBRIGATÓRIA]**

Toda decisão deste volume é, por definição, custosa de reverter e serve de precedente para outros. Ver
`CON-034` e `ARC-036`.

---

## Capítulo 2.2 — Estilos de organização interna

Estes estilos não são alternativas excludentes: Clean, Hexagonal e Onion são a **mesma ideia** — dependências
apontando para o domínio — com vocabulários diferentes. Tratá-los como opções distintas é confusão de
terminologia, e escolher "entre" eles é uma discussão vazia.

### SEL-005 — Clean, Hexagonal e Onion: escolha o vocabulário, não a arquitetura **[OBRIGATÓRIA]**

| Nome | Ênfase própria | Vocabulário |
| --- | --- | --- |
| Clean Architecture | Camadas concêntricas e regra de dependência | entidade, caso de uso, adaptador |
| Hexagonal (Ports & Adapters) | Simetria entre entradas e saídas | porta, adaptador |
| Onion | Domínio no centro, infraestrutura na borda | núcleo, serviço de domínio, infraestrutura |

Escolha **um vocabulário** e use-o de forma consistente. O defeito real nunca é ter escolhido o "errado" — é
misturar os três no mesmo repositório, o que faz cada pessoa nova precisar aprender três mapas para o mesmo
território.

O que importa em qualquer um deles é `ARC-001` e `ARC-002`: o domínio não conhece infraestrutura.

### SEL-006 — Camadas técnicas versus fatia vertical **[RECOMENDADA]**

| Organização | Quando serve | Quando falha |
| --- | --- | --- |
| **Por camada técnica** (`controllers/`, `services/`) | Sistemas pequenos, com um único contexto | Assim que há mais de 2–3 contextos: toda mudança toca 5 pastas |
| **Por capacidade de negócio** (`pedidos/`, `catalogo/`) | Padrão recomendado | Raramente falha; pode gerar duplicação inicial entre módulos |
| **Vertical Slice / Feature First** (uma pasta por caso de uso) | Muitos casos de uso independentes, equipe grande, alta rotatividade | Regra compartilhada por muitas fatias tende a se duplicar e divergir |

O critério objetivo é `ARC-019`: uma mudança de requisito típica deve tocar **um** diretório.

**Vertical slice tem um risco específico** que precisa de vigilância: ele torna a duplicação de regra
confortável. Aceite duas duplicações (`CON-004`), mas rastreie — na terceira, o conceito de domínio ausente
(`ARC-016`) é o achado.

### SEL-007 — Feature First não dispensa fronteira de domínio **[OBRIGATÓRIA]**

Organizar por funcionalidade não elimina a necessidade de um lugar único para a regra de negócio
(`ARC-011`). "Cada fatia tem sua própria cópia do cálculo de frete" é violação, não estilo.

---

## Capítulo 2.3 — Monólito, monólito modular e serviços

### SEL-008 — Monólito modular é o padrão para produto em evolução **[RECOMENDADA]**

Um deploy, fronteiras internas explícitas, banco único. Entrega quase todo o benefício de modularidade sem
nenhum dos custos de distribuição: sem latência de rede, sem consistência eventual, sem rastreamento
distribuído, sem falha parcial, sem versionamento de contrato interno.

### SEL-009 — Separar em serviço exige autonomia real em três eixos **[OBRIGATÓRIA]**

Só separe quando **pelo menos um** eixo tiver necessidade demonstrada, e nomeie qual:

| Eixo | Necessidade que justifica |
| --- | --- |
| **Deploy** | A parte precisa subir sem coordenar com o resto, por cadência ou por risco |
| **Escala** | O perfil de recurso é radicalmente diferente (CPU vs memória vs I/O) e o custo de escalar junto é medido |
| **Falha** | A parte precisa continuar de pé quando o resto cai, ou o inverso |

**Não justificam separar:** tamanho do código · preferência de linguagem · organograma da empresa ·
"microsserviços são mais modernos" · desejo de "isolar" o que uma fronteira de módulo já isola.

### SEL-010 — Dois serviços que sempre sobem juntos são um serviço com custo de rede **[IMUTÁVEL]**

É o pior resultado possível: paga toda a complexidade da distribuição e recebe nenhum dos benefícios.
Detectável objetivamente — verifique o histórico de deploy.

Ver `ARC-024`.

### SEL-011 — Separar exige a infraestrutura da separação, antes **[OBRIGATÓRIA]**

Antes do primeiro serviço separado, precisa existir: rastreamento distribuído · identificador de correlação
atravessando processos · versionamento de contrato · teste de contrato · deploy e rollback independentes ·
comportamento definido para falha parcial.

Separar sem isso troca um problema de acoplamento por um problema de operação — e o segundo se paga com
incidentes, não com refatoração.

### SEL-012 — Extraia um serviço por vez, pela fronteira mais clara **[OBRIGATÓRIA]**

Nunca decomponha o monólito inteiro de uma vez. `CON-016` proíbe: concentra todo o risco num único momento.
A primeira extração é também o teste da sua capacidade operacional de sustentar serviços.

### SEL-013 — Banco compartilhado entre serviços anula a separação **[OBRIGATÓRIA]**

Dois serviços escrevendo na mesma tabela estão acoplados no lugar mais difícil de desacoplar. Se a separação
de dados não é viável, a separação de serviços não está pronta.

### SEL-014 — BFF só com clientes de necessidades divergentes **[RECOMENDADA]**

Um agregador por cliente (web, móvel) se justifica quando as necessidades de dados **realmente** divergem e a
divergência custa. Com um cliente só, ou dois com necessidades parecidas, é uma camada de passagem
(`ARC-008`).

Quando existe, o BFF pode agregar e adaptar. Não pode conter regra de negócio (`ARC-020`).

---

## Capítulo 2.4 — CQRS e event sourcing

### SEL-015 — CQRS é resposta a uma assimetria medida **[RECOMENDADA]**

Separar modelo de leitura e de escrita se justifica quando: a carga de leitura e escrita difere em ordem de
magnitude **medida**, ou o modelo de leitura exige uma forma que a escrita torna caro produzir.

Sem essa assimetria, CQRS dobra o código e introduz consistência eventual em troca de nada.

### SEL-016 — CQRS assíncrono cria consistência eventual visível ao usuário **[OBRIGATÓRIA]**

Se a projeção de leitura é atualizada de forma assíncrona, o usuário salva e não vê a mudança. Isso precisa
ser tratado na interface (`ARC-031`), ou a projeção precisa ser sincrônica.

Este é o custo que quase nunca é declarado ao adotar CQRS, e é o que gera o bug mais confuso possível: o
usuário age sobre informação que acredita ser atual.

### SEL-017 — Event sourcing exige compromisso permanente **[OBRIGATÓRIA]**

Adote apenas quando o **histórico de mudanças é requisito de negócio** — auditoria regulatória, reconstrução
de estado, análise temporal. Nunca por elegância.

Custos que são permanentes e frequentemente ignorados: versionamento de evento para sempre · reprocessamento
para corrigir projeção · consulta ad hoc difícil · direito de eliminação de dado pessoal em log imutável
(`SEC-056`) — este último é um problema jurídico real, não técnico.

### SEL-018 — Evento de domínio não é event sourcing **[OBRIGATÓRIA]**

Emitir eventos para desacoplar (`ARC-018`) é barato e recomendado. Usar o log de eventos como **fonte de
verdade do estado** é outra decisão, de outra magnitude. Confundi-las é como equipes adotam event sourcing
sem decidir adotá-lo.

---

## Capítulo 2.5 — Síncrono e assíncrono

### SEL-019 — Nenhum dos dois é padrão; a escolha é registrada **[OBRIGATÓRIA]**

| | Acopla | Custa |
| --- | --- | --- |
| **Síncrono** | Disponibilidade: se a dependência cai, você cai | Latência somada; falha propagada |
| **Assíncrono** | Ordem e tempo | Idempotência obrigatória; consistência eventual; observabilidade mais difícil |

Ver `ARC-029`.

### SEL-020 — Assíncrono para o que o usuário não espera **[RECOMENDADA]**

E-mail, relatório, sincronização, indexação, notificação. Síncrono para o que ele espera na tela.

### SEL-021 — Assíncrono exige consumidor idempotente, sem exceção **[OBRIGATÓRIA]**

Toda entrega pode ocorrer mais de uma vez (`ARC-030`). Não é questão de se, é de quando.

### SEL-022 — Fila não conserta dependência instável **[OBRIGATÓRIA]**

Enfileirar chamadas para um fornecedor que falha muda **quando** você descobre a falha, não se ela ocorre.
Sem tratamento de destino final (`BAK-047`), a fila transforma falha visível em perda silenciosa de dado.

### SEL-023 — Escolha o modelo de entrega conscientemente **[RECOMENDADA]**

Fila com competição entre consumidores (trabalho a distribuir) · publicação e assinatura (fato a divulgar) ·
log particionado (ordem por chave importa). São garantias diferentes; usar o errado produz um bug de ordem
que só aparece sob carga.

---

## Capítulo 2.6 — Estratégia de renderização

Complementa o [Volume 4](04-frontend.md). A escolha muda onde o dado é buscado, o que é público, e o que
acontece quando o JavaScript falha.

### SEL-024 — Escolha por natureza do conteúdo, não por moda de framework **[OBRIGATÓRIA]**

| Estratégia | Serve para | Custo |
| --- | --- | --- |
| **Estático (SSG)** | Conteúdo igual para todos, muda com baixa frequência | Reconstrução ou revalidação a cada mudança |
| **Servidor (SSR)** | Conteúdo por usuário que precisa aparecer na primeira pintura, ou indexável | Carga no servidor; cache mais difícil |
| **Cliente (CSR)** | Aplicação atrás de login, com muita interação e pouca necessidade de primeira pintura rápida | Primeira pintura lenta; SEO fraco |
| **Componentes de servidor (RSC)** | Reduzir JavaScript enviado mantendo composição no servidor | Modelo mental mais difícil; fronteira servidor/cliente vira decisão constante |
| **Streaming** | Página cuja parte lenta pode chegar depois | Ordem de chegada e deslocamento de layout precisam de projeto |

### SEL-025 — Dado por usuário nunca em resposta cacheada publicamente **[OBRIGATÓRIA]** · `S0`

O erro mais grave desta área. Página renderizada no servidor com dado de um usuário, servida por CDN a
outro, é `S0` — a mesma falha de `PRF-020`, num lugar onde é ainda mais fácil de cometer.

A chave de cache precisa incluir tudo que muda a resposta: usuário, tenant, permissão, idioma, moeda.

### SEL-026 — A fronteira servidor/cliente é uma fronteira de segurança **[OBRIGATÓRIA]**

Em modelos que misturam os dois, o que é importado por um componente de cliente **vai para o navegador**,
incluindo o que a cadeia de imports arrastar. Segredo alcançável por essa cadeia é `S0` (`FRT-038`).

### SEL-027 — Streaming exige espaço reservado **[OBRIGATÓRIA]**

Conteúdo que chega depois e empurra o layout causa erro de clique (`FRT-034`, `PRF-033`).

### SEL-028 — Misturar estratégias é normal; misturar sem critério declarado não é **[RECOMENDADA]**

A maioria dos produtos usa três estratégias. O que precisa existir é a regra: "página de marketing é
estática, catálogo é servidor com cache por idioma, painel é cliente".

---

## Capítulo 2.7 — Comprar, usar ou construir

### SEL-029 — Construir o que é diferencial; comprar o resto **[RECOMENDADA]**

Autenticação, pagamento, e-mail transacional, busca, observabilidade e antifraude são resolvidos por
fornecedores com anos de investimento. Construí-los consome a capacidade que deveria ir para o que
diferencia o produto.

A exceção é quando aquilo **é** o produto.

### SEL-030 — Dependência é decisão com quatro perguntas **[OBRIGATÓRIA]**

O que ela resolve que 30 linhas não resolvem · qual o custo (bytes, superfície, manutenção) · quem a mantém
e com que atividade · **qual o caminho de saída**.

A quarta é a mais esquecida e a mais caro descobrir depois. Ver `FRT-029` e `SEC-043`.

### SEL-031 — Fornecedor entra pela borda, com tradução **[OBRIGATÓRIA]**

Modelo de terceiro não entra no domínio (`ARC-028`). A tradução parece redundante no primeiro dia e é o que
permite trocar de fornecedor sem reescrever regra de negócio.

### SEL-032 — Fornecedor crítico exige comportamento em falha declarado **[OBRIGATÓRIA]**

Ver `BAK-045`. Se o fornecedor de pagamento cai, o produto faz o quê? Sem resposta escrita, a resposta na
prática é "cai também".

### SEL-033 — Construir para evitar custo de assinatura exige o cálculo completo **[RECOMENDADA]**

Inclua desenvolvimento, manutenção, plantão, conformidade e custo de oportunidade. Quase sempre a
comparação honesta inverte a conclusão intuitiva.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Escolher microsserviços no início do produto | Paga a complexidade de distribuição antes de ter o problema que ela resolve |
| Debater Clean vs Hexagonal vs Onion | Discussão de vocabulário disfarçada de discussão técnica |
| Misturar os três vocabulários no mesmo repositório | Cada pessoa nova aprende três mapas do mesmo território |
| CQRS sem assimetria medida | Dobra o código, adiciona consistência eventual, resolve nada |
| Event sourcing por elegância | Compromisso permanente com versionamento de evento e um problema de eliminação de dado pessoal |
| Fila na frente de dependência instável | Converte falha visível em perda silenciosa |
| BFF com um único cliente | Camada de passagem |
| SSR de conteúdo por usuário com cache público | `S0` |
| Serviços separados com banco compartilhado | Acoplamento no lugar mais difícil de desfazer |
| Extrair todos os serviços de uma vez | Concentra todo o risco num momento |
| Construir autenticação própria | Consome a capacidade que deveria ir ao diferencial |
| Escolher por "vamos precisar escalar" | Custo hoje, benefício talvez |

---

## Verificação obrigatória de saída

```
## Decisão de estilo
| Dimensão | Escolhido | Restrição observada que exige | Gatilho para mudar |

## Degrau de complexidade
Degrau atual: <função | módulo | módulo com fronteira | monólito modular | serviço>
Degrau proposto: <...> | Gatilho nomeado: <...> | Custo estimado: <...>

## Se propõe serviço separado
| Eixo de autonomia | Necessidade demonstrada? | Evidência |
| Deploy | | |
| Escala | | |
| Falha | | |
Infraestrutura de separação já existe? <itens de SEL-011 presentes/ausentes>

## Renderização
| Rota/área | Estratégia | Natureza do conteúdo | Dado por usuário? | Chave de cache |

## Dependências novas
| Dependência | O que resolve | Custo | Caminho de saída | Veredito |
```
