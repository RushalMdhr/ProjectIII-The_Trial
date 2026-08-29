// src/components/AIOrb.jsx
import { useState } from "react";
import { Bot, MessageCircle, Mic, X } from "lucide-react";

export default function AIOrb({ onAsk, onInterview }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="relative flex flex-col items-center justify-center">
      
      {/* Rotating rings - decorative */}
      <div className="absolute w-[340px] h-[340px] rounded-full border border-blue-500/20 animate-[spin_18s_linear_infinite]" />
      <div className="absolute w-[280px] h-[280px] rounded-full border border-purple-400/20 animate-[spin_12s_linear_infinite_reverse]" />

      {/* Main Orb - Clickable area with dark translucent background */}
      <div
        onClick={() => setExpanded((v) => !v)}
        className="relative z-10 w-52 h-52 rounded-full flex flex-col items-center justify-center
                   bg-slate-800/50 backdrop-blur-3xl border border-white/20
                   shadow-[0_0_80px_-10px_rgba(59,130,246,0.3)]
                   hover:scale-105 hover:shadow-[0_0_120px_-10px_rgba(59,130,246,0.5)]
                   transition-all duration-300 cursor-pointer
                   group overflow-hidden"
      >
        {/* Inner glow */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-br from-blue-500/15 via-purple-500/15 to-cyan-500/15"></div>
        
        {/* Pulsing inner glow */}
        <div className="absolute inset-2 rounded-full bg-blue-500/5 animate-pulse"></div>
        
        {/* Content inside the circle */}
        <div className="relative z-10 flex flex-col items-center w-full h-full">
          
          {!expanded ? (
            // Default state - Show AI Helper
            <div className="flex flex-col items-center justify-center h-full">
              <Bot className="w-12 h-12 text-blue-400 mb-1 group-hover:text-blue-300 transition-colors" />
              <span className="text-sm font-semibold tracking-wide text-white/90">
                AI Interview Helper
              </span>
              <span className="text-[10px] text-white/30 mt-1">
                Tap to begin
              </span>
            </div>
          ) : (
            // Expanded state - Show options inside the circle
            <div className="flex flex-col items-center justify-center h-full w-full px-4 animate-[fadeIn_0.3s_ease]">
              <span className="text-xs text-white/40 mb-3">Choose option</span>
              
              {/* Ask a question */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setExpanded(false);
                  onAsk();
                }}
                className="w-full flex items-center justify-center gap-2 px-3 py-1.5 rounded-full 
                           bg-white/10 hover:bg-white/20 border border-white/10 hover:border-cyan-400/50
                           transition-all duration-200 text-white/90 text-sm"
              >
                <MessageCircle className="w-4 h-4 text-cyan-300" /> 
                Ask a question
              </button>
              
              {/* Take interview */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setExpanded(false);
                  onInterview();
                }}
                className="w-full flex items-center justify-center gap-2 px-3 py-1.5 rounded-full 
                           bg-white/10 hover:bg-white/20 border border-white/10 hover:border-violet-400/50
                           transition-all duration-200 text-white/90 text-sm mt-1.5"
              >
                <Mic className="w-4 h-4 text-violet-300" /> 
                Take interview
              </button>
              
              {/* Close/hint text */}
              <span className="text-[8px] text-white/20 mt-2">tap circle to close</span>
            </div>
          )}
        </div>
      </div>

      {/* Start Interview Button - Outside the circle */}
      <button
        onClick={onInterview}
        className="mt-8 px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-full hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-lg shadow-blue-900/40 hover:scale-105"
      >
        Start Interview
      </button>

      {/* Add animation keyframes */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes fadeIn {
          from { 
            opacity: 0; 
            transform: scale(0.95); 
          }
          to { 
            opacity: 1; 
            transform: scale(1); 
          }
        }
      `}</style>
    </div>
  );
}