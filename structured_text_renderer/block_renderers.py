class BaseBlockRenderer(object):
    def __init__(self, text_renderer=None):
        self.text_renderer = text_renderer

    def render(self, node):
        return "\n".join(
            "<{0}>{1}</{0}>".format(self._render_tag, self.text_renderer.render(c))
            for c in node["content"]
        )

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


class EntryBlockRenderer(object):
    def render(self, node):
        return "<div>{0}</div>".format(node["data"])
