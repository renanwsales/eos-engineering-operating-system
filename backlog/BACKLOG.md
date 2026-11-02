# Backlog

Fonte única de trabalho pendente. Formato: [`templates/entrada-de-backlog.md`](../templates/entrada-de-backlog.md).

**Regra de entrada:** toda `OPPORTUNITY` encontrada e não corrigida entra aqui **na mesma sessão** em
que foi encontrada. Achado que só existe no chat é trabalho de diagnóstico jogado fora.

Se o projeto usa um rastreador de issues, use o rastreador **ou** este arquivo — nunca os dois.
Duplicidade de fonte é como o backlog morre.

---

## Ativos

Ordenados por score. Recalcular os 10 do topo a cada rodada.

| ID | Título | Sev. | Conf. | Esforço | Risco | Score | Gatilho de promoção | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EOS-016 | Incidente com dado pessoal sem caminho de notificação regulatória | S2 | MEDIUM | S | LOW | 6.3 | Primeiro incidente com dado pessoal, ou primeira auditoria de conformidade | aberto |
| EOS-017 | `A-021` manda rodar dois scripts; o CI roda três | S3 | HIGH | XS | LOW | 4.0 | Próxima mudança `MAJOR` do livro (regra `[IMUTÁVEL]`) | aberto |
| EOS-002 | Limiares de métrica nunca calibrados contra um módulo real | S2 | MEDIUM | M | LOW | 3.4 | Primeira revisão completa de módulo concluída | aberto |
| EOS-012 | Regras fora da ordem numérica no corpo dos Vols 06, 10 e 19 | S3 | HIGH | M | LOW | 1.5 | Próxima edição editorial de um deles ou reclamação de navegação | aberto |
| EOS-010 | Volume 00 tem numeração fora de ordem no documento | S3 | HIGH | M | MEDIUM | 1.3 | Se um leitor humano relatar dificuldade de navegação no Vol 00 | aberto |
| EOS-013 | Nenhuma regra geral de fail-closed em exceção de controle de segurança (OWASP A10:2025) | S2 | HIGH | S | LOW | 16.0 | Próxima edição do Vol 06, ou primeiro achado de exceção que libera acesso | feito |
| EOS-014 | Segurança operacional do próprio agente de desenvolvimento sem norma | S2 | MEDIUM | M | LOW | 6.5 | Agente com shell, banco ou credencial de nuvem num repositório adotante | feito |
| EOS-009 | Playbooks podem divergir das regras que citam | S2 | MEDIUM | S | LOW | 4.0 | Primeira alteração de regra em volume citado pelo Vol 21 | feito |
| EOS-001 | Perfil do projeto ainda não preenchido para o repositório alvo | S1 | HIGH | S | LOW | 20.0 | Primeira rodada de revisão em qualquer projeto | feito |
| EOS-003 | Verificação do EOS não roda automaticamente | S2 | HIGH | XS | LOW | 14.0 | Primeira hospedagem do repositório em plataforma com CI | feito |
| EOS-011 | Anatomia AUTHORING incompleta nos volumes herdados | S2 | HIGH | L | LOW | 8.0 | Fechamento editorial v3 | feito |

### EOS-001 — Perfil do projeto ainda não preenchido

```
Severidade: S1 | Confiança: HIGH | Esforço: S | Risco: LOW | Score: 20.0
Evidência: templates/perfil-do-projeto.md contém apenas placeholders
Consequência se ignorado: todo julgamento técnico dos agentes fica sem base — stack, comandos de
  validação, limiares, classificação de módulos e tolerância a risco são desconhecidos. Sem os
  comandos, nenhuma mudança pode ser validada, e mudança não validada não existe.
Gatilho de promoção: primeira rodada de revisão em qualquer projeto que adote o EOS
Origem: criação do framework, 2026-07-29
Status: feito — perfil preenchido vive no repositório adotante (`.eos/perfil.md`); o template
  público permanece placeholder de propósito (2026-07-29)
```

### EOS-003 — Verificação do EOS não roda automaticamente

```
Severidade: S2 | Confiança: HIGH | Esforço: XS | Risco: LOW | Score: 14.0
Evidência: scripts/build-rules-index.py e scripts/check-links.py existem e passam, mas nada os
  executa a cada mudança. Não há arquivo de pipeline no repositório.
Consequência se ignorado: o índice de regras e o índice de links divergem do conteúdo na primeira
  vez que alguém adicionar uma regra sem rodar o gerador. Isso é exatamente o que OPS-028 chama de
  teatro: verificação que existe e não bloqueia.
Correção: um job que rode os dois scripts e falhe o build.
Gatilho de promoção: primeira hospedagem do repositório em plataforma com CI
Origem: migração para volumes, 2026-07-29
Status: feito — `.github/workflows/ci.yml` roda `build-rules-index.py --check` e `check-links.py`
  em push/PR (2026-07-29)
```

