import DashboardLayout from "@/components/DashboardLayout";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Filter, Search, Tag } from "lucide-react";
import { useEffect, useState } from "react";

interface Listing {
  id: string;
  name: string;
  category: string;
  subcategory: string;
  country: string;
  status: string;
  tags: string[];
  specializations: string[];
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

  useEffect(() => {
    fetch("/dashboard_data.json")
      .then((res) => res.json())
      .then((data: DashboardData) => {
        setListings(data.listings);
        setFilteredListings(data.listings);
        
        // Extract unique categories
        const uniqueCategories = Array.from(new Set(data.listings.map(l => l.category)));
        setCategories(uniqueCategories);
      })
      .catch((err) => console.error("Failed to fetch listings", err));
  }, []);

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
        </div>

        {/* Search and Filter Bar */}
        <div className="flex flex-col md:flex-row gap-4 p-4 glass-card rounded-2xl">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search suppliers, ingredients, or tags..."
              className="pl-10 bg-black/20 border-white/10 focus:border-primary/50"
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
            {filteredListings.map((listing) => (
              <div
                key={listing.id}
                className="glass-card p-5 rounded-2xl hover:bg-white/5 transition-all duration-300 group border border-white/5 hover:border-primary/20"
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
                  <Badge variant="outline" className="bg-white/5 border-white/10 text-xs">
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
                      <span className="inline-flex items-center px-2 py-1 rounded-md bg-white/5 text-muted-foreground text-[10px] font-medium">
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
      </div>
    </DashboardLayout>
  );
}
