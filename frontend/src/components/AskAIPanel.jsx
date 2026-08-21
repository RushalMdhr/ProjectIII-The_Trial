// src/components/AskAIPanel.jsx
//
// This component OWNS its messages/input state because nothing else in the
// app needs to read it. It calls askQuestion() from services/api.js instead
// of faking the delay itself — so when your backend goes live, you flip
// USE_MOCK to false in api.js and this file never changes.

import { useState } from "react";
import { ChevronLeft, Send } from "lucide-react";
import { askQuestion } from "../services/api";

export default function AskAIPanel({ onBack }) {
  const [messages, setMessages] = useState([
    { role: "ai", text: "Hi! Ask me anything about interview prep." },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);

  async function handleSend() {
    if (!input.trim()) return;

    const question = input;
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setInput("");
    setSending(true);

    try {
      const res = await askQuestion(question);
      setMessages((prev) => [...prev, { role: "ai", text: res.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "Something went wrong reaching the AI. Try again." },
      ]);
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="w-full max-w-md flex flex-col h-[420px] rounded-2xl bg-white/5 border border-white/15 backdrop-blur-xl overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10">
        <button onClick={onBack} className="text-white/60 hover:text-white">
          <ChevronLeft className="w-5 h-5" />
        </button>
        <span className="text-white/80 text-sm">Ask InterviewAI</span>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`max-w-[85%] px-3 py-2 rounded-xl text-sm ${
              m.role === "user" ? "ml-auto bg-violet-500/30 text-white" : "bg-white/10 text-white/80"
            }`}
          >
            {m.text}
          </div>
        ))}
        {sending && <div className="text-xs text-white/40">InterviewAI is typing…</div>}
      </div>

      <div className="flex items-center gap-2 px-3 py-3 border-t border-white/10">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your question…"
          className="flex-1 bg-white/5 border border-white/10 rounded-full px-4 py-2 text-sm text-white
                     placeholder:text-white/30 outline-none focus:border-cyan-400/50"
        />
        <button
          onClick={handleSend}
          className="w-9 h-9 flex items-center justify-center rounded-full bg-cyan-500/20 border border-cyan-400/40 hover:bg-cyan-500/30"
        >
          <Send className="w-4 h-4 text-cyan-200" />
        </button>
      </div>
    </div>
  );
}
