import React, { useState, useEffect } from "react";
import BotMessage from "./components/BotMessage";
import UserMessage from "./components/UserMessage";
import Messages from "./components/Messages";
import Input from "./components/Input";
import Header from "./components/Header";
import API from "./ChatbotAPI";  // Import the API object
import "./styles.css";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [conversationHistory, setConversationHistory] = useState("");

  useEffect(() => {
    async function loadWelcomeMessage() {
      const welcomeMessage = "Hello! How can I assist you today?";
      setMessages([
        <BotMessage
          key="0"
          fetchMessage={async () => welcomeMessage}
        />
      ]);
      setConversationHistory(welcomeMessage);
    }
    loadWelcomeMessage();
  }, []);

  const send = async (text) => {
    const newMessages = messages.concat(
      <UserMessage key={messages.length + 1} text={text} />,
      <BotMessage
        key={messages.length + 2}
        fetchMessage={async () => {
          const response = await API.GetChatbotResponse(text, conversationHistory);
          setConversationHistory(conversationHistory + "\n" + text + "\n" + response);
          return response;
        }}
      />
    );
    setMessages(newMessages);
  };

  return (
    <div className="chatbot">
      <Header />
      <Messages messages={messages} />
      <Input onSend={send} />
    </div>
  );
}

export default Chatbot;
