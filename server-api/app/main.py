from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Importa o grafo compilado que acabamos de construir
from app.agents import evaluation_graph 

app = FastAPI(
    title="Orquestrador RAG Multiagente",
    description="API para avaliação de incerteza semântica e métricas RAGAS",
    version="1.0.0"
)

class InteractionPayload(BaseModel):
    user_prompt: str
    llm_response: str
    model_name: str 
    timestamp: datetime = datetime.now()
    
    model_config = ConfigDict(protected_namespaces=())

@app.get("/")
async def health_check():
    return {"status": "online", "message": "Servidor de Avaliação Ativo", "gpu_mode": "enabled"}

def execute_graph_task(payload_dict: dict):
    """
    Função envelopadora para executar o LangGraph fora da thread principal,
    evitando bloqueios de I/O na API.
    """
    print(f"\n--- INICIANDO AUDITORIA PARA: {payload_dict['model_name']} ---")
    
    # Injeta o estado inicial no grafo
    initial_state = {
        "user_prompt": payload_dict["user_prompt"],
        "llm_response": payload_dict["llm_response"],
        "model_name": payload_dict["model_name"]
    }
    
    # Invoca o LangGraph
    final_state = evaluation_graph.invoke(initial_state)
    print(f"--- RESULTADO DA AUDITORIA: {final_state['final_status']} ---\n")

@app.post("/api/evaluate")
async def evaluate_interaction(payload: InteractionPayload, background_tasks: BackgroundTasks):
    
    # Adiciona a execução do grafo nas tarefas de segundo plano
    background_tasks.add_task(execute_graph_task, payload.model_dump())
    
    return {
        "status": "processing",
        "message": "Grafo multiagente acionado. Auditoria em andamento no servidor local."
    }