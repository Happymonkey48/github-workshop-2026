# Coffee Machine

This is a small coffee-ordering app, and a Git workshop. Clone the repository and finish five missions from a terminal.

Read this file. It is the only instruction page in the repository. The mission descriptions are in [Read this for each mission](#read-this-for-each-mission).

The app is simple on purpose. The work is the Git history.

## Setup

You need Python 3.11 or newer. There is nothing to install.

On `main`, the app tests should already pass:

```bash
python -m unittest discover -s tests/app -t .
```

## Run a mission

From the repository root, pick a number from 1 to 5:

```bash
python scripts/mission.py 1
```

That command checks your repository and prints the same description that is written below. It checks the result, not the exact commands you typed. More than one way can pass, as long as the app tests still pass.

Run that check from `main`. The mission files on `main` are the ones to use. After you commit on another branch, switch back and run the check again:

```bash
git switch main
python scripts/mission.py 1
```

A new clone starts on `main`. `git fetch` downloads the other branches as `origin/<branch>`. `git branch -r` lists those remote names. It does not create a local branch. To start a mission, switch to the branch named below. Git creates the local branch from the remote one:

```bash
git switch feature/menu
```

## The missions

| Mission | Name                     | Branch                                          |
| ------- | ------------------------ | ----------------------------------------------- |
| 1       | Ship the Menu            | `feature/menu`                                  |
| 2       | Production Emergency     | `hotfix/payment`                                |
| 3       | Just Give Me That Commit | `main`                                          |
| 4       | Integration Nightmare    | `feature/mobile-menu` or `feature/matcha-promo` |
| 5       | We Need to Undo That     | `feature/receipt-debug`                         |

The five missions are separate. Finishing one does not move the others.

Mission 3 is the only one that adds a commit on `main`.

Missions 1 and 2 are not finished until you push. Commit, push, switch back to `main`, and run the mission again.

## Read this for each mission

This is the place to read what each mission asks you to do.

### Mission 1 — Ship the Menu

Work on `feature/menu`.

```bash
git switch feature/menu
```

You are shipping a seasonal drink. `feature/menu` already drafts a Mocha, but its price is still 0. Finish Mocha at 4.25 in `app/menu.json`, commit that change on `feature/menu`, and push the branch.

Git to practice: status, branch, add, commit, push.

### Mission 2 — Production Emergency

Leave `feature/checkout` as it is. Do the fix on `hotfix/payment`.

```bash
git switch hotfix/payment
```

`feature/checkout` has unfinished tax work in `app/tax.py`. Leave that file intact. Customers are getting the wrong change. On `hotfix/payment`, fix `apply_payment` in `app/checkout.py` and push the hotfix. A 4.50 order paid with 10.00 should hand back 5.50. Paying the exact total should hand back 0.

Git to practice: keep in-progress work, switch context, commit a hotfix, push.

### Mission 3 — Just Give Me That Commit

Work on `main`. Read `feature/pricing` first.

```bash
git switch main
```

`feature/pricing` has several commits. `main` only needs the fall latte price adjustment in `app/pricing.py`: latte should adjust by -0.50. Leave `app/mobile_teaser.py` and `notes/pricing-experiment.md` off `main`.

Git to practice: switch, log, show, cherry-pick.

### Mission 4 — Integration Nightmare

Work on `feature/mobile-menu` or `feature/matcha-promo`.

```bash
git switch feature/mobile-menu
```

`feature/mobile-menu` and `feature/matcha-promo` both change Matcha Latte in `app/menu.json`. Combine them so the drink stays featured and still offers 12oz and 16oz. Keep the price at 5.5. Toronto is expensive. The menu must be valid JSON, conflict markers must be gone, and the result must be committed on one of those branches.

Git to practice: merge, conflict resolution.

### Mission 5 — We Need to Undo That

Work on `feature/receipt-debug`.

```bash
git switch feature/receipt-debug
```

`feature/receipt-debug` added a debug pricing dump in `app/checkout.py` that should not ship. Remove it with a new commit. The original debug commit has to remain in the branch history.

Git to practice: log, show, revert.

## Look at the history

```bash
git log --oneline --graph --decorate --all
```

| Branch                  | What is already there            |
| ----------------------- | -------------------------------- |
| `feature/menu`          | a drafted Mocha                  |
| `feature/checkout`      | tax work that is not finished    |
| `hotfix/payment`        | a payment bug                    |
| `feature/pricing`       | several pricing commits          |
| `feature/mobile-menu`   | Matcha sizes                     |
| `feature/matcha-promo`  | featured Matcha                  |
| `feature/receipt-debug` | a debug commit                   |

## Start over

This throws away uncommitted files and commits you added, and puts the branch back to the published start.

The whole clone, back on `main`:

```bash
git fetch origin
git switch main
git reset --hard origin/main
git clean -fd
```

One branch. This example is `feature/menu`. Use the branch you want to redo:

```bash
git fetch origin
git switch feature/menu
git reset --hard origin/feature/menu
git clean -fd
```

`git reset --hard` and `git clean -fd` delete work you have not committed.

## What is in here

```text
app/                 the coffee app
tests/app/           app tests
scripts/mission.py   prints a mission and checks it
```

GitHub runs the app tests when you push. The mission checks run on your machine.
