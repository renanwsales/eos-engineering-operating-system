# 📙 Volume 10 — DevOps e SRE

Prefixo: `OPS` · Regras: OPS-001 a OPS-048 · Papel: [DevOps/SRE](agents/08-devops-sre.md)

Camada coberta: **8 (entrega)**.

Estado que impede escala horizontal, limites de recurso e descarte de carga estão no
[Volume 14](14-escalabilidade.md).

---

## As duas perguntas do volume

### OPS-001 — Quando isso falhar, quanto tempo até sabermos e até voltarmos? **[IMUTÁVEL]**

Tudo neste volume serve a essas duas perguntas. **Funcionalidade que funciona mas não pode ser observada nem
revertida não é entregável**, independentemente da qualidade do código.

### OPS-002 — Ordem de análise **[OBRIGATÓRIA]**

```
rollback → compatibilidade de deploy → detecção → portões do pipeline
→ configuração e segredos → recuperação → infraestrutura e custo
```

Começar por rollback é deliberado: se a mudança não pode ser desfeita, isso decide a conversa antes de
qualquer outra consideração.

---

## Capítulo 10.1 — Rollback

### OPS-003 — Rollback é um comando documentado **[OBRIGATÓRIA]**
### OPS-004 — Rollback foi executado ao menos uma vez **[OBRIGATÓRIA]**

Rollback que ninguém nunca rodou não é rollback: é uma suposição, e será testada pela primeira vez durante um
incidente.

### OPS-005 — Qualquer pessoa do time consegue reverter **[OBRIGATÓRIA]**

Não apenas o autor da mudança. Autor indisponível é o cenário normal às 3h da manhã.

### OPS-006 — Rollback inclui o caminho de dados **[OBRIGATÓRIA]**

Quando há migração. É aqui que o rollback normalmente quebra.

### OPS-007 — Migração destrutiva nunca no mesmo deploy que mudança de comportamento **[OBRIGATÓRIA]**

Juntas, tornam o rollback impossível. Ver DAT-035.

### OPS-008 — Tempo de rollback é conhecido **[RECOMENDADA]**

Estimativa medida, não presumida. Ela determina o dano máximo de uma falha.

### OPS-009 — Flag onde a faixa de risco exige **[OBRIGATÓRIA]**

`R3`/`R4` com flag permite reverter em segundos, sem deploy — o degrau 1 da escala de reversibilidade
(CON-016).

---

## Capítulo 10.2 — Compatibilidade de deploy

### OPS-010 — Versões antiga e nova coexistem **[OBRIGATÓRIA]**

Durante o rollout, ambas rodam contra o mesmo banco, a mesma fila e o mesmo cache. **A causa mais comum de "o
deploy quebrou produção mas os testes passaram".**

| Risco de coexistência | Pergunta |
| --- | --- |
| Schema | Código antigo funciona contra o schema novo? |
| Fila | Mensagens em trânsito no formato antigo são processadas? |
| Cache | Código novo lê valor cacheado no formato antigo? |
| API | Cliente antigo (app móvel) continua atendido? |
| Configuração | Código antigo tolera a configuração nova, e vice-versa? |

Qualquer "não" força rollout aditivo em duas fases.

### OPS-011 — Aditivo primeiro, remoção depois **[OBRIGATÓRIA]**

Ver DAT-031.

### OPS-012 — Cliente que você não controla nunca é atualizado pelo seu deploy **[OBRIGATÓRIA]**

App instalado no dispositivo do usuário permanece na versão antiga por semanas. A janela de compatibilidade é
declarada no [perfil do projeto](templates/perfil-do-projeto.md).

---

## Capítulo 10.3 — Detecção e observabilidade

### OPS-013 — Log correlacionável **[OBRIGATÓRIA]**

Todo registro carrega identificador que permite reconstruir a requisição inteira, atravessando serviços, filas
e jobs. Sem correlação, o log é uma pilha de frases desconexas e a investigação vira arqueologia.

Contexto mínimo: identificador de requisição, sujeito (usuário/tenant), operação, resultado, duração.

### OPS-014 — Log estruturado em campos **[OBRIGATÓRIA]**

`{"evento":"pedido.pago","pedidoId":"...","valorCents":12900}` é consultável;
`"Pedido 123 pago com sucesso"` não é.

### OPS-015 — Nível com significado **[OBRIGATÓRIA]**

| Nível | Uso | Consequência |
| --- | --- | --- |
| `ERROR` | Falha que exige ação humana | Deve ser raro. Frequente significa que não é erro, ou não está tratado |
| `WARN` | Anomalia tolerada, degradação | Monitorado, não acionado |
| `INFO` | Marco de negócio relevante | Auditável |
| `DEBUG` | Detalhe de investigação | Desligado em produção |

