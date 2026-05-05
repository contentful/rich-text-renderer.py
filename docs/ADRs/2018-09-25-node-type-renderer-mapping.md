# Node-Type → Renderer Class Mapping Architecture

## Status

Accepted

## Context

The Rich Text field in Contentful's API returns a JSON document tree where each node has a `nodeType` string (e.g., `"paragraph"`, `"heading-1"`, `"embedded-entry-block"`). The initial implementation (commit `d01aa0b`) used a more monolithic approach. As node types grew, the architecture needed a pattern that would let consumers override rendering behavior for individual node types without forking the library.

The key tension: the library must work out-of-the-box for the common case (HTML output) while remaining fully customizable for non-HTML targets (Markdown, plain text, custom CMS markup).

## Decision

A central `DEFAULT_MAPPINGS` dictionary maps each `nodeType` string to a dedicated renderer class. The `RichTextRenderer` constructor accepts an optional `mappings` dict that is merged over the defaults via `dict.update()`.

Each renderer class implements a single `render(self, node)` method. Block renderers extend `BaseBlockRenderer` (which provides `_render_content()` for recursive child dispatch); inline mark renderers extend `BaseInlineRenderer`. A `NullRenderer` is registered under the `None` key as the catch-all for unmapped node types — it raises an `Exception` rather than silently returning empty strings, making missing mappings visible.

Source: commit `f94d885` ("Change architecture to use global mappings", 2018-09-25).

## Consequences

- Consumers can swap any renderer by passing `{node_type: MyRendererClass}` — no subclassing of `RichTextRenderer` required.
- Adding new node types (e.g., table support in v0.2.5) is purely additive: add the renderer class and add the mapping to `DEFAULT_MAPPINGS`.
- The `NullRenderer` default ensures unknown node types fail loudly. Consumers who want silent fallback must explicitly register `{None: SilentRenderer}`.
- All renderer classes receive the full `mappings` dict in their constructor, allowing nested/recursive rendering through the same dispatch mechanism.
- The pattern is consistent with sibling renderers in Ruby, Java, Swift, and PHP — lowering the cognitive cost of cross-language SDK work.
