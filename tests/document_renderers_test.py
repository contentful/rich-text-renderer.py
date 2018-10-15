from unittest import TestCase
from rich_text_renderer.text_renderers import TextRenderer, BoldRenderer
from rich_text_renderer.block_renderers import ParagraphRenderer, HeadingOneRenderer
from rich_text_renderer.document_renderers import DocumentRenderer


mock_document = {
    "nodeType": "document",
    "content": [
        {
            "content": [
                {"value": "foo", "nodeType": "text", "marks": [{"type": "bold"}]}
            ],
            "nodeType": "heading-1",
        }
    ],
}

mock_document_with_unknown_nodetype = {
    "nodeType": "document",
    "content": [
        {
            "content": [
                {"value": "foo", "nodeType": "text", "marks": [{"type": "bold"}]}
            ],
            "nodeType": "unknown",
        }
    ],
}


class DocumentRendererTest(TestCase):
    def test_render(self):
        document_renderer = DocumentRenderer(
            {
                "heading-1": HeadingOneRenderer,
                "paragraph": ParagraphRenderer,
                "text": TextRenderer,
                "bold": BoldRenderer,
            }
        )

        self.assertEqual(
            document_renderer.render(mock_document), "\n".join(["<h1><b>foo</b></h1>"])
        )

    def test_render_will_skip_unknown_node_types(self):
        document_renderer = DocumentRenderer()

        self.assertEqual(
            document_renderer.render(mock_document_with_unknown_nodetype), "\n".join([])
        )
