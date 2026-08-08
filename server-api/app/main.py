from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, ConfigDict
from datetime import datetime

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

    # Resolve o conflito de namespace do Pydantic V2
    model_config = ConfigDict(protected_namespaces=())

@app.get("/")
async def health_check():
    return {"status": "online", "message": "Servidor de Avaliação Ativo", "gpu_mode": "enabled"}

@app.post("/api/evaluate")
async def evaluate_interaction(payload: InteractionPayload, background_tasks: BackgroundTasks):
    return {
        "status": "received",
        "message": "Interação recebida. Avaliação em andamento...",
        "payload_recebido": payload.model_dump() # Usando o padrão V2
    }