# 01 — Filosofia de Engenharia

Este documento existe para resolver discussões, não para inspirar. Cada princípio tem uma
consequência prática e uma regra de desempate quando colide com outro.

---

## Os oito princípios

### 1. Correção antes de elegância

Código elegante que está errado é pior do que código feio que está certo, porque a elegância
inspira confiança. A primeira pergunta em qualquer revisão é "isto está correto sob todas as
entradas possíveis?", não "isto está bonito?".

**Na prática:** um caso de borda não tratado é `S1`. Um padrão de projeto ausente é, no
máximo, `OPPORTUNITY`.

### 2. O código existente tem razões

Todo trecho estranho foi escrito por alguém resolvendo um problema real, muitas vezes um
problema que não está mais visível. Antes de "corrigir", procure a razão: histórico do git,
issue vinculada, teste que cobre o comportamento, comentário adjacente.

**Na prática:** ao propor remover uma verificação aparentemente redundante, você deve
declarar o que aconteceria se ela existisse por um motivo que você não encontrou.

### 3. Mudança é custo, não progresso

Toda linha alterada carrega risco de regressão, custo de revisão, custo de deploy e custo de
rollback. Progresso é problema resolvido, não linha escrita. A ausência de mudança é o padrão
e precisa ser vencida por um argumento.

**Na prática:** "por que mudar isso agora?" é sempre uma pergunta legítima, e a resposta
"porque está errado" precisa vir com a definição de errado.

### 4. Duplicação é mais barata que a abstração errada

Duplicação é visível, local e fácil de remover. A abstração errada é invisível, global e
propaga a decisão errada por todo o sistema. Espere o terceiro caso real antes de abstrair —
e o terceiro caso precisa ser *realmente* o mesmo, não parecido.

**Na prática:** abstração criada para um único uso é rejeitada. Duas duplicações são
aceitáveis e devem ser anotadas, não eliminadas.

### 5. Explícito vence esperto

Otimize para o leitor que chega às 3h da manhã durante um incidente, sem contexto e sob
pressão. Toda economia de digitação paga com clareza é um empréstimo com juros.

**Na prática:** comportamento implícito (side effects escondidos, magia de framework,
inferência sutil) precisa ser documentado ou removido. Fluxo de controle não óbvio é `S2`.

### 6. Sem medição não há performance

Intuição sobre desempenho é errada com frequência suficiente para ser inútil. Nenhuma
otimização entra sem número antes e número depois, obtidos pelo mesmo método.

**Na prática:** "melhorei a performance" sem medida é rejeitado como afirmação e registrado
como refatoração cosmética.

### 7. Segurança e dados não têm zona cinzenta

Autenticação, autorização, dados pessoais, dinheiro e destruição de dados operam sob regras
diferentes: ambiguidade nesses caminhos é bloqueio, não risco aceitável. O padrão é negar.

**Na prática:** dúvida sobre quem pode acessar o quê interrompe o trabalho e escala para o
dono humano. Confiança `MEDIUM` já é bloqueante nesses caminhos.

### 8. O produto está vivo

Um módulo nunca está "pronto para sempre" — está pronto *para agora*, com uma lista conhecida
do que foi deliberadamente deixado de fora. Dívida decidida e registrada é engenharia; dívida
esquecida é negligência.

**Na prática:** toda revisão termina com o backlog atualizado. Achado que só existe no chat
foi trabalho jogado fora.

---

## Regra de desempate

Quando dois princípios colidem, decida na ordem abaixo. O item mais alto vence sempre. Esta
ordem é lexicográfica: só se passa ao próximo critério quando há empate real no anterior.

```
1. Segurança e integridade de dados
2. Correção do comportamento
3. Reversibilidade da decisão
4. Clareza para quem mantém
5. Performance
6. Consistência com o padrão existente
7. Elegância e concisão
```

**Exemplos de aplicação:**

| Conflito | Resolução |
| --- | --- |
| Correção exige quebrar o padrão do projeto | Corrija (2 vence 6) e registre a divergência em ADR |
| Otimização deixa o código obscuro | Não otimize (4 vence 5), a menos que a métrica esteja violando um limiar declarado |
| Solução mais limpa exige migração destrutiva | Escolha a reversível (3 vence 7) |
| Consistência exige repetir um padrão insegura | Rompa a consistência (1 vence 6) e proponha migração do resto |

---

## O que rejeitamos explicitamente

- **Perfeccionismo sem alvo.** "Poderia ser melhor" não é justificativa. Melhor em qual
  métrica, para quem, a que custo?
- **Modernização por moda.** Trocar tecnologia funcionando por tecnologia nova exige ADR com
  ganho quantificado e plano de migração.
- **Cobertura de testes como meta.** Cobertura é sintoma, não objetivo. 90% de cobertura em
  getters e 0% nas regras de negócio é pior que 50% bem distribuído.
- **Revisão por volume.** Trinta observações de estilo escondem os três defeitos reais. O
  ruído tem custo: ele faz o leitor parar de ler.
- **Autoridade por citação.** "É best practice" não encerra discussão. O argumento precisa
  ser feito no contexto deste sistema, com estas restrições.

---

## O critério final

> Um sistema é bem construído quando a próxima pessoa consegue mudá-lo com segurança sem
> perguntar nada a quem o escreveu.

Toda decisão de engenharia pode ser avaliada por essa frase. Ela mede simultaneamente
clareza, testes, documentação, acoplamento e observabilidade — porque a falha em qualquer um
deles obriga a pergunta.
