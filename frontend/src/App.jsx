import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

import "./App.css";

function App() {
  const [messages, setMessages] = useState([{
      id: 1,
      role: "assistant",
      content: "how can i help you ?",
    }
  ]);

  const [chatHistory, setChatHistory] = useState([
    {
      id: 1,
      title: "",
    },
  ]);

  const [activeChat, setActiveChat] = useState(1);

  // Send message
const handleSendMessage = async (message) => {
  if (!message.trim()) return;

  const userMessage = { id: Date.now(), role: "user", content: message };
  const botId = Date.now() + 1;

  // Show user message + "Thinking..." placeholder immediately
  setMessages((prev) => [
    ...prev,
    userMessage,
    { id: botId, role: "assistant", content: "Thinking..." },
  ]);

  const updateBot = (content) =>
    setMessages((prev) =>
      prev.map((m) => (m.id === botId ? { ...m, content } : m))
    );

  try {
    
      const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/admission/chat/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: message
        })
      }
    );

    if (!response.ok || !response.body) {
      throw new Error(`Server error: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let text = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      text += decoder.decode(value, { stream: true });
      updateBot(text);   // replaces "Thinking..." with the first chunk
    }
  } catch (error) {
    console.error("CHAT API ERROR:", error);
    updateBot(`Error: ${error.message}`);
  }
};


  // New chat
  const handleNewChat = () => {
    setMessages([
      {
        id: Date.now(),
        role: "assistant",
        content: "Hello! How can I help you today?",
      },
    ]);

    setActiveChat(null);
  };

  // Select history chat
  const handleSelectChat = (chatId) => {
    setActiveChat(chatId);

    // For now, demo messages
    setMessages([
      {
        id: 1,
        role: "user",
        content: "Can you help me with this project?",
      },
      {
        id: 2,
        role: "assistant",
        content:
          "Of course! Tell me more about your project and what you want to build.",
      },
    ]);
  };

  return (
    <div className="app">

      {/* Sidebar */}
      <Sidebar
        history={chatHistory}
        activeChat={activeChat}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
      />

      {/* Main Chat Area */}
      <main className="main-content">

        {/* Chat Window */}
        <ChatWindow messages={messages} />

        {/* Input */}
        <ChatInput onSend={handleSendMessage} />

      </main>
    </div>
  );
}

export default App;