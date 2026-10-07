# 📓 Volume 06 — Segurança e DevSecOps

Prefixo: `SEC` · Regras: SEC-001 a SEC-076 · Papel: [Security Engineer](agents/05-security.md)

Camada coberta: **3 (segurança)**.

**Fronteira.** OWASP Top 10 completo, criptografia, autenticação e sessão, segredos, dados
pessoais, cadeia de suprimentos, SSRF, níveis progressivos de verificação. Não cobre:
infraestrutura de deploy e política de acesso operacional (→ [10](10-devops.md)); isolamento de
inquilino como decisão de arquitetura (→ [16](16-multi-tenant.md)), com achados classificados por
este volume.

---

## Fundamentos

Em autenticação, autorização, pagamento e dado pessoal, o ônus da prova é invertido (`SEC-001`):
ausência de verificação é achado, não inconclusão. A ameaça realista é o usuário autenticado
mal-intencionado (`SEC-002`), não só o anônimo na borda.

A ordem fixa — autorização antes de tudo (`SEC-003`) — evita gastar a rodada em headers enquanto
IDOR permanece aberto. Isolamento de tenant no banco (`SEC-006`) e autorização por objeto
(`SEC-004`) são o núcleo `S0`; o restante do volume fecha as classes OWASP e a prova de que a
correção realmente fechou o caminho (`SEC-064`).

---

## A regra que governa o volume inteiro

### SEC-001 — O ônus da prova é invertido **[IMUTÁVEL]**

> Você não precisa provar que uma vulnerabilidade é explorável para bloquear. **Alguém precisa provar que o
> caminho está seguro.**

Em caminhos de autenticação, autorização, pagamento e dado pessoal, confiança `MEDIUM` já bloqueia. "Não
encontrei a verificação de autorização" é um **achado**, não um resultado inconclusivo.

Esta regra sobrepõe CON-010 e é a única exceção deliberada à política de confiança do framework.

### SEC-002 — Pense como atacante autenticado **[OBRIGATÓRIA]**

A ameaça realista é alguém que **já tem uma conta válida**. É a que a maioria das revisões perde, porque foca
em ataque não autenticado. Pergunte sempre: o que um usuário mal-intencionado com credencial legítima
consegue fazer?

### SEC-003 — Ordem de análise dentro da segurança **[OBRIGATÓRIA]**

`autorização → autenticação → entrada → saída → segredos → dependências → configuração → SSRF →
integridade → registro`.

Comece por autorização mesmo que lhe perguntem outra coisa. Autorização ausente supera qualquer outra classe
de achado.

---

## Capítulo 5.1 — Controle de acesso (OWASP A01)

A falha mais comum e mais grave em aplicações reais.

### SEC-004 — Autorização por objeto **[OBRIGATÓRIA]** · `S0`

Verifique se **este** sujeito pode agir sobre **este** recurso. Checar papel não basta.

### SEC-005 — Negar por omissão **[OBRIGATÓRIA]**

Rota, campo ou operação nova nasce inacessível. Lista de exceções públicas é mais segura que lista de
proteções.

### SEC-006 — Isolamento de tenant na camada de dados **[OBRIGATÓRIA]** · `S0`

Aplicado no ponto mais interno possível: política no banco ou camada de acesso obrigatória. Nunca na
disciplina de cada desenvolvedor.

### SEC-007 — As quatro perguntas por ponto de entrada **[OBRIGATÓRIA]**

1. O chamador está autenticado?
2. Está autorizado para a **operação**?
3. Está autorizado para o **objeto específico**?
4. O filtro de tenant é aplicado na camada de dados?

### SEC-008 — Os caminhos que a revisão esquece **[OBRIGATÓRIA]**

- [ ] Endpoint de lote: autoriza cada item, ou só o primeiro?
- [ ] Exportação e relatório: mesmas regras da leitura individual?
- [ ] Recurso aninhado: `b` pertence a `a`?
- [ ] Escrita e exclusão, não só leitura.
- [ ] Parâmetro de filtro, busca e ordenação alcança dado de outro tenant?
- [ ] Ordenação por coluna que o chamador não deveria saber que existe.
- [ ] Webhook e callback verificam o remetente?
- [ ] Job em background roda com a autoridade do solicitante ou com privilégio total?
- [ ] Endpoint de diagnóstico, métrica ou administração exposto?
- [ ] E-mail HTML, callback OAuth e template `body_html` escapam saída? (`SEC-072`, `SEC-075`)

### SEC-009 — Campo privilegiado do cliente é ignorado **[OBRIGATÓRIA]** · `S0`

Papel, plano, preço, status, dono, tenant e permissão vindos da requisição são explicitamente rejeitados.

### SEC-010 — Autorização centralizada por construção **[RECOMENDADA]**

Mecanismo que falha fechado quando a declaração falta. Repetir a verificação em cada handler garante que um
dia alguém esquecerá.

### SEC-011 — Registro de auditoria em operação sensível **[RECOMENDADA]**

Quem, quando, o que mudou, de qual valor para qual. Sem isso, investigação de fraude é impossível.

---

