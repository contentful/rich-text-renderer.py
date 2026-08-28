# Architecture

`rich_text_renderer` turns a Contentful Rich Text document — the nested `dict`
returned by the Content Delivery API for a `RichText` field — into a string.
Out of the box that string is HTML, but every part of the serialization is
replaceable, so the same traversal can emit Markdown, plain text, or anything
else.

The library has **no runtime dependencies**. `setup.py` declares
`requirements = []` and passes it as `install_requires`, and the package never
imports the Contentful Delivery SDK — see "Duck-typed asset detection" below.

## Package layout

| Path | Contents |
| --- | --- |
| `rich_text_renderer/__init__.py` | Public surface: re-exports `RichTextRenderer`, and holds `__version__`, `__author__`, `__email__` (read by `setup.py` via regex) |
| `rich_text_renderer/rich_text_renderer.py` | `RichTextRenderer` — the entry point and the default node-type → renderer mapping |
| `rich_text_renderer/base_node_renderer.py` | `BaseNodeRenderer` — the base class every renderer extends; owns `mappings` and `_find_renderer` |
| `rich_text_renderer/document_renderers.py` | `DocumentRenderer` — handles the top-level `document` node |
| `rich_text_renderer/block_renderers.py` | Block and inline-block renderers (headings, lists, tables, hyperlinks, assets, `hr`) plus the `_safe_url` URL allow-list |
| `rich_text_renderer/text_renderers.py` | `TextRenderer` and the mark renderers (`bold`, `italic`, `underline`, `code`, `superscript`, `subscript`) |
| `rich_text_renderer/null_renderer.py` | `NullRenderer` — raises for node types with no mapping |
| `tests/` | `unittest` test cases, one module per source module |
| `runtests.py` | Test entry point used by CI: `from tests import *` then `unittest.main()` |

## The dispatch loop

There is no visitor, no registry singleton, and no AST. Rendering is a
recursive walk in which each renderer looks up the renderer for its children in
a `mappings` dict it carries with it.

1. `RichTextRenderer.__init__` builds `DEFAULT_MAPPINGS`, a dict keyed by
   Contentful `nodeType` strings (`"heading-1"`, `"paragraph"`,
   `"embedded-asset-block"`, …) whose values are renderer **classes**, not
   instances. A user-supplied `mappings` dict is merged over it with
   `dict.update`, so callers override individual keys rather than supplying a
   complete table. The key `None` maps to `NullRenderer` and acts as the
   fallback for unrecognised node types.
2. `RichTextRenderer.render(document)` calls `self._find_renderer(document)`,
   which for a well-formed document resolves `"document"` → `DocumentRenderer`.
3. `BaseNodeRenderer._find_renderer` reads `node["nodeType"]`, looks the class
   up in `self.mappings`, and instantiates it as `renderer(self.mappings)`.
   The mapping table is therefore threaded down the whole tree — every child
   renderer sees the same overrides the caller passed at the top.
4. `DocumentRenderer.render` iterates `document["content"]`, renders each child,
   and joins the results with `"\n"`.
5. `BaseBlockRenderer._render_content` does the same for nested content but
   joins with `""`, and `BaseBlockRenderer.render` wraps the result in
   `<{_render_tag}>…</{_render_tag}>`.

`_find_renderer` returns `None` when a node has no `nodeType` key at all, and
both `DocumentRenderer.render` and `BaseBlockRenderer._render_content` skip such
nodes with `continue`. Only nodes that *do* carry an unmapped `nodeType` reach
`NullRenderer` and raise.

### Marks are dispatched on a different key

Text nodes carry formatting in `node["marks"]`, and marks are keyed by `type`,
not `nodeType`. `TextRenderer` therefore overrides `_find_renderer` to read
`node.get("type")`. `TextRenderer.render` escapes the value once, then folds
each mark renderer over it — `node["value"] = renderer.render(node)` — so marks
compose by successive wrapping. Mark renderers extend `BaseInlineRenderer`,
whose `render` emits `<tag>{node["value"]}</tag>` and deliberately does *not*
re-escape; the escaping already happened in `TextRenderer`.

## The extension point

