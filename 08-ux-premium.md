# 📘 Volume 8 — UX/UI Premium

Prefixo: `UXI` · Regras: UXI-001 a UXI-055 · Papéis:
[Product/UX](agents/09-product-ux.md) e [Frontend](agents/03-frontend.md)

Camada coberta: **6 (UX/A11y)**.

Escopo deste volume: o que é **verificável em revisão de engenharia** — estados, feedback, prevenção de
erro, consistência, microinterações, acessibilidade e proteção do trabalho do usuário.

**Fronteira.** Princípios de usabilidade que produtos de referência aplicam, estados e
microinterações, redação de erro, consistência, fluxos, caminhos infelizes, acessibilidade
WCAG 2.2 AA, proteção do trabalho do usuário. Não cobre: tokens e componentes concretos
(→ [09](09-design-system.md)); decidir *o que* construir e para quem (→ [18](18-produto.md)).
Detalhe técnico dos oito estados na implementação: [04](04-frontend.md) (`FRT-001`).

---

## Fundamentos

UX verificável em engenharia não é gosto (`UXI-001`): é estado ausente, erro incompreensível,
trabalho perdido e barreira de acesso. O mesmo produto que cobre o caminho feliz e abandona o
caminho infeliz (`UXI-039`) gera suporte e abandono — não “dívida de design”.

Consistência é economia cognitiva (`UXI-028`): um padrão por problema. Acessibilidade não é capa
no fim — semântica, teclado e nome acessível (`UXI-041`, `UXI-044`, `UXI-049`) são requisitos do
fluxo. Ferramenta automática sozinha cobre uma fração; o restante exige teclado, leitor e zoom.

---

### UXI-001 — Gosto visual não é achado **[IMUTÁVEL]**

Escolha estética, layout e estilo de texto que sejam apenas diferentes da sua preferência **não** são
achados. Somente inconsistência com o produto existente, incompreensibilidade, ou violação de norma deste
volume. Isso é CON-013 aplicado à interface.

---

## Capítulo 8.1 — Estados

### UXI-002 — Os oito estados são projetados **[OBRIGATÓRIA]**

Inicial/primeira vez · carregando · vazio · parcial · erro · sucesso · sem permissão · offline.
Detalhamento e severidades em [FRT-001](04-frontend.md).

Ausência de estado de erro ou de vazio é `S2` — é a lacuna mais comum e a que mais gera suporte.

### UXI-003 — Três vazios diferentes **[OBRIGATÓRIA]**

"Nada aqui ainda" (primeira vez) · "nenhum resultado para esta busca" · "falha ao carregar". Confundi-los faz
o usuário concluir que o sistema quebrou.

### UXI-004 — Estado vazio diz o que fazer **[OBRIGATÓRIA]**

"Sem resultados" sozinho é um beco. Ofereça a próxima ação: limpar filtro, criar o primeiro item, ajustar a
busca.

---

## Capítulo 8.2 — Feedback e microinterações

### UXI-005 — Toda ação tem resposta imediata **[OBRIGATÓRIA]**

Nenhuma ação fica sem retorno visível. Se leva mais que um instante, mostre progresso. Se leva mais de alguns
segundos, informe o que está acontecendo e permita continuar em outra coisa.

### UXI-006 — Feedback proporcional à espera **[RECOMENDADA]**

| Duração | Tratamento |
| --- | --- |
| Instantâneo | Mudança de estado visual imediata |
| Até ~1 s | Indicador simples |
| 1–10 s | Progresso, com o que está sendo feito |
| > 10 s | Trabalho em segundo plano com notificação ao concluir |

### UXI-007 — Impedir envio duplicado **[OBRIGATÓRIA]** · `S1`

Botão desabilitado durante o envio. Ausência gera pedido duplicado e cobrança dupla — é defeito de negócio,
não de interface.

### UXI-008 — Sucesso confirmado sem ambiguidade **[OBRIGATÓRIA]**

Sucesso silencioso faz o usuário repetir a ação por dúvida.

### UXI-009 — Microinteração informa, não decora **[RECOMENDADA]**

Toda animação responde a uma pergunta do usuário: o que mudou? de onde veio? o que aconteceu com o item que
eu movi? Animação que não responde nada é custo de desempenho e de atenção.

### UXI-010 — Transição preserva a continuidade **[RECOMENDADA]**

Elemento que se transforma em outro deve ser rastreável visualmente. Corte abrupto obriga o usuário a
reencontrar o contexto.

