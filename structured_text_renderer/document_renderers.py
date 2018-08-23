class DocumentRenderer(object):
    def __init__(
            self,
            heading_1_renderer=None,
            heading_2_renderer=None,
            paragraph_renderer=None,
            entry_block_renderer=None):
        self.heading_1_renderer = heading_1_renderer
        self.heading_2_renderer = heading_2_renderer
        self.paragraph_renderer = paragraph_renderer
        self.entry_block_renderer = entry_block_renderer

    def render(self, document):
        mappings = {
            'heading-1': self.heading_1_renderer,
            'heading-2': self.heading_2_renderer,
            'paragraph': self.paragraph_renderer,
            'embedded-entry-block': self.entry_block_renderer
        }

        result = []
        for node in document['content']:
            result.append(
                mappings[node['nodeType']].render(node)
            )

        return "\n".join(result)
