import DashboardLayout from "@/components/DashboardLayout";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Filter, Search, Tag, Globe, MapPin, Info, Download } from "lucide-react";
import { useEffect, useState } from "react";
import { trpc } from "@/lib/trpc";

interface Listing {
  id: string;
  name: string;
  category: string;
  subcategory: string;
  country: string;
  status: string;
  tags: string[];
  specializations: string[];
  // Add optional fields for detail view
  url?: string;
  address?: string;
  notes?: string;
}

interface DashboardData {
  listings: Listing[];
}

export default function Suppliers() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [filteredListings, setFilteredListings] = useState<Listing[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedListing, setSelectedListing] = useState<Listing | null>(null);

  const handleExport = () => {
    const dataStr = JSON.stringify(filteredListings, null, 2);
    const blob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `pcsdbx_suppliers_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Fetch listings from tRPC API
  const { data: apiListings = [], isLoading } = trpc.dashboard.getListings.useQuery({
    limit: 1000,
  });

  useEffect(() => {
    if (apiListings.length > 0) {
      const transformedListings: Listing[] = apiListings.map((item: any) => ({
        id: item.id,
        name: item.name,
        category: item.categoryType || "Unknown",
        subcategory: item.subcategory || "",
        country: "USA", // Default country since not in DB
        status: "active",
        tags: item.tags ? JSON.parse(item.tags) : [],
        specializations: item.specializations ? JSON.parse(item.specializations) : [],
        url: item.website,
        address: item.address,
        notes: item.notes,
      }));
      setListings(transformedListings);
      setFilteredListings(transformedListings);
      
      // Extract unique categories
      const uniqueCategories = Array.from(new Set(transformedListings.map(l => l.category)));
      setCategories(uniqueCategories);
    }
  }, [apiListings]);

  useEffect(() => {
    let result = listings;

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (item) =>
          item.name.toLowerCase().includes(query) ||
          item.tags.some((tag) => tag.toLowerCase().includes(query)) ||
          item.specializations.some((spec) => spec.toLowerCase().includes(query))
      );
    }

    // Filter by category
    if (selectedCategory) {
      result = result.filter((item) => item.category === selectedCategory);
    }

    setFilteredListings(result);
  }, [searchQuery, selectedCategory, listings]);

  return (
    <DashboardLayout>
      <div className="space-y-8 h-[calc(100vh-140px)] flex flex-col">
        <div className="flex flex-col md:flex-row justify-between gap-4">
          <div>
            <h1 className="text-4xl font-display font-bold bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
              Supplier Explorer
            </h1>
            <p className="text-muted-foreground">
              Browse and filter {listings.length} verified suppliers across the ecosystem.
            </p>
          </div>
          <Button onClick={handleExport} variant="outline" className="bg-secondary/20 border-border/50 hover:bg-secondary/30">
            <Download className="w-4 h-4 mr-2" />
            Export Data
          </Button>
        </div>

        {/* Search and Filter Bar */}
        <div className="flex flex-col md:flex-row gap-4 p-4 glass-card rounded-2xl">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search suppliers, ingredients, or tags..."
              className="pl-10 bg-secondary/10 border-border/50 focus:border-primary/50"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0 no-scrollbar">
            <Button
              variant={selectedCategory === null ? "default" : "outline"}
              onClick={() => setSelectedCategory(null)}
              className="whitespace-nowrap"
            >
              All
            </Button>
            {categories.map((cat) => (
              <Button
                key={cat}
                variant={selectedCategory === cat ? "default" : "outline"}
                onClick={() => setSelectedCategory(cat)}
                className="whitespace-nowrap"
              >
                {cat}
              </Button>
            ))}
          </div>
        </div>

        {/* Listings Grid */}
        <ScrollArea className="flex-1 -mx-4 px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 pb-10">
            {filteredListings.map((listing, index) => (
              <div
                key={`${listing.id}-${index}`}
                className="glass-card p-5 rounded-2xl hover:bg-secondary/20 transition-all duration-300 group border border-border/50 hover:border-primary/20 cursor-pointer"
                onClick={() => setSelectedListing(listing)}
              >
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <div className="text-xs font-bold text-primary uppercase tracking-wider mb-1">
                      {listing.subcategory || listing.category}
                    </div>
                    <h3 className="text-lg font-bold font-display group-hover:text-primary transition-colors">
                      {listing.name}
                    </h3>
                  </div>
                  <Badge variant="outline" className="bg-secondary/20 border-border/50 text-xs">
                    {listing.country}
                  </Badge>
                </div>

                <div className="space-y-3">
                  {listing.specializations.length > 0 && (
                    <div className="text-sm text-muted-foreground line-clamp-2">
                      {listing.specializations.join(", ")}
                    </div>
                  )}

                  <div className="flex flex-wrap gap-2 mt-auto pt-2">
                    {listing.tags.slice(0, 3).map((tag) => (
                      <span
                        key={tag}
                        className="inline-flex items-center px-2 py-1 rounded-md bg-secondary/20 text-secondary-foreground text-[10px] font-medium"
                      >
                        <Tag className="w-3 h-3 mr-1 opacity-50" />
                        {tag}
                      </span>
                    ))}
                    {listing.tags.length > 3 && (
                      <span className="inline-flex items-center px-2 py-1 rounded-md bg-secondary/20 text-muted-foreground text-[10px] font-medium">
                        +{listing.tags.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
            
            {filteredListings.length === 0 && (
              <div className="col-span-full flex flex-col items-center justify-center py-20 text-muted-foreground">
                <Filter className="w-12 h-12 mb-4 opacity-20" />
                <p>No suppliers found matching your criteria.</p>
                <Button 
                  variant="link" 
                  onClick={() => {setSearchQuery(""); setSelectedCategory(null);}}
                  className="mt-2"
                >
                  Clear filters
                </Button>
              </div>
            )}
          </div>
        </ScrollArea>

        <Dialog open={!!selectedListing} onOpenChange={(open) => !open && setSelectedListing(null)}>
          <DialogContent className="glass-card border-border/50 sm:max-w-[600px]">
            <DialogHeader>
              <div className="flex items-center gap-2 mb-2">
                <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">
                  {selectedListing?.subcategory || selectedListing?.category}
                </Badge>
                <Badge variant="outline" className="bg-secondary/20 border-border/50">
                  {selectedListing?.country}
                </Badge>
              </div>
              <DialogTitle className="text-2xl font-display font-bold">{selectedListing?.name}</DialogTitle>
              <DialogDescription className="text-muted-foreground">
                Listing ID: {selectedListing?.id}
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-6 py-4">
              {/* Contact Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {selectedListing?.url && (
                  <div className="flex items-center gap-3 p-3 rounded-xl bg-secondary/20">
                    <Globe className="w-5 h-5 text-primary" />
                    <div className="overflow-hidden">
                      <div className="text-xs text-muted-foreground uppercase tracking-wider">Website</div>
                      <a href={selectedListing.url} target="_blank" rel="noopener noreferrer" className="text-sm font-medium hover:text-primary truncate block">
                        {selectedListing.url}
                      </a>
                    </div>
                  </div>
                )}
                
                {selectedListing?.address && (
                  <div className="flex items-center gap-3 p-3 rounded-xl bg-secondary/20">
                    <MapPin className="w-5 h-5 text-primary" />
                    <div>
                      <div className="text-xs text-muted-foreground uppercase tracking-wider">Location</div>
                      <div className="text-sm font-medium">{selectedListing.address}</div>
                    </div>
                  </div>
                )}
              </div>

              {/* Specializations */}
              {selectedListing?.specializations && selectedListing.specializations.length > 0 && (
                <div>
                  <h4 className="text-sm font-bold mb-2 flex items-center gap-2">
                    <Info className="w-4 h-4 text-primary" /> Specializations
                  </h4>
                  <ul className="grid grid-cols-1 gap-2">
                    {selectedListing.specializations.map((spec, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 shrink-0" />
                        {spec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Notes */}
              {selectedListing?.notes && (
                <div className="bg-secondary/20 p-4 rounded-xl border border-border/50">
                  <h4 className="text-sm font-bold mb-2">Notes</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {selectedListing.notes}
                  </p>
                </div>
              )}

              {/* Tags */}
              <div className="flex flex-wrap gap-2">
                {selectedListing?.tags.map((tag) => (
                  <Badge key={tag} variant="secondary" className="bg-secondary/20 text-secondary-foreground hover:bg-secondary/30">
                    #{tag}
                  </Badge>
                ))}
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
}
