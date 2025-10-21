import { useState } from "react";
import Navbar from "@/components/Navbar"; // Import the new Navbar component
import { WelcomeScreen } from "@/components/WelcomeScreen";
import { AnalysisScreen } from "@/components/AnalysisScreen";
import { ResultsScreen } from "@/components/ResultsScreen";

interface ClassificationResult {
  prediction: string;
  confidence: number;
}
import { useToast } from "@/hooks/use-toast";

type Screen = "welcome" | "analyzing" | "results";

const Index = () => {
  const [currentScreen, setCurrentScreen] = useState<Screen>("welcome");
  const [imageUrl, setImageUrl] = useState<string>("");
  const [results, setResults] = useState<ClassificationResult[]>([]);
  const { toast } = useToast();

  const handleImageSelect = async (file: File) => {
    const url = URL.createObjectURL(file);
    setImageUrl(url);
    setCurrentScreen("analyzing");

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/classify', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ClassificationResult = await response.json();
      setResults([data]); // Wrap the single result in an array for ResultsScreen
      setCurrentScreen("results");
    } catch (error) {
      console.error("Error classifying image:", error);
      toast({
        title: "Classification Failed",
        description: "There was an error classifying the image. Please try again.",
        variant: "destructive",
      });
      setCurrentScreen("welcome"); // Go back to welcome screen on error
    }
  };

  const handleNewScan = () => {
    setCurrentScreen("welcome");
    setImageUrl("");
    setResults([]);
  };

  const handleSaveToHistory = () => {
    toast({
      title: "Saved to History",
      description: "Your analysis has been saved successfully.",
    });
  };

  const handleHistoryClick = () => {
    toast({
      title: "History",
      description: "History feature coming soon!",
    });
  };

  const handleBack = () => {
    setCurrentScreen("welcome");
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      {currentScreen === "welcome" && (
        <WelcomeScreen
          onImageSelect={handleImageSelect}
          onHistoryClick={handleHistoryClick}
        />
      )}

      {currentScreen === "analyzing" && (
        <AnalysisScreen imageUrl={imageUrl} />
      )}

      {currentScreen === "results" && (
        <ResultsScreen
          imageUrl={imageUrl}
          results={results}
          onNewScan={handleNewScan}
          onSaveToHistory={handleSaveToHistory}
          onBack={handleBack}
        />
      )}
    </div>
  );
};

export default Index;
