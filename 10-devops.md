# 📙 Volume 10 — DevOps e SRE

Prefixo: `OPS` · Regras: OPS-001 a OPS-049 · Papel: [DevOps/SRE](agents/08-devops-sre.md)

Camada coberta: **8 (entrega)**.

Estado que impede escala horizontal, limites de recurso e descarte de carga estão no
[Volume 14](14-escalabilidade.md).

**Fronteira.** É deste volume: empacotamento e ambientes; CI/CD que bloqueia; compatibilidade durante
rollout; rollback documentado e testado; feature flags com prazo; configuração e segredos em runtime;
backups com restauração medida; alta disponibilidade e modo degradado; resposta a incidente e plantão;
o núcleo de detecção — log correlacionável e estruturado, as quatro métricas mínimas, alerta acionável
com runbook e dono (`OPS-013`–`OPS-027`).

**Não é deste volume:** log, tracing, métricas, SLO e custo de telemetria em profundidade
(→ [17](17-observabilidade.md) — opera sobre a fundação deste volume e a cita, não a reafirma).
Capacidade, contrapressão e estado que impede escala horizontal (→ [14](14-escalabilidade.md)).
Classificação de dado sensível em log e gestão de segredos como norma de segurança
(→ [06](06-seguranca.md); este volume exige o controle operacional e cita `SEC`).

---

## Fundamentos

Entrega sem caminho de volta e sem caminho de detecção não é entrega: é aposta. As duas perguntas de
`OPS-001` — quanto tempo até sabermos, quanto tempo até voltarmos — são o filtro de tudo que segue.
Rollback sem comando, sem teste e sem dono vira descoberta às 3h. Pipeline que só reporta é teatro.
Log sem correlação é pilha de frases. Alerta sem runbook é interrupção sem ação.

A ordem de `OPS-002` é deliberada: rollback primeiro. Se a mudança não pode ser desfeita, o resto da
conversa é decoração. Compatibilidade de deploy vem em seguida porque versões antiga e nova
coexistem contra o mesmo banco e a mesma fila (`OPS-010`) — a causa clássica de "testes passaram,
produção quebrou". Detecção e alerta vêm antes de pipeline porque um portão verde sem sintoma
visível deixa o defeito no ar até o cliente reclamar.

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

Dependências travadas por versão exata (lockfile versionado); o mesmo commit produz o mesmo
artefato. Build que depende do que estava disponível no dia é impossível de auditar. Instalação no
CI e no setup documentado segue `SEC-067` (frozen), não resolve à solta.

### OPS-030 — Um artefato, vários ambientes **[RECOMENDADA]**

O mesmo artefato promovido, com configuração vindo de fora. Recompilar por ambiente introduz diferenças que só
aparecem em produção.

### OPS-031 — Pipeline é código revisado **[OBRIGATÓRIA]**

Quem controla o pipeline controla a produção. Ver SEC-042.

### OPS-032 — Nenhum segredo em log de pipeline **[OBRIGATÓRIA]**
### OPS-033 — Pipeline rápido o suficiente para não ser contornado **[RECOMENDADA]**

Pipeline lento produz a prática de contorná-lo, que anula todos os portões.

### OPS-034 — Varredura de dependências e de segredos automatizada **[OBRIGATÓRIA]**

Ver SEC-038 e SEC-052. Varredura de CVE **não** substitui `SEC-043`/`SEC-069`: pacote inventado
ou typosquat pode não ter advisory.

### OPS-049 — Install do CI desliga lifecycle de deps e rebuilda só o toolchain **[OBRIGATÓRIA]**

Jobs que instalam dependências usam install frozen (`SEC-067`) com scripts de lifecycle
desligados (`SEC-068`). Se o build precisa de binário nativo (bundler, compilador SWC, etc.),
o rebuild é um passo explícito com allowlist versionada no repositório — nunca
`ignore-scripts=false` global "para o CI passar". Diff de workflow ou `.npmrc` que reabre
scripts sem allowlist é revisão de segurança, não nit de DevOps.

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

## Padrões reutilizáveis

**Rollback em um comando.** Script versionado, documentado no runbook do serviço, executado ao menos
uma vez em ambiente real (`OPS-003`–`OPS-005`). *Use sempre* em `R2`+. *Não trate* "reverter o PR"
como rollback se a migração já rodou — o caminho de dados precisa estar no mesmo comando (`OPS-006`).

**Rollout aditivo em duas fases.** Schema/config novos primeiro, compatíveis com código antigo; remoção
só depois que a versão antiga saiu do ar (`OPS-011`, `DAT-031`). *Use quando* qualquer linha da tabela
de coexistência de `OPS-010` for "não".

**Flag com prazo e backlog.** Flag ligada ao risco da mudança, item de backlog com data de remoção
(`OPS-009`, `OPS-038`). *Use* em `R3`/`R4`. *Não use* como substituto permanente de versionamento de
contrato.

**Artefato único promovido.** Um build, vários ambientes; configuração injetada de fora (`OPS-030`).
*Use* quando a divergência "funcionava em homologação" for recorrente.

