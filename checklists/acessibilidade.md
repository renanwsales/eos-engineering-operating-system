# Checklist — Acessibilidade (WCAG 2.2 AA)

Ferramenta automática detecta cerca de um terço dos problemas reais. **Verificação automática sozinha
não aprova nada.** Os blocos de teclado e leitor de tela são manuais e obrigatórios.

Norma: [Volume 8 — UX/UI](../volumes/vol-08-ux-ui.md).

---

## 1. Automático — o piso

- [ ] axe (ou equivalente) roda no pipeline e **bloqueia**.
- [ ] Zero erros na tela alterada.
- [ ] Contraste verificado em cada par de cores do sistema de design.

## 2. Teclado — percorra a tarefa inteira sem mouse

Este bloco encontra a maior parte dos problemas reais.

- [ ] Completei a tarefa do início ao fim usando só o teclado.
- [ ] Foco visível em **todos** os elementos focáveis.
- [ ] Nenhum indicador de foco removido sem substituto equivalente.
- [ ] Ordem de foco segue a ordem visual.
- [ ] Nenhum `tabindex` positivo.
- [ ] Elemento não interativo não recebe foco.
- [ ] Nenhuma armadilha de foco (exceto modal).
- [ ] Modal: foco entra, fica preso, `Esc` fecha, e ao fechar volta ao elemento que abriu.
- [ ] Ao remover um elemento focado, o foco vai para um lugar previsível.
- [ ] Menu, combobox e abas respondem a setas, `Home`, `End`, `Esc`.
- [ ] Link de pular para o conteúdo principal.

## 3. Leitor de tela — uma tarefa crítica por rodada

- [ ] Todo controle é anunciado com nome e papel corretos.
- [ ] Estado é anunciado: selecionado, expandido, pressionado, inválido, ocupado, desabilitado, atual.
- [ ] Mudança dinâmica é anunciada: resultado de busca, erro, confirmação, notificação.
- [ ] Nenhuma divergência entre o texto visível e o nome acessível.
- [ ] Ordem de leitura faz sentido.
- [ ] Nada importante está oculto de forma que o leitor não alcance.

## 4. Nome, papel e estado

- [ ] Todo campo tem rótulo associado. **Placeholder não é rótulo.**
- [ ] Botão de ícone tem nome textual acessível.
- [ ] Texto de link descreve o destino — nada de "clique aqui" repetido.
- [ ] Imagem significativa tem alternativa textual; decorativa tem alternativa vazia.
- [ ] Elemento nativo usado em vez de elemento genérico com manipulador de evento.
- [ ] Nenhum `role` declarado sem implementar o comportamento correspondente.
- [ ] Nenhum ARIA redundante ou conflitante com o texto visível.

## 5. Estrutura

- [ ] Um `h1` por página; hierarquia de títulos sem salto de nível.
- [ ] Regiões identificadas: navegação, principal, complementar, rodapé.
- [ ] Lista marcada como lista; tabela de dados com cabeçalhos associados.
- [ ] Ordem do código corresponde à ordem visual.
- [ ] Idioma da página declarado; trecho em outro idioma marcado.

## 6. Formulários

- [ ] Erro é anunciado, aponta o campo, explica o problema e diz como corrigir.
- [ ] Erro não é comunicado apenas por cor.
- [ ] Instrução e formato esperado informados **antes** do erro.
- [ ] Campo com propósito conhecido tem autocompletar declarado.
- [ ] **Erro de validação nunca limpa o que o usuário digitou.**
- [ ] Agrupamentos (rádio, checkbox) têm rótulo de grupo.
- [ ] Campo obrigatório é indicado de forma programática, não só visual.

## 7. Apresentação

- [ ] Contraste: texto normal 4,5:1; texto grande 3:1; componente e indicador de estado 3:1.
- [ ] Vale para texto sobre imagem, placeholder e estado desabilitado que precisa ser lido.
- [ ] Funciona com zoom de 200%, sem rolagem horizontal e sem perda de conteúdo.
- [ ] Funciona em viewport estreita.
- [ ] Funciona com espaçamento de texto aumentado.
- [ ] Nenhum estado comunicado apenas por cor.
- [ ] Alvo de toque com área e espaçamento adequados, especialmente perto de ação destrutiva.

## 8. Movimento e tempo

- [ ] Animação automática, carrossel e vídeo têm controle de pausa.
- [ ] Preferência de redução de movimento do sistema é respeitada.
- [ ] Nenhum conteúdo piscando (risco de convulsão).
- [ ] Limite de tempo é ajustável, extensível ou avisado antes de expirar.
- [ ] Sessão não expira descartando trabalho sem aviso.

---

## Severidades

| Situação | Severidade |
| --- | --- |
| Tarefa crítica impossível por teclado | `S1` |
| Tarefa não crítica impossível por teclado | `S2` |
| Erro automatizado de a11y | `S2` (bloqueia entrega) |
| Controle sem nome acessível | `S2` |
| Foco não visível | `S2` |
| Mudança dinâmica não anunciada | `S2` |
| Contraste abaixo de AA | `S2` |
| Formulário que perde dados no erro | `S1` |
| Conteúdo piscando | `S1` |

---

## Registro

```
Tela: <qual>
Automático: <ferramenta> → <n erros>
Teclado: <tarefa percorrida> → <resultado>
Leitor de tela: <ferramenta> → <resultado>
Zoom 200%: <resultado>
Contraste: <pares verificados> → <resultado>
Não verificado: <o que e por quê>
```
