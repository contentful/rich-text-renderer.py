from unittest import TestCase
from rich_text_renderer.text_renderers import BoldRenderer, TextRenderer
from rich_text_renderer.block_renderers import (
    ParagraphRenderer,
    BaseBlockRenderer,
    HeadingOneRenderer,
    HeadingTwoRenderer,
    HeadingThreeRenderer,
    HeadingFourRenderer,
    HeadingFiveRenderer,
    HeadingSixRenderer,
    EntryBlockRenderer,
    AssetHyperlinkRenderer,
    AssetBlockRenderer,
    ListItemRenderer,
    OrderedListRenderer,
    UnorderedListRenderer,
    BlockQuoteRenderer,
    HrRenderer,
    HyperlinkRenderer,
    TableCellRenderer,
    TableHeaderCellRenderer,
    TableRowRenderer,
    TableRenderer
)


class Asset(object):
    def __init__(self, json):
        self.fields = json["fields"]
        self.file = self.fields["file"]
        self.title = self.fields["title"]
        self.url = lambda: self.file["url"]


mock_node = {"content": [{"value": "foo", "nodeType": "text"}]}

mock_node_with_marks = {
    "content": [{"value": "foo", "nodeType": "text", "marks": [{"type": "bold"}]}]
}

mock_data_node = {
    "data": {"target": {"sys": {"id": "foo", "type": "Link", "linkType": "Entry"}}}
}

mock_image_asset_node = {
    "data": {
        "target": {
            "fields": {
                "title": "Foo",
                "file": {
                    "contentType": "image/jpeg",
                    "url": "https://example.com/cat.jpg",
                },
            }
        }
    }
}

mock_image_asset_resolved_node = {
    "data": {
        "target": Asset(
            {
                "fields": {
                    "title": "Foo",
                    "file": {
                        "contentType": "image/jpeg",
                        "url": "https://example.com/cat.jpg",
                    },
                }
            }
        )
    }
}

mock_non_image_asset_node = {
    "data": {
        "target": {
            "fields": {
                "title": "Foo",
                "file": {
                    "contentType": "text/csv",
                    "url": "https://example.com/cat.csv",
                },
            }
        }
    }
}

mock_non_image_asset_resolved_node = {
    "data": {
        "target": Asset(
            {
                "fields": {
                    "title": "Foo",
                    "file": {
                        "contentType": "text/csv",
                        "url": "https://example.com/cat.csv",
                    },
                }
            }
        )
    }
}

mock_asset_hyperlink_node = {
    "data": {
        "target": Asset(
            {
                "fields": {
                    "title": "Foo",
                    "file": {
                        "contentType": "image/jpeg",
                        "url": "https://example.com/cat.jpg",
                    },
                }
            }
        )
    },
    "content": [{"value": "Example", "nodeType": "text", "marks": []}],
}

mock_hyperlink_node = {
    "data": {"uri": "https://example.com"},
    "content": [{"value": "Example", "nodeType": "text", "marks": []}],
}

mock_list_node = {
    "content": [
        {"content": [{"value": "foo", "nodeType": "text"}], "nodeType": "list-item"}
    ]
}

mock_node_with_multiple_content_nodes = {
    "content": [
        {"value": "foo", "nodeType": "text", "marks": [{"type": "bold"}]},
        {"value": " bar", "nodeType": "text"},
    ]
}

mock_paragraph_node = {
    "content": [
        {
            "nodeType": "paragraph",
            "data": {},
            "content": [
                {
                    "nodeType": "text",
                    "data": {},
                    "marks": [],
                    "value": "Hello world!"
                }
            ]
        }
    ]
}

mock_table_cell_node = {
    "content": [
        {
            "nodeType": "table-cell",
            "data": {},
            "content": [
                {
                    "nodeType": "paragraph",
                    "data": {},
                    "content": [
                        {
                            "nodeType": "text",
                            "data": {},
                            "marks": [],
                            "value": "Hello world!"
                        }
                    ]
                }
            ]
        }
    ]
}

mock_table_row_node = {
    "content": [
        {
            "nodeType": "table-row",
            "data": {},
            "content": [
                {
                    "nodeType": "table-cell",
                    "data": {},
                    "content": [
                        {
                            "nodeType": "paragraph",
                            "data": {},
                            "content": [
                                {
                                    "nodeType": "text",
                                    "data": {},
                                    "marks": [],
                                    "value": "Hello world!"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
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


class HeadingThreeRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            HeadingThreeRenderer({"text": TextRenderer}).render(mock_node),
            "<h3>foo</h3>",
        )


class HeadingFourRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            HeadingFourRenderer({"text": TextRenderer}).render(mock_node),
            "<h4>foo</h4>",
        )


class HeadingFiveRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            HeadingFiveRenderer({"text": TextRenderer}).render(mock_node),
            "<h5>foo</h5>",
        )


class HeadingSixRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            HeadingSixRenderer({"text": TextRenderer}).render(mock_node), "<h6>foo</h6>"
        )


class ParagraphRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            ParagraphRenderer({"text": TextRenderer}).render(mock_node), "<p>foo</p>"
        )


class BlockQuoteRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            BlockQuoteRenderer({"text": TextRenderer}).render(mock_node),
            "<blockquote>foo</blockquote>",
        )


class ListItemRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            ListItemRenderer({"text": TextRenderer}).render(mock_node), "<li>foo</li>"
        )


class OrderedListRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            OrderedListRenderer(
                {"text": TextRenderer, "list-item": ListItemRenderer}
            ).render(mock_list_node),
            "<ol><li>foo</li></ol>",
        )


class UnorderedListRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            UnorderedListRenderer(
                {"text": TextRenderer, "list-item": ListItemRenderer}
            ).render(mock_list_node),
            "<ul><li>foo</li></ul>",
        )


class BaseBlockRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            BaseBlockRenderer({"text": TextRenderer}).render(mock_node),
            "<div>foo</div>",
        )

    def test_render_will_skip_unknown_nodes_if_no_null_renderer_is_provided(self):
        self.assertEqual(BaseBlockRenderer().render(mock_unknown_node), "<div></div>")

    def test_render_will_propagate_to_text_renderers(self):
        self.assertEqual(
            BaseBlockRenderer({"text": TextRenderer, "bold": BoldRenderer}).render(
                mock_node_with_marks
            ),
            "<div><b>foo</b></div>",
        )

    def test_render_will_properly_render_nodes_with_multiple_content_nodes(self):
        self.assertEqual(
            BaseBlockRenderer({"text": TextRenderer, "bold": BoldRenderer}).render(
                mock_node_with_multiple_content_nodes
            ),
            "<div><b>foo</b> bar</div>",
        )


class EntryBlockRendererTest(TestCase):
    def test_render_will_return_str_of_data(self):
        entry_block_renderer = EntryBlockRenderer()

        self.assertEqual(
            entry_block_renderer.render(mock_data_node),
            "<div>{0}</div>".format(mock_data_node["data"]["target"]),
        )


class HrRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(HrRenderer().render(mock_node), "<hr />")


class HyperlinkRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            HyperlinkRenderer({"text": TextRenderer}).render(mock_hyperlink_node),
            '<a href="https://example.com">Example</a>',
        )


class AssetBlockRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            AssetBlockRenderer({"text": TextRenderer}).render(mock_image_asset_node),
            '<img src="https://example.com/cat.jpg" alt="Foo" />',
        )

        self.assertEqual(
            AssetBlockRenderer({"text": TextRenderer}).render(
                mock_image_asset_resolved_node
            ),
            '<img src="https://example.com/cat.jpg" alt="Foo" />',
        )

        self.assertEqual(
            AssetBlockRenderer({"text": TextRenderer}).render(
                mock_non_image_asset_node
            ),
            '<a href="https://example.com/cat.csv">Foo</a>',
        )

        self.assertEqual(
            AssetBlockRenderer({"text": TextRenderer}).render(
                mock_non_image_asset_resolved_node
            ),
            '<a href="https://example.com/cat.csv">Foo</a>',
        )


class AssetHyperlinkRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            AssetHyperlinkRenderer({"text": TextRenderer}).render(
                mock_asset_hyperlink_node
            ),
            '<a href="https://example.com/cat.jpg">Example</a>',
        )

    def test_render_raises_exception_when_node_is_not_asset(self):
        with self.assertRaises(Exception) as cm:
            AssetHyperlinkRenderer().render(mock_node)
        self.assertEqual(cm.exception.__class__, KeyError)

        with self.assertRaises(Exception) as cm:
            AssetHyperlinkRenderer().render({"data": {"target": None}})
        self.assertEqual(cm.exception.__class__, Exception)
        self.assertTrue("Node target is not an asset" in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            AssetHyperlinkRenderer().render({"data": {"target": {}}})
        self.assertEqual(cm.exception.__class__, Exception)
        self.assertTrue("Node target is not an asset" in str(cm.exception))


class TableCellRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            TableCellRenderer({"text": TextRenderer, "paragraph": ParagraphRenderer}).render(
                mock_paragraph_node
            ), "<td><p>Hello world!</p></td>"
        )


class TableHeaderCellRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            TableHeaderCellRenderer({"text": TextRenderer, "paragraph": ParagraphRenderer}).render(
                mock_paragraph_node
            ), "<th><p>Hello world!</p></th>"
        )


class TableRowRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            TableRowRenderer({"text": TextRenderer, "paragraph": ParagraphRenderer,
                              "table-cell": TableCellRenderer}).render(
                mock_table_cell_node
            ), "<tr><td><p>Hello world!</p></td></tr>"
        )


class TableRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            TableRenderer({"text": TextRenderer, "paragraph": ParagraphRenderer,
                           "table-cell": TableCellRenderer, "table-row": TableRowRenderer}).render(
                mock_table_row_node
            ), "<table><tr><td><p>Hello world!</p></td></tr></table>"
        )


class HeadingOneWithOneAttributeRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            HeadingOneRenderer(
                {"text": TextRenderer},
                attributes={"class": "ui header"}
            ).render(mock_node),
            '<h1 class="ui header">foo</h1>'
        )


class UnorderedListRendererWithTwoAttributesRendererTest(TestCase):
    def test_render(self):
        self.assertEqual(
            UnorderedListRenderer(
                {"text": TextRenderer, "list-item": ListItemRenderer},
                attributes={"class": "ui list", "style": "list-style: circle;"}
            ).render(mock_list_node),
            '<ul class="ui list" style="list-style: circle;"><li>foo</li></ul>',
        )