## Capítulo 5.2 — Criptografia (OWASP A02)

### SEC-012 — Senha com hash lento e específico **[OBRIGATÓRIA]** · `S0`

bcrypt, argon2 ou scrypt, com custo adequado e revisado periodicamente. Nunca hash rápido (MD5, SHA-*),
nunca criptografia reversível.

### SEC-013 — TLS em trânsito, sem exceção interna **[OBRIGATÓRIA]**

"É rede interna" não é justificativa: movimento lateral é o passo seguinte de qualquer invasão.

### SEC-014 — Dado sensível criptografado em repouso **[OBRIGATÓRIA]**

Com chave gerenciada e **rotacionável**. Criptografia com chave que não pode ser trocada é criptografia com
prazo.

### SEC-015 — Nenhum algoritmo obsoleto e nenhuma criptografia caseira **[OBRIGATÓRIA]**

Use primitiva de biblioteca padrão auditada. Modo de operação e vetor de inicialização são decisões, não
padrões implícitos.

### SEC-016 — Aleatoriedade criptográfica para token **[OBRIGATÓRIA]**

Gerador de números pseudoaleatórios comum é previsível. Vale para token de sessão, de recuperação de senha,
de convite e de idempotência.

### SEC-017 — Comparação de segredo em tempo constante **[OBRIGATÓRIA]**

Comparação byte a byte com saída antecipada vaza informação por tempo de resposta.

### SEC-018 — Hash não é criptografia, e codificação não é nenhum dos dois **[OBRIGATÓRIA]**

Base64 não protege nada. Confundir os três é erro conceitual que produz vulnerabilidade real.

---

## Capítulo 5.3 — Injeção (OWASP A03)

### SEC-019 — Consulta parametrizada, sempre **[OBRIGATÓRIA]** · `S0`

Concatenação de entrada em SQL é `S0`. Vale igualmente para NoSQL, comando de sistema, LDAP, XPath e
template. Usar ORM ou cliente HTTP de banco **não** dispensa a regra: se a biblioteca monta o predicado
a partir de uma string que você interpolou, você concatenou.

### SEC-020 — Nunca execute entrada **[OBRIGATÓRIA]** · `S0`

Como código, comando, template ou expressão. Inclui avaliação dinâmica e desserialização em objeto
executável.

### SEC-021 — Escape na saída por contexto **[OBRIGATÓRIA]**

HTML, atributo, URL e JavaScript têm regras diferentes. Escapar para o contexto errado não protege.
Texto de usuário, API ou integração que entra em HTML de resposta, e-mail ou template precisa de
encoding **no momento da interpolação**, no contexto certo:

| Contexto | Escape mínimo |
| --- | --- |
| Texto HTML (`<p>…</p>`) | Entidades: `& < > " '` |
| Atributo quoted | Idem + nunca quebrar aspas do atributo |
| URL em `href` / `src` | Esquema permitido (`SEC-073`) **e** escape de atributo |
| JavaScript inline / handler | Não interpolar; se inevitável, encoding JS dedicado |

Frameworks que escapam por padrão (JSX texto, engines com auto-escape) cobrem o caminho feliz.
String HTML montada à mão, `innerHTML` e respostas `text/html` no servidor **não** herdam isso —
trate como superfície explícita (`SEC-072`, `SEC-076`).

### SEC-022 — Nenhuma inserção de HTML não confiável **[OBRIGATÓRIA]** · `S1`

Renderizar HTML vindo de usuário, CMS, ticket ou modelo (`dangerouslySetInnerHTML`, `innerHTML`,
documento HTML gerado no servidor) é `S1`. Se o produto exige rich text: sanitize com biblioteca
dedicada (allowlist de tags/atributos), documente o motivo, e teste payload com script, evento e
URL `javascript:`. Filtro caseiro de tags não satisfaz (`SEC-074`).

### SEC-023 — Upload de arquivo tratado como hostil **[OBRIGATÓRIA]**

Tipo verificado pelo conteúdo e não pela extensão · nome gerado pelo servidor · armazenado fora da raiz
servida · nunca executável · limite de tamanho · varredura quando aplicável.

### SEC-024 — Nome de arquivo, cabeçalho e caminho validados **[OBRIGATÓRIA]**

Travessia de diretório e injeção de cabeçalho vêm de campos que ninguém considera entrada.

### SEC-067 — SQL dinâmico só com identificador allowlist e valor bound **[OBRIGATÓRIA]** · `S0`

Quando a consulta precisa ser montada em runtime (`EXECUTE`, `format`, query builder com fragmentos),
**identificadores** (tabela, coluna, direção de sort, nome de campo de data) vêm de um mapa fechado no
código — nunca do texto do usuário. **Valores** (busca, IDs, datas, enums) entram só como parâmetros
vinculados (`$1`, placeholders do driver). Concatenar o termo de busca na string SQL é a mesma classe
de falha que `SEC-019`, mesmo dentro de uma função `SECURITY DEFINER` ou de um “fast path”.

Violação típica: `format('… ORDER BY %s …', userSort)` sem CASE/allowlist; ou
`ilike '%' || userInput` embutido no texto do `format` em vez de `USING`.

