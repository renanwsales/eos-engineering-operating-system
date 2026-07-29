# Norma — Observabilidade e entrega

O critério que governa esta norma: **quando isso falhar em produção, quanto tempo até sabermos, e
quanto tempo até voltarmos ao normal?** Tudo aqui serve a essas duas perguntas.

---

## Log

### O1. Correlacionável **[OBRIGATÓRIA]**

Todo registro carrega um identificador que permite reconstruir a requisição inteira, atravessando
serviços, filas e jobs. Sem correlação, o log é uma pilha de frases desconexas e a investigação
vira arqueologia.

Contexto mínimo: identificador de requisição, sujeito (usuário/tenant), operação, resultado,
duração.

### O2. Estruturado **[OBRIGATÓRIA]**

Campos, não frases interpoladas. `{"evento":"pedido.pago","pedidoId":"...","valorCents":12900}` é
consultável; `"Pedido 123 pago com sucesso"` não é.

### O3. Nível com significado **[OBRIGATÓRIA]**

| Nível | Uso | Consequência |
| --- | --- | --- |
| `ERROR` | Falha que exige ação humana | Deve ser raro; se é frequente, não é erro ou não está tratado |
| `WARN` | Anomalia tolerada, degradação | Monitorado, não acionado |
| `INFO` | Marco de negócio relevante | Auditável |
| `DEBUG` | Detalhe de investigação | Desligado em produção por padrão |

`ERROR` que ninguém age deve virar `WARN` ou desaparecer. Ruído em `ERROR` faz o alerta real ser
ignorado.

### O4. Nunca registre dado sensível **[OBRIGATÓRIA]**

Senha, token, chave, cartão e dado pessoal completo. Mascare **no ponto de escrita**, não no
visualizador — o log já foi copiado para outros sistemas antes de alguém olhar.

Dado pessoal em log é `S0`.

### O5. Erro registrado uma vez, com contexto **[OBRIGATÓRIA]**

Registre onde há contexto para agir, não em cada nível da pilha. O mesmo erro em cinco linhas
diferentes multiplica o volume e dificulta a contagem.

E nunca registre em vez de tratar: `catch` que só faz log é falha silenciosa.

---

## Métricas

### O6. As quatro métricas mínimas por serviço **[OBRIGATÓRIA]**

Taxa de requisições, taxa de erro, latência (p50/p95/p99) e saturação (CPU, memória, conexões,
fila). Sem essas quatro, nenhuma pergunta operacional pode ser respondida.

### O7. Métricas de negócio, não só técnicas **[RECOMENDADA]**

Pedidos por minuto, pagamentos recusados, cadastros concluídos. Elas detectam falhas que as métricas
técnicas não veem: um deploy que zera as vendas com 100% de sucesso HTTP.

### O8. Um painel que responde "está tudo bem?" **[RECOMENDADA]**

Em dez segundos, sem interpretação. Se é preciso montar consulta durante um incidente, o painel não
existe.

---

## Rastreamento

### O9. Rastreamento em fluxo distribuído **[RECOMENDADA]**

Onde uma requisição atravessa serviços ou filas, propague o contexto de rastreamento. Sem isso,
"está lento" não pode ser localizado.

---

## Alertas

### O10. Alerta é acionável ou não existe **[OBRIGATÓRIA]**

Todo alerta responde: o que está quebrado, para quem, e qual a primeira ação. Alerta informativo
pertence a painel, não a notificação.

### O11. Alerte por sintoma, não por causa **[RECOMENDADA]**

"Taxa de erro de checkout acima de 2%" é útil. "CPU em 85%" pode ser normal. Alerte no que o usuário
sente; use as métricas de causa para investigar.

### O12. Todo alerta tem runbook **[OBRIGATÓRIA]**

Um documento curto: como confirmar, como mitigar, como escalar. Escrito antes do incidente, porque
durante o incidente ninguém escreve.

