# ADR-0001 — Adotar um framework de engenharia em camadas em vez de um prompt único

| Campo | Valor |
| --- | --- |
| Status | aceito |
| Data | 2026-07-29 |
| Decisor | dono do produto |
| Consultados | — |
| Faixa de risco | R1 |
| Reversibilidade | degrau 1 — é documentação; abandonar custa zero em código |

---

## Contexto

Prompts longos para revisão de código produzem resultados inconsistentes. O padrão observado é
sempre o mesmo:

- **Achados superficiais.** O modelo lista problemas de estilo e nomenclatura porque são os mais
  fáceis de encontrar por leitura linear, e não chega aos defeitos de domínio, autorização e
  concorrência.
- **Refatoração cosmética.** Mudanças justificadas por "mais limpo" ou "best practice", sem defeito,
  métrica ou norma associada. O diff cresce, o risco cresce, e nada foi resolvido.
- **Solução única.** A primeira abordagem que surge é apresentada como inevitável, sem alternativa
  comparada.
- **Validação afirmada, não executada.** "Isso resolve o problema" sem comando rodado.
- **Volume como sinal de qualidade.** Quarenta observações triviais escondem os três defeitos reais, e
  treinam o leitor a ignorar o relatório inteiro.
- **Trabalho perdido.** Achados que não entram em backlog são redescobertos na revisão seguinte.

A causa raiz é estrutural: um prompt único mistura **instruções**, **objetivos** e **critérios** num
só texto. O modelo não tem como saber o que é obrigatório, o que é preferência, em que ordem
investigar, nem o que caracteriza "pronto".

## Problema como restrição

> A qualidade da revisão não pode depender de quem escreveu o prompt, de qual modelo foi usado, nem da
> ordem em que o modelo escolheu ler os arquivos.

## Alternativas consideradas

### A — Um prompt único e mais detalhado (2 a 3 páginas)

- Como funciona: um único texto com mais instruções e mais checklists.
- Custo: baixo para escrever.
- Risco: alto. Não resolve a mistura de camadas; apenas a torna mais longa. Quanto mais longo o
  prompt, mais as instruções do meio são diluídas.
- Reversibilidade: total.
- Retorno: marginal. É o que já falha hoje, com mais palavras.

### B — Framework em camadas com papéis, portões e normas (escolhida)

- Como funciona: filosofia e processo separados de normas técnicas, separados de papéis, separados de
  portões de verificação. Um roteador (`AGENTS.md`) carrega apenas o que a tarefa exige.
- Custo: alto para escrever uma vez; baixo para usar. Exige preencher um perfil por projeto.
- Risco: médio. O principal é o excesso de cerimônia — processo mais caro que o trabalho. Mitigado por
  compressão de portões para mudanças triviais e por carregamento seletivo de documentos.
- Reversibilidade: total. É documentação.
- Retorno: alto e reutilizável. Serve qualquer módulo e qualquer projeto.

### C — Não fazer nada, continuar com prompts avulsos

- O que acontece: os seis problemas acima continuam, com custo proporcional ao tamanho do sistema.
- Custo de conviver: retrabalho de diagnóstico em cada revisão; defeitos estruturais nunca alcançados;
  risco de que uma revisão introduza um defeito pior do que corrigiu.
- O que faria isso deixar de ser aceitável: já é inaceitável para módulos que tratam dinheiro, acesso
  ou dado pessoal.

### Comparação

| Critério | A | B | C |
| --- | --- | --- | --- |
| Resolve o problema inteiro | não | sim | não |
| Custo | baixo | alto uma vez, baixo por uso | zero |
| Risco | alto (falso senso de rigor) | médio (excesso de cerimônia) | alto |
| Reversibilidade | total | total | total |
| Carga operacional | nenhuma | manter as normas atualizadas | nenhuma |
| Aderência | — | serve qualquer stack | — |

## Decisão

Escolhida: **B — framework em camadas**.

### Troca aceita

Aceito um custo inicial alto de escrita e a obrigação de manter as normas vivas, em troca de revisões
cuja profundidade não depende de quem escreveu o prompt. Aceito também que tarefas triviais paguem um
pequeno custo de enquadramento — mitigado pela compressão explícita de portões.

### Condição de invalidação

Esta decisão se torna errada se:

- O processo passar a consumir mais esforço do que o trabalho que orienta em mais de uma rodada
  consecutiva. Nesse caso, reduzir o núcleo em vez de abandoná-lo.
- Os modelos evoluírem ao ponto de aplicarem consistentemente ordem de análise, protocolo de decisão e
  validação sem instrução explícita. Nesse ponto, o framework se reduz às normas e aos limiares — que
  são específicos do projeto e continuarão necessários.

---

## Consequências

**Positivas:** ordem de análise garantida; toda afirmação exige evidência; toda mudança exige
alternativa descartada; refatoração cosmética tem veto explícito; achados sobrevivem à sessão via
backlog; qualidade fica mensurável por dimensão.

**Negativas:** volume de documentação a manter; risco de as normas divergirem da prática real do
código (o que as torna piores do que ausência de normas); tarefas triviais pagam um custo pequeno de
enquadramento.

**Novas obrigações:** o perfil do projeto precisa ser preenchido e mantido; as normas precisam ser
revisadas quando a prática divergir; divergências deliberadas exigem ADR próprio.

**Impacto em contratos públicos:** nenhum. É documentação.

---

## Plano de execução

| Fase | O que | Reversível? |
| --- | --- | --- |
| 1 | Escrever núcleo, manual, normas, papéis, checklists e templates | sim |
| 2 | Preencher o perfil do primeiro projeto alvo (EOS-001) | sim |
| 3 | Rodar uma revisão completa em um módulo real e medir o resultado | sim |
| 4 | Ajustar limiares e normas conforme o aprendizado da fase 3 | sim |

## Verificação

Como saberemos que funcionou, na primeira revisão real:

1. Proporção de achados de domínio, segurança e dados versus achados de estilo — deve inverter em
   relação ao padrão atual.
2. Nenhuma mudança entregue sem validação com saída de comando registrada.
3. Toda `OPPORTUNITY` reportada aparece no backlog: reportadas = registradas.
4. Nenhum item cosmético no diff final.

## Rollback

Parar de usar. Custo zero em código.
