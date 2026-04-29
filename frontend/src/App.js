import React, { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const userId = "user123";

  const sendMessage = async (msg = input) => {
    if (!msg) return;

    const userMsg = { sender: "user", text: msg };
    setMessages((prev) => [...prev, userMsg]);

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id: userId, message: msg }),
    });

    const data = await res.json();

    const botMsg = { sender: "bot", text: data.response };
    setMessages((prev) => [...prev, botMsg]);

    setInput("");
  };

  return (
    <div className="app">
      <div className="chat-container">
        <h1>🥗 NutriBot-AI</h1>

        {/* Quick Buttons */}
        <div className="quick-buttons">
          <button onClick={() => sendMessage("I want to lose weight")}>Weight Loss</button>
          <button onClick={() => sendMessage("I want to gain muscle")}>Muscle Gain</button>
          <button onClick={() => sendMessage("Healthy recipes")}>Recipes</button>
          <button onClick={() => sendMessage("Suggest healthy food to order")}>Order Food</button>
        </div>

        <div className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={msg.sender}>
  {msg.text.split("\n").map((line, i) => (
    <div key={i}>{line}</div>
         ))}
        </div>
          ))}
        </div>

        <div className="input-box">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything about food, diet, or meals..."
          />
          <button onClick={() => sendMessage()}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;