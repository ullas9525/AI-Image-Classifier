import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ClassificationOrb } from "./ClassificationOrb";

export interface ClassificationResult {
  prediction: string;
  confidence: number;
  all_confidences?: { [breed: string]: number }; // Optional, as it might only be present in the main result object
}

interface ResultsScreenProps {
  imageUrl: string;
  results: ClassificationResult; // Now expects a single ClassificationResult object
  onNewScan: () => void;
  onSaveToHistory: () => void;
  onBack: () => void;
}

export const ResultsScreen = ({
  imageUrl,
  results, // This is now a single object, not an array
  onNewScan,
  onSaveToHistory,
  onBack,
}: ResultsScreenProps) => {
  const topResult = results; // The main result is now the top result

  // Convert all_confidences into an array of { prediction, confidence } for the breakdown
  const breakdownResults = topResult.all_confidences
    ? Object.entries(topResult.all_confidences)
        .map(([prediction, confidence]) => ({ prediction, confidence }))
        .sort((a, b) => b.confidence - a.confidence) // Sort by confidence descending
    : [];

  return (
    <div className="flex flex-col lg:flex-row min-h-screen w-full max-w-7xl mx-auto p-6 gap-8 animate-fade-in">
      {/* Left Column */}
      <div className="flex flex-col items-center justify-center lg:justify-start pt-16 lg:pt-24 flex-1">
        {/* Header with Image Thumbnail */}
        <div className="flex items-center gap-4 mb-8 w-full">
          <Button
            variant="ghost"
            size="icon"
            onClick={onBack}
            className="rounded-full"
          >
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div className="w-16 h-16 rounded-2xl overflow-hidden border-2 border-primary/30">
            <img
              src={imageUrl}
              alt="Analyzed"
              className="w-full h-full object-cover"
            />
          </div>
          <div className="flex-1">
            <h2 className="text-sm font-medium text-muted-foreground">Analysis Complete</h2>
            <p className="text-xs text-muted-foreground">Tap for details</p>
          </div>
        </div>

        {/* Primary Result with Classification Orb */}
        <div className="mb-8">
          {/* Pass the single result object, ClassificationOrb will need to be updated too */}
          <ClassificationOrb results={[topResult]} />
        </div>

        {/* Primary Identification */}
        <div className="flex flex-col items-center mb-8 w-full">
          <h1 className="text-4xl font-bold mb-2">{topResult.prediction}</h1>
          <div className="inline-flex items-center gap-2 glass rounded-full px-4 py-2">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            <span className="text-sm font-medium">
              {(topResult.confidence * 100).toFixed(1)}% Certainty
            </span>
          </div>
        </div>
      </div>

      {/* Right Column - Detailed Breakdown */}
      <div className="flex justify-center lg:justify-end pt-16 lg:pt-24">
        <div className="glass rounded-3xl p-12 space-y-5 w-full max-w-2xl h-fit">
          <h3 className="text-lg font-semibold text-muted-foreground mb-8">
            CLASSIFICATION BREAKDOWN
          </h3>
          {breakdownResults.slice(0, 5).map((result, index) => (
            <div
              key={index}
              className="space-y-4 pb-5 border-b border-border/50 last:border-0 last:pb-0"
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-xl">{result.prediction}</span>
                <span className="text-lg text-muted-foreground">
                  {(result.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-muted/30 rounded-full h-4 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-1000"
                  style={{
                    width: `${(result.confidence * 100).toFixed(1)}%`,
                    background:
                      index === 0
                        ? 'hsl(var(--primary))'
                        : 'hsl(var(--secondary))',
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
