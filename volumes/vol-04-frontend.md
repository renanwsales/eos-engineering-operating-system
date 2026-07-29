# 📕 Volume 4 — Framework Frontend

Prefixo: `FRT` · Regras: FRT-001 a FRT-042 · Papel: [Frontend](../agents/03-frontend.md)

Camadas cobertas: **6 (UX/A11y)** na parte técnica, com apoio de [Vol 7](vol-07-performance.md) e
[Vol 8](vol-08-ux-ui.md). A escolha da estratégia de renderização (SSR, CSR, RSC, estático, streaming) está no
[Volume 13](vol-13-selecao-de-arquitetura.md), capítulo 13.6.

Aviso de calibragem: revisão de frontend é onde achados cosméticos se multiplicam. Estrutura de
componentes, abordagem de estilização e organização de arquivos **não são achados** salvo violação de norma
documentada ou defeito causado. Isso é CON-013 aplicado ao domínio em que ele é mais frequentemente
violado.

O achado de maior valor aqui não é arquitetural: é **estado ausente**. Interface que não trata erro e vazio
é o defeito de frontend mais comum e o que mais gera suporte.

---

## Capítulo 4.1 — Cobertura de estados

### FRT-001 — Os oito estados de toda tela **[OBRIGATÓRIA]**

Para cada tela e cada componente que busca ou envia dados:

| Estado | Requisito | Severidade se ausente |
| --- | --- | --- |
| **Inicial / primeira vez** | Explica o que é e qual a próxima ação | `S2` |
| **Carregando** | Feedback dentro de um quadro da ação | `S2` |
| **Vazio** | Diz por que está vazio e o que fazer | `S2` |
| **Parcial** | Parte carregou, parte falhou, e isso está claro | `S2` |
| **Erro** | Acionável e com nova tentativa | `S2` |
| **Sucesso** | Confirma sem ambiguidade | `S2` |
| **Sem permissão** | Diferencia de "não existe" quando é seguro | `S2` |
| **Offline** | Comportamento definido, sem falha silenciosa | `S2` |

### FRT-002 — Vazio não é erro **[OBRIGATÓRIA]**

Lista vazia legítima (primeira vez), busca sem resultado e falha de carregamento são três estados
diferentes. Confundi-los faz o usuário concluir que o sistema quebrou.

### FRT-003 — Impedir envio duplicado **[OBRIGATÓRIA]**

Botão de ação com efeito externo é desabilitado durante o envio. Ausência gera pedido duplicado e cobrança
dupla: é `S1`, não detalhe de interface.

### FRT-004 — Nunca exponha erro bruto do servidor **[OBRIGATÓRIA]**

Stack trace, SQL ou caminho interno na tela é `S1` e é simultaneamente achado de segurança — reporte junto
ao [Volume 5](vol-05-seguranca.md).

### FRT-005 — Percorra os caminhos de falha **[OBRIGATÓRIA]**

O que o usuário vê quando: a requisição falha, expira, retorna 403, retorna 500, a rede cai no meio do
envio, a sessão expira durante o preenchimento.

---

## Capítulo 4.2 — Gerenciamento de estado

### FRT-006 — Separe dado do servidor de estado do cliente **[OBRIGATÓRIA]**

Dado remoto cacheado tratado como estado local diverge do servidor e produz exibição obsoleta. São duas
naturezas diferentes: uma é cache com invalidação, a outra é estado de interface.

### FRT-007 — Derive, não duplique **[OBRIGATÓRIA]**

Estado que pode ser calculado a partir de outro não é armazenado. Duas fontes de verdade divergem — é
ARC-011 aplicado à interface.

### FRT-008 — Estado no menor escopo possível **[RECOMENDADA]**

Estado global para preocupação local acopla tudo a tudo e transforma qualquer mudança em risco de
regressão em telas não relacionadas.

### FRT-009 — Invalidação declarada após mutação **[OBRIGATÓRIA]**

Após uma escrita, quais consultas ficaram obsoletas? Sem resposta, o usuário vê o valor antigo, conclui que
a ação falhou, e repete — gerando o efeito duplicado que FRT-003 tenta evitar.

### FRT-010 — Corrida entre requisições tratada **[OBRIGATÓRIA]**

Duas requisições em voo, a mais lenta resolve por último e sobrescreve o dado mais novo. É `S2` real e
quase nunca testado. Cancele a anterior, ou descarte a resposta obsoleta por sequência.

