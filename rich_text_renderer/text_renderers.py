from __future__ import unicode_literals
from copy import deepcopy

from .base_node_renderer import BaseNodeRenderer


class TextRenderer(BaseNodeRenderer):
    def render(self, node):
        node = deepcopy(node)
        for mark in node.get("marks", []):
            renderer = self._find_renderer(mark)

            if renderer is not None:
                node["value"] = renderer.render(node)
        return node["value"]

    def _find_renderer(self, node):
        renderer = self.mappings.get(node.get("type", None), None)

        if renderer is not None:
            return renderer(self.mappings)


class BaseInlineRenderer(BaseNodeRenderer):
    def render(self, node):
        return "<{0}>{1}</{0}>".format(self._render_tag, node["value"])

    @property
    def _render_tag(self):
        return "span"


class BoldRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "b"


class CodeRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "code"


class ItalicRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "i"


class UnderlineRenderer(BaseInlineRenderer):
    @property
    def _render_tag(self):
        return "u"
