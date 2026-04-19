const API_URL = "http://localhost:8000";
const customerId = "CUST0001"; // Demo customer

function previewImage() {
    const input = document.getElementById('image-input');
    const container = document.getElementById('image-preview-container');
    const nameSpan = document.getElementById('image-preview-name');
    
    if (input.files && input.files[0]) {
        nameSpan.innerText = `📎 ${input.files[0].name}`;
        container.style.display = 'block';
    }
}

function clearImage() {
    const input = document.getElementById('image-input');
    const container = document.getElementById('image-preview-container');
    input.value = '';
    container.style.display = 'none';
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    const imageInput = document.getElementById('image-input');
    
    if (!message && !imageInput.files[0]) return;

    // Add user message to UI
    appendMessage('user', message || (imageInput.files[0] ? "Sent an image" : ""));
    input.value = '';

    // Show typing indicator
    const typingIndicator = document.getElementById('typing-indicator');
    typingIndicator.style.display = 'block';

    // Prepare Multipart Form Data
    const formData = new FormData();
    formData.append('customer_id', customerId);
    formData.append('message', message);
    if (imageInput.files[0]) {
        formData.append('image', imageInput.files[0]);
    }

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        // Hide typing indicator
        typingIndicator.style.display = 'none';
        clearImage();

        // Add bot response to UI
        appendMessage('bot', data.response);

        // Update sentiment UI
        const sentimentVal = document.getElementById('sentiment-val');
        if (sentimentVal) {
            sentimentVal.innerText = data.sentiment.charAt(0).toUpperCase() + data.sentiment.slice(1);
            if (data.sentiment === 'angry') {
                sentimentVal.style.color = '#ef4444';
            } else {
                sentimentVal.style.color = '#10b981';
            }
        }

    } catch (error) {
        typingIndicator.style.display = 'none';
        appendMessage('bot', "Sorry, I'm having trouble connecting to the server. Please try again later.");
        console.error("Chat Error:", error);
    }
}

function appendMessage(sender, text) {
    const container = document.getElementById('chat-messages');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerText = text;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
