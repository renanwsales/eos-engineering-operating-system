# 📗 Volume 09 — Design System

Prefixo: `DSY` · Regras: DSY-001 a DSY-069 · Papel: [Frontend](agents/03-frontend.md)

Um produto SaaS de trinta telas contém alguns milhares de decisões visuais: quanto respiro entre o título da
fatura e a tabela de itens, qual cinza para o texto secundário, quanto tempo dura a abertura do painel de
inquilino, se o aviso de cobrança recusada é um bloco na tela ou uma notificação que passa. Nenhuma delas é
difícil. O problema é que elas são **muitas**, e que cada pessoa que toca no produto responde a elas
novamente, do zero, sob prazo. O resultado previsível é o que qualquer revisão encontra: sete cinzas
diferentes, quatro escalas de espaçamento sobrepostas, dois modais com comportamento distinto e um botão
destrutivo que muda de cor entre a tela de assinatura e a de cobrança.

O custo disso não é estético. É de tempo — cada decisão refeita é tempo que não foi para o problema de
negócio — e de confiança: o usuário que vê o mesmo conceito representado de duas formas conclui, sem
consciência disso, que são duas coisas. Um design system existe para tornar a maioria dessas decisões
**já tomadas**, e para que a decisão restante seja tomada uma vez, no lugar certo, por quem responde por ela.

Este volume trata das peças concretas: os tokens e sua hierarquia, as escalas de cor, espaço, tipo, raio e
movimento, o catálogo de componentes com anatomia e estados, e a governança que impede o sistema de virar
uma pasta de arquivos que ninguém mantém. O erro caro que ele previne tem nome: **deriva visual
irreversível** — o estado em que mudar o cinza do texto secundário exige tocar em 200 arquivos e ninguém
sabe quais dos 200 estão certos.

**Fronteira.** É deste volume: tokens e sua hierarquia; escalas de cor com contraste construído; escala de
espaçamento e densidade; tipografia; grade, contêiner e pontos de quebra; ícones; raio, borda e elevação;
duração e curva de movimento; hierarquia dos mecanismos de feedback; catálogo de componentes com anatomia,
variantes e estados; tema claro e escuro; versionamento, depreciação e governança de contribuição.
Não é: princípios de usabilidade, redação de erro, fluxo e acessibilidade como norma —
[Volume 08](08-ux-premium.md), que este volume **aplica** e nunca reafirma. Não é gerenciamento de estado,
cache de cliente, orçamento de bundle e segurança no cliente — [Volume 04](04-frontend.md). Não é escolha da
estratégia de renderização nem de biblioteca — [Volume 02](02-arquitetura.md), prefixo `SEL`.

---

## Fundamentos

### Consistência é economia, não estética

A justificativa de um design system que sobrevive a uma conversa com quem paga a conta é aritmética. Uma tela
de listagem de pedidos exige, na implementação ingênua, algo entre 40 e 80 decisões visuais. Com um sistema
maduro, entre 3 e 8: qual componente de tabela, qual densidade, qual mecanismo de feedback para a ação em
lote. As outras 70 já foram respondidas, e foram respondidas **melhor** — porque foram respondidas uma vez,
com tempo, por alguém que considerou contraste, teclado e tela estreita.

Do lado do usuário o mecanismo é o mesmo. Aprender uma interface é construir um modelo de como ela se
comporta. Cada padrão duplicado obriga a manter duas entradas no modelo em vez de uma, e o custo se paga em
cada tela, para sempre. É o que `UXI-028` protege do lado do princípio; este volume garante que exista uma
peça única para o padrão ser cumprido sem esforço.

### Design system e biblioteca de componentes não são a mesma coisa

Uma biblioteca de componentes é um conjunto de peças de interface reutilizáveis. Um design system é a
biblioteca **mais** quatro coisas, e é a ausência de qualquer uma delas que produz os fracassos:

| Camada | O que é | O que falha sem ela |
| --- | --- | --- |
| **Tokens** | Os valores nomeados e sua hierarquia | Tema impossível; mudança global exige busca e substituição |
| **Componentes** | As peças, com anatomia, variantes e estados | Cada tela improvisa estado de erro e de foco |
| **Documentação** | Quando usar cada peça, e quando não usar | Uso errado da peça certa; três variantes para o mesmo caso |
| **Governança** | Quem adiciona, quem aprova, como se deprecia | O sistema congela e o produto passa a contorná-lo |

A biblioteca sem tokens é a falha mais comum e a mais caalada: os componentes existem, parecem coerentes, e o
primeiro pedido de tema escuro revela que cada um carrega valores literais e que não há camada onde intervir.

### Por que design systems falham na prática

Quatro causas cobrem quase todos os casos observados em revisão:

1. **Falta de dono.** Foi construído num sprint, por quem depois mudou de time. Ninguém aprova adição,
   ninguém deprecia nada, e a resposta a "posso adicionar um botão?" é o silêncio — que na prática significa
   sim, no código de quem perguntou.
2. **Camada semântica ausente.** Os tokens existem, mas são primitivos (`azul-500`, `espaco-12`) consumidos
   diretamente pelas telas. Tema, densidade e mudança de marca ficam inviáveis, e o sistema é abandonado no
   primeiro requisito que exigiria essa camada.
3. **Escape sem medição.** O componente aceita sobreposição livre de estilo. A pressão de prazo faz disso o
   caminho padrão, e dois anos depois o sistema descreve uma minoria do que está em produção.
4. **Adoção presumida.** Ninguém mede a divergência. O sistema é declarado pronto, a produção segue com
   valores literais, e a discrepância só aparece quando alguém tenta mudar uma cor e o produto fica
   remendado.

Nenhuma dessas causas é técnica. Três são de governança e uma é de arquitetura de tokens — o que explica por
que este volume dedica um capítulo inteiro a cada.

### O que faz a camada semântica ser a camada que importa

A hierarquia de três níveis existe por um motivo estrutural, não organizacional. Um valor primitivo responde
"que cor é esta". Um valor semântico responde "para que serve esta cor". Só a segunda pergunta tem resposta
diferente em outro tema, em outra densidade ou em outra marca — e é por isso que **tema é uma propriedade da
camada semântica**, não dos primitivos e não dos componentes.

```
primitivo    →  --cinza-100 : #f4f4f5      valor fixo, sem opinião, nunca muda com o tema
semantico    →  --superficie-elevada : var(--cinza-100)   no tema claro
                --superficie-elevada : var(--cinza-800)   no tema escuro
componente   →  --tabela-cobranca-cabecalho-fundo : var(--superficie-elevada)
```

Uma tela que consome `--cinza-100` está fora do alcance do tema, permanentemente, e nenhuma varredura
automática distingue esse uso de um uso legítimo dentro da própria definição do tema. É o vazamento mais
barato de introduzir e o mais caro de reverter.

### O que este volume não decide

Nada aqui autoriza um achado de gosto. `UXI-001` vale integralmente: um raio de 6 px onde você preferia 8 não
é achado, e `CON-013` proíbe a mudança que só satisfaz preferência. O que é achado é **divergência do sistema
declarado**, **ausência de estado obrigatório**, **valor fora da escala** e **contraste não garantido** —
todos verificáveis por um terceiro sem discussão de gosto.

---

## Capítulo 9.1 — O sistema, seu dono e sua fronteira

### DSY-001 — Um design system existe para eliminar decisão repetida, não para padronizar gosto **[IMUTÁVEL]**

Toda regra deste volume se justifica por uma decisão que deixa de ser tomada em cada tela, ou por um defeito
que deixa de ser possível. Uma regra cuja única justificativa é uniformidade visual é preferência com número
e cai em `CON-013`.

A consequência de inverter isso é observável: sistemas defendidos por estética perdem a discussão contra
prazo na terceira semana, porque o interlocutor sabe que uniformidade não paga fatura. Sistemas defendidos por
decisões eliminadas e por contraste garantido não perdem, porque a alternativa é refazer o trabalho.

### DSY-002 — Uma biblioteca de componentes sem tokens, documentação e governança não é o sistema **[OBRIGATÓRIA]**

As quatro camadas são exigidas em conjunto. Declarar um design system que só tem componentes produz a falha
silenciosa mais comum do domínio: o time acredita ter a capacidade de mudar cor, densidade e tema de forma
central, e descobre o contrário no dia em que precisa — normalmente com prazo já assumido com o cliente.

Se apenas os componentes existem, o entregável correto é o **plano das camadas ausentes**, não a declaração de
que o sistema está pronto.

### DSY-003 — O sistema tem dono nomeado e uma fonte única **[OBRIGATÓRIA]**

Uma pessoa nomeada que aprova adição, aprova depreciação e responde por conflito entre produtos. Um único
repositório ou pacote como origem — nunca "a pasta de componentes de cada aplicação".

Sem dono, a fila de contribuições não é rejeitada nem aceita: ela é contornada. Cada contorno é uma peça nova
fora do sistema, e a soma dos contornos é o segundo design system que ninguém decidiu criar. É `ARC-011`
aplicado à camada visual.

### DSY-004 — A promoção de uma peça ao sistema tem limiar declarado **[OBRIGATÓRIA]**

