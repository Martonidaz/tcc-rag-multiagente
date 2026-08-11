console.log("AuditAI: Content script ativado e monitorando o DOM.");

// Função para capturar a última interação da página (Exemplo genérico estruturado para ChatGPT/Gemini)
function captureLatestInteraction() {
    // Seletores simulados para demonstração de engenharia. 
    // No TCC, isso abrångera as tags HTML específicas do DOM de cada LLM.
    const userPrompts = document.querySelectorAll('div[data-message-author-role="user"], .user-query');
    const assistantResponses = document.querySelectorAll('div[data-message-author-role="assistant"], .model-response-text');

    let promptText = "Prompt de teste capturado via extensão";
    let responseText = "Resposta gerada pela LLM comercial.";

    if (userPrompts.length > 0) {
        promptText = userPrompts[userPrompts.length - 1].innerText;
    }
    if (assistantResponses.length > 0) {
        responseText = assistantResponses[assistantResponses.length - 1].innerText;
    }

    return {
        user_prompt: promptText,
        llm_response: responseText,
        model_name: "ChatGPT_Commercial_DOM"
    };
}

// Função assíncrona para despachar os dados para o backend no WSL
async function sendPayloadToLocalServer(data) {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/evaluate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log("AuditAI: Servidor local respondeu com sucesso:", result);
    } catch (error) {
        console.error("AuditAI Erro de Conexão: Certifique-se de que o Uvicorn está rodando no WSL.", error);
    }
}

// Gatilho de teste: Dispara a captura após 5 segundos da página carregada
setTimeout(() => {
    const interactionData = captureLatestInteraction();
    sendPayloadToLocalServer(interactionData);
}, 5000);