class HeadingOneRenderer(object):
    def __init__(self, text_renderer=None):
        self.text_renderer = text_renderer

    def render(self, node):
        return "\n".join("<h1>{0}</h1>".format(
            self.text_renderer.render(c)
        ) for c in node['content'])


class HeadingTwoRenderer(object):
    def __init__(self, text_renderer=None):
        self.text_renderer = text_renderer

    def render(self, node):
        return "\n".join("<h2>{0}</h2>".format(
            self.text_renderer.render(c)
        ) for c in node['content'])


class EntryBlockRenderer(object):
    def render(self, node):
        return "<div>{0}</div>".format(
            node['data']
        )


class ParagraphRenderer(object):
    def __init__(self, text_renderer=None):
        self.text_renderer = text_renderer

    def render(self, node):
        return "\n".join("<p>{0}</p>".format(
            self.text_renderer.render(c)
        ) for c in node['content'])