Declare o número: uma peça sobe ao sistema quando o mesmo padrão de interação aparece em **N** lugares com o
mesmo comportamento esperado (`[perfil]`, tipicamente 3, ou 2 quando envolve mais de um produto). Abaixo do
limiar, a peça vive local.

Promover no primeiro uso produz componente desenhado para um caso, que ganha uma propriedade por cada caso
seguinte e vira configuração impossível de manter — é `ARC-007` no design system, e `CON-004` explica por que
duplicar duas vezes é mais barato que abstrair errado uma vez. Não promover nunca produz o inverso: a peça
divergente em cinco telas, com cinco comportamentos de foco.

### DSY-005 — O sistema é consumido como artefato versionado, nunca copiado **[OBRIGATÓRIA]**

Pacote com versão, com registro de mudanças, instalado como dependência. Pasta copiada entre repositórios não
é distribuição: é bifurcação com aparência de reuso.

A consequência é medível no primeiro defeito. Uma correção de gerenciamento de foco em diálogo (`UXI-047`)
aplicada ao pacote alcança todos os consumidores na próxima atualização; aplicada à cópia, alcança um
produto, e os outros continuam com o defeito por tempo indeterminado, sem que ninguém saiba. Contratos
versionados são `ARC-026`.

---

## Capítulo 9.2 — Tokens

Tokens são o contrato entre design e implementação. A hierarquia não é organização de arquivos: é o que
determina o que pode mudar depois e o que não pode.

### DSY-006 — Três níveis de token, com o consumidor declarado por nível **[OBRIGATÓRIA]**

| Nível | Exemplo | Quem pode consumir | Muda com o tema |
| --- | --- | --- | --- |
| **Primitivo** | `--cinza-100`, `--azul-600`, `--escala-4` | só a definição de tokens semânticos | nunca |
| **Semântico** | `--superficie-elevada`, `--texto-secundario`, `--espaco-secao` | componentes e telas | sim |
| **De componente** | `--campo-altura`, `--tabela-linha-espaco` | o componente que ele nomeia | por herança |

Sem os três níveis separados, uma das duas coisas acontece: ou o sistema tem apenas primitivos e tema é
impossível, ou tem apenas semânticos e a paleta não é auditável porque cada valor é único e ninguém sabe se
`--texto-secundario` e `--borda-forte` são o mesmo cinza por decisão ou por acidente.

### DSY-007 — Componente e tela consomem token semântico, nunca primitivo **[OBRIGATÓRIA]**

O primitivo é vocabulário interno da camada de tema. Uso direto em componente ou tela é o vazamento que
desativa o tema para aquele ponto, e apenas para aquele ponto — a tela fica clara dentro do tema escuro, com
texto escuro sobre fundo escuro em metade dos casos.

Este é o achado mais frequente em auditoria de design system, e o mais fácil de detectar mecanicamente:
qualquer referência a um token primitivo fora do diretório de definição de tema é violação. Ver `DSY-068`
para a varredura.

### DSY-008 — O nome do token semântico descreve papel, nunca aparência **[OBRIGATÓRIA]**

```
Ruim:  --cinza-claro-de-fundo   --azul-do-botao   --vermelho-erro
Bom:   --superficie-recuada     --acao-primaria   --estado-critico-texto
```

O nome que descreve aparência mente na primeira mudança de tema ou de marca: `--azul-do-botao` valendo
laranja é pior do que um nome ruim, porque quem lê o código acredita no nome e toma decisões erradas a partir
dele. É `CON-065` aplicado ao token, e o custo de corrigir depois é uma renomeação em todo o produto.

### DSY-009 — Token de componente existe só quando o semântico não basta **[RECOMENDADA]**

Legítimo para dimensão própria da peça: altura do campo, largura da faixa lateral, espaço interno da célula da
tabela de cobrança. Ilegítimo como atalho para escapar da escala.

Um token de componente por propriedade de cada componente reintroduz o problema que os tokens resolvem: 400
nomes, nenhuma escala, e nenhuma forma de mudar densidade sem editar 400 valores.

### DSY-010 — Nenhum valor bruto atravessa a camada semântica **[OBRIGATÓRIA]**

Um token semântico cujo valor é `#3f3f46` em vez de `var(--cinza-700)` parece correto e não é: ele saiu da
escala sem sair da nomenclatura. Na próxima revisão da paleta, todos os tokens que referenciam a escala
mudam, e esse fica atrás — divergindo em silêncio, com nome que afirma pertencer ao sistema.

O mesmo vale para valor calculado no componente. `calc(var(--espaco-3) + 2px)` é um valor fora da escala com
disfarce de token. É `FRT-021` no nível em que ele é mais difícil de detectar.

### DSY-011 — Os tokens têm uma fonte única, e cada plataforma é gerada dela **[OBRIGATÓRIA]**

Um arquivo de definição, e os artefatos por plataforma (CSS, tema do aplicativo móvel, biblioteca de design,
documentação) gerados por processo automático a partir dele.

Manter a paleta em dois lugares mantidos à mão garante divergência: a cor de estado crítico é ajustada na web
e não no aplicativo, e o mesmo aviso de cobrança recusada aparece em dois vermelhos diferentes para o mesmo
usuário. Duas fontes de verdade divergem na primeira revisão de uma delas (`ARC-011`).

### DSY-012 — Todo token semântico tem valor em todos os temas declarados **[OBRIGATÓRIA]**

A verificação é mecânica: o conjunto de chaves de cada tema é idêntico. Chave ausente no tema escuro cai no
valor herdado do claro, e o resultado é o texto de baixo contraste que passa por toda revisão visual porque
quem revisa está no tema padrão.

Falta de token no tema é a origem mais comum de falha de contraste em produção depois de o sistema já ter sido
auditado — a auditoria olhou um tema.

### DSY-013 — Nenhum valor tem dois nomes semânticos **[OBRIGATÓRIA]**

Se `--texto-secundario` e `--rotulo-de-campo` apontam para o mesmo primitivo, a pergunta é se eles são o mesmo
papel. Se são, um deve deixar de existir. Se não são, eles vão divergir um dia e a duplicação atual é
coincidência, não sinônimo — e isso precisa estar escrito.

Dois nomes para um valor produzem o defeito clássico: alguém ajusta o contraste do rótulo de campo, altera o
token errado, e o texto secundário de doze telas muda sem que nada no pedido de mudança mencionasse isso.

### DSY-014 — Token removido ou renomeado passa por depreciação, nunca por substituição direta **[OBRIGATÓRIA]**

Aditivo primeiro: o token novo entra, o antigo passa a apontar para ele e é marcado como depreciado, o uso é
medido, e a remoção vem depois de o uso chegar a zero. É `OPS-011` aplicado ao sistema visual.

Renomear e corrigir os consumidores no mesmo passo funciona quando o sistema tem um consumidor. Com três
produtos e um aplicativo móvel em versões diferentes, a remoção direta quebra o build de quem não atualizou —
e o time bloqueado aprende a fixar a versão antiga, que é como um design system para de evoluir.

---

## Capítulo 9.3 — Cor

### DSY-015 — Cor vive em escala com passos fixos **[OBRIGATÓRIA]**

Cada matiz do sistema é uma escala com número fixo de passos (`[perfil]`, tipicamente 10 a 12), com
luminosidade progressiva e previsível. Cor avulsa adicionada para um caso específico não é passo de escala: é
o primeiro dos sete cinzas.

A escala é o que permite responder "qual o próximo tom mais escuro" sem convocar uma reunião, e é o que torna
possível construir a garantia de contraste de `DSY-016`. Sem passos fixos, cada par é uma verificação
manual, e verificação manual em volume não acontece.

### DSY-016 — O contraste é garantido pela construção da escala, não verificado depois **[OBRIGATÓRIA]**

A escala é construída de forma que a distância entre passos seja suficiente por definição: por exemplo, com
uma escala de luminosidade perceptual em que qualquer passo `N` sobre qualquer passo `N+5` satisfaz o limiar
de texto normal. A tabela de garantias faz parte da definição do sistema e é verificada por teste automático
no pipeline (`PRF-038`, `OPS-028`).

Isso é diferente de conferir o token depois de escolhê-lo (`FRT-026`) e diferente do limiar em si, que é
`UXI-053`. A construção é o que muda o custo: com garantia por construção, um par novo é seguro sem
verificação; sem ela, cada combinação nova é uma verificação que alguém vai esquecer, e o esquecimento produz
texto ilegível para parte dos usuários em produção.

### DSY-017 — Os pares de cor permitidos são declarados; combinação livre é proibida **[OBRIGATÓRIA]**

O sistema expõe pares — `superficie-recuada` com `texto-sobre-superficie-recuada`, `acao-primaria` com
`texto-sobre-acao-primaria` — e o componente aceita o par, não duas cores independentes.

Uma etiqueta de estado que aceita `cor` e `corDoTexto` como propriedades livres transfere para cada tela uma
decisão de contraste, e a etiqueta "Cobrança pendente" em âmbar claro com texto cinza médio é o resultado
previsível. A propriedade correta é `tom="atencao"`, e o par vem do sistema.

