# Checklist — Segurança (OWASP Top 10)

Regra que governa este checklist: **o ônus da prova é de quem afirma que está seguro.** Item que você
não conseguiu verificar é reportado como não verificado — nunca presumido em ordem.

Norma completa: [Volume 06 — Segurança](../06-seguranca.md).

---

## 1. Controle de acesso — comece aqui, sempre

Para **cada** ponto de entrada:

- [ ] Exige autenticação (ou é público por decisão declarada)?
- [ ] Verifica autorização para a **operação**?
- [ ] Verifica autorização para o **objeto específico**? ← a que costuma faltar
- [ ] Aplica filtro de tenant na camada de dados?

Caminhos que a revisão esquece:

- [ ] Endpoint de lote: autoriza cada item, ou só o primeiro?
- [ ] Exportação e relatório: mesmas regras da leitura individual?
- [ ] Recurso aninhado (`/pedidos/{a}/itens/{b}`): `b` pertence a `a`?
- [ ] Escrita e exclusão, não só leitura.
- [ ] Parâmetro de filtro, busca e ordenação: alcança dado de outro tenant?
- [ ] Campo de papel, plano, preço ou permissão vindo do cliente é ignorado explicitamente?
- [ ] Rota nova nasce inacessível (negar por omissão)?
- [ ] Webhook e callback verificam o remetente?
- [ ] Job em background roda com a autoridade do solicitante ou com privilégio total?

`S0` se: falta autorização por objeto · falta filtro de tenant.

## 2. Falha criptográfica

- [ ] Senha com hash lento e específico (bcrypt/argon2/scrypt), custo adequado.
- [ ] TLS em trânsito, sem exceção "interna".
- [ ] Dado sensível criptografado em repouso, chave gerenciada e rotacionável.
- [ ] Nenhum algoritmo obsoleto; nenhuma criptografia caseira.
- [ ] Token gerado com aleatoriedade criptográfica.
- [ ] Comparação de segredo em tempo constante.

## 3. Injeção

- [ ] Toda consulta parametrizada. Nenhuma concatenação de entrada. (`S0`) (`SEC-019`)
- [ ] Vale para NoSQL, comando de sistema, LDAP e template. (`SEC-019`, `SEC-020`)
- [ ] SQL dinâmico: coluna/sort/tabela só via allowlist; valores só com bind/`USING`. (`S0`) (`SEC-067`, `SEC-069`)
- [ ] Filtro montado em string (PostgREST `.or()`, DSL, where serializado): sem texto cru; preferir API tipada; sanitizar gramática se inevitável. (`S0`) (`SEC-068`)
- [ ] Cliente privilegiado (service role / admin): IDs e termos de integração com formato fechado antes de interpolar. (`S0`) (`SEC-070`)
- [ ] Helper único de sanitização de filtro onde a DSL exige interpolação. (`SEC-071`)
- [ ] Escape na saída por contexto: HTML, atributo, URL, JavaScript. (`SEC-021`)
- [ ] Nenhuma inserção de HTML não confiável; rich text só com sanitizer dedicado. (`SEC-022`)
- [ ] HTML fora do SPA: e-mail, callback OAuth/erro, `body_html`, recibo HTML no servidor. (`S1`) (`SEC-072`, `SEC-075`)
- [ ] `href`/`src`/`action`: só `http(s)` (ou relativo documentado). (`SEC-073`)
- [ ] Filtro parcial (`.replace(<>&)`, strip de tags) não conta como escape. (`S1`) (`SEC-074`)
- [ ] Caça mecânica anexada antes de “sem XSS” (`dangerouslySetInnerHTML`, `innerHTML`, `text/html`). (`SEC-076`)
- [ ] Nenhuma execução de entrada como código, comando ou template. (`SEC-020`)
- [ ] Validação por lista de permitidos, não de proibidos. (`SEC-069`)
- [ ] Nome de arquivo, cabeçalho e destino de redirecionamento validados. (`SEC-024`)

## 4. Design inseguro

- [ ] Reautenticação em fluxo sensível (senha, e-mail, meio de pagamento). (`SEC-025`)
- [ ] Lockout de autenticação no servidor de identidade (por conta/fator, teto + janela). (`S1`) (`SEC-026`)
- [ ] Controle **não** é só UI, Edge opcional ou rate limit por IP. (`SEC-026`)
- [ ] Janela cheia rejeita mesmo com senha correta na tentativa atual. (`SEC-026`)
- [ ] Login, reset/recovery, OTP/MFA e códigos de recuperação cobertos. (`SEC-026`)
- [ ] Captcha (se usado) complementa o lockout; Dashboard e cliente alinhados. (`SEC-026`)
- [ ] Prova: N+1 falhas bloqueiam; API Auth direta (sem UI) também bloqueia. (`SEC-026`, `SEC-064`)
- [ ] Erro de login não revela se o e-mail existe. (`SEC-027`)
- [ ] Operação irreversível confirmada e registrada. (`SEC-028`)
- [ ] Abuso modelado: o que faria um usuário mal-intencionado **com credencial válida**? (`SEC-029`)

## 5. Configuração insegura

- [ ] Nenhuma credencial padrão em produção.
- [ ] Depuração e mensagens detalhadas desligadas.
- [ ] CORS restrito. `*` com credencial é `S0`.
- [ ] Cabeçalhos de segurança presentes (política de conteúdo, HSTS, `nosniff`, referenciador,
      enquadramento).
