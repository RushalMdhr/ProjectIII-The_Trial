import { Navigate, useLocation } from "react-router-dom";
import { useState } from "react";
import { askQuestion } from "../services/api";

function Interview() {
  const { state } = useLocation();
  const level = state?.level;

  // -----------------------------
  // STATE
  // -----------------------------

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // -----------------------------
  // IF NO LEVEL WAS SELECTED
  // -----------------------------

  if (!level) {
    return <Navigate to="/interview-setup" replace />;
  }

  // -----------------------------
  // HANDLE ASK BUTTON
  // -----------------------------

  const handleAskQuestion = async (e) => {
    e.preventDefault();

    // Don't do anything if input is empty
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setAnswer([]);

    try {
      // Send question to our API
      const res = await askQuestion(question);

      console.log("API response:", res);

      // Get answer from API
      setAnswer(res.answer);

    } catch (err) {
      console.error(err);

      setError("Something went wrong. Please try again.");

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-16 text-white">

      <div className="mx-auto max-w-4xl">

        {/* ----------------------------- */}
        {/* HEADER */}
        {/* ----------------------------- */}

        <p className="text-sm text-blue-400">
          {level.name}
        </p>

        <h1 className="mt-2 text-3xl font-bold">
          {level.label} interview
        </h1>

        <p className="mt-3 text-white/60">
          {level.desc}
        </p>

        <p className="mt-6 text-sm text-white/50">
          Estimated time: {level.time}
        </p>


        {/* ----------------------------- */}
        {/* ASK QUESTION */}
        {/* ----------------------------- */}

        <div className="mt-12">

          <h2 className="text-xl font-semibold mb-4">
            Ask InterviewAI
          </h2>

          <form
            onSubmit={handleAskQuestion}
            className="flex gap-3"
          >

            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask something like: 2026 most asked questions"
              className="flex-1 px-4 py-3 rounded-xl
                         bg-white/10
                         border border-white/10
                         text-white
                         placeholder-white/30
                         focus:outline-none
                         focus:border-blue-500"
            />

            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3 rounded-xl
                         bg-blue-600
                         hover:bg-blue-700
                         font-semibold
                         transition
                         disabled:opacity-50"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>

          </form>

        </div>


        {/* ----------------------------- */}
        {/* ERROR */}
        {/* ----------------------------- */}

        {error && (
          <div className="mt-6 p-4 rounded-xl
                          bg-red-500/10
                          border border-red-500/20
                          text-red-400">
            {error}
          </div>
        )}


        {/* ----------------------------- */}
        {/* ANSWER */}
        {/* ----------------------------- */}

        {answer.length > 0 && (

          <div className="mt-8">

            <h2 className="text-xl font-semibold mb-4">
              InterviewAI says:
            </h2>

            <div className="space-y-3">

              {answer.map((item, index) => (

                <div
                  key={index}
                  className="p-5 rounded-xl
                             bg-white/5
                             border border-white/10"
                >
                  {item}
                </div>

              ))}

            </div>

          </div>

        )}

      </div>

    </div>
  );
}

export default Interview;