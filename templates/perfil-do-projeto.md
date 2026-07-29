# Perfil do Projeto — `<nome>`

> **Este arquivo é obrigatório.** O núcleo do EOS é agnóstico de stack; toda decisão técnica depende
> deste perfil. Copie-o para o repositório alvo (sugestão: `.eos/perfil.md` ou `docs/perfil.md`) e
> preencha. Enquanto ele não existir, o primeiro entregável de qualquer agente é propô-lo.
>
> Campos marcados `<preencher>` são placeholders. Um campo em branco é uma pergunta aberta, não um
> detalhe.

Última atualização: `<data>` · Responsável: `<nome>`

---

## 1. O produto

| Campo | Valor |
| --- | --- |
| O que é | `<uma frase>` |
| Quem usa | `<perfil de usuário>` |
| Escala atual | `<usuários ativos, requisições/dia, volume de dados>` |
| Escala projetada em 12 meses | `<preencher>` |
| O que mais dói se falhar | `<o fluxo cuja falha causa maior dano>` |
| Custo de indisponibilidade | `<qualitativo ou financeiro>` |

## 2. Stack

| Camada | Tecnologia e versão |
| --- | --- |
| Linguagem(ns) | `<preencher>` |
| Frontend | `<preencher>` |
| Backend | `<preencher>` |
| Mobile | `<preencher>` |
| Banco de dados | `<preencher>` |
| Cache | `<preencher>` |
| Fila / eventos | `<preencher>` |
| Autenticação | `<preencher>` |
| Hospedagem | `<preencher>` |
| CI/CD | `<preencher>` |
| Observabilidade | `<preencher>` |
| Pagamentos | `<preencher>` |

## 3. Comandos

Preencha com os comandos reais. Um agente sem estes comandos não pode validar nada — e uma mudança
não validada não existe.

```bash
Instalar:            <preencher>
Rodar local:         <preencher>
Testes (todos):      <preencher>
Testes (arquivo):    <preencher>
Verificação de tipos:<preencher>
Lint:                <preencher>
Formatar:            <preencher>
Build:               <preencher>
Migração (aplicar):  <preencher>
Migração (reverter): <preencher>
Deploy:              <preencher>
Rollback:            <preencher>
```

## 4. Convenções do projeto

| Item | Convenção |
| --- | --- |
| Caixa em código | `<camelCase | snake_case | ...>` |
| Caixa no banco | `<preencher>` |
| Caixa na API | `<preencher>` |
| Nomes de arquivo | `<preencher>` |
| Organização de pastas | `<por domínio | por camada>` |
| Idioma do código | `<inglês | português>` |
| Idioma da interface | `<preencher>` |
| Formato de commit | `<preencher>` |
| Estratégia de branch | `<preencher>` |

**Idioma do código e do domínio:** escolha um e mantenha. Metade em inglês e metade em português é a
principal causa de vocabulário divergente.

## 5. Glossário do domínio

Um conceito, um nome, em todo lugar. Termo novo é decisão, não improviso.

| Conceito | Nome no código | Nome no banco | Nome na API | Nome na interface | Definição |
| --- | --- | --- | --- | --- | --- |
| `<preencher>` | | | | | |

## 6. Classificação dos módulos

Define o nível de exigência de cada parte. Perseguir excelência em módulo periférico é erro de
priorização.

| Módulo | Nível | Exigência |
| --- | --- | --- |
| `<preencher>` | `crítico` | [DoE](../manual/09-definition-of-excellence.md) exigida |
| `<preencher>` | `padrão` | [DoD](../manual/08-definition-of-done.md) suficiente |
| `<preencher>` | `periférico` | DoD reduzida |

Módulos com previsão de substituição em menos de 3 meses: `<preencher>` — o impacto de
manutenibilidade neles cai para 1 na priorização.

## 7. Limiares

Confirme ou ajuste os padrões de [métricas](../manual/10-metricas-de-qualidade.md). Valor em branco
significa que o padrão do EOS vale.

| Métrica | Limiar deste projeto |
| --- | --- |
| API p95 | `<300 ms>` |
| Consulta p95 | `<100 ms>` |
| LCP / INP / CLS | `<2,5 s / 200 ms / 0,1>` |
| Bundle inicial | `<250 KB comprimido>` |
| Cobertura de linhas (indicador) | `<60%>` |
| Tempo da suíte relevante | `<5 min>` |
| Taxa de erro aceitável | `<0,5%>` |
| MTTD / MTTR | `<5 min / 30 min>` |

## 8. Restrições e tolerância a risco

| Campo | Valor |
| --- | --- |
| Janela de deploy | `<livre | horários específicos>` |
| Indisponibilidade tolerada | `<zero | n minutos com aviso>` |
| Clientes que não controlamos | `<app móvel, integrações — e qual a versão mais antiga suportada>` |
| Requisitos regulatórios | `<LGPD, PCI, outros>` |
| Dado pessoal tratado | `<quais categorias>` |
| Quem aceita risco `R4` | `<nome>` |
| Quem aprova ADR | `<nome>` |

## 9. Dívida conhecida

Registro honesto do que já se sabe. Isso evita que cada revisão redescubra o mesmo.

| ID | O quê | Por que ainda existe | Gatilho de reavaliação |
| --- | --- | --- | --- |
| `<preencher>` | | | |

## 10. Divergências deliberadas das normas

Onde este projeto rompe uma norma do EOS de propósito, com ADR.

| Norma | Divergência | Motivo | ADR |
| --- | --- | --- | --- |
| `<preencher>` | | | |

## 11. Armadilhas conhecidas

Coisas que fazem alguém novo (humano ou agente) errar. Este é o campo de maior retorno do documento.

- `<ex.: a tabela pedidos_legado ainda recebe escrita do job de integração>`
- `<ex.: o ambiente de homologação usa outro provedor de pagamento>`
- `<ex.: migrações não rodam automaticamente no deploy>`

---

## Perguntas abertas

| Pergunta | Bloqueia | Quem responde |
| --- | --- | --- |
| `<preencher>` | | |
