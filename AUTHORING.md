# AUTHORING — contrato de autoria do EOS

Este documento existe por um motivo específico e mensurável: **um livro técnico de 25 volumes não pode ser
escrito com o livro inteiro na memória de quem escreve.** Nenhum autor, humano ou modelo, mantém 200 mil
palavras em contexto ativo. Sem um contrato explícito, o volume 20 contradiz o volume 3, usa outro vocabulário,
repete a mesma norma com palavras diferentes, e o resultado é uma pilha de textos com capa comum.

A solução não é memória. É a mesma solução que o próprio EOS prescreve para código: **fonte única de verdade,
fronteiras declaradas, e verificação mecânica.** Um autor não precisa lembrar o volume 3; precisa saber que a
norma de contrato de API mora lá, citá-la por ID, e nunca reafirmá-la.

Quem escreve ou revisa qualquer volume lê este documento primeiro. Sem exceção.

---

## 1. As cinco leis da autoria

### A-001 — Uma norma tem exatamente um lar **[IMUTÁVEL]**

É `ARC-011` aplicado ao próprio livro. Se a regra sobre autorização por objeto vive em `SEC-004`, nenhum outro
volume a reafirma. Volumes que precisam dela **citam o ID**: "autorize por objeto (`SEC-004`)".

Reafirmar cria duas fontes de verdade. Duas fontes de verdade divergem na primeira revisão de uma delas, e
divergência num manual normativo é pior do que ausência: o leitor obedece a versão errada de boa-fé.

**Teste antes de escrever qualquer regra nova:** procure o conceito em [`RULES-INDEX.md`](RULES-INDEX.md). Se
existir, cite. Se existir mas estiver incompleta, **estenda a regra existente no volume dela** — não escreva
uma nova no seu.

### A-002 — Cada volume declara sua fronteira, incluindo o que não cobre **[IMUTÁVEL]**

Todo volume abre com um bloco `Fronteira` que diz o que é dele e o que pertence a outro volume, com link. É o
dispositivo que impede sobreposição, e ele é verificável: se dois volumes reivindicam o mesmo tema, um dos dois
está errado e a fronteira revela qual.

### A-003 — Toda regra é verificável por um terceiro **[IMUTÁVEL]**

Uma regra que não pode ser confrontada com o código não é regra: é opinião com número. Antes de escrever, e a
resposta precisa ser sim para as três:

1. Um revisor consegue apontar `arquivo:linha` que a viola?
2. Duas pessoas competentes chegariam ao mesmo veredito sobre um caso concreto?
3. Existe um caso real em que ela **não** se aplica? (Se não existe, é vaga demais para ser útil.)

Proibido: "use boas práticas", "mantenha o código limpo", "prefira soluções elegantes", "evite complexidade
desnecessária". Todas falham no teste 2.

### A-004 — Escreva a consequência, não a instrução **[OBRIGATÓRIA]**

O leitor cumpre a regra que entende. Toda regra explica **o que acontece se for violada**, em termos de
consequência concreta — dado perdido, usuário bloqueado, vazamento, indisponibilidade, custo — e não em termos
de virtude.

```
Ruim:  Sempre valide entrada no servidor. É uma boa prática de segurança.
Bom:   Valide no servidor. Validação de cliente é experiência do usuário, não controle:
       o atacante fala direto com a sua API e nunca executa o seu JavaScript.
```

A segunda versão é obedecida por quem entendeu. A primeira é obedecida por quem confia, e ignorada sob pressão
de prazo.

### A-005 — Nenhum enchimento **[IMUTÁVEL]**

A meta de páginas é consequência da profundidade, nunca objetivo. Proibido, e a revisão rejeita:

- Reafirmar em prosa o que a tabela ao lado já disse.
- Parágrafo de transição que não acrescenta ("Agora que entendemos X, vamos falar de Y").
- Enumerar sinônimos de uma ideia para ocupar espaço.
- Exemplo que ilustra o óbvio (`if` com condição invertida).
- Repetir a mesma regra em três volumes para "reforçar".
- Preencher uma seção obrigatória com conteúdo vazio em vez de declarar `N/A — motivo`.

Um volume de 40 páginas densas é superior a um de 120 diluídas, e `AUD-001` trata falha por excesso como igual
à falha por omissão. Se um volume não tem substância para o alvo de páginas, **o alvo estava errado** — reporte
em vez de encher.

---

## 2. Anatomia obrigatória de um volume

