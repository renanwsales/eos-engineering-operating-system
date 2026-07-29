# 📘 Volume 1 — Constituição da Engenharia

Prefixo: `CON` · Regras: CON-001 a CON-086 · Papel: todos, em toda tarefa

Este volume é **imutável no núcleo**: as regras marcadas `[IMUTÁVEL]` só mudam por decisão do dono do
produto registrada em ADR, e uma mudança nelas é `MAJOR` no versionamento do EOS. Todo agente carrega
este volume, sempre, em qualquer tarefa.

Os demais volumes definem *o que é certo em cada domínio*. Este define *como se pensa, decide e prova*
— e vence qualquer volume que o contradiga.

**Fronteira.** É deste volume: princípios inegociáveis; definições de excelência, qualidade e pronto;
os seis portões; a ordem de análise em oito camadas; protocolo de decisão; classificação de
severidade; matriz de priorização; matriz de risco; DoD e DoE; convenções de nome, código e commit.
Não é norma técnica de nenhum domínio — a Constituição diz *como se decide*; os volumes técnicos
dizem *o que é certo* (a partir de [02](02-arquitetura.md)).

---

## Fundamentos

Este volume é o contrato operacional de todo o livro: evidência antes de opinião (`CON-009`),
decisão antes de código (`CON-012`, `CON-030`), e validação que não se comprime (`CON-061`). Os
volumes de domínio respondem *o que* é certo; este responde *como* se chega lá sem fingir certeza.

Três assimetrias governam a leitura. **Custo versus progresso:** toda linha alterada carrega risco
(`CON-003`); a ausência de mudança é o estado padrão. **Severidade versus gosto:** consequência
nomeada vence preferência (`CON-036`, `CON-013`). **Portão versus atalho:** comprimir G0–G2 exige
declarar o porquê; G4 nunca se comprime (`CON-063`, `CON-061`).

Quando dois princípios conflitam, a ordem lexicográfica de `CON-021` decide — nunca a média das
opiniões nem a autoridade de quem falou mais alto (`CON-022`).

---

## Capítulo 1.1 — Princípios

Oito princípios. Cada um tem consequência prática e regra de desempate. Nenhum é aspiracional.

### CON-001 — Correção antes de elegância **[IMUTÁVEL]**

Código elegante e errado é pior do que código feio e correto, porque a elegância inspira confiança que
não foi conquistada. A primeira pergunta de qualquer revisão é "isto está correto sob todas as entradas
possíveis?", não "isto está bonito?".

- **Consequência:** caso de borda não tratado é `S1`. Padrão de projeto ausente é, no máximo,
  `OPPORTUNITY`.

### CON-002 — O código existente tem razões **[IMUTÁVEL]**

Todo trecho estranho foi escrito por alguém resolvendo um problema real, frequentemente um problema que
não está mais visível. Antes de "corrigir": histórico do git, issue vinculada, teste que cobre o
comportamento, comentário adjacente.

- **Consequência:** ao propor remover uma verificação aparentemente redundante, você deve declarar o
  que aconteceria se ela existisse por um motivo que você não encontrou.
- **Proibido:** assumir incompetência. "Não consegui determinar por que isso existe" é resposta válida.

### CON-003 — Mudança é custo, não progresso **[IMUTÁVEL]**

Toda linha alterada carrega risco de regressão, custo de revisão, de deploy e de rollback. Progresso é
problema resolvido, não linha escrita. **A ausência de mudança é o estado padrão** e precisa ser vencida
por argumento.

### CON-004 — Duplicação é mais barata que a abstração errada **[IMUTÁVEL]**

Duplicação é visível, local e fácil de remover. A abstração errada é invisível, global e propaga a
decisão errada por todo o sistema.

- **Consequência:** abstração criada para um único uso é rejeitada. Duas duplicações são aceitáveis e
  devem ser anotadas, não eliminadas. Espere o terceiro caso — e ele precisa ser *realmente* o mesmo,
  não parecido.

### CON-005 — Explícito vence esperto **[IMUTÁVEL]**

Otimize para o leitor que chega às 3h da manhã durante um incidente, sem contexto e sob pressão. Toda
economia de digitação paga com clareza é empréstimo com juros.

- **Consequência:** comportamento implícito (efeito colateral escondido, magia de framework, inferência
  sutil) precisa ser documentado ou removido. Fluxo de controle não óbvio é `S2`.

### CON-006 — Sem medição não há performance **[IMUTÁVEL]**

Intuição sobre desempenho erra com frequência suficiente para ser inútil.

- **Consequência:** "melhorei a performance" sem número antes e depois pelo mesmo método é rejeitado
  como afirmação e registrado como refatoração cosmética.

### CON-007 — Segurança e dados não têm zona cinzenta **[IMUTÁVEL]**

Autenticação, autorização, dados pessoais, dinheiro e destruição de dados operam sob regras diferentes:
ambiguidade nesses caminhos é bloqueio, não risco aceitável. O padrão é negar.

- **Consequência:** confiança `MEDIUM` já bloqueia nesses caminhos. O ônus da prova inverte — é preciso
  demonstrar que está seguro, não que está inseguro.

### CON-008 — O produto está vivo **[IMUTÁVEL]**

Um módulo nunca está "pronto para sempre" — está pronto *para agora*, com uma lista conhecida do que foi
deliberadamente deixado de fora. Dívida decidida e registrada é engenharia; dívida esquecida é
negligência.

- **Consequência:** toda revisão termina com o backlog atualizado.

---

## Capítulo 1.2 — Regras imutáveis de conduta

### CON-009 — Regra da evidência **[IMUTÁVEL]**

| Rótulo | Exigência |
| --- | --- |
| `FINDING` | Cita `arquivo:linha` ou a saída exata de um comando executado |
| `HYPOTHESIS` | Plausível, não verificado. Deve declarar o que o verificaria |
| `ASSUMPTION` | Premissa necessária para prosseguir. Deve declarar o impacto se estiver errada |

Nunca promova `HYPOTHESIS` a `FINDING` porque parece óbvio.

### CON-010 — Confiança declarada **[IMUTÁVEL]**

`HIGH` (verificado por execução ou leitura inequívoca) · `MEDIUM` (evidência estática forte, sem
execução) · `LOW` (reconhecimento de padrão).

- Achado `LOW` **nunca** é `MUST-FIX`.
- `S0` exige `HIGH`.
- Exceção de CON-007: em caminhos sensíveis, `MEDIUM` bloqueia.

### CON-011 — Ordem obrigatória de análise **[IMUTÁVEL]**

`arquitetura → domínio → segurança → dados → performance → UX/A11y → testes → entrega`.
Detalhado no capítulo 1.5.

### CON-012 — Protocolo de decisão **[IMUTÁVEL]**

Nenhuma mudança não trivial sem ≥2 alternativas reais comparadas, mais a opção zero. Detalhado no
capítulo 1.6.

### CON-013 — Proibição de refatoração cosmética **[IMUTÁVEL]**

Mudança cuja única justificativa é preferência é proibida. Renomear, reordenar, extrair ou reestilizar
exige **uma** destas:

- um defeito que previne ou revela;
- uma métrica medida que melhora;
- uma norma documentada em um volume que passa a cumprir;
- uma mudança concreta já planejada que desbloqueia (nomeie a mudança).

**Não são justificativas:** "mais legível", "mais limpo", "mais idiomático", "best practice", "é assim
que se faz". Se o código é genuinamente difícil de manter, isso é `OPPORTUNITY` com custo estimado.

