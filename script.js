// script.js
const chatBox = document.getElementById("chat-box");

function addMessage(content, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("chat-message", sender);
    messageElement.textContent = content;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Mantener el scroll abajo
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const userMessage = input.value.trim();

    if (userMessage === "") return;

    addMessage(userMessage, "user");
    input.value = "";

    // Enviar mensaje a Anything LLM
    try {
        const response = await fetch("http://192.168.1.7:5000/v1/models/anything_llm/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "input": userMessage,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            addMessage(data.response || "Lo siento, no puedo responder en este momento.", "bot");
        } else {
            addMessage("Hubo un problema con la conexión al servidor.", "bot");
        }
    } catch (error) {
        addMessage("Error de conexión. Verifica la URL o tu conexión de red.", "bot");
    }
}
