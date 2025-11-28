"use client";

import { useState } from "react";
import axios from "axios";
import ResultCard from "./ResultCard";
import Loader from "./Loader";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function VerificationForm() {
  const [claim, setClaim] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!claim.trim()) {
      setError("Please enter a claim to verify");
      return;
    }

    if (claim.length < 10) {
      setError("Please enter a longer claim (at least 10 characters)");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/api/verify`, {
        claim: claim.trim()
      });

      setResult(response.data);
    } catch (err) {
      console.error("Verification error:", err);
      setError(
        err.response?.data?.detail || 
        "Failed to verify claim. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setClaim("");
    setResult(null);
    setError(null);
  };

  return (
    <div className="space-y-6">
      {/* Input Form */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Verify a Claim
        </h2>
        <p className="text-gray-600 mb-6">
          Paste any news headline or claim below to check its accuracy.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <textarea
              value={claim}
              onChange={(e) => setClaim(e.target.value)}
              placeholder="Paste a news headline or claim here..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-32 text-gray-900"
              disabled={loading}
            />
            <div className="flex justify-between items-center mt-2">
              <span className="text-sm text-gray-500">
                {claim.length} characters
              </span>
              {claim && (
                <button
                  type="button"
                  onClick={handleReset}
                  className="text-sm text-gray-500 hover:text-gray-700"
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !claim.trim()}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Verifying...
              </>
            ) : (
              <>
                <span>🔍</span>
                Verify Claim
              </>
            )}
          </button>
        </form>
      </div>

      {/* Loading State */}
      {loading && <Loader />}

      {/* Result */}
      {result && !loading && <ResultCard result={result} />}
    </div>
  );
}
