---
name: dev-server-healer
description: "Start or repair a local dev server by looping: start server, wait for logs, extract errors, fix issues, restart until clean, then open the local URL. Use when asked to run a dev server, debug startup/runtime errors, or keep restarting until it runs without errors."
---

# Dev Server Healer

## Overview
Bring a dev server up cleanly using a repeatable loop: start it, wait for logs, extract actionable errors, fix them, restart, and stop only when logs are clean and the app URL is available.

## Workflow (loop until clean)
1. **Confirm context**
   - Identify repo root and the correct dev command.
   - If the repo has an AGENTS.md, read it and follow its guidance.
   - Ask for missing prerequisites (env vars, secrets, services) early.

2. **Run diagnostics first (when available)**
   - Prefer quick diagnostics to surface environment or dependency issues before starting the server.
   - Use JSON or verbose modes when parsing results.

3. **Start required services**
   - Start any docker-compose or service dependencies noted by the repo instructions.

4. **Start dev server**
   - Run the repo's dev command from the correct directory.
   - Ensure only one server instance is running.

5. **Wait for logs to appear**
   - Poll for the log file and wait until it has content.
   - If the repo does not write a log file, fall back to terminal output.

6. **Interpret and fix errors**
   - Extract the newest error blocks and stack traces.
   - Triage to the root cause; apply minimal, targeted fixes.
   - If errors reference missing env/config values, stop and ask for them.

7. **Restart and re-check**
   - Stop the server cleanly, restart, and re-check logs.
   - Repeat until no new errors appear during a stability window (30-60s).

8. **Open the app**
   - Parse the running URL from logs (prefer explicit URLs).
   - If absent, default to common dev ports (3000/3001) and confirm.
   - Open the URL in a browser (macOS: `open <url>`), requesting approval if needed.

## Repo-specific references
- If working in The Squad repo, load `references/the-squad.md` for exact commands, log locations, and services.

## Log parsing tips
- Use `rg` to pull error blocks: `rg -n "ERROR|FATAL|TypeError|ReferenceError|Cannot find module" <logfile>`
- Also scan for "App running at" or "listening on" to locate the URL/port.

## Exit criteria
- Dev server reports a running URL, and
- No new error entries appear during the stability window.