`ERROR` que ninguém age deve virar `WARN` ou desaparecer. Ruído em `ERROR` faz o alerta real ser ignorado.

### OPS-016 — Nenhum dado sensível em log **[OBRIGATÓRIA]** · `S0`

Mascare no ponto de escrita. Ver SEC-050.

### OPS-017 — Erro registrado uma vez, onde há contexto **[OBRIGATÓRIA]**

Registrar em cada nível da pilha multiplica o volume e impossibilita a contagem. E nunca registre **em vez
de** tratar: `catch` que só faz log é falha silenciosa.

### OPS-018 — As quatro métricas mínimas por serviço **[OBRIGATÓRIA]**

Taxa de requisições · taxa de erro · latência (p50/p95/p99) · saturação (CPU, memória, conexões, fila). Sem
essas quatro, nenhuma pergunta operacional pode ser respondida.

### OPS-019 — Métrica de negócio, não só técnica **[OBRIGATÓRIA]**

Pedidos por minuto, pagamentos recusados, cadastros concluídos. Elas detectam o que as métricas técnicas não
veem: **um deploy que zera as vendas retornando HTTP 200 é invisível para métrica técnica.**

### OPS-020 — Rastreamento em fluxo distribuído **[RECOMENDADA]**

Onde a requisição atravessa serviços ou filas. Sem isso, "está lento" não pode ser localizado.

### OPS-021 — Um painel que responde "está tudo bem?" em dez segundos **[RECOMENDADA]**

Se é preciso montar consulta durante um incidente, o painel não existe.

### OPS-022 — Se a mudança pode falhar em silêncio, existe detecção **[OBRIGATÓRIA]**

Métrica ou alerta que a revelaria. Sem isso, a mudança não é entregável (OPS-001).

---

## Capítulo 10.4 — Alertas

### OPS-023 — Alerta é acionável ou não existe **[OBRIGATÓRIA]**

Responde: o que está quebrado, para quem, e qual a primeira ação. Alerta informativo pertence a painel, não a
notificação.

### OPS-024 — Alerte por sintoma, não por causa **[RECOMENDADA]**

"Taxa de erro de checkout acima de 2%" é útil; "CPU em 85%" pode ser normal. Alerte no que o usuário sente;
use métricas de causa para investigar.

### OPS-025 — Todo alerta tem runbook **[OBRIGATÓRIA]**

Como confirmar, como mitigar, como escalar. Escrito **antes** do incidente, porque durante o incidente ninguém
escreve.

### OPS-026 — Ruído é falha de configuração **[OBRIGATÓRIA]**

Falso positivo alto faz o time silenciar o canal — e então o alerta real passa. Alerta que disparou e não
exigiu ação é corrigido ou removido na mesma rodada.

### OPS-027 — Alerta tem responsável nomeado **[OBRIGATÓRIA]**

Alerta sem dono é alerta que ninguém atende.

---

## Capítulo 10.5 — CI/CD

### OPS-028 — O pipeline bloqueia **[OBRIGATÓRIA]**

Testar sem bloquear é teatro. Reprova em: teste falhando · erro de tipo · erro de lint · vulnerabilidade
crítica ou alta · segredo detectado · orçamento de bundle excedido · erro automatizado de acessibilidade.

### OPS-029 — Build reproduzível **[OBRIGATÓRIA]**

Dependências travadas por versão exata; o mesmo commit produz o mesmo artefato. Build que depende do que
estava disponível no dia é impossível de auditar.

### OPS-030 — Um artefato, vários ambientes **[RECOMENDADA]**

O mesmo artefato promovido, com configuração vindo de fora. Recompilar por ambiente introduz diferenças que só
aparecem em produção.

### OPS-031 — Pipeline é código revisado **[OBRIGATÓRIA]**

Quem controla o pipeline controla a produção. Ver SEC-042.

### OPS-032 — Nenhum segredo em log de pipeline **[OBRIGATÓRIA]**
### OPS-033 — Pipeline rápido o suficiente para não ser contornado **[RECOMENDADA]**

Pipeline lento produz a prática de contorná-lo, que anula todos os portões.

### OPS-034 — Varredura de dependências e de segredos automatizada **[OBRIGATÓRIA]**

Ver SEC-038 e SEC-052.

---

## Capítulo 10.6 — Deploy

### OPS-035 — Verificação de saúde real **[OBRIGATÓRIA]**

