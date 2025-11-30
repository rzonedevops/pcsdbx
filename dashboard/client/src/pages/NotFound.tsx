import { Button } from "@/components/ui/button";
import { ArrowLeft, Home } from "lucide-react";
import { Link } from "wouter";

export default function NotFound() {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-background relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-primary/5 blur-[120px]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-secondary/5 blur-[120px]" />
      </div>

      <div className="relative z-10 text-center px-4">
        <div className="mb-8 relative inline-block">
          <div className="text-[150px] font-bold font-display leading-none bg-gradient-to-b from-white/20 to-transparent bg-clip-text text-transparent select-none">
            404
          </div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-2xl font-bold text-primary tracking-[1em] uppercase">
            Lost
          </div>
        </div>

        <h1 className="text-4xl font-bold font-display mb-4">Page Not Found</h1>
        <p className="text-muted-foreground max-w-md mx-auto mb-8 text-lg">
          The coordinates you're looking for don't exist in our ecosystem. Let's get you back on track.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/">
            <Button size="lg" className="gap-2">
              <Home className="w-4 h-4" />
              Return Home
            </Button>
          </Link>
          <Button variant="outline" size="lg" className="gap-2" onClick={() => window.history.back()}>
            <ArrowLeft className="w-4 h-4" />
            Go Back
          </Button>
        </div>
      </div>
    </div>
  );
}