Nearly every concrete renderer is a subclass that overrides one thing. Block
renderers override the `_render_tag` property (`ParagraphRenderer` → `"p"`,
`TableRowRenderer` → `"tr"`, and so on); mark renderers do the same against
`BaseInlineRenderer`. That is the entire pattern for structural tags.

Anything else is a `render` override. The contract for a custom renderer,
as documented in `README.rst` and enforced implicitly by `_find_renderer`:

- It must be constructible with a single positional argument, the `mappings`
  dict. Subclassing `BaseNodeRenderer` satisfies this.
- It must expose `render(self, node)` and return a string.
- If it renders children, it should subclass `BaseBlockRenderer` and call
  `self._render_content(node)` so the mapping table keeps propagating.

Two overrides matter in practice:

- **`"embedded-entry-block"`** — the default `EntryBlockRenderer` only emits
  `<div>{str(node["data"]["target"])}</div>`. Any application that embeds
  entries is expected to replace it.
- **`None`** — replacing `NullRenderer` with a renderer that returns `""` turns
  unknown node types from an exception into a silent skip.

## Escaping is a property of the renderers, not of the input

Untrusted content is neutralised at the point of serialization, in three places
(all introduced by `2b0518b`):

- `TextRenderer.render` HTML-escapes `node["value"]` on a `deepcopy` of the node
  before any mark renderer sees it.
- `_safe_url` in `block_renderers.py` rejects protocol-relative URLs, checks the
  scheme against `_ALLOWED_SCHEMES` (`https`, `http`, `mailto`, `tel`, and `""`
  for scheme-less relative links), substitutes `"#"` for anything else, and
  HTML-escapes what remains. `HyperlinkRenderer.render` and
  `AssetHyperlinkRenderer._render` route every URL through it.
- `AssetHyperlinkRenderer._render` escapes `alt`/link text when
  `formatted=False`, which is the path `AssetBlockRenderer` uses for asset
  titles.

The consequence for extenders is direct: a custom `render` that interpolates
`node["value"]` or a `data.uri` itself bypasses all of it. See
`docs/ADRs/2026-08-25-escape-at-the-render-boundary.md`.

## Duck-typed asset detection

`AssetHyperlinkRenderer.render` accepts either a Contentful SDK `Asset` object
or a plain `dict` from raw API JSON, and distinguishes them with
`asset.__class__.__name__ == "Asset"` rather than `isinstance`. The inline
comment states the reason: it avoids depending on the Contentful SDK. `Asset`
objects are read via `asset.url()` / `asset.title` / `asset.file`; dicts are
read via `asset["fields"]["file"]["url"]` / `asset["fields"]["title"]`.
`AssetBlockRenderer` subclasses it and overrides both branches to emit `<img>`
when the file's `contentType` contains `"image"`.

## Build, test, release

- Tests are plain `unittest`. `tests/__init__.py` star-imports the test modules
  and `runtests.py` runs `unittest.main()` over them.
- CI is CircleCI (`.circleci/config.yml`): a single `test` job on
  `cimg/python:<version>` for a matrix of `3.7`, `3.8`, `3.9`, which installs
  `requirements.txt` and runs `python runtests.py`.
  `.github/workflows/codeql.yml` additionally CodeQL-scans the GitHub Actions
  workflows themselves, not the Python source.
- `requirements.txt` is a pinned *development* manifest (flake8, coverage,
  ipython). It is not the package's dependency set.
- `Makefile` wraps the local loop: `make lint` (flake8), `make format` (black),
  `make test`, `make test-all` (tox), `make coverage`, `make dist`,
  `make release` (`python setup.py publish`). `tox.ini` sets
  `max_line_length = 100` and lists a wider envlist (`py27`…`py37`, pypy) than
  CI exercises.
- `setup.py publish` builds with `build`, uploads with `twine`, then tags the
  version from `__init__.py` and pushes. Version bumps are manual edits to
  `rich_text_renderer/__init__.py`, recorded by hand in `CHANGELOG.md`.
- Ownership is `@contentful/team-developer-experience`
  (`.github/CODEOWNERS`, `catalog-info.yaml`); service tier 4.
