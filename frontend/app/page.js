"use client";

import VerificationForm from "@/components/VerificationForm";

export default function Home() {
  return (
    <main className="relative min-h-dvh overflow-hidden">
      {/* Decorative background shapes */}
      <div aria-hidden className="pointer-events-none absolute inset-0">
        <div className="absolute -top-24 -left-24 w-[36rem] h-[36rem] rounded-full animated-gradient blur-3xl"></div>
        <div className="absolute -bottom-24 -right-24 w-[30rem] h-[30rem] rounded-full animated-gradient blur-3xl"></div>
      </div>

      {/* Header */}
      <header className="px-6 pt-10">
        <div className="container">
          <div className="flex items-center justify-between">
            <h1 className="text-4xl font-extrabold tracking-tight text-gradient">FactCheckit</h1>
          </div>
          <div className="mt-2 text-gray-600">
            <p className="text-base">AI-powered Crisis News & Claim Verification</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <section className="px-6 py-10">
        <div className="container grid gap-8">
          <div className="glass-surface rounded-3xl soft-glow">
            <div className="p-8 md:p-10">
              <VerificationForm />
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 pb-10">
        <div className="container text-center text-gray-500 text-sm">
          <p>Helping you understand verified news during crises</p>
        </div>
      </footer>
    </main>
  );
}

