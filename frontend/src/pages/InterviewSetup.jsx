import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Briefcase,
  Layers,
  Zap,
  Flame,
  Wind,
  ChevronRight,
} from "lucide-react";

const LEVELS = ["Intern", "Junior", "Mid", "Senior"];

const TYPES = [
  {
    id: "behavioral",
    label: "Behavioral",
    desc: "Situational & teamwork questions",
  },
  {
    id: "technical",
    label: "Technical",
    desc: "Role-specific technical rounds",
  },
  {
    id: "mixed",
    label: "Mixed",
    desc: "A blend of both",
  },
];

const DIFFICULTIES = [
  {
    id: "easy",
    label: "Easy",
    questions: 5,
    icon: Wind,
    color: "#45E0D0",
    soft: "rgba(69,224,208,0.14)",
    line: "rgba(69,224,208,0.35)",
    desc: "Warm-up round. Common questions, relaxed pace.",
  },
  {
    id: "medium",
    label: "Medium",
    questions: 8,
    icon: Zap,
    color: "#FFB35B",
    soft: "rgba(255,179,91,0.14)",
    line: "rgba(255,179,91,0.35)",
    desc: "Standard round. Real follow-ups, timed answers.",
  },
  {
    id: "hard",
    label: "Hard",
    questions: 10,
    icon: Flame,
    color: "#F4615B",
    soft: "rgba(244,97,91,0.14)",
    line: "rgba(244,97,91,0.35)",
    desc: "Advanced round. Rapid-fire, curveball follow-ups.",
  },
];

function FieldLabel({ icon: Icon, children }) {
  return (
    <div className="field-label">
      <Icon size={14} />
      <span>{children}</span>
    </div>
  );
}

function Pill({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`level-pill ${active ? "active" : ""}`}
    >
      {children}
    </button>
  );
}

function DifficultyCircle({
  difficulty,
  hovered,
  onHover,
  onLeave,
  onClick,
}) {
  const Icon = difficulty.icon;
  const isHovered = hovered === difficulty.id;

  return (
    <button
      type="button"
      onClick={onClick}
      onMouseEnter={onHover}
      onMouseLeave={onLeave}
      className="difficulty-button"
      style={{
        transform: isHovered
          ? "translateY(-6px) scale(1.03)"
          : "translateY(0) scale(1)",
      }}
    >
      <div
        className="difficulty-outer"
        style={{
          background: `radial-gradient(circle at 35% 30%, ${difficulty.color}55, ${difficulty.color}1a 60%, transparent 75%)`,
          borderColor: difficulty.line,
          boxShadow: isHovered
            ? `0 0 44px ${difficulty.color}55`
            : `0 0 22px ${difficulty.color}22`,
        }}
      >
        <div
          className="difficulty-inner"
          style={{
            background: `linear-gradient(150deg, ${difficulty.color}dd, ${difficulty.color}88)`,
          }}
        >
          <Icon size={22} color="#0E1024" strokeWidth={2.2} />

          <span className="difficulty-name">
            {difficulty.label}
          </span>

          <span className="difficulty-count">
            {difficulty.questions} QUESTIONS
          </span>
        </div>
      </div>

      <p className="difficulty-description">
        {difficulty.desc}
      </p>
    </button>
  );
}