### DSY-018 — O conjunto de cores de estado é fechado e semântico **[OBRIGATÓRIA]**

Quatro a cinco papéis (`[perfil]`): informação, sucesso, atenção, erro e, quando o domínio exige,
neutro-desabilitado. Cada um com a escala completa: fundo, borda, texto, ícone, e a variante para superfície
elevada.

Conjunto aberto produz o problema real: "pagamento em análise" recebe um roxo inventado numa tela e o âmbar de
atenção em outra, e o usuário passa a tratar cor como ruído — o que anula o valor de todas as outras cores de
estado, inclusive a de erro.

### DSY-019 — Cada cor de estado é entregue com um portador não cromático **[OBRIGATÓRIA]**

O sistema não expõe "o âmbar de atenção" isolado: expõe o componente de estado que traz cor, ícone e rótulo
juntos. Quem usa o sistema recebe os três por padrão e precisaria de esforço deliberado para ficar só com a
cor.

A norma sobre estado comunicado programaticamente é `UXI-050`; esta regra é sobre a **construção da peça**,
porque a norma sozinha depende de cada tela lembrar, e a estatística de revisão mostra que não lembram. Uma
tabela de assinaturas em que o único sinal de "inadimplente" é a linha avermelhada é inutilizável para parte
dos usuários e ilegível em impressão.

### DSY-020 — Tema é a troca da camada semântica, nunca a inversão do primitivo **[OBRIGATÓRIA]**

O tema escuro redefine o mapeamento semântico → primitivo. Ele não inverte, não filtra, não aplica
transformação global sobre cores já resolvidas.

Inversão global quebra o que precisa manter identidade: logotipo, imagem de produto do catálogo, gráfico de
consumo com escala de cor própria, e a cor de estado crítico — que invertida vira ciano. Além disso, produz
um resultado que nenhuma tabela de contraste descreve, tornando `DSY-016` inaplicável.

### DSY-021 — Tema escuro não é o tema claro invertido **[OBRIGATÓRIA]**

No tema escuro, saturação alta vibra, sombra deixa de comunicar elevação, e branco puro sobre fundo escuro
produz halo. O tema escuro tem sua própria escala de superfícies e suas próprias cores de estado, derivadas
mas não espelhadas.

Entregar o tema escuro como inversão gera dois efeitos concretos: cansaço visual relatado como "o modo escuro
está estranho", sem que ninguém consiga apontar o que, e perda total da hierarquia de profundidade — porque
`DSY-022` deixa de funcionar quando a sombra é invisível.

### DSY-022 — Superfície e elevação formam uma escala única de profundidade **[OBRIGATÓRIA]**

Um nível de profundidade determina, em conjunto: a cor da superfície, a sombra, e a borda quando ela
substitui a sombra. Não são três decisões independentes.

Definir superfície e sombra separadamente produz combinações incoerentes — o painel de detalhe do pedido com
sombra de nível 3 e superfície de nível 1 — que o usuário lê como erro de renderização. E impede o tema
escuro, onde o mesmo nível de profundidade se comunica por superfície mais clara em vez de sombra.

### DSY-023 — O tema inicial respeita a preferência do sistema, e a escolha do usuário persiste **[OBRIGATÓRIA]**

Sem escolha registrada, siga a preferência do sistema operacional. Com escolha registrada, ela vence e
sobrevive a recarregar, a navegar e a trocar de aba do produto.

Escolha que não persiste é lida como defeito, e com razão. O outro defeito é a aplicação do tema depois da
primeira pintura: o usuário de tema escuro recebe um lampejo branco em cada carregamento, o que é
desconfortável e faz o produto parecer instável — ver `FRT-034` sobre conteúdo que chega depois.

---

## Capítulo 9.4 — Espaçamento e densidade

### DSY-024 — A escala de espaçamento tem base única e passos nomeados **[OBRIGATÓRIA]**

Uma base (`[perfil]`, tipicamente 4 px) e uma progressão declarada. Todo espaço do produto é um passo dessa
escala, e os passos têm nomes de papel além do índice: `--espaco-interno-campo`, `--espaco-entre-secoes`.

Escala com duas bases concorrentes — parte do produto em múltiplos de 4, parte em múltiplos de 5 — é
indistinguível de ausência de escala, porque quase todo valor pertence a alguma delas e a verificação deixa
de discriminar.

### DSY-025 — Proximidade codifica relação, e é por isso que espaço arbitrário destrói a leitura **[OBRIGATÓRIA]**

O espaço entre elementos é o principal sinal de agrupamento que a interface tem. O rótulo precisa estar mais
perto do seu campo do que do campo seguinte; o total precisa estar mais perto da tabela de itens do que do
bloco de endereço de cobrança.

Quando o espaçamento vem de valores escolhidos por elemento, essa hierarquia se dissolve, e o usuário passa a
depender de bordas e caixas para entender o que pertence a quê — o que adiciona ruído visual para resolver um
problema que o espaço resolvia. O sintoma reportado é "a tela está confusa"; a causa é ritmo vertical
inexistente, e ela é verificável: liste os espaços verticais de uma tela e conte quantos valores distintos
aparecem.

### DSY-026 — O espaçamento externo é responsabilidade do contêiner **[RECOMENDADA]**

O componente controla seu espaço interno. Margem externa vem do contêiner que o posiciona, tipicamente por
uma primitiva de pilha ou grade.

Componente com margem externa embutida não é reutilizável: ele traz o espaçamento de onde nasceu para onde é
reaproveitado, e cada uso novo começa por anular a margem — que é exatamente a sobreposição de estilo que
`FRT-023` evita e que `DSY-062` obriga a medir.

### DSY-027 — Densidade é variante declarada do sistema **[OBRIGATÓRIA]**

Se o produto precisa de uma tabela de conciliação com linhas compactas e de um formulário de assinatura com
respiro, isso é uma variante de densidade do sistema — confortável e compacta, com a escala de espaço e a
altura de controle derivadas do modo — não um ajuste na tela.

Densidade resolvida por tela produz cinco densidades não nomeadas, e torna impossível oferecer a escolha ao
usuário depois. Densidade como variante custa uma decisão agora e nenhuma depois.

### DSY-028 — A variante densa preserva o alvo de toque **[OBRIGATÓRIA]**

Reduzir espaço interno não reduz a área acionável abaixo do mínimo. O padrão do sistema é área acionável
maior que a caixa visível quando necessário.

Modo compacto que encolhe o alvo transforma a tabela de cobranças em campo minado em tela de toque,
especialmente onde há ação destrutiva adjacente — o limiar é `UXI-055` e a separação é `UXI-025`. O defeito
aparece como "cliquei em cancelar sem querer", e a causa é a variante, não o usuário.

---

## Capítulo 9.5 — Tipografia

### DSY-029 — A escala tipográfica é fechada, com papel declarado por passo **[OBRIGATÓRIA]**

Cinco a sete passos (`[perfil]`), cada um com papel nomeado: título de página, título de seção, corpo,
corpo secundário, rótulo, legenda, numérico tabular. O papel é o que a tela escolhe; o tamanho é
consequência.

Escala aberta produz o efeito conhecido: quinze tamanhos de fonte no produto, dos quais nove diferem em 1 px
do vizinho, sem nenhuma diferença de significado. O custo é que a hierarquia visual deixa de ser informação —
o usuário não consegue mais inferir importância a partir do tamanho, porque tamanho passou a ser aleatório.

### DSY-030 — Papel tipográfico e nível de cabeçalho são independentes **[OBRIGATÓRIA]**

O sistema expõe as duas coisas separadamente: o elemento (que define a estrutura do documento, sob `UXI-042`)
e o papel visual. A tela declara `nivel={3}` e `papel="titulo-de-secao"` sem que um determine o outro.

Sem essa separação, alguém escolhe `h4` porque o tamanho está certo, e a estrutura do documento passa a ter
saltos de nível. Quem navega por cabeçalhos com leitor de tela recebe um sumário quebrado, e o defeito é
invisível para quem revisa olhando a tela.

### DSY-031 — Altura de linha é proporcional ao tamanho, não fixa **[OBRIGATÓRIA]**

Texto corpo precisa de mais entrelinha proporcional que título. A escala declara a proporção por passo
(`[perfil]`, tipicamente entre 1,2 para títulos grandes e 1,6 para corpo), e ela é parte do token
tipográfico, não uma decisão da tela.

Altura de linha única para toda a escala produz título apertado ou corpo esparso — e, no corpo, entrelinha
insuficiente é a variável que mais degrada leitura de texto longo, como a descrição de um item do catálogo ou
os termos de uma assinatura.

### DSY-032 — A medida de linha é limitada **[RECOMENDADA]**

Texto corrido tem largura máxima em unidade de caractere (`[perfil]`, tipicamente entre 45 e 90 caracteres),
e o limite vive no token de contêiner de texto, não em cada tela.

Parágrafo que atravessa um monitor largo faz o olho perder a linha no retorno. Em painéis administrativos com
área de conteúdo fluida, isso acontece por padrão sempre que ninguém definiu o limite.

### DSY-033 — O conjunto de pesos é fechado e efetivamente carregado **[OBRIGATÓRIA]**

