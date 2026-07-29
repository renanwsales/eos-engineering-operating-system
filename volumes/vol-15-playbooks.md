# 📕 Volume 15 — Playbooks

Prefixo: `PLB` · Regras: PLB-001 a PLB-058 · Papel: qualquer, conforme a tarefa

Os outros volumes dizem o que é certo. Este diz **em que ordem fazer**, para as tarefas que se repetem toda
semana. É a camada que transforma 500 regras em trabalho executável.

A diferença em relação a [`runbooks/`](../runbooks/): runbook coordena **papéis** numa rodada de revisão;
playbook executa **uma tarefa** de construção, normalmente por um papel só.

---

## Capítulo 15.1 — Como usar um playbook

### PLB-001 — Playbook não substitui os portões **[IMUTÁVEL]**

Ele é a trilha de G3 (implementação). G0 a G2 continuam valendo: você precisa saber o que existe, ter um
achado ou requisito, e ter decidido entre alternativas. G4 é obrigatório e nunca comprimido (`CON-061`).

### PLB-002 — A ordem dos passos é a substância, não a formalidade **[OBRIGATÓRIA]**

Todo playbook aqui é ordenado do mais interno para o mais externo: **invariante → dado → regra → contrato →
borda → interface → teste → observabilidade**.

Essa ordem existe porque o oposto — começar pela tela ou pelo endpoint — produz um sistema em que a regra
vive na borda (`ARC-020`) e a integridade não existe no banco (`DAT-001`). Começar por fora é como se produz
o modelo anêmico.

### PLB-003 — Pule passo declarando que pulou **[OBRIGATÓRIA]**

Passo irrelevante para a tarefa é `N/A` com uma frase de justificativa. Pular em silêncio é como um passo
esquecido se torna indistinguível de um passo dispensado.

### PLB-004 — Playbook divergente da realidade é achado **[OBRIGATÓRIA]**

Se o passo não se aplica ao projeto por causa de uma convenção local, o achado é a lacuna no
[perfil do projeto](../templates/perfil-do-projeto.md), não uma exceção informal.

---

## Capítulo 15.2 — Playbook: criar um CRUD

O caso mais frequente e o mais frequentemente feito ao contrário. "CRUD" sugere quatro operações
simétricas sobre uma tabela; **é a suposição que produz a maioria dos defeitos** desta tarefa, porque as
quatro operações têm regras, autorizações e invariantes diferentes.

### PLB-005 — Comece pelas invariantes, não pela tabela **[OBRIGATÓRIA]**

Escreva em linguagem de negócio o que precisa ser sempre verdade. Só então desenhe o schema. Ver `ARC-009` e
`DAT-002`.

### PLB-006 — Enumere os estados e as transições válidas **[OBRIGATÓRIA]**

Antes de escrever `update`. Quase nenhuma entidade real aceita "alterar qualquer campo a qualquer momento" —
e `update` genérico é o que permite alterar um pedido pago. Ver `BAK-008`.

### PLB-007 — Modele com as constraints desde a primeira migração **[OBRIGATÓRIA]**

`NOT NULL`, `UNIQUE`, chave estrangeira com comportamento, `CHECK`. Adicionar depois exige lidar com dado que
já viola (`DAT-032`), o que é sempre mais caro.

### PLB-008 — Escreva a regra de negócio antes de qualquer borda **[OBRIGATÓRIA]**

Pura e testável sem banco (`CON-074`, `QAT-024`). Se você não consegue testá-la sem infraestrutura, pare: a
dependência está invertida.

### PLB-009 — Trate as quatro operações como quatro decisões **[OBRIGATÓRIA]**

| Operação | Perguntas que precisam de resposta explícita |
| --- | --- |
| **Criar** | Quem pode? Que campos o cliente **não** pode enviar (`BAK-011`)? É idempotente? Que unicidade se aplica? |
| **Ler** | Autorização por objeto (`SEC-004`)? Filtro de inquilino (`ESC-038`)? Que campos **não** saem (`BAK-033`)? Paginação com limite do servidor (`BAK-032`)? |
| **Atualizar** | Que transições são válidas? Que campos são imutáveis após criar? Como se trata escrita concorrente (`DAT-027`)? Parcial ou total? |
| **Excluir** | Físico ou marcação de inativo (`DAT-011`)? O que acontece com os dependentes? É reversível? Exige confirmação (`UXI-021`)? |

Um endpoint único que faz tudo conforme um parâmetro de ação é antipadrão: impossível autorizar, versionar e
monitorar separadamente.

### PLB-010 — Autorize por objeto em todas as quatro **[OBRIGATÓRIA]** · `S0`

Inclusive na leitura em lote e na exportação (`SEC-008`).

### PLB-011 — Valide no servidor com lista de permitidos e rejeite campo desconhecido **[OBRIGATÓRIA]**

`BAK-009`, `BAK-010`, `BAK-012`.

### PLB-012 — Índice para cada filtro e ordenação que a listagem oferece **[OBRIGATÓRIA]**

