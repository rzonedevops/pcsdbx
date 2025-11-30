import DashboardLayout from "@/components/DashboardLayout";
import { CheckCircle2, Circle, Clock, Flag } from "lucide-react";

const milestones = [
  {
    month: "Month 1",
    date: "November 2025",
    title: "Data Foundation",
    status: "completed",
    metrics: [
      { label: "Listings", value: "613", target: "75", status: "exceeded" },
      { label: "Categories", value: "61", target: "15", status: "exceeded" },
    ],
    description: "Massively exceeded all targets. Established comprehensive supplier database structure and schema compliance.",
  },
  {
    month: "Month 3",
    date: "January 2026",
    title: "Breadth Expansion",
    status: "completed",
    metrics: [
      { label: "Listings", value: "613", target: "300", status: "exceeded" },
      { label: "Categories", value: "61", target: "75", status: "on-track" },
    ],
    description: "Achieved listing targets 90+ days ahead of schedule. Focus shifting to category breadth and strategic depth.",
  },
  {
    month: "Month 6",
    date: "April 2026",
    title: "Product Mapping",
    status: "upcoming",
    metrics: [
      { label: "Listings", value: "Target: 500+", target: "500", status: "pending" },
      { label: "Categories", value: "Target: 150+", target: "150", status: "pending" },
    ],
    description: "Activation of Component 2 (Product-Supplier Mapping) and Component 3 (Pricing Intelligence Pilot).",
  },
  {
    month: "Month 12",
    date: "November 2026",
    title: "Ecosystem Integration",
    status: "upcoming",
    metrics: [
      { label: "Listings", value: "Target: 1000+", target: "1000", status: "pending" },
      { label: "Coverage", value: "100%", target: "100%", status: "pending" },
    ],
    description: "Full integration with SKIN-TWIN Formulation Engine and deployment of Constraint Optimization.",
  },
];

export default function Milestones() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="flex flex-col gap-2">
          <h1 className="text-4xl font-display font-bold bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
            Milestone Timeline
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl">
            Tracking the strategic evolution of the platform from data foundation to full ecosystem integration.
          </p>
        </div>

        <div className="relative space-y-12 before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-white/10 before:to-transparent">
          {milestones.map((milestone, index) => (
            <div
              key={index}
              className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active"
            >
              {/* Icon Node */}
              <div className="absolute left-0 md:left-1/2 -translate-x-1/2 flex items-center justify-center w-10 h-10 rounded-full border-4 border-background bg-card shadow-lg z-10 group-hover:scale-110 transition-transform duration-300">
                {milestone.status === "completed" ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                ) : milestone.status === "current" ? (
                  <Clock className="w-5 h-5 text-amber-400 animate-pulse" />
                ) : (
                  <Circle className="w-5 h-5 text-muted-foreground" />
                )}
              </div>

              {/* Content Card */}
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] glass-card p-6 rounded-3xl hover:bg-white/5 transition-colors duration-300">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <span className="px-3 py-1 rounded-full bg-white/5 text-xs font-bold uppercase tracking-wider text-muted-foreground">
                      {milestone.month}
                    </span>
                    <span className="text-sm text-muted-foreground">{milestone.date}</span>
                  </div>
                  {milestone.status === "completed" && (
                    <Flag className="w-4 h-4 text-emerald-400" />
                  )}
                </div>

                <h3 className="text-xl font-bold font-display mb-2">{milestone.title}</h3>
                <p className="text-muted-foreground text-sm mb-6 leading-relaxed">
                  {milestone.description}
                </p>

                <div className="grid grid-cols-2 gap-4">
                  {milestone.metrics.map((metric, i) => (
                    <div key={i} className="bg-black/20 rounded-xl p-3 border border-white/5">
                      <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
                        {metric.label}
                      </div>
                      <div className="flex items-baseline gap-2">
                        <span className="text-lg font-bold font-mono">{metric.value}</span>
                        {metric.status === "exceeded" && (
                          <span className="text-[10px] text-emerald-400 font-bold">EXCEEDED</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
}
