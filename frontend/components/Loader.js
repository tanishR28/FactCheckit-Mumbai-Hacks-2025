export default function Loader() {
  return (
    <div className="rounded-2xl p-8 border border-white/50 bg-white/70 backdrop-blur-lg shadow-lg">
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
        <div className="flex gap-4 text-sm text-gray-500">
          <span className="animate-pulse">Extracting claim</span>
          <span className="animate-pulse delay-200">Cross-referencing</span>
          <span className="animate-pulse delay-400">Analyzing</span>
        </div>
      </div>
    </div>
  );
}
