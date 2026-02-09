import pytest
from pydantic import ValidationError

from django_object_detail.config import (
    PropertyConfig,
    PropertyGroupConfig,
    parse_property_display,
    x,
)


class TestPropertyConfig:
    def test_minimal(self):
        cfg = PropertyConfig(path="title")
        assert cfg.path == "title"
        assert cfg.title is None
        assert cfg.detail is None
        assert cfg.type is None
        assert cfg.template is None

    def test_full(self):
        cfg = PropertyConfig(
            path="info__text",
            title="Custom",
            detail="Detail text",
            type="timestamp",
            template="my/template.html",
        )
        assert cfg.path == "info__text"
        assert cfg.title == "Custom"
        assert cfg.type == "timestamp"


class TestX:
    def test_simple(self):
        cfg = x("title")
        assert isinstance(cfg, PropertyConfig)
        assert cfg.path == "title"

    def test_with_kwargs(self):
        cfg = x("info__text", title="custom", detail="some detail")
        assert cfg.title == "custom"
        assert cfg.detail == "some detail"

    def test_with_template(self):
        cfg = x("info__owner", template="foo/bar.html")
        assert cfg.template == "foo/bar.html"


class TestPropertyGroupConfig:
    def test_string_normalization(self):
        group = PropertyGroupConfig(
            title="Test",
            properties=["title", "owner"],
        )
        assert len(group.properties) == 2
        assert all(isinstance(p, PropertyConfig) for p in group.properties)
        assert group.properties[0].path == "title"
        assert group.properties[1].path == "owner"

    def test_mixed_properties(self):
        group = PropertyGroupConfig(
            title="Test",
            properties=[
                "title",
                x("info__text", title="Custom"),
                {"path": "owner", "type": "foreignkey"},
            ],
        )
        assert len(group.properties) == 3
        assert group.properties[0].path == "title"
        assert group.properties[1].title == "Custom"
        assert group.properties[2].type == "foreignkey"

    def test_optional_fields(self):
        group = PropertyGroupConfig(title="Test", properties=["title"])
        assert group.description is None
        assert group.icon is None

    def test_with_icon_and_description(self):
        group = PropertyGroupConfig(
            title="Info",
            description="Some description",
            icon="info-circle-fill",
            properties=["title"],
        )
        assert group.icon == "info-circle-fill"
        assert group.description == "Some description"

    def test_invalid_property_raises(self):
        with pytest.raises(ValidationError):
            PropertyGroupConfig(title="Test", properties=[123])


class TestParsePropertyDisplay:
    def test_parse_list(self):
        raw = [
            {
                "title": "Report",
                "description": "Report details",
                "properties": ["title", "owner"],
            },
            {
                "title": "Info",
                "properties": [
                    x("info__text", title="custom"),
                    "info__is_public",
                ],
            },
        ]
        groups = parse_property_display(raw)
        assert len(groups) == 2
        assert groups[0].title == "Report"
        assert len(groups[0].properties) == 2
        assert groups[1].properties[0].title == "custom"

    def test_empty_list(self):
        groups = parse_property_display([])
        assert groups == []
