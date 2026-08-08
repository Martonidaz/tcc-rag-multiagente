# Fase 0 - Fundação e Topologia do Repositório

## Objetivo Arquitetural
Estabelecer um ambiente de controle de versão unificado (Monorepo) que abrigue simultaneamente o código-fonte (frontend e backend), a infraestrutura (DevOps) e a documentação acadêmica (DSR/QFD).

## Decisões Técnicas e Instruções
A estrutura de pastas foi dividida de forma semântica para respeitar o princípio de Separação de Preocupações (*Separation of Concerns*):

*   **`/client-extension`**: Isolamento do código JavaScript (frontend). Garante que as dependências da interface não interfiram no backend.
*   **`/server-api`**: Isolamento do código Python (FastAPI/LangGraph).
*   **`/infra`**: Centralização dos scripts de provisionamento de ambiente (Docker).
*   **`/docs`**: Repositório da pesquisa científica, matrizes QFD e o documento final do TCC.

O arquivo `README.md` raiz foi introduzido não apenas como um guia, mas como o **Sumário Executivo do Projeto**, essencial para que a banca avaliadora compreenda a topologia de *edge computing* (processamento na borda) antes mesmo de ler a base de código.