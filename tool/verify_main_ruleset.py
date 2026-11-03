#!/usr/bin/env python3
"""Fail closed when production main has no enforceable GitHub branch ruleset.

This checks GitHub ruleset configuration, not whether a bypass-capable account
has secretly pushed. GitHub enforcement is independently verified via API.
"""

from __future__ import annotations

import argparse
import json
import os
from urllib.request import Request, urlopen

REPOSITORY = "riccardopinato/World-Days"
RULESET_ID = 26445843


def verify_ruleset(data: object) -> None:
    if not isinstance(data, dict):
        raise ValueError("GitHub ruleset response is not an object")
    if data.get("name") != "World Days — Main Protection":
        raise ValueError("unexpected GitHub ruleset identity")
    if data.get("source") != REPOSITORY or data.get("target") != "branch":
        raise ValueError("ruleset does not belong to the World Days branch source")
    if data.get("enforcement") != "active":
        raise ValueError("ruleset is NOT active")
    condition = data.get("conditions")
    if not isinstance(condition, dict):
        raise ValueError("ruleset branch target missing")
    ref_names = condition.get("ref_name")
    if not isinstance(ref_names, dict):
        raise ValueError("ruleset ref conditions missing")
    includes = ref_names.get("include")
    if not isinstance(includes, list) or not any(
        x in ("refs/heads/main", "~DEFAULT_BRANCH") for x in includes
    ):
        raise ValueError("ruleset does not target main")
    excludes = ref_names.get("exclude") or []
    if "refs/heads/main" in excludes or "~DEFAULT_BRANCH" in excludes:
        raise ValueError("ruleset explicitly excludes main")

    rules = data.get("rules")
    if not isinstance(rules, list):
        raise ValueError("ruleset rules missing")
    kinds = {rule.get("type"): rule for rule in rules if isinstance(rule, dict)}
    for kind in ("pull_request", "non_fast_forward", "deletion", "required_status_checks"):
        if kind not in kinds:
            raise ValueError(f"required branch rule missing: {kind}")

    review = kinds["pull_request"].get("parameters") or {}
    if not review.get("required_review_thread_resolution", False):
        raise ValueError("review conversation resolution is not required")
    checks = kinds["required_status_checks"].get("parameters") or {}
    if not checks.get("strict_required_status_checks_policy", False):
        raise ValueError("up-to-date required checks are not enforced")
    required = checks.get("required_status_checks") or []
    if not any(
        isinstance(item, dict) and item.get("context") == "validate"
        for item in required
    ):
        raise ValueError("Development checks / validate is not required")
    if data.get("bypass_actors"):
        raise ValueError("branch ruleset contains bypass actors")


def fetch_ruleset(token: str) -> dict:
    if not token:
        raise ValueError("GITHUB_TOKEN is required to inspect branch protection")
    url = f"https://api.github.com/repos/{REPOSITORY}/rulesets/{RULESET_ID}"
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "World-Days-release-governance-gate",
        },
    )
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise ValueError(f"ruleset API returned HTTP {response.status}")
        raw = response.read(512 * 1024 + 1)
        if len(raw) > 512 * 1024:
            raise ValueError("ruleset response exceeds 512 KiB")
        return json.loads(raw.decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", help="Offline JSON fixture used only for tests")
    args = parser.parse_args()
    if args.fixture:
        raise SystemExit(
            "release gate cannot use --fixture; run isolated unit tests instead"
        )
    try:
        data = fetch_ruleset(os.environ.get("GITHUB_TOKEN", ""))
        verify_ruleset(data)
    except Exception as error:
        raise SystemExit(f"::error::Production release ruleset gate FAILED: {error}")
    print("Production release branch ruleset gate PASS: active main, PR and validate enforced")


if __name__ == "__main__":
    main()
