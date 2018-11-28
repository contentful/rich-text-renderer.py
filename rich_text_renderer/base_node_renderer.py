from __future__ import unicode_literals


class BaseNodeRenderer(object):
    def __init__(self, mappings=None):
        if mappings is None:
            mappings = {}
        self.mappings = mappings

    def _find_renderer(self, node):
        renderer = self.mappings.get(node.get("nodeType", None), None)
        if renderer is not None:
            return renderer(self.mappings)
