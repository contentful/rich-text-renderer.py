from __future__ import unicode_literals
from .base_node_renderer import BaseNodeRenderer


class DocumentRenderer(BaseNodeRenderer):
    def render(self, document):
        result = []
        for node in document["content"]:
            renderer = self._find_renderer(node)

            if renderer is None:
                continue

            result.append(renderer.render(node))

        return "\n".join(result)
