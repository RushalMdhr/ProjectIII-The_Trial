// src/components/AIOrb.jsx
//
// Stays "dumb" on purpose: it doesn't know about routes, pages, or the API.
// It only knows two things can happen — onAsk and onInterview — and calls
// whichever prop it's given. That's what makes it reusable: you could drop
// this same file into a dashboard page later with different callbacks.

import { useState } from "react";
import { Sparkles, MessageCircle, Mic } from "lucide-react";

export default function AIOrb({ onAsk, onInterview }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="relative flex flex-col items-center justify-center">
      <div className="absolute w-[340px] h-[340px] rounded-full border border-violet-500/20 animate-[spin_18s_linear_infinite]" />
      <div className="absolute w-[280px] h-[280px] rounded-full border border-cyan-400/20 animate-[spin_12s_linear_infinite_reverse]" />

      <button
        onClick={() => setExpanded((v) => !v)}
        className="relative z-10 w-52 h-52 rounded-full flex flex-col items-center justify-center gap-2
                   bg-white/5 backdrop-blur-xl border border-white/15 shadow-[0_0_60px_-10px_rgba(139,92,246,0.6)]
                   hover:scale-105 transition-transform duration-300"
      >
        <Sparkles className="w-8 h-8 text-violet-300" />
        <span className="text-sm tracking-wide text-white/80">
          {expanded ? "Choose below" : "Tap to begin"}
        </span>
      </button>

      {expanded && (
        <div className="mt-8 flex flex-col sm:flex-row gap-4 animate-[fadeIn_0.4s_ease]">
          <button
            onClick={onAsk}
            className="flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/15
                       backdrop-blur-md text-white/90 hover:border-cyan-400/60 hover:bg-white/10 transition-colors"
          >
            <MessageCircle className="w-4 h-4 text-cyan-300" /> Ask a question
          </button>
          <button
            onClick={onInterview}
            className="flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/15
                       backdrop-blur-md text-white/90 hover:border-violet-400/60 hover:bg-white/10 transition-colors"
          >
            <Mic className="w-4 h-4 text-violet-300" /> Take interview
          </button>
        </div>
      )}
    </div>
  );
}
