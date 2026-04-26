import { describe, it, expect } from "vitest";
import { getSessionCookieOptions } from "./_core/cookies";
import type { Request } from "express";

function makeRequest(
  protocol: string,
  headers: Record<string, string | string[]> = {}
): Request {
  return { protocol, headers } as unknown as Request;
}

describe("getSessionCookieOptions", () => {
  it("returns secure=true when protocol is https", () => {
    const req = makeRequest("https");
    const opts = getSessionCookieOptions(req);
    expect(opts.secure).toBe(true);
    expect(opts.httpOnly).toBe(true);
    expect(opts.path).toBe("/");
    expect(opts.sameSite).toBe("none");
  });

  it("returns secure=false when protocol is http with no forwarded header", () => {
    const req = makeRequest("http");
    const opts = getSessionCookieOptions(req);
    expect(opts.secure).toBe(false);
  });

  it("returns secure=true when x-forwarded-proto is https", () => {
    const req = makeRequest("http", { "x-forwarded-proto": "https" });
    const opts = getSessionCookieOptions(req);
    expect(opts.secure).toBe(true);
  });

  it("returns secure=true when x-forwarded-proto list contains https", () => {
    const req = makeRequest("http", { "x-forwarded-proto": "http, https" });
    const opts = getSessionCookieOptions(req);
    expect(opts.secure).toBe(true);
  });

  it("returns secure=false when x-forwarded-proto is only http", () => {
    const req = makeRequest("http", { "x-forwarded-proto": "http" });
    const opts = getSessionCookieOptions(req);
    expect(opts.secure).toBe(false);
  });

  it("returns secure=true when x-forwarded-proto is an array containing https", () => {
    const req = makeRequest("http", { "x-forwarded-proto": ["http", "https"] });
    const opts = getSessionCookieOptions(req);
    expect(opts.secure).toBe(true);
  });

  it("returns secure=false when x-forwarded-proto array has no https", () => {
    const req = makeRequest("http", { "x-forwarded-proto": ["http", "ftp"] });
    const opts = getSessionCookieOptions(req);
    expect(opts.secure).toBe(false);
  });

  it("always sets httpOnly=true", () => {
    const req = makeRequest("http");
    const opts = getSessionCookieOptions(req);
    expect(opts.httpOnly).toBe(true);
  });

  it("always sets path=/", () => {
    const req = makeRequest("https");
    const opts = getSessionCookieOptions(req);
    expect(opts.path).toBe("/");
  });

  it("always sets sameSite=none", () => {
    const req = makeRequest("http");
    const opts = getSessionCookieOptions(req);
    expect(opts.sameSite).toBe("none");
  });

  it("does not include a domain field", () => {
    const req = makeRequest("https");
    const opts = getSessionCookieOptions(req);
    expect(opts.domain).toBeUndefined();
  });
});