Declare os pesos do sistema (`[perfil]`, tipicamente três) e garanta que cada um exista como arquivo
carregado. Peso usado e não carregado é sintetizado pelo navegador, e o resultado é um negrito falso, mais
pesado e com espaçamento errado.

Além do defeito visual, cada peso adicional tem custo de bytes que entra no orçamento de `FRT-028`. Quatro
pesos em duas famílias é uma decisão de performance disfarçada de decisão tipográfica (`SEL-030`).

### DSY-034 — O texto escala com a preferência do usuário **[OBRIGATÓRIA]**

Tamanho de fonte em unidade relativa à raiz, e componentes cujas dimensões derivam do tamanho do texto onde
isso é possível. Tamanho em pixel absoluto ignora a configuração de corpo maior do navegador.

O usuário que aumentou a fonte do sistema e não vê diferença no produto conclui que o produto está quebrado, e
está certo. A verificação de reflow em zoom é `UXI-054`; esta regra é sobre a unidade nos tokens, que é o que
faz a verificação passar em vez de exigir correção tela por tela.

### DSY-035 — Tamanho responsivo é interpolação declarada, não salto por ponto de quebra **[RECOMENDADA]**

O título de página que passa de 32 px a 24 px em telas estreitas muda de forma perceptível ao redimensionar.
Interpolação contínua entre um mínimo e um máximo, declarada no token, produz transição sem degrau e menos
tokens.

Quando a interpolação não é possível, o salto é aceitável — mas ele é declarado no token tipográfico, nunca
numa consulta de mídia dentro da tela, onde ninguém o encontra depois.

### DSY-036 — A fonte tem orçamento, e o texto é legível antes de ela chegar **[OBRIGATÓRIA]**

Subconjunto de caracteres, formato moderno, pré-carregamento do peso do corpo, e substituta com métricas
ajustadas para que a troca não desloque o layout. O comportamento durante o carregamento é declarado
(`FRT-037`).

Sem métricas ajustadas, a chegada da fonte reflui a tabela de itens do pedido inteira, e o usuário que já
estava clicando erra o alvo — o mesmo defeito de `FRT-034`, com origem tipográfica. Sem orçamento, cada peso
novo entra sem ninguém notar até o bundle estourar.

---

## Capítulo 9.6 — Grade, contêiner e pontos de quebra

### DSY-037 — O layout vem de grade declarada, não de posição arbitrária **[OBRIGATÓRIA]**

Colunas, medianiz (gutter) e largura de contêiner são tokens. As telas compõem sobre a grade por meio de
primitivas do sistema — pilha, grade, divisor de painéis — em vez de valores próprios.

Layout resolvido com larguras percentuais e deslocamentos por tela não sobrevive a nenhuma mudança de
conteúdo: o painel de resumo da assinatura fica 3 px desalinhado da tabela abaixo, e o alinhamento passa a
ser mantido à mão em cada revisão.

### DSY-038 — O ponto de quebra nomeia a necessidade do conteúdo, não o dispositivo **[OBRIGATÓRIA]**

```
Ruim:  --bp-iphone   --bp-ipad   --bp-desktop
Bom:   --bp-lista-em-duas-colunas   --bp-navegacao-lateral-fixa   --bp-tabela-completa
```

Ponto de quebra por dispositivo envelhece por construção: o nome codifica um tamanho de aparelho que muda a
cada geração, e o próximo formato — dobrável, janela lado a lado, tela ultralarga — não tem nome na lista. Em
dois anos, `--bp-ipad` descreve nada e ninguém tem coragem de mudar o valor porque não sabe o que depende
dele.

O nome pela necessidade é verificável e estável: "a partir daqui, a tabela de cobranças mostra as sete colunas
sem rolagem horizontal" continua verdadeiro em qualquer aparelho.

### DSY-039 — O componente reage ao espaço que recebeu, não à largura da janela **[RECOMENDADA]**

O cartão de plano de assinatura precisa mudar de disposição quando **ele** fica estreito, o que acontece na
faixa lateral de uma tela larga. Consulta baseada na largura da janela erra nesse caso e em todos os casos de
reuso.

Consequência de errar: o componente funciona na tela onde foi construído e quebra na primeira reutilização
dentro de um painel estreito, e a correção usual é uma variante nova — que é como o catálogo cresce sem
ganhar capacidade.

### DSY-040 — Nenhuma primitiva de layout reordena o visual sem reordenar o documento **[OBRIGATÓRIA]**

As primitivas do sistema não expõem propriedade de reordenação puramente visual. Quando a ordem precisa mudar
em tela estreita, o sistema oferece composição que muda também a ordem do documento.

A norma de ordem — visual igual à do código, foco seguindo o visual — é `UXI-042` e `UXI-046`. O que esta
regra impede é o sistema **oferecer a ferramenta** que viola a norma: uma propriedade de ordem disponível
será usada, e o resultado é a navegação por teclado que salta do meio da tela para o topo, num defeito que
nenhuma revisão visual encontra.

---

## Capítulo 9.7 — Ícones

### DSY-041 — Conjunto único, com grade e traço únicos **[OBRIGATÓRIA]**

Um conjunto, uma grade de desenho, uma espessura de traço, um estilo de terminação. Ícone de fora do conjunto
entra por decisão registrada, com a versão adaptada à grade.

Misturar conjuntos é perceptível mesmo por quem não sabe nomear o que vê: os ícones parecem de pesos
diferentes, a linha do cabeçalho fica visualmente irregular, e o produto parece montado com peças de origens
distintas. O custo de corrigir depois é redesenhar todos os ícones de um dos conjuntos.

### DSY-042 — O tamanho de ícone vem de uma escala alinhada à tipografia **[OBRIGATÓRIA]**

Os tamanhos de ícone são poucos (`[perfil]`, tipicamente três a quatro) e cada um é dimensionado para
alinhar-se opticamente a um passo da escala tipográfica, incluindo o alinhamento de linha de base junto ao
texto.

Ícone dimensionado por tela produz o desalinhamento vertical de 1 a 2 px ao lado do rótulo, que aparece em
todo botão com ícone do produto. Ninguém abre um defeito para isso, e ele degrada a percepção de acabamento
de forma difusa e permanente.

### DSY-043 — Ícone sozinho não identifica ação fora do conjunto convencional **[OBRIGATÓRIA]**

Apenas um punhado de ícones é entendido sem rótulo: fechar, buscar, menu, mais. Fora deles, o componente do
sistema exige rótulo visível, ou rótulo revelável com nome permanentemente disponível.

Barra de ferramentas só com ícones para "reprocessar cobrança", "estornar" e "gerar segunda via" força o
usuário a adivinhar ou testar — e testar uma ação de cobrança é caro. O nome acessível é `UXI-049`; esta
regra é sobre quem vê a tela e não sabe o que o ícone faz.

### DSY-044 — Um significado, um ícone, em todo o produto **[OBRIGATÓRIA]**

O mapeamento significado → ícone é parte do sistema, documentado, e não se repete: o mesmo ícone não serve
para dois conceitos, e o mesmo conceito não recebe dois ícones.

Ícone reutilizado para dois significados é pior que ícone ambíguo: o usuário aprendeu o primeiro significado e
aplica o modelo errado ao segundo. É `UXI-028` e `UXI-029` na camada visual, e o caso caro é o ícone de seta
circular servindo para "recarregar a listagem" numa tela e para "reprocessar a cobrança" em outra.

---

## Capítulo 9.8 — Raio, borda e elevação

### DSY-045 — O raio é escala, e o passo carrega hierarquia **[RECOMENDADA]**

Três a quatro passos (`[perfil]`), com significado: controle pequeno, contêiner, superfície flutuante,
elemento circular. O passo comunica escala do elemento, não preferência.

Raio por elemento produz o botão de 6 px dentro do cartão de 4 px, que é lido como desalinhamento. E impede a
regra de composição óbvia — o raio interno é menor que o do contêiner que o abriga — porque não há escala
para derivá-lo.

### DSY-046 — Sombra codifica distância do plano, e o separador tem mecanismo único por superfície **[OBRIGATÓRIA]**

Sombra existe para dizer que algo flutua acima de outra coisa, e o quanto. Cada superfície do sistema declara
como separa seu conteúdo: por borda ou por variação de superfície — um mecanismo, não os dois somados.

Sombra decorativa em elemento que não flutua destrói a informação: quando tudo tem sombra, nada está acima de
nada, e o menu suspenso deixa de se distinguir do conteúdo. Borda somada a sombra somada a mudança de
superfície é o triplo separador que produz a interface visualmente pesada sem que nenhum dos três esteja
errado isoladamente. E `UXI-009` já estabelece que o elemento visual responde a uma pergunta ou é custo.

### DSY-047 — Elevação e ordem de empilhamento saem da mesma tabela **[OBRIGATÓRIA]**

Uma tabela nomeada, com poucos níveis, que define para cada nível a sombra, a superfície e o valor de
empilhamento: conteúdo, cabeçalho fixo, menu suspenso, painel lateral, diálogo, notificação transitória.

