class DocumentRenderer(object):
    def __init__(
        self,
        heading_one_renderer=None,
        heading_two_renderer=None,
        paragraph_renderer=None,
        entry_block_renderer=None,
    ):
        self.mappings = {
            "heading-1": heading_one_renderer,
            "heading-2": heading_two_renderer,
            "paragraph": paragraph_renderer,
            "embedded-entry-block": entry_block_renderer,
        }

    def render(self, document):
        result = []
        for node in document["content"]:
            renderer = self.mappings.get(node["nodeType"], None)

            if renderer is None:
                continue

            result.append(renderer.render(node))

        return "\n".join(result)
