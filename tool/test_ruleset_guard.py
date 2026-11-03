#!/usr/bin/env python3
"""Offline fail-closed tests of the World Days production ruleset gate."""

from __future__ import annotations

import copy
import unittest

from verify_main_ruleset import verify_ruleset


def valid() -> dict:
    return {
        "name": "World Days — Main Protection",
        "source": "riccardopinato/World-Days",
        "target": "branch",
        "enforcement": "active",
        "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
        "bypass_actors": [],
        "rules": [
            {"type": "pull_request", "parameters": {
                "required_approving_review_count": 0,
                "required_review_thread_resolution": True,
            }},
            {"type": "non_fast_forward"},
            {"type": "deletion"},
            {"type": "required_status_checks", "parameters": {
                "strict_required_status_checks_policy": True,
                "required_status_checks": [{"context": "validate"}],
            }},
        ],
    }


class MainProtectionGateTest(unittest.TestCase):
    def test_valid_active_main_ruleset_passes(self) -> None:
        verify_ruleset(valid())

    def test_disabled_ruleset_never_passes(self) -> None:
        data = valid()
        data["enforcement"] = "disabled"
        with self.assertRaisesRegex(ValueError, "NOT active"):
            verify_ruleset(data)

    def test_empty_target_never_passes(self) -> None:
        data = valid()
        data["conditions"]["ref_name"]["include"] = []
        with self.assertRaisesRegex(ValueError, "does not target main"):
            verify_ruleset(data)

    def test_missing_validate_never_passes(self) -> None:
        data = valid()
        data["rules"][-1]["parameters"]["required_status_checks"] = []
        with self.assertRaisesRegex(ValueError, "validate is not required"):
            verify_ruleset(data)

    def test_missing_delete_protection_never_passes(self) -> None:
        data = valid()
        data["rules"] = [r for r in data["rules"] if r["type"] != "deletion"]
        with self.assertRaisesRegex(ValueError, "deletion"):
            verify_ruleset(data)

    def test_bypass_never_passes(self) -> None:
        data = valid()
        data["bypass_actors"] = [{"actor_type": "OrganizationAdmin", "bypass_mode": "always"}]
        with self.assertRaisesRegex(ValueError, "bypass"):
            verify_ruleset(data)

    def test_weak_check_up_to_date_fails(self) -> None:
        data = valid()
        data["rules"][-1]["parameters"]["strict_required_status_checks_policy"] = False
        with self.assertRaisesRegex(ValueError, "up-to-date"):
            verify_ruleset(data)

    def test_unresolved_review_policy_fails(self) -> None:
        data = copy.deepcopy(valid())
        data["rules"][0]["parameters"]["required_review_thread_resolution"] = False
        with self.assertRaisesRegex(ValueError, "conversation"):
            verify_ruleset(data)


if __name__ == "__main__":
    unittest.main()