A ausência dessa tabela produz o defeito mais previsível do frontend: valores de empilhamento escolhidos por
tentativa, escalando até números arbitrários, e o menu suspenso que fica atrás do cabeçalho em uma tela e na
frente do diálogo em outra. Cada correção pontual é um valor maior que o anterior, e o problema é estrutural —
é `CON-073` com aparência de detalhe de estilo.

---

## Capítulo 9.9 — Movimento

### DSY-048 — Duração e curva são tokens, com papel declarado **[OBRIGATÓRIA]**

Poucas durações (`[perfil]`, tipicamente três: micro, padrão, entrada de superfície) e poucas curvas, cada
uma com papel: entrada de elemento, saída, movimento contínuo, resposta a toque. A tela escolhe o papel.

Duração literal por animação produz um produto onde nada tem o mesmo ritmo: o painel abre em 300 ms e fecha
em 150 ms sem que isso tenha sido decidido, e o resultado é a sensação de irregularidade que `UXI-011`
descreve pelo lado do princípio.

### DSY-049 — A lista do que anima é fechada **[OBRIGATÓRIA]**

O sistema declara o que anima — entrada e saída de superfície flutuante, expansão de conteúdo, mudança de
estado de controle, reordenação de lista — e, explicitamente, o que nunca anima: número, valor monetário,
conteúdo de tabela de dados, indicador de progresso real.

Sem a lista, animação vira decoração aplicada por gosto. O caso concreto que dói: o total da fatura animado
contando de zero até o valor final impede o usuário de lê-lo, e num contexto de cobrança isso é
constrangedor. A lista também protege o custo de renderização (`FRT-036`).

### DSY-050 — Nada anima entre a ação e a primeira evidência de resposta **[OBRIGATÓRIA]**

A confirmação visual de que o clique foi registrado é imediata. Nenhuma animação de entrada é inserida antes
dela, e nenhuma transição atrasa a aparição do indicador de carregamento.

Uma animação de 250 ms antes de o botão mostrar estado de envio soma-se à latência real e produz a percepção
de sistema lento mesmo quando o servidor respondeu em 40 ms. Pior: o usuário que não vê retorno clica de
novo, e o efeito é o envio duplicado que `UXI-007` trata como defeito de negócio. O princípio de resposta
imediata é `UXI-005`; o que esta regra proíbe é o movimento que o contradiz.

### DSY-051 — Movimento reduzido é uma variante completa do sistema, não a ausência de animação **[OBRIGATÓRIA]**

Com movimento reduzido, deslocamento e escala desaparecem; variação de opacidade e mudança de estado
permanecem. A variante é definida token por token e é testada.

Desligar tudo com uma regra global é o erro frequente: o painel de inquilino passa a aparecer instantâneo, sem
qualquer sinal de origem, e o usuário perde a continuidade que `UXI-010` protege. A obrigação de respeitar a
preferência é `UXI-012`; o que esta regra exige é que o resultado continue comunicando.

### DSY-052 — O esqueleto reproduz a forma real do conteúdo **[RECOMENDADA]**

Os elementos de carregamento do sistema têm as dimensões do conteúdo que substituem: mesma altura de linha,
mesmo número de colunas, mesma altura de cabeçalho.

Esqueleto genérico é pior do que espaço reservado vazio, porque promete uma forma e entrega outra — o layout
salta na troca, e o salto ocorre justamente quando o usuário começou a mirar. É `FRT-034` do lado da peça, e
`PRF-034` explica por que a percepção de velocidade merece o trabalho.

---

## Capítulo 9.10 — Feedback: a hierarquia dos mecanismos

Escolher o mecanismo errado é o defeito de feedback mais comum depois de não dar feedback nenhum, e ele custa
mais do que parece: erro em notificação transitória é erro perdido, e informação secundária em diálogo é
interrupção do trabalho.

### DSY-053 — Cada mecanismo de feedback tem critério de uso declarado **[OBRIGATÓRIA]**

O sistema documenta, para cada mecanismo, a condição em que ele é o correto e as condições em que não é. Sem
isso, a escolha é feita por hábito de quem implementa, e o mesmo evento aparece de três formas no produto.

| Mecanismo | Use quando | Nunca use para |
| --- | --- | --- |
| **Inline, junto ao elemento** | O problema pertence a um campo ou item específico | Resultado de operação em segundo plano |
| **Bloco na tela (banner)** | Condição persistente que afeta a tela inteira | Confirmação de ação pontual |
| **Notificação transitória (toast)** | Confirmação de sucesso que não exige leitura | Erro, ou qualquer texto acionável |
| **Diálogo modal** | O usuário não pode prosseguir sem decidir | Informar; confirmar o que poderia ser desfeito |
| **Estado da própria peça** | A ação mudou aquele elemento e nada mais | Falha que exige explicação |

### DSY-054 — Erro de campo é inline e permanente **[OBRIGATÓRIA]** · `S2`

O erro de validação vive junto ao campo, sobrevive à rolagem e desaparece só quando é resolvido. O componente
de campo do sistema oferece isso por construção — a tela não decide onde o erro aparece.

Erro em notificação transitória é erro que o usuário não consegue reler: ele volta ao formulário de cobrança
sem saber qual dos onze campos falhou, tenta enviar de novo e recebe a mesma mensagem que desaparece outra
vez. A associação programática do erro ao campo é `UXI-052`; esta regra é sobre o mecanismo, e é `S2` porque
bloqueia a conclusão da tarefa de forma reproduzível.

### DSY-055 — Notificação transitória não carrega o que precisa ser relido **[OBRIGATÓRIA]**

Nada que o usuário precise anotar, copiar, ler com atenção ou agir sobre vai num mecanismo que expira. Isso
inclui identificador de suporte, resumo de resultado parcial e qualquer link.

O sintoma é a mensagem "3 de 40 cobranças falharam" que passa em quatro segundos: o usuário viu que algo
falhou, não sabe o quê, e não tem como recuperar a informação. O correto é o bloco persistente com a lista.
A confirmação de sucesso simples continua sendo caso legítimo (`UXI-008`).

### DSY-056 — Modal só para o que impede prosseguir **[OBRIGATÓRIA]**

Diálogo modal é para decisão bloqueante: confirmar o cancelamento de uma assinatura, resolver um conflito de
edição. Não é para informar, não é para formulário longo, e não é para o que a tela poderia mostrar no lugar.

Modal usado como recipiente genérico produz três custos concretos: perda de contexto do que estava abaixo,
formulário sem espaço em tela estreita, e o encadeamento de modais que impede o usuário de saber onde está.
O gerenciamento de foco exigido é `UXI-047`, e cada modal que não é necessário é uma implementação disso que
poderia não existir.

### DSY-057 — Um mecanismo por evento, e a fila é limitada **[RECOMENDADA]**

O mesmo evento não é anunciado em dois mecanismos ao mesmo tempo. As notificações transitórias têm limite
simultâneo declarado e política para o excedente — agrupar, ou substituir.

Notificação e banner para o mesmo sucesso ensinam o usuário a ignorar os dois. E um processamento em lote sem
limite de fila empilha quarenta notificações que cobrem a interface e, com o anúncio exigido por `UXI-051`,
tornam o leitor de tela inutilizável até a fila esvaziar.

---

## Capítulo 9.11 — Catálogo de componentes

### DSY-058 — Todo componente do catálogo tem anatomia declarada **[OBRIGATÓRIA]**

A anatomia lista as partes nomeadas, quais são obrigatórias e quais opcionais, e a regra de composição entre
elas. Para um campo: rótulo, controle, texto de apoio, mensagem de erro, ícone de ação.

Sem anatomia, cada consumidor descobre por tentativa quais combinações funcionam, e o componente ganha
propriedades para casos que já eram possíveis por composição. A anatomia é também o que permite responder se
uma solicitação nova é variante, parte opcional, ou componente distinto — a decisão de `DSY-060`.

### DSY-059 — A matriz variante × estado é enumerada e verificada **[OBRIGATÓRIA]**

Os estados obrigatórios estão em `FRT-024`. O que esta regra exige é a **matriz**: cada variante do
componente tem cada estado verificado, e a verificação é automática — captura visual revisada por pessoa
(`QAT-015`) ou teste de interação, no pipeline.

O padrão de falha é conhecido e barato de detectar: a variante primária tem os oito estados, a variante
destrutiva tem quatro, e o estado de foco da variante destrutiva usa a cor de foco padrão sobre fundo
vermelho, com contraste insuficiente. Ninguém percebe porque ninguém enumerou. Uma matriz de 4 variantes por
8 estados são 32 casos, e é exatamente por serem 32 que precisam ser gerados em vez de conferidos por
lembrança.

### DSY-060 — Nenhuma variante nasce sem regra de quando usar **[OBRIGATÓRIA]**

A variante entra no catálogo com a frase que a distingue das existentes, em termos de situação de uso, não de
aparência. "Use `destrutivo` quando a ação remove dado ou encerra um contrato" é regra; "use `destrutivo`
para o botão vermelho" é tautologia.

Variante sem regra é escolhida por aparência, e a distinção que ela codificava se dissolve em três meses:
metade dos cancelamentos de assinatura em `destrutivo`, metade em `secundario`, e o usuário não tem mais como
saber quais ações são perigosas. `FRT-023` exige que a variante seja declarada; esta regra exige que ela seja
decidível.

