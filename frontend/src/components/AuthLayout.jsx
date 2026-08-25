import { Link } from "react-router-dom";

function AuthLayout({ children, title, subtitle }) {
  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-hidden relative">

      {/* Background circles */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl"></div>

      <div className="absolute top-1/2 -left-20 w-72 h-72 bg-purple-600/20 rounded-full blur-3xl"></div>

      <div className="absolute -bottom-40 right-0 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl"></div>

      {/* Decorative circles */}
      <div className="absolute top-24 left-1/2 w-24 h-24 border border-blue-400/20 rounded-full"></div>

      <div className="absolute bottom-20 left-1/3 w-12 h-12 border border-purple-400/20 rounded-full"></div>

      {/* Main container */}
      <div className="relative min-h-screen flex items-center justify-center px-6 py-10">

        <div className="w-full max-w-6xl grid lg:grid-cols-2 gap-12 items-center">

          {/* LEFT SIDE */}
          <div className="hidden lg:flex flex-col items-center justify-center text-center">

            {/* Logo */}
            <Link to="/" className="text-3xl font-bold mb-10">
              <span className="text-blue-400">Interview</span>
              <span className="text-white">Helper</span>
            </Link>

            {/* Main Circle */}
            <div className="relative">

              {/* Outer circle */}
              <div className="absolute inset-[-35px] rounded-full border border-blue-400/10"></div>

              {/* Middle circle */}
              <div className="absolute inset-[-18px] rounded-full border border-purple-400/20"></div>

              {/* Main circle */}
              <div className="w-72 h-72 rounded-full bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 flex items-center justify-center shadow-2xl shadow-blue-900/50">

                <div className="text-center">

                  <div className="text-6xl mb-4">
                    🤖
                  </div>

                  <h2 className="text-2xl font-bold">
                    Interview Helper
                  </h2>

                  <p className="text-blue-100 mt-2 text-sm">
                    Your AI Interview Partner
                  </p>

                </div>

              </div>

              {/* Small floating circles */}
              <div className="absolute -top-8 right-8 w-5 h-5 bg-blue-400 rounded-full shadow-lg"></div>

              <div className="absolute bottom-4 -left-10 w-4 h-4 bg-purple-400 rounded-full"></div>

              <div className="absolute top-1/2 -right-14 w-3 h-3 bg-cyan-400 rounded-full"></div>

            </div>

            {/* Description */}
            <div className="mt-16 max-w-md">

              <h1 className="text-3xl font-bold mb-4">
                Prepare. Practice. <span className="text-blue-400">Succeed.</span>
              </h1>

              <p className="text-slate-400 leading-relaxed">
                Practice engineering interviews, improve your answers,
                receive intelligent feedback, and build confidence for
                your next interview.
              </p>

            </div>

          </div>

          {/* RIGHT SIDE */}
          <div className="flex justify-center">

            <div className="w-full max-w-md">

              {/* Mobile logo */}
              <div className="lg:hidden text-center mb-8">
                <Link to="/" className="text-3xl font-bold">
                  <span className="text-blue-400">Interview</span>
                  Helper
                </Link>
              </div>

              {/* Auth card */}
              <div className="bg-white text-slate-900 rounded-3xl shadow-2xl p-8 sm:p-10">

                <div className="mb-8">

                  <h2 className="text-3xl font-bold">
                    {title}
                  </h2>

                  <p className="text-slate-500 mt-2">
                    {subtitle}
                  </p>

                </div>

                {children}

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default AuthLayout;