# 📗 Volume 2 — Framework de Arquitetura

Prefixo: `ARC` · Regras: ARC-001 a ARC-040 · Papel: [Arquiteto](../agents/01-architect.md)

Camadas de análise cobertas: **1 (arquitetura)** e **2 (domínio)**.

Este volume trata de **como fazer certo** dentro da abordagem escolhida. A escolha da abordagem — estilo
arquitetural, monólito ou serviços, síncrono ou assíncrono, comprar ou construir — está no
[Volume 13](vol-13-selecao-de-arquitetura.md).

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

Mantenha o glossário no [perfil do projeto](../templates/perfil-do-projeto.md). Termo novo é decisão, não
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
