import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AIOrb from "../components/AIOrb";
import AskAIPanel from "../components/AskAIPanel";

function Home() {
  const navigate = useNavigate();
  const [showChat, setShowChat] = useState(false);

  return (
    <div className="min-h-screen w-full relative overflow-hidden bg-slate-950 text-white flex flex-col items-center justify-center px-6 py-16">

      {/* ================= BACKGROUND GLOWS ================= */}

      <div className="pointer-events-none absolute -top-40 -left-40 w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px] animate-[float1_10s_ease-in-out_infinite]" />

      <div className="pointer-events-none absolute -bottom-40 -right-20 w-[450px] h-[450px] bg-purple-600/20 rounded-full blur-[120px] animate-[float2_12s_ease-in-out_infinite]" />

      <div className="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-cyan-500/10 rounded-full blur-[120px]" />

      {/* ================= DOT BACKGROUND ================= */}

      <div
        className="pointer-events-none absolute inset-0 opacity-[0.12]"
        style={{
          backgroundImage:
            "radial-gradient(rgba(255,255,255,0.4) 1px, transparent 1px)",
          backgroundSize: "26px 26px",
        }}
      />

      {/* ================= ANIMATIONS ================= */}

      <style>{`
        @keyframes float1 {
          0%, 100% {
            transform: translate(0, 0);
          }
          50% {
            transform: translate(40px, 30px);
          }
        }

        @keyframes float2 {
          0%, 100% {
            transform: translate(0, 0);
          }
          50% {
            transform: translate(-30px, -40px);
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(6px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>

      {/* ================= MAIN CONTENT ================= */}

      <div className="relative z-10 flex flex-col items-center w-full">

        {/* Logo */}

        <p className="text-white/40 text-xs tracking-[0.3em] mb-4">
          INTERVIEWAI
        </p>

        {!showChat ? (
          <>
            {/* Title */}

            <h1 className="text-3xl sm:text-4xl font-bold text-center mb-3">
              <span className="text-blue-400">Interview</span>
              <span className="text-white">AI</span>
            </h1>

            {/* Subtitle */}

            <p className="text-white/60 text-center max-w-lg mb-10">
              Practice interviews with an AI that actually pushes back.
            </p>

            {/* AI Orb */}

            <AIOrb
              onAsk={() => setShowChat(true)}
              onInterview={() => navigate("/interview-setup")}
            />

            {/* Start Interview Button */}

            <button
              onClick={() => navigate("/interview-setup")}
              className="mt-10 px-12 py-5 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg font-semibold rounded-2xl hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-lg shadow-blue-900/40 hover:scale-105"
            >
              Start Interview
            </button>

            {/* Small description */}

            <p className="mt-5 text-sm text-white/40">
              Prepare smarter. Practice better. Interview confidently.
            </p>
          </>
        ) : (
          /* ================= ASK AI PANEL ================= */

          <AskAIPanel
            onBack={() => setShowChat(false)}
          />
        )}

      </div>
    </div>
  );
}

export default Home;