### UXI-011 — Duração curta e curva natural **[RECOMENDADA]**

Animação de interface é da ordem de fração de segundo. Animação longa parece lentidão, mesmo quando o sistema
está rápido.

### UXI-012 — Respeite a redução de movimento **[OBRIGATÓRIA]**

Preferência do sistema é honrada. Para parte dos usuários, movimento causa desconforto físico real.

### UXI-013 — Nenhuma animação bloqueia a interação **[OBRIGATÓRIA]**

O usuário pode agir antes de a animação terminar.

### UXI-014 — Estado de foco e sobreposição são microinterações obrigatórias **[OBRIGATÓRIA]**

Elemento interativo sem retorno visual ao foco, ao passar o cursor e ao pressionar não comunica que é
interativo.

---

## Capítulo 8.3 — Mensagens de erro

### UXI-015 — Erro no vocabulário do usuário **[OBRIGATÓRIA]**

| Ruim | Bom |
| --- | --- |
| "Erro 500" | "Não conseguimos salvar agora. Tente novamente em instantes." |
| "Erro de validação" | "O CEP precisa ter 8 dígitos." |
| "Requisição inválida" | "Escolha uma data a partir de hoje." |
| "null is not an object" | Nunca deve chegar ao usuário |

### UXI-016 — Todo erro diz o que fazer **[OBRIGATÓRIA]**

Erro sem próxima ação é meia mensagem.

### UXI-017 — Nenhum detalhe técnico na interface **[OBRIGATÓRIA]**

Sem stack trace, SQL, caminho interno ou nome de tabela. Exceto um código de referência para suporte.
Vazamento técnico é simultaneamente achado de segurança (FRT-004).

### UXI-018 — Ofereça caminho de saída **[RECOMENDADA]**

Erro que o usuário não pode resolver oferece: tentar novamente, contatar suporte com o identificador, ou uma
alternativa.

### UXI-019 — Nenhum jargão interno **[OBRIGATÓRIA]**

`tenant`, `payload`, `flag`, `sync`, `deploy`, `token` não pertencem à interface.

---

## Capítulo 8.4 — Prevenção de erro e proteção do trabalho

### UXI-020 — Prefira desfazer a confirmar **[RECOMENDADA]**

Confirmação é ignorada por reflexo depois da terceira vez. Desfazer preserva o fluxo e protege de verdade.

### UXI-021 — Confirmação nomeia o que será destruído **[OBRIGATÓRIA]**

Não "Tem certeza?", mas "Excluir o pedido #1234 e seus 3 itens?".

### UXI-022 — Ação destrutiva sem confirmação nem desfazer é `S1` **[OBRIGATÓRIA]**

### UXI-023 — Nunca perca o trabalho do usuário **[OBRIGATÓRIA]** · `S1` em formulário longo

Formulário não é limpo por erro de validação, falha de rede, navegação acidental nem expiração de sessão.

### UXI-024 — Valide no momento certo **[RECOMENDADA]**

Formato ao sair do campo; regra de negócio no envio. Mostrar erro antes de a pessoa terminar de digitar é
hostil.

### UXI-025 — Ação destrutiva longe da ação comum **[RECOMENDADA]**

Separação visual e de posição entre "Salvar" e "Excluir", especialmente em tela pequena.

### UXI-026 — Limite de tempo avisado e extensível **[OBRIGATÓRIA]**

Sessão que expira sem aviso e descarta trabalho é `S2`.

### UXI-027 — Nenhum beco sem saída **[OBRIGATÓRIA]**

Todo estado tem como voltar, cancelar, ou ir para um lugar conhecido.

---

## Capítulo 8.5 — Consistência

Inconsistência é invisível em revisão isolada e óbvia para o usuário, que circula entre telas.

### UXI-028 — Um padrão por problema **[OBRIGATÓRIA]**

O mesmo tipo de ação se comporta igual em todo o produto: mesmo lugar, mesmo rótulo, mesmo retorno.

### UXI-029 — Vocabulário único na interface **[OBRIGATÓRIA]**

O mesmo conceito com o mesmo nome, e esse nome é o do glossário do domínio (ARC-015).

### UXI-030 — Mesmas regras de validação para o mesmo campo **[OBRIGATÓRIA]**

Dois formulários que validam o mesmo dado de formas diferentes é ARC-011 na interface.

### UXI-031 — Mesmo padrão de ação destrutiva em todo o produto **[OBRIGATÓRIA]**
### UXI-032 — Formato local consistente **[OBRIGATÓRIA]**

