# Norma — Banco de dados

Princípio central: **o banco é a última linha de defesa da integridade**. A aplicação tem bugs, é
reescrita, ganha novos pontos de escrita, scripts pontuais e importações manuais. O que o banco
garante, está garantido para sempre.

---

## Modelagem

### D1. Integridade declarada no schema **[OBRIGATÓRIA]**

Toda invariante que o banco pode garantir, ele garante:

- `NOT NULL` em tudo que é obrigatório. Coluna anulável é uma pergunta: "o que significa nulo
  aqui?" — se não há resposta de negócio, é erro de modelagem.
- `UNIQUE` no que é único, incluindo unicidade composta.
- Chave estrangeira com comportamento explícito de `ON DELETE`.
- `CHECK` para faixas e combinações válidas (`quantidade > 0`, `total >= 0`).
- Valor padrão que seja válido no domínio, nunca um valor "neutro" que crie estado inválido.

Depender apenas da aplicação é `S2`, e `S1` em dado crítico (financeiro, pessoal, de acesso).

### D2. Tipos corretos **[OBRIGATÓRIA]**

| Dado | Correto | Errado |
| --- | --- | --- |
| Dinheiro | Inteiro na menor unidade, ou decimal exato | Ponto flutuante — `S1` |
| Data/hora | Tipo temporal com fuso explícito (UTC) | Texto, ou fuso implícito |
| Enumeração | Enum nativo, ou texto com `CHECK` | Texto livre |
| Identificador | Tipo dedicado (UUID, inteiro) | Texto genérico |
| Booleano | Booleano | `0/1` em texto, `S/N` |
| JSON | Tipo JSON, para dado realmente sem forma | JSON para fugir de modelagem |

JSON não é atalho para não modelar. Dado que se consulta, filtra ou valida merece coluna.

### D3. Estado inválido não representável **[RECOMENDADA]**

Se um pedido `pago` exige `pagoAt` e `total`, o schema deve impedir a combinação impossível — com
`CHECK` condicional, ou separando em tabela dedicada. Isso é o que distingue integridade real de
esperança.

### D4. Sem exclusão física de histórico **[RECOMENDADA]**

Registro com valor histórico ou financeiro é marcado como inativo, não removido. Exclusão real
apenas para atender a direito de eliminação de dado pessoal — e nesse caso deliberadamente,
documentada, com todos os locais mapeados.

### D5. Auditoria do que importa **[RECOMENDADA]**

Operação sensível (mudança de permissão, valor financeiro, dado pessoal) registra quem, quando, o
que mudou, de qual valor para qual. Sem isso, uma investigação de fraude ou de incidente é
impossível.

---

## Consultas

### D6. Toda consulta frequente usa índice **[OBRIGATÓRIA]**

Coluna usada em filtro, junção ou ordenação frequente precisa de índice. Verifique o **plano de
execução** — não presuma. Índice composto respeita a ordem de seletividade e serve às consultas
reais, não a consultas hipotéticas.

Índice não usado também é problema: custa em cada escrita e em cada backup, sem retorno.

### D7. Zero N+1 **[OBRIGATÓRIA]**

Número de consultas não pode crescer com o tamanho do resultado. É o defeito de performance mais
comum e o mais fácil de encontrar: conte as consultas de uma requisição que retorna 1 item e de
outra que retorna 50.

`S2`, ou `S1` em fluxo principal.

### D8. Selecione o que precisa **[RECOMENDADA]**

`SELECT *` em tabela larga transfere colunas não usadas, impede índice de cobertura e faz a
consulta mudar de comportamento quando alguém adiciona uma coluna.

### D9. Limite obrigatório **[OBRIGATÓRIA]**

Nenhuma consulta sem limite em caminho de requisição. O que funciona com mil registros derruba o
serviço com um milhão — e o crescimento é garantido.

### D10. Trabalho em lote, em lotes **[RECOMENDADA]**

Processamento de volume percorre em blocos, com limite de tempo por bloco e possibilidade de
retomar. Uma transação gigante bloqueia, estoura memória e, ao falhar, não deixa progresso.

