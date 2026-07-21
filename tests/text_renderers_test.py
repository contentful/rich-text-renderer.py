from unittest import TestCase
from rich_text_renderer.text_renderers import (
    UnderlineRenderer,
    ItalicRenderer,
    BoldRenderer,
    CodeRenderer,
    TextRenderer,
    BaseInlineRenderer,
    SuperscriptRenderer,
    SubscriptRenderer
)
from rich_text_renderer.base_node_renderer import BaseNodeRenderer


class BoldMarkdownRenderer(BaseNodeRenderer):
    def render(self, node):
        return "**{0}**".format(node["value"])


mock_node = {"value": "foo"}

mock_node_underline_only = {"value": "foo", "marks": [{"type": "underline"}]}

mock_node_italic_only = {"value": "foo", "marks": [{"type": "italic"}]}

mock_node_bold_only = {"value": "foo", "marks": [{"type": "bold"}]}

mock_node_multiple_marks = {
    "value": "foo",
    "marks": [{"type": "underline"}, {"type": "italic"}, {"type": "bold"}],
}


mock_node_unsupported_mark = {"value": "foo", "marks": [{"type": "foobar"}]}

mock_node_xss = {"value": "<script>alert(1)</script>"}

mock_node_xss_with_mark = {
    "value": "<script>alert(1)</script>",
    "marks": [{"type": "bold"}],
}


class UnderlineRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(UnderlineRenderer().render(mock_node), "<u>foo</u>")


class CodeRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(CodeRenderer().render(mock_node), "<code>foo</code>")


class ItalicRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(ItalicRenderer().render(mock_node), "<i>foo</i>")


class BoldRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(BoldRenderer().render(mock_node), "<b>foo</b>")


class BaseInlineRendererTest(TestCase):
    def test_render_will_return_spans(self):
        self.assertEqual(BaseInlineRenderer().render(mock_node), "<span>foo</span>")


class SuperscriptRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(SuperscriptRenderer().render(mock_node), "<sup>foo</sup>")


class SubscriptRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(SubscriptRenderer().render(mock_node), "<sub>foo</sub>")


class TextRendererTest(TestCase):
    def test_render_single_mark(self):
        text_renderer = TextRenderer(
            {
                "bold": BoldRenderer,
                "italic": ItalicRenderer,
                "underline": UnderlineRenderer,
            }
        )

        self.assertEqual(text_renderer.render(mock_node_bold_only), "<b>foo</b>")
        self.assertEqual(text_renderer.render(mock_node_italic_only), "<i>foo</i>")
        self.assertEqual(text_renderer.render(mock_node_underline_only), "<u>foo</u>")

    def test_render_multiple_marks(self):
        text_renderer = TextRenderer(
            {
                "bold": BoldRenderer,
                "italic": ItalicRenderer,
                "underline": UnderlineRenderer,
            }
        )

        self.assertEqual(
            text_renderer.render(mock_node_multiple_marks), "<b><i><u>foo</u></i></b>"
        )

    def test_render_unsupported_mark(self):
        text_renderer = TextRenderer(
            {
                "bold": BoldRenderer,
                "italic": ItalicRenderer,
                "underline": UnderlineRenderer,
            }
        )

        self.assertEqual(text_renderer.render(mock_node_unsupported_mark), "foo")

    def test_render_with_different_renderer(self):
        text_renderer = TextRenderer({"bold": BoldMarkdownRenderer})

        self.assertEqual(text_renderer.render(mock_node_bold_only), "**foo**")

    def test_render_escapes_html_in_value(self):
        # AIS-256 / AIS-259: text node content must be HTML-escaped to prevent
        # stored XSS.
        text_renderer = TextRenderer({})

        self.assertEqual(
            text_renderer.render(mock_node_xss),
            "&lt;script&gt;alert(1)&lt;/script&gt;",
        )

    def test_render_escapes_html_before_wrapping_marks(self):
        # Escaping happens before the mark tags are applied, so the mark markup
        # is preserved while the value is neutralized (no double-escaping).
        text_renderer = TextRenderer({"bold": BoldRenderer})

        self.assertEqual(
            text_renderer.render(mock_node_xss_with_mark),
            "<b>&lt;script&gt;alert(1)&lt;/script&gt;</b>",
        )