Data, hora, moeda, número e endereço no formato do usuário, idênticos em todas as telas. Data ambígua
(03/04) é fonte de erro real.

### UXI-033 — Estado de navegação preservado **[RECOMENDADA]**

Filtro, busca, ordenação e paginação sobrevivem a navegar e voltar. Perder o filtro ao voltar de um detalhe é
das maiores fontes de irritação em painéis administrativos.

### UXI-034 — Uma ação primária por tela **[RECOMENDADA]**

Se tudo tem o mesmo destaque, nada tem destaque.

### UXI-035 — Números com contexto **[RECOMENDADA]**

"Restam 2 unidades" é melhor que "estoque: 2".

---

## Capítulo 8.6 — Fluxos

### UXI-036 — O objetivo do usuário está declarado **[OBRIGATÓRIA]**

Para cada fluxo: o que a pessoa está tentando fazer, e o que é sucesso do ponto de vista dela. Fluxo sem
objetivo declarado é `S1` — ninguém sabe se ele funciona.

### UXI-037 — O usuário sabe onde está e quanto falta **[RECOMENDADA]**

Em processo de múltiplas etapas, com possibilidade de voltar sem perder o já preenchido.

### UXI-038 — Não bloqueie o que pode ser postergado **[RECOMENDADA]**

Cada campo obrigatório é uma chance de desistir.

### UXI-039 — Percorra os caminhos infelizes **[OBRIGATÓRIA]**

Entrada errada, sem permissão, falha de rede, sessão expirada, resultado vazio, resultado parcial, envio
duplicado, voltar no meio do fluxo.

### UXI-040 — Degradação aceitável para o usuário, não só para o engenheiro **[OBRIGATÓRIA]**

"Falha em silêncio e tenta depois" pode servir para uma sincronização e ser inaceitável para um pagamento.

---

## Capítulo 8.7 — Acessibilidade (WCAG 2.2 AA)

### UXI-041 — Semântica antes de ARIA **[OBRIGATÓRIA]**

Use o elemento correto. Botão nativo já é focável, acionável por teclado, anunciado como botão e compatível
com tecnologia assistiva.

> **Nenhum ARIA é melhor do que ARIA errado.** ARIA descreve, não adiciona comportamento. Se você declara
> `role="button"`, você é responsável por implementar tudo o que um botão faz.

### UXI-042 — Estrutura significativa **[OBRIGATÓRIA]**

Um `h1` por página, hierarquia sem salto de nível · regiões identificadas · lista como lista · tabela de
dados com cabeçalhos associados · ordem do código igual à ordem visual.

### UXI-043 — Idioma declarado **[OBRIGATÓRIA]**

Da página, e de trechos em outro idioma. Sem isso, o leitor de tela pronuncia com as regras erradas.

### UXI-044 — Toda tarefa completável por teclado **[OBRIGATÓRIA]**

`S1` se a tarefa é crítica; `S2` caso contrário. Verifique percorrendo o fluxo inteiro sem mouse.

### UXI-045 — Foco sempre visível **[OBRIGATÓRIA]**

Remover o indicador sem substituto equivalente é violação direta. Se o padrão é feio, desenhe um melhor — não
o apague.

### UXI-046 — Ordem de foco lógica **[OBRIGATÓRIA]**

Segue a ordem visual. Sem `tabindex` positivo. Elemento não interativo não recebe foco.

### UXI-047 — Foco gerenciado em conteúdo dinâmico **[OBRIGATÓRIA]**

Modal: foco entra, fica preso, `Esc` fecha, e ao fechar volta ao elemento que abriu. Ao remover elemento
focado, o foco vai para lugar previsível. Menu, combobox e abas seguem o padrão de teclado esperado.

### UXI-048 — Sem armadilha de foco **[OBRIGATÓRIA]**

Exceto em modal, sempre é possível sair pelo teclado.

### UXI-049 — Todo controle tem nome acessível **[OBRIGATÓRIA]**

Campo com rótulo associado — **placeholder não é rótulo**, desaparece ao digitar. Botão de ícone com nome
textual. Link com texto que descreve o destino. Imagem significativa com alternativa textual; decorativa com
alternativa vazia.

### UXI-050 — Estado comunicado programaticamente **[OBRIGATÓRIA]**

Selecionado, expandido, pressionado, inválido, ocupado, desabilitado, atual. Comunicar só por cor ou posição
exclui quem não vê.

### UXI-051 — Mudança dinâmica anunciada **[OBRIGATÓRIA]**

