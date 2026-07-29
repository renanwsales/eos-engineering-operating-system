# 05 — Classificação de problemas

Sem classificação, toda revisão vira uma lista plana onde um `float` em cálculo de dinheiro
aparece ao lado de um import fora de ordem. A classificação é o que permite agir.

Todo achado recebe quatro atributos: **severidade**, **confiança**, **esforço** e **risco de
correção**. Desses quatro sai a classe (`MUST-FIX` ou `OPPORTUNITY`) e a prioridade.

---

## Severidade

A severidade mede **consequência**, nunca esforço nem elegância.

### S0 — Crítico

Dano ativo ou iminente, sem contorno.

- Vazamento ou exposição de dado pessoal, credencial ou segredo.
- Falha de autorização que permite acessar ou alterar dado de outro usuário/tenant.
- Perda ou corrupção de dados.
- Erro de cálculo financeiro.
- Indisponibilidade total, ou caminho de crash trivialmente alcançável.
- Execução remota de código, injeção explorável.

**Ação:** para tudo. Corrige antes de qualquer outra atividade. Não vai para o backlog.

### S1 — Alto

Quebra funcional real, ou risco de segurança com pré-condição.

- Regra de negócio incorreta em fluxo principal.
- Estado inválido representável e alcançável no fluxo normal.
- Falha de autorização que exige condição incomum.
- Ausência de integridade no banco em dado crítico.
- Degradação de performance que torna um fluxo inutilizável sob carga real.
- Ação destrutiva sem confirmação nem desfazer.
- Ausência total de teste em regra de negócio crítica.

**Ação:** bloqueia a entrega do módulo. `MUST-FIX`.

### S2 — Médio

Funciona, mas com custo relevante — de manutenção, de confiabilidade ou de experiência.

- Regra duplicada com risco de divergir.
- Caso de borda não tratado fora do fluxo principal.
- Ausência de estado de erro/vazio na interface.
- Barreira de acessibilidade que impede uma tarefa por teclado ou leitor de tela.
- Log sem contexto que impedirá diagnosticar um incidente.
- Teste frágil que vai falhar de forma intermitente.
- Acoplamento que fará a próxima mudança nesta área custar muito mais.

**Ação:** `MUST-FIX` se estiver no caminho da mudança atual; `OPPORTUNITY` caso contrário.

### S3 — Baixo

Melhoria sem consequência funcional demonstrável.

- Inconsistência de nomenclatura em relação às normas.
- Código morto.
- Comentário desatualizado.
- Duplicação pequena e estável.
- Oportunidade de simplificação sem métrica associada.

**Ação:** `OPPORTUNITY`. Nunca bloqueia. Só é corrigido quando o arquivo já está sendo tocado
por outro motivo e o custo é praticamente zero.

---

## Confiança

| Nível | Significado |
| --- | --- |
| `HIGH` | Verificado por execução, ou leitura inequívoca do código com o contexto completo |
| `MEDIUM` | Evidência estática forte, sem execução; depende de premissa razoável |
| `LOW` | Reconhecimento de padrão, sem confirmar o contexto real |

**Regras:**
- Achado `LOW` **não pode** ser `MUST-FIX`. Ele vira uma pergunta aberta ou uma investigação.
- `S0` exige confiança `HIGH`. Sem verificação, é `HYPOTHESIS` com prioridade máxima de
  investigação — o que é diferente de um achado.
- **Exceção de segurança:** em caminhos de autenticação, autorização, pagamento e dados
  pessoais, confiança `MEDIUM` já bloqueia. O ônus da prova se inverte: é preciso demonstrar
  que está seguro, não que está inseguro.

---

## Esforço

Estimativa de implementação **mais** validação, não só de escrever o código.

| Nível | Referência |
| --- | --- |
| `XS` | < 30 min, um arquivo, sem risco |
| `S` | < 2 h, poucos arquivos, testes existentes cobrem |
| `M` | < 1 dia, exige testes novos |
| `L` | 2–5 dias, toca contrato ou vários módulos |
| `XL` | > 1 semana, exige ADR e plano de migração |

`XL` nunca entra numa rodada de revisão. Vai para o backlog como proposta com ADR.

---

## Risco de correção

Frequentemente ignorado, é o que causa o pior resultado possível: uma revisão que introduz um
defeito pior do que o que corrigiu.

| Nível | Característica |
| --- | --- |
| `LOW` | Escopo isolado, coberto por testes, reversível por commit |
| `MEDIUM` | Toca código compartilhado, cobertura parcial, exige regressão ampla |
| `HIGH` | Contrato público, schema, migração, autenticação, concorrência, sem cobertura |

Correção `HIGH` entra **isolada**, com plano de rollback declarado, e nunca junto de outras
mudanças no mesmo commit ou PR.

---

## `MUST-FIX` versus `OPPORTUNITY`

Esta separação é o coração do EOS. Manter as duas listas separadas é obrigatório em todo
relatório.

### É `MUST-FIX` quando qualquer condição se aplica:

- Severidade `S0` ou `S1`.
- `S2` no caminho direto da mudança atual (você já está mexendo ali).
- Viola uma norma de `standards/` marcada como **obrigatória**.
- Impede a [Definition of Done](08-definition-of-done.md) do módulo.
- Segurança em caminho sensível com confiança ≥ `MEDIUM`.

### É `OPPORTUNITY` em todos os outros casos:

- `S2` fora do escopo atual, e todo `S3`.
- Melhoria arquitetural sem defeito ativo associado.
- Esforço `L` ou `XL` sem urgência.
- Qualquer coisa com confiança `LOW`.

**Toda `OPPORTUNITY` vai para o [backlog](12-gestao-de-backlog.md).** Sem exceção. É o que
mantém o produto vivo em vez de transformar cada revisão numa lista descartável.

---

## Antipadrões de classificação

| Antipadrão | Por que é grave |
| --- | --- |
| Inflar severidade para conseguir aprovação da mudança | Destrói a confiança na classificação inteira |
| Marcar preferência de estilo como `S2` | Ruído que faz o leitor ignorar os achados reais |
| Classificar por esforço ("é fácil, então faço agora") | Facilidade não é justificativa; consequência é |
| Reportar 40 itens `S3` e 2 itens `S1` na mesma lista | Os `S1` desaparecem |
| Usar `S0` para chamar atenção | `S0` significa "pare tudo". Uso indevido é falha grave de processo |
| Deixar `OPPORTUNITY` só no chat | Trabalho de diagnóstico jogado fora |

---

## Tabela de decisão rápida

| Severidade | Confiança | No escopo? | Classe |
| --- | --- | --- | --- |
| S0 | HIGH | qualquer | `MUST-FIX` — para tudo |
| S0 | < HIGH | qualquer | Investigar imediatamente (`HYPOTHESIS`) |
| S1 | ≥ MEDIUM | qualquer | `MUST-FIX` |
| S1 | LOW | qualquer | Investigar antes de classificar |
| S2 | ≥ MEDIUM | sim | `MUST-FIX` |
| S2 | ≥ MEDIUM | não | `OPPORTUNITY` |
| S2/S3 | LOW | qualquer | `OPPORTUNITY` (ou descartar) |
| S3 | qualquer | qualquer | `OPPORTUNITY` |
