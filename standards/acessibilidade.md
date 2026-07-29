# Norma — Acessibilidade

Alvo: **WCAG 2.2 nível AA**. Acessibilidade não é uma camada aplicada no final; é consequência de
usar a plataforma corretamente. A maior parte dos problemas vem de recriar controles nativos com
elementos genéricos.

Verificação: [`checklists/acessibilidade.md`](../checklists/acessibilidade.md).

---

## Fundamento

### X1. Semântica antes de ARIA **[OBRIGATÓRIA]**

Use o elemento correto. Um botão nativo já é focável, acionável por teclado, anunciado como botão e
compatível com todas as tecnologias assistivas. Um `div` com clique não é nada disso, e recriar
esse comportamento exige acertar foco, teclado, papel e estado — o que quase nunca acontece por
completo.

> Regra: **nenhum ARIA é melhor do que ARIA errado.** ARIA não adiciona comportamento, apenas
> descreve; se você usa `role="button"`, você é responsável por implementar tudo o que um botão faz.

### X2. Estrutura significativa **[OBRIGATÓRIA]**

- Um `h1` por página, hierarquia de títulos sem salto de nível.
- Regiões de página identificadas (navegação, principal, complementar, rodapé).
- Listas marcadas como listas; tabelas de dados com cabeçalhos associados.
- Ordem do código igual à ordem visual — reordenar apenas por CSS quebra a navegação por teclado.

### X3. Idioma declarado **[OBRIGATÓRIA]**

Idioma da página declarado, e trecho em outro idioma marcado. Sem isso, o leitor de tela pronuncia
com as regras erradas.

---

## Teclado

### X4. Toda tarefa é completável por teclado **[OBRIGATÓRIA]**

Sem exceção. Barreira que impede completar uma tarefa é `S2`, e `S1` se a tarefa for crítica.

### X5. Foco sempre visível **[OBRIGATÓRIA]**

Remover o indicador de foco sem substituto equivalente é violação direta. Se o indicador padrão é
feio, desenhe um melhor — não o apague.

### X6. Ordem de foco lógica **[OBRIGATÓRIA]**

Segue a ordem visual. Sem `tabindex` positivo. Elemento não interativo não recebe foco.

### X7. Foco gerenciado em conteúdo dinâmico **[OBRIGATÓRIA]**

- Ao abrir modal: foco move para dentro, fica preso no modal, `Esc` fecha, e ao fechar o foco volta
  ao elemento que o abriu.
- Ao remover um elemento focado: o foco vai para um lugar previsível, nunca para o início da página.
- Menu, combobox e abas seguem o padrão de teclado esperado (setas, `Home`, `End`, `Esc`).

### X8. Sem armadilha de foco **[OBRIGATÓRIA]**

Exceto em modal, o usuário sempre pode sair de um componente pelo teclado.

### X9. Atalho para o conteúdo principal **[RECOMENDADA]**

Link de pular navegação, para quem usa teclado ou leitor de tela não repetir o menu em cada página.

---

## Nome, papel e estado

### X10. Todo controle tem nome acessível **[OBRIGATÓRIA]**

- Campo de formulário com rótulo associado. Placeholder **não** é rótulo: desaparece ao digitar.
- Botão de ícone tem nome textual acessível.
- Link tem texto que descreve o destino. "Clique aqui" e "Saiba mais" repetidos são inúteis para
  quem navega por lista de links.
- Imagem significativa tem alternativa textual; imagem decorativa tem alternativa vazia.

### X11. Estado comunicado programaticamente **[OBRIGATÓRIA]**

Selecionado, expandido, pressionado, inválido, ocupado, desabilitado, atual. Comunicar apenas por
cor ou posição visual exclui quem não vê.

### X12. Mudança dinâmica anunciada **[OBRIGATÓRIA]**

Resultado de busca, mensagem de erro, confirmação e notificação precisam ser anunciados por região
dinâmica. Sem isso, o usuário de leitor de tela não sabe que algo aconteceu — ele clica e recebe
silêncio.

---

## Formulários

### X13. Erro identificado, descrito e associado **[OBRIGATÓRIA]**

O erro é anunciado, aponta qual campo, explica o problema e diz como corrigir. Erro apenas em
vermelho, apenas no topo, não associado ao campo, é violação.

### X14. Sem dependência exclusiva de cor **[OBRIGATÓRIA]**

Estado sempre tem um segundo indicador: ícone, texto, borda, forma.

### X15. Campo com propósito declarado **[RECOMENDADA]**

Autocompletar declarado em nome, e-mail, telefone e endereço. Reduz esforço para todos, e muito
para quem tem limitação motora.

### X16. Não perca o que o usuário digitou **[OBRIGATÓRIA]**

Erro de validação nunca limpa o formulário. Perder dados digitados é a falha de usabilidade mais
custosa que existe, e afeta desproporcionalmente quem digita com dificuldade.

---

## Apresentação

### X17. Contraste **[OBRIGATÓRIA]**

- Texto normal: 4,5:1. Texto grande: 3:1.
- Componente de interface e indicador de estado: 3:1.
- Vale para texto sobre imagem, estado desabilitado que precisa ser lido, e placeholder.

### X18. Redimensionamento e reflow **[OBRIGATÓRIA]**

Funciona com zoom de 200% e em viewport estreita, sem rolagem horizontal e sem perda de conteúdo ou
funcionalidade.

### X19. Alvo de toque adequado **[RECOMENDADA]**

Área mínima confortável e espaçamento entre alvos adjacentes, especialmente em ações destrutivas
próximas de ações comuns.

### X20. Movimento controlável **[OBRIGATÓRIA]**

Animação automática, carrossel e vídeo têm controle de pausa. Respeite a preferência de redução de
movimento do sistema. Conteúdo que pisca é risco real de convulsão.

### X21. Tempo suficiente **[OBRIGATÓRIA]**

Limite de tempo é ajustável, extensível ou avisado antes de expirar. Sessão que expira sem aviso e
descarta trabalho é `S2`.

---

## Verificação

| Etapa | Como | Cobertura |
| --- | --- | --- |
| Automática | axe, ou equivalente, no pipeline | ~30% dos problemas |
| Teclado | Percorra a tarefa inteira sem mouse | Boa parte do restante |
| Leitor de tela | Uma tarefa crítica por rodada | Problemas de anúncio e contexto |
| Zoom | 200% e viewport estreita | Reflow |
| Contraste | Verificação de cada par de cores do sistema de design | Contraste |

**Ferramenta automática sozinha não aprova nada.** Ela não detecta rótulo errado, ordem de foco
ilógica, anúncio ausente ou alternativa textual inadequada — que são a maioria dos problemas
reais.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| `div` com clique no lugar de botão | Inacessível por teclado e não anunciado |
| Remover indicador de foco | Usuário de teclado se perde |
| Placeholder como rótulo | Rótulo desaparece ao digitar |
| `aria-label` em elemento que já tem texto visível | Divergência entre o que se vê e o que se ouve |
| `role` sem implementar o comportamento | Promessa não cumprida ao leitor de tela |
| Modal sem gerenciar foco | Usuário fica preso no fundo da página |
| Erro só por cor | Invisível para parte dos usuários |
| Ocultar com `display: none` o que deveria ser lido | Conteúdo desaparece do leitor de tela |
| `tabindex` positivo | Quebra a ordem natural de toda a página |