Resultado de busca, erro, confirmação, notificação. Sem isso, o usuário de leitor de tela clica e recebe
silêncio.

### UXI-052 — Erro identificado, descrito e associado ao campo **[OBRIGATÓRIA]**

Erro apenas em vermelho, apenas no topo, não associado ao campo, é violação.

### UXI-053 — Contraste conforme AA **[OBRIGATÓRIA]**

Texto normal 4,5:1 · texto grande 3:1 · componente e indicador de estado 3:1. Vale para texto sobre imagem,
placeholder e estado desabilitado que precise ser lido. Verifique no token, não na tela (FRT-026).

### UXI-054 — Zoom 200% e viewport estreita sem perda **[OBRIGATÓRIA]**

Sem rolagem horizontal e sem perda de conteúdo ou funcionalidade. Também com espaçamento de texto aumentado.

### UXI-055 — Alvo de toque adequado **[RECOMENDADA]**

Área e espaçamento suficientes, especialmente perto de ação destrutiva.

---

## Padrões reutilizáveis

**Padrão: oito estados projetados.** Mesma matriz de `FRT-001`, com cópia e próxima ação
(`UXI-002`–`UXI-004`).

**Padrão: erro acionável.** O que aconteceu + o que fazer + saída (`UXI-015`–`UXI-018`).

**Padrão: desfazer > confirmar.** Confirmação só quando nomeia destruição (`UXI-020`,
`UXI-021`).

**Padrão: um padrão por problema.** Inventário de variantes → escolher uma (`UXI-028`).

**Padrão: a11y em cinco etapas.** Automático bloqueante → teclado → leitor → zoom → contraste
(tabela de verificação abaixo; `UXI-041`–`UXI-054`).

---

## Matrizes de decisão

| Pergunta | Prefira | Evite se |
| --- | --- | --- |
| Vazio vs erro | Três vazios distintos (`UXI-003`) | Uma tela “sem dados” genérica |
| Desfazer vs confirmar | Desfazer (`UXI-020`) | Confirmar ação comum |
| Feedback de espera | Proporcional (`UXI-006`) | Spinner eterno |
| ARIA vs HTML | Semântica nativa (`UXI-041`) | `div`+ARIA por padrão |
| Token/componente | [09](09-design-system.md) | Inventar token neste volume |
| O que construir | [18](18-produto.md) | Priorizar feature aqui |

---

## Fluxo de trabalho

```
1. Objetivo do usuário e critério de sucesso (UXI-036)
2. Oito estados + três vazios (UXI-002–004); cite FRT para implementação
3. Feedback, duplicidade, sucesso (UXI-005–008)
4. Erros na linguagem do usuário (UXI-015–019)
5. Proteção do trabalho e destrutivo (UXI-020–027)
6. Consistência de padrão e vocabulário (UXI-028–035)
7. Caminhos infelizes e degradação (UXI-039–040)
8. A11y: semântica → teclado → nome/estado → contraste/zoom (UXI-041–055)
```

Playbook de tela: [21](21-playbooks.md). Checklist: [`checklists/acessibilidade.md`](checklists/acessibilidade.md).

---

## Exemplos de implementação

```
# Ruim — UXI-015 / UXI-016
"Erro 500"

# Bom
"Não conseguimos salvar agora. Tente novamente em instantes."
[Tentar de novo]
```

```
# Ruim — UXI-021
"Tem certeza?"

# Bom
"Excluir o pedido #1234 e seus 3 itens? Esta ação não pode ser desfeita."
```

```
<!-- Ruim — UXI-041 / UXI-049 -->
<div onclick="submit()">Salvar</div>

<!-- Bom -->
<button type="submit">Salvar</button>
```

---

## Verificação de acessibilidade

| Etapa | Como | Cobertura real |
| --- | --- | --- |
| Automática | axe ou equivalente, no pipeline, **bloqueando** | ~30% dos problemas |
| Teclado | Percorra a tarefa inteira sem mouse | Boa parte do restante |
| Leitor de tela | Uma tarefa crítica por rodada | Anúncio e contexto |
| Zoom | 200% e viewport estreita | Reflow |
| Contraste | Cada par de cores do sistema | Contraste |

