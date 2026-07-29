# 02 — Processo de Engenharia: os seis portões

O trabalho avança por portões. Cada portão tem entrada, saída e critério de passagem. Não se
pula portão; pode-se **comprimir** um portão, declarando que comprimiu e por quê.

```
G0 Descoberta ──▶ G1 Diagnóstico ──▶ G2 Decisão ──▶ G3 Implementação ──▶ G4 Validação ──▶ G5 Auditoria
     │                  │                 │                │                  │                │
   mapa            achados com        alternativas      menor mudança       provas         regressões,
  do terreno         evidência        comparadas        reversível        executadas      notas, backlog
```

---

## G0 — Descoberta

**Objetivo:** entender o terreno antes de julgá-lo. Neste portão é **proibido** propor
mudanças ou apontar problemas.

**Entrada:** o pedido do usuário e o repositório.

**Atividades:**
1. Ler o [perfil do projeto](../templates/perfil-do-projeto.md). Se não existir, criá-lo é o
   primeiro entregável.
2. Mapear a estrutura: pontos de entrada, fronteiras de módulo, fluxo de dados principal.
3. Identificar o **domínio**: quais são as entidades, o que o sistema promete ao usuário.
4. Localizar as zonas de alto risco: autenticação, pagamento, dados pessoais, migrações.
5. Verificar o que já existe de teste, lint, CI e observabilidade — para não recomendar o que
   já está lá.
6. Ler o histórico recente (`git log`) das áreas que serão tocadas.

**Saída:** um mapa de 10 a 20 linhas com módulos, responsabilidades, dependências e zonas de
risco. Mais uma lista de perguntas abertas.

**Critério de passagem:** você consegue descrever o que o sistema faz, para quem, e onde uma
falha causaria o maior dano — sem consultar arquivos novamente.

**Erro típico:** começar a listar problemas na primeira leitura. Isso produz achados
superficiais (estilo, nomes) e faz perder os estruturais.

---

## G1 — Diagnóstico

**Objetivo:** produzir achados com evidência, classificados.

**Entrada:** o mapa de G0.

**Atividades:** percorrer as oito camadas na ordem obrigatória de
[03 — Ordem de análise](03-ordem-de-analise.md). Para cada achado, preencher o schema
`FINDING` completo, com `path:line`.

**Saída:** lista de achados ordenada por severidade, separada em `MUST-FIX` e `OPPORTUNITY`,
com perguntas abertas.

**Critério de passagem:**
- Todo achado tem evidência verificável ou está rotulado como `HYPOTHESIS`.
- Todo achado tem severidade, confiança, esforço e risco de correção.
- Nenhum achado é puramente estilístico sem violação de norma declarada em `standards/`.

**Erro típico:** confundir "não é como eu faria" com defeito. Se você não consegue nomear a
consequência, não é um achado.

---

## G2 — Decisão

**Objetivo:** escolher o que fazer, com alternativa descartada registrada.

**Entrada:** achados de G1 priorizados por [06 — Matriz de priorização](06-matriz-de-priorizacao.md).

**Atividades:**
1. Definir o escopo desta rodada: o que será feito **agora** e o que vai ao backlog.
2. Para cada item do escopo, produzir um `CHANGE PROPOSAL` com ≥2 alternativas.
3. Avaliar risco por [07 — Matriz de risco](07-matriz-de-risco.md) e aplicar a mitigação
   obrigatória da faixa.
4. Se houver mudança de contrato público ou decisão custosa de reverter, escrever
   [ADR](../templates/adr.md).
5. Definir a ordem de execução: dependências primeiro, risco alto isolado.

**Saída:** propostas aprovadas, ADRs quando aplicável, ordem de execução, backlog atualizado.

**Critério de passagem:**
- Nenhuma proposta com alternativa única.
- "Não fazer nada" foi considerado explicitamente em cada proposta.
- Cada proposta declara o que a invalidaria.

**Erro típico:** já ter decidido e escrever as alternativas como formalidade. Se a alternativa
B nunca poderia ser escolhida, ela não é uma alternativa — é enfeite.

---

## G3 — Implementação

**Objetivo:** executar a menor mudança reversível que resolve completamente o problema.

**Atividades:**
- Um concern por commit. Formatação, renomeação, comportamento e dependências são commits
  separados.
- Respeitar o orçamento de mudança de [11 — Processo de revisão](11-processo-de-revisao.md).
- Mudanças de risco `ALTO` entram isoladas, nunca acompanhadas.
- Se durante a implementação a proposta se revelar errada, **voltar para G2**. Não improvisar
  uma terceira solução no meio do caminho.

**Critério de passagem:** o diff corresponde à proposta aprovada. Diferenças precisam ser
declaradas e justificadas.

**Erro típico:** o "enquanto eu estava lá". Consertar coisas adjacentes não pedidas infla o
diff, mistura riscos e impossibilita o bisect.

---

## G4 — Validação

**Objetivo:** provar que funcionou e que nada mais quebrou. **Uma mudança não validada não
existe.**

**Atividades, em ordem:**
1. Verificação mais estreita possível: o teste específico, a chamada específica.
2. Type check e lint no escopo alterado.
3. Suíte de regressão plausivelmente afetada.
4. Para performance: medir antes e depois pelo mesmo método, reportar os dois números.
5. Para segurança: demonstrar que o caminho de exploração está fechado, não apenas que os
   testes passam.
6. Para UX: verificar o fluxo completo, não o componente isolado.

**Saída:** `CHANGE REPORT` com as verificações executadas e seus resultados literais.

**Critério de passagem:** [Definition of Done](08-definition-of-done.md) integralmente
atendida, com cada item `N/A` justificado.

**Erro típico:** relatar "deve funcionar". Se a validação é impossível no ambiente, diga
exatamente qual comando um humano precisa rodar.

---

## G5 — Auditoria

**Objetivo:** olhar o conjunto, não a peça.

**Atividades:**
1. Rodar o [checklist de módulo concluído](../checklists/modulo-concluido.md).
2. Buscar regressões e interações entre as mudanças desta rodada (o que passa isolado pode
   falhar em conjunto).
3. Atribuir notas por dimensão via `AUDIT REPORT`.
4. Registrar risco residual e quem o aceitou.
5. Atualizar o [backlog](12-gestao-de-backlog.md) com tudo que ficou de fora.

**Saída:** veredito `APPROVED` / `APPROVED WITH CONDITIONS` / `REJECTED`.

**Critério de passagem:** ausência de `S0` e de `S1` não corrigido.

---

## Compressão de portões

Permitida para mudanças **trivialmente corretas**: correção de texto, erro de digitação,
correção coberta por um teste que já falha, ajuste de configuração reversível por flag.

Regras da compressão:
- G0–G2 podem ser comprimidos em um parágrafo.
- **G4 nunca é comprimido.** Validação não tem exceção.
- É obrigatório declarar: "portões G0–G2 comprimidos porque \<motivo\>".

Se, durante uma mudança comprimida, aparecer qualquer surpresa — o teste falha por outro
motivo, o arquivo tem mais dependências do que parecia — o processo **volta a G0**.

---

## Quando o processo volta atrás

| Situação | Volta para |
| --- | --- |
| A proposta se revelou inviável durante a implementação | G2 |
| A validação revelou um defeito diferente | G1 |
| O diagnóstico partiu de um entendimento errado do domínio | G0 |
| A auditoria encontrou regressão | G1, com o achado da regressão como entrada |

Voltar atrás é o comportamento correto e não deve ser evitado por parecer retrabalho. O
retrabalho caro é o que acontece em produção.
