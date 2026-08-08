# Fase 2 - Backend, Orquestração e Resolução de Conflitos

## Objetivo Arquitetural
Criar a API Gateway (FastAPI) que atuará como o avaliador assíncrono no padrão **Gerador-Avaliador** e orquestrará os nós do LangGraph.

## A Correção do Ambiente Virtual (Ubuntu/WSL)
Durante a inicialização, o erro `uvicorn: command not found` evidenciou um mecanismo de segurança do Ubuntu 24.04 (PEP 668), que bloqueia instalações globais de pacotes Python para evitar a corrupção do sistema.
*   A instrução `python3 -m venv venv` criou um Ambiente Virtual local na pasta `server-api`. Isso garante que a instalação do FastAPI, RAGAS e LangGraph ocorra de forma enclausurada, garantindo que o código rode de forma idêntica em qualquer máquina, independente do SO hospedeiro.

## A Correção de Conflito do Pydantic
O aviso `UserWarning: Field "model_name" has conflict...` surgiu devido à arquitetura do Pydantic V2, que reserva o prefixo `model_` para métodos internos.
*   **Solução:** Implementou-se `model_config = ConfigDict(protected_namespaces=())` na classe `InteractionPayload`. Essa supressão de *namespace* previne falhas de validação, permitindo o uso da variável `model_name` sem comprometer a estabilidade da biblioteca.

## Decisões Técnicas de Orquestração
*   **Processamento Assíncrono:** O *endpoint* `app.post("/api/evaluate")` utiliza `BackgroundTasks`. Para que a extensão do navegador não cause travamentos (*timeout*) no cliente, a API devolve um status `200 OK` imediatamente e executa a avaliação dos agentes em segundo plano.
*   **Esqueletos (Mocks) do LangGraph:** Criou-se a separação de responsabilidades no arquivo `agents.py` (Nó A para Fidelidade, Nó B para Relevância e Nó C para Entropia Semântica), preparando o terreno para a implementação das métricas.