function toggleChatbot() {
    const box = document.getElementById("chatbot-box");
    box.style.display = box.style.display === "none" ? "block" : "none";
}

function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendMessage() {
    const input = document.getElementById("chatbot-input");
    const message = input.value.trim();
    if (!message) return;

    addMessage("You", message);
    input.value = "";

    const typingIndicator = document.getElementById("typing-indicator");
    typingIndicator.style.display = "block";

    fetch("/chatbot/response/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        typingIndicator.style.display = "none";
        addMessage("Bot", data.response);
    })
    .catch(error => {
        console.error("Chatbot error:", error);
        typingIndicator.style.display = "none";
        addMessage("Bot", "⚠️ Error connecting to AI.");
    });
}

function addMessage(sender, text) {
    const messagesDiv = document.getElementById("chatbot-messages");
    const messageElement = document.createElement("div");
    messageElement.className = sender === "You" ? "user-message" : "bot-message";
    messageElement.innerHTML = `<span>${text}</span>`;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

function addTypingBubble() {
    const chatBox = document.getElementById("chat-messages");
    const bubble = document.createElement("div");
    bubble.className = "message bot typing";
    bubble.innerHTML = `<span class="dot"></span><span class="dot"></span><span class="dot"></span>`;
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
    return bubble;
}

function removeTypingBubble(bubble) {
    if (bubble && bubble.parentNode) {
        bubble.parentNode.removeChild(bubble);
    }
}
