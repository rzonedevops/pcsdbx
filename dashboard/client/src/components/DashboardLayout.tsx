import { cn } from "@/lib/utils";
import { Activity, BarChart3, Database, Layers, LayoutDashboard, Settings } from "lucide-react";
import { Link, useLocation } from "wouter";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [location] = useLocation();

  const navItems = [
    { icon: LayoutDashboard, label: "Overview", href: "/" },
    { icon: Database, label: "Supplier Data", href: "/suppliers" },
    { icon: Layers, label: "Ecosystem", href: "/ecosystem" },
    { icon: Activity, label: "Milestones", href: "/milestones" },
    { icon: BarChart3, label: "Analytics", href: "/analytics" },
    { icon: Settings, label: "Settings", href: "/settings" },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      {/* Ambient Background Elements */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/5 blur-[120px] animate-pulse duration-[10s]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary/5 blur-[120px] animate-pulse duration-[15s]" />
        <div className="absolute top-[20%] right-[20%] w-[20%] h-[20%] rounded-full bg-accent/5 blur-[100px] animate-pulse duration-[12s]" />
      </div>

      <div className="relative z-10 flex min-h-screen">
        {/* Sidebar Navigation */}
        <aside className="hidden lg:flex flex-col w-64 border-r border-border/50 bg-background/30 backdrop-blur-xl sticky top-0 h-screen">
          <div className="p-6 flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/20">
              <div className="w-3 h-3 bg-white rounded-full" />
            </div>
            <span className="font-display text-xl font-bold tracking-wide">PCSDBX</span>
          </div>

          <nav className="flex-1 px-4 py-6 space-y-2">
            {navItems.map((item) => {
              const isActive = location === item.href;
              return (
                <Link key={item.href} href={item.href}>
                  <div
                    className={cn(
                      "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group cursor-pointer",
                      isActive
                        ? "bg-primary/10 text-primary shadow-[0_0_20px_-5px_var(--primary)]"
                        : "text-muted-foreground hover:text-foreground hover:bg-secondary/20"
                    )}
                  >
                    <item.icon
                      className={cn(
                        "w-5 h-5 transition-transform duration-300",
                        isActive ? "scale-110" : "group-hover:scale-110"
                      )}
                    />
                    <span className="font-medium">{item.label}</span>
                    {isActive && (
                      <div className="ml-auto w-1.5 h-1.5 rounded-full bg-primary shadow-[0_0_10px_var(--primary)]" />
                    )}
                  </div>
                </Link>
              );
            })}
          </nav>

          <div className="p-6 mt-auto">
            <div className="glass-card p-4 rounded-2xl">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-medium text-muted-foreground">System Status</span>
                <span className="flex items-center gap-1.5 text-xs font-bold text-emerald-400">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </span>
                  Operational
                </span>
              </div>
              <div className="w-full bg-secondary/20 h-1 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-full w-[98%] rounded-full" />
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 flex flex-col min-w-0">
          {/* Mobile Header */}
          <header className="lg:hidden flex items-center justify-between p-4 border-b border-border/50 bg-background/50 backdrop-blur-md sticky top-0 z-50">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
                <div className="w-3 h-3 bg-white rounded-full" />
              </div>
              <span className="font-display text-xl font-bold">PCSDBX</span>
            </div>
            <button className="p-2 text-muted-foreground hover:text-foreground">
              <LayoutDashboard className="w-6 h-6" />
            </button>
          </header>

          <div className="flex-1 p-4 md:p-8 lg:p-10 overflow-y-auto">
            <div className="max-w-7xl mx-auto w-full animate-in fade-in slide-in-from-bottom-4 duration-700">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
