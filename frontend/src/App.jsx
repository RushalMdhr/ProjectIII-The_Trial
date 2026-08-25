import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import InterviewSetup from "./pages/InterviewSetup";
import Interview from "./pages/Interview";
// import Feedback from "./pages/Feedback";
import Results from "./pages/Results";
import Test from "./pages/test";
function App() {
  return (
    <BrowserRouter>

      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/interview-setup" element={<InterviewSetup />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/test" element={<Test />} />
        {/* <Route path="/feedback" element={<Feedback />} /> */}
        <Route path="/results" element={<Results />} />
      </Routes>

    </BrowserRouter>
  );
}

export default App;