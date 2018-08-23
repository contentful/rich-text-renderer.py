class TextRenderer(object):
    def __init__(
            self,
            bold_renderer=None,
            italic_renderer=None,
            underline_renderer=None,
            **kwargs):
        self.bold_renderer = bold_renderer
        self.italic_renderer = italic_renderer
        self.underline_renderer = underline_renderer

    def render(self, node):
        for mark in node.get('marks', []):
            node['value'] = getattr(
                self,
                '{0}_renderer'.format(mark['type'])
            ).render(node)
        return node['value']


class BoldRenderer(object):
    def render(self, node):
        return "<b>{0}</b>".format(node['value'])


class ItalicRenderer(object):
    def render(self, node):
        return "<i>{0}</i>".format(node['value'])


class UnderlineRenderer(object):
    def render(self, node):
        return "<u>{0}</u>".format(node['value'])