- [ ] Armazenamento privado por padrão. (`SEC-035`)
- [ ] Menor privilégio em toda credencial de serviço. (`SEC-036`, `DAT-038`)
- [ ] Nenhum endpoint de diagnóstico ou console de administração exposto. (`SEC-037`)
- [ ] BaaS / API de dados no cliente: chave publishable modelada como atacante — não “esconder a chave”. (`S0`) (`SEC-077`)
- [ ] Allowlist versionada de todo `GRANT` a `anon`/`public`/`authenticated` (tabela, view, RPC, storage). (`S0`) (`SEC-078`)
- [ ] Coluna secreta na linha pública: `GRANT` por coluna ou view de projeção — RLS de linha não basta. (`S0`) (`SEC-079`)
- [ ] Sem `DEFAULT PRIVILEGES` doando `EXECUTE`/`SELECT` ao papel público. (`S0`) (`SEC-080`)
- [ ] RPC `SECURITY DEFINER` pública catalogada, com authz/tenant no corpo e prova. (`S0`) (`SEC-081`)
- [ ] `REVOKE` só com cliente alinhado (duas fases). (`SEC-082`, `DAT-031`)
- [ ] Suite CI/SQL falha se a superfície pública divergir da allowlist. (`SEC-083`)
- [ ] Bucket legado público após migração para privado/assinado = superfície ainda aberta. (`S1`) (`SEC-084`)

## 6. Componentes vulneráveis

- [ ] Varredura automatizada no pipeline, bloqueando crítico e alto.
- [ ] Nenhuma vulnerabilidade crítica ou alta em aberto.
- [ ] Nenhuma dependência abandonada sem risco registrado.
- [ ] Toda supressão tem **análise de explorabilidade escrita**.
- [ ] Nenhum pacote suspeito de typosquatting.

## 7. Autenticação e sessão

- [ ] Sessão expira, renova com segurança, e é invalidada em logout e troca de senha.
- [ ] Token com escopo, vida curta e possibilidade de revogação.
- [ ] Identificador de sessão regenerado após autenticar.
- [ ] MFA disponível para conta e operação sensível.
- [ ] Nenhum segredo de longa duração no cliente. Chave em bundle de frontend é `S0`.
- [ ] Proteção contra requisição forjada entre sites em fluxo com cookie.

## 8. Integridade

- [ ] Script externo, artefato de build e imagem de contêiner com integridade verificada.
- [ ] Nenhuma desserialização de dado não confiável em objeto executável.
- [ ] Pipeline revisado como código.
- [ ] Artefato de deploy assinado ou com hash verificado.

## 9. Registro e monitoramento

- [ ] Eventos de segurança registrados: autenticação, mudança de permissão, acesso a dado sensível,
      operação destrutiva.
- [ ] **Nenhuma senha, token, chave, cartão ou dado pessoal em log.** (`S0`)
- [ ] Mascaramento no ponto de escrita, não no visualizador.
- [ ] Log correlacionável e com retenção suficiente.
- [ ] Alerta para pico de falha de autenticação e acesso em volume anômalo.

## 10. SSRF

- [ ] URL fornecida pelo usuário passa por lista de permitidos.
- [ ] Faixas internas e endpoint de metadados de nuvem bloqueados.
- [ ] Redirecionamento não é seguido cegamente.
- [ ] Verificado em: importação por URL, webhook, miniatura, conversão de documento.

---

## Segredos

- [ ] Nenhum no repositório, no histórico, no cliente, no log ou no artefato de build.
- [ ] Gerenciador de segredos, injeção em execução, rotação sem deploy.
- [ ] Varredura automática no pipeline e em pre-commit.
- [ ] **Se encontrado: rotacionar primeiro, remover depois.** Nunca o inverso. (`SEC-052`)
- [ ] Segredo de provedor fora de `VITE_` / `NEXT_PUBLIC_` / equivalente. (`S0`) (`SEC-085`)
- [ ] Resposta de configuração não ecoa `api_key` / `*_token` / `*_secret`; revelação admin-only. (`S1`) (`SEC-086`)
- [ ] Webhook com segundo fator (header ou HMAC) + fail-closed; comparação em tempo constante. (`S1`) (`SEC-087`, `SEC-017`)
- [ ] Caça mecânica anexada antes de “sem chave de integração exposta”. (`SEC-088`)

## Dados pessoais

- [ ] Inventário: o que existe, onde, por quanto tempo, quem acessa, por quê.
- [ ] Nenhum em log. (`S0`)
- [ ] Nenhum em ambiente de desenvolvimento ou em fixture de teste.
- [ ] Retenção declarada e eliminação automatizada.
- [ ] Direito de eliminação tecnicamente possível, inclusive em backup e analytics.
- [ ] Compartilhamento com terceiro é decisão registrada.

---

## Regras de bloqueio

Nenhuma entrega passa com qualquer um destes:

1. Endpoint sem autorização por objeto
2. Consulta multi-tenant sem filtro de isolamento
3. Segredo no repositório ou no cliente
4. Concatenação de entrada em consulta ou comando
5. Senha com hash inadequado
6. Dado pessoal em log
7. Vulnerabilidade crítica ou alta sem análise registrada
8. CORS permissivo com credencial
9. Dado sensível sem TLS
10. Ausência de limite de tentativas em autenticação (`SEC-026`: lockout no IdP por conta; UI/IP não bastam)

---

## Verificação de uma correção de segurança

Testes passando não basta. Demonstre:

```
Antes: <requisição do usuário B contra recurso do usuário A> → 200, dados retornados
Depois: <mesma requisição>                                    → 403
Regressão: <requisição legítima do usuário A>                 → 200, inalterado
```
