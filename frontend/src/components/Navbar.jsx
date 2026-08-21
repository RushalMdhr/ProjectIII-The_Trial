import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-white shadow-md px-8 py-4 flex items-center justify-between">

      {/* Logo */}
      <Link to="/" className="text-2xl font-bold text-blue-600">
        InterviewAI
      </Link>

      {/* Navigation */}
      <div className="flex items-center gap-4">

        <Link
          to="/login"
          className="px-5 py-2 text-blue-600 font-semibold border border-blue-600 rounded-lg hover:bg-blue-50 transition"
        >
          Login
        </Link>

        <Link
          to="/register"
          className="px-5 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition"
        >
          Register
        </Link>

      </div>
    </nav>
  );
}

export default Navbar;