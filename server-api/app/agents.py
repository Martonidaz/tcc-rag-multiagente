# Esqueleto estrutural dos Agentes (A ser preenchido com a lógica do LangGraph)

def agent_ragas_faithfulness(state: dict):
    """
    Nó A do Grafo: Avalia se a resposta da LLM é fiel ao contexto recuperado.
    """
    print("Executando avaliação de Fidelidade (RAGAS)...")
    # Lógica de chamada ao Ollama para calcular nota de 0 a 1
    return {"faithfulness_score": 0.85}

def agent_ragas_relevance(state: dict):
    """
    Nó B do Grafo: Avalia se a resposta atende diretamente à pergunta do usuário.
    """
    print("Executando avaliação de Relevância (RAGAS)...")
    # Lógica de cálculo vetorial (Embeddings via ChromaDB)
    return {"relevance_score": 0.90}

def agent_semantic_entropy(state: dict):
    """
    Nó C do Grafo: Induz variância no modelo local e calcula a entropia para detectar alucinação.
    """
    print("Calculando Entropia Semântica...")
    # Lógica baseada na Fórmula de Farquhar (Agrupamento de significados)
    return {"entropy_score": 0.2}

def aggregator_node(state: dict):
    """
    Nó Final: Consolida as métricas, salva no Banco de Dados (Perfil do Usuário) 
    e prepara o resultado para o frontend.
    """
    print("Consolidando métricas e finalizando o grafo.")
    return {"final_status": "completed"}