### EOS-009 — Playbooks podem divergir das regras que citam

```
Severidade: S2 | Confiança: MEDIUM | Esforço: S | Risco: LOW | Score: 4.0
Evidência: ../21-playbooks.md cita 60+ regras de outros volumes por ID. Nenhum mecanismo
  verifica se a regra citada ainda diz o que o passo do playbook afirma que ela diz.
Consequência se ignorado: a duplicação que o ADR-0003 quis evitar entra pela porta dos playbooks. Um
  passo que reafirma o conteúdo de uma regra em vez de referenciá-la divergirá dela na primeira
  alteração, e passará a ser uma segunda fonte de verdade — ARC-011.
Correção: verificação que confirme que todo passo de PLB referencia sem reafirmar; ou revisão manual
  do Vol 15 a cada mudança nos volumes citados.
Gatilho de promoção: primeira alteração de regra em qualquer volume citado pelo Vol 21
Origem: ADR-0003, 2026-07-29
Status: feito — `scripts/check-playbook-refs.py` exige citação de domínio em todo PLB;
  passos sem citação corrigidos; job no CI (2026-07-29). Reafirmação literal ainda é
  revisão humana; existência de IDs = `check-links.py`.
```

### EOS-012 — Regras fora da ordem numérica no corpo dos Vols 06, 10 e 19

```
Severidade: S3 | Confiança: HIGH | Esforço: M | Risco: LOW | Score: 1.5
Evidência: 06-seguranca.md — após SEC-024 vêm SEC-067–076 (cap. 6.3); SEC-077–084 no 6.5b;
  SEC-038–043/094–096 no 6.6; SEC-044+ no 6.7. 10-devops.md — OPS-049 entre OPS-034 e OPS-035.
  19-ia-no-produto.md — IAX-070–074 antes de IAX-066. IDs estáveis (correto, A-007); leitura
  linear do arquivo salta a numeração. Ampliado em 2026-11-01 (revisão 3.1.1).
Consequência se ignorado: revisor humano/agente pode achar que faltam regras ou que houve
  colisão de ID; aumenta custo de onboarding no volume mais editado da série de segurança.
Gatilho de promoção: próxima edição editorial do Vol 06, 10 ou 19, ou reclamação de navegação
Origem: auditoria pós-merge PRs #1–#7, 2026-10-07
Status: aberto — não renumerar IDs; só melhorar âncoras/sumário interno por capítulo
```

### EOS-010 — Volume 00 tem numeração fora de ordem no documento

```
Severidade: S3 | Confiança: HIGH | Esforço: M | Risco: MEDIUM | Score: 1.3
Evidência: ../00-constituicao-da-engenharia.md — o capítulo 0.4 (CON-056 a CON-064) aparece antes do
  capítulo 0.5 (CON-023), e o fechamento CON-055 aparece depois de CON-086. A numeração é contínua e
  única (o gerador valida), mas a ordem no documento não é crescente.
Causa: o capítulo dos seis portões e as convenções de ofício foram inseridos na reorganização v2.0.0
  recebendo números no fim da faixa, em posições anteriores no texto.
Consequência se ignorado: leitor humano percorrendo o volume vê a numeração retroceder, o que reduz a
  confiança no índice. Nenhum efeito sobre agentes, que resolvem por ID.
Por que não foi corrigido agora: corrigir exige renumerar 64 regras. Os IDs são citados em ADR-0002,
  ADR-0003, no AGENTS.md e no contrato comum — e a estabilidade do ID é o que torna a regra citável.
  Trocar estabilidade de ID por ordem estética é precisamente o que CON-013 proíbe. O mesmo problema
  no Vol 5 foi corrigido nesta sessão porque as regras eram novas e não publicadas.
Correção, se promovido: renumerar com script, atualizar toda referência cruzada, e registrar em ADR o
  mapa de IDs antigos para novos.
Gatilho de promoção: relato humano de dificuldade de navegação no Vol 00
Origem: validação da v2.1.0, 2026-07-29
Status: aberto
```

### EOS-011 — Anatomia AUTHORING incompleta nos volumes herdados

```
Severidade: S2 | Confiança: HIGH | Esforço: L | Risco: LOW | Score: 8.0
Evidência: 00, 01, 02, 03, 04, 05, 06, 07, 08, 10, 11, 12, 14, 21 — faltam seções
  obrigatórias de AUTHORING.md (Fronteira, Fundamentos, Padrões, Prompt, etc.)
Consequência: agentes e humanos não encontram o mesmo "fechamento" operacional que
  os volumes 09+ têm; prompts por volume ausentes; checklists do volume ausentes.
Correção: acrescentar seções sem criar regras novas nem renumerar IDs (A-007).
Gatilho: esta sessão / ADR-0004
Origem: ADR-0004, 2026-07-29
Status: feito — anatomia acrescentada sem novas regras (2026-07-29)
```

