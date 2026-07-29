# Template — Entrada de backlog

Use para **toda** `OPPORTUNITY` encontrada e não corrigida, registrada na mesma sessão em que foi
encontrada. Ver [gestão de backlog](../volumes/vol-11-auditoria.md).

---

## Forma curta (o padrão)

```
[EOS-NNN] <título dizendo a consequência, não o sintoma>
Severidade: S0|S1|S2|S3 | Confiança: HIGH|MEDIUM|LOW | Esforço: XS|S|M|L|XL | Risco: LOW|MEDIUM|HIGH
Score: <número>
Evidência: <arquivo:linha> (ou comando + saída)
Consequência se ignorado: <o que quebra, para quem, quando>
Gatilho de promoção: <o que faz este item deixar de esperar>
Origem: <rodada/auditoria, data>
Status: aberto
```

O **gatilho de promoção** é o campo mais importante e o mais esquecido. Sem ele, o item depende de
alguém reler o backlog por acidente.

Exemplos de gatilho: "qualquer mudança neste arquivo" · "quando o volume passar de 10 mil/dia" ·
"na próxima auditoria de segurança" · "se o defeito reincidir" · "quando migrarmos para a versão 15".

---

## Forma longa (esforço `L`/`XL`, ou risco alto)

```
[EOS-NNN] <título>

## Classificação
Severidade: <> | Confiança: <> | Esforço: <> | Risco de corrigir: <> | Score: <>
Camada: <arquitetura|domínio|segurança|dados|performance|ux|testes|entrega>
Papel responsável: <>

## Evidência
<arquivo:linha, ou comando + saída>

## Problema como restrição
<uma frase, livre de solução>

## Consequência se ignorado
<concreta: o que quebra, para quem, sob qual condição, com que frequência>

## Por que não foi feito agora
<decisão explícita: fora de escopo | esforço alto | depende de X | risco de corrigir agora>
Decidido por: <nome>

## Gatilho de promoção
<preencher>

## Abordagem provável
<esboço, não projeto. Duas linhas>
Precisa de ADR? <sim|não>

## Dependências
<o que precisa acontecer antes>

## Histórico
| Data | Evento |
| <data> | criado a partir de <origem> |
| <data> | postergado na rodada <n> (1ª vez) |
```

Regra das três postergações: no terceiro adiamento, decida entre promover ou marcar `não faremos`.
Nunca postergue uma quarta vez.

---

## Dívida técnica assumida deliberadamente

Formato específico. Dívida sem estes campos não é dívida — é defeito não registrado.

```
[EOS-NNN] <o que foi deixado incompleto>
Dívida assumida em: <data>, para <motivo — prazo, lançamento, dependência>
Custo de manter: <concreto: horas/mês, risco, retrabalho>
Custo de pagar: <esforço>
Gatilho: <o que obriga a reavaliar>
Aceito por: <nome — pessoa, não "o time">
Monitoramento: <o que revelaria a materialização do risco>
```

---

## Estados

```
aberto → em análise → priorizado → em execução → concluído
   │                                      │
   ├──────────▶ não faremos ◀─────────────┘
   └──────────▶ obsoleto
```

`não faremos` exige motivo escrito e é um estado **saudável**. Backlog que só cresce perde utilidade.

`obsoleto` quando a evidência (`arquivo:linha`) não existe mais e o item deixou de fazer sentido.

---

## O que não entra

- Ideia sem consequência nomeada.
- Preferência de estilo sem norma associada.
- "Investigar se dá para melhorar X" sem hipótese concreta.
- Refatoração sem defeito, métrica ou norma associada.

Backlog cheio de item vago é indistinguível de backlog vazio: ninguém consegue priorizá-lo.