### SEC-068 — Predicado montado em string é superfície de injeção **[OBRIGATÓRIA]** · `S0`

APIs de consulta que aceitam filtro como string (PostgREST `.or()` / `.filter()`, GraphQL where
serializado, query-string de motor de busca interno) tratam essa string como **gramática**, não como
valor. Caracteres como `,` `()` `.` e operadores da DSL mudam o predicado.

Se a busca precisa ir nessa string: (1) sanitize removendo metacaracteres da gramática; (2) prefira
APIs tipadas (`.eq(coluna, valor)`, `.ilike(coluna, valor)`) em que o valor não reconstrói a
expressão; (3) mantenha filtro de inquilino / autorização por objeto no mesmo caminho (`SEC-004`,
`SEC-006`). Sanitizar não substitui parametrizar SQL (`SEC-019`).

### SEC-069 — Identificador e enum de consulta por lista de permitidos **[OBRIGATÓRIA]**

Sort, campo de data, status, escopo e nomes de coluna aceitos na API pública são allowlist no
servidor. Lista de proibidos (blocklist) falha: o atacante usa o metacaractere que você esqueceu.
Enum do schema OpenAPI **não** basta se o runtime ainda interpola `asString(input)` na DSL.

### SEC-070 — Cliente privilegiado exige validação mais rígida do interpolado **[OBRIGATÓRIA]** · `S0`

Service role, conexão admin ou qualquer cliente que **ignora RLS / row policy** não pode interpolar
IDs ou termos vindos de integração externa (webhook, CRM, gateway) sem validar formato fechado
(ex.: só dígitos, UUID canônico). O blast radius é o banco inteiro, não o inquilino do JWT.
Isolamento de tenant na query (`company_id = …`) continua obrigatório (`SEC-006`) e não absolve a
injeção de gramática.

### SEC-071 — Helper único de sanitização de filtro compartilhado **[RECOMENDADA]**

Onde a DSL exige interpolação (busca multi-campo em `.or()`), existe **uma** função nomeada —
testada — que remove metacaracteres da gramática, limita comprimento e colapsa espaços. Tools de
agente, telas admin e webhooks usam a mesma. Sanitização parcial e divergente entre módulos é o
defeito que reabre `SEC-068` na próxima feature.

### SEC-072 — Superfície HTML fora do SPA também escapa **[OBRIGATÓRIA]** · `S1`

XSS não mora só no bundle do front. Toda resposta ou artefato `text/html` (ou corpo HTML embutido)
escapa saída (`SEC-021`) ou sanitiza (`SEC-022`):

- e-mail transacional e digest com HTML;
- callback OAuth / página de erro / “feche esta janela”;
- template de mensageria com `body_html`;
- PDF/recibo/kit gerado como HTML no servidor;
- webhook ou Edge que devolve HTML em vez de JSON.

Revisão que só grepou o cliente e declarou “sem XSS” violou a caça (`SEC-076`) e o ônus invertido
(`SEC-001`).

### SEC-073 — Href e URL de navegação só com esquema permitido **[OBRIGATÓRIA]**

Valor que entra em `href`, `src`, `action`, `formaction` ou equivalente aceita apenas `http:` /
`https:` (ou caminho relativo documentado no perfil). `javascript:`, `data:` e esquema vazio com
quebra de atributo executam código no navegador da vítima.

Escape de HTML **não** substitui esta regra: um `href` bem escapado ainda pode ser
`javascript:alert(1)`. Fetch server-side de URL do usuário continua em `SEC-049` (SSRF); aqui o
risco é navegação no cliente.

### SEC-074 — Filtro parcial de caracteres não é escape **[OBRIGATÓRIA]** · `S1`

`.replace(/[<>&]/g, "")`, strip de tags, ou allowlist de tags sem política de atributo **parece**
correção e falha em aspas, handlers (`onerror=`), entidades incompletas e URLs. Em revisão, trate
como ainda aberto até haver encoding por contexto (`SEC-021`) ou sanitizer dedicado (`SEC-022`).

### SEC-075 — Template em modo HTML escapa toda variável **[OBRIGATÓRIA]**

Motor de template ou `renderTemplate` que gera HTML escapa **cada** variável na interpolação.
Chaves tipadas como link usam `SEC-073`. Canal só texto (SMS, push plaintext) permanece sem escape
HTML. Preferir modo explícito (`html: true` ou engine com auto-escape) a “às vezes escapamos no
handler”. Um campo esquecido (nome, descrição, Pix copia-e-cola) reabre XSS armazenado.

### SEC-076 — Caça mecânica antes de declarar ausência de XSS **[OBRIGATÓRIA]**

Antes de afirmar que não há XSS no escopo, execute busca (ou equivalente no perfil) e anexe o
resultado:

- `dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`, `document.write`, `insertAdjacentHTML`;
- respostas / strings com `text/html` ou `Content-Type: text/html`;
- `body_html`, rich text, e-mail HTML, callback HTML;
- interpolação `${…}` / `{{…}}` em literais HTML sem helper de escape.

