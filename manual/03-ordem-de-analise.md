# 03 — Ordem obrigatória de análise

A ordem existe porque defeitos das camadas superiores **invalidam** conclusões das inferiores.
Otimizar uma consulta dentro de um módulo que será extinto é trabalho perdido. Renomear
variáveis num fluxo de autenticação quebrado é pior: dá aparência de cuidado.

```
1. Arquitetura  →  2. Domínio  →  3. Segurança  →  4. Dados
                                                      │
        8. Entrega  ←  7. Testes  ←  6. UX/A11y  ←  5. Performance
```

**Regra de avanço:** só se passa para a camada seguinte após concluir a anterior. Achados de
camadas posteriores percebidos por acaso são **anotados** e revisitados na vez deles — nunca
investigados fora de ordem.

**Regra de parada:** se a camada 1 ou 2 revelar um defeito `S0`, pare a análise e reporte. Não
faz sentido diagnosticar performance de um sistema cuja modelagem está errada.

---

## Camada 1 — Arquitetura

**Pergunta central:** as fronteiras estão nos lugares certos e as dependências apontam para a
direção certa?

O que procurar:
- Dependências circulares entre módulos.
- Regra de negócio vazando para controllers, views ou componentes de UI.
- Módulo que conhece detalhes internos de outro (acoplamento por implementação).
- Camada de infraestrutura sendo importada pelo domínio.
- "Módulo Deus": arquivo ou pasta que toda mudança precisa tocar.
- Duplicação de responsabilidade: duas partes do sistema decidindo a mesma coisa de formas
  diferentes.
- Abstração sem uso real, ou uma única implementação por trás de uma interface.

Norma: [`standards/arquitetura.md`](../standards/arquitetura.md).

**Não é desta camada:** nome de arquivo, organização de pastas por preferência, escolha de
biblioteca sem consequência estrutural.

---

## Camada 2 — Domínio

**Pergunta central:** o código representa corretamente as regras do negócio, incluindo os
estados que não deveriam existir?

O que procurar:
- Estados inválidos representáveis (ex.: pedido `pago` sem valor, usuário sem tenant).
- Invariantes aplicadas em alguns caminhos e não em outros.
- Regra de negócio duplicada com implementações divergentes — a divergência **é** o defeito.
- Uso de tipos primitivos onde o domínio exige tipo próprio (dinheiro como `float` é `S1`).
- Casos de borda do negócio ignorados: quantidade zero, estoque negativo, cancelamento após
  envio, reembolso parcial, fuso horário, moeda.
- Concorrência de domínio: duas operações simultâneas violando uma invariante.
- Vocabulário inconsistente entre código, banco, API e interface para a mesma entidade.

**Por que vem antes de segurança:** um modelo de domínio errado gera falhas de autorização
que parecem bugs de permissão. Corrigir a permissão sem corrigir o modelo apenas move o
defeito.

---

## Camada 3 — Segurança

**Pergunta central:** quem pode fazer o quê, e o sistema verifica isso em todos os caminhos?

O que procurar, na ordem:
1. **Autorização** — verificação por objeto, não só por rota. É a falha mais comum e mais
   grave (IDOR/BOLA).
2. **Autenticação** — expiração e rotação de sessão, força de senha, MFA, invalidação em
   logout.
3. **Entrada** — validação no servidor (a do cliente não conta), injeção (SQL, comando,
   template, NoSQL), upload de arquivo.
4. **Saída** — XSS, vazamento de dados sensíveis em respostas, mensagens de erro verbosas.
5. **Segredos** — chaves em código, em log, em bundle de frontend, em variável exposta ao
   cliente.
6. **Dependências** — vulnerabilidades conhecidas, pacotes abandonados.
7. **Configuração** — CORS permissivo, headers ausentes, debug ligado, bucket público.

Norma: [`standards/seguranca.md`](../standards/seguranca.md) ·
Checklist: [`checklists/seguranca-owasp.md`](../checklists/seguranca-owasp.md).

**Regra especial:** nesta camada, confiança `MEDIUM` já é bloqueante para caminhos de
autenticação, autorização, pagamento e dados pessoais.

---

## Camada 4 — Dados

**Pergunta central:** o modelo persistido protege a integridade por si mesmo, sem depender da
aplicação se comportar bem?

O que procurar:
- Integridade delegada exclusivamente à aplicação: falta de `NOT NULL`, `UNIQUE`, chave
  estrangeira, `CHECK`.
