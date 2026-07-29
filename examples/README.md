# examples — exemplos de implementação

Código citado pelos volumes, quando o exemplo é longo demais para caber no corpo da regra sem quebrar a
leitura.

Regras deste diretório:

1. **Todo exemplo cita a regra que prova**, por ID, no topo do arquivo. Exemplo que não prova nada é ruído
   (`A-010`).
2. **Domínio de SaaS real.** Pedido, assinatura, inquilino, cobrança, catálogo. Nunca `foo`, `bar` ou `Test1`.
3. **Par bom/ruim quando o contraste ensina.** O ruim vem primeiro, com o comentário do defeito; o bom vem
   depois, sem comentário elogioso.
4. **Framework declarado.** O núcleo do EOS é agnóstico de stack (`CON-006`); quando o exemplo depende de
   framework, o arquivo diz qual e se apresenta como ilustração.
5. **Exemplo que não compila é defeito.** Um exemplo errado num manual normativo é pior que ausência: ele é
   copiado.

Estado atual: vazio. Os volumes ainda cabem com os exemplos embutidos. Este diretório existe para quando
deixarem de caber.