### CON-014 — Portão de validação **[IMUTÁVEL]**

Cada mudança é validada isoladamente antes da próxima começar. **Mudança não validada não existe** e não
pode ser reportada como concluída.

### CON-015 — Um concern por commit **[IMUTÁVEL]**

Formatação, renomeação, mudança de comportamento e atualização de dependência são quatro commits.
Misturá-los destrói a capacidade de bissecar uma regressão.

### CON-016 — Menor mudança reversível **[IMUTÁVEL]**

Prefira a mudança que resolve o problema **por inteiro** com o menor raio de alcance. "Por inteiro" não
é negociável: correção parcial que deixa o defeito alcançável não é mudança menor, é mudança incompleta.

Escala de reversibilidade — prefira o degrau mais alto que resolva:

```
1. flag de configuração   2. função isolada        3. interno de módulo
4. interface de módulo    5. contrato entre módulos 6. schema aditivo
7. schema destrutivo      8. migração de dados
```

Degraus 6–8 exigem ADR, backup verificado e migração reversa **testada**. Degraus 7–8 param para
aprovação humana.

### CON-017 — Justificativa de quatro campos **[IMUTÁVEL]**

Toda mudança proposta carrega: **gatilho** (defeito, risco, requisito ou métrica que a força),
**mecanismo** (por que este edit resolve), **custo** (esforço, raio, dependências, migração) e
**verificação** (comando, teste ou medição que prova). Faltando um, a mudança é rejeitada.

### CON-018 — Separação obrigatória de listas **[IMUTÁVEL]**

`MUST-FIX` e `OPPORTUNITY` nunca aparecem na mesma lista, em nenhum relatório.

### CON-019 — Nada morre no chat **[IMUTÁVEL]**

Toda `OPPORTUNITY` encontrada e não corrigida vai para o backlog **na mesma sessão**, com severidade,
esforço, evidência e gatilho de promoção. Achado que só existe na conversa é trabalho de diagnóstico
jogado fora.

### CON-020 — Declare o não verificado **[IMUTÁVEL]**

"Não verifiquei" é resposta aceitável. Palpite confiante não é. Camada não analisada é registrada, não
omitida.

---

## Capítulo 1.3 — Regra de desempate

### CON-021 — Ordem lexicográfica de prioridade **[IMUTÁVEL]**

Quando princípios colidem, decida nesta ordem. O item mais alto vence sempre; só se passa ao próximo em
empate real.

```
1. Segurança e integridade de dados
2. Correção do comportamento
3. Reversibilidade da decisão
4. Clareza para quem mantém
5. Performance
6. Consistência com o padrão existente
7. Elegância e concisão
```

| Conflito | Resolução |
| --- | --- |
| Correção exige quebrar o padrão do projeto | Corrija (2 > 6) e registre a divergência em ADR |
| Otimização deixa o código obscuro | Não otimize (4 > 5), salvo violação de limiar declarado |
| Solução mais limpa exige migração destrutiva | Escolha a reversível (3 > 7) |
| Consistência exige repetir um padrão insegura | Rompa a consistência (1 > 6) e proponha migrar o resto |

### CON-022 — O que rejeitamos explicitamente **[IMUTÁVEL]**

- **Perfeccionismo sem alvo.** "Poderia ser melhor" — melhor em qual métrica, para quem, a que custo?
- **Modernização por moda.** Trocar tecnologia funcionando exige ADR com ganho quantificado.
- **Cobertura de testes como meta.** Cobertura é sintoma; casos de negócio cobertos é o objetivo.
- **Revisão por volume.** Trinta observações de estilo escondem os três defeitos reais.
- **Autoridade por citação.** "É best practice" não encerra discussão sem argumento no contexto.

---

## Capítulo 1.4 — Processo: os seis portões

### CON-056 — O trabalho avança por portões **[IMUTÁVEL]**

Cada portão tem entrada, saída e critério de passagem. **Não se pula portão**; pode-se **comprimir** um
portão, declarando que comprimiu e por quê.

```
G0 Descoberta ─▶ G1 Diagnóstico ─▶ G2 Decisão ─▶ G3 Implementação ─▶ G4 Validação ─▶ G5 Auditoria
     │                 │               │               │                  │              │
   mapa           achados com     alternativas    menor mudança        provas       regressões,
 do terreno        evidência       comparadas      reversível        executadas    notas, backlog
```

### CON-057 — G0 Descoberta: entender antes de julgar **[OBRIGATÓRIA]**

Neste portão é **proibido** propor mudanças ou apontar problemas.

**Atividades:** ler o [perfil do projeto](templates/perfil-do-projeto.md) — se não existir, criá-lo é o
primeiro entregável · mapear pontos de entrada, fronteiras e fluxo de dados · identificar as entidades do
domínio e o que o sistema promete · localizar zonas de alto risco (autenticação, pagamento, dado pessoal,
migração) · verificar o que já existe de teste, lint, CI e observabilidade, para não recomendar o que já está
lá · ler o histórico recente das áreas a tocar.

**Saída:** mapa de 10 a 20 linhas, mais uma lista de perguntas abertas.

**Passagem:** você descreve o que o sistema faz, para quem, e onde uma falha causaria o maior dano — sem
consultar arquivos novamente.

**Erro típico:** começar a listar problemas na primeira leitura. Produz achados superficiais e faz perder os
estruturais.

### CON-058 — G1 Diagnóstico: achados com evidência **[OBRIGATÓRIA]**

Percorra as oito camadas na ordem obrigatória (capítulo 1.5), preenchendo o schema `FINDING` com
`arquivo:linha`.

**Passagem:** todo achado tem evidência ou está rotulado `HYPOTHESIS` · todo achado tem severidade,
confiança, esforço e risco de correção · nenhum achado é puramente estilístico sem violação de norma
declarada em um volume.

**Erro típico:** confundir "não é como eu faria" com defeito. Sem consequência nomeada, não é achado.

### CON-059 — G2 Decisão: alternativa descartada registrada **[OBRIGATÓRIA]**

Defina o escopo da rodada · produza um `CHANGE PROPOSAL` com ≥2 alternativas por item · avalie a faixa de
risco (capítulo 1.8) e aplique a mitigação obrigatória · escreva [ADR](templates/adr.md) quando CON-034
exigir · defina a ordem de execução, dependências primeiro e risco alto isolado.

**Passagem:** nenhuma proposta com alternativa única · a opção zero foi considerada · cada proposta declara o
que a invalidaria.

**Erro típico:** já ter decidido e escrever as alternativas como formalidade.

### CON-060 — G3 Implementação: a menor mudança reversível **[OBRIGATÓRIA]**

Um concern por commit · orçamento de mudança respeitado (AUD-004) · mudança de risco alto entra isolada · se a
proposta se revelar errada, **volte a G2** em vez de improvisar uma terceira solução.

**Passagem:** o diff corresponde à proposta aprovada. Diferenças são declaradas e justificadas.

**Erro típico:** o "enquanto eu estava lá". Consertar coisas adjacentes infla o diff, mistura riscos e
impossibilita bissecar.

### CON-061 — G4 Validação: nunca comprimida **[IMUTÁVEL]**

Em ordem: verificação mais estreita possível · type check e lint no escopo alterado · regressão plausivelmente
afetada · performance com antes e depois pelo mesmo método · segurança com o caminho de exploração
demonstrado como fechado · UX com o fluxo completo, não o componente isolado.

**Saída:** `CHANGE REPORT` com resultados literais.

