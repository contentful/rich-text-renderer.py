from unittest import TestCase
from copy import copy
from structured_text_renderer.text_renderers import BoldRenderer, TextRenderer
from structured_text_renderer.block_renderers import (
    ParagraphRenderer,
    BaseBlockRenderer,
    HeadingOneRenderer,
    HeadingTwoRenderer,
    EntryBlockRenderer,
)


mock_node = {"content": [{"value": "foo", "nodeType": "text"}]}

mock_node_with_marks = {
    "content": [{"value": "foo", "nodeType": "text", "marks": [{"type": "bold"}]}]
}

mock_data_node = {
    "data": {"target": {"sys": {"id": "foo", "type": "Link", "linkType": "Entry"}}}
}

mock_unknown_node = {"content": [{"value": "foo", "nodeType": "unknown"}]}


class HeadingOneRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            HeadingOneRenderer({"text": TextRenderer}).render(mock_node), "<h1>foo</h1>"
        )


class HeadingTwoRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            HeadingTwoRenderer({"text": TextRenderer}).render(mock_node), "<h2>foo</h2>"
        )


class ParagraphRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            ParagraphRenderer({"text": TextRenderer}).render(mock_node), "<p>foo</p>"
        )


class BaseBlockRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            BaseBlockRenderer({"text": TextRenderer}).render(mock_node),
            "<div>foo</div>",
        )

    def test_render_will_skip_unknown_nodes_if_no_null_renderer_is_provided(self):
        self.assertEqual(BaseBlockRenderer().render(mock_unknown_node), "")

    def test_render_will_propagate_to_text_renderers(self):
        self.assertEqual(
            BaseBlockRenderer({"text": TextRenderer, "bold": BoldRenderer}).render(
                mock_node_with_marks
            ),
            "<div><b>foo</b></div>",
        )


class EntryBlockRendererTest(TestCase):
    def test_render_will_return_str_of_data(self):
        entry_block_renderer = EntryBlockRenderer()

        self.assertEqual(
            entry_block_renderer.render(mock_data_node),
            "<div>{'target': {'sys': {'id': 'foo', 'type': 'Link', 'linkType': 'Entry'}}}</div>",
        )
