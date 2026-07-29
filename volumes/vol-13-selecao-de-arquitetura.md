# 📔 Volume 13 — Seleção de Arquitetura

Prefixo: `SEL` · Regras: SEL-001 a SEL-033 · Papel: [Arquiteto](../agents/01-architect.md)

O [Volume 2](vol-02-arquitetura.md) diz **como fazer certo** depois que a abordagem foi escolhida. Este
volume trata da escolha em si: qual estilo, qual estratégia de renderização, síncrono ou assíncrono,
comprar ou construir.

Existe porque a lacuna mais cara de um framework de engenharia não é ignorar a norma — é aplicar
corretamente a norma de uma abordagem que não deveria ter sido escolhida. Um agente que sabe inverter
dependências mas não sabe que aquele módulo não precisava ser um serviço separado produz trabalho
impecável e inútil.

---

## Capítulo 13.1 — A regra que governa toda escolha

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

## Capítulo 13.2 — Estilos de organização interna

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

## Capítulo 13.3 — Monólito, monólito modular e serviços

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

## Capítulo 13.4 — CQRS e event sourcing

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

## Capítulo 13.5 — Síncrono e assíncrono

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

## Capítulo 13.6 — Estratégia de renderização

Complementa o [Volume 4](vol-04-frontend.md). A escolha muda onde o dado é buscado, o que é público, e o que
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

## Capítulo 13.7 — Comprar, usar ou construir

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
