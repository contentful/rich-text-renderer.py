# Escape at the render boundary, and allow-list URL schemes

- **Date:** 2026-08-25
- **Status:** Accepted
- **Evidence:** commit `2b0518b` — *"fix: HTML-encode rendered content and block
  dangerous URI schemes [AIS-256–259] (#39)"*, 2026-07-21 —
  `rich_text_renderer/block_renderers.py`,
  `rich_text_renderer/text_renderers.py`

> This record was written on 2026-08-25 from the commit history and the code as
> it stands. It documents a decision that was already made and shipped in
> `2b0518b`; it is a reconstruction, not a contemporaneous record. The rationale
> below is taken from that commit's message and from the inline comments the
> commit added — nothing here is inferred beyond those sources.

## Context

Rich Text documents are author-supplied content. A Contentful `text` node's
`value` and a `hyperlink` node's `data.uri` both arrive as arbitrary strings, and
this library's whole job is to interpolate them into markup. Before `2b0518b`
that interpolation was literal: `TextRenderer.render` returned `node["value"]`
unchanged, and `HyperlinkRenderer.render` formatted `node["data"]["uri"]`
straight into an `href`. A document containing `<script>alert(1)</script>` or
`javascript:alert(1)` rendered as working markup — stored XSS in any application
that emitted the result into a page.

The fix had to work within two existing constraints:

- The mapping architecture means callers can substitute their own renderer for
  any node type (see `ARCHITECTURE.md`), so there is no single chokepoint the
  library fully controls.
- Marks compose by successive wrapping: `TextRenderer.render` folds each mark
  renderer over `node["value"]`, so any escaping has to happen at a point where
  it runs exactly once. Escaping inside `BaseInlineRenderer` would
  double-escape a value carrying two marks.

## Decision

Neutralise untrusted values in the renderers that own them, on output, rather
than sanitising documents on input.

1. `TextRenderer.render` `deepcopy`s the node and HTML-escapes `node["value"]`
   **once, before** the mark loop. `BaseInlineRenderer` subclasses stay dumb tag
   wrappers and do not escape, which is what avoids double-escaping.
2. URLs go through a single `_safe_url` helper in `block_renderers.py`, used by
   both `HyperlinkRenderer.render` and `AssetHyperlinkRenderer._render`. It
   rejects protocol-relative `//host` URLs first, then checks the parsed scheme
   against an **allow-list** `_ALLOWED_SCHEMES = {"https", "http", "mailto",
   "tel", ""}`, rewrites anything else to `"#"`, and HTML-escapes what it
   returns with `quote=True`.
3. `AssetHyperlinkRenderer._render` escapes link text and `alt` values when
   `formatted=False` — the path `AssetBlockRenderer` uses for asset titles.

Two details of the allow-list are deliberate and documented inline. `""` is a
member so that scheme-less relative links (`/path`, `#anchor`) keep working,
which is also why protocol-relative URLs need their own earlier check — they
carry no scheme and would otherwise be accepted as relative. `mailto` and `tel`
are members because they are common in real content and cannot execute script.

Regression tests were added alongside, tagged with their ticket ids:
`test_render_escapes_html_in_value`, `test_render_escapes_html_before_wrapping_marks`
in `tests/text_renderers_test.py`; `test_render_neutralizes_dangerous_scheme`,
`test_render_rejects_protocol_relative_url`, `test_render_preserves_mailto`,
`test_render_escapes_alt_attribute` in `tests/block_renderers_test.py`.

## Consequences

- Default output is safe to emit into an HTML page without further escaping.
- Callers who consume the output as something other than HTML — a Markdown or
  plain-text renderer built on the mapping override mechanism — get
  HTML-escaped text they did not ask for, because `TextRenderer` escapes before
  marks are applied. Such callers must override `"text"` as well as the mark
  keys, and take on escaping themselves.
- The guarantee does not extend to custom renderers. A replacement for
  `"hyperlink"`, `"text"`, or `"embedded-entry-block"` that interpolates
  `node["value"]` or `data.uri` directly reintroduces the vulnerability. The
  default `EntryBlockRenderer` is itself an example of an unescaped path: it
  emits `str(node["data"]["target"])` inside a `<div>`, and applications are
  expected to replace it.
- Adding a scheme to `_ALLOWED_SCHEMES` is a security decision, not a
  configuration tweak. There is no public API for extending the list, which is
  intentional.
- Because escaping lives in renderers rather than in a sanitising pass, any new
  renderer that emits an attribute or raw value must route it through `escape`
  or `_safe_url` itself. This is called out in `AGENTS.md`.
