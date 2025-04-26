// /static/script.js

// Wait for the entire DOM to load before attaching event listeners
document.addEventListener("DOMContentLoaded", function() {
    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    // Send message when the "Send" button is clicked
    sendBtn.addEventListener("click", sendMessage);

    // Allow sending the message by pressing Enter key
    userInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    // Core function to send user's message to the server
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return; // Do nothing if input is empty

        appendMessage("user", message); // Show user's message in the chat
        userInput.value = ""; // Clear the input box

        appendTypingDots(); // Show typing dots while waiting for server response

        // Send the message to the backend via POST request
        fetch("/get", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            removeTypingDots(); // Remove typing dots once response is received
            appendMessage("bot", data.response); // Display bot's response
        })
        .catch(error => {
            removeTypingDots(); // Always remove typing dots, even on error
            appendMessage("bot", "Oops! Something went wrong."); // Show error message to user
            console.error("Error:", error); // Log the error in the console
        });
    }

    // Function to display a chat message (user or bot)
    function appendMessage(sender, text) {
        const messageEl = document.createElement("div");
        messageEl.classList.add(sender === "user" ? "user-message" : "bot-message");
        messageEl.textContent = text;
        chatBox.appendChild(messageEl);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
    }

    // Show typing dots animation while the bot is "thinking"
    function appendTypingDots() {
        const typingDots = document.createElement("div");
        typingDots.classList.add("bot-message");
        typingDots.setAttribute("id", "typing-dots");
        typingDots.innerHTML = "<span class='typing-dots'>...</span>";
        chatBox.appendChild(typingDots);
        chatBox.scrollTop = chatBox.scrollHeight; // Keep chat scrolled down
    }

    // Remove typing dots once the bot sends a response
    function removeTypingDots() {
        const dots = document.getElementById("typing-dots");
        if (dots) {
            dots.remove();
        }
    }
});
