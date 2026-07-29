# Norma — Segurança

Regra que governa esta norma inteira: **nesta camada, o ônus da prova se inverte.** Não é preciso
provar que existe uma vulnerabilidade para bloquear; é preciso provar que o caminho está seguro.
Confiança `MEDIUM` já bloqueia em autenticação, autorização, pagamento e dado pessoal.

Organizada pela OWASP Top 10, com as verificações práticas de cada item.
Checklist executável: [`checklists/seguranca-owasp.md`](../checklists/seguranca-owasp.md).

---

## S1. Falha de controle de acesso

**A vulnerabilidade mais comum e mais grave em aplicações reais.**

- **Autorização por objeto, não por rota.** Verificar "é usuário logado" ou "é admin" não basta:
  verifique se **este** sujeito pode agir sobre **este** recurso. `GET /pedidos/{id}` que só checa
  autenticação é `S0`.
- **Negar por omissão.** Rota, campo ou operação nova é inacessível até que a permissão seja
  declarada. Lista de exceções ("estas rotas são públicas") é mais segura do que lista de
  proteções.
- **Verificação no servidor.** Ocultar um botão não é controle de acesso.
- **Isolamento de tenant obrigatório** em toda consulta de sistema multi-inquilino. Uma consulta
  sem o filtro de tenant é `S0`. Prefira aplicar no nível mais interno possível (política no banco,
  camada de acesso obrigatória) — não na disciplina de cada desenvolvedor.
- **Autorização também na escrita, no lote e na exportação.** Endpoints de lote e relatórios são
  onde a verificação costuma faltar.
- **Não permita escolher o próprio papel.** Campo de papel, plano ou permissão vindo do cliente
  precisa ser explicitamente ignorado.

## S2. Falha criptográfica

- Senha com algoritmo de hash lento e específico (bcrypt, argon2, scrypt), com custo adequado.
  Nunca hash rápido, nunca criptografia reversível.
- TLS obrigatório em trânsito; sem exceção "interna".
- Dado pessoal sensível criptografado em repouso, com chave gerenciada e rotacionável.
- Sem algoritmo obsoleto (MD5, SHA1 para senha, DES) e sem criptografia caseira.
- Aleatoriedade criptográfica para token, e não gerador de números pseudoaleatórios comum.
- Comparação de segredo em tempo constante.

## S3. Injeção

- **Consulta parametrizada, sempre.** Concatenação de entrada em SQL é `S0`. Vale igualmente para
  NoSQL, comando de sistema, LDAP e template.
- **Escape por contexto na saída:** HTML, atributo, URL e JavaScript têm regras diferentes.
  Inserção de HTML não confiável é `S1`.
- **Nunca execute entrada** como comando, código ou template.
- **Validação por lista de permitidos**, não por lista de proibidos. Lista de proibidos sempre tem
  um caso a mais.
- Cuidado com injeção via nome de arquivo, cabeçalho e valor de redirecionamento.

## S4. Design inseguro

- Fluxos sensíveis (recuperação de senha, mudança de e-mail, alteração de pagamento) exigem
  reautenticação.
- Limite de tentativas em autenticação, com bloqueio progressivo.
- Não conte ao atacante o que existe: mensagem de erro de login não revela se o e-mail está
  cadastrado.
- Toda operação irreversível é confirmada e registrada.
- Modele o abuso, não só o uso: o que um usuário mal-intencionado com credencial válida faria?

## S5. Configuração insegura

- Sem credencial ou configuração padrão em produção.
- Modo de depuração e mensagens detalhadas desligados em produção.
- CORS restrito a origens conhecidas. `*` com credencial é `S0`.
- Cabeçalhos de segurança presentes: política de conteúdo, HSTS, `nosniff`, política de
  referenciador, controle de enquadramento.
- Armazenamento (bucket, blob) privado por padrão.
- Menor privilégio em toda credencial de serviço.
- Superfície mínima: sem endpoint de diagnóstico, sem console de administração exposto.

## S6. Componentes vulneráveis