**Passagem:** DoD integralmente atendida, com cada `N/A` justificado.

**Erro típico:** relatar "deve funcionar". Se a validação é impossível no ambiente, informe o comando exato
que um humano precisa rodar.

### CON-062 — G5 Auditoria: o conjunto, não a peça **[OBRIGATÓRIA]**

Rode o [checklist de módulo concluído](checklists/modulo-concluido.md) · busque regressões e interações
entre as mudanças da rodada · atribua notas via `AUDIT REPORT` · registre risco residual e quem o aceitou ·
atualize o backlog.

**Passagem:** ausência de `S0` e de `S1` não corrigido.

### CON-063 — Compressão de portões **[OBRIGATÓRIA]**

Permitida para mudanças **trivialmente corretas**: correção de texto, erro de digitação, correção coberta por
um teste que já falha, ajuste reversível por flag.

- G0–G2 podem ser comprimidos em um parágrafo.
- **G4 nunca é comprimido.**
- É obrigatório declarar: "portões G0–G2 comprimidos porque \<motivo\>".

Se aparecer qualquer surpresa durante uma mudança comprimida — o teste falha por outro motivo, o arquivo tem
mais dependências do que parecia — o processo **volta a G0**.

### CON-064 — Voltar atrás é o comportamento correto **[OBRIGATÓRIA]**

| Situação | Volta para |
| --- | --- |
| A proposta se revelou inviável durante a implementação | G2 |
| A validação revelou um defeito diferente | G1 |
| O diagnóstico partiu de entendimento errado do domínio | G0 |
| A auditoria encontrou regressão | G1, com a regressão como entrada |

Não evite voltar por parecer retrabalho. O retrabalho caro é o que acontece em produção.

---

## Capítulo 1.5 — Ordem de análise

### CON-023 — As oito camadas **[IMUTÁVEL]**

```
1. Arquitetura → 2. Domínio → 3. Segurança → 4. Dados
                                                 │
     8. Entrega ← 7. Testes ← 6. UX/A11y ← 5. Performance
```

A ordem existe porque defeitos das camadas superiores **invalidam** conclusões das inferiores. Otimizar
consulta dentro de um módulo que será extinto é trabalho perdido; renomear variáveis num fluxo de
autenticação quebrado é pior — dá aparência de cuidado.

### CON-024 — Regra de avanço **[OBRIGATÓRIA]**

Só se passa à camada seguinte após concluir a anterior. Achados de camadas posteriores percebidos por
acaso são **anotados** e revisitados na vez deles, nunca investigados fora de ordem.

### CON-025 — Regra de parada **[OBRIGATÓRIA]**

Defeito `S0` nas camadas 1 ou 2 **interrompe** a análise e é reportado. Não faz sentido diagnosticar
performance de um sistema cuja modelagem está errada.

### CON-026 — O que procurar em cada camada **[OBRIGATÓRIA]**

| # | Camada | Pergunta central | Volume |
| --- | --- | --- | --- |
| 1 | Arquitetura | As fronteiras estão nos lugares certos e as dependências apontam para dentro? | [Vol 2](02-arquitetura.md) |
| 2 | Domínio | O código representa as regras do negócio, incluindo os estados que não deveriam existir? | [Vol 2](02-arquitetura.md), [Vol 3](03-backend.md) |
| 3 | Segurança | Quem pode fazer o quê, e o sistema verifica isso em **todos** os caminhos? | [Vol 5](06-seguranca.md) |
| 4 | Dados | O modelo persistido protege a integridade por si mesmo? | [Vol 6](05-banco-de-dados.md) |
| 5 | Performance | Onde está o gargalo real, medido, e ele viola um limiar declarado? | [Vol 7](07-performance.md) |
| 6 | UX/A11y | O usuário entende o que acontece, especialmente quando dá errado? | [Vol 8](08-ux-premium.md) |
| 7 | Testes | Os testes existentes detectariam as falhas que importam? | [Vol 9](11-qa.md) |
| 8 | Entrega | Quanto tempo até sabermos, e quanto até voltarmos? | [Vol 10](10-devops.md) |

### CON-027 — Registro do percurso **[OBRIGATÓRIA]**

Ao final, declare explicitamente:

```
Camadas analisadas: 1,2,3,4 (completas) | 5 (parcial: só acesso a dados) | 6,7,8 (não analisadas)
Motivo da parada: <escopo definido | defeito S0 na camada 2 | limite de contexto>
```

---

## Capítulo 1.6 — Tomada de decisão

### CON-028 — Enuncie o problema como restrição **[OBRIGATÓRIA]**

Restrição descreve o que precisa ser verdade; solução descreve como. Começar pela solução elimina
alternativas antes de considerá-las.

| Errado (solução disfarçada) | Correto (restrição) |
| --- | --- |
| "Precisamos adicionar Redis" | "Leituras repetidas do catálogo não podem custar uma consulta por requisição" |
| "Precisamos migrar para microsserviços" | "Pagamentos precisa fazer deploy sem coordenar com catálogo" |
| "Precisamos de uma máquina de estados" | "Um pedido não transita para `enviado` sem estar `pago`" |

Se você não consegue enunciar sem nomear tecnologia, ainda não entendeu o problema.

### CON-029 — A opção zero é obrigatória **[OBRIGATÓRIA]**

"Não fazer nada / aceitar o risco" é sempre uma alternativa e deve ser considerada explicitamente. É a
escolha certa mais vezes do que parece: quando o custo excede o dano, quando o módulo será substituído,
quando o risco é aceitável e monitorado, quando falta informação.

### CON-030 — Alternativas reais **[OBRIGATÓRIA]**

Uma alternativa é real quando existe cenário plausível em que seria escolhida. Alternativa de fachada
invalida o processo. Fontes quando você só pensa em uma:

- **Mudar a camada:** resolver no banco, na aplicação, no cliente ou na infraestrutura.
- **Mudar o momento:** validar na escrita ou na leitura; síncrono ou assíncrono.
- **Mudar o alcance:** consertar o caso reportado ou toda a classe do problema.
- **Mudar a forma:** prevenir por tipo, por constraint, por teste ou por monitoramento.
- **Comprar em vez de construir**, ou o inverso.

### CON-031 — Seis dimensões de comparação **[OBRIGATÓRIA]**

Correção · custo (implementação + revisão + manutenção) · risco · reversibilidade · carga operacional ·
aderência à arquitetura atual.

**Correção é eliminatória:** alternativa que não resolve o problema inteiro sai da mesa, salvo se
declarada como mitigação temporária com prazo e item de backlog. Depois dela, **reversibilidade** é a
dimensão mais subestimada: decisão medíocre e reversível vence decisão boa e irreversível tomada com
informação incompleta.

### CON-032 — Declare a troca aceita **[OBRIGATÓRIA]**

> "Escolhida a alternativa B. Aceito 15% mais código e uma dependência nova em troca de eliminar a
> possibilidade estrutural do estado inválido, em vez de apenas validá-lo."

### CON-033 — Declare a condição de invalidação **[OBRIGATÓRIA]**

O que faria esta decisão passar a estar errada. É o campo que transforma decisão em conhecimento
reutilizável — sem ele, ninguém no futuro sabe se a decisão ainda vale.

### CON-034 — Registre no nível adequado **[OBRIGATÓRIA]**

