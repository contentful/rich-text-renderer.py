from unittest import TestCase
from structured_text_renderer.text_renderers import (
    TextRenderer,
    BoldRenderer,
    ItalicRenderer,
    UnderlineRenderer,
)
from structured_text_renderer.block_renderers import (
    ParagraphRenderer,
    HeadingOneRenderer,
    HeadingTwoRenderer,
    EntryBlockRenderer,
)
from structured_text_renderer.document_renderers import DocumentRenderer


mock_document = {
    "nodeType": "document",
    "content": [
        {
            "content": [{"value": "foo", "marks": [{"type": "bold"}]}],
            "nodeType": "heading-1",
        }
    ],
}

mock_document_with_unknown_nodetype = {
    "nodeType": "document",
    "content": [
        {
            "content": [{"value": "foo", "marks": [{"type": "bold"}]}],
            "nodeType": "unknown",
        }
    ],
}


class DocumentRendererTest(TestCase):
    def test_render(self):
        text_renderer = TextRenderer(
            bold_renderer=BoldRenderer(),
            italic_renderer=ItalicRenderer(),
            underline_renderer=UnderlineRenderer(),
        )
        heading_one_renderer = HeadingOneRenderer(text_renderer=text_renderer)
        heading_two_renderer = HeadingTwoRenderer(text_renderer=text_renderer)
        paragraph_renderer = ParagraphRenderer(text_renderer=text_renderer)
        entry_block_renderer = EntryBlockRenderer()

        document_renderer = DocumentRenderer(
            heading_one_renderer=heading_one_renderer,
            heading_two_renderer=heading_two_renderer,
            paragraph_renderer=paragraph_renderer,
            entry_block_renderer=entry_block_renderer,
        )

        self.assertEqual(
            document_renderer.render(mock_document), "\n".join(["<h1><b>foo</b></h1>"])
        )

    def test_render_will_skip_unknown_node_types(self):
        text_renderer = TextRenderer(
            bold_renderer=BoldRenderer(),
            italic_renderer=ItalicRenderer(),
            underline_renderer=UnderlineRenderer(),
        )
        heading_one_renderer = HeadingOneRenderer(text_renderer=text_renderer)
        heading_two_renderer = HeadingTwoRenderer(text_renderer=text_renderer)
        paragraph_renderer = ParagraphRenderer(text_renderer=text_renderer)
        entry_block_renderer = EntryBlockRenderer()

        document_renderer = DocumentRenderer(
            heading_one_renderer=heading_one_renderer,
            heading_two_renderer=heading_two_renderer,
            paragraph_renderer=paragraph_renderer,
            entry_block_renderer=entry_block_renderer,
        )

        self.assertEqual(
            document_renderer.render(mock_document_with_unknown_nodetype), "\n".join([])
        )