Verifique o plano (`DAT-016`). Uma listagem com filtro sem índice funciona na revisão e falha no crescimento.

### PLB-013 — Conte as consultas com 1 e com 50 itens **[OBRIGATÓRIA]**

Antes de considerar pronto. É a medição mais barata que existe (`PRF-008`).

### PLB-014 — Interface com os oito estados **[OBRIGATÓRIA]**

`FRT-001`. Vazio, erro e sem permissão são os esquecidos.

### PLB-015 — Impeça envio duplicado no formulário **[OBRIGATÓRIA]** · `S1`

`UXI-007`.

### PLB-016 — Teste os casos de negócio e os caminhos de erro **[OBRIGATÓRIA]**

Não os getters. Cada invariante de `PLB-005` tem um teste que falha sem a regra (`QAT-004`).

### PLB-017 — Registre a operação sensível **[OBRIGATÓRIA]**

Exclusão e alteração de dado relevante, com quem e o que mudou (`SEC-011`, `DAT-013`).

---

## Capítulo 15.3 — Playbook: criar um endpoint

### PLB-018 — Comece pelo contrato, e pelo que ele **não** expõe **[OBRIGATÓRIA]**

Método, caminho, entrada, saída, códigos de erro. A saída é construída campo por campo, nunca serializando a
entidade (`BAK-033`) — é o que evita vazar a coluna sensível que alguém adicionar no futuro.

### PLB-019 — Método e status corretos desde o início **[OBRIGATÓRIA]**

`BAK-031`. `GET` não altera estado. Erro de entrada nunca é 5xx.

### PLB-020 — Autenticação e autorização antes da lógica **[OBRIGATÓRIA]**

Nasce inacessível até a autorização ser declarada (`SEC-005`).

### PLB-021 — Paginação com limite do servidor desde a primeira versão **[OBRIGATÓRIA]**

Adicionar depois é mudança incompatível (`BAK-032`).

### PLB-022 — Idempotência se houver efeito externo **[OBRIGATÓRIA]**

`BAK-042`. A rede vai falhar e o cliente vai repetir.

### PLB-023 — Limite de taxa e limite de tamanho de entrada **[OBRIGATÓRIA]**

`BAK-035`, `BAK-013`.

### PLB-024 — Formato de erro igual ao do resto da API, com identificador de rastreamento **[OBRIGATÓRIA]**

`BAK-026`.

### PLB-025 — Declare timeout e comportamento em falha de cada chamada externa **[OBRIGATÓRIA]**

`BAK-043`, `BAK-045`.

### PLB-026 — Atualize o contrato declarado e teste o caminho de erro **[OBRIGATÓRIA]**

`BAK-029`, `QAT-019`.

### PLB-027 — Log com contexto correlacionável e métrica de erro **[OBRIGATÓRIA]**

`OPS-013`, `OPS-018`.

---

## Capítulo 15.4 — Playbook: criar uma tela

### PLB-028 — Comece pelo objetivo do usuário e pelo critério de sucesso dele **[OBRIGATÓRIA]**

`UXI-036`. Tela sem objetivo declarado não pode ser avaliada.

### PLB-029 — Liste os oito estados antes de escrever componente **[OBRIGATÓRIA]**

`FRT-001`. Projetar o estado de erro depois é como ele deixa de existir.

### PLB-030 — Use componentes do design system; variante antes de sobreposição **[OBRIGATÓRIA]**

`FRT-022`, `FRT-023`. Se o padrão não existe no sistema, criá-lo lá é parte da tarefa.

### PLB-031 — Nenhum valor literal de cor, espaçamento ou tipografia **[OBRIGATÓRIA]**

`FRT-021`.

### PLB-032 — Nenhuma regra de negócio na tela **[OBRIGATÓRIA]**

`FRT-016`. A tela formata e exibe; não decide.

### PLB-033 — Declare a invalidação de cada mutação **[OBRIGATÓRIA]**

`FRT-009`. Sem isso o usuário vê o valor antigo e repete a ação.

### PLB-034 — Proteja o trabalho do usuário **[OBRIGATÓRIA]** · `S1` em formulário longo

Erro de validação, falha de rede, navegação acidental e sessão expirada não apagam o que foi preenchido
(`UXI-023`).

### PLB-035 — Percorra a tela inteira pelo teclado antes de considerar pronta **[OBRIGATÓRIA]**

Com foco visível (`UXI-044`, `UXI-045`). Leva dois minutos e encontra o que a ferramenta automática não pega.

### PLB-036 — Todo controle com nome acessível; estado comunicado programaticamente **[OBRIGATÓRIA]**

`UXI-049`, `UXI-050`. Placeholder não é rótulo.

### PLB-037 — Reserve espaço para conteúdo assíncrono **[OBRIGATÓRIA]**

`FRT-034`.

### PLB-038 — Verifique em tela pequena e em zoom 200% **[OBRIGATÓRIA]**

`UXI-054`.

### PLB-039 — Percorra os caminhos infelizes na tela real **[OBRIGATÓRIA]**