### DSY-061 — Composição por padrão; configuração para o que é fechado **[RECOMENDADA]**

Conteúdo variável entra por composição — partes nomeadas, encaixes. Conjunto fechado de opções entra por
propriedade: tom, tamanho, densidade.

O sinal de que a linha foi cruzada é observável: um componente com mais de uma dezena de propriedades
booleanas de aparência, ou propriedades que aceitam trechos de interface. Nesse ponto, a peça reimplementa
composição com uma linguagem pior, e cada caso novo exige uma alteração no sistema em vez de uma composição
no consumidor — o que transforma o dono do sistema em gargalo de todo o produto.

### DSY-062 — Propriedade de escape é nomeada, rara e medida **[OBRIGATÓRIA]**

Se o sistema aceita sobreposição de estilo, ela tem nome explícito que declara o que é, é documentada como
saída de emergência com prazo, e o número de usos é contado e reportado.

Escape sem medição é o mecanismo pelo qual um design system deixa de descrever o produto. Ele não falha
ruidosamente: cada uso é razoável, o prazo aperta, e dois anos depois há 300 sobreposições, nenhuma
justificada por escrito, e mudar um token não muda mais o produto. Uma contagem crescente é o gatilho de
promoção (`AUD-036`) de um item de backlog: ou a lacuna do sistema é real e vira componente, ou os usos são
indevidos e voltam para variantes.

### DSY-063 — Componente que envolve elemento nativo repassa propriedades e referência **[OBRIGATÓRIA]**

O componente de botão, campo e link do sistema aceita e repassa os atributos do elemento nativo e expõe a
referência a ele. Fechar essa porta parece disciplina e é o oposto.

Consequência concreta: o botão do sistema que não repassa o tipo do elemento não pode ser o botão de envio de
um formulário, e o campo que não expõe referência não pode receber foco programático depois de um erro de
validação — que é justamente o que `UXI-052` e `UXI-047` exigem. O resultado é cada tela recriando o
componente com elemento nativo, perdendo tudo o que `FRT-020` e `FRT-025` garantiam.

---

## Capítulo 9.12 — Governança

### DSY-064 — Um caminho único de contribuição, com revisor nomeado **[OBRIGATÓRIA]**

O caminho é escrito e curto: onde se propõe, o que a proposta contém (caso de uso, contagem de ocorrências,
anatomia, variantes, estados), quem revisa, e qual o prazo de resposta. Prazo de resposta faz parte do
caminho.

Sem prazo declarado, a contribuição não é rejeitada: ela é abandonada, e a peça nasce local e permanente. O
custo de um caminho de contribuição lento é sempre pago em divergência, nunca em espera.

### DSY-065 — O que o produto precisa e o sistema não tem nasce local, com dono e prazo **[OBRIGATÓRIA]**

A resposta correta a "o sistema não tem isso" não é bloquear o produto nem adicionar às pressas: é construir
local, marcado como candidato, com dono e data de revisão. Se o limiar de `DSY-004` for atingido, sobe. Se
não, permanece local sem culpa.

Bloquear o produto até o sistema evoluir ensina o time a não perguntar, e adicionar sob pressão de prazo põe
no catálogo uma peça desenhada para um caso — que é a causa de `DSY-061` ser violada depois. Ambos os erros
custam mais que a permanência local declarada.

### DSY-066 — Mudança de aparência é mudança incompatível **[OBRIGATÓRIA]**

Alterar o valor de um token semântico, a altura de um controle ou o comportamento de um estado muda o produto
de todos os consumidores. Isso é incremento maior no versionamento do pacote, com registro do que muda
visualmente e onde olhar.

Tratar mudança visual como correção é o que produz o incidente clássico: uma atualização de rotina de
dependência altera a altura do campo em 2 px, a tabela de conciliação perde uma linha por tela, e ninguém
relaciona a queixa do cliente à atualização — porque o registro de mudanças dizia "ajustes visuais". O
princípio de contrato versionado é `ARC-026`; aqui ele se aplica a uma superfície que raramente é tratada
como contrato.

### DSY-067 — Depreciação tem substituto, prazo e uso medido **[OBRIGATÓRIA]**

Um componente ou token depreciado continua funcionando, avisa em tempo de build, aponta o substituto e tem
data. A remoção acontece quando o uso medido chega a zero, não quando a data passa.

Remover antes de medir quebra o consumidor que não acompanhou, e o consumidor quebrado aprende a fixar a
versão — deixando de receber correções de acessibilidade e de contraste. Depreciação anunciada e medida antes
da remoção é a mesma disciplina de `BAK-036` aplicada ao sistema visual.

### DSY-068 — A divergência entre o sistema e a produção é medida, não presumida **[OBRIGATÓRIA]**

Uma verificação periódica e automática que reporta, no mínimo: valores literais de cor, espaço e tipografia
fora da camada de tokens (`PLB-031`), referências a tokens primitivos fora da definição de tema (`DSY-007`),
usos da propriedade de escape (`DSY-062`), e componentes locais que duplicam padrão do catálogo (`FRT-022`).

Adoção presumida é a quarta causa de fracasso de design system, e é a única que se resolve com uma linha de
pipeline. Sem a medição, a única evidência de divergência é a tentativa de mudar uma cor — que é o momento
mais caro possível para descobrir. O número reportado tem limiar e reação declarada, como toda métrica
(`PRF-038`).

### DSY-069 — O catálogo é executável e é a fonte de verdade da documentação **[RECOMENDADA]**

A documentação de cada componente é gerada do código e inclui exemplos que rodam, com todas as variantes e
estados navegáveis. Documento estático mantido à parte divergirá do código, e a divergência é descoberta pelo
consumidor que seguiu o documento.

O catálogo executável tem um segundo retorno, maior que a documentação: é onde a matriz de `DSY-059` é
verificada, onde o teclado é percorrido, e onde o tema escuro e a variante compacta são inspecionados sem
precisar de uma tela do produto que os use.

---

## Padrões reutilizáveis

**Escala perceptual com garantia de par.** Construa cada matiz sobre um espaço de cor perceptualmente
uniforme, com passos de luminosidade regulares, e publique a tabela de pares garantidos (`passo N` sobre
`passo N+K` satisfaz texto normal; `N+J` satisfaz componente). Um teste no pipeline recalcula a tabela a cada
mudança de paleta. *Use quando* o produto tem tema e mais de um par de cor por estado. *Não use quando* o
sistema tem menos de dez cores e um único tema — a tabela manual é suficiente e mais barata (`DSY-016`).

**Par superfície–conteúdo.** Exponha superfície e o conteúdo sobre ela como um par indivisível, e faça os
componentes aceitarem o nome do par. Elimina a decisão de contraste do consumidor por construção
(`DSY-017`). *Não use quando* o componente é puramente estrutural e não pinta fundo.

**Tabela de profundidade.** Uma tabela com poucos níveis nomeados que define, por nível, superfície, sombra,
separador e valor de empilhamento — para os dois temas. É o antídoto ao empilhamento por tentativa
(`DSY-047`). *Use sempre* que o produto tem menu suspenso, diálogo e cabeçalho fixo, o que é praticamente
todo SaaS.

**Variante de densidade em dois modos.** Dois modos apenas — confortável e compacto — com a escala de espaço
interno e a altura de controle derivadas do modo, e o alvo de toque preservado (`DSY-027`, `DSY-028`).
*Não use* três ou mais modos: o terceiro nunca é testado por completo.

**Ponte de token para o legado.** Ao introduzir tokens num produto existente, mapeie os valores literais
encontrados para o token semântico mais próximo e substitua por módulo, com captura visual antes e depois.
Um alias temporário do valor antigo para o token novo permite a migração incremental sem mudança visual.
*Use quando* a adoção não pode ser feita de uma vez. *Não use* como estado permanente: o alias tem prazo, sob
`DSY-014`.

**Relatório de divergência.** Uma varredura que produz um número por categoria, com tendência entre execuções,
publicada onde o time vê. É o que transforma `DSY-068` de intenção em prática. *Use sempre.* O relatório sem
limiar e sem reação é decoração.

**Candidato local marcado.** Uma convenção de diretório e um comentário com dono e data para peças que estão
abaixo do limiar de promoção. Torna visível o que é candidato e o que é dívida, e alimenta a revisão
periódica de `DSY-065`.

---

## Matrizes de decisão

**Onde a necessidade nova deve morar**

| Situação | Resposta | Gatilho de mudança |
| --- | --- | --- |
| Um caso, um lugar, comportamento novo | Local, marcado como candidato (`DSY-065`) | Atingir o limiar de `DSY-004` |
| Mesmo componente, conjunto fechado de opções | Variante, com regra de uso (`DSY-060`) | Mais de ~5 variantes: revisar se é outro componente |
| Mesmo componente, conteúdo diferente | Composição por partes nomeadas (`DSY-061`) | — |
| Comportamento de interação diferente | Componente novo (`FRT-022`) | — |
| Só a aparência difere, sem regra que a justifique | Nada. Use o existente (`UXI-001`, `CON-013`) | — |

