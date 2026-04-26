import { describe, it, expect } from "vitest";
import { TRPCError } from "@trpc/server";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";
import type { User } from "../drizzle/schema";

type AuthenticatedUser = NonNullable<TrpcContext["user"]>;

function makeCtx(user: AuthenticatedUser | null): TrpcContext {
  return {
    user,
    req: { protocol: "https", headers: {} } as TrpcContext["req"],
    res: {} as TrpcContext["res"],
  };
}

function makeUser(role: "user" | "admin" = "user"): AuthenticatedUser {
  return {
    id: 1,
    openId: "test-open-id",
    email: "test@example.com",
    name: "Test User",
    loginMethod: "manus",
    role,
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };
}

describe("auth.me", () => {
  it("returns null when unauthenticated", async () => {
    const caller = appRouter.createCaller(makeCtx(null));
    const result = await caller.auth.me();
    expect(result).toBeNull();
  });

  it("returns the user when authenticated", async () => {
    const user = makeUser();
    const caller = appRouter.createCaller(makeCtx(user));
    const result = await caller.auth.me();
    expect(result).not.toBeNull();
    expect(result?.email).toBe("test@example.com");
    expect(result?.role).toBe("user");
  });

  it("returns admin user when authenticated as admin", async () => {
    const admin = makeUser("admin");
    const caller = appRouter.createCaller(makeCtx(admin));
    const result = await caller.auth.me();
    expect(result?.role).toBe("admin");
  });
});

describe("system.health", () => {
  it("returns ok=true for valid timestamp", async () => {
    const caller = appRouter.createCaller(makeCtx(null));
    const result = await caller.system.health({ timestamp: Date.now() });
    expect(result).toEqual({ ok: true });
  });

  it("returns ok=true for zero timestamp", async () => {
    const caller = appRouter.createCaller(makeCtx(null));
    const result = await caller.system.health({ timestamp: 0 });
    expect(result).toEqual({ ok: true });
  });

  it("throws validation error for negative timestamp", async () => {
    const caller = appRouter.createCaller(makeCtx(null));
    await expect(
      caller.system.health({ timestamp: -1 })
    ).rejects.toThrow();
  });
});

describe("system.notifyOwner (admin procedure)", () => {
  it("throws FORBIDDEN when called without authentication", async () => {
    const caller = appRouter.createCaller(makeCtx(null));
    await expect(
      caller.system.notifyOwner({ title: "Test", content: "Test content" })
    ).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("throws FORBIDDEN when called by a regular user", async () => {
    const caller = appRouter.createCaller(makeCtx(makeUser("user")));
    await expect(
      caller.system.notifyOwner({ title: "Test", content: "Test content" })
    ).rejects.toMatchObject({ code: "FORBIDDEN" });
  });
});
