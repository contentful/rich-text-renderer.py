from unittest import TestCase
from structured_text_renderer.null_renderer import NullRenderer

mock_node_with_nodeType = {"nodeType": "foo"}

mock_node_with_type = {"type": "bar"}

mock_node_with_none = {"foo": "bar"}


class NullRendererTest(TestCase):
    def test_uses_nodeType_if_found(self):
        with self.assertRaisesRegexp(Exception, "No renderer defined for 'foo' nodes"):
            NullRenderer().render(mock_node_with_nodeType)

    def test_uses_type_if_found(self):
        with self.assertRaisesRegexp(Exception, "No renderer defined for 'bar' nodes"):
            NullRenderer().render(mock_node_with_type)

    def test_stringifies_node_otherwise(self):
        with self.assertRaisesRegexp(
            Exception, "No renderer defined for '{0}' nodes".format(mock_node_with_none)
        ):
            NullRenderer().render(mock_node_with_none)
