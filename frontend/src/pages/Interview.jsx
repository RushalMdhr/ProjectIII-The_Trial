import React, { useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { ArrowLeft, Send, Sparkles } from "lucide-react";
import { askQuestion } from "../services/api";

export default function Interview() {
  const { state } = useLocation();
  const navigate = useNavigate();

  const level = state?.level;

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // If user opens /interview directly
  if (!level) {
    return <Navigate to="/interview-setup" replace />;
  }

  const handleAskQuestion = async (e) => {
    e.preventDefault();

    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setAnswer([]);

    try {
      const res = await askQuestion(question);

      console.log("API response:", res);

      setAnswer(res.answer || []);
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="interview-page">

      <style>{`
        .interview-page {
          min-height: 100vh;
          width: 100%;
          box-sizing: border-box;
          padding: 28px 24px;
          background:
            radial-gradient(
              circle at 20% 20%,
              rgba(139, 124, 246, 0.25),
              transparent 35%
            ),
            radial-gradient(
              circle at 80% 70%,
              rgba(69, 224, 208, 0.15),
              transparent 35%
            ),
            #2B2F63;
          color: #FBFAFF;
          font-family: Inter, Arial, sans-serif;
        }

        .interview-wrapper {
          width: 100%;
          max-width: 900px;
          margin: 0 auto;
        }

        /* TOP */

        .interview-top {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 35px;
        }

        .interview-logo {
          font-size: 20px;
          font-weight: 800;
          letter-spacing: -0.02em;
        }

        .interview-logo span {
          color: #45E0D0;
        }

        .interview-back {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          background: transparent;
          border: none;
          color: #C2C4EC;
          cursor: pointer;
          font-size: 13px;
          padding: 6px 0;
        }

        .interview-back:hover {
          color: #FFFFFF;
        }

        /* HEADER */

        .interview-header {
          text-align: center;
          margin-bottom: 35px;
        }

        .interview-label {
          display: inline-block;
          color: #FFB35B;
          font-size: 11px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          margin-bottom: 10px;
        }

        .interview-header h1 {
          margin: 0 0 10px;
          font-size: 36px;
          font-weight: 700;
          letter-spacing: -0.02em;
        }

        .interview-header p {
          margin: 0;
          color: #C2C4EC;
          font-size: 14px;
          line-height: 1.6;
        }

        /* INFO */

        .interview-info {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 10px;
          flex-wrap: wrap;
          margin-top: 20px;
        }

        .info-pill {
          padding: 8px 14px;
          border-radius: 999px;
          background: rgba(255,255,255,0.07);
          border: 1px solid rgba(255,255,255,0.12);
          color: #C2C4EC;
          font-size: 12px;
        }

        .info-pill strong {
          color: #45E0D0;
          font-weight: 600;
        }

        /* QUESTION BOX */

        .question-area {
          padding: 25px;
          border-radius: 20px;
          background: rgba(255,255,255,0.06);
          border: 1px solid rgba(255,255,255,0.12);
        }

        .question-title {
          display: flex;
          align-items: center;
          gap: 9px;
          margin-bottom: 16px;
          color: #FBFAFF;
          font-size: 16px;
          font-weight: 600;
        }

        .question-title svg {
          color: #45E0D0;
        }

        .question-form {
          display: flex;
          gap: 10px;
        }

        .question-input {
          flex: 1;
          min-width: 0;
          box-sizing: border-box;
          padding: 14px 17px;
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.14);
          background: rgba(255,255,255,0.07);
          color: white;
          font-size: 14px;
          outline: none;
        }

        .question-input::placeholder {
          color: rgba(194,196,236,0.5);
        }

        .question-input:focus {
          border-color: rgba(69,224,208,0.6);
          background: rgba(255,255,255,0.09);
        }

        .ask-button {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 14px 22px;
          border: none;
          border-radius: 12px;
          background: #45E0D0;
          color: #0B2B2B;
          font-weight: 700;
          cursor: pointer;
          transition: 0.2s ease;
        }

        .ask-button:hover:not(:disabled) {
          transform: translateY(-1px);
          background: #5BE9DA;
        }

        .ask-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        /* EMPTY */

        .empty-state {
          text-align: center;
          padding: 28px 10px 4px;
          color: #9295BE;
          font-size: 13px;
        }

        /* ERROR */

        .error-box {
          margin-top: 18px;
          padding: 14px;
          border-radius: 12px;
          background: rgba(244,97,91,0.1);
          border: 1px solid rgba(244,97,91,0.25);
          color: #F88B85;
          font-size: 13px;
        }

        /* ANSWER */

        .answer-area {
          margin-top: 25px;
        }

        .answer-title {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 15px;
          color: #FBFAFF;
          font-size: 16px;
          font-weight: 600;
        }

        .answer-title svg {
          color: #45E0D0;
        }

        .answer-item {
          padding: 16px 18px;
          margin-bottom: 10px;
          border-radius: 13px;
          background: rgba(255,255,255,0.06);
          border: 1px solid rgba(255,255,255,0.1);
          color: #E8E8F5;
          font-size: 14px;
          line-height: 1.6;
        }

        /* MOBILE */

        @media (max-width: 600px) {
          .interview-page {
            padding: 20px 15px;
          }

          .interview-top {
            margin-bottom: 28px;
          }

          .interview-header h1 {
            font-size: 29px;
          }

          .question-area {
            padding: 18px;
          }

          .question-form {
            flex-direction: column;
          }

          .ask-button {
            width: 100%;
          }
        }
      `}</style>

      <div className="interview-wrapper">

        {/* TOP */}
        <div className="interview-top">

          <div className="interview-logo">
            AI <span>HELPER</span>
          </div>

          <button
            className="interview-back"
            onClick={() => navigate("/interview-setup")}
          >
            <ArrowLeft size={14} />
            Back
          </button>

        </div>


        {/* HEADER */}
        <div className="interview-header">

          <span className="interview-label">
            Mock Interview
          </span>

          <h1>
            {level.label} Interview
          </h1>

          <p>
            {level.desc}
          </p>

          <div className="interview-info">

            <div className="info-pill">
              Level: <strong>{level.label}</strong>
            </div>

            <div className="info-pill">
              Time: <strong>{level.time}</strong>
            </div>

          </div>

        </div>


        {/* ASK QUESTION */}
        <div className="question-area">

          <div className="question-title">
            <Sparkles size={17} />
            Ask InterviewAI
          </div>

          <form
            className="question-form"
            onSubmit={handleAskQuestion}
          >

            <input
              className="question-input"
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask an interview question..."
            />

            <button
              className="ask-button"
              type="submit"
              disabled={loading || !question.trim()}
            >

              <Send
                size={15}
                style={{
                  marginRight: 6,
                }}
              />

              {loading ? "Thinking..." : "Ask"}

            </button>

          </form>


          {!answer.length && !loading && (
            <div className="empty-state">
              Ask your first question to start practicing.
            </div>
          )}

        </div>


        {/* ERROR */}
        {error && (
          <div className="error-box">
            {error}
          </div>
        )}


        {/* ANSWER */}
        {answer.length > 0 && (

          <div className="answer-area">

            <div className="answer-title">
              <Sparkles size={17} />
              InterviewAI says
            </div>

            {answer.map((item, index) => (

              <div
                key={index}
                className="answer-item"
              >
                {item}
              </div>

            ))}

          </div>

        )}

      </div>

    </div>
  );
}