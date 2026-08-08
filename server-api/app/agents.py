from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator
import math

# 1. Definição do Estado (A Memória Compartilhada do Grafo)
# O StateDict garante a tipagem rigorosa exigida na engenharia de software
class AgentState(TypedDict):
    user_prompt: str
    llm_response: str
    model_name: str
    faithfulness_score: float
    relevance_score: float
    entropy_score: float
    final_status: str

# 2. Nós de Execução (Papéis dos Agentes)

def dispatcher_node(state: AgentState):
    """
    Nó de Entrada: O Agente Coordenador que recebe a carga do Client-Side
    e prepara a bifurcação paralela.
    """
    print(f"[Coordenador] Interceptação recebida. Modelo Base: {state.get('model_name')}")
    return {} # Não altera o estado, apenas roteia

def agent_ragas_metrics(state: AgentState):
    """
    Agente Avaliador RAGAS: Focado na Fidelidade e Relevância.
    Neste nó, o motor Ollama será chamado para checar a validade do contexto.
    """
    print("[Avaliador RAGAS] Calculando Fidelity e Answer Relevancy...")
    # TODO: Integrar a chamada da biblioteca 'ragas' com o modelo local GGUF
    return {"faithfulness_score": 0.88, "relevance_score": 0.95}

def agent_semantic_entropy(state: AgentState):
    """
    Agente de Monitoramento de Entropia: O núcleo matemático do TCC.
    Quantifica a incerteza probabilística nas respostas.
    """
    print("[Avaliador Entropia] Injetando variância e calculando dispersão semântica...")
    
    # A implementação completa exigirá gerar amostras com alta temperatura no Ollama
    # e calcular a similaridade de cosseno. Por hora, estabelecemos o fluxo algébrico:
    # SE(x) = - \sum P(c|x) * log(P(c|x))
    
    mock_entropy = 0.12 # Valor baixo = Alta confiabilidade / Baixa incerteza
    return {"entropy_score": mock_entropy}

def aggregator_node(state: AgentState):
    """
    Nó de Convergência: Analisa as métricas de qualidade e emite o parecer final.
    """
    print("[Agregador] Consolidando governança do artefato...")
    
    # Lógica de bloqueio algorítmico baseada em limiares (Thresholds)
    if state.get("entropy_score", 1.0) > 0.5 or state.get("faithfulness_score", 0.0) < 0.7:
        status = "ALUCINACAO_DETECTADA"
    else:
        status = "INFORMACAO_CONFIAVEL"
        
    return {"final_status": status}

# 3. Compilação do Grafo (DAG) - Otimizado para Edge Computing (2GB VRAM)
workflow = StateGraph(AgentState)

# Adicionando os nós ao grafo
workflow.add_node("dispatcher", dispatcher_node)
workflow.add_node("ragas_evaluator", agent_ragas_metrics)
workflow.add_node("entropy_evaluator", agent_semantic_entropy)
workflow.add_node("aggregator", aggregator_node)

# Desenhando as arestas (Fluxo de Controle Sequencial)
workflow.set_entry_point("dispatcher")

# Execução Sequencial: Mitiga o gargalo de VRAM impedindo acessos simultâneos ao Ollama
workflow.add_edge("dispatcher", "ragas_evaluator")
workflow.add_edge("ragas_evaluator", "entropy_evaluator")
workflow.add_edge("entropy_evaluator", "aggregator")

# Fim do ciclo
workflow.add_edge("aggregator", END)

# O aplicativo compilado que será exportado para a API
evaluation_graph = workflow.compile()