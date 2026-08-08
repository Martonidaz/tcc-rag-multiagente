# Fase 3 - Frontend, Interceptação de DOM e Governança

## Parte 1: Arquitetura Client-Side (A Extensão)

### Objetivo Arquitetural
Desenvolver o componente *Client-Side* que atuará como um proxy transparente (homem-no-meio benigno), capturando interações em plataformas comerciais de IA e injetando a camada de observabilidade.

### Decisões Técnicas e Instruções
*   **`manifest.json` (Manifest V3):** Adotou-se o padrão mais recente e rigoroso de extensões. 
    *   A permissão `scripting` concede autoridade para injetar JavaScript nas abas autorizadas sem permissão global irrestrita.
    *   O `host_permissions` atua como uma *whitelist*, incluindo o backend local (`http://127.0.0.1:8000/*`). Isso resolve proativamente bloqueios de CORS (*Cross-Origin Resource Sharing*).
*   **`content.js`:** O interceptador de DOM. Utiliza a API `fetch` nativa para despachar o tráfego interceptado de forma assíncrona (promises) para a rota da API local.
*   **`popup.html`:** Interface desenvolvida em HTML puro e CSS embutido, garantindo renderização ultra-rápida e baixo consumo de RAM, atendendo aos requisitos de usabilidade do QFD.

---

## Parte 2: Governança de Repositório e Resolução de Conflitos

### Objetivo Arquitetural
Garantir a integridade, leveza e reprodutibilidade do Monorepo, isolando arquivos locais e impedindo o vazamento de binários do sistema para o ambiente de versionamento.

### O Incidente de Rastreamento (*Tracking Error*)
Durante o versionamento no WSL 2, o Git tentou indexar recursivamente o diretório `server-api/venv/`. O versionamento de um Ambiente Virtual é um erro crítico, pois carrega binários compilados especificamente para a arquitetura local (arquivos ELF do Linux), o que inviabilizaria a clonagem do projeto em outras máquinas.

### Decisões Técnicas de Correção
1.  **Configuração do `.gitignore`:** Elaborou-se um contrato rigoroso bloqueando:
    *   `venv/`, `__pycache__/`, `*.pyc`: Bloqueio de binários do Python.
    *   `node_modules/`: Bloqueio preventivo da árvore do frontend.
    *   `*.sqlite3`, `*.db`: Isolamento dos bancos de dados locais.
2.  **Limpeza de Cache (`git rm -r --cached`):** Intervenção cirúrgica na árvore do Git. Removeu a pasta `venv` estritamente do índice de monitoramento (memória do Git), preservando intactos todos os arquivos físicos no sistema WSL.
3.  **Aviso LF vs CRLF:** Evento benigno tratado automaticamente pelo Git devido à topologia híbrida entre o Kernel do Linux (WSL) e a interface do Windows.