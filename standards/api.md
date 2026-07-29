# Norma — API

Vale para HTTP/REST, GraphQL, RPC e eventos, com adaptações óbvias. O princípio comum: **a API é
um contrato**, e contrato quebrado em silêncio é o defeito mais caro que existe, porque quem paga
é o consumidor.

---

## Contrato

### P1. Explícito e versionado **[OBRIGATÓRIA]**

O contrato é declarado (OpenAPI, schema GraphQL, tipos compartilhados), versionado, e é a fonte de
verdade. Documentação escrita à mão que divirja do comportamento real é pior do que nenhuma.

### P2. Mudança incompatível exige versão **[OBRIGATÓRIA]**

São incompatíveis: remover ou renomear campo; tornar campo opcional em obrigatório; mudar tipo;
mudar significado; restringir valores aceitos; mudar código de status; mudar semântica de erro.

São compatíveis: adicionar campo opcional na entrada; adicionar campo na saída (se os
consumidores toleram campos extras); adicionar endpoint.

Com cliente que você não controla (app móvel, integração de terceiro), **não existe** mudança
incompatível sem período de convivência. Deploy não atualiza o app do usuário.

### P3. Padrão de nomes consistente **[OBRIGATÓRIA]**

Escolha uma convenção no [perfil do projeto](../templates/perfil-do-projeto.md) e aplique em toda
a superfície. Duas convenções na mesma API forçam todo consumidor a manter um mapa mental de
exceções.

### P4. Coleções são paginadas **[OBRIGATÓRIA]**

Toda listagem tem paginação com **limite máximo imposto pelo servidor**. Endpoint que retorna
"todos" é um incidente esperando volume de dados. Prefira cursor a offset quando os dados mudam
durante a navegação.

Resposta de coleção inclui o mecanismo de continuação, nunca apenas o array cru — adicionar
paginação depois é mudança incompatível.

---

## Semântica

### P5. Métodos e status corretos **[OBRIGATÓRIA]**

`GET` não altera estado, nunca. `PUT` e `DELETE` são idempotentes.

| Status | Uso |
| --- | --- |
| 200 / 201 / 204 | Sucesso, com corpo / criado / sem corpo |
| 400 | Entrada malformada ou inválida |
| 401 | Não autenticado |
| 403 | Autenticado, sem permissão |
| 404 | Não existe — **ou existe e você não pode saber** |
| 409 | Conflito de estado (versão, duplicata) |
| 422 | Sintaxe válida, regra de negócio violada |
| 429 | Limite de taxa |
| 5xx | Falha nossa. Nunca use 5xx para erro de entrada |

Devolver 200 com `{"erro": ...}` no corpo é violação: quebra todo cliente que confia no status.

### P6. Erros estruturados e acionáveis **[OBRIGATÓRIA]**

Um formato único de erro em toda a API:

```json
{
  "code": "ESTOQUE_INSUFICIENTE",
  "message": "Restam 2 unidades de SKU-1234.",
  "details": [{ "field": "itens[0].quantidade", "issue": "max", "max": 2 }],
  "traceId": "01HF3..."
}
```

- `code` é estável e legível por máquina — clientes não devem parsear `message`.
- `message` é acionável e sem detalhe interno.
- `traceId` correlaciona com o log do servidor. É o que permite suporte útil.
- Nunca inclua stack trace, SQL, caminho de arquivo ou nome de tabela.

### P7. Escrita idempotente onde importa **[OBRIGATÓRIA]**

Operação que cria efeito externo (cobrança, envio, emissão) aceita chave de idempotência. Rede
falha, cliente repete, e cobrar duas vezes é `S0`.

### P8. Validação no servidor, sempre **[OBRIGATÓRIA]**

Validação no cliente é experiência do usuário; validação no servidor é correção. Rejeite campos
desconhecidos em vez de ignorá-los: campo ignorado silenciosamente esconde bug de integração por
meses.

---

## Segurança

### P9. Autorização por objeto **[OBRIGATÓRIA]**

Verificar o papel do usuário não basta. Verifique se **este** usuário pode acessar **este**
recurso. A falha mais comum e mais grave em APIs é `GET /pedidos/{id}` que só checa autenticação.

Padrão obrigatório: negar por omissão. Rota nova é inacessível até que a autorização seja
declarada.

### P10. Não exponha o que não precisa **[OBRIGATÓRIA]**

Resposta contém o necessário para o caso de uso. Serializar a entidade inteira vaza campos
internos hoje e no futuro — quando alguém adicionar uma coluna sensível, ela aparece na API sem
que ninguém perceba.

### P11. Limite de taxa e de tamanho **[OBRIGATÓRIA]**

Toda API pública tem limite de taxa e de tamanho de corpo. Ausência é vetor de indisponibilidade
trivialmente explorável.

### P12. Enumeração protegida **[RECOMENDADA]**

Identificador sequencial permite enumerar seus dados e inferir volume de negócio. Prefira
identificador não sequencial em recurso exposto.

---

## Evolução e operação

### P13. Deprecação anunciada **[OBRIGATÓRIA]**

Campo ou endpoint a ser removido: marque como deprecado no contrato, comunique, meça o uso real,
e só remova quando o uso chegar a zero ou o prazo acordado vencer. Remover porque "parece que
ninguém usa" é `S1`.

### P14. Compatibilidade durante o deploy **[OBRIGATÓRIA]**

Durante o deploy, versões antiga e nova coexistem. Toda mudança precisa funcionar nos dois
sentidos, o que implica migrações em duas fases: primeiro aditivo, depois remoção.

### P15. Observabilidade por endpoint **[RECOMENDADA]**

Latência, taxa de erro e volume por endpoint. Sem isso, "a API está lenta" é impossível de
investigar.

---

## Eventos e mensagens

### P16. Evento é fato, no passado **[RECOMENDADA]**

`PedidoPago`, não `PagarPedido`. Evento descreve o que aconteceu; comando pede que aconteça.
Confundir os dois produz acoplamento entre produtor e consumidor.

### P17. Consumidor idempotente **[OBRIGATÓRIA]**

Toda entrega pode ocorrer mais de uma vez. Consumidor que não é idempotente vai duplicar efeito —
não é uma questão de se, mas de quando.

### P18. Evento versionado e autocontido **[OBRIGATÓRIA]**

O evento carrega o que o consumidor precisa, tem versão de schema, e não depende do estado atual
da origem (que pode ter mudado desde a emissão).

### P19. Falha tratada **[OBRIGATÓRIA]**

Defina: número de tentativas, espera entre elas, e destino final da mensagem que não pode ser
processada (fila morta). Mensagem perdida em silêncio é perda de dado.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Endpoint que faz tudo conforme um parâmetro `acao` | Impossível autorizar, versionar e monitorar |
| 200 com erro no corpo | Quebra todo cliente e todo monitoramento |
| Retornar entidade do banco diretamente | Vaza campo interno no futuro |
| Listagem sem limite | Incidente proporcional ao crescimento |
| Erro genérico "algo deu errado" | Suporte impossível |
| Verbo na URL (`/criarPedido`) | Perde a semântica de método e cache |
| Mudança silenciosa de significado de campo | O pior tipo de quebra: os testes passam |
