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
        return "<div>{0}</div>".format(node["data"])
