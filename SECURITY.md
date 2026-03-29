# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest  | ✅ |

## Reporting a Vulnerability

If you discover a security vulnerability in Renzo OS, please do **not** open a public issue.

Instead, report it privately by opening a [GitHub Security Advisory](https://github.com/renzo-os/renzo-os/security/advisories/new).

We will respond within 48 hours and issue a patch as quickly as possible.

## Security Notes

- Never commit your `.env` file — it is listed in `.gitignore`
- All API keys should be stored in environment variables only
- The Solana onchain agent is read-only by default — it does not sign or send transactions