**Qual nível de token usar**

| O valor... | Nível | Motivo |
| --- | --- | --- |
| é um ponto da paleta ou da escala | primitivo | vocabulário interno do tema (`DSY-007`) |
| tem um papel na interface | semântico | é o que muda com tema e densidade |
| é dimensão própria de uma peça | de componente | não pertence a nenhuma escala global (`DSY-009`) |
| difere do semântico só nesta tela | nenhum | é sobreposição; ver `DSY-062` |

**Separador entre conteúdo e superfície**

| Contexto | Mecanismo | Por quê |
| --- | --- | --- |
| Mesmo nível de profundidade, agrupamento | espaço (`DSY-025`) | mais leve, e é o sinal que o usuário já lê |
| Mesmo nível, limite preciso necessário | borda de 1 unidade | tabela, campo, célula |
| Nível acima, tema claro | sombra do nível (`DSY-046`) | comunica flutuação |
| Nível acima, tema escuro | superfície mais clara | sombra não é perceptível (`DSY-021`) |

**Mecanismo de feedback:** ver a tabela de `DSY-053`, que é a matriz canônica.

---

## Fluxo de trabalho

Do mais interno para o mais externo. Cada passo depende do anterior, e inverter a ordem é a causa da maioria
dos sistemas que precisam ser refeitos.

1. **Primitivos.** Paleta com escalas, base de espaço, escala tipográfica, escala de raio, durações. Nada
   nomeado por papel ainda. A garantia de contraste de `DSY-016` é construída aqui, porque depois é tarde.
2. **Semânticos.** Papéis nomeados, os pares de `DSY-017`, a tabela de profundidade, e todos os temas com o
   mesmo conjunto de chaves (`DSY-012`).
3. **Geração.** A fonte única produz os artefatos por plataforma (`DSY-011`), e o pipeline passa a verificar
   contraste e paridade de chaves.
4. **Primitivas de layout.** Pilha, grade, contêiner, pontos de quebra nomeados pela necessidade
   (`DSY-038`). Antes dos componentes, porque os componentes vão compor sobre elas.
5. **Componentes, por ordem de frequência de uso.** Para cada um: anatomia (`DSY-058`), variantes com regra
   (`DSY-060`), matriz variante × estado no catálogo executável (`DSY-059`, `DSY-069`), teclado percorrido.
6. **Adoção.** Um módulo do produto por vez, com a ponte de token e captura visual antes e depois. A varredura
   de divergência entra no pipeline junto com o primeiro módulo, não no fim (`DSY-068`).
7. **Governança em operação.** Caminho de contribuição publicado com prazo (`DSY-064`), revisão periódica dos
   candidatos locais, relatório de divergência com limiar e reação.

Para construir uma tela usando o sistema, o passo a passo é o playbook de tela — `PLB-030` e `PLB-031` são os
pontos onde ele encontra este volume.

---

## Exemplos de implementação

**Vazamento de primitivo na tela (`DSY-007`, `DSY-010`)**

```css
/* Ruim — DSY-007: o painel de cobrança consome primitivos e o tema escuro não o alcança */
.painel-cobranca__aviso {
  color: var(--cinza-900);
  background: var(--ambar-100);
  border-radius: 5px;              /* fora da escala de raio */
  padding: calc(var(--espaco-3) + 2px);  /* DSY-010: valor fora da escala com disfarce de token */
}

/* Bom */
.painel-cobranca__aviso {
  color: var(--estado-atencao-texto);
  background: var(--estado-atencao-superficie);
  border-radius: var(--raio-contêiner);
  padding: var(--espaco-interno-bloco);
}
```

**Contraste transferido para a tela (`DSY-017`)**

```tsx
// Ruim — DSY-017: duas cores independentes, e a decisão de contraste vai para cada consumidor
<Etiqueta cor="ambar-300" corDoTexto="cinza-500">Cobrança pendente</Etiqueta>

// Bom
<Etiqueta tom="atencao">Cobrança pendente</Etiqueta>
```

**Escape aberto e não medido (`DSY-062`)**

```tsx
// Ruim — DSY-062: sobreposição livre; o botão fica fora de qualquer varredura e de qualquer tema
<Botao style={{ background: '#c0392b', padding: '6px 10px' }}>
  Cancelar assinatura
</Botao>

// Bom
<Botao tom="destrutivo" densidade="compacta">Cancelar assinatura</Botao>
```

**Movimento reduzido tratado como ausência (`DSY-051`)**

```css
/* Ruim — DSY-051: o painel do inquilino passa a aparecer instantâneo, sem sinal de origem */
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}

/* Bom — a variante troca deslocamento por opacidade, e a duração encurta sem desaparecer */
:root {
  --duracao-entrada-superficie: 180ms;
  --deslocamento-entrada: 8px;
}
@media (prefers-reduced-motion: reduce) {
  :root {
    --duracao-entrada-superficie: 80ms;
    --deslocamento-entrada: 0px;
  }
}
```

**Nível de cabeçalho escolhido pelo tamanho (`DSY-030`)**

```tsx
// Ruim — DSY-030: o nível do documento foi escolhido porque o tamanho estava certo
<h4>Itens do pedido</h4>

// Bom — estrutura e aparência são declaradas separadamente
<Titulo nivel={2} papel="titulo-de-secao">Itens do pedido</Titulo>
```

**Varredura de divergência (`DSY-068`)**

```bash
# Valores literais de cor e de dimensão fora da camada de tokens
rg --glob 'src/**/*.{ts,tsx,css}' --glob '!src/design-system/tokens/**' \
   -e '#[0-9a-fA-F]{3,8}\b' -e '\b[0-9]+px\b' --count-matches

# Primitivos consumidos fora da definição de tema
rg --glob 'src/**' --glob '!src/design-system/tokens/**' \
   -e 'var\(--(cinza|azul|ambar|vermelho|verde)-[0-9]{3}\)' --count-matches

# Usos da propriedade de escape
rg --glob 'src/**/*.tsx' -e '<[A-Z][A-Za-z]*[^>]*\b(style|className)=' --count-matches
```

Os três números vão para o relatório com tendência entre execuções. Número sem limiar e sem reação declarada
não muda comportamento.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Componentes sem camada de token | Tema impossível; a descoberta acontece com prazo já assumido |
| Tela consumindo token primitivo | Fica fora do tema para sempre, e a varredura não distingue do uso legítimo |
| Token semântico com valor literal | Sai da escala sem sair da nomenclatura; diverge na próxima revisão da paleta |
| Nome de token pela aparência | Mente na primeira mudança de marca, e quem lê acredita no nome |
| Chave ausente em um dos temas | Contraste insuficiente que passa por toda revisão feita no tema padrão |
| Contraste verificado por combinação, não por construção | Cada par novo é uma verificação que alguém esquece |
| Tema escuro por inversão global | Logotipo, gráfico e cor crítica quebram; a tabela de contraste deixa de valer |
| Duas bases de espaçamento concorrentes | Equivale a não ter escala: a verificação deixa de discriminar |
| Densidade resolvida por tela | Cinco densidades não nomeadas; escolha do usuário fica inviável |
| Modo compacto que encolhe o alvo de toque | Ação destrutiva acionada por engano em tela de toque |
| Ponto de quebra com nome de dispositivo | Envelhece por construção; ninguém ousa mudar o valor |
| Consulta pela largura da janela em componente reutilizável | Quebra na primeira reutilização em painel estreito |
| Propriedade de reordenação visual na primitiva de layout | Ordem de foco salta, e nenhuma revisão visual detecta |
| Empilhamento por tentativa, sem tabela | Menu atrás do cabeçalho aqui, na frente do diálogo lá |
| Sombra decorativa em elemento que não flutua | Quando tudo flutua, nada flutua |
| Valor monetário animado contando até o total | Impede a leitura exatamente onde a precisão importa |
| Animação antes da primeira evidência de resposta | Percepção de lentidão e clique repetido |
| Movimento reduzido implementado como desligar tudo | Perde a continuidade que o movimento existia para dar |
| Erro de validação em notificação transitória | O usuário não consegue reler qual campo falhou |
| Modal como recipiente genérico | Perda de contexto, formulário sem espaço, modais encadeados |
| Variante nova sem regra de quando usar | Escolhida por aparência; a distinção se dissolve em meses |
| Componente com dezenas de propriedades de aparência | O dono do sistema vira gargalo de todo o produto |
| Componente do sistema que não repassa a referência nativa | Cada tela recria a peça e perde foco, teclado e papel |
| Escape de estilo sem contagem | Em dois anos o sistema descreve a minoria do que está em produção |
| Mudança visual publicada como correção | Regressão de layout que ninguém relaciona à atualização |
| Sistema copiado entre repositórios | Uma correção de foco alcança um produto e os outros seguem com o defeito |
| Adoção presumida | A divergência é descoberta no momento mais caro: ao tentar mudar uma cor |

---

## Checklist

