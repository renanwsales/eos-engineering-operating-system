# 07 — Matriz de risco

A matriz de priorização decide o que fazer. A matriz de risco decide **como** fazer: quanta
cerimônia, qual mitigação e quem precisa aprovar.

Risco aqui é o risco de **executar a mudança**, não o risco de não fazer nada (esse é o
Impacto na priorização).

---

## Dimensões

### Probabilidade de a mudança causar problema

| Nível | Indicadores |
| --- | --- |
| **Alta** | Sem cobertura de testes; concorrência; código que ninguém entende bem; toca > 5 módulos |
| **Média** | Cobertura parcial; toca código compartilhado; comportamento parcialmente documentado |
| **Baixa** | Escopo isolado; bem coberto por testes; comportamento óbvio e verificável |

### Impacto caso ocorra

| Nível | Indicadores |
| --- | --- |
| **Crítico** | Perda de dados; falha financeira; brecha de segurança; indisponibilidade total |
| **Alto** | Fluxo principal quebrado para muitos usuários |
| **Médio** | Funcionalidade secundária quebrada, ou degradação perceptível |
| **Baixo** | Falha visível apenas internamente, ou contornável |

---

## A matriz

|  | Impacto Baixo | Impacto Médio | Impacto Alto | Impacto Crítico |
| --- | --- | --- | --- | --- |
| **Prob. Alta** | R2 | R3 | **R4** | **R4** |
| **Prob. Média** | R1 | R2 | R3 | **R4** |
| **Prob. Baixa** | R1 | R1 | R2 | R3 |

---

## Mitigação obrigatória por faixa

### R1 — Rotina

Fluxo normal. Commit único, validação padrão, revisão comum.

### R2 — Controlado

- Teste específico que cobre o comportamento alterado **antes** da mudança.
- Mudança isolada em commit próprio.
- Rollback documentado em uma linha no `CHANGE REPORT`.

### R3 — Elevado

Tudo de R2, mais:

- Teste de regressão escrito **antes** da alteração, provando o comportamento atual correto.
- PR isolado, sem nenhuma outra mudança.
- Plano de rollback testado, não apenas descrito.
- Flag de configuração quando tecnicamente possível.
- Métrica ou log que evidenciaria a falha em produção.
- Revisão humana obrigatória por alguém familiarizado com a área.

### R4 — Crítico

Tudo de R3, mais:

- **[ADR](../templates/adr.md) obrigatório** com alternativas e condição de invalidação.
- **Aprovação humana explícita antes da implementação.** O agente para e pede.
- Backup verificado quando envolve dados (verificado = restauração testada, não "existe rotina
  de backup").
- Migração reversa escrita e executada em ambiente de teste com volume representativo.
- Deploy gradual ou janela acordada, com critério objetivo de abortar.
- Monitoramento definido **antes** do deploy, com alerta acionável e responsável nomeado.
- Nenhuma outra mudança em voo simultaneamente na mesma área.

---

## Classificação automática

Estas mudanças são **R4 por definição**, independentemente de quão simples pareçam:

- Migração destrutiva de schema (`DROP`, `ALTER` com perda de tipo, remoção de coluna).
- Qualquer migração de dados.
- Alteração em autenticação, gestão de sessão ou emissão de token.
- Alteração em regra de autorização.
- Alteração em cálculo financeiro, cobrança, imposto, desconto ou frete.
- Alteração em tratamento de dado pessoal, incluindo log e retenção.
- Rotação de segredo ou credencial em ambiente de produção.
- Mudança incompatível em contrato público consumido por terceiros.

São **R3 por definição**:

- Alteração em código de concorrência, fila, retry ou idempotência.
- Alteração em cache com risco de servir dado de outro usuário.
- Atualização de dependência com mudança de major.
- Alteração em pipeline de CI/CD que afeta o portão de qualidade.
- Remoção de código que "parece" não usado sem prova de que não é.

---

## Riscos que não aparecem no diff

Categorias sistematicamente esquecidas. Verifique todas antes de fechar G2.

| Risco | Pergunta |
| --- | --- |
| **Dados existentes** | A regra nova é violada por registros que já estão no banco? |
| **Clientes antigos** | App móvel em versão anterior continua funcionando? |
| **Compatibilidade de deploy** | Durante o deploy, código novo e antigo coexistem. Ambos funcionam? |
| **Cache envenenado** | Dado em cache no formato antigo será lido pelo código novo? |
| **Fila em trânsito** | Mensagens no formato antigo já enfileiradas serão processadas? |
| **Integração externa** | Terceiro depende do comportamento exato que está mudando? |
| **Fuso e localidade** | Comportamento muda conforme timezone, moeda ou idioma? |
| **Escala** | Funciona com o volume de produção, não só com dados de teste? |
| **Retrocompatibilidade de índice** | A migração bloqueia a tabela durante a criação? |

---

## Aceitação de risco

Risco pode ser aceito em vez de mitigado, sob três condições obrigatórias:

1. **Nomeado:** quem aceita, com nome, não "o time".
2. **Registrado:** ADR ou item de backlog com data.
3. **Monitorado:** existe uma métrica ou alerta que revelaria a materialização.

Risco `R4` **não pode** ser aceito por um agente. Só pelo dono humano do produto, de forma
explícita.

Aceitação sem os três itens não é aceitação de risco — é omissão. E omissão registrada em
lugar nenhum é o que produz incidentes que "ninguém previu".
