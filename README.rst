Contentful Structured Text Renderer
===================================

`Contentful <https://www.contentful.com>`_ provides a content infrastructure for digital teams to power content in websites, apps, and devices. Unlike a CMS, Contentful was built to integrate with the modern software stack. It offers a central hub for structured content, powerful management and delivery APIs, and a customizable web app that enable developers and content creators to ship digital products faster.

This library provides rendering capabilities for the ``StructuredText`` field type. It is recommended to be used alongside the `Contentful Delivery SDK <https://www.github.com/contentful/contentful.py>`.
By default this library will serialize ``StructuredText`` fields into it's corresponding HTML representation. All behaviour can be overridden to serialize to different formats.

Installation
------------

Install Contentful Structured Text Renderer from the Python Package Index::

    pip install structured_text_renderer

Usage
-----

Create a renderer::

    from structured_text_renderer import StructuredTextRenderer

    renderer = StructuredTextRenderer()

Render your document::

    renderer.render(document)

Using different renderers
-------------------------

There are many cases in which HTML serialization is not what you want.
Therefore, all renderers are overridable when creating a `structured_text_renderer.StructuredTextRenderer <structured_text_renderer.StructuredTextRenderer>`.

Also, if you're planning to embed entries within your structured text, overriding the ``entry_block_renderer`` option is a must,
as by default it only does ``<div>str(entry)</div>``.

You can override the configuration like follows::

    renderer = StructuredTextRenderer(
        entry_block_renderer=MyEntryBlockRenderer
    )

Where ``MyEntryBlockRenderer`` requires to have a ``render(self, node)`` method and needs to return a string.

An example entry renderer, assuming our entry has 2 fields called ``name`` and ``description`` could be::

    class MyEntryBlockRenderer(object):
        def render(self, node):
            entry = node['data']

            return "<div class='my-entry'><h3>{0}</h3><p><small>{1}</p></small></div>".format(
                entry.name,
                entry.description
            )

License
-------

Copyright (c) 2018 Contentful GmbH. See `LICENSE <./LICENSE>`_ for further details.

Contributing
------------

Feel free to improve this tool by submitting a Pull Request.