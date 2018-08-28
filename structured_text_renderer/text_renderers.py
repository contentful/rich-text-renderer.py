from copy import deepcopy


class TextRenderer(object):
    def __init__(
        self,
        bold_renderer=None,
        italic_renderer=None,
        underline_renderer=None,
        **kwargs
    ):

        self.mappings = {
            'bold': bold_renderer,
            'italic': italic_renderer,
            'underline': underline_renderer
        }

    def render(self, node):
        node = deepcopy(node)
        for mark in node.get("marks", []):
            renderer = self.mappings.get(mark["type"], None)

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
