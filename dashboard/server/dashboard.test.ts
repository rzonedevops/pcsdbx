import { describe, it, expect } from "vitest";
import { appRouter } from "../server/routers";
import { getDb } from "../server/db";

describe("Dashboard API", () => {
  it("should fetch overview data from database", async () => {
    const db = await getDb();
    expect(db).toBeDefined();

    const caller = appRouter.createCaller({
      req: {} as any,
      res: {} as any,
      user: null,
    });

    const overview = await caller.dashboard.getOverview();

    expect(overview).toBeDefined();
    expect(overview.total_listings).toBeGreaterThan(0);
    expect(overview.total_categories).toBeGreaterThan(0);
    expect(overview.chart_data).toBeInstanceOf(Array);
    expect(overview.chart_data.length).toBeGreaterThan(0);
  });

  it("should fetch listings from database", async () => {
    const caller = appRouter.createCaller({
      req: {} as any,
      res: {} as any,
      user: null,
    });

    const listings = await caller.dashboard.getListings({ limit: 10 });

    expect(listings).toBeInstanceOf(Array);
    expect(listings.length).toBeGreaterThan(0);
    expect(listings.length).toBeLessThanOrEqual(10);
    
    // Verify listing structure
    const firstListing = listings[0];
    expect(firstListing).toHaveProperty("id");
    expect(firstListing).toHaveProperty("name");
    expect(firstListing).toHaveProperty("category");
  });

  it("should filter listings by search term", async () => {
    const caller = appRouter.createCaller({
      req: {} as any,
      res: {} as any,
      user: null,
    });

    const listings = await caller.dashboard.getListings({ 
      search: "basf",
      limit: 100 
    });

    expect(listings).toBeInstanceOf(Array);
    // Should find at least one BASF listing
    expect(listings.length).toBeGreaterThan(0);
  });

  it("should fetch categories with counts", async () => {
    const caller = appRouter.createCaller({
      req: {} as any,
      res: {} as any,
      user: null,
    });

    const categories = await caller.dashboard.getCategories();

    expect(categories).toBeInstanceOf(Array);
    expect(categories.length).toBeGreaterThan(0);
    
    // Verify category structure
    const firstCategory = categories[0];
    expect(firstCategory).toHaveProperty("id");
    expect(firstCategory).toHaveProperty("name");
    expect(firstCategory).toHaveProperty("type");
    expect(firstCategory).toHaveProperty("count");
  });

  it("should fetch network data for visualization", async () => {
    const caller = appRouter.createCaller({
      req: {} as any,
      res: {} as any,
      user: null,
    });

    const networkData = await caller.dashboard.getNetworkData();

    expect(networkData).toBeDefined();
    expect(networkData.nodes).toBeInstanceOf(Array);
    expect(networkData.links).toBeInstanceOf(Array);
    expect(networkData.nodes.length).toBeGreaterThan(0);
    
    // Verify node structure
    const firstNode = networkData.nodes[0];
    expect(firstNode).toHaveProperty("id");
    expect(firstNode).toHaveProperty("name");
    expect(firstNode).toHaveProperty("type");
  });
});