Todo volume tem estas seções, nesta ordem. Seção sem conteúdo real recebe `N/A` com uma frase de justificativa
— nunca é preenchida com placeholder.

```
# <emoji> Volume NN — <Título>

Prefixo: `XXX` · Regras: XXX-001 a XXX-0NN · Papel: <link para o papel dono em agents/>

<Abertura: 2 a 4 parágrafos. Por que este volume existe, qual erro caro ele previne,
 e o que muda no trabalho de quem o lê. Nunca "este volume aborda...".>

**Fronteira.** <O que é deste volume. O que pertence a outro, com link e motivo.>

---

## Fundamentos

<A teoria mínima necessária para as regras não parecerem arbitrárias. Não é aula:
 é o modelo mental que faz o leitor derivar a regra certa num caso que o livro não previu.
 Aqui entram os conceitos, os trade-offs estruturais e a história de por que o padrão existe.>

## Capítulo NN.1 — <Tema>

<Prosa introdutória do capítulo quando ela acrescenta contexto. Opcional.>

### XXX-001 — <Enunciado imperativo e curto> **[NÍVEL]** · `SEV`

<Corpo: o que a regra exige, por que, e a consequência de violá-la.
 Exemplo bom e ruim quando o contraste esclarecer.
 Referências a outras regras por ID.>

## Padrões reutilizáveis

<Soluções nomeadas e prontas para copiar, com quando usar e quando não usar.
 Esta seção é o que torna o volume operacional em vez de apenas normativo.>

## Matrizes de decisão

<Tabelas de escolha entre alternativas legítimas, com o critério objetivo e o gatilho de mudança.
 N/A quando o volume não envolve escolha.>

## Fluxo de trabalho

<A ordem de execução das tarefas deste domínio, do mais interno para o mais externo.
 Aponta para o playbook correspondente quando existir, em vez de duplicá-lo.>

## Exemplos de implementação

<Código real, agnóstico de framework quando possível, com o defeito e a correção.
 Cada exemplo prova uma regra específica, citada por ID.>

## Antipadrões

| Antipadrão | Consequência |

## Checklist

<Itens verificáveis, cada um rastreável a uma regra por ID. Ver limite em A-011.>

## Prompt do volume

<Prompt em inglês, pronto para uso, que faz um agente aplicar este volume.
 Ver seção 5.>

## Critérios de aceite

<O que precisa ser verdade para um módulo passar neste domínio.
 Distinto do checklist: aceite é o veredito, checklist é o caminho.>

## Verificação obrigatória de saída

<Bloco de código com o formato exato do relatório que este volume exige.>
```

### A-006 — Níveis de obrigatoriedade têm significado fixo **[IMUTÁVEL]**

| Nível | Significado | Quem pode abrir exceção |
| --- | --- | --- |
| `[IMUTÁVEL]` | Nunca se viola. Não existe contexto que justifique | Ninguém. Nem o usuário pedindo |
| `[OBRIGATÓRIA]` | Viola-se apenas com aceitação de risco registrada, com nome de pessoa | Humano identificado, por escrito (`CON-042`) |
| `[RECOMENDADA]` | O padrão. Divergir exige justificativa na entrega, não aprovação | O autor da mudança, declarando |

Severidade (`S0` a `S3`) aparece só quando a violação tem severidade **fixa** independente de contexto. A
maioria das regras não tem: a severidade sai da matriz de `CON-035`.

### A-007 — IDs são estáveis para sempre **[IMUTÁVEL]**

Um ID publicado nunca é reciclado, nunca é renumerado, nunca muda de significado. Regra que deixa de valer é
marcada `[REVOGADA]` no lugar, com data e o ID que a substitui — o número não é reaproveitado.

Isso não é burocracia: o ID é citado em revisões, ADRs, commits e relatórios de auditoria. Renumerar invalida
retroativamente todo registro histórico que o citou.

Regras novas entram **no fim da faixa do prefixo**, mesmo que o lugar natural no texto seja o meio.

### A-008 — Numeração contínua e um prefixo por assunto **[OBRIGATÓRIA]**

Sem lacunas, sem duplicatas. [`scripts/build-rules-index.py`](scripts/build-rules-index.py) verifica e falha.
Um volume pode hospedar mais de um prefixo quando o livro exige (o volume de Arquitetura hospeda `ARC` e
`SEL`), mas cada prefixo tem faixa contínua no repositório inteiro.

---

## 3. Voz

