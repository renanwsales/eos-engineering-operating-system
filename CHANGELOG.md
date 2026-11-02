# Changelog

Versionamento semântico conforme [`AUTHORING.md`](AUTHORING.md) seção 7 (`A-020`). Decisões estruturais
ficam em [`backlog/adr/`](backlog/adr/); este arquivo registra **o que** mudou em cada versão.

## 3.2.0 — 2026-11-01

`MINOR`. Cinco regras novas no Volume 06; nenhuma regra existente alterada.

- `SEC-097` — exceção dentro de controle de segurança nega (OWASP A10:2025). Linha 17 da tabela de
  bloqueio. Fecha `EOS-013`.
- Capítulo 6.13, `SEC-098`–`SEC-101` — o agente de desenvolvimento como superfície: sem credencial de
  produção por padrão, operação destrutiva com aprovação humana no ato, conteúdo lido é dado e não
  instrução, ferramenta e servidor MCP são dependência. Linha 18 da tabela de bloqueio; não negociável 7
  e duas condições de parada no `AGENTS.md`; `dist/system-prompt.md` e papel Security alinhados. Fecha
  `EOS-014`.
- O checklist de segurança deixou de copiar a tabela de bloqueio do Vol 06 e passou a citá-la (`A-001`):
  a cópia tinha 12 condições, e o volume, 16.

## 3.1.1 — 2026-11-01

`PATCH`. Nenhuma regra criada, alterada, revogada ou renumerada.

- **Referências de volume herdadas da v2 corrigidas.** A tabela de `ORC-001` mandava papéis para volumes
  errados (Orquestrador → 12, QA → 9, Auditor → 11, Segurança ↔ Banco trocados); `ORC-002`/`ORC-005`
  citavam a Constituição como "Volume 1" e "os doze" volumes; 13 links diziam um volume e apontavam
  para outro.
- **Capítulos numerados pelo volume que os contém**, como a anatomia de `AUTHORING.md` prescreve
  (`Capítulo NN.x`). Antes: Vol 11 usava 9.x (colidindo com o Vol 09), e Vols 00, 01, 05, 06 e 12 usavam
  numeração da v2. A Parte II do Vol 02 passou de 2.1–2.7 (duplicando a Parte I) para 2.8–2.14.
- **SUMARIO** alinhado aos volumes: o núcleo de multi-inquilino (`ESC-036`–`ESC-042`) vive no Vol 14 e o
  Vol 16 o cita, como os dois volumes já diziam.
- **Vol 01** ganhou a seção `Verificação obrigatória de saída` na posição da anatomia.
- **Vol 19**: checklist reduzido de 28 para 25 itens (`A-011`, `CHK-016`), sem perder rastreio.
- **Vol 06 e checklist de segurança**: códigos OWASP atualizados para o Top 10:2025, com mapa
  2025 ↔ 2021 ↔ EOS e bloco para A10:2025 (condições excepcionais) usando regras existentes.
- **`dist/system-prompt.md`**: contagem obsoleta removida; alinhado ao `AGENTS.md` (incidente ativo,
  afrouxar asserção) e à cadeia de suprimentos (`SEC-043`, `SEC-094`, `SEC-096`).
- **`scripts/check-links.py`** falha quando o texto de um link nomeia um volume e o alvo é outro.
  Rodado contra a 3.1.0, aponta os 13 casos corrigidos aqui.

## 3.1.0 — 2026-10-07

`MINOR`. 41 regras novas, sem alteração das existentes. (Publicada sem incremento de versão; registrada
retroativamente.)

- `SEC-067`–`SEC-076` — SQL dinâmico, DSL de filtro, XSS em HTML fora do SPA.
- `SEC-077`–`SEC-084` — superfície de dados pública (BaaS / "banco aberto").
- `SEC-085`–`SEC-088` — chave de API de integração exposta.
- `SEC-089`–`SEC-093` e `PLB-059`–`PLB-063` — rotas de API expostas sem sessão de usuário.
- `SEC-094`–`SEC-096` e `OPS-049` — lockfile travado, scripts de lifecycle, slopsquatting.
- `IAX-070`–`IAX-074` — injeção de prompt em agentes com ferramentas.
- `SEC-026` aprofundada (brute force no provedor de identidade).

## 3.0.0 — 2026-07-29

Reestruturação como livro de 25 volumes, com contrato de autoria e sumário de fronteiras
([ADR-0004](backlog/adr/0004-livro-de-25-volumes.md)).
