# Norma — Arquitetura

Cada regra é marcada como **[OBRIGATÓRIA]** (violação é achado, mínimo `S2`) ou
**[RECOMENDADA]** (divergência exige justificativa, não bloqueia).

---

## A1. Direção das dependências **[OBRIGATÓRIA]**

O domínio não conhece a infraestrutura. Dependências apontam para dentro.

```
UI / API / CLI  ──▶  Aplicação (casos de uso)  ──▶  Domínio (regras)
                              │
                              ▼
                     Infraestrutura (banco, HTTP, fila, SDK)
                     — implementa interfaces definidas pelo domínio
```

Violações concretas: entidade de domínio importando o ORM; regra de negócio recebendo objeto de
requisição HTTP; domínio chamando SDK de fornecedor diretamente.

**Teste da regra:** é possível testar a regra de negócio sem banco, sem rede e sem framework? Se
não, a dependência está invertida.

## A2. Zero dependências circulares **[OBRIGATÓRIA]**

Ciclo entre módulos é `S2` estrutural. Ele significa que as duas partes são, na prática, um
módulo só — e que nenhuma pode ser entendida, testada ou substituída isoladamente.

Correções, em ordem de preferência: mover o conceito compartilhado para um terceiro módulo;
inverter a dependência com uma interface; emitir um evento em vez de chamar.

## A3. Interface pública explícita **[OBRIGATÓRIA]**

Todo módulo declara o que expõe. O resto é inacessível de fora.

- Um ponto de entrada por módulo (`index`, `api`, ou equivalente na linguagem).
- Import que alcança arquivo interno de outro módulo é violação.
- O que é público é contrato: mudá-lo exige avaliar os chamadores.

## A4. Regra de negócio fora das bordas **[OBRIGATÓRIA]**

Controllers, handlers, componentes de UI e jobs **orquestram**; não decidem.

Sinais de violação: cálculo de preço, desconto, imposto ou frete em controller; condicional de
permissão em componente visual; validação de invariante de domínio em rota HTTP.

Bordas podem: validar formato, autenticar, traduzir formato, chamar caso de uso, mapear erro
para resposta.

## A5. Uma fonte de verdade por decisão **[OBRIGATÓRIA]**

Cada regra de negócio tem **uma** implementação. Duas implementações da mesma regra é `S2`,
mesmo que estejam idênticas hoje: o defeito é a divergência futura, que é inevitável.

Aplica-se a: cálculo, validação, transição de estado, autorização e formatação com significado
de negócio.

## A6. Fronteiras alinhadas ao domínio **[RECOMENDADA]**

Organize por capacidade de negócio (`pedidos/`, `catalogo/`, `pagamentos/`), não por tipo
técnico (`controllers/`, `services/`, `models/`).

Critério: uma mudança de requisito típica deve tocar **um** diretório. Se toca cinco, a
organização está por camada técnica e o custo de cada mudança é multiplicado.

## A7. Sem abstração especulativa **[OBRIGATÓRIA]**

Interface com uma única implementação, sem necessidade de teste ou de troca real, é abstração
especulativa e deve ser rejeitada.

Abstraia quando: existem duas implementações reais; é fronteira de teste necessária; é fronteira
de fornecedor que se pretende trocar. Nunca "porque pode ser útil depois".

## A8. Estado compartilhado explícito **[OBRIGATÓRIA]**

Estado mutável global, singleton com estado e cache implícito precisam ser declarados e
justificados. Cada um é um ponto de acoplamento invisível e uma fonte de teste intermitente.

## A9. Falha nas fronteiras **[OBRIGATÓRIA]**

Toda chamada externa (rede, banco, fornecedor, fila) declara: timeout, comportamento em falha e
se pode ser repetida com segurança.

- Timeout ausente é `S2` — em caso de dependência crítica, `S1`.
- Retry sem idempotência é `S1`: duplica efeito.
- Falha silenciosa (`catch` vazio ou que só registra log) é `S2`.

## A10. Contratos versionados **[OBRIGATÓRIA]**

Mudança incompatível em contrato consumido por outro sistema ou por cliente que você não
controla (app móvel, integração) exige versionamento ou período de compatibilidade. Não existe
"deploy simultâneo" com app instalado no dispositivo do usuário.

## A11. Configuração fora do código **[OBRIGATÓRIA]**

Endpoint, credencial, limite, flag e tudo que varia por ambiente vem de configuração validada na
inicialização. Falhar no start com mensagem clara é melhor do que falhar na primeira requisição.

## A12. Documente o mapa, não o código **[RECOMENDADA]**

Um diagrama de uma página com módulos, responsabilidades e dependências. Atualizado quando a
fronteira muda — não a cada commit. Documentação de arquitetura que não corresponde à realidade
é pior do que ausência de documentação.

---

## Antipadrões

| Antipadrão | Sinal | Consequência |
| --- | --- | --- |
| **Módulo Deus** | Arquivo tocado por mais de 60% das mudanças | Todo trabalho serializa nele |
| **Modelo anêmico** | Entidades só com dados, regras espalhadas em serviços | Invariantes não são garantidas |
| **Vazamento de ORM** | Entidade do ORM circulando por toda a aplicação | Impossível mudar persistência; carregamento acidental |
| **Camada de passagem** | Serviço que só repassa para o repositório | Custo sem benefício |
| **Nano-serviço** | Serviço separado que sempre muda junto com outro | Complexidade distribuída sem autonomia |
| **Ciclo disfarçado** | Módulo A importa B, B importa A via um terceiro | Mesmo problema, mais difícil de ver |
| **Configuração no código** | `if (ambiente === 'prod')` espalhado | Comportamento imprevisível por ambiente |
| **Data-driven demais** | Regra de negócio em tabela de configuração sem validação | Estado inválido sem trava |

---

## Quando romper a norma

Rompa quando o custo de cumprir excede o benefício **neste** contexto — e registre em
[ADR](../templates/adr.md) com: qual regra, por quê, qual o risco aceito, e o que faria reverter.

Divergência registrada é decisão. Divergência silenciosa é erosão: em seis meses ninguém sabe
qual é a regra real, e a norma deixa de existir.
