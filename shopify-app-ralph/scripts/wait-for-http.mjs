#!/usr/bin/env node

const args = process.argv.slice(2);

function valueFor(flag) {
  const index = args.indexOf(flag);
  return index === -1 ? undefined : args[index + 1];
}

function fail(message) {
  console.error(message);
  process.exit(1);
}

const rawUrl = valueFor("--url");
if (!rawUrl) {
  fail("Usage: wait-for-http.mjs --url <localhost-url> [--timeout-seconds 300] [--interval-ms 1000]");
}

let target;
try {
  target = new URL(rawUrl);
} catch {
  fail("--url must be an absolute HTTP(S) URL.");
}

if (!["http:", "https:"].includes(target.protocol)) {
  fail("--url must use http or https.");
}

const localHosts = new Set(["localhost", "127.0.0.1", "::1", "[::1]"]);
if (!localHosts.has(target.hostname)) {
  fail("Refusing to poll a non-local URL. Pass the localhost app URL emitted by shopify app dev.");
}

const timeoutSeconds = Number(valueFor("--timeout-seconds") ?? "300");
const intervalMs = Number(valueFor("--interval-ms") ?? "1000");

if (!Number.isFinite(timeoutSeconds) || timeoutSeconds <= 0) {
  fail("--timeout-seconds must be a positive number.");
}
if (!Number.isFinite(intervalMs) || intervalMs < 100) {
  fail("--interval-ms must be a number of at least 100.");
}

const deadline = Date.now() + timeoutSeconds * 1000;
const safeUrl = `${target.protocol}//${target.host}${target.pathname}`;
let attempts = 0;
let lastFailure = "no response";

while (Date.now() < deadline) {
  attempts += 1;
  const controller = new AbortController();
  const requestTimeout = setTimeout(() => controller.abort(), 5000);

  try {
    const response = await fetch(target, {
      method: "GET",
      redirect: "manual",
      signal: controller.signal,
    });

    if (response.status < 500) {
      clearTimeout(requestTimeout);
      console.log(`Ready: ${safeUrl} returned HTTP ${response.status} after ${attempts} attempt(s).`);
      process.exit(0);
    }

    lastFailure = `HTTP ${response.status}`;
  } catch (error) {
    lastFailure = error instanceof Error ? error.message : String(error);
  } finally {
    clearTimeout(requestTimeout);
  }

  await new Promise((resolve) => setTimeout(resolve, intervalMs));
}

fail(`Timed out after ${timeoutSeconds}s waiting for ${safeUrl}; last result: ${lastFailure}.`);
