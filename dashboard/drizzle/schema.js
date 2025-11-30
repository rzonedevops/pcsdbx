import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, json } from "drizzle-orm/mysql-core";
/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
    /**
     * Surrogate primary key. Auto-incremented numeric value managed by the database.
     * Use this for relations between tables.
     */
    id: int("id").autoincrement().primaryKey(),
    /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
    openId: varchar("openId", { length: 64 }).notNull().unique(),
    name: text("name"),
    email: varchar("email", { length: 320 }),
    loginMethod: varchar("loginMethod", { length: 64 }),
    role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
    createdAt: timestamp("createdAt").defaultNow().notNull(),
    updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
    lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});
/**
 * Categories table for organizing suppliers
 */
export const categories = mysqlTable("categories", {
    id: int("id").autoincrement().primaryKey(),
    name: varchar("name", { length: 255 }).notNull().unique(),
    type: varchar("type", { length: 100 }).notNull(), // e.g., "Raw Materials", "Packaging", etc.
    createdAt: timestamp("createdAt").defaultNow().notNull(),
    updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});
/**
 * Listings table for supplier information
 */
export const listings = mysqlTable("listings", {
    id: int("id").autoincrement().primaryKey(),
    listingId: varchar("listingId", { length: 255 }).notNull().unique(), // e.g., "pilot_chemical"
    name: varchar("name", { length: 255 }).notNull(),
    categoryId: int("categoryId").notNull(),
    subcategory: varchar("subcategory", { length: 255 }),
    description: text("description"),
    website: varchar("website", { length: 500 }),
    address: text("address"),
    specializations: json("specializations").$type(), // Array of specialization strings
    tags: json("tags").$type(), // Array of tag strings
    notes: text("notes"),
    createdAt: timestamp("createdAt").defaultNow().notNull(),
    updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});