export default function InterviewSetup() {
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [role, setRole] = useState("");
  const [level, setLevel] = useState("Mid");
  const [type, setType] = useState("mixed");
  const [hovered, setHovered] = useState(null);

  const canContinue = role.trim().length > 0;

  const handleDifficulty = (difficulty) => {
    navigate("/interview", {
      state: {
        role,
        level,
        type,
        difficulty: difficulty.label,
        questionCount: difficulty.questions,
      },
    });
  };

  return (
    <div className="interview-page">
      <style>{`
        * {
          box-sizing: border-box;
        }

        .interview-page {
          min-height: 100vh;
          width: 100%;
          background:
            radial-gradient(
              circle at 15% 20%,
              rgba(139, 124, 246, 0.25),
              transparent 35%
            ),
            radial-gradient(
              circle at 85% 70%,
              rgba(69, 224, 208, 0.16),
              transparent 35%
            ),
            #2B2F63;
          color: #FBFAFF;
          font-family: Inter, Arial, sans-serif;
          overflow-x: hidden;
        }

        .interview-content {
          width: 100%;
          max-width: 900px;
          margin: 0 auto;
          padding: 34px 24px 50px;
        }

        .interview-top {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 28px;
        }

        .interview-logo {
          font-size: 20px;
          font-weight: 800;
          letter-spacing: -0.03em;
        }

        .interview-logo span {
          color: #45E0D0;
        }

        .back-button {
          display: inline-flex;
          align-items: center;
          gap: 7px;
          border: none;
          background: transparent;
          color: #C2C4EC;
          cursor: pointer;
          font-size: 13px;
          padding: 5px 0;
        }

        .back-button:hover {
          color: #FBFAFF;
        }

        .setup-container {
          max-width: 640px;
          margin: 0 auto;
        }

        .setup-header {
          margin-bottom: 30px;
        }

        .setup-label {
          display: inline-block;
          color: #FFB35B;
          font-size: 11px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          margin-bottom: 10px;
        }

        .setup-header h1 {
          margin: 0 0 8px;
          font-size: 32px;
          font-weight: 700;
          letter-spacing: -0.02em;
        }

        .setup-header p {
          margin: 0;
          color: #C2C4EC;
          line-height: 1.55;
          font-size: 14px;
        }

        .setup-section {
          margin-bottom: 25px;
        }

        .field-label {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 10px;
          color: #C2C4EC;
        }

        .field-label svg {
          color: #FFB35B;
        }

        .field-label span {
          font-size: 11px;
          letter-spacing: 0.05em;
          text-transform: uppercase;
        }

        .role-input {
          width: 100%;
          background: rgba(255,255,255,0.06);
          border: 1px solid rgba(255,255,255,0.14);
          border-radius: 12px;
          padding: 13px 15px;
          font-size: 14px;
          color: #FBFAFF;
          outline: none;
        }

        .role-input::placeholder {
          color: rgba(194,196,236,0.55);
        }

        .role-input:focus {
          border-color: rgba(69,224,208,0.6);
          box-shadow: 0 0 0 3px rgba(69,224,208,0.08);
        }

        .level-pills {
          display: flex;
          gap: 9px;
          flex-wrap: wrap;
        }

        .level-pill {
          padding: 9px 17px;
          border-radius: 999px;
          border: 1px solid rgba(255,255,255,0.14);
          background: rgba(255,255,255,0.06);
          color: #C2C4EC;
          font-size: 13px;
          cursor: pointer;
          transition: all 0.18s ease;
        }

        .level-pill:hover {
          border-color: rgba(69,224,208,0.4);
        }

        .level-pill.active {
          border-color: rgba(69,224,208,0.6);
          background: rgba(69,224,208,0.14);
          color: #45E0D0;
          font-weight: 600;
        }

        .type-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 10px;
        }

        .type-card {
          text-align: left;
          padding: 14px;
          border-radius: 13px;
          border: 1px solid rgba(255,255,255,0.14);
          background: rgba(255,255,255,0.06);
          cursor: pointer;
          transition: all 0.18s ease;
        }

        .type-card:hover {
          transform: translateY(-2px);
          border-color: rgba(255,179,91,0.45);
        }

        .type-card.active {
          border-color: rgba(255,179,91,0.55);
          background: rgba(255,179,91,0.10);
        }

        .type-title {
          font-size: 13.5px;
          font-weight: 600;
          color: #FBFAFF;
          margin-bottom: 4px;
        }

        .type-card.active .type-title {
          color: #FFB35B;
        }

        .type-description {
          font-size: 11.5px;
          line-height: 1.4;
          color: #C2C4EC;
        }

        .continue-button {
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          padding: 14px 20px;
          border: none;
          border-radius: 13px;
          background: linear-gradient(135deg, #FFB35B, #45E0D0);
          color: #191C36;
          font-size: 14px;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.18s ease;
        }

        .continue-button:hover:not(:disabled) {
          transform: translateY(-2px);
        }

        .continue-button:disabled {
          background: rgba(255,255,255,0.08);
          color: #77799D;
          cursor: not-allowed;
        }

        /* STEP 2 */

        .difficulty-container {
          max-width: 900px;
          margin: 0 auto;
          text-align: center;
        }

        .difficulty-header {
          margin-bottom: 40px;
        }

        .difficulty-header h1 {
          margin: 0 0 10px;
          font-size: 34px;
          font-weight: 700;
        }

        .difficulty-header p {
          max-width: 480px;
          margin: 0 auto;
          color: #C2C4EC;
          font-size: 14px;
          line-height: 1.6;
        }

        .difficulty-back {
          display: flex;
          align-items: center;
          gap: 6px;
          border: none;
          background: transparent;
          color: #C2C4EC;
          cursor: pointer;
          font-size: 13px;
          margin-bottom: 30px;
        }

        .difficulty-options {
          display: flex;
          justify-content: center;
          gap: 48px;
          flex-wrap: wrap;
        }

        .difficulty-button {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 0;
          border: none;
          background: transparent;
          cursor: pointer;
          transition: transform 0.25s ease;
        }

        .difficulty-outer {
          width: 168px;
          height: 168px;
          border-radius: 50%;
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 1.5px solid;
          transition: box-shadow 0.25s ease;
        }

        .difficulty-inner {
          width: 128px;
          height: 128px;
          border-radius: 50%;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 4px;
        }

        .difficulty-name {
          font-size: 17px;
          font-weight: 800;
          color: #0E1024;
        }

        .difficulty-count {
          font-size: 9px;
          letter-spacing: 0.04em;
          color: #0E1024;
          opacity: 0.75;
        }

        .difficulty-description {
          max-width: 190px;
          margin: 15px 0 0;
          color: #C2C4EC;
          font-size: 12px;
          line-height: 1.5;
        }

        @media (max-width: 700px) {
          .interview-content {
            padding: 25px 18px 40px;
          }

          .setup-header h1 {
            font-size: 28px;
          }

          .type-grid {
            grid-template-columns: 1fr;
          }

          .difficulty-header h1 {
            font-size: 29px;
          }

          .difficulty-options {
            gap: 35px;
          }
        }
      `}</style>

      <div className="interview-content">

        {/* TOP */}
        <div className="interview-top">
          <div className="interview-logo">
            AI <span>HELPER</span>
          </div>

          <button
            className="back-button"
            onClick={() => navigate("/")}
          >
            <ArrowLeft size={14} />
            Back
          </button>
        </div>

        {/* STEP 1 */}
        {step === 1 && (
          <div className="setup-container">

            <div className="setup-header">
              <span className="setup-label">
                Mock Interview
              </span>

              <h1>
                Set up your session
              </h1>

              <p>
                Tell us what you're interviewing for and we'll
                tailor the questions to match.
              </p>
            </div>

            {/* ROLE */}
            <div className="setup-section">
              <FieldLabel icon={Briefcase}>
                Role you're interviewing for
              </FieldLabel>

              <input
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="e.g. Frontend Developer, Data Analyst"
                className="role-input"
              />
            </div>

            {/* LEVEL */}
            <div className="setup-section">
              <FieldLabel icon={Layers}>
                Experience level
              </FieldLabel>

              <div className="level-pills">
                {LEVELS.map((item) => (
                  <Pill
                    key={item}
                    active={level === item}
                    onClick={() => setLevel(item)}
                  >
                    {item}
                  </Pill>
                ))}
              </div>
            </div>

            {/* TYPE */}
            <div className="setup-section">
              <FieldLabel icon={Zap}>
                Interview type
              </FieldLabel>

              <div className="type-grid">
                {TYPES.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    className={`type-card ${
                      type === item.id ? "active" : ""
                    }`}
                    onClick={() => setType(item.id)}
                  >
                    <div className="type-title">
                      {item.label}
                    </div>

                    <div className="type-description">
                      {item.desc}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* CONTINUE */}
            <button
              className="continue-button"
              disabled={!canContinue}
              onClick={() => canContinue && setStep(2)}
            >
              Continue
              <ChevronRight size={17} />
            </button>

          </div>
        )}

        {/* STEP 2 */}
        {step === 2 && (
          <div className="difficulty-container">

            <button
              className="difficulty-back"
              onClick={() => setStep(1)}
            >
              <ArrowLeft size={14} />
              Back
            </button>

            <div className="difficulty-header">

              <h1>
                Choose your difficulty
              </h1>

              <p>
                Same interview, different pressure. Pick the
                level that matches how you want to practice.
              </p>

            </div>

            <div className="difficulty-options">

              {DIFFICULTIES.map((difficulty) => (
                <DifficultyCircle
                  key={difficulty.id}
                  difficulty={difficulty}
                  hovered={hovered}
                  onHover={() => setHovered(difficulty.id)}
                  onLeave={() => setHovered(null)}
                  onClick={() => handleDifficulty(difficulty)}
                />
              ))}

            </div>

          </div>
        )}

      </div>
    </div>
  );
}