Valida o que o serviço precisa para funcionar (banco alcançável, configuração carregada), não apenas que o
processo está de pé. **Verificação que sempre retorna sucesso é pior do que ausência** — ela roteia tráfego
para instâncias quebradas.

### OPS-036 — Gradual quando o risco justifica **[RECOMENDADA]**

`R3`/`R4`: liberação gradual ou por flag, com critério objetivo e pré-acordado de abortar.

### OPS-037 — Deploy é rotina e frequente **[RECOMENDADA]**

Deploy raro concentra risco: mais mudanças por vez, mais difícil localizar a causa.

### OPS-038 — Flags têm prazo e item de backlog **[RECOMENDADA]**

Flags eternas multiplicam exponencialmente os caminhos possíveis, e ninguém testa todas as combinações. Ver
ARC-034.

---

## Capítulo 10.7 — Configuração

### OPS-039 — Validada na inicialização **[OBRIGATÓRIA]**

Configuração ausente ou inválida faz o serviço falhar no start com mensagem clara. Descobrir na primeira
requisição do usuário é o pior momento possível.

### OPS-040 — Toda diferença entre ambientes é documentada **[OBRIGATÓRIA]**

Diferença não documentada é a explicação padrão para "funcionava em homologação".

### OPS-041 — Segredos gerenciados e rotacionáveis sem deploy **[OBRIGATÓRIA]**

Ver SEC-052.

---

## Capítulo 10.8 — Recuperação e alta disponibilidade

### OPS-042 — Restauração de backup testada em calendário **[OBRIGATÓRIA]**

Com o **tempo de restauração medido**. Backup nunca testado é uma suposição, e a hora de descobrir que ela era
falsa é sempre a pior. Ver DAT-037.

### OPS-043 — Objetivos de recuperação declarados **[OBRIGATÓRIA]**

Quanto de dado é aceitável perder, e em quanto tempo o serviço precisa voltar. Sem esses dois números, não é
possível projetar backup, réplica nem redundância — nem saber se o que existe é suficiente.

### OPS-044 — Modo degradado definido por dependência **[RECOMENDADA]**

Para cada dependência externa: o que acontece quando ela cai. Definir isso é projeto; descobrir durante o
incidente é sorte.

### OPS-045 — Nenhum ponto único de falha não declarado **[RECOMENDADA]**

Pontos únicos podem ser aceitáveis — desde que conhecidos, registrados e com o dano estimado.

### OPS-046 — Capacidade conhecida sob volume de produção **[RECOMENDADA]**

Não inferida a partir de ambiente de teste.

### OPS-047 — Incidente gera aprendizado registrado **[RECOMENDADA]**

Post-mortem sem culpa: linha de tempo, causa, o que faltou detectar, e a ação que evita a reincidência — com
item de backlog e ID. **Incidente sem ação registrada vai se repetir.**

### OPS-048 — Incidente ativo interrompe a rodada **[OBRIGATÓRIA]**

Alerta disparando em produção precede qualquer revisão. Ver CON-053.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Log sem identificador de correlação | Impossível reconstruir a requisição |
| Log de texto não estruturado | Impossível consultar sob pressão |
| Tudo em `ERROR` | Alerta real ignorado |
| Alerta sem runbook | Quem é acionado não sabe o que fazer |
| Alerta por causa, não por sintoma | Ruído alto, detecção baixa |
| Pipeline que testa mas não bloqueia | Falsa sensação de segurança |
| Rollback nunca testado | Descoberto durante o incidente |
| Migração destrutiva junto com deploy | Rollback impossível |
| Verificação de saúde que sempre passa | Instância quebrada recebe tráfego |
| Flag sem prazo | Explosão de caminhos não testados |
| Configuração divergente não documentada | "Funcionava em homologação" |
| Backup sem teste de restauração | Suposição no lugar de garantia |
| Só métricas técnicas | Falha de negócio silenciosa passa |

---

## Verificação obrigatória de saída

```
## Rollback
Método: <comando> | Testado: <sim/não, quando> | Inclui dados: <sim/não> | Tempo: <medido>

## Compatibilidade de deploy
| Risco | Código antigo vs estado novo | Veredito |

## Detecção
| Modo de falha | O que detecta | Tempo até detectar | Lacuna |

## Portões do pipeline
| Portão | Presente | Bloqueia |

## Divergência de configuração
| Configuração | Homologação | Produção | Documentada |

## Recuperação
Restauração testada: <data> | Duração: <medida> | Objetivos declarados: <sim/não>
Runbooks ausentes: <lista> | Pontos únicos de falha: <lista>
```
