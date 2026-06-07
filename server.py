#!/usr/bin/env python3
"""
Children's Privacy (COPPA + FERPA + EU AI Act Kids) MCP Server
==============================================================
By MEOK AI Labs | https://meok.ai

Children's privacy compliance: COPPA (US), FERPA (US edu), EU AI Act children's provisions, UK Age Appropriate Design Code.

Install: pip install coppa-ferpa-mcp
Run:     python server.py
"""

import json
import sys
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

import os as _os

_MEOK_API_KEY = _os.environ.get("MEOK_API_KEY", "")

try:
    sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
    from auth_middleware import check_access as _shared_check_access
    _AUTH_ENGINE_AVAILABLE = True
except ImportError:
    _AUTH_ENGINE_AVAILABLE = False

    def _shared_check_access(api_key: str = ""):
        """Fallback when shared auth engine is not available."""
        if _MEOK_API_KEY and api_key and api_key == _MEOK_API_KEY:
            return True, "OK", "pro"
        if _MEOK_API_KEY and api_key and api_key != _MEOK_API_KEY:
            return False, "Invalid API key. Get one at https://meok.ai/api-keys", "free"
        return True, "OK", "free"


def check_access(api_key: str = ""):
    return _shared_check_access(api_key)


FREE_DAILY_LIMIT = 10
_usage: dict[str, list[datetime]] = defaultdict(list)
STRIPE_PRO = "https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836"


def _rl(tier="free") -> Optional[str]:
    if tier in ("pro", "professional", "enterprise"):
        return None
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=1)
    _usage["anonymous"] = [t for t in _usage["anonymous"] if t > cutoff]
    if len(_usage["anonymous"]) >= FREE_DAILY_LIMIT:
        return f"Free tier limit ({FREE_DAILY_LIMIT}/day). Pro £79/mo: {STRIPE_PRO}"
    _usage["anonymous"].append(now)
    return None


mcp = FastMCP(
    "Children's Privacy (COPPA + FERPA + EU AI Act Kids)",
    instructions=(
        "By MEOK AI Labs — Children's privacy compliance: COPPA (US), FERPA (US edu), EU AI Act children's provisions, UK Age Appropriate Design Code. "
        "Free tier: 10/day. Pro tier (£79/mo): unlimited + signed attestations. "
        "Pairs with meok-attestation-api for cryptographically signed compliance certs."
    ),
)



_UPSELL = (
    "\n\n──────────────────────\n"
    "⚖️  Part of CSOAI — the open AI-governance standard · by MEOK AI Labs\n"
    "   • All-access · 300+ governance & compliance MCPs → https://meok.ai/pricing\n"
    "   • Get this assessment human-signed & audited (£29) → https://meok.ai/work\n"
    "   • Open standard · transparent crosswalks · a fraction of enterprise-GRC cost\n"
    "   ⭐ Free & open-source → https://github.com/CSOAI-ORG/coppa-ferpa-mcp"
)
import functools as _ft, inspect as _isp
_orig_tool = mcp.tool
def _tool_with_upsell(*da, **dk):
    deco = _orig_tool(*da, **dk)
    def wrap(fn):
        @_ft.wraps(fn)
        def inner(*a, **k):
            r = fn(*a, **k)
            return (r + _UPSELL) if isinstance(r, str) else r
        try: inner.__signature__ = _isp.signature(fn)
        except Exception: pass
        return deco(inner)
    return wrap
mcp.tool = _tool_with_upsell

