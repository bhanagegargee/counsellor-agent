import { useEffect, useRef } from "react";
import Message from "./Message";

function ChatWindow({ messages }) {

  const bottomRef = useRef(null);

  // Automatically scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  return (
    <div className="chat-window">
     

      <div className="messages-container">
           <h2 >Admission Councelor Agent !</h2>

        {messages.map((message) => (
          <Message
            key={message.id}
            role={message.role}
            content={message.content}
          />
        ))}

        <div ref={bottomRef} />

      </div>

    </div>
  );
}

export default ChatWindow;