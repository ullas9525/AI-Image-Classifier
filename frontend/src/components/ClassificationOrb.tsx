import { ClassificationResult } from "./ResultsScreen";

interface ClassificationOrbProps {
  results: ClassificationResult[]; // Still an array, but now contains a single top result
}

export const ClassificationOrb = ({ results }: ClassificationOrbProps) => {
  const size = 350; // Increased size for a bigger orb
  const strokeWidth = 25; // Adjusted stroke width
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;

  const topResult = results[0];
  const confidencePercentage = topResult ? (topResult.confidence * 100).toFixed(0) : "0";
  const strokeDashoffset = circumference - (parseFloat(confidencePercentage) / 100) * circumference;

  return (
    <div className="flex items-center justify-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="hsl(var(--muted))"
            strokeWidth={strokeWidth}
            opacity={0.1}
          />

          {/* Classification segment */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="hsl(var(--primary))"
            strokeWidth={strokeWidth}
            strokeDasharray={`${circumference} ${circumference}`}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{
              transform: `rotate(${-90}deg)`,
              transformOrigin: 'center',
              filter: 'drop-shadow(0 0 8px hsl(var(--primary)))',
              transition: 'all 1s ease-out',
            }}
            opacity={1}
          />
        </svg>

        {/* Center text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl font-bold bg-gradient-to-br from-primary to-secondary bg-clip-text text-transparent mb-1">
              {confidencePercentage}
              <span className="text-3xl">%</span>
            </div>
            <div className="text-xs text-muted-foreground font-medium">MATCH</div>
          </div>
        </div>
      </div>
    </div>
  );
};
