import { useState } from "react";

function ChatInput({ onSend }) {

  const [message, setMessage] = useState("");

  const handleSubmit = () => {

    if (!message.trim()) return;

    onSend(message);

    setMessage("");
  };

  const handleKeyDown = (e) => {

    // Enter = Send
    if (e.key === "Enter" && !e.shiftKey) {

      e.preventDefault();

      handleSubmit();
    }
  };

  return (
    <div className="input-area">

      <div className="input-wrapper">

        {/* Attachment button */}
        {/* <button
          className="input-icon-btn"
          title="Attach file"
        >
          ＋
        </button> */}

        {/* Text input */}
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message Assistant..."
          rows="1"
        />

        {/* Send */}
        <button
          className={`send-btn ${
            message.trim() ? "enabled" : ""
          }`}
          onClick={handleSubmit}
          disabled={!message.trim()}
        >
          ↑
        </button>

      </div>

      <div className="input-disclaimer">
        AI can make mistakes. Check important information.
      </div>

    </div>
  );
}

export default ChatInput;