**Health check que prova dependência.** Endpoint que falha se banco, fila ou config crítica estiver
indisponível (`OPS-035`). *Não use* `return 200` estático — pior que ausência.

**Alerta-sintoma com runbook e dono.** Dispara por sintoma do usuário ou do SLO local; runbook com
passos; responsável nomeado (`OPS-023`–`OPS-027`). *Não alerte* CPU ou reinício isolado sem ação.

---

## Matrizes de decisão

**Como reverter**

| Situação | Caminho | Motivo |
| --- | --- | --- |
| Código sem migração | Redeploy da versão anterior | `OPS-003` |
| Migração aditiva compatível | Redeploy; schema novo permanece | `OPS-006`, `OPS-011` |
| Migração destrutiva já aplicada | Sem rollback limpo — evitar o cenário | `OPS-007` |
| `R3`/`R4` com flag | Desligar flag sem deploy | `OPS-009` |
| Cliente móvel antigo no ar | Compatibilidade, não "force update" | `OPS-012` |

**O que o pipeline deve bloquear**

| Portão | Bloqueia merge/deploy? | Norma |
| --- | --- | --- |
| Testes, types, lint | Sim | `OPS-028` |
| Segredo detectado / CVE crítico | Sim | `OPS-034`, `SEC-038` |
| Orçamento de bundle estourado | Sim, se declarado no perfil | `OPS-028` |
| Aviso de estilo sem norma | Não | `CON-013` |
| Job amarelo "só informativo" | Não conta como portão | teatro |

**Detecção mínima vs Volume 17**

| Necessidade | Onde vive | Quando basta o Vol 10 |
| --- | --- | --- |
| Correlação, log em campos, 4 métricas, alerta com runbook | `OPS-013`–`OPS-027` | Sempre — fundação |
| Schema de log, SLO, cardinalidade, tracing | [17](17-observabilidade.md) | Quando o fluxo é crítico ou distribuído |
| Capacidade e contrapressão | [14](14-escalabilidade.md) | Quando o risco é saturação, não deploy |

---

## Fluxo de trabalho

```
1. Rollback              → comando, teste prévio, caminho de dados, flag se R3/R4 (OPS-003–009)
2. Compatibilidade       → schema, fila, cache, API, config com versão antiga no ar (OPS-010–012)
3. Detecção              → falha silenciosa tem sinal; correlação; métrica de negócio (OPS-013–022)
4. Alertas               → sintoma, runbook, dono; ruído é defeito (OPS-023–027)
5. Portões do pipeline   → bloqueia de verdade; artefato reproduzível; install frozen (OPS-028–034, OPS-049)
6. Deploy                → health real; gradual se o risco pede (OPS-035–038)
7. Configuração/segredos → valida no start; divergência documentada; rotação sem deploy (OPS-039–041)
8. Recuperação           → restauração medida; RPO/RTO; modo degradado; SPOF declarado (OPS-042–046)
9. Incidente             → se ativo, interrompe a rodada (OPS-048); depois, aprendizado com backlog (OPS-047)
```

Papel: [`agents/08-devops-sre.md`](agents/08-devops-sre.md). Aprofundamento de telemetria, se necessário,
em [17](17-observabilidade.md) — citando `OPS`, sem reescrevê-lo.

---

## Exemplos de implementação

**Rollback com migração (`OPS-006`, `OPS-007`)**

```
# Ruim — migração destrutiva no mesmo deploy que o comportamento novo
deploy: migrate drop column orders.legacy_status && app v42
# Rollback de app deixa o schema sem a coluna que v41 ainda lê.

# Bom — aditivo primeiro; remoção depois que v41 saiu
deploy 1: add column ... (nullable) ; app ainda lê a coluna antiga
deploy 2: app v42 escreve nas duas / lê a nova
deploy 3: remove coluna antiga + código morto
rollback de deploy 2 = redeploy v41; schema ainda serve as duas
```

**Health check (`OPS-035`)**

```js
// Ruim — sempre verde
app.get('/health', (_req, res) => res.status(200).send('ok'))

// Bom — prova o que o serviço precisa
app.get('/health', async (_req, res) => {
  await db.query('select 1')
  await fila.ping()
  res.status(200).json({ ok: true, versao: processo.versao })
})
```

**Alerta acionável (`OPS-023`, `OPS-025`)**

```
# Ruim
Alerta: CPU > 80% por 1m. Runbook: (vazio). Dono: (ninguém).

# Bom
Alerta: taxa de checkout_confirmado < 50% da baseline 7d por 5m
Consequência de ignorar: pedidos pagos sem confirmação visível ao cliente
Ação: runbooks/checkout-drop.md · Dono: plantão-pagamentos
```

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
| Install aberto / lifecycle ligado no CI | Pacote inventado ou postinstall malicioso (`OPS-049`, `SEC-067`) |
| Rollback nunca testado | Descoberto durante o incidente |
| Migração destrutiva junto com deploy | Rollback impossível |
| Verificação de saúde que sempre passa | Instância quebrada recebe tráfego |
| Flag sem prazo | Explosão de caminhos não testados |
| Configuração divergente não documentada | "Funcionava em homologação" |
| Backup sem teste de restauração | Suposição no lugar de garantia |
| Só métricas técnicas | Falha de negócio silenciosa passa |

