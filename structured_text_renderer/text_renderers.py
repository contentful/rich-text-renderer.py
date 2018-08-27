from copy import deepcopy


class TextRenderer(object):
    def __init__(
        self,
        bold_renderer=None,
        italic_renderer=None,
        underline_renderer=None,
        **kwargs
    ):
        self.bold_renderer = bold_renderer
        self.italic_renderer = italic_renderer
        self.underline_renderer = underline_renderer

    def render(self, node):
        node = deepcopy(node)
        for mark in node.get("marks", []):
            renderer = getattr(self, "{0}_renderer".format(mark["type"]), None)

            if renderer is not None:
                node["value"] = renderer.render(node)
        return node["value"]


class BaseInlineRenderer(object):
    def render(self, node):
        return "<{0}>{1}</{0}>".format(self._render_tag, node["value"])

    @property
    def _render_tag(self):
        return "span"


class BoldRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "b"


class ItalicRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "i"


class UnderlineRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "u"
