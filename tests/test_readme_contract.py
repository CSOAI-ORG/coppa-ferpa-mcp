"""Offline documentation contract; never import server.py or contact a service."""
from pathlib import Path
import ast
import os
import re
import unittest

ROOT = Path(os.environ.get("CSOAI_REVIEW_ROOT", Path(__file__).resolve().parents[1]))
README = (ROOT / "README.md").read_text(encoding="utf-8")
SOURCE = (ROOT / "server.py").read_text(encoding="utf-8")
PROJECT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)
SCAFFOLDS = {
    "check_under_13_processing", "ferpa_audit", "aadc_uk_check",
    "eu_ai_act_minors", "kids_data_flow_map",
}

def is_tool(node):
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
        isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute)
        and d.func.attr == "tool" and isinstance(d.func.value, ast.Name)
        and d.func.value.id == "mcp" for d in node.decorator_list
    )

class ReadmeContract(unittest.TestCase):
    def test_scaffold_notice_is_prominent(self):
        self.assertIn("early scaffold", README[:800])
        self.assertIn('status: "stub"', README[:1000])

    def test_each_documented_scaffold_matches_source(self):
        found = set()
        for fn in (n for n in TREE.body if is_tool(n)):
            for node in ast.walk(fn):
                if not isinstance(node, ast.Dict):
                    continue
                pairs = {k.value: v for k, v in zip(node.keys, node.values)
                         if isinstance(k, ast.Constant) and isinstance(k.value, str)}
                status = pairs.get("status")
                if isinstance(status, ast.Constant) and status.value == "stub":
                    found.add(fn.name)
                    self.assertIn(f"`{fn.name}`", README)
                    refs = pairs.get("regulation_refs")
                    self.assertIsInstance(refs, ast.List)
                    self.assertEqual(refs.elts, [])
        self.assertEqual(found, SCAFFOLDS, "Source changed: requalify the status table")

    def test_every_registered_tool_is_documented(self):
        for fn in (n for n in TREE.body if is_tool(n)):
            with self.subTest(tool=fn.name):
                self.assertIn(f"`{fn.name}`", README)

    def test_no_typed_prices(self):
        self.assertNotRegex(README, r"[£$€]\s*\d|\b(?:GBP|USD|EUR)\s*\d")

    def test_no_checkout_links(self):
        self.assertNotIn("buy.stripe.com", README)
        self.assertNotIn("cal.com/csoai/august-audit", README)

    def test_no_blanket_claims(self):
        for text in ["EU%20AI%20Act-Compliant", "compliance** built-in",
                     "- Production-ready", "instant HMAC signing key", "VAT-clean"]:
            with self.subTest(text=text):
                self.assertNotIn(text, README)

    def test_limitations_are_explicit(self):
        self.assertIn("not legal advice", README)
        self.assertIn("does not establish legal compliance", README)
        self.assertIn("not certification", README)

    def test_actual_readme_source_and_command_preserved(self):
        self.assertIn('readme = "README.md"', PROJECT)
        self.assertIn('coppa-ferpa-mcp = "server:main"', PROJECT)
        self.assertIn('"command": "coppa-ferpa-mcp"', README)

    def test_database_dependency_is_disclosed(self):
        self.assertIn("MEOK_EURLEX_DB", README)
        self.assertIn("not bundled", README)
        self.assertIn('only-include = ["server.py"]', PROJECT)

    def test_metering_and_local_auth_disclosed(self):
        for text in ["https://proofof.ai/verify", "`api_key`", "`tool`",
                     "installation-specific", "local usage"]:
            with self.subTest(text=text):
                self.assertIn(text, README)

    def test_identifier_and_licence_preserved(self):
        self.assertIn("mcp-name: io.github.CSOAI-ORG/coppa-ferpa-mcp", README)
        self.assertIn("[MIT](LICENSE)", README)
        self.assertIn("MEOK AI Labs", README)

    def test_service_and_runtime_boundary_disclosed(self):
        self.assertIn("https://councilof.ai/", README)
        self.assertIn("Legacy runtime responses", README)
        self.assertIn("No replacement subscription", README)
        self.assertIn("does not alter tool execution", README)

if __name__ == "__main__":
    unittest.main(verbosity=2)
