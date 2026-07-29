# Checklist — Pré-análise (portão G0)

Executar **antes** de apontar qualquer problema. Neste portão é proibido propor mudanças: o objetivo é
entender, e opinar cedo produz achados superficiais.

---

## Contexto

- [ ] O [perfil do projeto](../templates/perfil-do-projeto.md) existe e foi lido. Se não existe,
      criá-lo é o primeiro entregável.
- [ ] O objetivo desta rodada está escrito, com critério de sucesso mensurável.
- [ ] Os **não objetivos** estão escritos. Sem isso, o escopo infla.
- [ ] As camadas de [análise](../volumes/vol-01-constituicao.md) em escopo estão definidas.
- [ ] A tolerância a risco do projeto é conhecida.

## Terreno

- [ ] Pontos de entrada mapeados: rotas, jobs, consumidores de fila, comandos, webhooks.
- [ ] Módulos e responsabilidades listados.
- [ ] Direção das dependências observada.
- [ ] Fluxo do dado principal traçado, da entrada à persistência.
- [ ] Entidades do domínio e o que o sistema promete ao usuário identificados.

## Zonas de risco

- [ ] Onde estão: autenticação, autorização, pagamento, dado pessoal.
- [ ] Onde estão as migrações e operações destrutivas.
- [ ] Onde estão as integrações externas.
- [ ] Onde há concorrência sobre recurso escasso.
- [ ] Qual falha causaria o maior dano — e a quem.

## O que já existe

Verificar antes de recomendar o que já está lá. Recomendar o existente destrói a credibilidade do
relatório inteiro.

- [ ] Testes: quais tipos, o que cobrem, como rodar.
- [ ] Lint, formatter e verificação de tipos: configurados? bloqueiam?
- [ ] CI/CD: existe? bloqueia ou apenas reporta?
- [ ] Observabilidade: log, métrica, alerta.
- [ ] Documentação e ADRs existentes.
- [ ] Convenções reais do código — que podem divergir das documentadas.

## Histórico

- [ ] `git log` recente das áreas em escopo.
- [ ] Áreas com alta frequência de mudança (sinal de acoplamento ou de instabilidade).
- [ ] Incidentes ou correções emergenciais recentes.
- [ ] Código com comentário explicando decisão estranha — leia antes de "corrigir".

## Comandos base

- [ ] Sei rodar: instalação, testes, verificação de tipos, lint, build, aplicação local.
- [ ] Executei ao menos os testes e a verificação de tipos, para conhecer o estado inicial.
      Sem isso, é impossível distinguir o que você quebrou do que já estava quebrado.

---

## Saída obrigatória

```
## Mapa (10–20 linhas)
Módulos: <nome — responsabilidade — depende de>
Fluxo principal: <entrada → ... → persistência>
Zonas de risco: <lista>
Estado inicial: testes <passando/falhando>, tipos <ok/erros>, lint <ok/erros>

## Perguntas abertas
1. <pergunta> — bloqueia: <o que> — quem responde: <quem>
```

## Critério de passagem

Você consegue descrever, sem reabrir arquivos: o que o sistema faz, para quem, e onde uma falha
causaria o maior dano.

Se não consegue, continue em G0. Avançar sem o mapa é a origem do relatório que só encontra problemas
de estilo.
