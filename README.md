# Arquitetura de Software Multi-Agente com RAG: Detecção Algorítmica de Alucinações Utilizando Entropia Semântica e Métricas RAGAS

Este repositório contém o código-fonte, a infraestrutura e a documentação acadêmica de um Trabalho de Conclusão de Curso em Engenharia da Computação focado na mitigação e observabilidade de alucinações factuais em Large Language Models (LLMs).

## 🎯 Objetivo do Projeto
Desenvolver um artefato baseado em Design Science Research (DSR): uma extensão de navegador integrada a um orquestrador multi-agente local. O sistema atua como um avaliador assíncrono (padrão Gerador-Avaliador) que intercepta interações do usuário com LLMs comerciais, injeta contexto seguro (RAG invisível) e exibe métricas de confiabilidade (Fidelidade, Relevância e Entropia Semântica) em tempo real.

## 🏗️ Topologia e Restrições de Hardware
O projeto foi desenhado sob a premissa de processamento na borda (*edge computing*) com recursos estritamente limitados. Toda a orquestração e cálculo de métricas rodam localmente:
*   **Servidor:** Ubuntu Server (CLI)
*   **Aceleração de Hardware:** Pass-through configurado para NVIDIA GeForce 940MX (2GB VRAM).
*   **Inferência Local:** Modelos altamente quantizados (GGUF) rodando via Ollama e orquestrados por LangGraph, otimizados para não exceder o teto de memória disponível.

## 📂 Estrutura do Monorepo
*   `/client-extension`: Proxy interceptador e interface do usuário (JavaScript).
*   `/server-api`: Motor de avaliação, cálculo de entropia e banco de dados (Python/FastAPI).
*   `/infra`: Ambientes conteinerizados via Docker.
*   `/docs`: Fundamentação teórica, QFD (Engenharia de Requisitos) e texto da monografia.

## 🚀 Como iniciar (Guia de Reprodutibilidade)
*(Esta seção será preenchida ao longo do desenvolvimento com os comandos `docker-compose up`, instalação da extensão no modo desenvolvedor, etc.)*