import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { register } from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError(null);
    setSuccess(null);

    // -----------------------------
    // FRONTEND VALIDATION
    // -----------------------------

    if (form.password !== form.confirmPassword) {
      setError("Passwords don't match.");
      return;
    }

    if (form.password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    // -----------------------------
    // CALL OUR API
    // -----------------------------

    setLoading(true);

    try {
      const res = await register(
        form.name,
        form.email,
        form.password
      );

      console.log("Register response:", res);

      // -----------------------------
      // CHECK API RESPONSE
      // -----------------------------

      if (!res.success) {
        setError(res.message);
        return;
      }

      // -----------------------------
      // REGISTRATION SUCCESS
      // -----------------------------

      setSuccess(res.message);

      // Wait a little so user can see success message
      setTimeout(() => {
        navigate("/login");
      }, 1000);

    } catch (err) {
      console.error("Registration error:", err);

      setError("Couldn't create your account. Try again.");

    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Create your account"
      subtitle="Start your journey toward interview success."
    >

      <form onSubmit={handleSubmit} className="space-y-4">

        {/* ERROR MESSAGE */}
        {error && (
          <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2.5">
            {error}
          </div>
        )}

        {/* SUCCESS MESSAGE */}
        {success && (
          <div className="text-sm text-green-600 bg-green-50 border border-green-200 rounded-lg px-4 py-2.5">
            {success}
          </div>
        )}

        {/* Full Name */}
        <div>

          <label className="block text-sm font-semibold mb-2">
            Full Name
          </label>

          <input
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Enter your full name"
            required
            className="w-full px-4 py-3 rounded-xl border border-slate-200
            focus:outline-none focus:ring-2 focus:ring-blue-500
            focus:border-transparent transition"
          />

        </div>

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
            className="w-full px-4 py-3 rounded-xl border border-slate-200
            focus:outline-none focus:ring-2 focus:ring-blue-500
            focus:border-transparent transition"
          />

        </div>

        {/* Password */}
        <div>

          <label className="block text-sm font-semibold mb-2">
            Password
          </label>

          <div className="relative">

            <input
              type={showPassword ? "text" : "password"}
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Create a password"
              required
              className="w-full px-4 py-3 pr-12 rounded-xl border border-slate-200
              focus:outline-none focus:ring-2 focus:ring-blue-500"
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

        {/* Confirm Password */}
        <div>

          <label className="block text-sm font-semibold mb-2">
            Confirm Password
          </label>

          <div className="relative">

            <input
              type={showConfirmPassword ? "text" : "password"}
              name="confirmPassword"
              value={form.confirmPassword}
              onChange={handleChange}
              placeholder="Confirm your password"
              required
              className="w-full px-4 py-3 pr-12 rounded-xl border border-slate-200
              focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button
              type="button"
              onClick={() =>
                setShowConfirmPassword(!showConfirmPassword)
              }
              className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500"
            >
              {showConfirmPassword ? "🙈" : "👁️"}
            </button>

          </div>

        </div>

        {/* Terms */}
        <div className="flex items-start gap-2 pt-1">

          <input
            type="checkbox"
            required
            className="w-4 h-4 mt-1 accent-blue-600"
          />

          <p className="text-sm text-slate-500">
            I agree to the Terms of Service and Privacy Policy.
          </p>

        </div>

        {/* Register */}
        <button
          type="submit"
          disabled={loading}
          className="w-full py-3.5 rounded-xl bg-blue-600
          text-white font-semibold text-lg
          hover:bg-blue-700 hover:shadow-lg
          hover:shadow-blue-500/30 transition duration-300
          disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {loading ? "Creating account…" : "Create Account"}
        </button>

      </form>

      {/* Login */}
      <p className="text-center text-sm text-slate-600 mt-7">

        Already have an account?{" "}

        <Link
          to="/login"
          className="text-blue-600 font-semibold hover:underline"
        >
          Login
        </Link>

      </p>

    </AuthLayout>
  );
}

export default Register;