- [ ] As quatro camadas existem: tokens, componentes, documentação, governança. (`DSY-002`)
- [ ] Dono nomeado e fonte única declarados. (`DSY-003`)
- [ ] Limiar de promoção ao sistema escrito, com número. (`DSY-004`)
- [ ] Consumido como pacote versionado, não copiado. (`DSY-005`)
- [ ] Três níveis de token separados, com consumidor declarado por nível. (`DSY-006`)
- [ ] Zero referências a token primitivo fora da definição de tema. (`DSY-007`)
- [ ] Zero valores literais dentro de token semântico e zero `calc` de escape. (`DSY-010`)
- [ ] Conjunto de chaves idêntico em todos os temas, verificado no pipeline. (`DSY-012`)
- [ ] Tabela de pares de contraste garantidos por construção, testada no pipeline. (`DSY-016`)
- [ ] Componentes aceitam par de cor, não duas cores independentes. (`DSY-017`)
- [ ] Toda cor de estado é entregue com ícone e rótulo na mesma peça. (`DSY-019`)
- [ ] Tema escuro com escala própria de superfícies, não inversão. (`DSY-021`)
- [ ] Escolha de tema do usuário persiste e é aplicada antes da primeira pintura. (`DSY-023`)
- [ ] Base única de espaçamento; espaços verticais de uma tela cabem na escala. (`DSY-024`)
- [ ] Densidade é variante do sistema, e a compacta preserva o alvo de toque. (`DSY-027`, `DSY-028`)
- [ ] Papel tipográfico e nível de cabeçalho declarados separadamente. (`DSY-030`)
- [ ] Pesos declarados existem como arquivo carregado; substituta com métricas ajustadas. (`DSY-033`, `DSY-036`)
- [ ] Pontos de quebra nomeados pela necessidade do conteúdo. (`DSY-038`)
- [ ] Nenhuma primitiva de layout expõe reordenação puramente visual. (`DSY-040`)
- [ ] Tabela única de profundidade cobrindo superfície, sombra, separador e empilhamento. (`DSY-047`)
- [ ] Lista fechada do que anima e do que nunca anima. (`DSY-049`)
- [ ] Variante de movimento reduzido definida token por token e testada. (`DSY-051`)
- [ ] Critério de uso escrito para cada mecanismo de feedback. (`DSY-053`)
- [ ] Matriz variante × estado gerada e verificada no catálogo executável. (`DSY-059`, `DSY-069`)
- [ ] Usos da propriedade de escape contados, com tendência e limiar. (`DSY-062`, `DSY-068`)

---

## Prompt do volume

```
ROLE: Design System engineer, operating under EOS Volume 09 (`DSY`).

MISSION
Guarantee that the product's visual and interaction decisions are made once, in the system, and that the
system still describes what is actually in production. Two failures matter most: a token architecture that
makes theming impossible, and adoption that was assumed instead of measured.

LOAD
- `AGENTS.md`, `agents/_shared/core-contract.md`, `agents/_shared/output-schemas.md`
- `00-constituicao-da-engenharia.md`, `09-design-system.md`
- `04-frontend.md` and `08-ux-premium.md` by reference only — never restate their rules, cite the ID
- The filled project profile. Without it, thresholds marked `[perfil]` are undefined: propose it first.

MANDATORY SEQUENCE — do not skip forward
1. INVENTORY. Locate the system: token source, component directory, docs, governance document. Report which
   of the four layers are missing before judging anything.
2. TOKEN ARCHITECTURE. Are the three levels separated? Do components and screens consume semantic tokens
   only? Do all declared themes carry the same key set? Are there literal values inside semantic tokens?
3. CONTRAST BY CONSTRUCTION. Is there a published guaranteed-pair table, verified in the pipeline, or is
   contrast checked per combination? Report the mechanism, not a sample of passing pairs.
4. SCALES. Spacing base, type scale and its roles, radius, elevation and stacking table, motion durations.
   For each: is it closed, and does the product stay inside it?
5. BREAKPOINTS AND LAYOUT PRIMITIVES. Named by content need or by device? Any visual-only reorder property?
6. COMPONENT CATALOGUE. For the components used most: anatomy, variant rules, and the variant x state
   matrix. Report missing states per variant, not per component.
7. FEEDBACK MECHANISMS. Is there a written use criterion? Find field errors in transient mechanisms and
   modals used as generic containers.
8. DIVERGENCE, MEASURED. Run the scans: literal values outside the token layer, primitives consumed outside
   theme definition, escape-property usage, local components duplicating catalogue patterns. Numbers, with
   the command that produced them.
9. GOVERNANCE. Named owner, contribution path with a response deadline, deprecation with measured usage,
   versioning that treats appearance change as breaking.

EVIDENCE
Every FINDING cites `path:line` or the output of a command you ran. No citation means `HYPOTHESIS`.
Report counts, never impressions: "412 literal hex values outside the token layer, 87 of them in the billing
module" — not "widespread hardcoded colours".

NOT YOUR JOB
Usability principles, error copy, flows and accessibility norms (cite Volume 08 by ID; do not re-derive).
Client state, cache and bundle budget (Volume 04). Rendering strategy and library choice (Volume 02, `SEL`).
Visual taste: a radius or shade you would have chosen differently is not a finding.

OUTPUT
Use the report format in the "Verificação obrigatória de saída" section of `09-design-system.md`, verbatim.
Separate MUST-FIX from OPPORTUNITY. Every unfixed OPPORTUNITY goes to the backlog with a promotion trigger.
State which of the nine sequence steps you did not cover, and why.

STOP AND ESCALATE WHEN
- Fixing the token architecture requires changing every screen: that is a migration, propose it as one.
- The product has two competing systems in production: this is a decision, not a finding. Needs an ADR.
- Contrast cannot be satisfied with the current brand palette: the palette is the decision, escalate it.
```

---

## Critérios de aceite

Um módulo passa neste domínio quando **todas** as afirmações abaixo são verdadeiras e verificadas, não
presumidas:

1. Nenhum valor literal de cor, espaço, tipografia, raio ou duração no código do módulo, e a verificação que
   prova isso roda no pipeline. (`DSY-010`, `PLB-031`)
2. Nenhuma referência a token primitivo fora da definição de tema. (`DSY-007`)
3. Todo tema declarado carrega o conjunto completo de chaves semânticas, verificado automaticamente.
   (`DSY-012`)
4. Todo par de cor usado pelo módulo pertence à tabela de pares garantidos, e a tabela é testada.
   (`DSY-016`, `DSY-017`)
5. Cada componente do sistema usado pelo módulo tem a matriz variante × estado verificada, incluindo foco,
   desabilitado, carregando e erro. (`DSY-059`, `FRT-024`)
6. Cada mecanismo de feedback usado no módulo corresponde ao critério declarado, e nenhum erro de campo vive
   em mecanismo transitório. (`DSY-053`, `DSY-054`)
7. A contagem de usos da propriedade de escape no módulo é conhecida, e cada uso tem justificativa escrita ou
   um item de backlog com gatilho de promoção. (`DSY-062`, `AUD-036`)
8. Toda peça local do módulo que duplica padrão do catálogo está marcada como candidata, com dono e data, ou
   já foi promovida. (`DSY-065`, `FRT-022`)
9. O módulo foi percorrido nos dois temas e nas duas densidades, com teclado, e em zoom 200%. (`DSY-021`,
   `DSY-027`, `PLB-038`)

Reprovação em qualquer um dos itens 1 a 4 é reprovação do domínio: são os que tornam impossível corrigir os
demais de forma central.

---

## Verificação obrigatória de saída

```
## Camadas do sistema
| Camada | Existe | Onde | Lacuna |
| Tokens | | | |
| Componentes | | | |
| Documentação | | | |
| Governança | | | |

## Arquitetura de tokens
Três níveis separados: <sim/não> | Fonte única gerando plataformas: <sim/não>
| Verificação | Resultado | Comando/evidência |
| Primitivos consumidos fora do tema | <n ocorrências> | |
| Valor literal dentro de token semântico | <n> | |
| Paridade de chaves entre temas | <ok/faltam n> | |

## Contraste
Mecanismo: <garantido por construção | verificado por par | não verificado>
Tabela de pares garantidos: <onde> | Testada no pipeline: <sim/não>
| Par em uso fora da tabela | Onde | Razão de contraste | Severidade |

## Escalas
| Escala | Fechada | Valores fora dela (n) | Evidência |
| Espaçamento | | | |
| Tipografia | | | |
| Raio | | | |
| Profundidade/empilhamento | | | |
| Duração e curva | | | |

## Catálogo — matriz variante x estado
| Componente | Variantes | Estados verificados | Estados ausentes | Severidade |

## Feedback
| Evento | Mecanismo atual | Mecanismo correto (DSY-053) | Consequência |

## Divergência medida
| Categoria | Contagem | Tendência | Limiar | Reação declarada |
| Valores literais fora dos tokens | | | | |
| Primitivos fora do tema | | | | |
| Usos da propriedade de escape | | | | |
| Componentes locais duplicando o catálogo | | | | |

## Governança
Dono nomeado: <quem> | Caminho de contribuição: <onde> | Prazo de resposta: <qual>
Versionamento trata aparência como incompatível: <sim/não>
| Peça depreciada | Substituto | Uso medido | Prazo |

## Não verificado
| Item | Por quê | Como verificar |
```