- Varredura de dependências automatizada no pipeline, bloqueando severidade crítica e alta.
- Inventário de dependências conhecido; dependência abandonada é risco a ser registrado.
- Atualização como rotina, não como projeto anual.
- Ao suprimir um aviso, **registre a análise de explorabilidade**. Supressão sem análise é `S2`.
- Cuidado com typosquatting e com script de instalação de pacote.

## S7. Falha de autenticação e identificação

- Sessão com expiração, renovação segura e invalidação em logout e em troca de senha.
- Token com escopo, tempo de vida curto e possibilidade de revogação. Token que não pode ser
  revogado é uma decisão que exige ADR.
- Identificador de sessão regenerado após autenticar (evita fixação de sessão).
- MFA disponível para operações e contas sensíveis.
- Sem segredo de longa duração no cliente. Chave em bundle de frontend é `S0`.
- Proteção contra requisição forjada entre sites em fluxos baseados em cookie.

## S8. Falha de integridade

- Verifique a integridade e a origem de tudo que é executado: script externo, artefato de build,
  imagem de contêiner.
- Nunca desserialize dado não confiável em objeto executável.
- Pipeline de build é código, revisado como código. Comprometer o pipeline compromete tudo.
- Assinatura ou hash verificado em artefato de deploy.

## S9. Falha de registro e monitoramento

- Registre eventos de segurança: autenticação (sucesso e falha), mudança de permissão, acesso a
  dado sensível, operação destrutiva.
- **Nunca registre**: senha, token, chave, cartão, dado pessoal completo. Mascare no ponto de
  escrita, não no visualizador.
- Log correlacionável (id de requisição, sujeito, recurso) e com retenção suficiente para
  investigar.
- Alerta para padrão de abuso: pico de falha de autenticação, acesso em volume anômalo.
- Log é imutável para quem tem acesso à aplicação, na medida do possível.

## S10. Requisição forjada do lado do servidor (SSRF)

- Requisição para URL fornecida pelo usuário exige lista de permitidos de destino.
- Bloqueie faixas internas e endpoints de metadados de nuvem.
- Não siga redirecionamento cegamente.
- Aplica-se a: importação por URL, webhook, geração de miniatura, conversão de documento.

---

## Segredos

- **Nunca em código, nunca no repositório**, nem em histórico, nem em arquivo de exemplo com valor
  real.
- Gerenciador de segredos, injeção por ambiente em execução, rotação sem necessidade de deploy.
- Segredo exposto acidentalmente é `S0`: **rotacione primeiro**, remova do histórico depois.
  Remover do repositório sem rotacionar não resolve nada — o segredo já circulou.
- Varredura automática de segredo no pipeline e em pre-commit.
- Cuidado com o que vaza em: variável de ambiente de frontend, mapa de código-fonte, log de erro,
  imagem de contêiner, artefato de build.

## Dados pessoais

- **Inventário:** que dado pessoal existe, onde está, por quanto tempo, quem acessa, por quê.
- **Minimização:** não colete o que não usa. Cada campo é responsabilidade permanente.
- **Retenção:** prazo declarado e eliminação automatizada.
- **Direitos do titular:** acesso, correção e eliminação precisam ser tecnicamente possíveis —
  incluindo em backup, log e sistema analítico.
- **Sem dado pessoal em ambiente de desenvolvimento.** Use dado sintético ou anonimizado.
- Compartilhamento com terceiro é decisão registrada, não consequência de uma integração.

---

## Regras de bloqueio

Nenhuma entrega passa com qualquer um destes:

1. Endpoint sem verificação de autorização por objeto.
2. Consulta multi-tenant sem filtro de isolamento.
3. Segredo no repositório ou no cliente.
4. Concatenação de entrada em consulta ou comando.
5. Senha com hash inadequado.
6. Dado pessoal em log.
7. Vulnerabilidade crítica ou alta em dependência, sem análise registrada.
8. CORS permissivo com credencial.
9. Dado sensível trafegando sem TLS.
10. Ausência de limite de tentativas em autenticação.