“Não vi nada” sem evidência da busca é inconclusão disfarçada — em saída HTML, trate como achado
até provar o contrário (`SEC-001`).

---

## Capítulo 5.4 — Design inseguro (OWASP A04)

### SEC-025 — Reautenticação em fluxo sensível **[OBRIGATÓRIA]**

Recuperação e troca de senha, troca de e-mail, alteração de meio de pagamento, mudança de permissão.

### SEC-026 — Limite de tentativas com bloqueio progressivo **[OBRIGATÓRIA]**

Em autenticação, recuperação de senha e verificação de código. Ausência é `S1`.

### SEC-027 — Não revele existência **[OBRIGATÓRIA]**

Erro de login não diz se o e-mail está cadastrado. Tempo de resposta também não deve revelar.

### SEC-028 — Operação irreversível é confirmada e registrada **[OBRIGATÓRIA]**

### SEC-029 — Modele o abuso, não só o uso **[OBRIGATÓRIA]**

Para cada fluxo: como alguém o usaria para fraudar, extrair dados em volume, ou negar serviço a outro
usuário?

### SEC-030 — Controle de segurança que empurra para contorno é falha **[RECOMENDADA]**

Política de senha que as pessoas escrevem em papel é falha de segurança disfarçada de controle. Reporte
junto com [Product/UX](agents/09-product-ux.md).

---

## Capítulo 5.5 — Configuração (OWASP A05)

### SEC-031 — Nenhuma credencial padrão em produção **[OBRIGATÓRIA]** · `S0`
### SEC-032 — Depuração e erro detalhado desligados em produção **[OBRIGATÓRIA]**
### SEC-033 — CORS restrito a origens conhecidas **[OBRIGATÓRIA]**

`*` combinado com credencial é `S0`.

### SEC-034 — Cabeçalhos de segurança presentes **[OBRIGATÓRIA]**

Política de conteúdo, HSTS, `nosniff`, política de referenciador, controle de enquadramento, política de
permissões.

### SEC-035 — Armazenamento privado por padrão **[OBRIGATÓRIA]**

Bucket ou blob público é a causa recorrente de vazamento em massa.

### SEC-036 — Menor privilégio em toda credencial de serviço **[OBRIGATÓRIA]**

A aplicação nunca usa credencial de administrador do banco. Migração usa outra credencial. Isso limita o
dano de uma injeção bem-sucedida.

### SEC-037 — Superfície mínima **[OBRIGATÓRIA]**

Sem endpoint de diagnóstico, console de administração ou porta de gerenciamento exposta.

---

## Capítulo 5.6 — Dependências e cadeia de suprimentos (OWASP A06 e A08)

### SEC-038 — Varredura automatizada que bloqueia **[OBRIGATÓRIA]**

No pipeline, reprovando severidade crítica e alta. Varredura que só reporta é teatro.

### SEC-039 — Supressão exige análise de explorabilidade escrita **[OBRIGATÓRIA]**

Se não é explorável, isso é uma **conclusão** que precisa estar registrada. Supressão sem análise é `S2`.

### SEC-040 — Dependência abandonada é risco registrado **[RECOMENDADA]**

### SEC-041 — Integridade verificada em tudo que executa **[OBRIGATÓRIA]**

Script externo, artefato de build, imagem de contêiner, artefato de deploy. Assinatura ou hash.

### SEC-042 — Pipeline é código revisado **[OBRIGATÓRIA]**

Quem controla o pipeline controla a produção. Mudança nele tem a mesma revisão do código, ou mais.

### SEC-043 — Cuidado com typosquatting e script de instalação **[RECOMENDADA]**

Pacote novo é decisão: verifique nome, mantenedor, volume de uso e o que ele executa na instalação.

---

## Capítulo 5.7 — Autenticação e sessão (OWASP A07)

### SEC-044 — Sessão expira, renova com segurança e é invalidada **[OBRIGATÓRIA]**

Em logout, em troca de senha, em revogação de acesso. Sessão que sobrevive à troca de senha é `S1`.

### SEC-045 — Identificador de sessão regenerado após autenticar **[OBRIGATÓRIA]**

Evita fixação de sessão.

### SEC-046 — Token com escopo, vida curta e revogação possível **[OBRIGATÓRIA]**

Token que não pode ser revogado é decisão que exige ADR, não padrão.

### SEC-047 — MFA disponível em conta e operação sensível **[RECOMENDADA]**
### SEC-048 — Proteção contra requisição forjada em fluxo com cookie **[OBRIGATÓRIA]**

---

## Capítulo 5.8 — SSRF (OWASP A10)

### SEC-049 — URL fornecida pelo usuário passa por lista de permitidos **[OBRIGATÓRIA]**

Bloqueie faixas internas e endpoints de metadados de nuvem. Não siga redirecionamento cegamente.

Verifique em: importação por URL, webhook configurável, geração de miniatura, conversão de documento,
pré-visualização de link.

---

## Capítulo 5.9 — Registro e monitoramento (OWASP A09)

### SEC-050 — Nenhum dado sensível em log **[OBRIGATÓRIA]** · `S0`

