# 09 — Definition of Excellence

A [Definition of Done](08-definition-of-done.md) é o piso. Esta é o teto: o que caracteriza um
módulo maduro, no qual a próxima pessoa muda coisas com confiança.

**Excelência é opcional e deliberada.** Não se exige DoE de todo módulo — exige-se dos módulos
que sustentam o negócio. Perseguir excelência em código periférico é desperdício, e o EOS
considera isso um erro de priorização, não uma virtude.

Nenhum módulo recebe nota 10 na auditoria sem atender a DoE. Ausência de problemas dá, no
máximo, 8.

---

## 1. O domínio é impossível de usar errado

Não é "validado". É **estruturalmente impossível**.

- Estados inválidos não são representáveis pelos tipos ou pelo schema — não apenas rejeitados
  em tempo de execução.
- Invariantes são garantidas no ponto mais interno possível (tipo > constraint de banco >
  validação de aplicação > validação de cliente).
- Conceitos do domínio têm tipos próprios: dinheiro, identificador, quantidade, e-mail e
  período não são `string`, `number` ou `float`.
- O vocabulário é idêntico em código, banco, API e interface. Um conceito, um nome, sempre.
- Operações que não podem ser repetidas são idempotentes por construção.

## 2. As fronteiras são visíveis e respeitadas

- Cada módulo tem uma interface pública explícita, e o que é interno é inacessível.
- O domínio não conhece infraestrutura: sem import de framework, ORM, HTTP ou SDK dentro dele.
- Dependências apontam para dentro; não existe ciclo.
- Uma mudança de requisito de negócio típica toca **um** módulo.
- É possível descrever o sistema em um diagrama de uma página que corresponde à realidade.
- Trocar um fornecedor externo (pagamento, e-mail, armazenamento) é uma mudança local.

## 3. Os testes são um ativo, não um imposto

- Toda regra de negócio tem teste; nenhum teste depende de detalhe de implementação.
- A suíte é determinística: mesma entrada, mesmo resultado, em qualquer ordem, sempre.
- A suíte relevante roda rápido o suficiente para ser executada a cada mudança.
- Casos de borda são testados por propriedade ou por tabela, não por exemplos avulsos.
- Todo bug histórico tem um teste com o nome do defeito.
- Falha de teste aponta a causa: a mensagem diz o que se esperava e o que ocorreu, no
  vocabulário do domínio.
- Existe pelo menos um teste do caminho crítico ponta a ponta.

## 4. A segurança é o comportamento padrão

- Negar é o padrão: um endpoint novo é inacessível até que a autorização seja declarada.
- Autorização é centralizada e obrigatória por construção, não repetida em cada handler.
- Segredos vêm de um gerenciador, com rotação possível sem deploy.
- Dado pessoal tem inventário: onde está, por quanto tempo, quem acessa.
- Log é seguro por padrão: campos sensíveis são mascarados no ponto de escrita.
- Dependências são verificadas automaticamente no pipeline, e a atualização é rotina.
- Existe registro de auditoria para operações sensíveis.

## 5. A performance é conhecida, não esperada

- Existem limiares declarados por operação crítica (ver [métricas](10-metricas-de-qualidade.md)).
- Os números atuais são medidos e registrados, com data e método.
- Existe proteção estrutural contra N+1, não vigilância manual em revisão.
- Toda listagem é paginada com limite máximo imposto pelo servidor.
- Existe teste ou verificação automática que falha quando um limiar regride.
- O comportamento sob carga real é conhecido, não inferido.

## 6. A experiência é consistente e previsível

- Todos os estados de toda tela são projetados: carregando, vazio, erro, parcial, offline, sem
  permissão, primeira vez.
- O mesmo tipo de ação se comporta igual em todo o produto.
- Erros são acionáveis e escritos no vocabulário do usuário.
- Nenhum caminho perde trabalho do usuário.
- Toda tarefa é completável por teclado e por leitor de tela.
- Conformidade com WCAG 2.2 AA verificada, não presumida.
- A percepção de velocidade é cuidada: feedback imediato, atualização otimista onde é seguro.

## 7. A operação é entediante

- Deploy é rotina, frequente e não requer coordenação humana.
- Rollback é um comando, testado, e conhecido por qualquer pessoa do time.
- Existe um painel que responde "está tudo bem?" em dez segundos.
- Alertas são acionáveis, e a taxa de falso positivo é baixa o suficiente para que sejam lidos.
- Cada alerta tem runbook.
- Log tem correlação ponta a ponta por id de requisição.
- Restauração de backup é testada em calendário, não presumida.
- Configuração é declarada, versionada e igual entre ambientes exceto por diferenças
  documentadas.

## 8. O conhecimento não vive nas pessoas

- Uma pessoa nova produz uma mudança útil no primeiro dia.
- Decisões relevantes têm ADR com alternativas e condição de invalidação.
- Não existe área que "só uma pessoa entende".
- O README responde: o que é, como rodar, como testar, como fazer deploy, onde olhar quando
  quebra.
- O backlog é honesto: a dívida conhecida está escrita, com custo estimado.

---

## Como usar sem cair em perfeccionismo

1. **Escolha o nível por módulo.** Marque no [perfil do projeto](../templates/perfil-do-projeto.md)
   quais módulos são `crítico` (DoE exigida), `padrão` (DoD suficiente) ou `periférico` (DoD
   reduzida).
2. **Meça a distância, não a perfeição.** Na auditoria, cada dimensão recebe nota de 0 a 10; a
   DoE define o que é 10. Saber que segurança está em 6 é mais útil do que exigir 10.
3. **Trate a lacuna como backlog, não como bloqueio.** Item de DoE não atendido é
   `OPPORTUNITY`, exceto quando coincide com `S0`/`S1`.
4. **Suba um degrau por rodada.** A meta razoável é +1 na dimensão mais fraca, não 10 em tudo.

---

## O critério único

> Excelência é quando a próxima mudança é **mais fácil** do que a anterior.

Se cada entrega deixa o módulo mais difícil de mudar, não há excelência — há acúmulo, mesmo
que todos os testes estejam verdes.
