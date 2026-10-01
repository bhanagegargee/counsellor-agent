function Message({ role, content }) {

  const isUser = role === "user";

  return (
    <div
      className={`message-row ${
        isUser ? "user-message" : "assistant-message"
      }`}
    >

      {/* Avatar */}
      <div
        className={`message-avatar ${
          isUser ? "user-avatar" : "assistant-avatar"
        }`}
      >
        {isUser ? "G" : "✦"}
      </div>

      {/* Message */}
      <div className="message-content">

        <div className="message-role">
          {isUser ? "You" : "Assistant"}
        </div>

        <div className="message-text">
          {content}
        </div>

      </div>

    </div>
  );
}

export default Message;