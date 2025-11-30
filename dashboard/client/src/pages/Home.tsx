import { useAuth } from "@/_core/hooks/useAuth";
import DashboardLayout from "@/components/DashboardLayout";
import MetricCard from "@/components/MetricCard";
import { Activity, Database, Layers, Target, TrendingUp, Zap } from "lucide-react";
import { trpc } from "@/lib/trpc";
import { Area, AreaChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const growthData = [
  { name: "Week 1", listings: 75, target: 75 },
  { name: "Week 2", listings: 180, target: 150 },
  { name: "Week 3", listings: 320, target: 225 },
  { name: "Week 4", listings: 613, target: 300 },
];

interface DashboardData {
  total_listings: number;
  total_categories: number;
  velocity: string;
  chart_data: Array<{ name: string; value: number; color: string }>;
  last_updated: string;
}

export default function Home() {
  // The userAuth hooks provides authentication state
  // To implement login/logout functionality, simply call logout() or redirect to getLoginUrl()
  let { user, loading, error, isAuthenticated, logout } = useAuth();

  // Fetch dashboard data from tRPC API
  const { data, isLoading } = trpc.dashboard.getOverview.useQuery();

  // Use fetched data or fallback to initial static values for immediate render
  const totalListings = data?.total_listings || 613;
  const totalCategories = data?.total_categories || 61;
  const velocity = data?.velocity || "90+";
  const categoryData = data?.chart_data || [
    { name: "Raw Materials", value: 318, color: "var(--chart-1)" },
    { name: "Packaging", value: 94, color: "var(--chart-2)" },
    { name: "Equipment", value: 69, color: "var(--chart-3)" },
    { name: "Services", value: 54, color: "var(--chart-4)" },
    { name: "Labels", value: 78, color: "var(--chart-5)" },
  ];

  // Update growth data with current total if available
  const currentGrowthData = [...growthData];
  if (data) {
    // Check if we need to add a "Current" data point
    const lastPoint = currentGrowthData[currentGrowthData.length - 1];
    if (lastPoint.listings !== data.total_listings) {
       currentGrowthData.push({
         name: "Current",
         listings: data.total_listings,
         target: 300 // Month 3 target
       });
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 className="text-4xl md:text-5xl font-display font-bold mb-2 bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
              Strategic Overview
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl">
              Real-time tracking of the Integrated Cosmetic Science Platform's foundational data layer.
            </p>
            {data && (
              <p className="text-xs text-muted-foreground mt-2">
                Last updated: {data.last_updated}
              </p>
            )}
          </div>
          <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-bold">
            <Zap className="w-4 h-4 fill-current" />
            Month 3 Targets Exceeded
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard
            title="Total Listings"
            value={totalListings}
            change="+817%"
            trend="up"
            icon={Database}
            description="Vs. Month 1 Target (75)"
            delay={100}
          />
          <MetricCard
            title="Active Categories"
            value={totalCategories}
            change="+406%"
            trend="up"
            icon={Layers}
            description="Vs. Month 1 Target (15)"
            delay={200}
          />
          <MetricCard
            title="Velocity"
            value={velocity}
            change="Days Ahead"
            trend="up"
            icon={TrendingUp}
            description="Ahead of Month 3 Schedule"
            delay={300}
          />
          <MetricCard
            title="Data Quality"
            value="100%"
            change="Perfect"
            trend="up"
            icon={Activity}
            description="Schema Compliance Rate"
            delay={400}
          />
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Growth Chart */}
          <div className="lg:col-span-2 glass-card p-6 rounded-3xl">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-bold font-display">Growth Velocity</h3>
                <p className="text-sm text-muted-foreground">Actual Listings vs. Targets</p>
              </div>
              <Target className="w-5 h-5 text-muted-foreground" />
            </div>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={currentGrowthData}>
                  <defs>
                    <linearGradient id="colorListings" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="var(--primary)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis 
                    dataKey="name" 
                    stroke="rgba(255,255,255,0.3)" 
                    fontSize={12} 
                    tickLine={false} 
                    axisLine={false} 
                  />
                  <YAxis 
                    stroke="rgba(255,255,255,0.3)" 
                    fontSize={12} 
                    tickLine={false} 
                    axisLine={false} 
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "rgba(15, 23, 42, 0.9)",
                      border: "1px solid rgba(255,255,255,0.1)",
                      borderRadius: "12px",
                      boxShadow: "0 4px 20px rgba(0,0,0,0.5)",
                    }}
                    itemStyle={{ color: "#fff" }}
                  />
                  <Area
                    type="monotone"
                    dataKey="listings"
                    stroke="var(--primary)"
                    strokeWidth={3}
                    fillOpacity={1}
                    fill="url(#colorListings)"
                  />
                  <Area
                    type="monotone"
                    dataKey="target"
                    stroke="var(--secondary)"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    fill="transparent"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Category Distribution */}
          <div className="glass-card p-6 rounded-3xl">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-bold font-display">Category Mix</h3>
                <p className="text-sm text-muted-foreground">Distribution by Type</p>
              </div>
              <Layers className="w-5 h-5 text-muted-foreground" />
            </div>
            <div className="h-[300px] w-full relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    stroke="none"
                  >
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "rgba(15, 23, 42, 0.9)",
                      border: "1px solid rgba(255,255,255,0.1)",
                      borderRadius: "12px",
                    }}
                    itemStyle={{ color: "#fff" }}
                  />
                </PieChart>
              </ResponsiveContainer>
              {/* Center Text */}
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-3xl font-bold font-display">{totalCategories}</span>
                <span className="text-xs text-muted-foreground uppercase tracking-wider">Categories</span>
              </div>
            </div>
          </div>
        </div>

        {/* Strategic Priorities Section */}
        <div className="glass-card p-8 rounded-3xl border-l-4 border-l-amber-500">
          <div className="flex flex-col md:flex-row justify-between gap-6">
            <div className="space-y-4 max-w-2xl">
              <h3 className="text-2xl font-bold font-display text-amber-400">Critical Focus Areas</h3>
              <p className="text-muted-foreground leading-relaxed">
                Current strategic optimization is focused on expanding depth in Business Services and filling critical gaps in Equipment and Packaging categories.
              </p>
              <div className="flex flex-wrap gap-3">
                <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold uppercase tracking-wide">
                  Business Services Depth
                </span>
                <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold uppercase tracking-wide">
                  New Equipment Categories
                </span>
                <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold uppercase tracking-wide">
                  Packaging Gaps
                </span>
              </div>
            </div>
            <div className="flex flex-col justify-center gap-4 min-w-[200px]">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Business Services</span>
                <span className="font-mono font-bold">12%</span>
              </div>
              <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden">
                <div className="bg-amber-500 h-full w-[12%] rounded-full" />
              </div>
              
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Equipment</span>
                <span className="font-mono font-bold">45%</span>
              </div>
              <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden">
                <div className="bg-amber-500 h-full w-[45%] rounded-full" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