`UXI-039`. Requisição falhando, 403, sessão expirando no meio do preenchimento.

---

## Capítulo 15.5 — Playbook: alterar o schema

### PLB-040 — Conte os registros que violam a nova regra, primeiro **[OBRIGATÓRIA]**

Antes de escrever a migração. Reporte a contagem (`DAT-032`). É o passo que evita a migração que falha em
produção — ou que "funciona" preenchendo um padrão que corrompe o significado do dado.

### PLB-041 — Aditivo primeiro, sempre **[OBRIGATÓRIA]**

Adicionar coluna anulável ou tabela nova é seguro. Tornar obrigatório, renomear e remover são fases
posteriores (`DAT-031`).

### PLB-042 — Verifique a compatibilidade nos dois sentidos **[OBRIGATÓRIA]**

Durante o rollout, código antigo e novo coexistem (`ARC-027`, `OPS-010`). O código antigo funciona contra o
schema novo?

### PLB-043 — Escreva a reversa e **execute-a** **[OBRIGATÓRIA]**

Em ambiente de teste, com dado (`DAT-030`). Reversa não executada não é reversa.

### PLB-044 — Verifique o risco de bloqueio de tabela na versão em uso **[OBRIGATÓRIA]**

`DAT-033`. O comportamento varia entre versões do banco; não presuma.

### PLB-045 — Migração de dados é `R4` **[OBRIGATÓRIA]**

Backup com restauração testada, aprovação humana prévia, lotes, retomável, contagem antes e depois
(`DAT-034`, `CON-041`).

### PLB-046 — Nunca junte migração destrutiva com mudança de comportamento **[OBRIGATÓRIA]**

`DAT-035`, `OPS-007`. Juntas, o rollback é impossível.

### PLB-047 — Cinco fases, cinco deploys **[OBRIGATÓRIA]**

Adicionar → escrever nos dois → migrar em lotes → ler do novo → remover o antigo. Um deploy por fase, com
confirmação de que nada mais usa o antigo antes de remover.

---

## Capítulo 15.6 — Playbook: integrar um serviço externo

### PLB-048 — Traduza na borda; o modelo do fornecedor não entra no domínio **[OBRIGATÓRIA]**

`ARC-028`, `SEL-031`.

### PLB-049 — Declare timeout, retry, idempotência e comportamento em falha **[OBRIGATÓRIA]**

Os quatro, antes da primeira chamada em produção (`BAK-043`, `BAK-044`, `BAK-045`).

### PLB-050 — Segredo no gerenciador, rotacionável sem deploy **[OBRIGATÓRIA]**

`SEC-052`.

### PLB-051 — Erro do fornecedor mapeado para erro de domínio **[OBRIGATÓRIA]**

Nunca repassado ao cliente (`BAK-027`).

### PLB-052 — Nenhuma chamada externa dentro de transação **[OBRIGATÓRIA]**

Persista a intenção, execute o efeito depois (`BAK-040`).

### PLB-053 — Webhook de entrada: verifique origem, seja idempotente, responda rápido **[OBRIGATÓRIA]**

`BAK-049`, `BAK-050`. Aceite, enfileire, processe fora do ciclo da requisição.

### PLB-054 — Registre a chamada com correlação e monitore a taxa de falha **[OBRIGATÓRIA]**

`OPS-013`, `OPS-018`. Integração sem métrica falha em silêncio.

---

## Capítulo 15.7 — Playbook: corrigir um bug

O playbook mais curto e o mais violado, porque a pressa é maior.

### PLB-055 — Reproduza antes de corrigir **[IMUTÁVEL]**

Sem reprodução você não sabe se corrigiu — sabe apenas que o sintoma não apareceu na sua tentativa. Se não
consegue reproduzir, isso é o achado, e o próximo passo é instrumentar, não editar.

### PLB-056 — Escreva o teste que falha, antes da correção **[OBRIGATÓRIA]**

`QAT-030`. Ele prova a reprodução e impede a reincidência de uma vez.

### PLB-057 — Corrija a classe, não só a instância reportada **[OBRIGATÓRIA]**

Procure os casos irmãos: o mesmo defeito no job, na importação, no admin (`BAK-002`). Correção parcial que
deixa o defeito alcançável não é mudança menor: é incompleta (`CON-016`).

### PLB-058 — Nada de "enquanto eu estava lá" **[IMUTÁVEL]**

O commit de correção contém a correção. Toda melhoria adjacente percebida vai ao backlog (`CON-019`). É o
antipadrão que mais infla diff de correção e o que mais dificulta bissecar a próxima regressão.

Se a reincidência for de um bug já corrigido antes, **o achado é o teste de regressão ausente**, não o código
(`QAT-031`).

---

## Verificação obrigatória de saída

Para qualquer playbook:

```
## Playbook aplicado: <nome>
| Passo | Status | Evidência ou justificativa de N/A |

## Passos pulados
| Passo | Por quê |

## Definition of Done
<checklist de CON-043, item a item>
```
