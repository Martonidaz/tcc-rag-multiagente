from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime

# Inicialização da API
app = FastAPI(
    title="Orquestrador RAG Multiagente",
    description="API para avaliação de incerteza semântica e métricas RAGAS",
    version="1.0.0"
)

# Definição do Schema (O formato do dado que a extensão vai enviar)
class InteractionPayload(BaseModel):
    user_prompt: str
    llm_response: str
    model_name: str # Ex: "ChatGPT", "Gemini", "Claude"
    timestamp: datetime = datetime.now()

@app.get("/")
async def health_check():
    """Rota para verificar se o servidor está online."""
    return {"status": "online", "message": "Servidor de Avaliação Ativo", "gpu_mode": "enabled"}

@app.post("/api/evaluate")
async def evaluate_interaction(payload: InteractionPayload, background_tasks: BackgroundTasks):
    """
    Recebe a interação capturada pela extensão.
    O processamento do LangGraph vai ocorrer em 'background' para não travar o navegador do usuário.
    """
    
    # Aqui chamaremos a função do LangGraph futuramente:
    # background_tasks.add_task(run_evaluation_graph, payload)
    
    return {
        "status": "received",
        "message": "Interação recebida. Avaliação em andamento...",
        "payload_recebido": payload.dict()
    }