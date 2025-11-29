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

  // Derived metrics for UX (does not alter logic)
  const recommendedMax = 300;
  const progress = Math.min((claim.length / recommendedMax) * 100, 100);

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
      {/* Input Form: two-column glass card */}
      <div className="rounded-3xl p-0 border border-white/50 bg-white/70 backdrop-blur-lg shadow-lg overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-5">
          {/* Left: Form */}
          <div className="md:col-span-3 p-8 md:p-10">
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Verify a Claim</h2>
            <p className="text-gray-600 mb-6">Paste any news headline or claim below to check its accuracy.</p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <label className="block text-sm font-medium text-gray-700">Claim or Headline</label>
              <div className="rounded-2xl border border-gray-300 focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-200 bg-white/80">
                <textarea
                  value={claim}
                  onChange={(e) => setClaim(e.target.value)}
                  placeholder="Paste a news headline or claim here..."
                  className="w-full px-4 py-3 rounded-2xl resize-none h-36 text-gray-900 bg-transparent outline-none"
                  disabled={loading}
                />
              </div>

              {/* Counters & actions */}
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">{claim.length} characters</span>
                  <span className="text-sm text-gray-500">Aim for concise, factual wording</span>
                </div>
                <div className="h-1.5 w-full rounded-full bg-gray-200 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 transition-[width] duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <div className="flex justify-end">
                  {claim && (
                    <button
                      type="button"
                      onClick={handleReset}
                      className="text-sm text-gray-600 hover:text-gray-800"
                    >
                      Clear input
                    </button>
                  )}
                </div>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">{error}</div>
              )}

              <button
                type="submit"
                disabled={loading || !claim.trim()}
                className="w-full md:w-auto btn-primary inline-flex items-center justify-center gap-2"
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
                  <>Verify Claim</>
                )}
              </button>
            </form>
          </div>

          {/* Right: Helper panel */}
          <aside className="md:col-span-2 border-t md:border-t-0 md:border-l border-white/50 p-8 md:p-10 bg-white/60">
            <div className="space-y-8">
              <div>
                <h3 className="text-2xl font-bold tracking-tight text-gradient mb-2">Write clear, verifiable claims</h3>
                <p className="text-sm text-gray-600 mb-4">Stronger inputs lead to more reliable verification.</p>
                <div className="grid grid-cols-1 gap-3">
                  <div className="rounded-2xl border border-gray-200 bg-white/85 px-4 py-3 text-[0.95rem] text-gray-800">Include key details (who, what, where, when).</div>
                  <div className="rounded-2xl border border-gray-200 bg-white/85 px-4 py-3 text-[0.95rem] text-gray-800">Prefer the original headline or precise claim text.</div>
                  <div className="rounded-2xl border border-gray-200 bg-white/85 px-4 py-3 text-[0.95rem] text-gray-800">Avoid opinions; use factual statements when possible.</div>
                </div>
              </div>

              <div>
                <h4 className="text-2xl font-bold tracking-tight text-gradient mb-2">Good examples</h4>
                <p className="text-sm text-gray-600 mb-4">Well-structured, factual statements the system understands reliably.</p>
                <div className="space-y-3">
                  <div className="rounded-2xl border border-gray-200 bg-white/85 px-4 py-3">
                    <p className="text-base text-gray-900">City X recorded a 7.2 magnitude earthquake on Friday.</p>
                  </div>
                  <div className="rounded-2xl border border-gray-200 bg-white/85 px-4 py-3">
                    <p className="text-base text-gray-900">The government announced a nationwide internet shutdown today.</p>
                  </div>
                  <div className="rounded-2xl border border-gray-200 bg-white/85 px-4 py-3">
                    <p className="text-base text-gray-900">Airline Y canceled 45 flights due to severe weather warnings.</p>
                  </div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>

      {/* Loading State */}
      {loading && <Loader />}

      {/* Result */}
      {result && !loading && <ResultCard result={result} />}
    </div>
  );
}
