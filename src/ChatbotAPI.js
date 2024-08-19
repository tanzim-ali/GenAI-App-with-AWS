// src/ChatbotAPI.js
const API = {
  GetChatbotResponse: async (query, conversationHistory) => {
    const response = await fetch(`http://127.0.0.1:8000/chat_with_knowledge_base?query=${query}&knowledge_base_id=COAJXQGNUF`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ conversation_history: conversationHistory })
    });
    const data = await response.json();
    return data.response;
  }
};

export default API;