Senha, token, chave, cartão, dado pessoal completo. **Mascare no ponto de escrita**, nunca no visualizador:
o log já foi copiado para outros sistemas antes de alguém olhar.

### SEC-051 — Eventos de segurança registrados e alertados **[OBRIGATÓRIA]**

Autenticação (sucesso e falha), mudança de permissão, acesso a dado sensível, operação destrutiva. Com
alerta para pico de falha de autenticação e acesso em volume anômalo.

---

## Capítulo 5.10 — Segredos

### SEC-052 — Ordem correta ao encontrar segredo exposto **[IMUTÁVEL]**

```
1. ROTACIONE a credencial          ← primeiro, sempre
2. Remova do código e do histórico
3. Adicione varredura automática
```

Remover do repositório sem rotacionar **não resolve nada**: o segredo já está em clones, caches de CI,
forks e máquinas de desenvolvedores. Esta ordem é rotineiramente executada ao contrário.

**Regras complementares:**

- Nunca em código, histórico, cliente, log ou artefato de build.
- Gerenciador de segredos, injeção em execução, rotação **sem deploy**.
- Varredura no pipeline e em pre-commit.
- Atenção ao que vaza em: variável de ambiente de frontend, mapa de código-fonte, log de erro, imagem de
  contêiner, log do próprio pipeline.

---

## Capítulo 5.11 — Dados pessoais

### SEC-053 — Inventário obrigatório **[OBRIGATÓRIA]**

Que dado pessoal existe, onde está, por quanto tempo, quem acessa, por quê. Sem inventário, nenhuma das
regras seguintes é verificável.

### SEC-054 — Minimização **[OBRIGATÓRIA]**

Não colete o que não usa. Cada campo é responsabilidade permanente e aumenta o dano de um vazamento.

### SEC-055 — Retenção declarada e eliminação automatizada **[OBRIGATÓRIA]**

### SEC-056 — Direitos do titular tecnicamente possíveis **[OBRIGATÓRIA]**

Acesso, correção e eliminação — **incluindo** backup, log e sistema analítico. Descobrir na primeira
solicitação que a eliminação é impossível é falha de conformidade.

### SEC-057 — Nenhum dado pessoal em desenvolvimento ou em fixture **[OBRIGATÓRIA]**

Use dado sintético ou anonimizado.

### SEC-058 — Compartilhamento com terceiro é decisão registrada **[OBRIGATÓRIA]**

Não consequência acidental de uma integração.

---

## Capítulo 5.12 — Níveis de verificação

Inspirado na ideia de níveis progressivos do OWASP ASVS, adaptada para ser executável numa rodada de revisão.
Existe para resolver um problema concreto: sem níveis, toda auditoria de segurança tende a "verificar tudo",
que na prática significa verificar superficialmente tudo — e passar pelo que importa.

### SEC-059 — Três níveis, escolhidos por criticidade do módulo **[OBRIGATÓRIA]**

| Nível | Aplica-se a | Profundidade |
| --- | --- | --- |
| **V1 — Base** | Todo código, sempre | As dez regras de bloqueio. Nenhuma entrega passa sem V1 |
| **V2 — Padrão** | Módulos que tocam dado de usuário, dinheiro ou permissão | V1 + capítulos 5.1 a 5.9 percorridos com evidência por ponto de entrada |
| **V3 — Crítico** | Autenticação, pagamento, dado pessoal, multi-inquilino | V2 + modelagem de abuso (`SEC-029`), caminho de exploração demonstrado como fechado (`SEC-064`), inventário de dado pessoal, revisão humana obrigatória |

A classificação por módulo vive no [perfil do projeto](templates/perfil-do-projeto.md). Módulo sem
classificação é tratado como **V2** até que alguém decida — o padrão erra para o lado seguro.

### SEC-060 — O nível é declarado no relatório, sempre **[OBRIGATÓRIA]**

```
Nível aplicado: V2
Justificativa: módulo lê e escreve dado de usuário, não toca pagamento
Não verificado neste nível: modelagem de abuso, inventário de dado pessoal
```

Auditoria sem nível declarado é auditoria de profundidade desconhecida, e não pode ser comparada com a
próxima nem servir de base para a nota.

### SEC-061 — Subir de nível é decisão registrada; descer também **[OBRIGATÓRIA]**

Descer de V3 para V2 num módulo de pagamento é aceitação de risco: exige nome de pessoa e registro
(`CON-042`). Nunca é decisão de agente.

### SEC-062 — V3 nunca é executado só por agente **[IMUTÁVEL]**

Ele **prepara** a evidência: caminhos de exploração, inventário, matriz de autorização por ponto de entrada. A
aprovação é humana. Ver `SEC-066`.

### SEC-063 — Nível não substitui as regras de bloqueio **[IMUTÁVEL]**

V1 é piso absoluto. Não existe módulo periférico o suficiente para ter segredo no repositório ou consulta
concatenada.

---

## Regras de bloqueio

Nenhuma entrega passa com qualquer um destes:

