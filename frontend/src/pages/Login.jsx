import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { login } from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError(null);
    setLoading(true);

    try {
      // Call our API
      const res = await login(
        form.email,
        form.password
      );

      console.log("Login response:", res);

      // -----------------------------
      // LOGIN FAILED
      // -----------------------------

      if (!res.success) {
        setError(res.message);
        return;
      }

      // -----------------------------
      // LOGIN SUCCESSFUL
      // -----------------------------

      console.log("Logged in user:", res.user);

      // Save the user for now.
      // Later Django/JWT will handle authentication.
      localStorage.setItem(
        "currentUser",
        JSON.stringify(res.user)
      );

      // Go to home page
      navigate("/");

    } catch (err) {
      console.error("Login error:", err);

      setError(
        "Couldn't log in. Check your email and password."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Sign in to continue your interview preparation."
    >

      <form onSubmit={handleSubmit} className="space-y-5">

        {/* Error */}
        {error && (
          <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2.5">
            {error}
          </div>
        )}

        {/* Email */}
        <div>

          <label className="block text-sm font-semibold mb-2">
            Email Address
          </label>

          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            placeholder="you@example.com"
            required
            className="w-full px-4 py-3.5 rounded-xl border border-slate-200
            focus:outline-none focus:ring-2 focus:ring-blue-500
            focus:border-transparent transition"
          />

        </div>

        {/* Password */}
        <div>

          <div className="flex justify-between items-center mb-2">

            <label className="text-sm font-semibold">
              Password
            </label>

            <button
              type="button"
              className="text-sm text-blue-600 hover:underline"
            >
              Forgot password?
            </button>

          </div>

          <div className="relative">

            <input
              type={showPassword ? "text" : "password"}
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
              className="w-full px-4 py-3.5 pr-12 rounded-xl border border-slate-200
              focus:outline-none focus:ring-2 focus:ring-blue-500
              focus:border-transparent transition"
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500"
            >
              {showPassword ? "🙈" : "👁️"}
            </button>

          </div>

        </div>

        {/* Remember me */}
        <div className="flex items-center gap-2">

          <input
            type="checkbox"
            className="w-4 h-4 accent-blue-600"
          />

          <span className="text-sm text-slate-600">
            Remember me
          </span>

        </div>

        {/* Login */}
        <button
          type="submit"
          disabled={loading}
          className="w-full py-3.5 rounded-xl bg-blue-600
          text-white font-semibold text-lg
          hover:bg-blue-700 hover:shadow-lg
          hover:shadow-blue-500/30 transition
          disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {loading ? "Logging in…" : "Login"}
        </button>

      </form>

      {/* Divider */}
      <div className="flex items-center gap-4 my-7">

        <div className="h-px bg-slate-200 flex-1"></div>

        <span className="text-sm text-slate-400">
          OR
        </span>

        <div className="h-px bg-slate-200 flex-1"></div>

      </div>

      {/* Google - UI only */}
      <button
        type="button"
        className="w-full py-3 border border-slate-200 rounded-xl
        font-medium hover:bg-slate-50 transition"
      >
        Continue with Google
      </button>

      {/* Register */}
      <p className="text-center text-sm text-slate-600 mt-7">

        Don't have an account?{" "}

        <Link
          to="/register"
          className="text-blue-600 font-semibold hover:underline"
        >
          Create account
        </Link>

      </p>

    </AuthLayout>
  );
}

export default Login;