// src/components/AskAIPanel.jsx
import { useState } from "react";

const AskAIPanel = ({ onBack }) => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    
    setIsLoading(true);
    // Simulate API call - replace with your actual API
    setTimeout(() => {
      setAnswer("Here's a thoughtful response to your interview question...");
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="w-full max-w-2xl animate-[fadeIn_0.5s_ease-out]">
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={onBack}
          className="text-white/50 hover:text-white transition-colors"
        >
          ← Back
        </button>
        <h2 className="text-2xl font-semibold text-white">Ask AI Anything</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about interview techniques, questions, or anything..."
          className="w-full p-4 bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl text-white placeholder:text-white/30 focus:outline-none focus:border-blue-500/50 transition-all min-h-[120px] resize-none"
        />
        
        <button
          type="submit"
          disabled={isLoading || !question.trim()}
          className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-2xl hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-900/40"
        >
          {isLoading ? 'Thinking...' : 'Ask AI →'}
        </button>
      </form>

      {answer && (
        <div className="mt-6 p-6 bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl animate-[fadeIn_0.5s_ease-out]">
          <div className="flex items-start gap-3">
            <span className="text-2xl">🤖</span>
            <div>
              <p className="text-white/80">{answer}</p>
              <p className="text-white/30 text-sm mt-2">AI Response</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AskAIPanel;