| Tipo de decisão | Registro |
| --- | --- |
| Muda contrato público (API, schema, evento, tipo exportado) | [ADR](templates/adr.md) obrigatório |
| Escolhe tecnologia ou padrão que outros seguirão | ADR obrigatório |
| Aceita risco conscientemente | ADR + matriz de risco |
| Custosa de reverter (> 1 dia) | ADR obrigatório |
| Local com alternativa não óbvia | Comentário explicando o **porquê** |
| Local óbvia | Nada. Não documente o trivial |

### CON-035 — Postergar é decisão, e se registra **[OBRIGATÓRIA]**

Poste quando a informação que falta chega logo e é decisiva, quando a decisão fica mais barata depois de
outra mudança planejada, ou quando errar agora custa mais que esperar. Registre: o que falta, quem traz,
e o evento que reabre. Postergar sem registro é esquecer.

---

## Capítulo 1.7 — Classificação e priorização

### CON-036 — Severidade mede consequência **[IMUTÁVEL]**

Nunca esforço, nunca elegância.

| Sev. | Definição | Exemplos | Ação |
| --- | --- | --- | --- |
| **S0** | Dano ativo ou iminente, sem contorno | Vazamento de dado pessoal ou segredo; acesso a dado de outro usuário/tenant; perda ou corrupção de dados; erro de cálculo financeiro; execução remota de código; indisponibilidade total | Para tudo. Nunca vai ao backlog |
| **S1** | Quebra funcional real, ou risco de segurança com pré-condição | Regra de negócio errada em fluxo principal; estado inválido alcançável; falha de autorização com condição incomum; ausência de integridade em dado crítico; ação destrutiva sem confirmação; regra crítica sem teste; dinheiro em ponto flutuante | Bloqueia entrega |
| **S2** | Funciona, com custo relevante | Regra duplicada com risco de divergir; caso de borda fora do fluxo principal; ausência de estado de erro/vazio; barreira de acessibilidade; log sem contexto; teste intermitente; acoplamento que encarece a próxima mudança | `MUST-FIX` se no escopo; senão `OPPORTUNITY` |
| **S3** | Melhoria sem consequência funcional | Divergência de nomenclatura contra norma; código morto; comentário desatualizado; duplicação pequena e estável | `OPPORTUNITY`. Nunca bloqueia |

### CON-037 — Esforço e risco de correção **[OBRIGATÓRIA]**

Esforço inclui **validação**, não só escrita: `XS` < 30 min · `S` < 2 h · `M` < 1 dia · `L` 2–5 dias ·
`XL` > 1 semana. `XL` nunca entra numa rodada de revisão: vai ao backlog como proposta com ADR.

Risco de correção: `LOW` (isolado, coberto, reversível por commit) · `MEDIUM` (código compartilhado,
cobertura parcial) · `HIGH` (contrato público, schema, migração, autenticação, concorrência, sem
cobertura). Correção `HIGH` entra **isolada**, com rollback declarado.

### CON-038 — `MUST-FIX` versus `OPPORTUNITY` **[IMUTÁVEL]**

É `MUST-FIX` quando qualquer condição se aplica: severidade `S0`/`S1` · `S2` no caminho direto da
mudança atual · viola norma marcada `[OBRIGATÓRIA]` · impede a Definition of Done · segurança em
caminho sensível com confiança ≥ `MEDIUM`.

É `OPPORTUNITY` em todos os outros casos, e **toda** `OPPORTUNITY` vai ao backlog (CON-019).

### CON-039 — Score de prioridade **[OBRIGATÓRIA]**

Severidade domina: primeiro todos os `S0`, depois `S1` por score, depois `MUST-FIX S2`, depois
`OPPORTUNITY`. O score só ordena **dentro** da mesma faixa.

```
                Impacto × Alcance × Confiança
Prioridade  =  ────────────────────────────────
                     Esforço × Risco
```

| Fator | Escala |
| --- | --- |
| Impacto | 10 dado/dinheiro/dado pessoal · 7 fluxo principal quebrado · 4 degradação com contorno · 2 manutenção · 1 cosmético |
| Alcance | 10 todos os usuários ou todo o time · 6 segmento grande · 3 segmento pequeno · 1 caso raro |
| Confiança | 1.0 `HIGH` · 0.6 `MEDIUM` · 0.3 `LOW` |
| Esforço | 1 `XS` · 2 `S` · 5 `M` · 13 `L` · 34 `XL` |
| Risco | 1.0 `LOW` · 1.5 `MEDIUM` · 2.5 `HIGH` |

Leitura: ≥ 20 faça agora · 8–20 nesta rodada · 2–8 backlog priorizado · < 2 backlog frio.

**Desempate:** desbloqueia outro trabalho → segurança ou dados → já está no caminho de uma mudança em
curso → reduz risco irreversível → menor esforço (só como último critério).

**Modificadores:** módulo a ser substituído em < 3 meses zera o impacto de manutenibilidade · área com
incidente nos últimos 30 dias multiplica impacto por 1,5 · prazo regulatório trata como `S1` até a data
· item postergado 3 vezes é promovido ou encerrado como "não faremos".

### CON-040 — Orçamento da rodada **[OBRIGATÓRIA]**

```
70% MUST-FIX  |  20% maior score do backlog  |  10% ferramental que reduz custo futuro
```

Os 20% garantem que o backlog **avança**. Se `MUST-FIX` consome 100% da capacidade por duas rodadas
seguidas, **esse é o achado principal**: o módulo está em dívida crítica e precisa de decisão de
produto, não de mais revisão.

---

## Capítulo 1.8 — Matriz de risco de execução

### CON-041 — Faixas e mitigação obrigatória **[IMUTÁVEL]**

Risco aqui é o risco de **executar** a mudança. Probabilidade (cobertura de testes, concorrência, raio)
× impacto (dados, dinheiro, segurança, disponibilidade).

|  | Impacto Baixo | Médio | Alto | Crítico |
| --- | --- | --- | --- | --- |
| **Prob. Alta** | R2 | R3 | **R4** | **R4** |
| **Prob. Média** | R1 | R2 | R3 | **R4** |
| **Prob. Baixa** | R1 | R1 | R2 | R3 |

| Faixa | Mitigação obrigatória |
| --- | --- |
| **R1** | Fluxo normal |
| **R2** | Teste do comportamento alterado antes da mudança · commit isolado · rollback documentado |
| **R3** | Tudo de R2 + teste de regressão escrito antes, provando o comportamento atual correto · PR isolado · rollback **testado** · flag quando possível · métrica que evidenciaria a falha · revisão humana |
| **R4** | Tudo de R3 + **ADR** · **aprovação humana antes da implementação** · backup verificado (restauração testada) · migração reversa executada com volume representativo · deploy gradual com critério objetivo de abortar · monitoramento definido antes do deploy · nenhuma outra mudança em voo na área |

**R4 por definição:** migração destrutiva de schema · qualquer migração de dados · alteração em
autenticação, sessão ou emissão de token · alteração em regra de autorização · alteração em cálculo
financeiro, cobrança, imposto, desconto ou frete · alteração em tratamento de dado pessoal · rotação de
segredo em produção · quebra de contrato consumido por terceiros.

**R3 por definição:** concorrência, fila, retry, idempotência · cache com risco de servir dado de outro
usuário · atualização de dependência com mudança de major · alteração no portão de qualidade do
pipeline · remoção de código sem prova de que não é usado.

### CON-042 — Riscos que não aparecem no diff **[OBRIGATÓRIA]**

Verifique todos antes de fechar a decisão:

