import { z } from "zod";
import { publicProcedure, router } from "../_core/trpc";
import { getDb } from "../db";
import { categories, listings } from "../../drizzle/schema";
import { count, eq, sql } from "drizzle-orm";

export const dashboardRouter = router({
  /**
   * Get dashboard overview data
   */
  getOverview: publicProcedure.query(async () => {
    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    // Get total listings count
    const [listingsCount] = await db.select({ count: count() }).from(listings);
    
    // Get total categories count
    const [categoriesCount] = await db.select({ count: count() }).from(categories);
    
    // Get category distribution
    const categoryDistribution = await db
      .select({
        type: categories.type,
        count: count(),
      })
      .from(listings)
      .leftJoin(categories, eq(listings.categoryId, categories.id))
      .groupBy(categories.type);
    
    // Calculate velocity (days ahead of schedule)
    // Month 3 target: 300 listings
    const velocity = Math.floor((listingsCount.count - 300) / 300 * 90);
    
    return {
      total_listings: listingsCount.count,
      total_categories: categoriesCount.count,
      velocity: velocity > 0 ? `${velocity}+` : "0",
      chart_data: categoryDistribution.map((item: any, index: number) => ({
        name: item.type || "Unknown",
        value: item.count,
        color: `var(--chart-${(index % 5) + 1})`,
      })),
      last_updated: new Date().toISOString(),
    };
  }),

  /**
   * Get all listings with optional filtering
   */
  getListings: publicProcedure
    .input(
      z.object({
        search: z.string().optional(),
        category: z.string().optional(),
        limit: z.number().min(1).max(1000).default(100),
        offset: z.number().min(0).default(0),
      }).optional()
    )
    .query(async ({ input }: any) => {
      const { search, category, limit = 100, offset = 0 } = input || {};
      
      const db = await getDb();
      if (!db) throw new Error("Database not available");

      let baseQuery = db
        .select({
          id: listings.listingId,
          name: listings.name,
          category: categories.name,
          categoryType: categories.type,
          subcategory: listings.subcategory,
          description: listings.description,
          website: listings.website,
          address: listings.address,
          specializations: listings.specializations,
          tags: listings.tags,
          notes: listings.notes,
        })
        .from(listings)
        .leftJoin(categories, eq(listings.categoryId, categories.id));

      // Apply filters if provided
      if (search) {
        baseQuery = baseQuery.where(
          sql`${listings.name} LIKE ${`%${search}%`} OR ${listings.description} LIKE ${`%${search}%`}`
        ) as any;
      }

      if (category) {
        baseQuery = baseQuery.where(eq(categories.type, category)) as any;
      }

      const results = await baseQuery.limit(limit).offset(offset);

      return results;
    }),

  /**
   * Get categories with listing counts
   */
  getCategories: publicProcedure.query(async () => {
    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    const result = await db
      .select({
        id: categories.id,
        name: categories.name,
        type: categories.type,
        count: count(listings.id),
      })
      .from(categories)
      .leftJoin(listings, eq(categories.id, listings.categoryId))
      .groupBy(categories.id, categories.name, categories.type);

    return result;
  }),

  /**
   * Get network data for ecosystem visualization
   */
  getNetworkData: publicProcedure.query(async () => {
    const db = await getDb();
    if (!db) throw new Error("Database not available");
    
    const allListings = await db
      .select({
        id: listings.listingId,
        name: listings.name,
        category: categories.name,
        categoryType: categories.type,
        subcategory: listings.subcategory,
      })
      .from(listings)
      .leftJoin(categories, eq(listings.categoryId, categories.id));

    // Build nodes and links
    const nodes: any[] = [];
    const links: any[] = [];
    const nodeIds = new Set<string>();

    // Add category type nodes
    const categoryTypes = new Set(allListings.map((l: any) => l.categoryType).filter(Boolean));
    categoryTypes.forEach((type) => {
      const nodeId = `type_${type}`;
      if (!nodeIds.has(nodeId)) {
        nodes.push({
          id: nodeId,
          name: type,
          type: "category_type",
          val: 15,
        });
        nodeIds.add(nodeId);
      }
    });

    // Add category nodes and links to types
    const categoryNames = new Set(allListings.map((l: any) => l.category).filter(Boolean));
    categoryNames.forEach((catName) => {
      const listing = allListings.find((l: any) => l.category === catName);
      if (!listing) return;

      const nodeId = `cat_${catName}`;
      if (!nodeIds.has(nodeId)) {
        nodes.push({
          id: nodeId,
          name: catName,
          type: "category",
          val: 10,
        });
        nodeIds.add(nodeId);

        // Link to category type
        if (listing.categoryType) {
          links.push({
            source: `type_${listing.categoryType}`,
            target: nodeId,
          });
        }
      }
    });

    // Add supplier nodes and links to categories
    allListings.forEach((listing: any) => {
      const nodeId = `supplier_${listing.id}`;
      if (!nodeIds.has(nodeId)) {
        nodes.push({
          id: nodeId,
          name: listing.name,
          type: "supplier",
          val: 5,
        });
        nodeIds.add(nodeId);

        // Link to category
        if (listing.category) {
          links.push({
            source: `cat_${listing.category}`,
            target: nodeId,
          });
        }
      }
    });

    return { nodes, links };
  }),
});
