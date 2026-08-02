# Add Rich Text Table Support

## Status

Accepted

## Context

Contentful added table support to the Rich Text field type (node types: `table`, `table-row`, `table-cell`, `table-header-cell`). Without explicit renderers, tables would hit `NullRenderer` and raise an exception, breaking any application using rich text with tables.

Source: commit `3797ddf` (merged PR #17, 2022-04-22), CHANGELOG v0.2.5.

## Decision

Four new renderer classes were added to `block_renderers.py`:
- `TableRenderer` → `<table>`
- `TableRowRenderer` → `<tr>`
- `TableCellRenderer` → `<td>`
- `TableHeaderCellRenderer` → `<th>`

All four extend `BaseBlockRenderer`, which provides the standard `_render_tag` + `_render_content()` pattern already used for headings, paragraphs, and lists. The four new node types were added to `DEFAULT_MAPPINGS` in `RichTextRenderer`.

## Consequences

- Applications processing rich text documents with tables no longer raise `NullRenderer` exceptions on upgrade to v0.2.5+.
- The table renderers output semantic HTML (`<table>`, `<tr>`, `<th>`, `<td>`) with no styling — consumers should apply CSS.
- Consumers building non-HTML output (e.g., Markdown) must override all four table node types in their custom mappings.
- The pattern is fully consistent with existing block renderers — no new abstractions introduced.
