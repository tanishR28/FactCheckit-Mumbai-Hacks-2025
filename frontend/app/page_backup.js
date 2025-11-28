export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="py-6 px-4 border-b border-gray-200 bg-white/80 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <span className="text-4xl">✓</span>
            <span>FactCheckit</span>
          </h1>
          <p className="text-gray-600 mt-1">AI-powered Crisis News & Claim Verification</p>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <VerificationForm />
      </div>

      {/* Footer */}
      <footer className="py-6 text-center text-gray-500 text-sm">
        <p>Helping you understand verified news during crises</p>
      </footer>
    </main>
  );
}