### FRT-011 — Atualização otimista tem rollback **[OBRIGATÓRIA]**

Interface que afirma sucesso que não aconteceu é pior do que interface lenta. Se não há caminho de reversão,
não faça atualização otimista.

### FRT-012 — Nenhum efeito colateral em renderização **[OBRIGATÓRIA]**

Requisição, escrita em armazenamento e mutação de estado global durante a renderização produzem
comportamento imprevisível e loop difícil de diagnosticar.

### FRT-013 — Nada de estado derivado de props copiado na inicialização **[RECOMENDADA]**

O clássico "inicializa estado a partir da prop" congela o valor e ignora atualizações posteriores.

---

## Capítulo 4.3 — Componentes

### FRT-014 — Componente tem uma responsabilidade **[RECOMENDADA]**

Indicador, não regra de tamanho. Fatiar componente para cumprir número de linhas produz o mesmo código,
mais espalhado, com mais indireção — e é proibido por CON-013.

### FRT-015 — Separe apresentação de orquestração **[RECOMENDADA]**

Componente que busca dados, decide regra e desenha simultaneamente não é testável nem reutilizável. A
separação se justifica quando há reuso real ou dificuldade de teste — não por princípio.

### FRT-016 — Nenhuma regra de negócio no componente **[OBRIGATÓRIA]**

Cálculo de preço, decisão de permissão e validação de invariante de domínio não vivem na interface. Isso é
ARC-020. A interface pode formatar e exibir; não pode decidir.

### FRT-017 — Componente controlado ou não controlado, nunca ambos **[RECOMENDADA]**

O estado híbrido é fonte de bug de sincronização difícil de reproduzir.

### FRT-018 — Chave estável em lista **[OBRIGATÓRIA]**

Índice como chave em lista que reordena, filtra ou remove causa perda de estado e re-render incorreto. É
defeito, não estilo.

### FRT-019 — Limite de erro na fronteira de tela **[OBRIGATÓRIA]**

Uma falha de renderização não deve deixar a aplicação em branco. Defina o que acontece e o caminho de
recuperação.

### FRT-020 — Elemento nativo antes de recriar comportamento **[OBRIGATÓRIA]**

Botão, link, campo, seleção e diálogo nativos já trazem foco, teclado, papel e estado. Recriá-los com
elemento genérico exige reimplementar tudo isso — e quase nunca se completa. Ver
[Volume 8](vol-08-ux-ui.md).

---

## Capítulo 4.4 — Design system

### FRT-021 — Um token, não um valor literal **[OBRIGATÓRIA]**

Cor, espaçamento, raio, sombra, tipografia e duração vêm de tokens. Valor literal espalhado impede mudança
consistente e produz a deriva visual que ninguém consegue reverter depois.

### FRT-022 — Um componente por padrão de interação **[OBRIGATÓRIA]**

Três implementações de botão, dois modais e quatro estilos de campo garantem inconsistência. Ao encontrar
duplicata, o achado é a **divergência de comportamento** entre elas, não a duplicação em si.

### FRT-023 — Variante declarada, não improvisada **[RECOMENDADA]**

Componente aceita variantes conhecidas em vez de sobreposição livre de estilo. Sobreposição livre torna
impossível mudar o padrão depois.

### FRT-024 — Estado visual completo em cada componente do sistema **[OBRIGATÓRIA]**

Repouso, foco, sobre, pressionado, desabilitado, carregando, inválido, selecionado. Componente do design
system sem esses estados obriga cada tela a improvisar.

### FRT-025 — Acessibilidade embutida no componente **[OBRIGATÓRIA]**

Nome acessível, papel, estado e navegação por teclado vivem no componente compartilhado. Delegar isso a
cada tela garante que a maioria vai errar.

### FRT-026 — Contraste verificado no token, não na tela **[OBRIGATÓRIA]**

Cada par de cores do sistema é verificado uma vez. Verificar tela por tela é trabalho infinito e incompleto.

### FRT-027 — Componente do sistema não conhece o domínio **[RECOMENDADA]**

`<BotaoConfirmarPedido>` no design system acopla o sistema visual ao negócio. O componente é genérico; a
tela dá o significado.

---

## Capítulo 4.5 — Performance de interface

Limiares e método em [Volume 7](vol-07-performance.md). Regra que governa: **sem número, não há achado.**

