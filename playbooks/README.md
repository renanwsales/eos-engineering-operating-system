# playbooks — índice das tarefas recorrentes

Este diretório é um **índice**, não uma cópia. O conteúdo dos playbooks vive no
[Volume 21](../21-playbooks.md), onde cada passo é uma regra numerada e citável (`PLB-001` em diante). Duplicar
aqui criaria duas fontes de verdade para a mesma sequência, que divergiriam na primeira alteração (`A-001`).

Um playbook é a trilha do portão G3 — implementação. Ele não substitui os portões anteriores: você ainda
precisa saber o que existe, ter um achado ou requisito, e ter decidido entre alternativas (`PLB-001`). E G4,
validação, nunca é comprimido (`CON-061`).

---

## Os playbooks

| Tarefa | Onde | Regras | Passo que mais se erra |
| --- | --- | --- | --- |
| **Criar um CRUD** | [Volume 21, cap. 15.2](../21-playbooks.md) | `PLB-005` a `PLB-017` | Tratar as quatro operações como simétricas. Elas têm regras, autorizações e invariantes diferentes (`PLB-009`) |
| **Criar um endpoint** | [Volume 21, cap. 15.3](../21-playbooks.md) | `PLB-018` a `PLB-027` | Serializar a entidade em vez de construir a saída campo por campo (`PLB-018`) |
| **Criar uma tela** | [Volume 21, cap. 15.4](../21-playbooks.md) | `PLB-028` a `PLB-039` | Deixar o estado de erro para depois — é assim que ele deixa de existir (`PLB-029`) |
| **Alterar o schema** | [Volume 21, cap. 15.5](../21-playbooks.md) | `PLB-040` a `PLB-047` | Escrever a migração antes de contar quantos registros violam a nova regra (`PLB-040`) |
| **Integrar serviço externo** | [Volume 21, cap. 15.6](../21-playbooks.md) | `PLB-048` a `PLB-054` | Chamar sem declarar timeout, retry, idempotência e comportamento em falha (`PLB-049`) |
| **Corrigir um bug** | [Volume 21, cap. 15.7](../21-playbooks.md) | `PLB-055` a `PLB-058` | "Enquanto eu estava lá" — melhoria adjacente no commit de correção (`PLB-058`) |

---

## A ordem que todos compartilham

```
invariante → dado → regra → contrato → borda → interface → teste → observabilidade
```

Do mais interno para o mais externo (`PLB-002`). Começar pela tela ou pelo endpoint é como se produz o modelo
anêmico: a regra acaba na borda (`ARC-020`) e a integridade não existe no banco (`DAT-001`).

---

## Como usar

1. Identifique a tarefa na tabela acima e abra o capítulo correspondente.
2. Percorra os passos **na ordem**. A ordem é a substância, não a formalidade.
3. Passo irrelevante recebe `N/A` com uma frase de justificativa. Pular em silêncio torna o passo esquecido
   indistinguível do passo dispensado (`PLB-003`).
4. Feche com a Definition of Done (`CON-043`) e o bloco de verificação de saída do Volume 21.

Se um passo não se aplica ao projeto por causa de uma convenção local, o achado é a lacuna no
[perfil do projeto](../templates/perfil-do-projeto.md), não uma exceção informal (`PLB-004`).

---

## Playbook novo

Um playbook entra no Volume 21 quando a tarefa se repete e a ordem dos passos tem consequência. Escreva-o lá,
com regras numeradas no fim da faixa `PLB` (`A-007`), e adicione a linha na tabela acima.

Candidatos ainda não escritos, em ordem de utilidade: criar um relatório ou exportação · adicionar um campo a
uma entidade existente · migrar de um fornecedor externo para outro · instrumentar um fluxo existente ·
promover um módulo de `V2` para `V3` de verificação de segurança (`SEC-059`).
