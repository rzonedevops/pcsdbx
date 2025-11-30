import DashboardLayout from "@/components/DashboardLayout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Switch } from "@/components/ui/switch";
import { useTheme } from "@/contexts/ThemeContext";
import { Bell, Globe, Moon, Palette, Shield, Sun } from "lucide-react";

export default function Settings() {
  const { theme, setTheme } = useTheme();

  return (
    <DashboardLayout>
      <div className="space-y-8 max-w-4xl mx-auto">
        <div>
          <h1 className="text-4xl font-display font-bold bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
            Settings
          </h1>
          <p className="text-muted-foreground">
            Manage your dashboard preferences and appearance.
          </p>
        </div>

        <div className="grid gap-6">
          {/* Appearance Section */}
          <Card className="glass-card border-border/50">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Palette className="w-5 h-5 text-primary" />
                <CardTitle>Appearance</CardTitle>
              </div>
              <CardDescription>Customize how the dashboard looks on your device.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <Label className="text-base">Theme Preference</Label>
                <RadioGroup 
                  defaultValue={theme} 
                  onValueChange={(val) => setTheme(val as "light" | "dark" | "system")}
                  className="grid grid-cols-3 gap-4"
                >
                  <div>
                    <RadioGroupItem value="light" id="light" className="peer sr-only" />
                    <Label
                      htmlFor="light"
                      className="flex flex-col items-center justify-between rounded-xl border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary cursor-pointer transition-all"
                    >
                      <Sun className="mb-3 h-6 w-6" />
                      Light
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem value="dark" id="dark" className="peer sr-only" />
                    <Label
                      htmlFor="dark"
                      className="flex flex-col items-center justify-between rounded-xl border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary cursor-pointer transition-all"
                    >
                      <Moon className="mb-3 h-6 w-6" />
                      Dark
                    </Label>
                  </div>
                  <div>
                    <RadioGroupItem value="system" id="system" className="peer sr-only" />
                    <Label
                      htmlFor="system"
                      className="flex flex-col items-center justify-between rounded-xl border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary cursor-pointer transition-all"
                    >
                      <Globe className="mb-3 h-6 w-6" />
                      System
                    </Label>
                  </div>
                </RadioGroup>
              </div>
            </CardContent>
          </Card>

          {/* Notifications Section */}
          <Card className="glass-card border-border/50">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Bell className="w-5 h-5 text-primary" />
                <CardTitle>Notifications</CardTitle>
              </div>
              <CardDescription>Configure how you receive alerts and updates.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between space-x-2">
                <Label htmlFor="new-listings" className="flex flex-col space-y-1">
                  <span>New Listings</span>
                  <span className="font-normal text-xs text-muted-foreground">Receive alerts when new suppliers are added.</span>
                </Label>
                <Switch id="new-listings" defaultChecked />
              </div>
              <div className="flex items-center justify-between space-x-2">
                <Label htmlFor="milestones" className="flex flex-col space-y-1">
                  <span>Milestone Achievements</span>
                  <span className="font-normal text-xs text-muted-foreground">Get notified when project goals are met.</span>
                </Label>
                <Switch id="milestones" defaultChecked />
              </div>
              <div className="flex items-center justify-between space-x-2">
                <Label htmlFor="system-updates" className="flex flex-col space-y-1">
                  <span>System Updates</span>
                  <span className="font-normal text-xs text-muted-foreground">Notifications about dashboard maintenance.</span>
                </Label>
                <Switch id="system-updates" />
              </div>
            </CardContent>
          </Card>

          {/* Data Privacy Section */}
          <Card className="glass-card border-border/50">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-primary" />
                <CardTitle>Data & Privacy</CardTitle>
              </div>
              <CardDescription>Manage your data preferences.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between space-x-2">
                <Label htmlFor="analytics" className="flex flex-col space-y-1">
                  <span>Usage Analytics</span>
                  <span className="font-normal text-xs text-muted-foreground">Allow anonymous usage data collection to improve the platform.</span>
                </Label>
                <Switch id="analytics" defaultChecked />
              </div>
              <div className="pt-4">
                <Button variant="destructive" className="w-full sm:w-auto">Clear Local Cache</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
