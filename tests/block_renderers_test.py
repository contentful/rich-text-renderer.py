from unittest import TestCase
from structured_text_renderer.text_renderers import (
    TextRenderer,
    BoldRenderer,
    ItalicRenderer,
    UnderlineRenderer,
)
from structured_text_renderer.block_renderers import (
    ParagraphRenderer,
    BaseBlockRenderer,
    HeadingOneRenderer,
    HeadingTwoRenderer,
    EntryBlockRenderer,
)


mock_node = {"content": [{"value": "foo"}]}

mock_node_with_marks = {"content": [{"value": "foo", "marks": [{"type": "bold"}]}]}

mock_data_node = {
    "data": {"target": {"sys": {"id": "foo", "type": "Link", "linkType": "Entry"}}}
}


class HeadingOneRendererTest(TestCase):
    def test_render(self):
        text_renderer = TextRenderer(
            bold_renderer=BoldRenderer(),
            italic_renderer=ItalicRenderer(),
            underline_renderer=UnderlineRenderer(),
        )
        heading_one_renderer = HeadingOneRenderer(text_renderer=text_renderer)

        self.assertEqual(heading_one_renderer.render(mock_node), "<h1>foo</h1>")


class HeadingTwoRendererTest(TestCase):
    def test_render(self):
        text_renderer = TextRenderer(
            bold_renderer=BoldRenderer(),
            italic_renderer=ItalicRenderer(),
            underline_renderer=UnderlineRenderer(),
        )
        heading_two_renderer = HeadingTwoRenderer(text_renderer=text_renderer)

        self.assertEqual(heading_two_renderer.render(mock_node), "<h2>foo</h2>")


class ParagraphRendererTest(TestCase):
    def test_render(self):
        text_renderer = TextRenderer(
            bold_renderer=BoldRenderer(),
            italic_renderer=ItalicRenderer(),
            underline_renderer=UnderlineRenderer(),
        )
        paragraph_renderer = ParagraphRenderer(text_renderer=text_renderer)

        self.assertEqual(paragraph_renderer.render(mock_node), "<p>foo</p>")


class BaseBlockRendererTest(TestCase):
    def test_render(self):
        text_renderer = TextRenderer(
            bold_renderer=BoldRenderer(),
            italic_renderer=ItalicRenderer(),
            underline_renderer=UnderlineRenderer(),
        )
        base_block_renderer = BaseBlockRenderer(text_renderer=text_renderer)

        self.assertEqual(base_block_renderer.render(mock_node), "<div>foo</div>")

    def test_render_will_propagate_to_text_renderers(self):
        text_renderer = TextRenderer(
            bold_renderer=BoldRenderer(),
            italic_renderer=ItalicRenderer(),
            underline_renderer=UnderlineRenderer(),
        )
        base_block_renderer = BaseBlockRenderer(text_renderer=text_renderer)

        self.assertEqual(
            base_block_renderer.render(mock_node_with_marks), "<div><b>foo</b></div>"
        )


class EntryBlockRendererTest(TestCase):
    def test_render_will_return_str_of_data(self):
        entry_block_renderer = EntryBlockRenderer()

        self.assertEqual(
            entry_block_renderer.render(mock_data_node),
            "<div>{'target': {'sys': {'id': 'foo', 'type': 'Link', 'linkType': 'Entry'}}}</div>",
        )