| Risco | Pergunta |
| --- | --- |
| Dados existentes | A regra nova é violada por registros que já estão no banco? |
| Clientes antigos | App móvel em versão anterior continua funcionando? |
| Janela de deploy | Código novo e antigo coexistem. Ambos funcionam? |
| Cache envenenado | Dado cacheado no formato antigo será lido pelo código novo? |
| Fila em trânsito | Mensagens já enfileiradas no formato antigo serão processadas? |
| Integração externa | Terceiro depende do comportamento exato que está mudando? |
| Fuso e localidade | Comportamento muda conforme timezone, moeda ou idioma? |
| Escala | Funciona com o volume de produção, não só com dados de teste? |
| Bloqueio de tabela | A migração bloqueia a tabela durante a criação do índice? |

**Aceitação de risco** exige três coisas: **nomeado** (pessoa, não "o time") · **registrado** (ADR ou
backlog) · **monitorado** (métrica que revelaria a materialização). Risco `R4` só o dono humano aceita —
nunca um agente.

---

## Capítulo 1.9 — Definition of Done

### CON-043 — DoD é obrigatória e verificada item a item **[IMUTÁVEL]**

Cada item recebe `OK`, `N/A + justificativa` ou `PENDENTE`. Um único `PENDENTE` significa `PARTIAL`,
nunca `DONE`. `N/A` sem justificativa conta como `PENDENTE`. Marcar sem verificar é a falha mais grave
deste framework, porque corrompe todos os relatórios subsequentes.

**A. Correção** — problema resolvido por inteiro, não só o caso reportado · casos irmãos verificados ·
bordas cobertas (nulo, vazio, zero, limite, duplicata, negativo, texto longo, caractere especial) ·
caminhos de erro tratados · nenhum estado inválido novo representável · nenhum comportamento existente
alterado sem intenção declarada.

**B. Validação executada** — verificação estreita com resultado literal · type check sem erro novo ·
lint sem erro novo e sem regra silenciada · regressão do escopo afetado · o que não pôde ser validado
está declarado com o comando exato para um humano rodar.

**C. Testes** — regra nova tem teste que **falha** sem a mudança · bug corrigido tem teste de regressão ·
nenhum teste depende de tempo real, ordem, rede ou estado compartilhado · nenhum teste desabilitado,
`skip` ou afrouxado · testes verificam comportamento, não implementação.

**D. Segurança** — entrada nova validada no servidor · autorização por objeto · nenhum segredo em
código, log ou bundle · nenhum dado pessoal novo em log · nenhuma dependência com vulnerabilidade
conhecida · em fluxo sensível, caminho de exploração demonstrado como fechado.

**E. Dados** — invariantes garantidas no banco onde possível · migração reversível com reversa executada
em teste · migração testada contra dados existentes que violariam a regra · consulta nova usa índice ·
escopo de transação correto.

**F. Interface** — estados presentes (carregando, vazio, erro, sucesso, sem permissão) · erro diz o que
fazer sem detalhe técnico · ação destrutiva com confirmação ou desfazer · operável por teclado com foco
visível · rótulo acessível em todo controle · nada quebra em tela pequena · nenhum trabalho do usuário
perdido.

**G. Observabilidade** — falha nova registrada com contexto correlacionável · nenhum erro engolido · se
pode falhar em silêncio, existe métrica ou alerta.

**H. Rastreabilidade** — commit explica o **porquê** · achados referenciados por ID · decisão não óbvia
registrada · ADR para mudança de contrato público · tudo que não foi corrigido está no backlog.

**I. Higiene do diff** — um concern por commit · nenhuma alteração cosmética misturada · nenhum arquivo
tocado sem necessidade · nenhum código comentado, `console.log` ou `TODO` sem ID · nenhuma dependência
nova sem justificativa.

### CON-044 — Redução de DoD apenas em `S0` de produção **[OBRIGATÓRIA]**

Para reduzir tempo de exposição, uma correção de `S0` pode cumprir apenas as seções A, B, D e o mínimo
de G. Nesse caso: a redução é declarada no relatório, um item `S1` de backlog é criado imediatamente
para completar a DoD, e o prazo é **a rodada seguinte**. Nenhuma outra situação autoriza redução.

### CON-045 — O teste das 3h da manhã **[OBRIGATÓRIA]**

> Se esta mudança causar um incidente às 3h da manhã, alguém que nunca a viu consegue entender o que ela
> fez, descobrir que ela é a causa, e revertê-la sem me perguntar nada?

Se a resposta é não, algum item acima está marcado incorretamente.

---

## Capítulo 1.10 — Definition of Excellence

### CON-046 — Excelência é deliberada e por módulo **[OBRIGATÓRIA]**

A DoD é o piso; a DoE é o teto. **Não se exige DoE de todo módulo** — exige-se dos que sustentam o
negócio. Perseguir excelência em código periférico é erro de priorização, não virtude. A classificação
por módulo (`crítico` / `padrão` / `periférico`) vive no
[perfil do projeto](templates/perfil-do-projeto.md).

Nenhum módulo recebe nota 10 na auditoria sem atender a DoE. **Ausência de problemas dá, no máximo, 8.**

### CON-047 — As oito marcas de excelência **[OBRIGATÓRIA]**

1. **O domínio é impossível de usar errado.** Estados inválidos não são representáveis pelos tipos ou
   pelo schema — não apenas rejeitados em execução. Conceitos têm tipos próprios. Operações não
   repetíveis são idempotentes por construção.
2. **As fronteiras são visíveis e respeitadas.** Interface pública explícita; domínio sem infraestrutura;
   sem ciclos; uma mudança de requisito toca um módulo; trocar fornecedor é mudança local.
3. **Os testes são um ativo.** Determinísticos, rápidos, focados em comportamento, com bordas por tabela
   ou propriedade, e todo bug histórico com teste nomeado.
4. **A segurança é o padrão.** Negar por omissão; autorização centralizada e obrigatória por construção;
   segredos rotacionáveis sem deploy; log seguro no ponto de escrita; inventário de dado pessoal.
5. **A performance é conhecida, não esperada.** Limiares declarados, números medidos e registrados com
   data e método, proteção estrutural contra N+1, verificação automática que falha na regressão.
6. **A experiência é consistente e previsível.** Todos os estados projetados; mesmo tipo de ação se
   comporta igual; erros acionáveis; WCAG 2.2 AA verificado, não presumido.
7. **A operação é entediante.** Deploy rotineiro; rollback de um comando testado; painel que responde
   "está tudo bem?" em dez segundos; todo alerta com runbook; restauração de backup testada em
   calendário.
8. **O conhecimento não vive nas pessoas.** Pessoa nova produz mudança útil no primeiro dia; decisões
   relevantes têm ADR; nenhuma área que "só uma pessoa entende"; backlog honesto.

### CON-048 — Suba um degrau por rodada **[OBRIGATÓRIA]**

Meça a distância, não a perfeição: cada dimensão recebe nota de 0 a 10 e a meta razoável é **+1 na
dimensão mais fraca**, não 10 em tudo. Lacuna de DoE é `OPPORTUNITY`, exceto quando coincide com
`S0`/`S1`.

### CON-049 — O critério único de excelência **[IMUTÁVEL]**

> Excelência é quando a próxima mudança é **mais fácil** do que a anterior.

Se cada entrega deixa o módulo mais difícil de mudar, não há excelência — há acúmulo, mesmo com todos os
testes verdes.

---

## Capítulo 1.11 — Métricas e limiares

### CON-050 — Métrica sem reação é decoração **[OBRIGATÓRIA]**

Toda métrica tem limiar, reação declarada e antipadrão de uso. Limiares marcados `[perfil]` são
confirmados ou ajustados no perfil do projeto; os valores abaixo valem até que alguém decida o
contrário — o que é diferente de não ter limiar.

