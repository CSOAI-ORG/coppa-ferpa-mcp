# Children's privacy MCP — implementation status

Maintained in the Council of AI / CSOAI Ltd ecosystem. The package and repository
identifier remain `coppa-ferpa-mcp`; existing MIT copyright notices are preserved.

**This repository contains an early scaffold, not a production compliance assessor.**
Five named assessment tools currently return `status: "stub"` with empty
`regulation_refs`. Installing or calling them does not establish legal compliance,
certification, a completed audit, or suitability for processing children's data.
Measurement and verification are not certification. This is not legal advice.

<!-- mcp-name: io.github.CSOAI-ORG/coppa-ferpa-mcp -->

## What the source implements

| Tool | Current source behaviour |
| --- | --- |
| `check_under_13_processing` | Returns a scaffold response, not a parental-consent determination. |
| `ferpa_audit` | Returns a scaffold response, not an education-records audit. |
| `aadc_uk_check` | Returns a scaffold response, not an assessment against the UK design code. |
| `eu_ai_act_minors` | Returns a scaffold response, not a legal assessment. |
| `kids_data_flow_map` | Returns a scaffold response, not an observed data-flow map or validated risk score. |
| `search_regulation` | Searches a separately configured local SQLite FTS5 database; reports an error when it is unavailable. |
| `list_regulations_in_db` | Reads metadata from that same optional local database; reports its absence explicitly. |

See [server.py](server.py) for the implementation. Tool names describe intended
areas of work; they are not evidence that those assessments are implemented.
A snippet retrieved from a database is not proof of completeness, legal currency,
or applicability to a particular organisation.

## Package interface

[pyproject.toml](pyproject.toml) declares Python 3.10 or newer and the command-line
entry point `coppa-ferpa-mcp = "server:main"`. The source uses MCP over stdio.
The existing package installation interface is:

```bash
python -m pip install coppa-ferpa-mcp
```

Example client configuration:

```json
{
  "mcpServers": {
    "coppa-ferpa-mcp": {
      "command": "coppa-ferpa-mcp"
    }
  }
}
```

Review the installed package version, dependencies and local configuration first.
This documentation correction does not establish a successful current package
installation, runtime acceptance, or a new package release.

## Data, network and storage boundaries

Do not provide children's personal data, student records, production credentials
or other sensitive inputs to this scaffold.

The optional regulation database is **not bundled** by the declared wheel file
list, which includes `server.py`. `MEOK_EURLEX_DB` can identify a separately
provisioned database. This README does not promise a database, a live sync, any
article count, or that its contents are current.

The source attempts to load shared authentication code from an installation-specific
location. Its available behaviour can depend on that environment and may maintain
local usage and API-key records. No universal free quota is promised here.

`server.py` also defines an HTTP metering helper for
`https://proofof.ai/verify`: if invoked, it submits an `api_key` and a `tool` field
(the latter is empty in the inspected helper). The five scaffold tool bodies do
not invoke that helper directly. Do not infer that all deployments are offline
or network-isolated from use of stdio.

Legacy runtime responses can still contain promotional text and signing links.
Those strings are not evidence that the promised service is active, that a
signature establishes compliance, or that a displayed price is authoritative.
This documentation-only correction does not alter tool execution, authentication,
rate limiting, billing, signing or published package bytes.

## Current commercial information

Earlier README revisions contained conflicting subscription prices and unverified
promises of unlimited audits, instant signing, service levels and refunds. Those
promotional claims and direct checkout links have been removed from this README.
No replacement subscription, new price, or automated signing offer is made here.

For separately scoped measurement or evidence work, use the current service and
contact information at [Council of AI](https://councilof.ai/). Agree the exact
scope, deliverable, limitations and commercial terms before any paid work. There
is no purchase required by this README to inspect the repository's MIT-licensed code.

## Documentation checks

Run the source-only documentation checks without installing or importing the server:

```bash
python3 tests/test_readme_contract.py
```

These check the description against the source and reject reintroduced pricing or
blanket compliance claims. They do not test legal correctness, server execution,
network behaviour or independent customer use.

## Licence

[MIT](LICENSE), copyright 2026 MEOK AI Labs, as recorded in the unchanged licence.
The package identifier, licence, historical commits and tool implementation are
unchanged. Council of AI is operated by CSOAI Ltd.