### O13. Ruído é falha de configuração **[OBRIGATÓRIA]**

Taxa de falso positivo alta faz o time silenciar o canal — e então o alerta real passa. Alerta que
disparou e não exigiu ação precisa ser corrigido ou removido na mesma rodada.

---

## CI/CD

### O14. O pipeline bloqueia **[OBRIGATÓRIA]**

Testar sem bloquear é teatro. O pipeline reprova em: teste falhando, erro de tipo, erro de lint,
vulnerabilidade crítica ou alta, segredo detectado, orçamento de bundle excedido.

### O15. Build reproduzível **[OBRIGATÓRIA]**

Dependências travadas por versão exata. O mesmo commit produz o mesmo artefato. Build que depende do
que estava disponível no dia é impossível de auditar.

### O16. Um artefato, vários ambientes **[RECOMENDADA]**

O mesmo artefato promovido entre ambientes, com a configuração vindo de fora. Recompilar por
ambiente introduz diferenças que só aparecem em produção.

### O17. Pipeline é código revisado **[OBRIGATÓRIA]**

Quem controla o pipeline controla o que vai a produção. Mudança nele tem a mesma revisão do código —
ou mais.

---

## Deploy

### O18. Rollback em um comando, testado **[OBRIGATÓRIA]**

Documentado, testado, e conhecido por qualquer pessoa do time. Rollback que ninguém nunca executou
não é rollback.

Se a mudança envolve migração, o rollback inclui o caminho de dados — e é por isso que migração
destrutiva e deploy nunca vão juntos.

### O19. Compatibilidade durante o deploy **[OBRIGATÓRIA]**

Versões antiga e nova coexistem durante o deploy. Ambas precisam funcionar com o mesmo banco, a
mesma fila e o mesmo cache. Isso força mudanças aditivas primeiro.

### O20. Verificação de saúde real **[OBRIGATÓRIA]**

A verificação valida o que o serviço precisa para funcionar (banco alcançável, configuração
carregada), não apenas que o processo está de pé. Verificação que sempre retorna sucesso é pior do
que ausência.

### O21. Gradual quando o risco justifica **[RECOMENDADA]**

Para risco `R3`/`R4`: liberação gradual ou por flag, com critério objetivo e pré-acordado de abortar.

### O22. Flags têm prazo **[RECOMENDADA]**

Toda flag temporária tem data e item de backlog para remoção. Flags eternas multiplicam os caminhos
possíveis do código exponencialmente, e ninguém testa todas as combinações.

---

## Configuração e segredos

### O23. Validada na inicialização **[OBRIGATÓRIA]**

Configuração ausente ou inválida faz o serviço falhar no start com mensagem clara. Descobrir na
primeira requisição do usuário é o pior momento possível.

### O24. Diferença entre ambientes é declarada **[OBRIGATÓRIA]**

Toda diferença entre homologação e produção é documentada. Diferença não documentada é a explicação
mais comum para "funcionava em homologação".

### O25. Segredos gerenciados e rotacionáveis **[OBRIGATÓRIA]**

Fora do repositório, injetados em execução, rotacionáveis sem deploy. Ver
[segurança](seguranca.md#segredos).

---

## Recuperação

### O26. Backup com restauração testada em calendário **[OBRIGATÓRIA]**

Com tempo de restauração medido. Backup não testado é uma suposição, e a hora de descobrir que a
suposição era falsa é sempre a pior.

### O27. Modo degradado definido **[RECOMENDADA]**

Para cada dependência externa: o que acontece quando ela cai? Definir isso é projeto; descobrir
durante o incidente é sorte.

### O28. Incidente gera aprendizado registrado **[RECOMENDADA]**

Post-mortem sem culpa: linha de tempo, causa, o que faltou detectar, e a ação que evita a
reincidência — com item de backlog e ID. Incidente sem ação registrada vai se repetir.

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