| Categoria | Métrica | Limiar padrão | Bloqueia? |
| --- | --- | --- | --- |
| Correção | `S0` / `S1` em aberto | 0 | Sim |
| Correção | Taxa de erro de requisições | < 0,5% `[perfil]` | Investigação obrigatória |
| Correção | Reincidência de defeito | 0 | Sim — o teste de regressão ausente é o achado |
| Testes | Casos de negócio declarados cobertos | 100% | Sim |
| Testes | Cobertura de linhas | ≥ 60% `[perfil]` | **Nunca** |
| Testes | Testes intermitentes | 0 | Corrigir em 1 rodada |
| Testes | Tempo da suíte relevante | < 5 min `[perfil]` | Não |
| Performance | API p95 | < 300 ms `[perfil]` | Não |
| Performance | Consulta p95 | < 100 ms `[perfil]` | Não |
| Performance | Consultas por requisição | constante em relação ao resultado | `S2`/`S1` |
| Performance | LCP / INP / CLS | < 2,5 s / < 200 ms / < 0,1 `[perfil]` | Não |
| Performance | Bundle inicial | < 250 KB comprimido `[perfil]` | Sim (pipeline) |
| Performance | Regressão entre versões | > 20% | Sim |
| Segurança | Vulnerabilidade crítica ou alta | 0 | Sim |
| Segurança | Segredos no repositório | 0 | Sim |
| Segurança | Endpoints sem autorização | 0 | Sim |
| Segurança | Dado pessoal em log | 0 | Sim |
| A11y | Erros automatizados | 0 | Sim |
| A11y | Tarefas críticas por teclado | 100% | Sim |
| Operação | MTTD fluxo crítico | < 5 min `[perfil]` | Não |
| Operação | MTTR | < 30 min `[perfil]` | Não |
| Operação | Alertas sem runbook | 0 | Não |
| Manutenibilidade | Dependências circulares | 0 | `S2` |
| Manutenibilidade | Implementações da mesma regra | 1 | `S2` |
| Manutenibilidade | Arquivos por mudança típica | ≤ 5 | **Indicador** |

### CON-051 — Métricas de manutenibilidade não justificam mudança **[IMUTÁVEL]**

As métricas de correção, segurança e acessibilidade **bloqueiam**. As de manutenibilidade apenas
**apontam onde olhar**. Nenhuma mudança de código pode ser justificada exclusivamente por mover um
número de manutenibilidade — isso é CON-013 aplicado a métricas.

> Toda métrica vira meta, e toda meta vira jogo. Por isso as duas categorias são tratadas de forma
> diferente.

### CON-052 — Pesos da nota final **[OBRIGATÓRIA]**

| Dimensão | Peso |
| --- | --- |
| Segurança | 20% |
| Correção de domínio | 20% |
| Dados e integridade | 15% |
| Testes | 15% |
| Arquitetura | 10% |
| Performance | 8% |
| UX e acessibilidade | 7% |
| Observabilidade e entrega | 5% |

Travas: qualquer `S0` ou `S1` não corrigido limita o total a 4 e força `REJECTED`. Segurança abaixo de 6
limita a `APPROVED WITH CONDITIONS`. Detalhado no [Volume 11](12-auditoria.md).

---

## Capítulo 1.12 — Condições de parada

### CON-053 — Pare e escale **[IMUTÁVEL]**

Pare e pergunte, em vez de adivinhar, quando:

- A mudança altera **contrato público** (API, schema, payload de evento, tipo exportado) e nenhum ADR a
  cobre.
- Toca **autenticação, autorização, pagamento ou dado pessoal** e o comportamento pretendido é ambíguo.
- Exige **excluir ou migrar dados**.
- Dois princípios colidem e CON-021 não resolve.
- Você falhou **três vezes** no mesmo problema. Reporte o que estabeleceu, o que descartou e os dois
  próximos passos mais prováveis.
- A correção correta custa mais de **3× o orçamento de mudança**. Proponha como item de backlog em vez de
  fazer em silêncio.
- Há indício de **incidente ativo em produção**. Isso interrompe a rodada inteira.

### CON-054 — Antipadrões proibidos **[IMUTÁVEL]**

| Nunca | Porque |
| --- | --- |
| Reescrever módulo funcionando para "modernizar" | Custo é real, benefício é presumido |
| Adicionar abstração para um único uso | Generalidade especulativa custa mais que duplicação |
| Corrigir formatação e lógica no mesmo commit | Impossibilita revisão e rollback |
| Afirmar ganho de performance sem medição | Trabalho de performance não medido é decoração |
| Adicionar dependência para o que 20 linhas resolvem | Cadeia de suprimentos e manutenção para sempre |
| Silenciar erro, tipo ou regra de lint para o build passar | Esconde o defeito |
| Escrever teste que afirma o comportamento atual sem saber se é correto | Trava o bug |
| Mudar mais de uma camada por commit | Torna a causa da regressão inencontrável |
| Reportar módulo pronto sem rodar a DoD | Pronto é checklist, não sensação |
| Produzir plano mais longo que a mudança que descreve | Processo deve servir ao trabalho |

---

## Capítulo 1.13 — Ofício: nomes, código e commits

Estas normas são universais: valem para qualquer linguagem e são carregadas por **todos** os papéis. Elas
existem para encerrar discussão, não para criar mais.

**Formatação não está aqui.** Formatação é responsabilidade da ferramenta, configurada uma vez, aplicada
automaticamente, e **nunca comentada em revisão**. Convenções de caixa seguem o idioma da linguagem e são
declaradas no [perfil do projeto](templates/perfil-do-projeto.md).

### CON-065 — O nome diz a intenção, não o tipo **[OBRIGATÓRIA]**

| Ruim | Bom | Por quê |
| --- | --- | --- |
| `data`, `info`, `obj`, `item` | `pedidoPendente`, `precoTotal` | Não informa nada |
| `userArray`, `strNome` | `usuarios`, `nome` | O tipo já está no tipo |
| `handleClick2` | `confirmarPagamento` | Numeração revela conceito ausente |
| `flag`, `temp`, `aux` | `estoqueReservado`, `precoOriginal` | Nome de rascunho em código definitivo |

### CON-066 — Vocabulário único, do banco à interface **[OBRIGATÓRIA]**

Ver ARC-015. Sinônimo é ambiguidade permanente e a principal fonte de bug de integração.

### CON-067 — Sufixos com significado fixo **[RECOMENDADA]**

| Sufixo | Significado |
| --- | --- |
| `...At` | Instante |
| `...Count` | Quantidade inteira |
| `...Id` | Identificador de referência |
| `...Cents` / `...Amount` | Valor monetário em unidade inteira |
| `is...` / `has...` / `can...` | Booleano |
| `...Total` | Resultado agregado |

Nunca use um sufixo com significado divergente. `precoAt` é ruído; `pagoCount` não é booleano.

### CON-068 — Booleano afirmativo **[OBRIGATÓRIA]**

`isAtivo`, não `isNaoInativo`. Negação dupla em condicional é fonte real de defeito, não questão de estilo.

### CON-069 — Funções são verbos, e o nome revela o efeito **[OBRIGATÓRIA]**

`calcularTotal` é puro e retorna valor · `salvarPedido` tem efeito e o nome diz isso · `getUsuario` **não
pode** criar, alterar ou enviar nada. Nome que esconde efeito é `S2`.