| # | Condição | Regra |
| --- | --- | --- |
| 1 | Endpoint sem autorização por objeto | SEC-004 |
| 2 | Consulta multi-tenant sem filtro de isolamento | SEC-006 |
| 3 | Segredo no repositório ou no cliente | SEC-052 |
| 4 | Concatenação de entrada em consulta ou comando | SEC-019 |
| 5 | Senha com hash inadequado | SEC-012 |
| 6 | Dado pessoal em log | SEC-050 |
| 7 | Vulnerabilidade crítica ou alta sem análise registrada | SEC-038 |
| 8 | CORS permissivo com credencial | SEC-033 |
| 9 | Dado sensível sem TLS | SEC-013 |
| 10 | Ausência de limite de tentativas em autenticação | SEC-026 |

---

## Verificação de uma correção de segurança

### SEC-064 — Testes passando não é prova **[OBRIGATÓRIA]**

Demonstre que o caminho de exploração está fechado:

```
Antes:     <requisição do usuário B contra recurso do usuário A> → 200, dados retornados
Depois:    <mesma requisição>                                    → 403
Regressão: <requisição legítima do usuário A>                    → 200, inalterado
```

### SEC-065 — Descreva o caminho de exploração concretamente **[OBRIGATÓRIA]**

Quem, com que acesso, faz o quê, para obter o quê. Aviso abstrato não é corrigido; caminho concreto é.

### SEC-066 — `S0` de segurança não é rebaixável por agente **[IMUTÁVEL]**

Nem pelo orquestrador. Somente o dono humano nomeado pode aceitar o risco, explicitamente e por escrito.
Um `S0` interrompe a rodada inteira, sem completar o restante da análise.

---

## Padrões reutilizáveis

**Padrão: authz por objeto no ponto de carga.** Carregar recurso e checar sujeito×ação×instância
antes de mutar (`SEC-004`); negar por omissão em rota nova (`SEC-005`).

**Padrão: quatro perguntas por entrada.** Quem · o que · em qual recurso · por qual caminho
esquecido (`SEC-007`, `SEC-008`).

**Padrão: parametrizar tudo.** SQL/NoSQL/comando/template sem concatenação (`SEC-019`,
`SEC-020`).

**Padrão: SQL dinâmico seguro.** Allowlist de identificadores + `USING` / placeholders para
valores (`SEC-067`). Sort e campo de data nunca vêm do texto livre (`SEC-069`).

**Padrão: busca em DSL de filtro.** Preferir API tipada; se interpolar, sanitizar gramática com
helper único (`SEC-068`, `SEC-071`) e nunca confiar nisso no lugar de RLS/authz.

**Padrão: escape na borda HTML.** Helper único (`escHtml` / `escapeHtml`) + `escHref` só `http(s)`
para todo HTML de e-mail, callback e template (`SEC-021`, `SEC-072`, `SEC-073`, `SEC-075`).

**Padrão: rich text só com sanitizer.** Allowlist de tags/atributos via biblioteca; documentar o
motivo (`SEC-022`). Filtro `.replace` parcial é falha (`SEC-074`).

**Padrão: caça XSS antes do veredito.** Grep das APIs de HTML + respostas `text/html`; anexa
evidência (`SEC-076`).

**Padrão: segredo encontrado.** Rotacionar → revogar → remover do histórico → post-mortem
(`SEC-052`) — nesta ordem.

**Padrão: prova antes/depois.** Mesma requisição exploratória → 403; legítima → 200 (`SEC-064`).

---

## Matrizes de decisão

| Pergunta | Prefira | Evite se |
| --- | --- | --- |
| Papel vs objeto | Objeto (`SEC-004`) | Só role check |
| Tenant | Filtro/policy no dado (`SEC-006`) | Confiar em cada query |
| Nível V1/V2/V3 | Por criticidade do módulo (`SEC-059`) | V3 só por agente (`SEC-062`) |
| Hash de senha | Algoritmo lento dedicado (`SEC-012`) | MD5/SHA “com salt” |
| CORS | Origens conhecidas (`SEC-033`) | `*` com credencial |
| Dado pessoal em log | Redact / não logar (`SEC-050`) | “só em staging” |
| HTML de saída | Escape por contexto / sanitizer (`SEC-021`, `SEC-022`) | `.replace(<>&)` (`SEC-074`) |
| Link em HTML | Só `http(s)` (`SEC-073`) | Qualquer string no `href` |

| Condição de bloqueio | Regra |
| --- | --- |
| Sem authz por objeto | `SEC-004` |
| Multi-tenant sem isolamento | `SEC-006` |
| Segredo no repo/cliente | `SEC-052` |
| Concatenação em consulta | `SEC-019` |
| SQL dinâmico com sort/coluna do usuário | `SEC-067`, `SEC-069` |
| Filtro `.or()` / DSL com texto livre | `SEC-068` |
| Service role interpolando ID externo | `SEC-070` |
| HTML de e-mail/callback/template | Escape por contexto (`SEC-021`, `SEC-072`, `SEC-075`) |
| `href` / link de usuário | Só `http(s)` (`SEC-073`) |
| `.replace(<>&)` como “fix” XSS | Ainda aberto (`SEC-074`) |
| Hash inadequado | `SEC-012` |

