"""
DevinGuard AI — Comprehensive Automated Test Suite
===================================================
Tests all 5 layers:
  1. Immutable Test Witness (tamper detection)
  2. Package Hallucination & Supply Chain Shield
  3. Lyapunov Convergence Governor (infinite loop detection)
  4. DCKG Context Pruner (AST topological ego-network)
  5. Synthetic Contract & Property Fuzz Generator
  6. Unified Engine Orchestrator
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from devinguard_engine import (
    DevinGuardEngine, ImmutableTestWitness, PackageHallucinationShield,
    LyapunovConvergenceGovernor, DCKGContextPruner, SyntheticContractGenerator
)

class TestDevinGuardEngine(unittest.TestCase):

    def setUp(self):
        self.engine = DevinGuardEngine()

    # ── 1. Immutable Test Witness Tests ─────────────────────────────────
    def test_immutable_test_witness_clean_suite(self):
        witness = ImmutableTestWitness()
        test_files = {
            "tests/test_auth.py": (
                "def test_token_expiration():\n"
                "    assert token.is_valid() is True\n"
                "    assert token.get_expiry() > 100\n"
            )
        }
        witness.register_test_suite(test_files)
        
        # Test unmodified suite
        verdict = witness.verify_patch(test_files)
        self.assertTrue(verdict.allowed)
        self.assertEqual(verdict.status, "CLEARED")

    def test_immutable_test_witness_detects_tampering(self):
        witness = ImmutableTestWitness()
        original_test = {
            "tests/test_billing.py": (
                "def test_charge_limit():\n"
                "    assert charge.amount > 0\n"
                "    assert charge.amount <= 500\n"
                "    assert charge.status == 'SUCCESS'\n"
            )
        }
        witness.register_test_suite(original_test)

        # Agent tampered with test to make flaky bug pass
        tampered_test = {
            "tests/test_billing.py": (
                "def test_charge_limit():\n"
                "    assert True  # Tampered by agent!\n"
            )
        }
        verdict = witness.verify_patch(tampered_test)
        self.assertFalse(verdict.allowed)
        self.assertEqual(verdict.status, "INTERCEPTED")
        self.assertIn("TAMPERING DETECTED", verdict.reason)
        self.assertEqual(verdict.metrics["original_assertions"], 3)
        self.assertEqual(verdict.metrics["tampered_assertions"], 1)

    # ── 2. Package Hallucination Shield Tests ─────────────────────────────
    def test_package_shield_safe_package(self):
        shield = PackageHallucinationShield()
        verdict = shield.evaluate_package_install("fastapi")
        self.assertTrue(verdict.allowed)
        self.assertEqual(verdict.status, "CLEARED")

    def test_package_shield_detects_hallucination(self):
        shield = PackageHallucinationShield()
        # Simulated hallucinated packages
        bad_pkgs = ["crypto-fast-hash-v2", "auth_bypass_lib", "temp-patch-fix"]
        for pkg in bad_pkgs:
            verdict = shield.evaluate_package_install(pkg)
            self.assertFalse(verdict.allowed)
            self.assertEqual(verdict.status, "INTERCEPTED")
            self.assertIn("HALLUCINATION RISK", verdict.reason)

    def test_package_shield_quarantines_unknown_package(self):
        shield = PackageHallucinationShield()
        verdict = shield.evaluate_package_install("some_random_unregistered_dependency_xyz")
        self.assertFalse(verdict.allowed)
        self.assertEqual(verdict.status, "INTERCEPTED")
        self.assertIn("ZERO-TRUST QUARANTINE", verdict.reason)

    # ── 3. Lyapunov Convergence Governor Tests ──────────────────────────
    def test_lyapunov_governor_converging(self):
        gov = LyapunovConvergenceGovernor()
        v1 = gov.evaluate_iteration(step=1, error_count=5, edit_distance=100, error_trace="SyntaxError line 4")
        v2 = gov.evaluate_iteration(step=2, error_count=2, edit_distance=40, error_trace="ValueError line 10")
        v3 = gov.evaluate_iteration(step=3, error_count=0, edit_distance=10, error_trace="")
        self.assertTrue(v1.allowed)
        self.assertTrue(v2.allowed)
        self.assertTrue(v3.allowed)

    def test_lyapunov_governor_detects_runaway_loop(self):
        gov = LyapunovConvergenceGovernor(max_stagnant_iterations=3)
        # Step 1: Base
        gov.evaluate_iteration(step=1, error_count=4, edit_distance=50, error_trace="Traceback...")
        # Steps 2, 3, 4: Stagnant or increasing energy (agent trapped in loop)
        gov.evaluate_iteration(step=2, error_count=4, edit_distance=60, error_trace="Traceback...")
        gov.evaluate_iteration(step=3, error_count=4, edit_distance=65, error_trace="Traceback...")
        v4 = gov.evaluate_iteration(step=4, error_count=5, edit_distance=70, error_trace="Traceback...")
        
        self.assertFalse(v4.allowed)
        self.assertEqual(v4.status, "CONVERGENCE_ABORT")
        self.assertIn("RUNAWAY LOOP INTERCEPTED", v4.reason)
        self.assertGreater(v4.metrics["estimated_dollars_saved"], 0.0)

    # ── 4. DCKG Context Pruner Tests ────────────────────────────────────
    def test_dckg_pruner_reduces_tokens(self):
        pruner = DCKGContextPruner()
        sample_repo = {
            "core/payment.py": (
                "def process_payment(amount, token):\n"
                "    validate_token(token)\n"
                "    record_audit(amount)\n"
                "    return True\n"
            ),
            "core/auth.py": (
                "def validate_token(token):\n"
                "    return len(token) > 10\n"
            ),
            "core/audit.py": (
                "def record_audit(amount):\n"
                "    pass\n"
            ),
            "unrelated/docs.py": "\n".join([f"def doc_item_{i}():\n    return 'doc {i}' * 50\n" for i in range(50)])
        }
        pruner.index_repository(sample_repo)
        ego = pruner.extract_ego_network("process_payment", k_hops=1)
        
        # Verify process_payment, validate_token, record_audit are included
        self.assertIn("process_payment", ego["included_symbols"])
        self.assertIn("validate_token", ego["included_symbols"])
        self.assertIn("record_audit", ego["included_symbols"])
        # Unrelated doc items must be excluded
        self.assertNotIn("doc_item_0", ego["included_symbols"])
        # Token reduction must be significant
        self.assertGreater(ego["token_reduction_pct"], 50.0)

    # ── 5. Synthetic Contract Generator Tests ───────────────────────────
    def test_synthetic_contract_generator(self):
        gen = SyntheticContractGenerator()
        suite = gen.generate_contract_suite("settle_invoice", ["invoice_id", "amount", "user_token"])
        self.assertIn("def test_settle_invoice_boundary_null_inputs", suite)
        self.assertIn("def test_settle_invoice_boundary_negative_numbers", suite)
        self.assertIn("def test_settle_invoice_idempotent_execution", suite)

    # ── 6. Unified Orchestrator Tests ───────────────────────────────────
    def test_orchestrator_telemetry(self):
        # Action 1: Package block
        self.engine.inspect_agent_action("install_package", {"package": "crypto-fast-hash-v2"})
        # Action 2: Context prune
        sample_files = {
            "math_ops.py": "def add(a, b):\n    return a + b\n",
            "big_docs.py": "# " + "long documentation content line\n" * 100
        }
        self.engine.pruner.index_repository(sample_files)
        self.engine.inspect_agent_action("prune_context", {"target_symbol": "add", "k_hops": 1})
        
        self.assertEqual(self.engine.telemetry["attacks_blocked"], 1)
        self.assertGreater(self.engine.telemetry["total_tokens_saved"], 0)


if __name__ == "__main__":
    unittest.main()
