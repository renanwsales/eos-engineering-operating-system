# Checklist — Módulo concluído (portão G5)

O último portão antes de declarar um módulo entregue. Executado pelo
[auditor final](../agents/09-final-auditor.md), que **não** participou da implementação.

Regra: toda afirmação de validação é tratada como não verificada até que a evidência apareça.

---

## 1. Verificação das afirmações

- [ ] Para cada `CHANGE REPORT`, a validação declarada realmente aconteceu — com saída de comando.
- [ ] Nenhuma afirmação de "melhorou a performance" sem antes e depois pelo mesmo método.
- [ ] Nenhuma correção de segurança validada apenas por "os testes passam".
- [ ] Rodei eu mesmo a suíte, a verificação de tipos e o lint.

Afirmação sem evidência conta como **falha**, não como pendência.

## 2. Integridade do escopo

- [ ] Cada arquivo do diff corresponde a uma proposta aprovada.
- [ ] Nenhuma mudança cosmética misturada com comportamento.
- [ ] Nenhuma dependência nova não prevista.
- [ ] Nenhum código removido sem justificativa — remoção é mudança de comportamento.
- [ ] Nenhuma formatação em massa dentro de commit de lógica.

Escopo não aprovado é código não revisado entrando sob a cobertura de código revisado.

## 3. Caça a regressões

- [ ] **Interação:** mudanças corretas isoladamente, contraditórias em conjunto.
- [ ] **Código compartilhado:** função alterada para um chamador, usada por outros.
- [ ] **Contrato:** servidor mudou e cliente não (ou o inverso).
- [ ] **Janela de deploy:** código antigo e novo coexistindo — ambos funcionam?
- [ ] **Dado existente:** a nova regra vale para o que já está no banco?
- [ ] **Formato em cache:** código novo lê valor cacheado no formato antigo?
- [ ] **Mensagens em trânsito:** enfileiradas antes da mudança.
- [ ] **Clientes antigos:** app móvel que não vai atualizar por semanas.
- [ ] **Mudança silenciosa:** valor padrão, ordem de listagem, arredondamento, fuso, código de erro.
- [ ] **Teste afrouxado:** revisei **cada** teste alterado. Asserção mudou porque o comportamento
      antigo estava errado, ou porque o novo não casava? O segundo caso é `S1`.
- [ ] **Nova intermitência:** algum teste passou a depender de tempo, ordem ou estado compartilhado.

## 4. Definition of Done por mudança

- [ ] Rodada item por item para cada mudança.
- [ ] Todo `N/A` tem justificativa.
- [ ] Nenhum item `PENDENTE`.
- [ ] DoD reduzida (correção emergencial de `S0`) tem item de backlog para a rodada seguinte.

## 5. Severidades em aberto

- [ ] Zero `S0`.
- [ ] Zero `S1` não corrigido.
- [ ] Todo `S2` conhecido está registrado no backlog com ID.
- [ ] Nenhuma severidade foi inflada nem deflacionada indevidamente.

## 6. Camadas cobertas

- [ ] Está declarado quais camadas de [análise](../manual/03-ordem-de-analise.md) foram cobertas e
      quais não foram.
- [ ] Camada não analisada está registrada como risco conhecido, não omitida.

## 7. Backlog

- [ ] **Toda** `OPPORTUNITY` reportada está no backlog. Contei: reportadas versus registradas.
- [ ] Cada entrada tem severidade, esforço, evidência e **gatilho de promoção**.
- [ ] Dívida assumida deliberadamente tem custo estimado e quem a aceitou.
- [ ] Itens obsoletos foram encerrados.

## 8. Operação

- [ ] Rollback existe, é um comando, e foi testado.
- [ ] Compatibilidade durante o deploy verificada nos dois sentidos.
- [ ] Falha nova é detectável: existe log, métrica ou alerta.
- [ ] Verificação de saúde valida dependências reais.
- [ ] Migração: reversa testada, dado existente verificado, separada de mudança de comportamento.
- [ ] Runbook existe para cada alerta novo.

## 9. Notas

Atribuir 0–10 por dimensão, com os pesos de
[métricas](../manual/10-metricas-de-qualidade.md#notas-da-auditoria):

| Dimensão | Peso | Nota | Justificativa |
| --- | --- | --- | --- |
| Segurança | 20% | | |
| Correção de domínio | 20% | | |
| Dados e integridade | 15% | | |
| Testes | 15% | | |
| Arquitetura | 10% | | |
| Performance | 8% | | |
| UX e acessibilidade | 7% | | |
| Observabilidade e entrega | 5% | | |
| **Total ponderado** | | | |

Lembretes de calibragem:

- Nota 10 exige [Definition of Excellence](../manual/09-definition-of-excellence.md) na dimensão.
- **Ausência de problemas não é excelência.** Módulo sem achados, sem testes, sem observabilidade e
  sem decisões registradas fica em torno de 5 — não se sabe se funciona.
- Travas: qualquer `S0` ou `S1` não corrigido limita o total a 4 e força `REJECTED`. Segurança abaixo
  de 6 limita a `APPROVED WITH CONDITIONS`.

## 10. Veredito

- [ ] `APPROVED` — sem `S0`/`S1`, DoD completa, escopo íntegro, backlog atualizado, afirmações
      verificadas.
- [ ] `APPROVED WITH CONDITIONS` — restam apenas itens triviais e verificáveis, listados como
      condições explícitas.
- [ ] `REJECTED` — qualquer `S0`, `S1` não corrigido, escopo não aprovado, afirmação não verificada,
      ou regressão detectada.

- [ ] Risco residual está registrado, com monitoramento e **nome** de quem o aceitou.

---

## Uma pergunta final

> Se o time inteiro sair de férias amanhã, este módulo continua operando, e um novo desenvolvedor
> consegue corrigir um bug nele na primeira semana?

Se a resposta é não, nomeie exatamente o que falta e registre no backlog antes de aprovar.
