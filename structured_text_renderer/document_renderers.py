class DocumentRenderer(object):
    def __init__(
        self,
        heading_one_renderer=None,
        heading_two_renderer=None,
        paragraph_renderer=None,
        entry_block_renderer=None,
    ):
        self.heading_one_renderer = heading_one_renderer
        self.heading_two_renderer = heading_two_renderer
        self.paragraph_renderer = paragraph_renderer
        self.entry_block_renderer = entry_block_renderer

    def render(self, document):
        mappings = {
            "heading-1": self.heading_one_renderer,
            "heading-2": self.heading_two_renderer,
            "paragraph": self.paragraph_renderer,
            "embedded-entry-block": self.entry_block_renderer,
        }

        result = []
        for node in document["content"]:
            renderer = mappings.get(node["nodeType"], None)

            if renderer is None:
                continue

            result.append(mappings[node["nodeType"]].render(node))

        return "\n".join(result)
