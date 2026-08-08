// Esqueleto estrutural: Interceptador de DOM

console.log("AuditAI: Content script carregado com sucesso.");

// Função mock para simular a extração do par (Prompt + Resposta)
function extractInteractionData() {
    // No futuro, aqui teremos seletores específicos para o DOM de cada LLM
    const mockData = {
        user_prompt: "Explique o padrão DSR",
        llm_response: "DSR (Design Science Research) é uma metodologia...",
        model_name: "Mock_LLM"
    };
    return mockData;
}

// Função mock para enviar o payload para nossa API local no WSL
async function sendToLocalBackend(payload) {
    try {
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        console.log("AuditAI: Sucesso ao enviar para o backend local", result);
    } catch (error) {
        console.error("AuditAI: Falha na comunicação com o servidor local", error);
    }
}