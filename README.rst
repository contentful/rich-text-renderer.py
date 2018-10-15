Contentful Rich Text Renderer
===================================

`Contentful <https://www.contentful.com>`_ provides a content infrastructure for digital teams to power content in websites, apps, and devices. Unlike a CMS, Contentful was built to integrate with the modern software stack. It offers a central hub for structured content, powerful management and delivery APIs, and a customizable web app that enable developers and content creators to ship digital products faster.

This library provides rendering capabilities for the ``RichText`` field type. It is recommended to be used alongside the `Contentful Delivery SDK <https://www.github.com/contentful/contentful.py>`.
By default this library will serialize ``RichText`` fields into it's corresponding HTML representation. All behaviour can be overridden to serialize to different formats.

Installation
------------

Install Contentful Rich Text Renderer from the Python Package Index::

    pip install rich_text_renderer

Usage
-----

Create a renderer::

    from rich_text_renderer import RichTextRenderer

    renderer = RichTextRenderer()

Render your document::

    renderer.render(document)

Using different renderers
-------------------------

There are many cases in which HTML serialization is not what you want.
Therefore, all renderers are overridable when creating a `rich_text_renderer.RichTextRenderer <rich_text_renderer.RichTextRenderer>`.

Also, if you're planning to embed entries within your rich text, overriding the ``'embedded-entry-block'`` option is a must,
as by default it only does ``<div>str(entry)</div>``.

You can override the configuration like follows::

    renderer = RichTextRenderer({
        'embedded-entry-node': MyEntryBlockRenderer
    })

Where ``MyEntryBlockRenderer`` requires to have a ``render(self, node)`` method and needs to return a string, also it requires to be initialized with a ``dict`` containing mappings for all renderers.

An example entry renderer, assuming our entry has 2 fields called ``name`` and ``description`` could be::

    from rich_text_renderer.base_node_mapper import BaseNodeMapper

    # BaseNodeRenderer implements the `__init__` method required.
    class MyEntryBlockRenderer(BaseNodeRenderer):
        def render(self, node):
            entry = node['data']

            return "<div class='my-entry'><h3>{0}</h3><p><small>{1}</p></small></div>".format(
                entry.name,
                entry.description
            )

Dealing with unknown node types
-------------------------------

By default, this library will treat all unknown node types as errors and will raise an exception letting the user know which node mapping is missing.
If you wish to remove this behaviour then replace the ``None`` key of the mapping with a ``NullRenderer`` that returns an empty string, or something similar.

An example would be like follows::

    class SilentNullRenderer(BaseNodeRenderer):
        def render(node):
            return ""

    renderer = RichTextRenderer({
        None: SilentNullRenderer
    })

License
-------

Copyright (c) 2018 Contentful GmbH. See `LICENSE <./LICENSE>`_ for further details.

Contributing
------------

Feel free to improve this tool by submitting a Pull Request.
