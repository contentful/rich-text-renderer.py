# Architectural Decision Records

Decision records for `rich-text-renderer.py`. One file per decision, named
`YYYY-MM-DD-<kebab-case-title>.md`.

Generated Sphinx HTML is written to `docs/api/`, which `make docs` owns and
empties on every build. It does not touch this directory. Nothing outside
`docs/api/` is generated, so hand-authored files under `docs/` survive a docs
build.

- [2026-08-25 — Escape at the render boundary, and allow-list URL schemes](./2026-08-25-escape-at-the-render-boundary.md):
  why untrusted values are neutralized in the renderers on output rather than by
  sanitizing documents on input, and what that means for custom renderers.
