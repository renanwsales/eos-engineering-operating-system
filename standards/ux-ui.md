# Norma — UX / UI

Esta norma trata do que é verificável em revisão de engenharia: estados, feedback, prevenção de
erro, consistência e proteção do trabalho do usuário. Não trata de gosto visual — decisão estética
pertence ao design, não a esta revisão.

---

## Estados

### U1. Todo estado é projetado **[OBRIGATÓRIA]**

Para cada tela e cada componente que busca ou envia dados, oito estados:

| Estado | Requisito |
| --- | --- |
| **Inicial / primeira vez** | Explica o que é e qual a próxima ação |
| **Carregando** | Feedback imediato; esqueleto quando a estrutura é conhecida |
| **Vazio** | Diz por que está vazio e o que fazer — nunca só "sem resultados" |
| **Parcial** | Parte carregou, parte falhou, e isso está claro |
| **Erro** | Diz o que houve, o que fazer, e permite tentar de novo |
| **Sucesso** | Confirma sem ambiguidade |
| **Sem permissão** | Diferencia "não existe" de "você não pode ver" quando é seguro |
| **Offline** | Comportamento definido, sem falha silenciosa |

Ausência de estado de erro ou de vazio é `S2`. É a lacuna mais comum e a que mais gera suporte.

### U2. Vazio não é erro **[OBRIGATÓRIA]**

Lista vazia legítima (primeira vez) tem tratamento diferente de busca sem resultado, que é diferente
de falha de carregamento. Confundi-los faz o usuário achar que o sistema quebrou.

---

## Feedback

### U3. Toda ação tem resposta imediata **[OBRIGATÓRIA]**

Nenhuma ação fica sem retorno visível. Se leva mais que um instante, mostre progresso. Se leva mais
de alguns segundos, informe o que está acontecendo e permita continuar em outra coisa.

### U4. Impedir envio duplicado **[OBRIGATÓRIA]**

Botão de ação com efeito externo é desabilitado durante o envio. Ausência disso gera pedido
duplicado e cobrança dupla — que é `S1`, não questão de interface.

### U5. Erro no vocabulário do usuário **[OBRIGATÓRIA]**

| Ruim | Bom |
| --- | --- |
| "Erro 500" | "Não conseguimos salvar agora. Tente novamente em instantes." |
| "Erro de validação" | "O CEP precisa ter 8 dígitos." |
| "Requisição inválida" | "Escolha uma data a partir de hoje." |
| "null is not an object" | Nunca deve chegar ao usuário |

Todo erro responde: o que aconteceu, e o que faço agora. Erro sem próxima ação é meia mensagem.

### U6. Ofereça o caminho de saída **[RECOMENDADA]**

Erro que o usuário não pode resolver oferece: tentar novamente, contatar suporte com o
identificador do erro, ou uma alternativa.

---

## Prevenção de erro

### U7. Confirmar ou desfazer em ação destrutiva **[OBRIGATÓRIA]**

Prefira desfazer a confirmar: confirmação é ignorada por reflexo depois da terceira vez. Onde
desfazer é impossível, a confirmação precisa nomear o que será destruído — não "Tem certeza?", mas
"Excluir o pedido #1234 e seus 3 itens?".

### U8. Nunca perca o trabalho do usuário **[OBRIGATÓRIA]**

Formulário não é limpo por erro de validação, por falha de rede, por navegação acidental, nem por
expiração de sessão. Perda de trabalho digitado é `S1` em formulário longo.

### U9. Valide no momento certo **[RECOMENDADA]**

Validação de formato ao sair do campo, não a cada tecla. Validação de regra de negócio no envio.
Mostrar erro antes de a pessoa terminar de digitar é hostil.

### U10. Ação destrutiva longe da ação comum **[RECOMENDADA]**

Separação visual e de posição entre "Salvar" e "Excluir". Vale especialmente em telas pequenas.

---

## Consistência

### U11. Um padrão por problema **[OBRIGATÓRIA]**

O mesmo tipo de ação se comporta igual em todo o produto: mesmo lugar, mesmo rótulo, mesmo retorno.
Três padrões diferentes de formulário obrigam o usuário a reaprender em cada tela.

### U12. Vocabulário único na interface **[OBRIGATÓRIA]**

O mesmo conceito tem o mesmo nome em toda a interface, e esse nome é o do glossário do domínio. Se
o código chama `pedido`, a interface não chama "compra" em uma tela e "venda" em outra.

### U13. Hierarquia clara **[RECOMENDADA]**

Uma ação primária por tela. Se tudo tem o mesmo destaque, nada tem destaque, e o usuário para para
decidir.

### U14. Estado da navegação preservado **[RECOMENDADA]**

Filtro, busca, ordenação e paginação sobrevivem a navegar e voltar. Perder o filtro ao voltar de um
detalhe é uma das maiores fontes de irritação em painéis administrativos.

---

## Conteúdo

### U15. Escreva para quem lê rápido **[RECOMENDADA]**

Rótulo curto e específico. "Salvar alterações" é melhor que "Enviar". Evite jargão interno na
interface: o usuário não sabe o que é "tenant", "sincronizar payload" ou "flag".

### U16. Formato local **[OBRIGATÓRIA]**

Data, hora, moeda, número e endereço no formato do usuário. Fuso horário correto e explícito quando
importa. Data ambígua (03/04) é fonte de erro real.

### U17. Números com significado **[RECOMENDADA]**

"Restam 2 unidades" é melhor que "estoque: 2". Contexto antes de valor cru.

---

## Fluxos

### U18. O fluxo tem começo, meio e fim visíveis **[RECOMENDADA]**

Em processo de múltiplas etapas: onde estou, quanto falta, posso voltar sem perder o que já fiz.

### U19. Não bloqueie o que pode ser postergado **[RECOMENDADA]**

Não exija tudo na entrada se parte pode vir depois. Cada campo obrigatório é uma chance de desistir.

### U20. Caminho de recuperação sempre existe **[OBRIGATÓRIA]**

Nenhum estado da interface é um beco sem saída. Sempre há como voltar, cancelar ou ir para um lugar
conhecido.

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Tela em branco durante o carregamento | Usuário acha que quebrou e recarrega |
| Girador infinito sem tempo limite | Espera indefinida sem informação |
| "Algo deu errado" | Suporte impossível, usuário sem ação |
| Confirmação em toda ação | Treina o usuário a confirmar sem ler |
| Formulário que limpa no erro | Abandono |
| Detalhe técnico na interface | Assusta e não ajuda |
| Vários padrões para a mesma coisa | Custo cognitivo permanente |
| Sucesso sem confirmação | Usuário repete a ação por dúvida |
| Filtro perdido ao voltar | Retrabalho em cada consulta |
| Ação irreversível sem aviso | Perda de dados do usuário |

---

## Verificação em revisão

Para cada tela alterada, percorra:

1. Os oito estados de U1 existem?
2. Cada ação tem retorno imediato, e envio duplo está impedido?
3. Cada mensagem de erro diz o que fazer?
4. Alguma ação destrui algo sem confirmação ou desfazer?
5. Algum caminho perde o que o usuário digitou?
6. Completa a tarefa só com teclado? (ver [acessibilidade](acessibilidade.md))
7. O vocabulário coincide com o do domínio e com o resto do produto?
8. Funciona em tela pequena e com texto ampliado?
