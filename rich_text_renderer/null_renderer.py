from .base_node_renderer import BaseNodeRenderer


class NullRenderer(BaseNodeRenderer):
    def render(self, node):
        raise Exception(
            "No renderer defined for '{0}' nodes".format(self._node_type(node))
        )

    def _node_type(self, node):
        if "nodeType" in node:
            return node["nodeType"]
        elif "type" in node:
            return node["type"]
        return node
