# Auditoria — `<módulo | PR | rodada>` — `<AAAA-MM-DD>`

# Veredito: `APPROVED` \| `APPROVED WITH CONDITIONS` \| `REJECTED`

`<uma frase dizendo por quê>`

| Campo | Valor |
| --- | --- |
| Auditor | `<nome/papel — não participou da implementação>` |
| Escopo auditado | `<mudanças, commits, PRs>` |
| Camadas cobertas | `<quais>` |
| Camadas **não** cobertas | `<quais — risco conhecido>` |

---

## 1. Verificação das afirmações

Toda validação declarada é tratada como não verificada até a evidência aparecer.

| Mudança | Validação declarada | Evidência encontrada | Veredito |
| --- | --- | --- | --- |
| `<ID>` | | | `confirmada` \| `não confirmada` |

Executado pelo auditor:

```
<comando> → <resultado>
```

## 2. Notas

| Dimensão | Peso | Nota | Justificativa em uma linha |
| --- | --- | --- | --- |
| Segurança | 20% | | |
| Correção de domínio | 20% | | |
| Dados e integridade | 15% | | |
| Testes | 15% | | |
| Arquitetura | 10% | | |
| Performance | 8% | | |
| UX e acessibilidade | 7% | | |
| Observabilidade e entrega | 5% | | |
| **Total ponderado** | 100% | | |

Calibragem: 10 exige [DoE](../volumes/vol-01-constituicao.md) na dimensão. Ausência de
problemas dá no máximo 8 — e módulo sem testes, sem observabilidade e sem decisões registradas fica em
torno de 5, porque não se sabe se funciona.

Travas aplicadas: `<nenhuma | S0 presente | S1 não corrigido | segurança < 6>`

## 3. Regressões detectadas

| ID | O que regrediu | Evidência | Introduzido por | Severidade |
| --- | --- | --- | --- | --- |

Fontes verificadas:

- [ ] Interação entre mudanças
- [ ] Código compartilhado com outros chamadores
- [ ] Deriva de contrato (servidor vs cliente)
- [ ] Janela de deploy (código antigo e novo coexistindo)
- [ ] Dado existente contra a regra nova
- [ ] Formato em cache
- [ ] Mensagens em trânsito
- [ ] Clientes antigos
- [ ] Mudança silenciosa (padrão, ordem, arredondamento, fuso, código de erro)
- [ ] **Teste afrouxado** — revisei cada teste alterado
- [ ] Nova intermitência

## 4. Integridade do escopo

| Arquivo | Proposta que o aprovou | Veredito |
| --- | --- | --- |

Escopo não aprovado encontrado: `<nenhum | lista>`

## 5. Revisão dos testes alterados

| Teste | Asserção afrouxada? | Justificado? |
| --- | --- | --- |

Asserção alterada para acomodar a mudança, sem confirmação de que o novo comportamento é correto, é
`S1`.

## 6. Definition of Done

| Mudança | Itens não atendidos | `N/A` justificados |
| --- | --- | --- |

## 7. Severidades em aberto

| ID | Severidade | Descrição | Status |
| --- | --- | --- | --- |

`S0`: `<n>` · `S1` não corrigido: `<n>` · `S2` registrado: `<n>`

## 8. Verificação do backlog

| Item | Valor |
| --- | --- |
| Oportunidades reportadas | `<n>` |
| Registradas no backlog | `<n>` |
| Faltando | `<lista>` |

Achado que só existe no relatório é trabalho de diagnóstico jogado fora.

## 9. Condições para aprovação

Preencher apenas em `APPROVED WITH CONDITIONS`. Cada condição precisa ser trivialmente verificável.

1. `<condição>` — verificável por: `<como>`

## 10. Risco residual

| Risco | Severidade | Monitoramento | Aceito por (nome) |
| --- | --- | --- | --- |

Aceitação de risco exige: nome de quem aceita, registro, e monitoramento que revelaria a
materialização. Risco `R4` só o dono humano aceita.

## 11. Recomendação para a próxima rodada

O item de maior valor a atacar em seguida, com o motivo.

> `<preencher>`
