# ADR-0003 — Três volumes novos (seleção, escala, playbooks) em vez de expandir para 25

- **Status:** aceito
- **Data:** 2026-07-29
- **Decisores:** dono do produto
- **Versão do EOS:** 2.0.0 → 2.1.0 (`MINOR` — adiciona sem invalidar nada existente)

---

## Contexto

Foi proposta uma expansão do EOS para **25 volumes, entre 250 e 500 páginas**, com uma lista explícita de
temas: seleção de estilo arquitetural, escalabilidade, multi-inquilino, APIs (GraphQL, webhooks),
observabilidade, design system, produto, IA, prompt engineering, playbooks, um checklist de mais de 500 itens e
outro de mais de 1.000 verificações, além de uma biblioteca de 15 prompts.

Auditei a lista item por item contra as 572 regras existentes, contando menções por tema para não presumir
cobertura. O resultado:

| Situação | Quantidade | Exemplos |
| --- | --- | --- |
| Já coberto por volume existente | 12 temas | Observabilidade é o cap. 10.3; Métricas é o cap. 1.11; Design System é o cap. 4.4; Auditoria e Code Review são o Vol 11 |
| Lacuna real | 7 temas | Seleção de arquitetura; escala de banco; renderização; isolamento de inquilino; webhooks de saída e GraphQL; contrapressão; playbooks de tarefa |
| Nocivo se adotado | 3 itens | Checklists de 500 e 1.000 itens; volume de prompt engineering; papel "refatorador" |

## Problema, como restrição

As sete lacunas compartilham uma forma: são **critérios de escolha**, não normas novas. O EOS dizia muito bem
o que é certo *dentro* de uma abordagem, e quase nada sobre **qual abordagem**. Um agente sabia inverter
dependências, mas não sabia se aquele módulo deveria ser um serviço separado.

A restrição em sentido oposto é `ORC-005` e `AUD-001`: volume de conteúdo tem custo. Contexto irrelevante
carregado degrada julgamento, e falha por excesso é tratada como igual à falha por omissão.

## Alternativas

### A — Expandir para os 25 volumes propostos

- **A favor:** cumpre a proposta literalmente; sensação de completude.
- **Contra:** cerca de 12 volumes seriam duplicação de conteúdo existente sob outro nome, violando `ARC-011` —
  duas fontes de verdade para a mesma norma divergem, e a divergência é o defeito. Os checklists de 500 e 1.000
  itens produzem `AUD-002` em escala industrial: ninguém lê 500 caixas, marca-se todas, e a auditoria passa a
  gerar afirmações não verificadas com aparência de rigor. Chegar a 500 páginas exigiria diluição deliberada.

### B — Não expandir; a cobertura é suficiente

- **A favor:** custo zero, nenhum risco de diluição.
- **Contra:** as sete lacunas são reais e verificadas por contagem. A ausência de critério de escolha é
  exatamente onde erros arquiteturais caros nascem, e é o tipo de erro que nenhuma das 572 regras existentes
  detecta, porque todas pressupõem a escolha já feita.

### C — Três volumes novos, fechando as sete lacunas **(escolhida)**

Volume 13 (Seleção de Arquitetura), Volume 14 (Escala e Multi-Inquilino), Volume 15 (Playbooks), mais
capítulos nos volumes existentes onde a lacuna era parcial: webhooks, GraphQL e trabalho agendado no Volume 3;
níveis de verificação no Volume 5.

- **A favor:** fecha cada lacuna verificada, sem duplicar nenhuma norma existente. Mantém o documento no
  tamanho em que ainda é carregado seletivamente. Os volumes 13 e 14 introduzem uma categoria que faltava —
  decisão entre alternativas legítimas — e o 15 é a camada que torna 735 regras executáveis numa tarefa
  concreta.
- **Contra:** 735 regras é mais do que a estimativa original de 200 a 400. E o Volume 15 tem natureza
  diferente dos outros: seus itens são passos ordenados, não normas atemporais.

## Decisão

Alternativa **C**. Três volumes novos, dois capítulos novos em volumes existentes, e recusa explícita dos
itens classificados como nocivos.

Do Volume 6 proposto (Segurança sobre NIST, CIS e ISO 27001), aproveitou-se apenas a ideia de **níveis
progressivos de verificação** do ASVS, como `SEC-059` a `SEC-063`. NIST, CIS e ISO 27001 foram recusados por
serem frameworks de conformidade organizacional — política, treinamento, gestão de fornecedor — com quase
nenhuma tradução para regra verificável em código.

O Volume 19 proposto (IA no produto) foi recusado por decisão de produto: a IA é ferramenta de
desenvolvimento, não funcionalidade entregue ao usuário. Registrado com gatilho em `EOS-004`.

## Contrapartidas aceitas

- Aceito **735 regras**, acima da estimativa inicial. A mitigação é estrutural, não editorial: `ORC-005` e a
  tabela de carregamento do `AGENTS.md` fazem com que nenhuma tarefa carregue os quinze volumes.
- Aceito que o Volume 15 misture natureza — passos ordenados numerados como regras. A alternativa era colocar
  playbooks em `runbooks/`, o que os deixaria fora do `RULES-INDEX.md` e, portanto, não citáveis num achado.
  Ser citável venceu a pureza taxonômica.
- Aceito que o Volume 3 fique grande (73 regras). Separar APIs num volume próprio duplicaria a fronteira entre
  contrato e regra de negócio, que é justamente o que ele existe para manter junta.
- Aceito que os capítulos de GraphQL e webhook sejam inaplicáveis a alguns projetos. São carregados por
  necessidade, e o cabeçalho do volume declara isso.

## Condições de invalidação

Esta decisão deve ser revista se:

- **Um volume passar de ~90 regras.** Sinal de que ele acumulou mais de um domínio e a divisão foi mal feita.
- **Duas regras de volumes diferentes se contradisserem.** É o defeito que a alternativa A garantiria e que
  esta pretende evitar; se ocorrer aqui, a separação escolhida está errada.
- **Os playbooks começarem a divergir dos volumes que citam.** Indica que a duplicação que eu quis evitar
  entrou por outra porta, e o Volume 15 precisa passar a apenas referenciar, nunca reafirmar.
- **O produto passar a ter funcionalidade de IA para o usuário final.** Gatilho de `EOS-004`.

## Consequências

Imediatas: `AGENTS.md` ganha rotas para escolha de abordagem, trabalho multi-inquilino e execução por
playbook. O Arquiteto passa a ser dono do Volume 13; Database, Performance e DevOps compartilham o Volume 14;
Segurança passa a declarar nível de verificação (`SEC-060`) em todo relatório.

A médio prazo, a métrica que decide se esta decisão foi boa é uma só: **os playbooks são de fato usados**, ou
viraram documento morto. Se em três meses nenhum relatório citar uma regra `PLB`, o Volume 15 falhou, e a
resposta correta é encurtá-lo, não expandi-lo.