### CON-070 — Sem abreviação não estabelecida **[RECOMENDADA]**

`quantidade`, não `qtd`. Exceções: abreviações universais do domínio (`id`, `url`, `cpf`, `sku`) e o índice
de laço.

### CON-071 — Uma responsabilidade por unidade **[RECOMENDADA]**

Se você precisa de "e" para descrever o que uma função faz, provavelmente são duas. Indicador, **não** regra
de tamanho: fatiar função para cumprir número de linhas produz o mesmo código, mais espalhado, e é proibido
por CON-013.

### CON-072 — Retorno antecipado **[RECOMENDADA]**

Trate erro e caso trivial no início; deixe o caminho principal sem aninhamento. Aninhamento acima de quatro
níveis é indicador de investigação.

### CON-073 — Sem número ou texto mágico **[OBRIGATÓRIA]**

Valor com significado de negócio é constante nomeada. Vale para status, códigos de erro e chaves.

### CON-074 — Funções puras onde é possível **[RECOMENDADA]**

Cálculo, transformação e decisão sem efeito, com o efeito empurrado para as bordas. É o que torna a cobertura
de negócio viável (QAT-024).

### CON-075 — Sem código morto **[OBRIGATÓRIA]**

Código comentado, função nunca chamada, flag que nunca muda, import não usado. O git é o histórico. Código
morto engana o leitor e infla a área de busca durante um incidente.

### CON-076 — Imutabilidade por padrão **[RECOMENDADA]**

Mutação de parâmetro é `S2`: é efeito invisível para o chamador.

### CON-077 — Sem escape do sistema de tipos **[OBRIGATÓRIA]**

`any`, cast forçado, supressão de erro de tipo e asserção de não nulo são proibidos sem comentário que
explique a garantia externa que os justifica. Cada escape é uma verificação desligada em silêncio.

### CON-078 — Tipos de domínio, não primitivos **[RECOMENDADA]**

Ver ARC-012. Dinheiro em ponto flutuante é `S1`, sempre.

### CON-079 — Ausência explícita **[OBRIGATÓRIA]**

Distinga "não informado", "vazio" e "zero". Sentinela de ausência (`0`, `""`, `-1`) é `S2`. Ver BAK-014.

### CON-080 — Nunca engula erro **[OBRIGATÓRIA]**

Ver BAK-023.

### CON-081 — Erro carrega contexto e separa usuário de sistema **[OBRIGATÓRIA]**

Ver BAK-024 e BAK-025.

### CON-082 — Comente o porquê, nunca o quê **[OBRIGATÓRIA]**

```
Ruim: // incrementa o contador
Bom:  // o fornecedor cobra em lotes de 100; abaixo disso a chamada é rejeitada
```

Comentário que narra o código é ruído que envelhece e passa a mentir.

### CON-083 — `TODO` exige identificador de backlog **[OBRIGATÓRIA]**

`// TODO(EOS-042): remover quando a migração de preço concluir`. Sem ID, o `TODO` é proibido — é dívida sem
registro, e viola CON-019.

### CON-084 — Documente o não óbvio, o perigoso e o contraintuitivo **[RECOMENDADA]**

Ordem de operação que importa, restrição externa, contorno de bug de terceiro, e o motivo de algo **não** ter
sido feito da forma esperada. Especialmente o último: é o que evita que alguém "corrija" para a forma
quebrada.

### CON-085 — A mensagem de commit explica o porquê **[OBRIGATÓRIA]**

```
Ruim:  "fix bug"  |  "ajustes"  |  "atualiza checkout.ts"

Bom:   impede pedido pago sem valor confirmado

       A transição para `pago` não verificava o retorno do provedor, permitindo
       pedido com total zero quando a cobrança falhava silenciosamente.
       Resolve EOS-031.
```

### CON-086 — Formatação em massa em commit separado **[OBRIGATÓRIA]**

Misturar reformatação com comportamento inutiliza a revisão e a bissecção. É CON-015 na prática.

---

## O critério final

### CON-055 — A frase que resume o volume **[IMUTÁVEL]**

> Um sistema é bem construído quando a próxima pessoa consegue mudá-lo com segurança sem perguntar nada
> a quem o escreveu.

Ela mede simultaneamente clareza, testes, documentação, acoplamento e observabilidade — porque a falha
em qualquer um deles obriga a pergunta.

---

## Padrões reutilizáveis

**Cartão de achado.** Cada item em G1 carrega evidência (`path:linha` ou saída de comando),
severidade, confiança, esforço e risco de correção (`CON-010`, `CON-037`). Sem evidência →
`HYPOTHESIS`, nunca `FINDING` (`CON-009`).

**Proposta com opção zero.** Em G2: ≥2 alternativas reais mais a opção de não mudar, comparadas
nas seis dimensões (`CON-029`–`CON-031`). A troca aceita e a condição de invalidação ficam
escritas (`CON-032`, `CON-033`).

**Orçamento 70/20/10.** Capacidade da rodada: correção obrigatória, melhoria no escopo, e margem
para o inesperado (`CON-040`). `MUST-FIX` acima da capacidade é o achado principal, não mais
lista.

**DoD item a item.** Cada entrega passa pela Definition of Done com `N/A` justificado
(`CON-043`). Redução só em `S0` de produção (`CON-044`).

**Backlog com gatilho.** Todo `OPPORTUNITY` não corrigido vira entrada com severidade, esforço,
evidência e gatilho de promoção (`CON-019`). Nada morre no chat.

---

## Matrizes de decisão

**Severidade pela consequência (`CON-036`)**

| Consequência | Severidade | Tratamento |
| --- | --- | --- |
| Dados errados, vazamento, perda irreversível, indisponibilidade total | `S0` | Bloqueia agora |
| Falha grave em caminho crítico ou regra de dinheiro/acesso | `S1` | Bloqueia entrega |
| Defeito real com contorno ou impacto limitado | `S2` | `MUST-FIX` no orçamento |
| Melhoria sem falha atual demonstrável | `S3` / `OPPORTUNITY` | Backlog com gatilho |

**Faixa de risco da mudança (`CON-041`)**

| Faixa | Exemplos | Mitigação mínima |
| --- | --- | --- |
| `R1` | Copy, typo, teste isolado | Diff + validação estreita |
| `R2` | Comportamento local com testes | Teste + DoD |
| `R3` | Contrato, schema, fluxo crítico | Teste de regressão *antes*; rollback |
| `R4` | Migração/deleção de dados, auth | Aprovação humana nomeada (`CON-042`) |

**Desempate quando princípios conflitam:** aplicar `CON-021` na ordem; registrar a resolução
(`CON-034`).

---

## Fluxo de trabalho

Os seis portões (`CON-056`). Não reordenar. Não pular.

1. **G0 Descoberta** — mapa do terreno; proibido propor (`CON-057`).
2. **G1 Diagnóstico** — oito camadas na ordem (`CON-011`, `CON-023`); achados com evidência
   (`CON-058`).
3. **G2 Decisão** — alternativas, risco, ADR se exigido (`CON-059`, `CON-034`).
4. **G3 Implementação** — menor mudança reversível; um concern por commit (`CON-060`, `CON-015`,
   `CON-016`).
5. **G4 Validação** — nunca comprimida; DoD verificada (`CON-061`, `CON-043`).
6. **G5 Auditoria** — conjunto, notas, backlog (`CON-062`, `CON-019`).

Surpresa em compressão → voltar a G0 (`CON-064`). Pare e escale sob `CON-053`.

---

## Exemplos de implementação

