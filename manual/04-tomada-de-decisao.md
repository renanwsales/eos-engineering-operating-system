# 04 — Tomada de decisão

O objetivo deste processo é impedir a falha mais comum em revisões assistidas por IA: partir
direto do problema para *uma* solução, aquela que veio primeiro à cabeça, e tratá-la como
inevitável.

---

## Passo 1 — Reformule o problema como restrição

Uma restrição descreve o que precisa ser verdade. Uma solução descreve como. Começar pela
solução elimina alternativas antes de considerá-las.

| Formulação errada (solução disfarçada) | Formulação correta (restrição) |
| --- | --- |
| "Precisamos adicionar Redis" | "Leituras repetidas do catálogo não podem custar uma consulta por requisição" |
| "Precisamos migrar para microsserviços" | "O time de pagamentos precisa fazer deploy sem coordenar com o time de catálogo" |
| "Precisamos usar uma máquina de estados" | "Um pedido não pode transitar para `enviado` sem estar `pago`" |
| "Precisamos refatorar esse arquivo" | "Mudar a regra de frete não deve exigir tocar em lógica de autenticação" |

Se você não consegue enunciar a restrição sem nomear tecnologia, você ainda não entendeu o
problema.

---

## Passo 2 — Gere alternativas reais

Mínimo de duas alternativas viáveis, mais a opção zero.

**"Não fazer nada" é sempre uma alternativa obrigatória.** Ela é a escolha certa com mais
frequência do que parece: quando o custo excede o dano, quando o módulo será substituído,
quando o risco é aceitável e monitorado, quando falta informação e a decisão pode esperar.

Uma alternativa é real quando existe um cenário plausível em que ela seria escolhida. Se você
escreveu a alternativa B apenas para cumprir o processo, o processo falhou — pense de novo ou
declare que só existe um caminho viável e por quê.

Fontes de alternativas quando você só consegue pensar em uma:
- **Mudar a camada:** resolver no banco, na aplicação, no cliente ou na infraestrutura.
- **Mudar o momento:** validar na escrita ou na leitura; síncrono ou assíncrono.
- **Mudar o alcance:** consertar só o caso reportado ou toda a classe do problema.
- **Mudar a forma:** prevenir por tipo, por constraint, por teste ou por monitoramento.
- **Comprar em vez de construir**, ou o inverso.

---

## Passo 3 — Compare nas seis dimensões

| Dimensão | O que perguntar |
| --- | --- |
| **Correção** | Resolve o problema inteiro ou apenas o sintoma observado? |
| **Custo** | Esforço de implementação + revisão + manutenção contínua |
| **Risco** | O que pode quebrar, e o dano se quebrar (ver [matriz de risco](07-matriz-de-risco.md)) |
| **Reversibilidade** | Quanto custa desfazer depois de 3 meses em produção? |
| **Carga operacional** | Novo componente para monitorar, escalar, atualizar, pagar? |
| **Aderência** | Combina com a arquitetura atual ou cria um segundo jeito de fazer a mesma coisa? |

Peso: **correção** é eliminatória. Alternativa que não resolve o problema inteiro sai da mesa,
salvo se declarada explicitamente como mitigação temporária com prazo e item de backlog.

Depois de correção, **reversibilidade** é a dimensão mais subestimada. Uma decisão medíocre e
reversível é melhor do que uma boa decisão irreversível tomada com informação incompleta.

---

## Passo 4 — Escolha e declare o que você aceitou

Toda escolha é uma troca. Declare a troca:

> Escolhida a alternativa B. Aceito 15% mais código e uma dependência nova em troca de
> eliminar a possibilidade estrutural do estado inválido, em vez de apenas validá-lo.

E declare a condição de invalidação:

> Esta decisão se torna errada se o volume de escrita passar de ~500/s, quando o custo da
> constraint superaria o ganho. Nesse ponto, reavaliar a alternativa A.

A condição de invalidação é o que transforma uma decisão em conhecimento reutilizável. Sem
ela, ninguém no futuro sabe se a decisão ainda vale.

---

## Passo 5 — Registre no nível adequado

| Tipo de decisão | Onde registrar |
| --- | --- |
| Muda contrato público (API, schema, evento, tipo exportado) | [ADR](../templates/adr.md) obrigatório |
| Escolha de tecnologia ou padrão que outros vão seguir | ADR obrigatório |
| Aceitação consciente de risco | ADR + [matriz de risco](07-matriz-de-risco.md) |
| Custosa de reverter (>1 dia para desfazer) | ADR obrigatório |
| Escolha local com alternativa não óbvia | Comentário no código explicando o *porquê*, nunca o *o quê* |
| Escolha local óbvia | Nada. Não documente o trivial |

---

## Reversibilidade: a escala

Prefira sempre o degrau mais alto que resolva o problema completamente.

```
1. Flag de configuração          — reverter em segundos, sem deploy
2. Função isolada                — reverter em um commit
3. Interno de um módulo          — reverter em um commit, testes locais
4. Interface de um módulo        — exige atualizar chamadores
5. Contrato entre módulos        — exige coordenação, possível versionamento
6. Schema de banco (aditivo)     — reversível com migração reversa testada
7. Schema de banco (destrutivo)  — irreversível sem backup
8. Migração de dados             — irreversível na prática
```

Degraus 6 a 8 exigem: ADR, backup verificado, migração reversa escrita **e testada**, e janela
de execução acordada. Degrau 7 e 8 sempre param para aprovação humana.

---

## Antipadrões de decisão

| Antipadrão | Como se manifesta | Correção |
| --- | --- | --- |
| **Solução procurando problema** | "Vamos adicionar X" antes de enunciar a restrição | Volte ao passo 1 |
| **Alternativa de fachada** | B é obviamente pior e existe só para cumprir tabela | Gere alternativa real ou declare caminho único |
| **Falsa urgência** | Tratar `S3` como se bloqueasse entrega | Aplique a [matriz de priorização](06-matriz-de-priorizacao.md) |
| **Solução acoplada** | Uma mudança que resolve cinco problemas ao mesmo tempo | Separe: uma decisão por problema |
| **Otimismo de migração** | Assumir que a migração vai funcionar sem testar a reversa | Escreva e teste a reversa antes |
| **Decisão sem dono** | Risco aceito sem ninguém nomeado | Nomeie quem aceitou, ou escale |
| **Reabertura infinita** | Rediscutir decisão registrada sem informação nova | Só reabra com a condição de invalidação atendida |

---

## Quando *não* decidir

Postergar é uma decisão legítima e deve ser registrada como tal. Poste quando:

- A informação que falta chega em breve e é decisiva.
- A decisão fica mais barata depois de outra mudança já planejada.
- O custo de errar agora é maior do que o custo de esperar.

Registre como postergada com: o que falta, quem traz, e a data ou evento que reabre. Postergar
sem registro não é postergar — é esquecer.
