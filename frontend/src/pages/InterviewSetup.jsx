import { useNavigate } from "react-router-dom";
import { ChevronLeft, Target, Zap, Trophy } from "lucide-react";

const LEVELS = [
  {
    id: 1,
    name: "Level 1",
    label: "Foundations",
    desc: "Warm-up questions on basics — good for building confidence before a real interview.",
    icon: Target,
    time: "10–15 min",
  },
  {
    id: 2,
    name: "Level 2",
    label: "Applied",
    desc: "Scenario and project-based questions, closer to what you'll actually get asked.",
    icon: Zap,
    time: "20–25 min",
  },
  {
    id: 3,
    name: "Level 3",
    label: "Advanced",
    desc: "System design, edge cases, and follow-up pressure questions. The real test.",
    icon: Trophy,
    time: "30+ min",
  },
];

function InterviewSetup() {
  const navigate = useNavigate();

  function pickLevel(level) {
    navigate("/interview", {
      state: { level },
    });
  }

  return (
    <div className="min-h-screen w-full relative overflow-hidden bg-slate-950 text-white flex flex-col items-center px-6 py-16">

      {/* ================= BACKGROUND ================= */}

      <div className="pointer-events-none absolute -top-40 -left-40 w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px]" />

      <div className="pointer-events-none absolute -bottom-40 -right-20 w-[450px] h-[450px] bg-purple-600/20 rounded-full blur-[120px]" />

      <div className="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-cyan-500/10 rounded-full blur-[120px]" />

      {/* ================= DOT PATTERN ================= */}

      <div
        className="pointer-events-none absolute inset-0 opacity-[0.12]"
        style={{
          backgroundImage:
            "radial-gradient(rgba(255,255,255,0.4) 1px, transparent 1px)",
          backgroundSize: "26px 26px",
        }}
      />

      {/* ================= CONTENT ================= */}

      <div className="relative z-10 w-full max-w-4xl">

        {/* Back Button */}

        <button
          onClick={() => navigate("/")}
          className="flex items-center gap-1 text-white/50 hover:text-white text-sm mb-8 transition"
        >
          <ChevronLeft className="w-4 h-4" />
          Back
        </button>

        {/* Heading */}

        <div className="mb-10">
          <p className="text-blue-400 text-xs tracking-[0.3em] mb-3">
            INTERVIEWAI
          </p>

          <h1 className="text-3xl sm:text-4xl font-bold mb-3">
            Choose your{" "}
            <span className="text-blue-400">level</span>
          </h1>

          <p className="text-white/50 text-sm sm:text-base">
            Difficulty scales the question depth and follow-ups.
            Choose the level that matches your preparation.
          </p>
        </div>

        {/* ================= LEVEL CARDS ================= */}

        <div className="grid sm:grid-cols-3 gap-5">

          {LEVELS.map((lvl) => {
            const Icon = lvl.icon;

            return (
              <button
                key={lvl.id}
                onClick={() => pickLevel(lvl)}
                className="group text-left p-6 rounded-2xl
                           bg-white/5 backdrop-blur-sm
                           border border-white/10
                           hover:border-blue-400/50
                           hover:bg-white/10
                           hover:-translate-y-1
                           transition-all duration-300
                           shadow-lg"
              >

                {/* Icon */}

                <div className="w-12 h-12 rounded-xl
                                bg-gradient-to-br from-blue-600/20 to-purple-600/20
                                border border-white/10
                                flex items-center justify-center
                                mb-5
                                group-hover:scale-110
                                transition-transform"
                >
                  <Icon className="w-6 h-6 text-blue-400" />
                </div>

                {/* Level */}

                <div className="text-white font-semibold text-lg">
                  {lvl.name}
                </div>

                <div className="text-purple-400 text-sm font-medium mt-1">
                  {lvl.label}
                </div>

                {/* Description */}

                <p className="text-white/50 text-sm mt-3 leading-relaxed">
                  {lvl.desc}
                </p>

                {/* Time */}

                <div className="mt-6 pt-4 border-t border-white/10">
                  <span className="text-xs text-white/40">
                    Estimated time
                  </span>

                  <div className="text-white/70 text-sm mt-1">
                    {lvl.time}
                  </div>
                </div>

              </button>
            );
          })}

        </div>

      </div>
    </div>
  );
}

export default InterviewSetup;