import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { useEffect, useState } from "react";

interface DashboardData {
  stats: {
    total_listings: number;
    total_categories: number;
    velocity_score: number;
  };
  category_counts: Record<string, number>;
  velocity_history: Array<{ date: string; listings: number }>;
}

export default function Analytics() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    fetch("/dashboard_data.json")
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => console.error("Failed to fetch analytics data", err));
  }, []);

  if (!data) return null;

  // Transform category data for charts
  const categoryData = Object.entries(data.category_counts)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);

  const topCategories = categoryData.slice(0, 10);
  
  const COLORS = [
    "var(--chart-1)",
    "var(--chart-2)",
    "var(--chart-3)",
    "var(--chart-4)",
    "var(--chart-5)",
    "#8884d8",
    "#82ca9d",
    "#ffc658",
    "#ff8042",
    "#0088fe"
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-display font-bold bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
            Platform Analytics
          </h1>
          <p className="text-muted-foreground">
            Deep dive into ecosystem growth, category distribution, and velocity metrics.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="glass-card border-border/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Listings</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold font-display">{data.stats.total_listings}</div>
              <p className="text-xs text-emerald-400 mt-1">+12% from last month</p>
            </CardContent>
          </Card>
          <Card className="glass-card border-border/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Active Categories</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold font-display">{data.stats.total_categories}</div>
              <p className="text-xs text-emerald-400 mt-1">+3 new this week</p>
            </CardContent>
          </Card>
          <Card className="glass-card border-border/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Growth Velocity</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold font-display">{data.stats.velocity_score}</div>
              <p className="text-xs text-emerald-400 mt-1">Listings/day avg</p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="growth" className="space-y-4">
          <TabsList className="bg-secondary/20 border border-border/50">
            <TabsTrigger value="growth">Growth Trends</TabsTrigger>
            <TabsTrigger value="distribution">Category Distribution</TabsTrigger>
          </TabsList>

          <TabsContent value="growth" className="space-y-4">
            <Card className="glass-card border-border/50">
              <CardHeader>
                <CardTitle>Listing Growth Velocity</CardTitle>
                <CardDescription>Cumulative listings over time</CardDescription>
              </CardHeader>
              <CardContent className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data.velocity_history}>
                    <defs>
                      <linearGradient id="colorListings" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="var(--primary)" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" strokeOpacity={0.3} vertical={false} />
                    <XAxis 
                      dataKey="date" 
                      stroke="var(--muted-foreground)" 
                      fontSize={12} 
                      tickLine={false} 
                      axisLine={false} 
                    />
                    <YAxis 
                      stroke="var(--muted-foreground)" 
                      fontSize={12} 
                      tickLine={false} 
                      axisLine={false} 
                      tickFormatter={(value) => `${value}`} 
                    />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'var(--popover)', border: '1px solid var(--border)', borderRadius: '8px' }}
                      itemStyle={{ color: 'var(--popover-foreground)' }}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="listings" 
                      stroke="var(--primary)" 
                      strokeWidth={3}
                      fillOpacity={1} 
                      fill="url(#colorListings)" 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="distribution" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <Card className="glass-card border-border/50">
                <CardHeader>
                  <CardTitle>Top 10 Categories</CardTitle>
                  <CardDescription>By number of listings</CardDescription>
                </CardHeader>
                <CardContent className="h-[400px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={topCategories} layout="vertical" margin={{ left: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" strokeOpacity={0.3} horizontal={false} />
                      <XAxis type="number" stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                      <YAxis 
                        dataKey="name" 
                        type="category" 
                        stroke="var(--muted-foreground)" 
                        fontSize={12} 
                        tickLine={false} 
                        axisLine={false} 
                        width={120}
                      />
                      <Tooltip 
                        cursor={{ fill: 'var(--secondary)', opacity: 0.2 }}
                        contentStyle={{ backgroundColor: 'var(--popover)', border: '1px solid var(--border)', borderRadius: '8px' }}
                      />
                      <Bar dataKey="value" fill="var(--primary)" radius={[0, 4, 4, 0]}>
                        {topCategories.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="glass-card border-border/50">
                <CardHeader>
                  <CardTitle>Category Share</CardTitle>
                  <CardDescription>Distribution of ecosystem listings</CardDescription>
                </CardHeader>
                <CardContent className="h-[400px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={topCategories}
                        cx="50%"
                        cy="50%"
                        innerRadius={80}
                        outerRadius={120}
                        paddingAngle={2}
                        dataKey="value"
                      >
                        {topCategories.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="var(--background)" strokeWidth={2} />
                        ))}
                      </Pie>
                      <Tooltip 
                        contentStyle={{ backgroundColor: 'var(--popover)', border: '1px solid var(--border)', borderRadius: '8px' }}
                        itemStyle={{ color: 'var(--popover-foreground)' }}
                      />
                      <Legend verticalAlign="bottom" height={36} iconType="circle" />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