O EOS é escrito como manual interno de uma empresa de engenharia madura, para leitores competentes sob pressão
de prazo. Não é livro didático, não é documentação de API, não é post de blog.

### A-009 — Regras de voz **[OBRIGATÓRIA]**

**Faça:**

- Frase declarativa e direta. Sujeito, verbo, consequência.
- Segunda pessoa para instrução ("valide no servidor"), terceira para descrição de sistema.
- Tabela para o que é enumerável; prosa para o que exige raciocínio.
- Números concretos onde existirem, com `[perfil]` marcando o que depende do projeto.
- Nomear o erro caro. "É o defeito que mais aparece em revisão de checkout."
- Português técnico, com o termo em inglês entre parênteses na primeira ocorrência quando o termo em inglês for
  o de uso corrente: "contrapressão (backpressure)".

**Não faça:**

- Hedging. Não escreva "talvez seja interessante considerar". A regra vale ou não vale.
- Elogio ao próprio material ("este poderoso framework").
- Metalinguagem ("neste capítulo veremos", "como vimos anteriormente").
- Emoji fora do título do volume.
- Primeira pessoa do plural moralizante ("devemos sempre nos preocupar com").
- Exclamação. Em nenhum lugar.
- Superlativo vazio ("extremamente importante", "absolutamente crítico"). Se é crítico, diga a consequência.

### A-010 — Exemplos provam uma regra e são realistas **[OBRIGATÓRIA]**

Todo exemplo cita o ID que ele demonstra. `foo`, `bar` e `Test1` são proibidos: use o domínio de um SaaS real —
pedido, assinatura, inquilino, cobrança, catálogo.

Par bom/ruim quando o contraste ensina. O ruim vem primeiro e recebe o comentário do defeito; o bom vem depois
sem comentário elogioso.

```
// Ruim — BAK-011: o cliente decide o próprio papel
const user = await User.create(req.body)

// Bom
const user = await User.create({
  email: input.email,
  name: input.name,
  role: 'member',
})
```

Código em blocos com linguagem declarada. Quando o exemplo depende de framework, diga qual e marque como
ilustração — o núcleo do EOS é agnóstico de stack (`CON-006`).

### A-011 — Checklist tem no máximo 25 itens por volume **[OBRIGATÓRIA]**

Cada item é verificável em minutos e rastreia uma regra por ID. Um checklist de 500 itens é marcado sem ser
lido, e produz `AUD-002` — afirmação não verificada — em escala industrial. Se o domínio parece exigir mais de
25, ele tem subdomínios: divida por contexto de uso, não por acúmulo.

---

## 4. Disciplina de referência cruzada

### A-012 — Cite por ID, com o mínimo de contexto para o leitor não precisar sair **[OBRIGATÓRIA]**

```
Ruim:  Ver SEC-004.
Ruim:  Autorize por objeto: verifique que este usuário pode acessar este registro,
       não apenas que ele tem o papel certo, porque o papel não diz nada sobre
       qual registro. <- reafirmou a regra inteira
Bom:   Autorize por objeto, não por papel (`SEC-004`).
```

Uma cláusula de contexto: suficiente para o leitor seguir sem abrir o link, insuficiente para substituir a
regra original.

### A-013 — Nunca cite um ID que você não verificou **[IMUTÁVEL]**

Confira em [`RULES-INDEX.md`](RULES-INDEX.md) que o ID existe e diz o que você afirma. ID inventado ou
deslocado é a falha mais corrosiva possível neste material: destrói a confiança em todas as outras citações,
inclusive as corretas. [`scripts/check-links.py`](scripts/check-links.py) verifica existência, mas não verifica
se o sentido corresponde — isso é responsabilidade do autor.

### A-014 — Um volume pode discordar de outro, mas então um dos dois muda **[OBRIGATÓRIA]**

Contradição descoberta não é resolvida com nota de rodapé. Escolhe-se a regra correta, corrige-se a outra, e se
a divergência for de decisão estrutural, registra-se um ADR em [`backlog/adr/`](backlog/adr/).

---

## 5. Prompts

Cada volume termina com um prompt operacional. A biblioteca completa vive em [`prompts/`](prompts/), e o
prompt do volume é a versão canônica.

### A-015 — Prompts em inglês; normas em português **[OBRIGATÓRIA]**

Os volumes, checklists e playbooks são em português: são lidos por pessoas. Prompts e contratos de agente são
em inglês, alinhados a [`agents/`](agents/) — é a língua em que os modelos foram majoritariamente treinados
para seguir instrução, e misturar as duas dentro de um prompt degrada aderência.

