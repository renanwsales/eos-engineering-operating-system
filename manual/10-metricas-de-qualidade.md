# 10 — Métricas de qualidade

Toda métrica aqui tem: um limiar, uma reação quando o limiar é violado, e um antipadrão de uso.
Métrica sem reação definida é decoração. Métrica sem antipadrão declarado será gamificada.

Limiares marcados como `[perfil]` devem ser confirmados ou ajustados no
[perfil do projeto](../templates/perfil-do-projeto.md). Os valores abaixo são o padrão até que
alguém decida o contrário — o que é diferente de não ter limiar.

---

## 1. Correção e confiabilidade

| Métrica | Limiar padrão | Reação ao violar |
| --- | --- | --- |
| Defeitos `S0` em aberto | 0 | Para tudo |
| Defeitos `S1` em aberto | 0 no módulo entregue | Bloqueia entrega |
| Taxa de erro de requisições | < 0,5% `[perfil]` | Investigação obrigatória na rodada |
| Falha em fluxo crítico | 0 tolerado | Corrige antes de qualquer novidade |
| Reincidência de defeito | 0 | Teste de regressão ausente é o achado real |

**Antipadrão:** fechar defeito sem teste de regressão. A métrica melhora, o problema volta.

---

## 2. Testes

| Métrica | Limiar padrão | Reação |
| --- | --- | --- |
| Cobertura de regras de negócio | 100% dos casos declarados | Bloqueia entrega |
| Cobertura global de linhas | ≥ 60% `[perfil]`, como indicador | Nunca bloqueia por si só |
| Testes intermitentes (`flaky`) | 0 | Corrigir ou remover em 1 rodada; nunca `retry` como solução |
| Tempo da suíte relevante | < 5 min `[perfil]` | Otimizar; suíte lenta deixa de ser executada |
| Testes desabilitados | 0 | Cada `skip` precisa de item de backlog com ID |

**Antipadrão:** perseguir percentual de cobertura. Cobertura alta em código trivial com regras
de negócio descobertas é pior do que cobertura média bem direcionada, porque produz confiança
falsa. Cobertura é sintoma; casos de negócio cobertos é a meta.

---

## 3. Performance

Medir sempre no percentil 95, sob volume representativo, e registrar o método.

| Métrica | Limiar padrão | Reação |
| --- | --- | --- |
| Resposta de API (p95) | < 300 ms `[perfil]` | Investigar acesso a dados primeiro |
| Consulta de banco (p95) | < 100 ms `[perfil]` | Verificar plano de execução e índice |
| Consultas por requisição | Constante em relação ao tamanho do resultado | N+1 é `S2`, ou `S1` em fluxo principal |
| LCP (web) | < 2,5 s `[perfil]` | Analisar carga útil e caminho crítico |
| INP (web) | < 200 ms `[perfil]` | Analisar trabalho na thread principal |
| CLS (web) | < 0,1 | Reservar espaço para conteúdo assíncrono |
| Tamanho do bundle inicial | < 250 KB comprimido `[perfil]` | Dividir código; revisar dependências |
| Regressão entre versões | > 20% em qualquer métrica acima | Bloqueia entrega |

**Antipadrão:** medir em ambiente local com dados de teste e reportar como se fosse produção.
Toda medição declara: ambiente, volume de dados, número de execuções, método.

---

## 4. Segurança

| Métrica | Limiar | Reação |
| --- | --- | --- |
| Vulnerabilidades críticas ou altas em dependências | 0 | Bloqueia entrega |
| Segredos no repositório | 0 | `S0`: rotacionar a credencial, depois remover do histórico |
| Endpoints sem verificação de autorização | 0 | `S0` ou `S1` conforme exposição |
| Entradas sem validação no servidor | 0 | `S1` |
| Dado pessoal em log | 0 | `S0` |
| Idade da última varredura de dependências | < 30 dias | Automatizar no pipeline |

