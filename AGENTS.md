# AGENTS.md

Guidance for coding agents working in `contentful/rich-text-renderer.py`.
Read `ARCHITECTURE.md` before changing rendering behaviour, and `CONTRIBUTING.md`
for the human PR workflow.

## What this repo is

A zero-runtime-dependency Python library that serializes a Contentful Rich Text
document (`dict`) to HTML, with every renderer overridable. Published to PyPI as
`rich_text_renderer`. Default branch is `master`, not `main`. Owned by
`@contentful/team-developer-experience`; service tier 4 per `catalog-info.yaml`.

## Commands

All of these exist in this repo — do not substitute ecosystem defaults.

| Task | Command | Source |
| --- | --- | --- |
| Run the tests | `python runtests.py` | `runtests.py`, and what CircleCI runs |
| Run tests across interpreters | `make test-all` (delegates to `tox`) | `Makefile`, `tox.ini` |
| Lint | `make lint` (`flake8 rich_text_renderer`) | `Makefile` |
| Format | `make format` (`black rich_text_renderer tests`) | `Makefile` |
| Coverage | `make coverage` (runs `format` and `lint` first) | `Makefile` |
| Install dev deps | `pip install -r requirements.txt` | `.circleci/config.yml` |
| Build distributions | `make dist` | `Makefile` |

`make test` shells out to the deprecated `python setup.py test`. Prefer
`python runtests.py`, which is the command CI actually uses.

## Do not run

- **`make release`** — runs `python setup.py publish`, which uploads to PyPI,
  creates a git tag, and pushes. Releases are a deliberate human action.
- **`make docs`** — it runs `rm -rf docs` and replaces `docs/` with generated
  Sphinx HTML. There is no `_docs/` directory in the repository, so the target
  cannot succeed as written anyway. Nothing hand-authored belongs under `docs/`;
  decision records live in `AI_CONTEXT/ADRs/`.
- **`make git-docs`** — runs `docs`, then `git commit --amend -C HEAD`.

## Layout

- `rich_text_renderer/` — the package. One module per renderer family; see the
  table in `ARCHITECTURE.md`.
- `tests/` — one `unittest` module per source module.
- `.circleci/config.yml` — the only CI that tests Python. Matrix: 3.7, 3.8, 3.9.
- `.github/workflows/codeql.yml` — CodeQL scan of the Actions workflows only.
- `CHANGELOG.md` — hand-maintained, newest version at the top.

## Conventions

- Code style is `black`, with flake8 at `max_line_length = 100` (`tox.ini`).
- Every module starts with `from __future__ import unicode_literals`. The
  package still carries Python 2 idioms (`class X(object)`,
  `super(Cls, self).__init__`) and `setup.py` still lists 2.7 classifiers, even
  though CI only tests 3.7+. Match the surrounding style rather than modernising
  it as a drive-by.
- Adding support for a new Contentful node type means: a renderer class in the
  right module (usually a `BaseBlockRenderer` subclass overriding
  `_render_tag`), a key in `DEFAULT_MAPPINGS` in
  `rich_text_renderer/rich_text_renderer.py`, a test, and a `CHANGELOG.md` entry.
- New test modules must be star-imported in `tests/__init__.py` or
  `runtests.py` will not discover them. `tests/null_renderer_test.py` is
  currently missing from that list, so its cases do not run under
  `python runtests.py`.

## Security-sensitive code

Escaping happens in the renderers, not on the way in. Before touching
`TextRenderer.render`, `_safe_url` / `_ALLOWED_SCHEMES` in
`rich_text_renderer/block_renderers.py`, or
`AssetHyperlinkRenderer._render`, read
`AI_CONTEXT/ADRs/2026-08-25-escape-at-the-render-boundary.md`. The regression tests
for these paths are tagged with their `AIS-` ticket numbers in
`tests/block_renderers_test.py` and `tests/text_renderers_test.py`; keep those
tests and their comments intact.

Do not add a runtime dependency. `install_requires` is empty by design, and
`AssetHyperlinkRenderer` duck-types the SDK's `Asset` class by name
(`asset.__class__.__name__ == "Asset"`) specifically to avoid importing
`contentful`.

## Versioning

`__version__` lives in `rich_text_renderer/__init__.py` and is read out of that
file by regex in `setup.py`. Bumping a version means editing that string and
adding a `CHANGELOG.md` section. There is no semantic-release automation here.
