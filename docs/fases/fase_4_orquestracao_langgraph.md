# Fase 4 - Orquestração Multiagente: Do Paralelismo Teórico ao Pipeline Sequencial

## 1. Ideação e Proposta Inicial
A proposta arquitetural primária para o núcleo decisório do artefato visava a implementação de um Grafo Direcionado Acíclico (DAG) com execução paralela (padrão *Fan-out*). O objetivo era que, após o nó inicial, o sistema disparasse a avaliação simultânea das métricas RAGAS e do cálculo da Entropia Semântica. A hipótese era de que o paralelismo reduziria a latência da API, entregando o resultado final de forma mais ágil para a extensão do navegador.

## 2. A Tentativa, o Erro e a Análise de Rastreamento
Durante a compilação do grafo via biblioteca LangGraph, a tentativa de adicionar duas arestas independentes saindo do mesmo nó coordenador resultou na seguinte interrupção do Uvicorn:

**Erro 1 (Ambiguidade de Roteamento):**
`ValueError: Already found path for dispatcher`
*Causa:* O motor do LangGraph, por padrão, exige um caminho determinístico. Ao tentar ramificar sem uma função condicional explícita, o sistema bloqueou a compilação.

**Erro 2 (Falha Assíncrona no ASGI):**
Ao tentarmos contornar a ambiguidade com arestas condicionais (`add_conditional_edges`) mal resolvidas, a API sofreu uma falha em tempo de execução ao tentar acessar o estado final:
`TypeError: 'NoneType' object is not subscriptable`
*Causa:* O grafo falhou em rotear a informação, encerrou a execução devolvendo um estado nulo (`None`), e o orquestrador colapsou ao tentar ler o campo `final_status`.

## 3. Avaliação Arquitetural e Restrições de Hardware (Edge Computing)
Embora os erros acima pudessem ser corrigidos com funções de roteamento mais complexas no código Python, a falha forçou uma revisão crítica dos requisitos não funcionais.

O projeto opera sob restrições severas de recursos computacionais. A infraestrutura provisionada conta com uma GPU NVIDIA GeForce 940MX limitada a 2GB de VRAM. Caso o sistema forçasse um paralelismo bem-sucedido via software, o motor Ollama seria acionado simultaneamente por duas *threads* diferentes (RAGAS e Entropia). Isso exigiria o carregamento de tensores de IA duplicados na memória gráfica, resultando em um inevitável colapso por esgotamento de memória (*Out Of Memory - OOM*) e travamento do *host*.

## 4. Decisão Técnica e Procedimentos de Correção
Diante da incompatibilidade entre o processamento paralelo e a infraestrutura local, decidiu-se pivotar a arquitetura do LangGraph para um **Fluxo Estruturado Sequencial (Pipeline)**. Esta abordagem sacrifica milissegundos de latência em favor da resiliência e da estabilidade absoluta do motor de inferência, impedindo gargalos de hardware.

**Implementação do Fluxo Corrigido:**
A memória compartilhada (`AgentState`) foi tipada rigorosamente e transita pelos nós autônomos na seguinte ordem determinística:

1. **Agente Coordenador (`dispatcher`)**: Gerencia o fluxo de controle, distribui tarefas iterativas e intercepta os resultados[cite: 1].
2. **Agente RAGAS (`ragas_evaluator`)**: Recebe o estado, avalia a fidelidade e relevância, e o repassa.
3. **Agente de Monitoramento de Entropia (`entropy_evaluator`)**: Recebe o estado atualizado e atua como um filtro algorítmico que quantifica as incertezas probabilísticas nas respostas geradas[cite: 1].
4. **Agregador (`aggregator`)**: Consolida as métricas avaliadas sequencialmente e emite o veredito de confiabilidade.

**Trecho do Código Refatorado:**
```python
# Desenhando as arestas (Fluxo de Controle Sequencial)
workflow.set_entry_point("dispatcher")

# Execução Sequencial: Mitiga o gargalo de VRAM impedindo acessos simultâneos ao Ollama
workflow.add_edge("dispatcher", "ragas_evaluator")
workflow.add_edge("ragas_evaluator", "entropy_evaluator")
workflow.add_edge("entropy_evaluator", "aggregator")
workflow.add_edge("aggregator", END)