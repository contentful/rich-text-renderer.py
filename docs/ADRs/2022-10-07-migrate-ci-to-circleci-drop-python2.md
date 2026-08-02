# Migrate CI to CircleCI and Drop Python 2.7

## Status

Accepted

## Context

The project originally used Travis CI. Travis CI changed its free tier policy in 2020–2021, making it less viable for open-source projects. The team needed to migrate to a supported CI provider. Contentful's SDK team was also moving to CircleCI as a standard.

Separately, Python 2.7 reached end-of-life in January 2020. The test matrix in `tox.ini` included `py27` alongside Python 3.x versions. Continuing to test against 2.7 added maintenance overhead with no practical benefit for new users.

Sources: commit `de9304e` ("Changed CI/CD vendor", 2022-10-07), commit `2d223af` ("Check against actively maintained versions of Python", 2022-10-10), CHANGELOG v0.2.7.

## Decision

CI was migrated from Travis CI to CircleCI using a Docker-matrix strategy (`.circleci/config.yml`). The test matrix was updated to run against Python 3.7, 3.8, and 3.9 only — Python 2.7 was removed from CI.

The `from __future__ import unicode_literals` guards were kept in source files (not removed), as removing them was a cosmetic change with no practical benefit and would introduce unnecessary diff noise.

Dev dependencies (`requirements.txt`) were slimmed — ipython and other interactive tooling were removed, keeping only test/lint tooling.

## Consequences

- Python 2.7 is no longer tested or officially supported. The `setup.py` classifiers still list Python 2 but this is stale.
- CircleCI provides the test matrix; no GitHub Actions-based test workflow exists (only CodeQL for workflow file scanning).
- Developers working on this repo should use Python 3.7+ locally.
- The `tox.ini` `envlist` still references `py27`/`py34`/`py35`/`py36` but these are not run in CI — the tox config is slightly stale relative to the CircleCI matrix.
