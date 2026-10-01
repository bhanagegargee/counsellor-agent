import { useState } from "react";

function Sidebar({
  history,
  activeChat,
  onNewChat,
  onSelectChat,
}) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>

      {/* Top Section */}
      <div className="sidebar-top">

        {/* Header */}
        <div className="sidebar-header">

          {!collapsed && (
            <div className="logo">
              <div className="logo-icon">✦</div>
              <span>ChatGPT</span>
            </div>
          )}

          <button
            className="collapse-btn"
            onClick={() => setCollapsed(!collapsed)}
            title="Toggle sidebar"
          >
            ☰
          </button>

        </div>

        {/* New Chat */}
        <button
          className="new-chat-btn"
          onClick={onNewChat}
        >
          <span className="new-chat-icon">＋</span>

          {!collapsed && (
            <span>New chat</span>
          )}
        </button>

        {/* History */}
        {!collapsed && (
          <div className="history-section">

            <div className="history-title">
              Recent
            </div>

            <div className="history-list">

              {history.map((chat) => (
                <button
                  key={chat.id}
                  className={`history-item ${
                    activeChat === chat.id ? "active" : ""
                  }`}
                  onClick={() => onSelectChat(chat.id)}
                >
                  <span className="history-icon">
                    💬
                  </span>

                  <span className="history-text">
                    {chat.title}
                  </span>
                </button>
              ))}

            </div>

          </div>
        )}

      </div>

      {/* Bottom Profile */}
      <div className="sidebar-bottom">

        <button className="profile-btn">

          <div className="profile-avatar">
            G
          </div>

          {!collapsed && (
            <div className="profile-info">
              <span className="profile-name">
                Gargi
              </span>

              <span className="profile-plan">
                Free
              </span>
            </div>
          )}

          {!collapsed && (
            <span className="profile-menu">
              ⋯
            </span>
          )}

        </button>

      </div>

    </aside>
  );
}

export default Sidebar;