# diagrams — diagramas

Diagramas referenciados pelos volumes.

Regras deste diretório:

1. **Formato textual, versionável.** Mermaid ou similar em arquivo `.md`. Imagem binária não aparece em diff, e
   um diagrama que ninguém revisa é um diagrama que mente em poucos meses.
2. **Todo diagrama tem dono e volume de origem**, declarado no arquivo.
3. **Diagrama não substitui regra.** Ele mostra estrutura; a norma continua sendo o texto com ID.
4. **Diagrama de arquitetura declara a data e a versão** que representa. Diagrama sem data é arqueologia.

Estado atual: vazio. Este diretório existe para os diagramas de fronteira de módulo e fluxo de deploy, que são
os dois casos em que texto é comprovadamente pior que imagem.