**Ferramenta automática sozinha não aprova nada.** Ela não detecta rótulo errado, ordem de foco ilógica,
anúncio ausente nem alternativa textual inadequada — que são a maioria dos problemas reais.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Tela em branco durante o carregamento | Usuário acha que quebrou e recarrega |
| Girador infinito sem tempo limite | Espera indefinida sem informação |
| "Algo deu errado" | Suporte impossível, usuário sem ação |
| Confirmação em toda ação | Treina o usuário a confirmar sem ler |
| Formulário que limpa no erro | Abandono |
| Vários padrões para a mesma coisa | Custo cognitivo permanente |
| Sucesso sem confirmação | Usuário repete por dúvida |
| Filtro perdido ao voltar | Retrabalho em cada consulta |
| `div` com clique no lugar de botão | Inacessível e não anunciado |
| Remover indicador de foco | Usuário de teclado se perde |
| Placeholder como rótulo | Rótulo desaparece ao digitar |
| `aria-label` divergente do texto visível | Quem vê e quem ouve recebem coisas diferentes |
| Modal sem gerenciar foco | Usuário preso no fundo da página |
| Erro só por cor | Invisível para parte dos usuários |
| `tabindex` positivo | Quebra a ordem natural da página inteira |
| Animação longa | Parece lentidão do sistema |

---

## Checklist

- [ ] Gosto não vira achado; objetivo do fluxo declarado. (`UXI-001`, `UXI-036`)
- [ ] Oito estados; vazios distintos e acionáveis. (`UXI-002`–`UXI-004`)
- [ ] Feedback imediato; envio duplicado impedido. (`UXI-005`, `UXI-007`)
- [ ] Erro acionável, sem jargão técnico. (`UXI-015`–`UXI-017`)
- [ ] Trabalho do usuário preservado; destrutivo nomeado. (`UXI-021`–`UXI-023`)
- [ ] Um padrão por problema; vocabulário único. (`UXI-028`, `UXI-029`)
- [ ] Caminhos infelizes percorridos. (`UXI-039`)
- [ ] Semântica antes de ARIA; tarefa por teclado; foco visível. (`UXI-041`, `UXI-044`, `UXI-045`)
- [ ] Nome acessível e estado programático. (`UXI-049`, `UXI-050`)
- [ ] Contraste AA; zoom 200% sem perda. (`UXI-053`, `UXI-054`)
- [ ] Verificação a11y além do automático (teclado/leitor/zoom).

---

## Prompt do volume

```
You are reviewing UX/UI under EOS Volume 08 (UXI).

Load: core-contract, output-schemas, 00-constituicao, 08-ux-premium.md,
04-frontend.md (FRT states), 09-design-system.md for tokens/components,
checklists/acessibilidade.md. Cite 18-produto.md for build/priority — do not
decide product scope here.

Sequence:
1. Reject taste-only findings (UXI-001 / CON-013).
2. Declare user goal; map eight states and unhappy paths (UXI-002, UXI-036, UXI-039).
3. Errors, duplicate submit, work preservation (UXI-015–023).
4. Consistency: one pattern per problem (UXI-028–035).
5. Accessibility: semantic → keyboard → name/state → contrast/zoom (UXI-041–055).
6. Cite FRT for implementation gaps; DSY for token/component gaps; do not restate.

Output: flow table, unhappy paths, a11y evidence, ambiguities needing human decision.
```

---

## Critérios de aceite

1. Fluxos em escopo com objetivo e oito estados (`UXI-002`, `UXI-036`).
2. Erros acionáveis sem detalhe técnico (`UXI-015`–`UXI-017`).
3. Trabalho do usuário não se perde nos caminhos revisados (`UXI-023`).
4. Um padrão por problema nas inconsistências encontradas (`UXI-028`).
5. Tarefa crítica completável por teclado com foco visível (`UXI-044`, `UXI-045`).
6. Contraste AA e zoom 200% sem perda de conteúdo (`UXI-053`, `UXI-054`).
7. A11y não aprovada só por ferramenta automática.

---

## Verificação obrigatória de saída

```
## Fluxos revisados
| Fluxo | Objetivo do usuário | Critério de sucesso | Veredito |

## Caminhos infelizes
| Fluxo | Cenário de falha | Comportamento atual | Esperado | Severidade |

## Trabalho do usuário em risco
| Caminho | Como o trabalho é perdido | Severidade |

## Consistência
| Padrão | Variantes encontradas (locais) | Padrão único recomendado |

## Acessibilidade
| Verificação | Resultado | Evidência |
| Automática | | |
| Teclado | | |
| Leitor de tela | | |
| Zoom 200% | | |
| Contraste | | |

## Ambiguidades que exigem decisão
| Pergunta | Por que importa | Quem decide | Bloqueia qual papel |
```