---

## Fluxo de trabalho

```
1. Declarar nível V1/V2/V3 do módulo (SEC-059–060)
2. Autorização por objeto + tenant + caminhos esquecidos (SEC-004–008)
3. Autenticação/sessão/MFA/CSRF (SEC-044–048, SEC-025–027)
4. Entrada: injeção, SQL dinâmico, DSL de filtro, upload, SSRF (SEC-019–024, SEC-067–071, SEC-049)
5. Saída XSS: escape por contexto, HTML fora do SPA, href, caça mecânica (SEC-021–022, SEC-072–076)
6. Criptografia, TLS, segredos (SEC-012–018, SEC-052)
7. Config, CORS, headers, superfície (SEC-031–037)
8. Dependências e pipeline (SEC-038–043)
9. Logs e eventos de segurança (SEC-050–051)
10. Dados pessoais: inventário, retenção, direitos (SEC-053–058)
11. Correção: prova de exploração fechada (SEC-064–065)
```

Checklist operacional: [`checklists/seguranca-owasp.md`](checklists/seguranca-owasp.md).

---

## Exemplos de implementação

```
// Ruim — SEC-004: só papel
if (user.role === 'admin') return db.orders.find(orderId)

// Bom — objeto
const order = await db.orders.find(orderId)
if (!can(user, 'read', order)) throw Forbidden()
return order
```

```
// Ruim — SEC-019
db.query(`SELECT * FROM users WHERE email = '${email}'`)

// Bom
db.query('SELECT * FROM users WHERE email = $1', [email])
```

```
-- Ruim — SEC-067: sort e termo no format
EXECUTE format('SELECT * FROM orders WHERE company_id = %L AND %s ORDER BY %s',
  company, 'description ILIKE ''%' || search || '%''', userSort);

-- Bom — allowlist + bind
v_sort := CASE user_sort WHEN 'due' THEN 'due_date' ELSE 'created_at' END;
EXECUTE format('SELECT * FROM orders WHERE company_id = $1 AND description ILIKE ''%%'' || $2 || ''%%'' ORDER BY %I',
  v_sort)
USING company_id, search;
```

```
// Ruim — SEC-068: termo na gramática PostgREST/filtro
q.or(`name.ilike.%${term}%,email.ilike.%${term}%`)

// Bom — sanitizar gramática (ou .ilike tipado por campo)
const safe = sanitizeFilterTerm(term) // remove , ( ) . % _ " ' \
q.or(`name.ilike.%${safe}%,email.ilike.%${safe}%`)
// ainda melhor: q.ilike('name', `%${safe}%`) quando um campo basta
```

```
// Ruim — SEC-070: ID de webhook no .or com service role
admin.from('leads').or(`external_id.eq.${payload.id}`)

// Bom
const id = String(payload.id)
if (!/^\d{1,20}$/.test(id)) throw BadRequest()
admin.from('leads').eq('external_id', id).eq('company_id', companyId)
```

```
// Ruim — SEC-074 / SEC-072: “escape” parcial em callback HTML
return `<p>Erro: ${message.replace(/[<>&]/g, "")}</p>`

// Bom — SEC-021 + SEC-073
return `<p>Erro: ${escapeHtml(message)}</p>
<p><a href="${escapeHref(safeHttpUrl)}">Voltar</a></p>`
```

```
// Ruim — SEC-075: variável crua no body_html
renderTemplate(tpl.body_html, { "cliente.nome": name })

// Bom — modo HTML escapa tudo; link só http(s)
renderTemplate(tpl.body_html, vars, { html: true })
```

```
# Ruim — SEC-064: "testes passaram"
# Bom — prova
Antes:  GET /orders/A  como user B → 200 + corpo
Depois: GET /orders/A  como user B → 403
Legítimo: GET /orders/A como user A → 200
```

---

## Antipadrões

| Antipadrão | Consequência |
| --- | --- |
| Confiar em papel sem objeto | IDOR / `S0` (`SEC-004`) |
| Isolamento só na disciplina de query | Vazamento multi-tenant (`SEC-006`) |
| Concatenar entrada em SQL/comando | Injeção (`SEC-019`, `SEC-020`) |
| `ORDER BY` / coluna a partir do request | SQL dinâmico inseguro (`SEC-067`, `SEC-069`) |
| Montar `.or()` / filtro DSL com texto cru | Predicado injetável (`SEC-068`) |
| Service role + ID de terceiro sem validar | Bypass de RLS + injeção (`SEC-070`) |
| Sanitizar “um pouco” em cada tela | Regressão na próxima feature (`SEC-071`) |
| Só revisar o SPA e ignorar e-mail/callback | XSS fora do bundle (`SEC-072`, `SEC-076`) |
| `.replace(<>&)` como mitigação XSS | Quebra de atributo / handler (`SEC-074`) |
| `href="${userUrl}"` sem esquema | `javascript:` / phishing (`SEC-073`) |
| Template HTML com variável crua | XSS armazenado (`SEC-075`) |
| Segredo no repositório “por enquanto” | Compromisso permanente até rotacionar (`SEC-052`) |
| Hash rápido de senha | Credential stuffing trivial (`SEC-012`) |
| CORS `*` com cookies | CSRF cross-origin (`SEC-033`) |
| Dado pessoal em log | Violação e impossível de apagar (`SEC-050`) |
| Suprimir CVE sem análise escrita | Risco invisível (`SEC-039`) |
| “Testes verdes” como prova de authz | Regressão de exploração (`SEC-064`) |
| Rebaixar `S0` de segurança por prazo | `SEC-066` |