### FRT-028 — Orçamento de bundle declarado e verificado no pipeline **[OBRIGATÓRIA]**

Sem verificação automática, o bundle cresce monotonicamente — nunca diminui por acaso.

### FRT-029 — Dependência é decisão de performance **[OBRIGATÓRIA]**

Antes de adicionar: qual o custo em bytes e o que ela resolve que 30 linhas não resolvem? Biblioteca inteira
importada para uma função é `S2`.

### FRT-030 — Divisão de código por rota **[RECOMENDADA]**

Carregue o necessário agora. Carregamento tardio para o que está fora da tela.

### FRT-031 — Nenhum re-render desnecessário por identidade instável **[RECOMENDADA]**

Objeto, array ou função recriados a cada render invalidam memoização. Corrija quando **medido**, não por
suspeita — memoização especulativa adiciona complexidade sem ganho.

### FRT-032 — Lista longa é virtualizada **[OBRIGATÓRIA]**

Acima de algumas centenas de itens, renderizar tudo bloqueia a interação.

### FRT-033 — Nenhum trabalho pesado na thread principal **[OBRIGATÓRIA]**

Processamento, parsing e ordenação de volume bloqueiam a interação. Mova para trabalho em segundo plano ou
para o servidor.

### FRT-034 — Reserve espaço para conteúdo assíncrono **[OBRIGATÓRIA]**

Conteúdo que chega depois e empurra o layout causa erro de clique. É defeito de interação, não estética.

### FRT-035 — Imagem otimizada por padrão **[OBRIGATÓRIA]**

Formato moderno, dimensão adequada ao uso, compressão, carregamento tardio fora da primeira tela, e
dimensões declaradas para evitar deslocamento.

### FRT-036 — Animação em propriedade que não recalcula layout **[RECOMENDADA]**

E respeitando a preferência de redução de movimento do sistema.

### FRT-037 — Fonte não bloqueia a primeira pintura **[RECOMENDADA]**

---

## Capítulo 4.6 — Segurança no cliente

### FRT-038 — Nenhum segredo no cliente **[OBRIGATÓRIA]**

Chave de API, credencial ou token de longa duração em bundle, variável de ambiente exposta ou mapa de
código-fonte é `S0`. Tudo que chega ao navegador é público.

### FRT-039 — Nenhuma decisão de segurança no cliente **[OBRIGATÓRIA]**

Ocultar um botão não é controle de acesso. A verificação real acontece no servidor; a interface apenas
reflete.

### FRT-040 — Nenhuma inserção de HTML não confiável **[OBRIGATÓRIA]**

Renderização direta de conteúdo vindo do usuário ou da API é `S1`. Se for inevitável, sanitize com
biblioteca dedicada e documente por quê.

### FRT-041 — Armazenamento local não guarda dado sensível **[OBRIGATÓRIA]**

Armazenamento do navegador é legível por qualquer script na página. Dado pessoal e token sensível não vão
para lá.

### FRT-042 — Destino de redirecionamento validado **[OBRIGATÓRIA]**

Redirecionamento controlado por parâmetro de URL permite phishing com o seu domínio como fachada.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Tela em branco durante o carregamento | Usuário acha que quebrou e recarrega |
| Girador infinito sem tempo limite | Espera indefinida sem informação |
| Estado do servidor duplicado em estado local | Divergência silenciosa |
| Índice como chave de lista | Perda de estado ao reordenar |
| Regra de negócio no componente | Divergirá do servidor |
| Valor literal de cor ou espaçamento | Deriva visual irreversível |
| Três implementações do mesmo botão | Inconsistência garantida |
| Memoizar tudo por precaução | Complexidade sem ganho medido |
| `div` com clique no lugar de botão | Inacessível e não anunciado |
| Segredo em variável de ambiente do frontend | `S0` — tudo no cliente é público |
| Atualização otimista sem rollback | Interface mente sobre o resultado |

---

## Verificação obrigatória de saída

```
## Cobertura de estados
| Tela/componente | Inicial | Carregando | Vazio | Parcial | Erro | Sucesso | Sem perm. | Offline |

## Trabalho do usuário em risco
| Caminho | Como o trabalho é perdido | Severidade |

## Performance (medida)
| Métrica | Antes | Depois | Método | Orçamento |

## Design system
| Padrão | Implementações encontradas | Divergência de comportamento | Recomendação |

## Não verificado
| Item | Por quê | Como verificar |
```
