"use client";

import VerificationForm from "@/components/VerificationForm";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="py-6 px-4 border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-10 shadow-sm">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                <span className="text-4xl">✓</span>
                <span>FactCheckit</span>
              </h1>
              <p className="text-gray-600 mt-1 text-sm sm:text-base">🇮🇳 AI-powered Crisis News & Claim Verification</p>
            </div>
            <div className="hidden sm:flex flex-col items-end text-xs text-gray-500">
              <span className="font-semibold text-green-600">● Live</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <VerificationForm />
        
        {/* Info Banner - Moved to bottom */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-4 flex items-start gap-3">
          <span className="text-2xl">🇮🇳</span>
          <div>
            <h3 className="font-semibold text-blue-900 mb-1">Powered by Indian Fact-Checkers</h3>
            <p className="text-sm text-blue-700">We verify claims using PIB, Alt News, BOOM Live, Factly, Vishvas News + AI analysis</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-8 text-center text-gray-500 text-sm border-t border-gray-200 mt-12">
        <p className="mb-2">🔍 Helping you understand verified news during crises</p>
        <p className="text-xs text-gray-400">Powered by Google Gemini AI • 100% Real-time Verification</p>
      </footer>
    </main>
  );
}

