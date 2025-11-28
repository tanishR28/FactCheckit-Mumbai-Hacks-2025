export default function Loader() {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
      <div className="flex flex-col items-center justify-center py-8 space-y-4">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
        </div>
        <div className="text-center space-y-2">
          <h3 className="text-xl font-semibold text-gray-800">
            Verifying your claim...
          </h3>
          <p className="text-gray-600 text-sm">
            Our AI is checking multiple sources
          </p>
        </div>
        <div className="flex gap-2 text-sm text-gray-500">
          <span className="animate-pulse">🔍 Extracting claim</span>
          <span className="animate-pulse delay-100">→</span>
          <span className="animate-pulse delay-200">✓ Cross-referencing</span>
          <span className="animate-pulse delay-300">→</span>
          <span className="animate-pulse delay-400">📊 Analyzing</span>
        </div>
      </div>
    </div>
  );
}