---

## Transações

### D11. Escopo pela invariante **[OBRIGATÓRIA]**

A transação envolve exatamente o conjunto de escritas que precisa ser atômico. Ampla demais gera
contenção; estreita demais gera inconsistência.

### D12. Nada externo dentro da transação **[OBRIGATÓRIA]**

Nunca faça chamada HTTP, envio de e-mail ou publicação em fila dentro de uma transação: a
transação fica aberta pela duração da rede, e o efeito externo não pode ser desfeito pelo
rollback.

Padrão correto: persista a intenção na mesma transação, execute o efeito externo depois.

### D13. Concorrência tratada explicitamente **[OBRIGATÓRIA]**

Onde duas operações simultâneas podem violar uma invariante (estoque, saldo, reserva, cupom de uso
único), a proteção é declarada: bloqueio, controle de versão, ou constraint que faça a segunda
falhar.

O padrão "leia, verifique, escreva" sem proteção é `S1` em qualquer recurso escasso. Não é uma
falha teórica: é o que produz estoque negativo e cupom usado duas vezes.

---

## Migrações

### D14. Versionadas, reversíveis, testadas **[OBRIGATÓRIA]**

Migração vive no repositório, é aplicada em ordem, e tem reversa **escrita e executada** em
ambiente de teste. "É só um ALTER" é a frase que antecede a indisponibilidade.

### D15. Duas fases para mudança incompatível **[OBRIGATÓRIA]**

```
Fase 1: adicionar o novo (coluna/tabela) — aditivo, compatível
Fase 2: aplicação passa a escrever nos dois
Fase 3: migrar o dado existente, em lotes
Fase 4: aplicação passa a ler do novo
Fase 5: remover o antigo — só depois de confirmar que nada mais o usa
```

Cada fase é um deploy separado. Renomear coluna em um passo derruba a aplicação durante o deploy,
porque as duas versões coexistem.

### D16. Verifique o dado existente **[OBRIGATÓRIA]**

Antes de adicionar `NOT NULL`, `UNIQUE` ou `CHECK`: conte quantos registros atuais violam a regra.
A migração vai falhar em produção — ou pior, será aplicada com um valor padrão que corrompe o
significado do dado.

### D17. Não bloqueie tabela grande **[OBRIGATÓRIA]**

Criação de índice e alteração de tipo em tabela grande pode bloquear escritas. Use as opções
concorrentes do banco, ou uma janela acordada. Verifique o comportamento na versão específica em
uso — isso varia.

### D18. Migração de dados é `R4` **[OBRIGATÓRIA]**

Backup verificado (restauração testada), execução em lotes, possibilidade de retomar, contagem
antes e depois, e aprovação humana. Ver [matriz de risco](../manual/07-matriz-de-risco.md).

---

## Operação

### D19. Backup com restauração testada **[OBRIGATÓRIA]**

Backup nunca testado não é backup: é uma suposição. Teste de restauração em calendário, com o
tempo de restauração medido e conhecido.

### D20. Sem credencial de administrador na aplicação **[OBRIGATÓRIA]**

A aplicação usa credencial com o mínimo necessário. Migração usa outra credencial. Isso limita o
dano de uma injeção bem-sucedida.

### D21. Retenção definida **[RECOMENDADA]**

Cada tabela com dado pessoal ou volumoso tem política de retenção declarada. Sem isso, o banco
cresce indefinidamente e a exposição em caso de vazamento cresce com ele.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Integridade só na aplicação | Primeira importação manual corrompe |
| Dinheiro em `float` | Divergência de centavos, impossível de reconciliar |
| Coluna anulável sem significado | Cada leitura precisa tratar um caso que ninguém definiu |
| `updated_at` mantido pela aplicação | Sempre haverá um caminho que esquece |
| Índice em tudo | Escrita lenta, sem ganho de leitura |
| Migração sem reversa | Rollback impossível durante incidente |
| Consulta em laço | N+1 garantido |
| `EAV` genérico | Perde tipo, integridade e desempenho de uma vez |
