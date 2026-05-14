# Children's Privacy (COPPA + FERPA + EU AI Act Kids) MCP

[![PyPI](https://img.shields.io/pypi/v/coppa-ferpa-mcp)](https://pypi.org/project/coppa-ferpa-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-governance--mcp-purple)](https://meok.ai)

Children's privacy compliance: COPPA (US), FERPA (US edu), EU AI Act children's provisions, UK Age Appropriate Design Code.

## Install

```bash
pip install coppa-ferpa-mcp
```

## Tools

| Tool | Purpose |
|------|---------|
| `check_under_13_processing` | COPPA Section 312 verifiable parental consent requirements |
| `ferpa_audit` | FERPA education records protection check |
| `aadc_uk_check` | UK ICO Age Appropriate Design Code 15 standards |
| `eu_ai_act_minors` | EU AI Act Article 5(1)(b) exploitation of minors prohibition |
| `kids_data_flow_map` | Map data flows that touch minors with risk scoring |

## Pairs with

- `meok-attestation-api` — POST results to https://meok-attestation-api.vercel.app/sign for cryptographically signed compliance certs
- `meok-attestation-verify` — public verification of any MEOK-signed cert
- Other MEOK governance MCPs via SOV3 `mcp_bridge_call`

## Pricing

- **Free**: 10 calls/day. No API key required.
- **Pro** £79/mo: unlimited + signed attestations. [Subscribe](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836)
- **Enterprise** £1,499/mo: white-label + on-premise + SLA. hello@meok.ai

## Status

Scaffold v1.0.0 ships the MCP framework + 5 tool stubs. v1.1.0 will add real regulation data ingestion.

If your team needs this MCP fully-loaded faster, ping hello@meok.ai for sponsored development.

## License

MIT © MEOK AI Labs

<!-- mcp-name: io.github.CSOAI-ORG/coppa-ferpa-mcp -->