- Ausência de índice em coluna usada para filtro, junção ou ordenação frequente.
- Índice redundante ou não utilizado (custo de escrita sem retorno).
- Migração irreversível, sem plano de rollback, ou que bloqueia tabela grande.
- Transação com escopo errado: ampla demais (contenção) ou estreita demais (inconsistência).
- N+1 na origem do dado.
- Tipo inadequado: dinheiro em ponto flutuante, data como texto, enum como texto livre.
- Ausência de estratégia de retenção, backup e restauração testada.

Norma: [`standards/banco-de-dados.md`](../standards/banco-de-dados.md).

---

## Camada 5 — Performance

**Pergunta central:** onde está o gargalo real, medido, e ele viola um limiar declarado?

Ordem de investigação — do maior para o menor impacto típico:
1. Acesso a dados: N+1, consulta sem índice, `SELECT *` em tabela larga, ausência de paginação.
2. Chamadas de rede: sequenciais quando podiam ser paralelas, sem timeout, sem cache.
3. Trabalho repetido: recomputação de valor estável, cache ausente ou mal invalidado.
4. Carga útil: resposta com campos não usados, imagem sem otimização, bundle inflado.
5. Renderização: re-render desnecessário, lista longa sem virtualização, trabalho pesado na
   thread de UI.
6. Algoritmo: complexidade inadequada ao volume **real** de dados.

Norma: [`standards/performance.md`](../standards/performance.md) ·
Checklist: [`checklists/performance.md`](../checklists/performance.md).

**Regra absoluta:** nenhum achado de performance sem medição ou sem análise de complexidade
explícita sobre volume real. Suposição vai como `HYPOTHESIS` com o método de verificação.

---

## Camada 6 — UX e Acessibilidade

**Pergunta central:** o usuário entende o que está acontecendo, especialmente quando algo dá
errado?

O que procurar:
- Estados ausentes: carregando, vazio, erro, parcial, offline, sem permissão.
- Erro que não diz o que fazer a seguir, ou que expõe detalhe técnico.
- Ação destrutiva sem confirmação ou sem desfazer.
- Perda de trabalho do usuário: formulário que zera, navegação que descarta rascunho.
- Inconsistência de linguagem, hierarquia visual ou padrão de interação entre telas.
- Acessibilidade: navegação por teclado, foco visível, contraste, rótulos, alternativa
  textual, hierarquia semântica, anúncio de mudanças dinâmicas.
- Feedback ausente após ação: o usuário não sabe se funcionou.

Normas: [`standards/ux-ui.md`](../standards/ux-ui.md) ·
[`standards/acessibilidade.md`](../standards/acessibilidade.md).

---

## Camada 7 — Testes

**Pergunta central:** os testes existentes conseguiriam detectar as falhas que importam?

O que procurar:
- Regra de negócio crítica sem teste — o único critério de cobertura que importa.
- Teste que afirma o comportamento atual sem que se saiba se ele é correto (trava o bug).
- Teste frágil: dependente de tempo, ordem, rede, estado compartilhado.
- Caso de borda ausente: nulo, vazio, limite, duplicata, concorrência, falha de dependência.
- Ausência de teste de regressão para bug já corrigido.
- Teste que testa a implementação (mocks demais) em vez do comportamento.
- Caminho de erro sem cobertura — normalmente o menos testado e o mais executado em produção.

Norma: [`standards/testes.md`](../standards/testes.md).

---

## Camada 8 — Entrega

**Pergunta central:** quando isso falhar em produção, quanto tempo levaremos para saber e
para voltar atrás?

O que procurar:
- Ausência de rollback simples, ou rollback que depende de migração reversa não testada.
- Deploy sem verificação de saúde ou sem estratégia gradual quando o risco justifica.
- Log sem contexto correlacionável (sem id de requisição, sem id de usuário/tenant).
- Ausência de alerta para a falha que mais importa — ou alerta que ninguém consegue acionar.
- Configuração diferente entre ambientes sem que a diferença esteja declarada.
- Segredo gerenciado manualmente.
- Pipeline sem portão de qualidade: testa, mas não bloqueia.

Norma: [`standards/observabilidade.md`](../standards/observabilidade.md).

---

## Registro do percurso

Ao final, declare explicitamente:

```
Camadas analisadas: 1,2,3,4 (completas) | 5 (parcial: só acesso a dados) | 6,7,8 (não analisadas)
Motivo da parada: escopo definido pelo orquestrador / defeito S0 na camada 2 / limite de contexto
```

Camada não analisada é informação valiosa. Silêncio sobre ela é o que produz falsa sensação
de revisão completa.
