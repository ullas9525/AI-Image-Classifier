import { Upload, History, Zap, Sparkles, ShieldCheck } from "lucide-react"; // Added new icons
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"; // Import Card components

interface WelcomeScreenProps {
  onImageSelect: (file: File) => void;
  onHistoryClick: () => void;
}

export const WelcomeScreen = ({ onImageSelect, onHistoryClick }: WelcomeScreenProps) => {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      onImageSelect(file);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 animate-fade-in">
      <div className="flex flex-col lg:flex-row items-center lg:items-start justify-center lg:justify-between w-full max-w-6xl mx-auto gap-16">
        {/* Left Column: Logo and Uploader */}
        <div className="flex flex-col items-center lg:w-1/2 text-center"> {/* Changed lg:items-start to lg:items-center and lg:text-left to text-center */}
          <div className="mb-10"> {/* Increased margin-bottom */}
            <h1 className="text-6xl font-bold tracking-tight mb-4 bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-transparent animate-pulse-glow"> {/* Increased font size and margin-bottom */}
              AuraLens AI
            </h1>
            <p className="text-muted-foreground text-base max-w-lg mx-auto"> {/* Increased font size and max-width */}
              Unlock the hidden essence of any image with cutting-edge AI classification technology
            </p>
          </div>

          {/* Upload Button */}
          <div className="relative mb-10"> {/* Increased margin-bottom */}
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              id="image-upload"
            />
            <label htmlFor="image-upload" className="cursor-pointer">
              <div className="glass rounded-3xl p-16 hover:scale-105 transition-transform duration-300 animate-pulse-glow glow-magenta"> {/* Increased padding */}
                <div className="flex flex-col items-center gap-6"> {/* Increased gap */}
                  <div className="w-24 h-24 rounded-full bg-primary/20 flex items-center justify-center"> {/* Increased size */}
                    <Upload className="w-12 h-12 text-primary" /> {/* Increased icon size */}
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-semibold mb-2">Tap to Scan Image</p> {/* Increased font size and margin-bottom */}
                    <p className="text-base text-muted-foreground">Upload or capture a photo</p> {/* Increased font size */}
                  </div>
                </div>
              </div>
            </label>
          </div>

          {/* History Button */}
          <Button
            variant="ghost"
            size="lg"
            onClick={onHistoryClick}
            className="gap-2 text-muted-foreground hover:text-foreground transition-colors"
          >
            <History className="w-5 h-5" />
            <span>View History</span>
          </Button>
        </div>

        {/* Right Column: Feature Cards */}
        <div className="flex flex-col gap-10 lg:w-1/2"> {/* Increased gap between cards */}
          <Card className="p-4 hover:scale-105 transition-transform duration-300 hover:shadow-lg"> {/* Added hover effect and padding */}
            <CardHeader className="flex flex-row items-center gap-6"> {/* Increased gap */}
              <div className="w-14 h-14 rounded-full bg-primary/20 flex items-center justify-center"> {/* Increased size */}
                <Zap className="w-8 h-8 text-primary" /> {/* Increased icon size */}
              </div>
              <CardTitle className="text-2xl">Instant Analysis</CardTitle> {/* Increased font size */}
            </CardHeader>
            <CardContent className="pl-20"> {/* Adjusted padding to align with icon */}
              <CardDescription className="text-base">Get results in seconds with our advanced AI engine</CardDescription> {/* Increased font size */}
            </CardContent>
          </Card>

          <Card className="p-4 hover:scale-105 transition-transform duration-300 hover:shadow-lg"> {/* Added hover effect and padding */}
            <CardHeader className="flex flex-row items-center gap-6"> {/* Increased gap */}
              <div className="w-14 h-14 rounded-full bg-secondary/20 flex items-center justify-center"> {/* Increased size */}
                <Sparkles className="w-8 h-8 text-secondary" /> {/* Increased icon size */}
              </div>
              <CardTitle className="text-2xl">Precision Insights</CardTitle> {/* Increased font size */}
            </CardHeader>
            <CardContent className="pl-20"> {/* Adjusted padding to align with icon */}
              <CardDescription className="text-base">Detailed classification with confidence scores</CardDescription> {/* Increased font size */}
            </CardContent>
          </Card>

          <Card className="p-4 hover:scale-105 transition-transform duration-300 hover:shadow-lg"> {/* Added hover effect and padding */}
            <CardHeader className="flex flex-row items-center gap-6"> {/* Increased gap */}
              <div className="w-14 h-14 rounded-full bg-primary/20 flex items-center justify-center"> {/* Increased size */}
                <ShieldCheck className="w-8 h-8 text-primary" /> {/* Increased icon size */}
              </div>
              <CardTitle className="text-2xl">Secure & Private</CardTitle> {/* Increased font size */}
            </CardHeader>
            <CardContent className="pl-20"> {/* Adjusted padding to align with icon */}
              <CardDescription className="text-base">Your images are processed securely and privately</CardDescription> {/* Increased font size */}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Footer Info */}
      <div className="absolute bottom-8 text-center">
        <p className="text-xs text-muted-foreground">
          Powered by advanced AI • Instant results
        </p>
      </div>
    </div>
  );
};
