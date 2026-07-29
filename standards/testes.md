# Norma — Testes

Um teste tem uma única função: **detectar que algo importante quebrou**. Teste que não pode falhar
por um motivo real é custo puro — ele precisa ser mantido, executado e lido, sem nunca proteger
nada.

---

## Princípios

### V1. Teste comportamento, não implementação **[OBRIGATÓRIA]**

O teste descreve o que o sistema faz do ponto de vista de quem o usa. Se uma refatoração que
preserva comportamento quebra o teste, o teste estava testando a implementação.

Sinais: verificar que um método interno foi chamado; simular tudo, inclusive o que se está testando;
duplicar o cálculo da implementação dentro do teste.

### V2. Todo teste novo deve falhar antes **[OBRIGATÓRIA]**

Verifique que o teste falha sem a mudança. Teste que passa em qualquer circunstância é o mais
perigoso que existe: ele dá confiança sem dar proteção.

### V3. Determinístico **[OBRIGATÓRIA]**

Mesma entrada, mesmo resultado, em qualquer ordem, em qualquer máquina, sempre.

Proibido: depender de hora real, de aleatoriedade sem semente, de rede externa, de ordem de
execução, de estado deixado por outro teste, de espera fixa por tempo.

**Teste intermitente é pior do que nenhum teste**, porque treina o time a reexecutar o pipeline até
passar — e a ignorar falhas reais. Corrija ou remova em uma rodada. `retry` não é correção: é
ocultação.

### V4. Um motivo de falha por teste **[RECOMENDADA]**

A mensagem de falha deve dizer o que quebrou sem precisar depurar. Teste que verifica quinze coisas
esconde qual delas falhou.

### V5. Nome descreve o cenário **[OBRIGATÓRIA]**

```
Ruim:  test_pedido_1
Bom:   rejeita finalizar pedido quando o estoque do item é insuficiente
Bom:   mantém o total original quando o cupom está expirado
```

O nome é lido no relatório de falha, muitas vezes por quem não escreveu o teste.

### V6. Sem lógica no teste **[RECOMENDADA]**

Condicional e laço dentro de teste geralmente indicam que deveriam ser vários testes, ou um teste
por tabela de casos. Teste com lógica precisa ser depurado, e nada testa o teste.

---

## Cobertura

### V7. A cobertura que importa é de casos de negócio **[OBRIGATÓRIA]**

Cobertura de linhas é indicador; **cobertura dos casos declarados de cada regra de negócio** é a
meta. Uma regra de frete com cinco faixas precisa dos cinco casos, mais os limites entre elas — não
de uma linha executada.

Regra de negócio crítica sem teste é `S1`.

### V8. Perseguir percentual é antipadrão **[OBRIGATÓRIA]**

Escrever teste para getters, construtores e código trivial para elevar o percentual produz
manutenção sem proteção, e esconde a falta de cobertura onde importa.

### V9. Caminho de erro é testado **[OBRIGATÓRIA]**

É o menos testado e o mais executado em produção. Teste: falha de dependência, timeout, entrada
inválida, permissão negada, conflito de concorrência.

---

## Casos de borda obrigatórios

Verifique explicitamente, para cada entrada relevante:

| Categoria | Casos |
| --- | --- |
| **Ausência** | nulo, ausente, vazio, apenas espaços |
| **Quantidade** | zero, um, muitos, o limite, o limite mais um |
| **Sinal** | negativo, onde não deveria ser aceito |
| **Texto** | muito longo, caractere especial, emoji, unicode combinado, direção invertida |
| **Número** | zero, precisão decimal, arredondamento, estouro |
| **Tempo** | fuso, horário de verão, virada de dia/mês/ano, ano bissexto, ordem invertida |
| **Duplicidade** | envio repetido, requisição concorrente |
| **Estado** | transição inválida, operação em recurso já finalizado |
| **Permissão** | dono, não dono, outro tenant, sem autenticação |
| **Dependência** | indisponível, lenta, resposta inesperada |

Para dinheiro e cálculo, teste arredondamento explicitamente. É onde os defeitos silenciosos vivem.

---

## Estrutura da suíte

Proporção como orientação, não como meta — o que decide é onde o risco está.

| Nível | O que cobre | Característica |
| --- | --- | --- |
| **Unidade** | Regras de negócio puras | Muitos, rápidos, sem infraestrutura |
| **Integração** | Módulo com banco, com fila, com fornecedor simulado | Alguns, cobrem o que unidade não alcança |
| **Ponta a ponta** | Fluxos críticos completos | Poucos, caros, apenas os que geram receita ou risco |
| **Contrato** | Compatibilidade entre serviços | Onde há integração real |

### V10. Regra de negócio testável sem infraestrutura **[OBRIGATÓRIA]**

Se testar uma regra exige banco, rede e framework, a arquitetura está errada — ver
[A1](arquitetura.md#a1-direção-das-dependências-obrigatória). A dificuldade de testar é um
diagnóstico de acoplamento, não um problema de teste.

### V11. Simule fronteiras, não o próprio código **[RECOMENDADA]**

Simule o que sai do processo: rede, tempo, aleatoriedade, sistema de arquivos, fornecedor. Simular o
código sob teste transforma o teste numa afirmação sobre si mesmo.

### V12. Dados de teste explícitos **[RECOMENDADA]**

O teste mostra os valores que importam para o cenário. Fixture compartilhada gigante torna
impossível saber por que um teste falha. Use construtores com padrões e sobreponha só o relevante.

---

## Manutenção

### V13. Bug corrigido ganha teste de regressão **[OBRIGATÓRIA]**

O teste reproduz o defeito original e falha sem a correção. Sem isso, a reincidência é questão de
tempo — e reincidência é o sinal mais claro de processo de teste falho.

### V14. Nenhum teste desabilitado sem ID **[OBRIGATÓRIA]**

`skip` exige item de backlog referenciado no próprio teste. Teste desabilitado e esquecido é uma
área sem proteção que ninguém sabe que existe.

### V15. Não afrouxe o teste para passar **[OBRIGATÓRIA]**

Quando um teste falha, a primeira hipótese é que o código está errado. Ajustar a expectativa para
casar com o novo comportamento **sem confirmar que o novo comportamento é correto** é como um
defeito se torna permanente e documentado.

### V16. Suíte rápida o suficiente para ser usada **[RECOMENDADA]**

Se a verificação relevante não roda em minutos, ela deixa de ser executada durante o
desenvolvimento, e o pipeline se torna o único lugar onde falhas aparecem — tarde e em lote.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Teste que reflete a implementação | Impede refatoração legítima |
| Teste tautológico (afirma o que o código faz) | Trava o bug junto com o comportamento |
| Simulação excessiva | Testa a simulação, não o sistema |
| Espera fixa por tempo | Intermitente e lento |
| Teste dependente de ordem | Falha inexplicável ao paralelizar |
| Fixture global gigante | Ninguém sabe o que o teste realmente pressupõe |
| `retry` em teste intermitente | Esconde defeito real de concorrência |
| Perseguir percentual de cobertura | Manutenção sem proteção |
| Teste que só roda no pipeline | Ciclo de correção longo |
| Snapshot aprovado sem leitura | Aceita a regressão automaticamente |

---

## Verificação em revisão

1. O teste falharia sem a mudança? (peça a evidência)
2. Ele testa comportamento observável?
3. Os casos de borda da tabela acima estão cobertos?
4. O caminho de erro está testado?
5. É determinístico — sem tempo real, rede, ordem ou estado compartilhado?
6. O nome descreve o cenário?
7. Algum teste foi desabilitado, afrouxado ou tem `retry` novo?
