# Rename StructuredText to RichText

## Status

Accepted

## Context

The Contentful Rich Text field type was initially called "StructuredText" during early development. The library was originally named `structured_text_renderer` and exposed a `StructuredTextRenderer` class. As the product moved from alpha to beta, Contentful standardized on "RichText" as the canonical name across all SDKs and the Contentful API.

Source: commit `4328648` ("Rename StructuredText to RichText", 2018-10-15) and CHANGELOG v0.1.0.

## Decision

The package was renamed from `structured_text_renderer` to `rich_text_renderer` and the primary class was renamed from `StructuredTextRenderer` to `RichTextRenderer`. This was treated as a feature release (v0.1.0) rather than a patch, reflecting the breaking rename. The CHANGELOG notes: "As `RichText` moves from `alpha` to `beta`, we're treating this as a feature release."

## Consequences

- Any code referencing the old `structured_text_renderer` package or `StructuredTextRenderer` class breaks on upgrade.
- The PyPI package name changed — consumers must update their `pip install` command and imports.
- The rename aligns the Python library with all other Contentful SDK languages, reducing confusion for developers working across multiple language SDKs.
- All subsequent node types and documentation use "Rich Text" consistently.
