export default function ResultCard({ result }) {
  const getVerdictStyle = (verdict) => {
    switch (verdict) {
      case "TRUE":
        return {
          bg: "bg-green-50",
          border: "border-green-200",
          badge: "bg-green-600",
          text: "text-green-800",
          icon: "✓"
        };
      case "FALSE":
        return {
          bg: "bg-red-50",
          border: "border-red-200",
          badge: "bg-red-600",
          text: "text-red-800",
          icon: "✗"
        };
      case "MISLEADING":
        return {
          bg: "bg-yellow-50",
          border: "border-yellow-200",
          badge: "bg-yellow-600",
          text: "text-yellow-800",
          icon: "⚠"
        };
      case "UNVERIFIED":
        return {
          bg: "bg-gray-50",
          border: "border-gray-200",
          badge: "bg-gray-600",
          text: "text-gray-800",
          icon: "?"
        };
      default:
        return {
          bg: "bg-gray-50",
          border: "border-gray-200",
          badge: "bg-gray-600",
          text: "text-gray-800",
          icon: "?"
        };
    }
  };

  const style = getVerdictStyle(result.verdict);

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
      {/* Verdict Header */}
      <div className={`${style.bg} ${style.border} border-b px-8 py-6`}>
        <div className="flex items-center gap-3 mb-2">
          <span className={`${style.badge} text-white px-4 py-1.5 rounded-full text-sm font-semibold flex items-center gap-2`}>
            <span className="text-lg">{style.icon}</span>
            {result.verdict}
          </span>
          <span className="text-sm text-gray-600">
            Confidence: {(result.confidence_score * 100).toFixed(0)}%
          </span>
        </div>
        <h3 className={`text-xl font-semibold ${style.text} mt-2`}>
          {result.verdict === "TRUE" && "This claim is true"}
          {result.verdict === "FALSE" && "This claim is false"}
          {result.verdict === "MISLEADING" && "This claim is misleading"}
          {result.verdict === "UNVERIFIED" && "We couldn't verify this claim"}
        </h3>
      </div>

      {/* Content */}
      <div className="px-8 py-6 space-y-6">
        {/* Real News Summary */}
        <div>
          <h4 className="text-lg font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <span>📰</span>
            Real News Summary
          </h4>
          <p className="text-gray-700 leading-relaxed">
            {result.real_news_summary}
          </p>
        </div>

        {/* Detailed Explanation */}
        <div>
          <h4 className="text-lg font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <span>💡</span>
            Detailed Explanation
          </h4>
          <p className="text-gray-700 leading-relaxed">
            {result.detailed_explanation}
          </p>
        </div>

        {/* Evidence Points */}
        {result.evidence_points && result.evidence_points.length > 0 && (
          <div>
            <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <span>🔍</span>
              Evidence Points
            </h4>
            <ul className="space-y-3">
              {result.evidence_points.map((evidence, index) => (
                <li key={index} className="flex gap-3">
                  <span className="text-blue-600 font-semibold mt-0.5">
                    {index + 1}.
                  </span>
                  <div>
                    <p className="text-gray-700">{evidence.point}</p>
                    {evidence.source && (
                      <p className="text-sm text-gray-500 mt-1">
                        Source: {evidence.source}
                      </p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Sources */}
        {result.sources && result.sources.length > 0 && (
          <div>
            <h4 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <span>🔗</span>
              Sources
            </h4>
            <ul className="space-y-2">
              {result.sources.map((source, index) => (
                <li key={index}>
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-2"
                  >
                    <span className="text-sm">🌐</span>
                    <span className="font-medium">{source.title}</span>
                    {source.publisher && (
                      <span className="text-sm text-gray-500">
                        - {source.publisher}
                      </span>
                    )}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Agent Reasoning (Optional) */}
        {result.agent_reasoning && (
          <div className="pt-4 border-t border-gray-200">
            <details className="text-sm">
              <summary className="cursor-pointer text-gray-600 hover:text-gray-900 font-medium">
                How was this verified? (Technical Details)
              </summary>
              <p className="mt-2 text-gray-600 text-xs bg-gray-50 p-3 rounded">
                {result.agent_reasoning}
              </p>
            </details>
          </div>
        )}

        {/* Original Claim */}
        <div className="pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            <strong>Original claim:</strong> {result.original_claim}
          </p>
          {result.extracted_claim !== result.original_claim && (
            <p className="text-xs text-gray-500 mt-1">
              <strong>Analyzed as:</strong> {result.extracted_claim}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