**Evidência versus impressão (`CON-009`)**

```
Ruim — FINDING: "o checkout parece lento"
Bom  — FINDING: GET /checkout p95=840ms (n=200, homologação, ferramenta X); limiar 300ms
       Evidência: output do comando … ; path do handler: checkout.ts:118
```

**Opção zero omitida (`CON-029`, `CON-030`)**

```
Ruim — "vamos extrair um serviço de preços" (única opção)
Bom  — A) não mudar (custo: duplicação anotada)
       B) extrair função pura compartilhada (menor raio)
       C) serviço separado (maior raio; ADR)
       Escolha: B; troca aceita: duplicação residual até 3º uso (CON-004)
```

**Commit misturado (`CON-015`, `CON-086`)**

```
Ruim — um commit: formata o módulo + corrige arredondamento de frete
Bom  — commit 1: impede frete negativo quando peso=0 (porquê no corpo)
       commit 2: formatação do módulo de frete (separado)
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Achado sem `path:linha` nem saída de comando | Opinião disfarçada de evidência (`CON-009`) |
| Pular camada porque "já sei onde está" | Defeito estrutural descoberto tarde (`CON-011`) |
| Uma alternativa só na proposta | Decisão teatral (`CON-030`) |
| Refatorar "enquanto estou aqui" | Diff ilegível; rollback impossível (`CON-013`) |
| Validação "deve funcionar" | G4 fingido (`CON-061`) |
| Misturar `MUST-FIX` e `OPPORTUNITY` | Prioridade destruída (`CON-018`) |
| `OPPORTUNITY` que morre no chat | Dívida invisível (`CON-019`) |
| Negociar `S0`/`S1` por prazo | Integridade trocada por calendário (`CON-036`) |
| Modernizar módulo que funciona | Custo real, benefício assumido (`CON-054`) |
| Afrouxar teste para passar | Bug vira especificação (`CON-054`, `QAT-008`) |

---

## Checklist

- [ ] Evidência em todo achado, ou rótulo `HYPOTHESIS`. (`CON-009`)
- [ ] Confiança declarada. (`CON-010`)
- [ ] Camadas na ordem; avanço só com camada atual limpa o suficiente. (`CON-011`, `CON-024`)
- [ ] Protocolo de decisão seguido antes de mudança não trivial. (`CON-012`)
- [ ] Sem refatoração cosmética. (`CON-013`)
- [ ] Validação isolada por mudança; G4 não comprimido. (`CON-014`, `CON-061`)
- [ ] Um concern por commit; formatação em massa separada. (`CON-015`, `CON-086`)
- [ ] Menor mudança reversível; justificativa de quatro campos. (`CON-016`, `CON-017`)
- [ ] `MUST-FIX` e `OPPORTUNITY` em listas separadas. (`CON-018`)
- [ ] `OPPORTUNITY` residual no backlog com gatilho. (`CON-019`)
- [ ] Não verificado declarado. (`CON-020`)
- [ ] Conflito resolvido por desempate, não por média. (`CON-021`)
- [ ] ≥2 alternativas + opção zero; troca e invalidação escritas.
      (`CON-029`–`CON-033`)
- [ ] Severidade por consequência; score e orçamento da rodada.
      (`CON-036`, `CON-039`, `CON-040`)
- [ ] Faixa de risco com mitigação; `R4` com humano. (`CON-041`, `CON-042`)
- [ ] DoD verificada item a item. (`CON-043`)
- [ ] Condições de parada respeitadas. (`CON-053`)
- [ ] Antipadrões proibidos ausentes no diff. (`CON-054`)

---

## Prompt do volume

```
ROLE: You operate under EOS Volume 00 — Constitution of Engineering (`CON`). Every task loads this
volume. Domain volumes never override it.

MISSION
Enforce how work is thought, decided, and proven: evidence before opinion, decision before code,
validation that is never skipped. You do not invent domain norms; you cite domain volumes by ID.

LOAD
- `AGENTS.md`, `agents/_shared/core-contract.md`, `agents/_shared/output-schemas.md`
- `00-constituicao-da-engenharia.md` (always)
- The filled `templates/perfil-do-projeto.md` — if missing, proposing it is the first deliverable
- Only the domain volumes the task requires (`ORC-005`)

MANDATORY SEQUENCE — the six gates (`CON-056`); do not skip forward
1. G0 Discovery — map the terrain; no findings yet (`CON-057`).
2. G1 Diagnosis — eight layers in order (`CON-011`, `CON-023`); FINDING needs evidence (`CON-009`).
3. G2 Decision — ≥2 real alternatives + option zero; risk band; ADR when required
   (`CON-029`–`CON-034`, `CON-041`).
4. G3 Implementation — smallest reversible change; one concern per commit (`CON-016`, `CON-015`).
5. G4 Validation — never compressed; DoD item by item (`CON-061`, `CON-043`).
6. G5 Audit — set of changes, residual risk, backlog (`CON-062`, `CON-019`).

RULES OF ENGAGEMENT
- No citation → label `HYPOTHESIS`, never `FINDING` (`CON-009`).
- Separate `MUST-FIX` from `OPPORTUNITY` (`CON-018`).
- Cosmetic refactor is forbidden (`CON-013`).
- Stop and escalate under `CON-053`; never silently degrade.
- Cite rule IDs; do not restate domain volumes.

OUTPUT
Use the "Verificação obrigatória de saída" block of `00-constituicao-da-engenharia.md`.
Declare layers covered and not covered (`CON-027`). Lead with outcome, then evidence.
```

---

## Critérios de aceite

Uma entrega passa neste volume quando **todas** são verdadeiras e verificadas:

1. Todo achado tem evidência ou está rotulado `HYPOTHESIS`. (`CON-009`)
2. Mudança não trivial passou por decisão com ≥2 alternativas e opção zero. (`CON-030`)
3. G4 foi executada; DoD está completa com `N/A` justificados. (`CON-061`, `CON-043`)
4. `MUST-FIX` e `OPPORTUNITY` estão separados; residual no backlog com gatilho. (`CON-018`,
   `CON-019`)
5. Faixa de risco respeitada; `R4` com aprovação humana nomeada. (`CON-041`, `CON-042`)
6. Nenhum `S0`/`S1` aberto sem aceitação de risco registrada. (`CON-036`, `CON-038`)
7. Camadas não cobertas estão declaradas. (`CON-027`)
8. Diff não contém antipadrão de `CON-054`.

Falha em 1, 3 ou 5 é reprovação direta: sem evidência não há engenharia; sem G4 não há entrega;
sem mitigação de risco a mudança é roleta.

---

## Verificação obrigatória de saída

```
## Portões
| Portão | Compactado? | Evidência de passagem |
| G0 | | |
| G1 | | |
| G2 | | |
| G3 | | |
| G4 | nunca | |
| G5 | | |

## Camadas (CON-023)
| Camada | Coberto | Achados | Por que fora (se N/A) |

## Achados
MUST-FIX (ordenados por CON-039):
OPPORTUNITY (com entrada de backlog e gatilho):

## Decisões
| Item | Alternativas (≥2 + zero) | Escolha | Troca (CON-032) | Invalidação (CON-033) |

## Risco
| Mudança | Faixa | Mitigação | Aprovação humana |

## Validação (G4)
| Verificação | Comando/resultado | Passou? |

## DoD
| Item | Status | N/A justificado? |

## Não verificado
| Item | Por quê | Como verificar |

## Antipadrões CON-054 no diff
| Item | Presente? | Evidência |
```
