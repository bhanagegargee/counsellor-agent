import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import {sendQuery} from "./services/api";
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
      title: "React project help",
    },
  ]);

  const [activeChat, setActiveChat] = useState(1);

  // Send message
const handleSendMessage = async (message) => {
  if (!message.trim()) return;

  const userMessage = {
    id: Date.now(),
    role: "user",
    content: message,
  };

  setMessages((prev) => [
    ...prev,
    userMessage,
  ]);

  try {
    // const response = await sendQuery(
    //     {
    //       query: message,
    //     }
    //   );

    const response = await fetch(
      "http://127.0.0.1:8000/api/admission/chat/",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          query: message,
        }),
      }
    );

    const assistantMessage = {
      id: Date.now() + 1,
      role: "assistant",
      content: response.data.answer,
    };

    setMessages((prev) => [
      ...prev,
      assistantMessage,
    ]);

  }catch (error) {
  console.error("CHAT API ERROR:", error);

  setMessages((prev) => [
    ...prev,
    {
      id: Date.now() + 1,
      role: "assistant",
      content: `Error: ${error.message}`,
    },
  ]);
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