### EOS-013 — Nenhuma regra geral de fail-closed em exceção de controle de segurança

```
Severidade: S2 | Confiança: HIGH | Esforço: S | Risco: LOW | Score: 16.0
Evidência: OWASP Top 10:2025 criou A10 (Mishandling of Exceptional Conditions). No EOS, fail-closed
  só existe para casos específicos — SEC-090 (JWT desligado no gateway), SEC-093 (sink sem segredo),
  SEC-087 (webhook). BAK-023 e BAK-045 tratam erro engolido e comportamento em falha, mas não dizem
  que exceção dentro de verificação de acesso, assinatura ou limite deve negar. Mapa no Vol 06.
Consequência se ignorado: o padrão `try { autoriza() } catch { log() }` seguido da operação passa
  pela revisão sem regra a citar. É o caminho clássico de bypass quando o provedor de identidade,
  o cache de permissão ou a verificação de assinatura falha.
Correção: regra nova "Exceção em controle de segurança nega" no fim da faixa SEC (A-007), com
  par ruim/bom; atualizar o bloco 11 do checklist de segurança para citá-la. MINOR.
Gatilho de promoção: próxima edição do Vol 06, ou primeiro achado de exceção que libera acesso
Origem: revisão 3.1.1, 2026-11-01
Status: feito — `SEC-097` no capítulo 6.1, linha 17 da tabela de bloqueio, bloco 11 do
  checklist de segurança (3.2.0, 2026-11-01)
```

### EOS-014 — Segurança operacional do próprio agente de desenvolvimento sem norma

```
Severidade: S2 | Confiança: MEDIUM | Esforço: M | Risco: LOW | Score: 6.5
Evidência: o EOS governa como o agente analisa e decide (Vols 00, 01, 20), e SEC-096 trata pacote
  sugerido por modelo. Nenhuma regra trata o que o agente pode executar: credencial de produção
  no ambiente do agente, comando destrutivo (DROP, migração, force push, rm) contra recurso real,
  confiança em servidor MCP/ferramenta de terceiro, conteúdo de repositório lido como instrução.
  Busca por "credencial de produção", "acesso à produção", "agente.*permiss" em 00, 01, 10, 20,
  AGENTS.md e agents/: nenhum resultado normativo.
Consequência se ignorado: o livro é escrito para desenvolvimento assistido por IA, e o dano mais
  caro desse modo de trabalho — o agente apagando ou alterando dado real por engano ou por injeção —
  não tem regra a citar nem portão que o bloqueie. CON-053 cobre "parar e perguntar" em migração de
  dado, mas depende do agente reconhecer que o alvo é produção.
Correção: capítulo curto no Vol 01 ou 20 (ou regras no 06): ambiente do agente sem credencial de
  produção por padrão; operação destrutiva só com aprovação humana explícita (R4); ferramenta/MCP
  novo é dependência (SEC-043); conteúdo lido do repositório é dado, não instrução (IAX-061).
Gatilho de promoção: agente com shell, banco ou credencial de nuvem num repositório adotante
Origem: revisão 3.1.1, 2026-11-01
Status: feito — capítulo 6.13, `SEC-098`–`SEC-101`; não negociável 7 e duas condições de
  parada no AGENTS.md; dist/system-prompt.md alinhado (3.2.0, 2026-11-01)
```

### EOS-016 — Incidente com dado pessoal sem caminho de notificação regulatória

```
Severidade: S2 | Confiança: MEDIUM | Esforço: S | Risco: LOW | Score: 6.3
Evidência: SEC-053–SEC-058 cobrem inventário, minimização, retenção e direitos do titular.
  OPS-048 trata incidente ativo. Nenhuma regra liga os dois: incidente que envolve dado pessoal
  dispara notificação à autoridade e aos titulares, com prazo regulatório (LGPD/ANPD, GDPR).
  templates/perfil-do-projeto.md já menciona LGPD, mas nada no livro consome esse campo.
Consequência se ignorado: o prazo de comunicação começa a correr enquanto a equipe ainda trata o
  incidente como técnico; descobrir quem notifica, o quê e até quando no meio do incidente é o
  cenário que gera sanção.
Correção: regra agnóstica de jurisdição no Vol 10 (resposta a incidente) ou 06 (dados pessoais),
  com prazo e responsável vindos do perfil do projeto ([perfil]).
Gatilho de promoção: primeiro incidente com dado pessoal, ou primeira auditoria de conformidade
Origem: revisão 3.1.1, 2026-11-01
Status: aberto
```

### EOS-017 — `A-021` manda rodar dois scripts; o CI roda três

