import React from "react";
import { ArrowUpRight, Sparkles } from "lucide-react";

export default function Footer() {
  return (
    <footer className="ai-footer">
      <div className="ai-footer-inner">

        {/* TOP SECTION */}
        <div className="ai-footer-top">

          {/* BRAND */}
          <div className="ai-footer-brand">
            <div className="ai-footer-logo">
              <div className="ai-footer-logo-icon">
                <Sparkles size={18} />
              </div>

              <span>AI HELPER</span>
            </div>

            <p>
              Your AI-powered career coach for smarter preparation,
              better answers, and interview confidence.
            </p>
          </div>


          {/* PRODUCT */}
          <div className="ai-footer-column">
            <h4>Product</h4>

            <a href="/">Home</a>
            <a href="/interview-setup">Mock Interview</a>
            <a href="/results">Results</a>
          </div>


          {/* RESOURCES */}
          <div className="ai-footer-column">
            <h4>Resources</h4>

            <a href="/">Career Guidance</a>
            <a href="/">Interview Practice</a>
            <a href="/">Resume Help</a>
          </div>


          {/* GET STARTED */}
          <div className="ai-footer-column">
            <h4>Get Started</h4>

            <a href="/login">
              Login
              <ArrowUpRight size={14} />
            </a>

            <a href="/register">
              Create Account
              <ArrowUpRight size={14} />
            </a>
          </div>

        </div>


        {/* DIVIDER */}
        <div className="ai-footer-divider" />


        {/* BOTTOM */}
        <div className="ai-footer-bottom">

          <span>
            © 2026 AI HELPER. All rights reserved.
          </span>

          <span>
            Built for better interviews.
          </span>

        </div>

      </div>
    </footer>
  );
}