# ADR-0002 — Reorganizar o EOS em 12 volumes com regras numeradas

- **Status:** aceito
- **Data:** 2026-07-29
- **Decisores:** dono do produto
- **Versão do EOS:** 1.0.0 → 2.0.0 (`MAJOR`)
- **Substitui parcialmente:** [ADR-0001](0001-adocao-do-eos.md), que permanece válido quanto à decisão de
  adotar um framework em camadas em vez de um prompt único

---

## Contexto

A versão 1.0.0 organizava o material em duas árvores paralelas: `manual/` (filosofia e processo, 12
documentos) e `standards/` (normas técnicas, 10 documentos). A separação era por **natureza do texto** —
processo versus norma.

Três problemas apareceram ao usar a estrutura:

1. **A consulta não segue a natureza do texto, segue o domínio.** Quem trabalha em banco de dados quer
   modelagem, índices, migrações e a matriz de risco de migração ao mesmo tempo. Isso estava dividido entre
   `standards/banco-de-dados.md` e `manual/07-matriz-de-risco.md`.
2. **Regras não eram citáveis de forma estável.** Os IDs eram locais a cada arquivo (`A5`, `N2`, `P19`),
   colidiam entre arquivos, e não sobreviviam a uma reorganização. Um relatório dizendo "viola A5" era
   ambíguo.
3. **Não havia como contar nem auditar a cobertura.** Sem inventário, não era possível responder "quantas
   regras obrigatórias existem?" nem detectar que uma área estava sub-especificada.

## Problema como restrição

O material precisa ser: consultável por domínio de trabalho; citável por identificador estável em relatórios
de revisão; e verificável automaticamente quanto a numeração, cobertura e referências cruzadas.

## Alternativas

### A — Manter `manual/` + `standards/` e apenas adicionar IDs globais

- **Custo:** baixo. Só renumeração.
- **A favor:** nenhuma migração de conteúdo, nenhum link quebrado.
- **Contra:** não resolve o problema 1, que é o que gera atrito diário. A pessoa continua abrindo dois
  arquivos de árvores diferentes para uma única tarefa.

### B — Reorganizar em 12 volumes por domínio, com prefixo de regra por volume **(escolhida)**

- **Custo:** médio-alto. Migração de 22 documentos, remapeamento de ~230 links, reescrita do roteador.
- **A favor:** um volume por domínio de decisão; prefixo por volume dá ID estável e legível (`SEC-004` diz o
  domínio antes de você abrir nada); o índice passa a ser gerável, e portanto verificável.
- **Contra:** o Volume 1 fica grande, porque absorve todo o processo mais as normas universais de ofício.
  Aceito: é o único volume carregado em toda tarefa, então concentrá-lo tem valor prático.

### C — Um arquivo por regra, com índice gerado

- **Custo:** alto, e permanente.
- **A favor:** granularidade máxima de carga de contexto; diff mínimo por mudança de regra.
- **Contra:** 572 arquivos. Perde-se completamente a legibilidade como documento — ninguém lê um volume, e
  a coerência interna de um capítulo (que é onde as regras se explicam mutuamente) desaparece. Rejeitada
  por otimizar a máquina contra o leitor humano.

### D — Não fazer nada

- **A favor:** a versão 1.0.0 é utilizável; o atrito é real mas tolerável.
- **Contra:** o custo de migrar cresce com cada documento adicionado e cada projeto que passa a referenciar
  os caminhos antigos. Este é o momento mais barato para fazer.

## Decisão

Alternativa **B**. Doze volumes em `volumes/`, um prefixo de regra por volume, `RULES-INDEX.md` gerado por
script, e `manual/` e `standards/` removidos — sem duplicação de conteúdo, porque duas fontes de verdade para
a mesma norma é exatamente o que `ARC-011` proíbe.

Acrescentado ao mesmo tempo: o papel **Performance Engineer** (`agents/06-performance.md`), que na versão
1.0.0 estava diluído entre Backend e Database. A cadeia passa de 10 para 11 papéis.

### Trocas aceitas

- Aceito **um Volume 1 grande** (86 regras) em troca de um único arquivo carregado por toda tarefa.
- Aceito **572 regras** em vez das 200–400 estimadas inicialmente. A contagem maior vem de numerar também
  princípios, portões e normas de ofício, que antes eram texto corrido. Preferi numerá-los: regra sem ID não
  é citável em revisão, e norma não citável é norma que não se aplica.
- Aceito **quebrar referências externas** aos caminhos antigos. Não há consumidores externos ainda, o que
  torna este o momento de menor custo.

## Condição de invalidação

Esta decisão passa a estar errada se:

- um volume passar de ~120 regras, ponto em que carregá-lo inteiro deixa de ser razoável e a divisão por
  capítulo em arquivos separados passa a valer;
- na prática as pessoas pararem de citar IDs nos relatórios, o que indicaria que o custo de olhar o índice
  supera o benefício da precisão;
- surgir a necessidade de servir o EOS a mais de um projeto com normas divergentes, caso em que a divisão
  correta passa a ser núcleo comum versus sobreposição por projeto, não por domínio.

## Consequências

**Positivas:** consulta alinhada ao trabalho real · IDs estáveis e autoexplicativos · índice e links
verificados por script no lugar de disciplina humana · lacunas de cobertura por domínio agora visíveis na
contagem por volume.

**Negativas:** Volume 1 concentra três assuntos (princípios, processo, ofício) · a remoção de `manual/` e
`standards/` invalida qualquer referência externa · o índice exige regenerar após cada mudança de regra, o
que é mitigado por `build-rules-index.py --check` no pipeline.

## Verificação

```bash
python3 scripts/build-rules-index.py --check   # numeração contínua, sem lacunas, índice em dia
python3 scripts/check-links.py                 # 263 links, 1330 referências de regra, 0 quebradas
```

## Rollback

O commit anterior (`checkpoint: EOS v1.0.0 antes da migracao para volumes`) contém a estrutura íntegra. O
rollback é `git revert` do commit de migração. Nenhum conteúdo foi descartado: todo texto de `manual/` e
`standards/` está redistribuído nos volumes, e a única perda deliberada foi a duplicação entre eles.
