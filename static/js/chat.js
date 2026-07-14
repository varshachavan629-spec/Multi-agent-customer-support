// Get HTML elements
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");

// Send message function
function sendMessage() {

    const message = userInput.value.trim();

    if (message === "") {
        return;
    }

    addUserMessage(message);

    userInput.value = "";


    // Send message to Flask backend
    fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    })

    .then(response => response.json())

    .then(data => {

        addBotMessage(data.response);

    })

    .catch(error => {

        console.error("Error:", error);

        addBotMessage(
            "Sorry, something went wrong."
        );

    });

}

// User message
function addUserMessage(message) {

    const div = document.createElement("div");

    div.className = "message user-message";

    div.innerHTML = `
        <div class="message-content">
            ${message}
        </div>
    `;

    chatBox.appendChild(div);

    scrollToBottom();

}

// Bot message
function addBotMessage(message) {

    const div = document.createElement("div");

    div.className = "message bot-message";

    div.innerHTML = `
        <div class="message-content">
            🤖 ${message}
        </div>
    `;

    chatBox.appendChild(div);

    scrollToBottom();

}

// Auto scroll
function scrollToBottom() {

    chatBox.scrollTop = chatBox.scrollHeight;

}

// Button click
sendButton.addEventListener("click", sendMessage);

// Enter key
userInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        sendMessage();

    }

});