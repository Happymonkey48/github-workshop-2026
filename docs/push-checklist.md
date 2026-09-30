# GitHub Push Checklist

The published history on `origin` is being replaced. A normal push will be rejected. Use `--force-with-lease` so the push stops if the remote has commits you have not fetched.

Do this only because nobody else has cloned the repository. It rewrites every remaining branch tip.

Mission 6 is no longer part of the workshop. After the branch pushes, delete `feature/loyalty` and the `backup/loyalty-before-reset` tag from GitHub.

```bash
git push --force-with-lease origin main
git push --force-with-lease origin feature/menu
git push --force-with-lease origin feature/checkout
git push --force-with-lease origin feature/pricing
git push --force-with-lease origin feature/mobile-menu
git push --force-with-lease origin feature/matcha-promo
git push --force-with-lease origin hotfix/payment
git push --force-with-lease origin feature/receipt-debug
git push origin --delete feature/loyalty
git push origin --delete backup/loyalty-before-reset
```

Afterward, check:

```bash
git fetch origin --prune
git branch -vv
git ls-remote --heads --tags origin
```

Every local branch above should match its `origin` counterpart. `feature/loyalty` and `backup/loyalty-before-reset` should be gone.