---

## Checklist

- [ ] Rollback é um comando documentado, já executado, com caminho de dados se houver migração.
      (`OPS-003`–`OPS-006`)
- [ ] Migração destrutiva não está no mesmo deploy que mudança de comportamento. (`OPS-007`)
- [ ] `R3`/`R4` tem flag ou caminho de reversão em segundos. (`OPS-009`)
- [ ] Versões antiga e nova coexistiram verificadas (schema, fila, cache, API, config). (`OPS-010`)
- [ ] Log correlacionável, estruturado; sem dado sensível. (`OPS-013`, `OPS-014`, `OPS-016`)
- [ ] Quatro métricas mínimas + métrica de negócio que pega falha silenciosa. (`OPS-018`, `OPS-019`)
- [ ] Todo alerta tem sintoma, runbook e dono; ruído tratado como defeito. (`OPS-023`–`OPS-027`)
- [ ] Pipeline bloqueia em teste, type, lint, segredo e CVE crítico. (`OPS-028`, `OPS-034`)
- [ ] Install do CI é frozen + lifecycle off + rebuild allowlist. (`OPS-049`, `SEC-067`, `SEC-068`)
- [ ] Health check prova dependência real. (`OPS-035`)
- [ ] Config válida no start; divergência entre ambientes documentada. (`OPS-039`, `OPS-040`)
- [ ] Segredos rotacionáveis sem deploy. (`OPS-041`)
- [ ] Restauração de backup testada com duração medida; RPO/RTO declarados. (`OPS-042`, `OPS-043`)
- [ ] Incidente ativo interrompe a rodada. (`OPS-048`)

---

## Prompt do volume

```
You are the DevOps/SRE agent of the EOS, operating Volume 10 — DevOps (`OPS`).

Mission: for every change in scope, answer OPS-001 — how long until we know it failed, and how long
until we are back — with evidence, not narrative.

Load first: agents/_shared/core-contract.md, 00-constituicao-da-engenharia.md, 10-devops.md,
agents/08-devops-sre.md, and the filled templates/perfil-do-projeto.md. Cite Volume 17 for deep
telemetry design; do not restate OBS rules. Cite Volume 14 for capacity and backpressure; do not
restate ESC rules.

Mandatory sequence (OPS-002). Do not reorder.
1. Rollback: documented command, previously executed, data path if migration, flag if R3/R4.
2. Deploy compatibility: old and new vs same DB, queue, cache, API, config (OPS-010).
3. Detection: silent-failure modes, correlation, structured logs, four baseline metrics, business
   metric, actionable alerts with runbook and owner.
4. Pipeline gates: does CI block, or only report? Reproducible artifact; no secrets in logs.
5. Configuration and secrets: startup validation; documented env drift; rotatable without deploy.
6. Recovery: restore tested with measured duration; RPO/RTO; degraded mode; declared SPOFs.
7. If an active production incident exists, stop the round (OPS-048).

Rules of engagement.
- Evidence or nothing (CON-009). "Rollback exists" requires the command and the last execution date.
- Personal data in logs is S0 — hand to Security (OPS-016); do not invent SEC rules.
- Never claim "observability is fine" because Volume 17 exists; verify the OPS foundation first.

Output: exactly the "Verificação obrigatória de saída" block of Volume 10, in Brazilian Portuguese,
with MUST-FIX and OPPORTUNITY separated (CON-018), and unfixed opportunities in the backlog with
promotion triggers (AUD-036).
```

---

## Critérios de aceite

Um módulo ou mudança passa em DevOps quando todos são verdadeiros:

1. Rollback documentado, executado ao menos uma vez, com caminho de dados quando há migração
   (`OPS-003`–`OPS-006`).
2. Nenhuma migração destrutiva no mesmo deploy que mudança de comportamento (`OPS-007`).
3. Coexistência old/new verificada nos eixos de `OPS-010`, ou rollout aditivo em fases.
4. Falha silenciosa do escopo tem detecção; logs correlacionáveis; quatro métricas + métrica de
   negócio (`OPS-013`–`OPS-022`).
5. Todo alerta do escopo tem runbook e dono (`OPS-025`, `OPS-027`).
6. Pipeline bloqueia nos portões obrigatórios (`OPS-028`, `OPS-034`); install segue `OPS-049`.
7. Health check real (`OPS-035`); config válida no start (`OPS-039`).
8. Restauração testada com duração medida e objetivos de recuperação declarados (`OPS-042`,
   `OPS-043`) — ou N/A justificado no perfil para serviço sem estado persistente próprio.

Falha em 1, 4 ou 6 é reprovação direta: sem volta, sem detecção ou com teatro de CI, a entrega não
é operável.

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