---

## Checklist

- [ ] Ônus invertido em authz/pagamento/PII; nível declarado. (`SEC-001`, `SEC-060`)
- [ ] Autorização por objeto; negar por omissão. (`SEC-004`, `SEC-005`)
- [ ] Isolamento de tenant no dado quando aplicável. (`SEC-006`)
- [ ] Caminhos esquecidos percorridos. (`SEC-008`)
- [ ] Consulta parametrizada; sem executar entrada. (`SEC-019`, `SEC-020`)
- [ ] SQL dinâmico: allowlist de identificadores + valores bound. (`SEC-067`, `SEC-069`)
- [ ] Filtro/DSL de busca sem texto cru; service role valida IDs. (`SEC-068`, `SEC-070`)
- [ ] Saída HTML: escape por contexto; e-mail/callback/template; href só http(s); caça anexada. (`SEC-021`, `SEC-022`, `SEC-072`–`SEC-076`)
- [ ] Hash adequado; TLS; sem segredo no cliente/repo. (`SEC-012`, `SEC-013`, `SEC-052`)
- [ ] Sessão/token com expiração e regeneração. (`SEC-044`, `SEC-045`)
- [ ] SSRF com allowlist. (`SEC-049`)
- [ ] Sem PII em log; eventos de segurança. (`SEC-050`, `SEC-051`)
- [ ] Inventário/minimização/retenção de PII. (`SEC-053`–`SEC-055`)
- [ ] Correção com prova antes/depois. (`SEC-064`)
- [ ] Regras de bloqueio da tabela do volume: zero violações abertas.

---

## Prompt do volume

```
You are performing a security review under EOS Volume 06 (SEC).

Load: core-contract, output-schemas, 00-constituicao, 06-seguranca.md,
checklists/seguranca-owasp.md. Cite 16-multi-tenant.md for tenant product
decisions; 10-devops.md for deploy/access ops — do not restate OPS norms.

Sequence (SEC-003):
1. authorization → 2. authentication → 3. input → 4. output → 5. secrets →
6. dependencies → 7. configuration → 8. SSRF → 9. integrity → 10. logging.

Rules of engagement:
- Burden of proof inverted on authz/payment/PII (SEC-001).
- Authenticated attacker threat model (SEC-002).
- Object-level authz and tenant isolation are S0 (SEC-004, SEC-006).
- Parameterized queries; dynamic SQL only with allowlisted identifiers + bound
  values (SEC-019, SEC-067–SEC-069). Filter/DSL strings are injection surface
  (SEC-068); privileged clients validate external IDs (SEC-070).
- XSS: context escape + sanitize untrusted HTML (SEC-021–022). HTML outside the
  SPA (email, OAuth callback, body_html) (SEC-072). href allowlist http(s)
  (SEC-073). Partial .replace is not escape (SEC-074). HTML templates escape
  every variable (SEC-075). Mechanical hunt before “no XSS” (SEC-076).
- Fix requires exploit-path closed with before/after (SEC-064).
- Do not downgrade security S0 (SEC-066). Do not invent new SEC rules.

Output: findings with path:line, severity, exploit path, verification level
(V1/V2/V3), blocking-table hits, unverified items.
```

---

## Critérios de aceite

1. Nenhum endpoint em escopo sem autorização por objeto (`SEC-004`).
2. Multi-tenant em escopo com isolamento no dado (`SEC-006`).
3. Zero concatenação de entrada em consulta/comando (`SEC-019`, `SEC-020`).
4. SQL dinâmico e DSL de filtro conformes (`SEC-067`–`SEC-070`).
5. Saída HTML no escopo conforme (`SEC-021`, `SEC-022`, `SEC-072`–`SEC-076`), com evidência de caça.
6. Nenhum segredo no repositório ou no cliente (`SEC-052`).
7. Sem dado pessoal em log nos caminhos revisados (`SEC-050`).
8. Nível de verificação declarado (`SEC-060`).
9. Correções `S0`/`S1` com prova antes/depois (`SEC-064`).

---

## Verificação obrigatória de saída

```
## Escopo e nível
Módulo/superfície: <...>
Nível: <V1 | V2 | V3> | Criticidade: <...>

## Ordem SEC-003
| Etapa | Percorrida? | Evidência |

## Bloqueios (tabela do volume)
| # | Condição | Presente? | Evidência |

## Achados
| ID | Sev | Regra | Caminho de exploração | path:line |

## Correções verificadas
| Achado | Antes | Depois | Regressão legítima |

## Não verificado
| Item | Motivo |
```
