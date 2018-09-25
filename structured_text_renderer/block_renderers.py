from .base_node_renderer import BaseNodeRenderer


class BaseBlockRenderer(BaseNodeRenderer):
    def render(self, node):
        result = []
        for c in node["content"]:
            renderer = self._find_renderer(c)
            if renderer is None:
                continue
            result.append("<{0}>{1}</{0}>".format(self._render_tag, renderer.render(c)))
        return "\n".join(result)

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


class ParagraphRenderer(BaseBlockRenderer):
    @property
    def _render_tag(self):
        return "p"


class EntryBlockRenderer(BaseNodeRenderer):
    def render(self, node):
        return "<div>{0}</div>".format(node["data"])
