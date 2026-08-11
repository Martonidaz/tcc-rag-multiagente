from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.agents import evaluation_graph 

app = FastAPI(
    title="Orquestrador RAG Multiagente",
    description="API para avaliação de incerteza semântica e métricas RAGAS",
    version="1.0.0"
)

# Configuração de CORS para permitir requisições da Extensão de Navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção restritíriamos, mas para o TCC local liberamos tudo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    print(f"\n--- INICIANDO AUDITORIA VIA EXTENSÃO PARA: {payload_dict['model_name']} ---")
    initial_state = {
        "user_prompt": payload_dict["user_prompt"],
        "llm_response": payload_dict["llm_response"],
        "model_name": payload_dict["model_name"]
    }
    final_state = evaluation_graph.invoke(initial_state)
    print(f"--- RESULTADO DA AUDITORIA (EXTENSÃO): {final_state['final_status']} ---\n")

@app.post("/api/evaluate")
async def evaluate_interaction(payload: InteractionPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(execute_graph_task, payload.model_dump())
    return {
        "status": "processing",
        "message": "Payload da extensão recebido. Grafo multiagente acionado no WSL."
    }