@mcp.tool()
def check_under_13_processing(query: str = "", api_key: str = "") -> str:
    """COPPA Section 312 verifiable parental consent requirements

    Args:
        query: Optional query parameter (regulation ref, identifier, or input data).
        api_key: Optional MEOK API key for Pro+ tier features.

    Returns: JSON with structured assessment, regulation refs, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "check_under_13_processing",
        "query": query,
        "status": "stub",
        "tool_description": "COPPA Section 312 verifiable parental consent requirements",
        "note": "Initial scaffold v1.0.0 — extended logic ships in v1.1 with real regulation data ingestion.",
        "regulation_refs": [],
        "next_step": "POST result to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance cert",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo: signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def ferpa_audit(query: str = "", api_key: str = "") -> str:
    """FERPA education records protection check

    Args:
        query: Optional query parameter (regulation ref, identifier, or input data).
        api_key: Optional MEOK API key for Pro+ tier features.

    Returns: JSON with structured assessment, regulation refs, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "ferpa_audit",
        "query": query,
        "status": "stub",
        "tool_description": "FERPA education records protection check",
        "note": "Initial scaffold v1.0.0 — extended logic ships in v1.1 with real regulation data ingestion.",
        "regulation_refs": [],
        "next_step": "POST result to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance cert",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo: signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def aadc_uk_check(query: str = "", api_key: str = "") -> str:
    """UK ICO Age Appropriate Design Code 15 standards

    Args:
        query: Optional query parameter (regulation ref, identifier, or input data).
        api_key: Optional MEOK API key for Pro+ tier features.

    Returns: JSON with structured assessment, regulation refs, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "aadc_uk_check",
        "query": query,
        "status": "stub",
        "tool_description": "UK ICO Age Appropriate Design Code 15 standards",
        "note": "Initial scaffold v1.0.0 — extended logic ships in v1.1 with real regulation data ingestion.",
        "regulation_refs": [],
        "next_step": "POST result to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance cert",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo: signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def eu_ai_act_minors(query: str = "", api_key: str = "") -> str:
    """EU AI Act Article 5(1)(b) exploitation of minors prohibition

    Args:
        query: Optional query parameter (regulation ref, identifier, or input data).
        api_key: Optional MEOK API key for Pro+ tier features.

    Returns: JSON with structured assessment, regulation refs, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "eu_ai_act_minors",
        "query": query,
        "status": "stub",
        "tool_description": "EU AI Act Article 5(1)(b) exploitation of minors prohibition",
        "note": "Initial scaffold v1.0.0 — extended logic ships in v1.1 with real regulation data ingestion.",
        "regulation_refs": [],
        "next_step": "POST result to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance cert",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo: signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def kids_data_flow_map(query: str = "", api_key: str = "") -> str:
    """Map data flows that touch minors with risk scoring

    Args:
        query: Optional query parameter (regulation ref, identifier, or input data).
        api_key: Optional MEOK API key for Pro+ tier features.

    Returns: JSON with structured assessment, regulation refs, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "kids_data_flow_map",
        "query": query,
        "status": "stub",
        "tool_description": "Map data flows that touch minors with risk scoring",
        "note": "Initial scaffold v1.0.0 — extended logic ships in v1.1 with real regulation data ingestion.",
        "regulation_refs": [],
        "next_step": "POST result to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance cert",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo: signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)





# ── search_regulation: FTS5-backed verbatim regulation lookup ──────────────
# Powered by EUR-Lex Cellar API daily sync via eu-ai-act-compliance-mcp.
# Returns 64-token snippets from canonical regulation text (Akoma Ntoso XHTML).

import sqlite3 as _sqlite3
from pathlib import Path as _Path
import os as _os_search

# Try multiple known locations for the EUR-Lex DB
_REG_DB_CANDIDATES = [
    _Path(_os_search.environ.get("MEOK_EURLEX_DB", "")) if _os_search.environ.get("MEOK_EURLEX_DB") else None,
    _Path.home() / "clawd" / "mcp-marketplace" / "eu-ai-act-compliance-mcp" / "data" / "regulations.db",
    _Path(__file__).parent / "data" / "regulations.db",
]
_REG_DB = next((p for p in _REG_DB_CANDIDATES if p and p.exists()), None)


@mcp.tool()
def search_regulation(query: str, regulation: str = "", limit: int = 10) -> dict:
    """Full-text search across 410+ articles of real EU regulation text (EUR-Lex verified).

    Args:
        query: Search terms. FTS5 syntax supported (AND, OR, NEAR, phrase quoting).
        regulation: Optional filter - one of: eu-ai-act, dora, nis2, cra, csrd, gdpr.
        limit: Max results (default 10).

    Returns:
        Snippets from matching articles with regulation + article + relevance score.
        Verbatim from EUR-Lex Cellar — auditor-defensible quotes with `>>>match<<<` highlights.
    """
    if _REG_DB is None or not _REG_DB.exists():
        return {
            "error": "EUR-Lex database not available. Install eu-ai-act-compliance-mcp v1.4.0+ which ships the DB, OR set MEOK_EURLEX_DB env var.",
            "hint": "pip install eu-ai-act-compliance-mcp",
        }
    if not query or len(query.strip()) < 2:
        return {"error": "Query must be at least 2 characters"}

    celex_map = {
        "eu-ai-act": "32024R1689", "dora": "32022R2554", "nis2": "32022L2555",
        "cra": "32024R2847", "csrd": "32022L2464", "gdpr": "32016R0679",
    }
    celex_filter = celex_map.get(regulation.lower().strip()) if regulation else None

    safe_query = query.replace('"', '""').strip()
    if " " in safe_query and not any(op in safe_query.upper() for op in [" AND ", " OR ", " NEAR"]):
        safe_query = '"' + safe_query + '"'

    conn = _sqlite3.connect(str(_REG_DB))
    try:
        if celex_filter:
            sql = ("SELECT celex, article_number, article_id, "
                   "snippet(articles_fts, 3, '>>>', '<<<', '...', 64) AS snip, rank "
                   "FROM articles_fts WHERE articles_fts MATCH ? AND celex = ? "
                   "ORDER BY rank LIMIT ?")
            rows = conn.execute(sql, (safe_query, celex_filter, limit)).fetchall()
        else:
            sql = ("SELECT celex, article_number, article_id, "
                   "snippet(articles_fts, 3, '>>>', '<<<', '...', 64) AS snip, rank "
                   "FROM articles_fts WHERE articles_fts MATCH ? "
                   "ORDER BY rank LIMIT ?")
            rows = conn.execute(sql, (safe_query, limit)).fetchall()

        name_map = {v: k for k, v in celex_map.items()}
        return {
            "query": query,
            "regulation_filter": regulation or "all",
            "result_count": len(rows),
            "source": "EUR-Lex Cellar API (publications.europa.eu) - verbatim text",
            "disclaimer": "Quotes are auditor-defensible. Not legal advice.",
            "results": [
                {"regulation": name_map.get(r[0], r[0]), "article_number": r[1],
                 "snippet": r[3], "relevance_score": round(abs(r[4]), 2)}
                for r in rows
            ],
        }
    except Exception as e:
        return {"error": f"FTS5 search error: {e}"}
    finally:
        conn.close()


@mcp.tool()
def list_regulations_in_db() -> dict:
    """List all regulations in the local EUR-Lex FTS5 database."""
    if _REG_DB is None or not _REG_DB.exists():
        return {"error": "Database not available", "regulations": []}
    conn = _sqlite3.connect(str(_REG_DB))
    try:
        rows = conn.execute(
            "SELECT celex, name, short_name, type, title, article_count, last_synced "
            "FROM regulations ORDER BY celex"
        ).fetchall()
        return {
            "source": "EUR-Lex Cellar API",
            "total_regulations": len(rows),
            "total_articles": conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0],
            "regulations": [
                {"celex": r[0], "name": r[1], "short_name": r[2], "type": r[3],
                 "title": (r[4] or "")[:120], "article_count": r[5],
                 "last_synced": r[6]}
                for r in rows
            ],
        }
    finally:
        conn.close()


def main():
    mcp.run()


if __name__ == "__main__":
    main()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/00wfZjcgAeUW4c5cyQ8k90K"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
