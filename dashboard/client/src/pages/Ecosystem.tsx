import DashboardLayout from "@/components/DashboardLayout";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { trpc } from "@/lib/trpc";
import { Loader2, MousePointer2, Share2, ZoomIn, Filter } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import ForceGraph2D, { ForceGraphMethods } from "react-force-graph-2d";

interface Node {
  id: string;
  group: "supplier" | "category" | "subcategory";
  label: string;
  val?: number;
}

interface Link {
  source: string;
  target: string;
  value: number;
}

interface NetworkData {
  nodes: Node[];
  links: Link[];
}

export default function Ecosystem() {
  const [data, setData] = useState<NetworkData>({ nodes: [], links: [] });
  const [filteredData, setFilteredData] = useState<NetworkData>({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);
  const fgRef = useRef<ForceGraphMethods | undefined>(undefined);

  // Fetch network data from tRPC API
  const { data: networkData, isLoading: networkLoading } = trpc.dashboard.getNetworkData.useQuery();

  useEffect(() => {
    if (networkData) {
      const dashboardData = { network: networkData };
      if (dashboardData.network) {
          // Process data to add visual properties
          const nodes = dashboardData.network.nodes.map((node: any) => ({
            ...node,
            val: node.group === "category" ? 20 : node.group === "subcategory" ? 10 : 3,
            color: node.group === "category" 
              ? "var(--primary)" 
              : node.group === "subcategory" 
                ? "var(--secondary)" 
                : "rgba(255,255,255,0.6)"
          }));
          
          const networkData = {
            nodes,
            links: dashboardData.network.links
          };
          
          setData(networkData);
          setFilteredData(networkData);
          
          // Extract categories for filter
          const cats = nodes
            .filter((n: any) => n.group === "category")
            .map((n: any) => n.label);
          setCategories(cats);
        }
        setLoading(false);
      }

    // Handle resize
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight
        });
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize(); // Initial size

    return () => window.removeEventListener("resize", handleResize);
  }, [networkData]);

  // Filter graph data when category changes
  useEffect(() => {
    if (!selectedCategory) {
      setFilteredData(data);
      return;
    }

    // Find the category node ID
    const categoryNode = data.nodes.find(n => n.group === "category" && n.label === selectedCategory);
    if (!categoryNode) return;

    // 1. Get all links connected to this category (Category -> Subcategory)
    const catLinks = data.links.filter(l => 
      (typeof l.source === 'object' ? (l.source as any).id : l.source) === categoryNode.id || 
      (typeof l.target === 'object' ? (l.target as any).id : l.target) === categoryNode.id
    );
    
    // 2. Get all subcategory IDs connected to this category
    const subcatIds = new Set<string>();
    catLinks.forEach(l => {
      const targetId = typeof l.target === 'object' ? (l.target as any).id : l.target;
      if (targetId !== categoryNode.id) subcatIds.add(targetId);
    });

    // 3. Get all links connected to these subcategories (Subcategory -> Supplier)
    const subcatLinks = data.links.filter(l => {
      const sourceId = typeof l.source === 'object' ? (l.source as any).id : l.source;
      const targetId = typeof l.target === 'object' ? (l.target as any).id : l.target;
      return subcatIds.has(sourceId) || subcatIds.has(targetId);
    });

    // 4. Collect all relevant node IDs
    const relevantNodeIds = new Set<string>([categoryNode.id]);
    subcatIds.forEach(id => relevantNodeIds.add(id));
    
    subcatLinks.forEach(l => {
      const sourceId = typeof l.source === 'object' ? (l.source as any).id : l.source;
      const targetId = typeof l.target === 'object' ? (l.target as any).id : l.target;
      relevantNodeIds.add(sourceId);
      relevantNodeIds.add(targetId);
    });

    // 5. Filter nodes and links
    const filteredNodes = data.nodes.filter(n => relevantNodeIds.has(n.id));
    const filteredLinks = [...catLinks, ...subcatLinks];

    setFilteredData({
      nodes: filteredNodes,
      links: filteredLinks
    });
    
    // Zoom to fit after a short delay to allow graph to stabilize
    setTimeout(() => {
      fgRef.current?.zoomToFit(1000, 50);
    }, 500);
    
  }, [selectedCategory, data]);

  return (
    <DashboardLayout>
      <div className="space-y-6 h-[calc(100vh-140px)] flex flex-col">
        <div className="flex flex-col md:flex-row justify-between gap-4 shrink-0">
          <div>
            <h1 className="text-4xl font-display font-bold bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
              Ecosystem Network
            </h1>
            <p className="text-muted-foreground">
              Visualizing the hypergraph connections between Suppliers, Categories, and Subcategories.
            </p>
          </div>
          <div className="flex gap-2">
            <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">
              Categories
            </Badge>
            <Badge variant="outline" className="bg-secondary/10 text-secondary-foreground border-secondary/20">
              Subcategories
            </Badge>
            <Badge variant="outline" className="bg-white/5 text-muted-foreground border-white/10">
              Suppliers
            </Badge>
          </div>
        </div>

        {/* Filter Bar */}
        <div className="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
          <Button
            variant={selectedCategory === null ? "default" : "outline"}
            onClick={() => setSelectedCategory(null)}
            size="sm"
            className="whitespace-nowrap"
          >
            All Networks
          </Button>
          {categories.map((cat) => (
            <Button
              key={cat}
              variant={selectedCategory === cat ? "default" : "outline"}
              onClick={() => setSelectedCategory(cat)}
              size="sm"
              className="whitespace-nowrap"
            >
              {cat}
            </Button>
          ))}
        </div>

        <Card className="flex-1 glass-card border-white/5 overflow-hidden relative" ref={containerRef}>
          {loading ? (
            <div className="absolute inset-0 flex items-center justify-center">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
          ) : (
            <>
              <ForceGraph2D
                ref={fgRef}
                width={dimensions.width}
                height={dimensions.height}
                graphData={filteredData}
                nodeLabel="label"
                nodeColor={(node: any) => {
                  if (node.group === "category") return "#14B8A6"; // Teal
                  if (node.group === "subcategory") return "#64748B"; // Slate
                  return "rgba(255,255,255,0.6)"; // White/Grey
                }}
                linkColor={() => "rgba(255,255,255,0.1)"}
                backgroundColor="rgba(0,0,0,0)"
                nodeRelSize={6}
                linkWidth={1}
                linkDirectionalParticles={2}
                linkDirectionalParticleWidth={2}
                d3VelocityDecay={0.3}
                cooldownTicks={100}
                onNodeClick={(node) => {
                  fgRef.current?.centerAt(node.x, node.y, 1000);
                  fgRef.current?.zoom(4, 2000);
                }}
              />
              
              {/* Controls Overlay */}
              <div className="absolute bottom-6 right-6 flex flex-col gap-2">
                <div className="bg-black/40 backdrop-blur-md p-2 rounded-lg border border-white/10 text-xs text-muted-foreground space-y-1">
                  <div className="flex items-center gap-2">
                    <MousePointer2 className="w-3 h-3" />
                    <span>Click node to focus</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <ZoomIn className="w-3 h-3" />
                    <span>Scroll to zoom</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Share2 className="w-3 h-3" />
                    <span>Drag to pan</span>
                  </div>
                </div>
              </div>
            </>
          )}
        </Card>
      </div>
    </DashboardLayout>
  );
}
