import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Send,
  Sparkles,
  MessageCircleQuestion,
} from "lucide-react";

export default function AskQuestion() {
  const navigate = useNavigate();
  const [input, setInput] = useState("");

  const handleSend = () => {
    const question = input.trim();

    if (!question) return;

    // Backend will be connected here later.
    console.log("Question:", question);

    setInput("");
  };

  return (
    <div className="ask-page">

      {/* =========================
          TOP BAR
      ========================= */}

      <div className="ask-topbar">
        <button
          className="ask-back"
          onClick={() => navigate("/")}
        >
          <ArrowLeft size={16} />
          Back to Home
        </button>
      </div>


      {/* =========================
          MAIN AREA
      ========================= */}

      <main className="ask-main">

        {/* Empty chat / welcome screen */}

        <div className="ask-welcome">

          <div className="ask-icon">
            <MessageCircleQuestion size={27} />
          </div>

          <h1>
            What can I help you with?
          </h1>

          <p>
            Ask anything about your career, resume,
            interviews, job search, or professional growth.
          </p>

        </div>


        {/* =========================
            INPUT AREA
        ========================= */}

        <div className="ask-input-area">

          <div className="ask-input-box">

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSend();
                }
              }}
              placeholder="Ask a career question..."
            />

            <button
              className={`ask-send ${
                input.trim() ? "active" : ""
              }`}
              onClick={handleSend}
              disabled={!input.trim()}
              aria-label="Send question"
            >
              <Send size={17} />
            </button>

          </div>

          <div className="ask-disclaimer">
            <Sparkles size={11} />
            <span>
              AI Helper can make mistakes. Verify important information.
            </span>
          </div>

        </div>

      </main>

    </div>
  );
}

