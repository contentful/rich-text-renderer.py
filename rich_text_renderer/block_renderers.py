from __future__ import unicode_literals
from .base_node_renderer import BaseNodeRenderer


class BaseBlockRenderer(BaseNodeRenderer):
    def render(self, node):
        return "<{0}>{1}</{0}>".format(self._render_tag, self._render_content(node))

    def _render_content(self, node):
        result = []
        for c in node["content"]:
            renderer = self._find_renderer(c)
            if renderer is None:
                continue
            result.append(renderer.render(c))
        return "".join(result)

    @property
    def _render_tag(self):
        return "div"


class HeadingOneRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "h1"


class HeadingTwoRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "h2"


class HeadingThreeRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "h3"


class HeadingFourRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "h4"


class HeadingFiveRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "h5"


class HeadingSixRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "h6"


class ParagraphRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "p"


class OrderedListRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "ol"


class UnorderedListRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "ul"


class ListItemRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "li"


class BlockQuoteRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "blockquote"


class HrRenderer(BaseNodeRenderer):
    def render(self, _node):
        return "<hr />"


class HyperlinkRenderer(BaseBlockRenderer):
    def render(self, node):
        return '<a href="{0}">{1}</a>'.format(
            node["data"]["uri"], self._render_content(node)
        )


class EntryBlockRenderer(BaseNodeRenderer):
    def render(self, node):
        return "<div>{0}</div>".format(node["data"]["target"])


class AssetHyperlinkRenderer(BaseBlockRenderer):
    ANCHOR_HTML = '<a href="{0}">{1}</a>'

    def render(self, node):
        asset = node["data"]["target"]

        # Check by class name instead of instance type to
        # avoid dependending on the Contentful SDK.
        if asset.__class__.__name__ == "Asset":
            return self._render_asset(asset, node)
        elif isinstance(asset, dict):
            if "fields" not in asset and "file" not in asset.get("fields", {}):
                raise Exception("Node target is not an asset - Node: {0}".format(node))
            return self._render_hash(asset, node)
        else:
            raise Exception("Node target is not an asset - Node: {0}".format(node))

    def _render_asset(self, asset, node=None):
        return self._render(
            self.__class__.ANCHOR_HTML,
            asset.url(),
            node if node is not None else asset.title,
            bool(node),
        )

    def _render_hash(self, asset, node=None):
        return self._render(
            self.__class__.ANCHOR_HTML,
            asset["fields"]["file"]["url"],
            node if node is not None else asset["fields"]["title"],
            bool(node),
        )

    def _render(self, markup, url, text, formatted=True):
        if formatted:
            text = self._render_content(text)
        return markup.format(url, text)


class AssetBlockRenderer(AssetHyperlinkRenderer):
    IMAGE_HTML = '<img src="{0}" alt="{1}" />'

    def _render_asset(self, asset, node=None):
        if "contentType" in asset.file and "image" in asset.file["contentType"]:
            return self._render(
                self.__class__.IMAGE_HTML, asset.url(), asset.title, False
            )
        return super(AssetBlockRenderer, self)._render_asset(asset)

    def _render_hash(self, asset, node=None):
        if (
            "contentType" in asset["fields"]["file"]
            and "image" in asset["fields"]["file"]["contentType"]
        ):
            return self._render(
                self.__class__.IMAGE_HTML,
                asset["fields"]["file"]["url"],
                asset["fields"]["title"],
                False,
            )
        return super(AssetBlockRenderer, self)._render_hash(asset)
