import pytest
from django.test import override_settings

from django_object_detail.conf import get_layout_pack, get_property_text_newline, get_types_pack


class TestGetLayoutPack:
    def test_default(self):
        assert get_layout_pack() == "split-card"

    @override_settings(OBJECT_DETAIL_TEMPLATE_PACK_LAYOUT="accordion")
    def test_override(self):
        assert get_layout_pack() == "accordion"


class TestGetTypesPack:
    def test_default(self):
        assert get_types_pack() == "default"

    @override_settings(OBJECT_DETAIL_TEMPLATE_PACK_TYPES="custom")
    def test_override(self):
        assert get_types_pack() == "custom"


class TestGetPropertyTextNewline:
    def test_default(self):
        assert get_property_text_newline() == "linebreaksbr"

    @override_settings(OBJECT_DETAIL_PROPERTY_TEXT_NEWLINE="linebreaks")
    def test_override(self):
        assert get_property_text_newline() == "linebreaks"