**Antipadrão:** suprimir aviso de vulnerabilidade sem avaliar a explorabilidade **e** sem
registrar a análise. Se não é explorável, isso é uma conclusão que precisa estar escrita.

---

## 5. Manutenibilidade

Estas métricas são **indicadores para investigar**, nunca metas. Nenhuma delas justifica uma
mudança por si só — isso violaria o veto cosmético.

| Métrica | Indicador de atenção | Reação |
| --- | --- | --- |
| Arquivos alterados por mudança típica | > 5 | Investigar fronteiras de módulo |
| Dependências circulares | > 0 | `S2` estrutural |
| Duplicação da mesma regra de negócio | > 1 implementação | `S2` — a divergência é o risco |
| Profundidade de aninhamento | > 4 níveis | Investigar, se coincidir com defeitos |
| Tamanho de função | > 60 linhas | Investigar, se coincidir com defeitos |
| Arquivos tocados por > 60% das mudanças | 0 | Sinal de "módulo Deus" |

**Antipadrão:** transformar limites de tamanho em regra e fatiar funções para cumprir número.
O resultado é o mesmo código, mais espalhado, com mais indireção e mais difícil de seguir.

---

## 6. Acessibilidade

| Métrica | Limiar | Reação |
| --- | --- | --- |
| Erros automatizados de a11y (axe ou equivalente) | 0 | Bloqueia entrega |
| Tarefas críticas completáveis por teclado | 100% | `S2` por tarefa bloqueada |
| Contraste WCAG AA | 100% do texto | `S2` |
| Elementos interativos com nome acessível | 100% | `S2` |

**Antipadrão:** aprovar só com verificação automática. Ferramentas detectam cerca de um terço
dos problemas reais; a verificação por teclado é manual e obrigatória.

---

## 7. Operação

| Métrica | Limiar padrão | Reação |
| --- | --- | --- |
| Tempo até detectar falha (MTTD) | < 5 min para fluxo crítico `[perfil]` | Adicionar alerta |
| Tempo até restaurar (MTTR) | < 30 min `[perfil]` | Melhorar rollback |
| Rollback testado | Sim, na rodada atual | Testar antes do próximo deploy de risco |
| Restauração de backup testada | < 90 dias | Agendar teste |
| Alertas sem runbook | 0 | Escrever ou remover o alerta |
| Taxa de falso positivo em alertas | < 10% | Ajustar; alerta ruidoso é alerta ignorado |

---

## Notas da auditoria

O [auditor final](../agents/09-final-auditor.md) atribui de 0 a 10 por dimensão, com estes
pesos:

| Dimensão | Peso |
| --- | --- |
| Segurança | 20% |
| Correção de domínio | 20% |
| Dados e integridade | 15% |
| Testes | 15% |
| Arquitetura | 10% |
| Performance | 8% |
| UX e acessibilidade | 7% |
| Observabilidade e entrega | 5% |

Escala:

| Nota | Significado |
| --- | --- |
| 10 | Atende a [Definition of Excellence](09-definition-of-excellence.md) na dimensão |
| 8–9 | Atende a DoD com folga; lacunas de DoE conhecidas e registradas |
| 6–7 | Atende a DoD; existem `S2` conhecidos no backlog |
| 4–5 | Atende parcialmente; existem `S2` não registrados |
| 1–3 | Existe `S1` |
| 0 | Existe `S0` |

**Travas obrigatórias:**
- Qualquer `S0` → total limitado a 4 e veredito `REJECTED`.
- Qualquer `S1` não corrigido → total limitado a 4 e veredito `REJECTED`.
- Nota de segurança < 6 → no máximo `APPROVED WITH CONDITIONS`.

---

## Regra geral sobre métricas

> Toda métrica vira meta, e toda meta vira jogo.

Por isso: as métricas de correção, segurança e acessibilidade **bloqueiam**. As de
manutenibilidade apenas **apontam onde olhar**. Nenhuma mudança de código pode ser justificada
exclusivamente por mover um número de manutenibilidade.
