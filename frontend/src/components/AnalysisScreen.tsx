interface AnalysisScreenProps {
  imageUrl: string;
}

export const AnalysisScreen = ({ imageUrl }: AnalysisScreenProps) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 animate-fade-in">
      {/* Image Container with Scan Effect */}
      <div className="relative w-full max-w-md aspect-square rounded-3xl overflow-hidden mb-8">
        <img
          src={imageUrl}
          alt="Analyzing"
          className="w-full h-full object-cover opacity-60"
        />
        
        {/* Scanning Animation Overlay */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-secondary/30 to-transparent h-32 animate-scan" />
        </div>

        {/* Corner Brackets */}
        <div className="absolute top-4 left-4 w-12 h-12 border-t-2 border-l-2 border-secondary" />
        <div className="absolute top-4 right-4 w-12 h-12 border-t-2 border-r-2 border-secondary" />
        <div className="absolute bottom-4 left-4 w-12 h-12 border-b-2 border-l-2 border-secondary" />
        <div className="absolute bottom-4 right-4 w-12 h-12 border-b-2 border-r-2 border-secondary" />

        {/* Scanning Grid */}
        <div className="absolute inset-0 bg-[linear-gradient(0deg,transparent_24%,hsl(var(--secondary)/0.05)_25%,hsl(var(--secondary)/0.05)_26%,transparent_27%,transparent_74%,hsl(var(--secondary)/0.05)_75%,hsl(var(--secondary)/0.05)_76%,transparent_77%,transparent),linear-gradient(90deg,transparent_24%,hsl(var(--secondary)/0.05)_25%,hsl(var(--secondary)/0.05)_26%,transparent_27%,transparent_74%,hsl(var(--secondary)/0.05)_75%,hsl(var(--secondary)/0.05)_76%,transparent_77%,transparent)] bg-[length:50px_50px]" />
      </div>

      {/* Status Text */}
      <div className="text-center space-y-2">
        <div className="flex items-center justify-center gap-3">
          <div className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
          <p className="text-2xl font-semibold">Revealing the Aura</p>
          <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
        </div>
        <p className="text-sm text-muted-foreground">
          Analyzing visual patterns and classifications...
        </p>
      </div>

      {/* Animated Dots */}
      <div className="flex gap-2 mt-8">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-3 h-3 rounded-full bg-primary/50"
            style={{
              animation: `pulse 1.5s ease-in-out infinite`,
              animationDelay: `${i * 0.2}s`,
            }}
          />
        ))}
      </div>
    </div>
  );
};
