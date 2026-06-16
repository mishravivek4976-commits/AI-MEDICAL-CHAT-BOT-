from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

# Simulated medical AI response
def get_medical_response(user_message):
    """
    Medical chatbot response generator
    Replace this with your actual AI model (TensorFlow, PyTorch, etc.)
    """
    user_message = user_message.lower()
    
    # Medical symptom database
    medical_db = {
        "fever": "🌡️ Fever detected. Symptoms: High temperature, chills, body aches. Recommendation: Rest, stay hydrated, take paracetamol, consult doctor if persists >3 days.",
        "cough": "🫁 Cough detected. Symptoms: Throat irritation, chest discomfort. Recommendation: Stay hydrated, use cough drops, avoid cold foods, consult doctor if cough lasts >2 weeks.",
        "headache": "🤕 Headache reported. Symptoms: Head pain, dizziness. Recommendation: Rest in dark room, drink water, take rest, apply cold compress. Seek help if severe.",
        "cold": "🤒 Common cold detected. Symptoms: Runny nose, sneezing, mild fever. Recommendation: Rest, vitamin C, warm fluids, steam inhalation.",
        "flu": "🦠 Influenza symptoms. Recommendation: Rest, antiviral medication, consult doctor immediately.",
        "throat": "🫂 Sore throat detected. Recommendation: Salt water gargle, honey, warm tea, rest voice.",
        "stomach": "🤢 Stomach issues. Recommendation: Light diet, clear fluids, rest, probiotics. Avoid spicy food.",
        "chest pain": "⚠️ CHEST PAIN ALERT - Seek immediate medical attention! Call emergency services.",
        "breathing": "🚨 Breathing difficulty detected. Seek immediate medical help!",
    }
    
    # Check for keywords in user message
    for keyword, response in medical_db.items():
        if keyword in user_message:
            return response
    
    return "📋 Please describe your symptoms in detail (fever, cough, headache, cold, flu, throat, stomach, chest pain, breathing, etc.) for accurate diagnosis guidance."

@app.get("/")
def home():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🏥 AI Medical Chatbot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                width: 100%;
                max-width: 600px;
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                opacity: 0.9;
                font-size: 0.95em;
            }
            .chat-box {
                height: 400px;
                overflow-y: auto;
                padding: 20px;
                background: #f7f7f7;
                border-bottom: 1px solid #e0e0e0;
            }
            .message {
                margin-bottom: 15px;
                padding: 12px 15px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .user-message {
                background: #667eea;
                color: white;
                margin-left: auto;
                text-align: right;
            }
            .bot-message {
                background: #e3f2fd;
                color: #333;
                margin-right: auto;
            }
            .input-area {
                padding: 20px;
                display: flex;
                gap: 10px;
            }
            #userInput {
                flex: 1;
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            #userInput:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1em;
                font-weight: 600;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            button:active {
                transform: translateY(0);
            }
            .footer {
                text-align: center;
                padding: 15px;
                background: #f7f7f7;
                color: #999;
                font-size: 0.85em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 AI Medical Chatbot</h1>
                <p>Your AI-powered health assistant - Describe your symptoms</p>
            </div>
            <div class="chat-box" id="chatBox"></div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Type your symptoms here..." />
                <button onclick="sendMessage()">Send</button>
            </div>
            <div class="footer">
                <p>⚠️ Disclaimer: This is an AI assistant. Always consult a licensed doctor for medical advice.</p>
            </div>
        </div>

        <script>
            const chatBox = document.getElementById('chatBox');
            const userInput = document.getElementById('userInput');

            function addMessage(text, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
                messageDiv.textContent = text;
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            async function sendMessage() {
                const message = userInput.value.trim();
                if (!message) return;

                addMessage(message, true);
                userInput.value = '';

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({text: message})
                    });
                    const data = await response.json();
                    addMessage(data.response, false);
                } catch (error) {
                    addMessage('Error: Unable to get response. Please try again.', false);
                }
            }

            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });

            // Welcome message
            setTimeout(() => {
                addMessage('Hello! 👋 Welcome to AI Medical Chatbot. Please describe your symptoms (e.g., fever, cough, headache) and I will provide guidance.', false);
            }, 500);
        </script>
    </body>
    </html>
    """)

@app.post("/chat")
def chat(message: Message):
    """Chat endpoint for medical queries"""
    response = get_medical_response(message.text)
    return {"response": response}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
