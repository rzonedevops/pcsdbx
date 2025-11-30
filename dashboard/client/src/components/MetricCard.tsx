import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: string;
  trend?: "up" | "down" | "neutral";
  icon: LucideIcon;
  description?: string;
  className?: string;
  delay?: number;
}

export default function MetricCard({
  title,
  value,
  change,
  trend = "neutral",
  icon: Icon,
  description,
  className,
  delay = 0,
}: MetricCardProps) {
  return (
    <div
      className={cn(
        "glass-card p-6 rounded-3xl relative overflow-hidden group transition-all duration-300 hover:translate-y-[-4px] hover:shadow-primary/10",
        className
      )}
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Background Glow on Hover */}
      <div className="absolute -right-10 -top-10 w-32 h-32 bg-primary/10 rounded-full blur-3xl group-hover:bg-primary/20 transition-all duration-500" />

      <div className="relative z-10">
        <div className="flex items-start justify-between mb-4">
          <div className="p-3 rounded-2xl bg-white/5 border border-white/5 group-hover:border-primary/20 transition-colors duration-300">
            <Icon className="w-6 h-6 text-primary" />
          </div>
          {change && (
            <div
              className={cn(
                "px-3 py-1 rounded-full text-xs font-bold border backdrop-blur-sm",
                trend === "up"
                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                  : trend === "down"
                  ? "bg-rose-500/10 text-rose-400 border-rose-500/20"
                  : "bg-white/5 text-muted-foreground border-white/10"
              )}
            >
              {change}
            </div>
          )}
        </div>

        <div className="space-y-1">
          <h3 className="text-sm font-medium text-muted-foreground tracking-wide uppercase">
            {title}
          </h3>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl md:text-4xl font-bold font-display tracking-tight text-foreground glow-text">
              {value}
            </span>
          </div>
          {description && (
            <p className="text-sm text-muted-foreground/80 mt-2 leading-relaxed">
              {description}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
