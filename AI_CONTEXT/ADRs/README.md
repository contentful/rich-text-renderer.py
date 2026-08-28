# Architectural Decision Records

Decision records for `rich-text-renderer.py`. One file per decision, named
`YYYY-MM-DD-<kebab-case-title>.md`.

These live under `AI_CONTEXT/`, not `docs/`. `make docs` runs `rm -rf docs` and
replaces the directory with generated Sphinx HTML, so anything hand-authored
under `docs/` is deleted by the next docs build.

- [2026-08-25 — Escape at the render boundary, and allow-list URL schemes](./2026-08-25-escape-at-the-render-boundary.md):
  why untrusted values are neutralized in the renderers on output rather than by
  sanitizing documents on input, and what that means for custom renderers.
