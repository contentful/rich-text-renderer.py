from .text_renderers import (
    TextRenderer,
    BoldRenderer,
    ItalicRenderer,
    UnderlineRenderer,
)
from .block_renderers import (
    HeadingOneRenderer,
    HeadingTwoRenderer,
    EntryBlockRenderer,
    ParagraphRenderer,
)
from .document_renderers import DocumentRenderer
from .null_renderer import NullRenderer
from .base_node_renderer import BaseNodeRenderer


class StructuredTextRenderer(BaseNodeRenderer):
    def __init__(self, mappings=None):
        DEFAULT_MAPPINGS = {
            "document": DocumentRenderer,
            "heading-1": HeadingOneRenderer,
            "heading-2": HeadingTwoRenderer,
            "embedded-entry-block": EntryBlockRenderer,
            "paragraph": ParagraphRenderer,
            "text": TextRenderer,
            "bold": BoldRenderer,
            "italic": ItalicRenderer,
            "underline": UnderlineRenderer,
            None: NullRenderer,
        }

        self.mappings = DEFAULT_MAPPINGS
        if mappings is not None:
            self.mappings.update(mappings)

    def render(self, document):
        return self._find_renderer(document).render(document)
