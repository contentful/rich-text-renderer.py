from .text_renderers import TextRenderer, BoldRenderer, ItalicRenderer, UnderlineRenderer
from .block_renderers import HeadingOneRenderer, HeadingTwoRenderer, EntryBlockRenderer, ParagraphRenderer
from .document_renderers import DocumentRenderer


class StructuredTextRenderer(object):
    def __init__(
            self,
            document_renderer=None,
            heading_1_renderer=None,
            heading_2_renderer=None,
            entry_block_renderer=None,
            paragraph_renderer=None,
            text_renderer=None,
            bold_renderer=None,
            italic_renderer=None,
            underline_renderer=None):

        self.bold_renderer = (BoldRenderer if bold_renderer is None else bold_renderer)()
        self.italic_renderer = (ItalicRenderer if italic_renderer is None else italic_renderer)()
        self.underline_renderer = (UnderlineRenderer if underline_renderer is None else underline_renderer)()
        self.text_renderer = (TextRenderer if text_renderer is None else text_renderer)(
            bold_renderer=self.bold_renderer,
            italic_renderer=self.italic_renderer,
            underline_renderer=self.underline_renderer
        )

        self.heading_1_renderer = (HeadingOneRenderer if heading_1_renderer is None else heading_1_renderer)(
            text_renderer=self.text_renderer
        )
        self.heading_2_renderer = (HeadingTwoRenderer if heading_2_renderer is None else heading_2_renderer)(
            text_renderer=self.text_renderer
        )
        self.paragraph_renderer = (ParagraphRenderer if paragraph_renderer is None else paragraph_renderer)(
            text_renderer=self.text_renderer
        )
        self.entry_block_renderer = (EntryBlockRenderer if entry_block_renderer is None else entry_block_renderer)()

        self.document_renderer = (DocumentRenderer if document_renderer is None else document_renderer)(
            heading_1_renderer=self.heading_1_renderer,
            heading_2_renderer=self.heading_2_renderer,
            paragraph_renderer=self.paragraph_renderer,
            entry_block_renderer=self.entry_block_renderer
        )

    def render(self, document):
        return self.document_renderer.render(document)
