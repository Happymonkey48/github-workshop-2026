#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

BRIEFS = {
    1: """Mission 1 — Ship the Menu
You are shipping a seasonal drink. feature/menu already drafts a Mocha, but its price is still 0.
Finish Mocha at 4.25, commit that change on feature/menu, and push the branch.
Concepts: status, branch, add, commit, push.""",
    2: """Mission 2 — Production Emergency
feature/checkout has unfinished tax work. Leave that work intact.
Customers are getting the wrong change. On hotfix/payment, fix apply_payment and push the hotfix.
A 4.50 order paid with 10.00 should hand back 5.50. Paying the exact total should hand back 0.
Concepts: keep in-progress work, switch context, commit a hotfix, push.""",
    3: """Mission 3 — Just Give Me That Commit
feature/pricing has several commits. Main only needs the fall latte price adjustment: latte should adjust by -0.50.
Leave the mobile teaser and the pricing experiment notes off main.
Concepts: fetch, log, show, cherry-pick.""",
    4: """Mission 4 — Integration Nightmare
feature/mobile-menu and feature/matcha-promo both change Matcha Latte.
Combine them so the drink stays featured and still offers 12oz and 16oz.
The menu must be valid JSON, conflict markers must be gone, and the result must be committed on one of those branches.
Concepts: merge, conflict resolution.""",
    5: """Mission 5 — We Need to Undo That
feature/receipt-debug added a debug pricing dump that should not ship.
Remove it with a new commit. The original debug commit has to remain in the branch history.
Concepts: log, show, revert.""",
    6: """Mission 6 — The Commit Is Gone
feature/loyalty used to contain a reward catalog and redemption. Those commits were removed from the branch, but they are still recoverable.
Inspect the reflog and any ref that still points at the dropped tip, then restore that work onto feature/loyalty.
Concepts: reflog, recovering commits.""",
}


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or not 1 <= int(sys.argv[1]) <= 6:
        print("Usage: python scripts/mission.py <1-6>", file=sys.stderr)
        return 1

    mission = int(sys.argv[1])
    print(BRIEFS[mission])
    print("\nValidation checks the repository state. It does not require one exact command.\n")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", f"tests.missions.test_mission_0{mission}"],
        cwd=REPO_ROOT,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