### A-016 — Prompt referencia o volume, nunca o reproduz **[IMUTÁVEL]**

Um prompt que copia as regras do volume é uma segunda fonte de verdade que envelhece em silêncio. O prompt diz
**como operar**: missão, sequência obrigatória, o que investigar, o formato de saída, e o que **não** é da sua
conta. As normas ele carrega por referência.

### A-017 — Todo prompt declara a sequência e o formato de saída **[OBRIGATÓRIA]**

Prompt sem sequência produz análise em ordem arbitrária, e sem formato de saída produz relatório que ninguém
consegue comparar com o da semana passada.

---

## 6. Como um volume é aceito

### A-018 — Portões de aceite de um volume **[OBRIGATÓRIA]**

Um volume só entra no livro quando todos passam:

| Portão | Verificação | Como |
| --- | --- | --- |
| G-A | Numeração contínua, prefixo íntegro | `scripts/build-rules-index.py` |
| G-B | Links, âncoras e IDs citados existem | `scripts/check-links.py` |
| G-C | Todas as seções da anatomia presentes ou `N/A` justificado | revisão |
| G-D | Nenhuma norma reafirmada de outro volume | busca do conceito no índice |
| G-E | Fronteira declarada e sem sobreposição com volume vizinho | leitura das duas fronteiras |
| G-F | Toda regra passa nos três testes de `A-003` | revisão, por amostragem de 20% |
| G-G | Nenhum item da lista de enchimento de `A-005` | revisão |
| G-H | Prompt presente, em inglês, sem reproduzir normas | revisão |

### A-019 — Volume incompleto é declarado, nunca entregue como pronto **[IMUTÁVEL]**

É `CON-014` aplicado ao livro. Um volume com três capítulos escritos e cinco planejados tem no cabeçalho:

```
> **Estado:** parcial — capítulos NN.1 a NN.3 escritos; NN.4 a NN.8 pendentes.
> Regras já publicadas são estáveis e citáveis (`A-007`).
```

Volume marcado como completo e que não está é a única falha deste contrato que corrompe todo o resto: quem cita
uma regra dele acredita que ela passou pelos portões.

---

## 7. Versionamento

### A-020 — Versionamento semântico do livro **[OBRIGATÓRIA]**

| Mudança | Incremento | Exige ADR |
| --- | --- | --- |
| Regra nova, volume novo, capítulo novo | `MINOR` | Não |
| Correção de texto, exemplo, link | `PATCH` | Não |
| Regra existente muda de exigência, nível ou severidade | `MAJOR` | Sim |
| Regra revogada, prefixo movido, estrutura do livro alterada | `MAJOR` | Sim |

### A-021 — Toda sessão de autoria termina com os scripts verdes **[IMUTÁVEL]**

Rode os dois. Estado quebrado commitado é dívida que a próxima sessão herda sem saber que herdou.

```bash
python3 scripts/build-rules-index.py && python3 scripts/check-links.py
```

---

## Checklist de quem escreve um volume

- [ ] Li a fronteira dos volumes vizinhos antes de começar. (`A-002`)
- [ ] Procurei cada conceito no `RULES-INDEX.md` antes de criar regra nova. (`A-001`)
- [ ] Toda regra passa nos três testes de verificabilidade. (`A-003`)
- [ ] Toda regra tem consequência escrita, não só instrução. (`A-004`)
- [ ] Nenhum parágrafo existe para ocupar espaço. (`A-005`)
- [ ] Todas as seções da anatomia presentes, ou `N/A` justificado. (seção 2)
- [ ] Níveis atribuídos com o significado exato da tabela. (`A-006`)
- [ ] Regras novas no fim da faixa; nenhum ID reciclado. (`A-007`)
- [ ] Nenhuma exclamação, emoji fora do título, ou superlativo vazio. (`A-009`)
- [ ] Exemplos com domínio de SaaS real e ID da regra que provam. (`A-010`)
- [ ] Checklist com no máximo 25 itens, cada um rastreável. (`A-011`)
- [ ] Todo ID citado foi conferido no índice. (`A-013`)
- [ ] Prompt em inglês, com sequência e formato de saída, sem reproduzir normas. (`A-015` a `A-017`)
- [ ] Estado declarado no cabeçalho se o volume estiver parcial. (`A-019`)
- [ ] `build-rules-index.py` e `check-links.py` verdes. (`A-021`)
