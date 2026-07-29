# Checklist — Performance

Regra que governa este checklist: **sem número, não há achado.** Item não medido é reportado como
hipótese, com o método que o verificaria.

Norma: [`standards/performance.md`](../standards/performance.md) ·
Limiares: [`manual/10-metricas-de-qualidade.md`](../manual/10-metricas-de-qualidade.md).

---

## 0. Método — antes de qualquer coisa

- [ ] Declarei: ambiente, volume de dados, número de execuções, percentil, ferramenta.
- [ ] Uso p95, não média.
- [ ] O volume de dados é representativo da produção, atual **e** projetado.
- [ ] Tenho a medição **antes** da mudança.

Medição sem método declarado não é evidência.

---

## 1. Acesso a dados — quase sempre o gargalo

- [ ] Contei as consultas de uma requisição com 1 item e com 50. O número cresce? → N+1.
- [ ] Toda coluna de filtro, junção e ordenação frequente tem índice.
- [ ] **Verifiquei o plano de execução**, não presumi o uso do índice.
- [ ] Ordem das colunas do índice composto corresponde às consultas reais.
- [ ] Nenhum índice não utilizado (custo de escrita sem retorno).
- [ ] Nenhuma consulta em caminho de requisição sem limite.
- [ ] Nenhum `SELECT *` em tabela larga.
- [ ] Nenhuma consulta dentro de laço.
- [ ] Agregação feita no banco, não na aplicação.
- [ ] Nenhuma transação longa causando contenção.

## 2. Rede e integrações

- [ ] Chamadas independentes são paralelas, não sequenciais.
- [ ] **Toda** chamada externa tem timeout. Ausência é `S2`, ou `S1` em caminho crítico.
- [ ] Retry com espera crescente e limite, e só onde a operação é idempotente.
- [ ] Nenhuma chamada repetida para dado estável sem cache.
- [ ] Carga útil enviada e recebida contém só o necessário.
- [ ] Conexões reutilizadas.

## 3. Trabalho repetido

- [ ] Nenhuma recomputação de valor estável na mesma requisição.
- [ ] Nenhuma serialização/desserialização redundante.
- [ ] Cache presente onde o dado é caro e estável.

## 4. Cache — se existe, responda tudo

- [ ] Está declarado: **o que** é cacheado, **por quanto tempo**, **como é invalidado**, e **o que
      acontece se servir dado velho**.
- [ ] A chave inclui usuário, permissão, tenant, idioma e moeda quando a resposta depende deles.
      **Servir dado de um usuário para outro é `S0`** — a falha de cache mais comum.
- [ ] Invalidação após mutação está definida para cada consulta afetada.
- [ ] O cache não está escondendo um N+1 em vez de corrigi-lo.

## 5. Carga útil e ativos

- [ ] Resposta sem campos que ninguém usa.
- [ ] Imagens: formato moderno, dimensão adequada, compressão, carregamento tardio.
- [ ] Compressão habilitada nas respostas.
- [ ] Bundle dentro do orçamento declarado, verificado no pipeline.
- [ ] Nenhuma biblioteca inteira importada para uma função (`S2`).
- [ ] Divisão de código por rota.

## 6. Renderização e interface

- [ ] Nenhum re-render desnecessário por identidade instável de referência.
- [ ] Lista longa virtualizada.
- [ ] Nenhum trabalho pesado bloqueando a thread principal.
- [ ] Espaço reservado para conteúdo assíncrono — deslocamento de layout causa erro de clique.
- [ ] Animação em propriedade que não força recálculo de layout.
- [ ] Fonte não bloqueia a primeira pintura.

## 7. Algoritmo

- [ ] Complexidade adequada ao volume real.
- [ ] Nenhuma busca linear repetida onde um índice em memória resolveria.
- [ ] Estrutura de dados adequada ao padrão de acesso.

## 8. Concorrência e resiliência

- [ ] Paralelismo com limite — sem limite, exaure conexões e derruba a dependência.
- [ ] Degradação definida: falha em recurso secundário não impede o fluxo principal.
- [ ] Trabalho em volume processado em lotes, retomável.

---

## Limiares (confirmar no perfil do projeto)

| Métrica | Limiar padrão |
| --- | --- |
| API p95 | < 300 ms |
| Consulta p95 | < 100 ms |
| Consultas por requisição | constante em relação ao resultado |
| LCP | < 2,5 s |
| INP | < 200 ms |
| CLS | < 0,1 |
| Bundle inicial | < 250 KB comprimido |
| Regressão entre versões | > 20% bloqueia |

---

## Registro obrigatório da correção

```
Métrica: <qual>
Antes:   <n>  (n=<execuções>, <volume>, <ambiente>)
Depois:  <n>  (mesmo método)
Causa:   <o que era>
Correção: <o que foi feito>
Risco:   <e como está coberto>
```

- [ ] O ganho está acima da variação da medição. Se está dentro do ruído, **não houve ganho** — e a
      complexidade adicionada é prejuízo líquido.
- [ ] Existe verificação automática que falha se o limiar regredir.
