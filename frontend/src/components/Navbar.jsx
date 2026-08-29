import React from "react";
import { useNavigate } from "react-router-dom";

const tokens = {
  gold: "#FFB35B",
  teal: "#45E0D0",
  text: "#FBFAFF",
};

function Logo() {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate("/")}
      aria-label="Go to homepage"
      style={{
        display: "flex",
        alignItems: "center",
        gap: 10,
        background: "none",
        border: "none",
        padding: 0,
        cursor: "pointer",
      }}
    >
      <svg
        width="34"
        height="34"
        viewBox="0 0 40 40"
        fill="none"
      >
        <circle
          cx="20"
          cy="20"
          r="17.5"
          stroke="rgba(255,255,255,0.2)"
          strokeWidth="3"
        />

        <path
          d="M20 2.5 A17.5 17.5 0 0 1 35.4 28.7"
          stroke={tokens.gold}
          strokeWidth="3"
          strokeLinecap="round"
        />

        <circle
          cx="20"
          cy="20"
          r="6"
          fill={tokens.teal}
        />
      </svg>

      <span
        className="cp-display"
        style={{
          fontSize: 18,
          fontWeight: 700,
          color: tokens.text,
        }}
      >
        AI
        <span style={{ color: tokens.teal }}>
          HELPER
        </span>
      </span>
    </button>
  );
}

export default function Navbar() {
  return (
    <nav
      className="cp-navbar"
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "22px 48px",
        width: "100%",
      }}
    >
      {/* LOGO */}
      <Logo />

      {/* PROFILE */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 14,
        }}
      >
        <span
          style={{
            fontSize: 13.5,
            color: "#C2C4EC",
          }}
        >
          Hi, Jane
        </span>

        <div
          style={{
            width: 34,
            height: 34,
            borderRadius: "50%",
            background:
              `linear-gradient(135deg, ${tokens.gold}, ${tokens.teal})`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 13,
            fontWeight: 700,
            color: "#191C36",
          }}
        >
          JD
        </div>
      </div>
    </nav>
  );
}

export { Logo };