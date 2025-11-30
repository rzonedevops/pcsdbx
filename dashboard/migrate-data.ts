import { drizzle } from "drizzle-orm/mysql2";
import { eq } from "drizzle-orm";
import mysql from "mysql2/promise";
import { categories, listings } from "./drizzle/schema.ts";
import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Database connection
const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
  throw new Error("DATABASE_URL environment variable is required");
}

const connection = await mysql.createConnection(connectionString);

const db = drizzle(connection);

// Path to the listings directory in the pcsdbx repository
const listingsPath = path.join(__dirname, "..", "pcsdbx", "listings");

async function migrateData() {
  console.log("Starting data migration...");

  try {
    // Read all category directories
    const categoryDirs = await fs.readdir(listingsPath);

    for (const categoryDir of categoryDirs) {
      const categoryPath = path.join(listingsPath, categoryDir);
      const stats = await fs.stat(categoryPath);

      if (!stats.isDirectory()) continue;

      console.log(`\nProcessing category: ${categoryDir}`);

      // Read all subcategory directories
      const subcategoryDirs = await fs.readdir(categoryPath);

      for (const subcategoryDir of subcategoryDirs) {
        const subcategoryPath = path.join(categoryPath, subcategoryDir);
        const subcategoryStats = await fs.stat(subcategoryPath);

        if (!subcategoryStats.isDirectory()) continue;

        console.log(`  Processing subcategory: ${subcategoryDir}`);

        // Determine category type
        let categoryType = categoryDir.replace(/_/g, " ");

        // Insert or get category
        const existingCategory = await db
          .select()
          .from(categories)
          .where(eq(categories.name, subcategoryDir))
          .limit(1);

        let categoryId;
        if (existingCategory.length > 0) {
          categoryId = existingCategory[0].id;
        } else {
          const [newCategory] = await db
            .insert(categories)
            .values({
              name: subcategoryDir,
              type: categoryType,
            })
            .$returningId();
          categoryId = newCategory.id;
        }

        // Read all JSON files in the subcategory
        const files = await fs.readdir(subcategoryPath);

        for (const file of files) {
          if (!file.endsWith(".json")) continue;

          const filePath = path.join(subcategoryPath, file);
          const fileContent = await fs.readFile(filePath, "utf-8");
          
          let listingData;
          try {
            listingData = JSON.parse(fileContent);
          } catch (jsonError) {
            console.log(`    ⚠️  Skipping invalid JSON: ${file}`);
            continue;
          }

          // Extract listing ID from filename
          const listingId = file.replace(".json", "");

          console.log(`    Importing: ${listingData.name || listingId}`);

          // Check if listing already exists
          const existingListing = await db
            .select()
            .from(listings)
            .where(eq(listings.listingId, listingId))
            .limit(1);

          if (existingListing.length > 0) {
            // Update existing listing
            await db
              .update(listings)
              .set({
                name: listingData.name || listingId,
                categoryId: categoryId,
                subcategory: subcategoryDir,
                description: listingData.description || null,
                website: listingData.website || null,
                address: listingData.address || null,
                specializations: listingData.specializations || [],
                tags: listingData.tags || [],
                notes: listingData.notes || null,
                updatedAt: new Date(),
              })
              .where(eq(listings.listingId, listingId));
          } else {
            // Insert new listing
            await db.insert(listings).values({
              listingId: listingId,
              name: listingData.name || listingId,
              categoryId: categoryId,
              subcategory: subcategoryDir,
              description: listingData.description || null,
              website: listingData.website || null,
              address: listingData.address || null,
              specializations: listingData.specializations || [],
              tags: listingData.tags || [],
              notes: listingData.notes || null,
            });
          }
        }
      }
    }

    console.log("\n✅ Data migration completed successfully!");
  } catch (error) {
    console.error("❌ Migration failed:", error);
    throw error;
  } finally {
    await connection.end();
  }
}

// Run migration
migrateData().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
