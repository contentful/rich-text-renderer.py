from __future__ import unicode_literals

from .text_renderers import (
    TextRenderer,
    BoldRenderer,
    CodeRenderer,
    ItalicRenderer,
    UnderlineRenderer,
    SuperscriptRenderer,
    SubscriptRenderer
)
from .block_renderers import (
    HrRenderer,
    HeadingOneRenderer,
    HeadingTwoRenderer,
    HeadingThreeRenderer,
    HeadingFourRenderer,
    HeadingFiveRenderer,
    HeadingSixRenderer,
    BlockQuoteRenderer,
    HyperlinkRenderer,
    ListItemRenderer,
    OrderedListRenderer,
    UnorderedListRenderer,
    ParagraphRenderer,
    EntryBlockRenderer,
    AssetBlockRenderer,
    AssetHyperlinkRenderer,
    TableCellRenderer,
    TableHeaderCellRenderer,
    TableRowRenderer,
    TableRenderer
)
from .document_renderers import DocumentRenderer
from .null_renderer import NullRenderer
from .base_node_renderer import BaseNodeRenderer


class RichTextRenderer(BaseNodeRenderer):
    def __init__(self, mappings=None):
        DEFAULT_MAPPINGS = {
            "document": DocumentRenderer,
            "heading-1": HeadingOneRenderer,
            "heading-2": HeadingTwoRenderer,
            "heading-3": HeadingThreeRenderer,
            "heading-4": HeadingFourRenderer,
            "heading-5": HeadingFiveRenderer,
            "heading-6": HeadingSixRenderer,
            "blockquote": BlockQuoteRenderer,
            "hyperlink": HyperlinkRenderer,
            "list-item": ListItemRenderer,
            "ordered-list": OrderedListRenderer,
            "unordered-list": UnorderedListRenderer,
            "hr": HrRenderer,
            "embedded-entry-block": EntryBlockRenderer,
            "embedded-asset-block": AssetBlockRenderer,
            "asset-hyperlink": AssetHyperlinkRenderer,
            "paragraph": ParagraphRenderer,
            "text": TextRenderer,
            "bold": BoldRenderer,
            "code": CodeRenderer,
            "superscript": SuperscriptRenderer,
            "subscript": SubscriptRenderer,
            "italic": ItalicRenderer,
            "underline": UnderlineRenderer,
            "table-cell": TableCellRenderer,
            "table-row": TableRowRenderer,
            "table-header-cell": TableHeaderCellRenderer,
            "table": TableRenderer,
            None: NullRenderer,
        }

        self.mappings = DEFAULT_MAPPINGS
        if mappings is not None:
            self.mappings.update(mappings)

    def render(self, document):
        return self._find_renderer(document).render(document)