```
Severidade: S3 | Confiança: HIGH | Esforço: XS | Risco: LOW | Score: 4.0
Evidência: AUTHORING.md A-021 ("Rode os dois") lista build-rules-index.py e check-links.py;
  .github/workflows/ci.yml e o README rodam também check-playbook-refs.py.
Consequência se ignorado: quem segue A-021 localmente descobre a falha de playbook só no CI.
Por que não foi corrigido agora: A-021 é [IMUTÁVEL]; alterar o texto é MAJOR com ADR (A-020).
Correção, se promovido: substituir a lista por "todos os scripts em scripts/" para não envelhecer
  de novo.
Gatilho de promoção: próxima mudança MAJOR do livro
Origem: revisão 3.1.1, 2026-11-01
Status: aberto
```

### EOS-002 — Limiares de métrica nunca calibrados contra um módulo real

```
Severidade: S2 | Confiança: MEDIUM | Esforço: M | Risco: LOW | Score: 3.4
Evidência: CON-050 declara limiares padrão marcados [perfil]; nenhum foi confrontado com medição
  de um módulo real deste ou de outro projeto.
Consequência se ignorado: os agentes bloqueiam ou liberam entregas com base em números escolhidos
  por plausibilidade, não por evidência. Limiar mal calibrado gera ruído (bloqueia o que não
  importa) ou falsa segurança (libera o que importa) — e ambos corroem a confiança no framework.
Correção: rodar o runbook de revisão completa em um módulo real, medir, e ajustar os limiares do
  perfil do projeto com os números observados e a data.
Gatilho de promoção: primeira revisão completa de módulo concluída
Origem: ADR-0001, mantido na migração para volumes
Status: aberto
```

---

## Dívida assumida deliberadamente

| ID | O quê | Custo de manter | Custo de pagar | Gatilho | Aceito por |
| --- | --- | --- | --- | --- | --- |
| EOS-011 | Volumes herdados — anatomia AUTHORING | Pago na v3.0.0 | — | — | ADR-0004 |
| EOS-004 | Vol 19 escrito mas **não é norma ativa na Vire** (banner de estado) | Risco de carregar IAX em tarefa sem feature de IA | Remover banner quando produto ganhar IA ao usuário | Feature de IA no produto | dono do produto |

---

## Não faremos

Estado saudável e necessário. Backlog que só cresce perde utilidade.

| ID | Título | Motivo da decisão | Data | Decidido por |
| --- | --- | --- | --- | --- |
| EOS-005 | Checklists de 500 e 1.000 itens | Produz `AUD-002` em escala: 500 caixas não são lidas, são marcadas. Doutrina no Vol 22; 7 checklists em `checklists/` | 2026-07-29 | dono do produto |
| EOS-007 | Papel "Refatorador" na cadeia de agentes | Convida o que `CON-013` proíbe. Refatoração nasce de achado de outro papel | 2026-07-29 | dono do produto |
| EOS-008 | Volumes sobre NIST, CIS e ISO 27001 | Conformidade organizacional; quase nada vira regra em código. ASVS níveis em `SEC-059+` | 2026-07-29 | dono do produto |

---

## Obsoletos

| ID | Título | Por que deixou de existir | Data |
| --- | --- | --- | --- |
| EOS-015 | Trilha de auditoria de negócio sem regra | Aberto por erro de leitura: `SEC-011` (registro de auditoria em operação sensível) já cobre. Registrado para que o ID não seja reaproveitado | 2026-11-01 |
| EOS-006 | Volume de prompt engineering como "não faremos" | Invalidado por ADR-0004: Vol 20 existe como doutrina operacional (não meta-prompt vazio) | 2026-07-29 |
| EOS-004 (não-faremos absoluto) | Não escrever Vol de IA | Substituído: Vol 19 existe como referência; dívida EOS-004 acima = não ativar como norma Vire | 2026-07-29 |

---

## Higiene periódica

Executada pelo orquestrador a cada rodada. Ver
[gestão de backlog](../12-auditoria.md).

- [ ] Verificar obsolescência: evidência (`arquivo:linha`) que não existe mais.
- [ ] Reavaliar severidade com os modificadores de contexto.
- [ ] Aplicar a **regra das três postergações**: no terceiro adiamento, promover ou marcar
      `não faremos`. Nunca postergar uma quarta vez.
- [ ] Agrupar itens relacionados no mesmo módulo — cinco itens costumam ser um item estrutural.
- [ ] Recalcular o score dos 10 do topo.

Reserva de capacidade que garante o avanço do backlog: **20% de cada rodada** vai para o item de maior
score daqui. Sem essa reserva, `MUST-FIX` consome 100% da capacidade indefinidamente e a dívida cresce
até virar `MUST-FIX` ela mesma — normalmente na forma de um incidente.

---

## Próximo ID disponível

`EOS-018`
