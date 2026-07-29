# Backlog

Fonte única de trabalho pendente. Formato: [`templates/entrada-de-backlog.md`](../templates/entrada-de-backlog.md).

**Regra de entrada:** toda `OPPORTUNITY` encontrada e não corrigida entra aqui **na mesma sessão** em
que foi encontrada. Achado que só existe no chat é trabalho de diagnóstico jogado fora.

Se o projeto usa um rastreador de issues, use o rastreador **ou** este arquivo — nunca os dois.
Duplicidade de fonte é como o backlog morre.

---

## Ativos

Ordenados por score. Recalcular os 10 do topo a cada rodada.

| ID | Título | Sev. | Conf. | Esforço | Risco | Score | Gatilho de promoção | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EOS-001 | Perfil do projeto ainda não preenchido para o repositório alvo | S1 | HIGH | S | LOW | 20.0 | Primeira rodada de revisão em qualquer projeto | aberto |

### EOS-001 — Perfil do projeto ainda não preenchido

```
Severidade: S1 | Confiança: HIGH | Esforço: S | Risco: LOW | Score: 20.0
Evidência: templates/perfil-do-projeto.md contém apenas placeholders
Consequência se ignorado: todo julgamento técnico dos agentes fica sem base — stack, comandos de
  validação, limiares, classificação de módulos e tolerância a risco são desconhecidos. Sem os
  comandos, nenhuma mudança pode ser validada, e mudança não validada não existe.
Gatilho de promoção: primeira rodada de revisão em qualquer projeto que adote o EOS
Origem: criação do framework, 2026-07-29
Status: aberto
```

---

## Dívida assumida deliberadamente

| ID | O quê | Custo de manter | Custo de pagar | Gatilho | Aceito por |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | — |

---

## Não faremos

Estado saudável e necessário. Backlog que só cresce perde utilidade.

| ID | Título | Motivo da decisão | Data | Decidido por |
| --- | --- | --- | --- | --- |
| — | — | — | — | — |

---

## Obsoletos

| ID | Título | Por que deixou de existir | Data |
| --- | --- | --- | --- |
| — | — | — | — |

---

## Higiene periódica

Executada pelo orquestrador a cada rodada. Ver
[gestão de backlog](../manual/12-gestao-de-backlog.md).

- [ ] Verificar obsolescência: evidência (`arquivo:linha`) que não existe mais.
- [ ] Reavaliar severidade com os modificadores de contexto.
- [ ] Aplicar a **regra das três postergações**: no terceiro adiamento, promover ou marcar
      `não faremos`. Nunca postergar uma quarta vez.
- [ ] Agrupar itens relacionados no mesmo módulo — cinco itens costumam ser um item estrutural.
- [ ] Recalcular o score dos 10 do topo.

Reserva de capacidade que garante o avanço do backlog: **20% de cada rodada** vai para o item de maior
score daqui. Sem essa reserva, `MUST-FIX` consome 100% da capacidade indefinidamente e a dívida cresce
até virar `MUST-FIX` ela mesma — normalmente na forma de um incidente.

---

## Próximo ID disponível

`EOS-002`
