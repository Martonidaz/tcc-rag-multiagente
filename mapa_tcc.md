# Mapa da Estrutura do TCC

Este arquivo serve como um guia dinâmico para a estrutura do repositório. Sua arquitetura foi formatada para dupla finalidade: leitura estruturada e renderização automatizada de mapas mentais para a documentação de Engenharia de Software.

## 🌳 Árvore de Diretórios (Formato Markmap / Universal)

* **`tcc-rag-multiagente/`** (Raiz do Monorepo)
  * `.github/`
    * `workflows/` (Regras de CI/CD e automação)
  * `client-extension/` (Frontend - Proxy Interceptador)
    * `package.json`
    * `public/`
      * `content.js` (Script de interceptação de DOM)
      * `manifest.json` (Contrato Manifest V3)
      * `popup.html` (Interface de métricas)
      * `popup.js`
    * `src/`
  * `docs/` (Documentação Acadêmica e DSR)
    * `arquitetura/`
    * `fases/`
      * `fase_0_fundacao.md`
      * `fase_1_infraestrutura.md`
      * `fase_2_backend.md`
      * `fase_3_frontend_e_governanca.md`
    * `qfd/` (Desdobramento da Função Qualidade)
    * `tcc_document/` (Arquivos LaTeX da Monografia)
  * `infra/` (DevOps e Provisionamento)
    * `docker/`
      * `docker-compose.yml` (Orquestração do GPU Passthrough)
    * `scripts/`
  * `server-api/` (Backend - Motor RAG e Avaliador)
    * `Dockerfile`
    * `requirements.txt`
    * `app/`
      * `agents.py` (Nós do LangGraph)
      * `main.py` (Gateway FastAPI)
    * `tests/` (Testes unitários via Pytest)
  * `.gitignore`
  * `mapa_tcc.md`
  * `README.md` (Sumário Executivo)

---

## 📊 Grafo Arquitetural (Formato Mermaid)
*No GitHub, o bloco abaixo é renderizado automaticamente como um diagrama visual.*

```mermaid
graph TD
    Root[tcc-rag-multiagente] --> Git[.github]
    Root --> Client[client-extension]
    Root --> Docs[docs]
    Root --> Infra[infra]
    Root --> Server[server-api]

    %% Expansão Client
    Client --> Public[public]
    Public --> contentJS(content.js)
    Public --> manifest(manifest.json)
    
    %% Expansão Docs
    Docs --> Fases[fases]
    Fases --> f1(Fases 0 a 3 em Markdown)
    Docs --> QFD[qfd]
    
    %% Expansão Infra
    Infra --> Docker[docker]
    Docker --> compose(docker-compose.yml)
    
    %% Expansão Server
    Server --> App[app]
    App --> agents(agents.py)
    App --> main(main.py)
    Server --> req(requirements.txt)