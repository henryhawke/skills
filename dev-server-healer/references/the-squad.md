# The Squad dev server defaults

Use these defaults only when working in `/Users/henrymayo/Desktop/thesquad` or a repo that matches The Squad structure.

## Key commands
- Diagnostics (full): `yarn diagnose`
- Diagnostics (quick): `yarn diagnose:quick`
- Diagnostics (JSON): `yarn diagnose:json`
- Start dev server: `yarn dev`
- Build packages: `yarn build`
- Lint: `yarn lint`

## Services
- Start dependencies: `docker-compose -f docker-compose.dev.yml up -d`
- Check services: `yarn diagnose --services --verbose`

## Logs
- Dev server logs: `app/logs.txt`
- Docker logs: `docker-compose -f docker-compose.dev.yml logs -f`

## Working directory
- Run diagnostics and dev server from `app/` unless repo instructions specify otherwise.

## Helpful notes
- Node.js >= 22.16.0, Yarn 4.11.0, Meteor 3.3.2 required.
- Dev server is expected to print the running URL in logs (use that URL to open the browser).
