import pytest
from django.template import Template, Context
from django.utils import timezone

from django_object_detail.config import x
from django_object_detail.resolvers import (
    ResolvedGroup,
    ResolvedProperty,
    resolve_all,
)
from django_object_detail.config import PropertyGroupConfig
from tests.models import Info, Report


@pytest.fixture
def now():
    return timezone.now()


@pytest.fixture
def user(db):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        username="testuser",
        first_name="Test",
        last_name="User",
        password="testpass",
    )


@pytest.fixture
def info(db, now):
    return Info.objects.create(
        text="Some text",
        is_public=True,
        create_dt=now,
        update_dt=now,
    )


@pytest.fixture
def report(db, info, user):
    return Report.objects.create(title="Test Report", info=info, owner=user)


@pytest.fixture
def groups(report):
    configs = [
        PropertyGroupConfig(
            title="Report",
            description="Report details",
            icon="file-text",
            properties=["title", "owner"],
        ),
        PropertyGroupConfig(
            title="Info",
            properties=[
                x("info__text", title="Body"),
                "info__is_public",
            ],
        ),
    ]
    return resolve_all(report, configs)


class TestRenderObjectDetail:
    def test_renders_all_groups(self, groups):
        tpl = Template(
            "{% load object_detail %}{% render_object_detail obj groups %}"
        )
        ctx = Context({"obj": None, "groups": groups})
        html = tpl.render(ctx)
        assert "Report" in html
        assert "Info" in html

    def test_renders_property_values(self, groups):
        tpl = Template(
            "{% load object_detail %}{% render_object_detail obj groups %}"
        )
        ctx = Context({"obj": None, "groups": groups})
        html = tpl.render(ctx)
        assert "Test Report" in html
        assert "testuser" in html


class TestRenderGroup:
    def test_renders_group_title(self, groups):
        tpl = Template(
            "{% load object_detail %}{% render_group group %}"
        )
        ctx = Context({"group": groups[0]})
        html = tpl.render(ctx)
        assert "Report" in html
        assert "Report details" in html

    def test_renders_icon(self, groups):
        tpl = Template(
            "{% load object_detail %}{% render_group group %}"
        )
        ctx = Context({"group": groups[0]})
        html = tpl.render(ctx)
        assert "bi-file-text" in html

    def test_no_icon(self, groups):
        tpl = Template(
            "{% load object_detail %}{% render_group group %}"
        )
        ctx = Context({"group": groups[1]})
        html = tpl.render(ctx)
        assert "text-primary fs-5" not in html


class TestRenderProperty:
    def test_renders_label_and_value(self, groups):
        prop = groups[0].properties[0]  # title
        tpl = Template(
            "{% load object_detail %}{% render_property prop %}"
        )
        ctx = Context({"prop": prop})
        html = tpl.render(ctx)
        assert "Report title" in html
        assert "Test Report" in html

    def test_renders_detail(self):
        prop = ResolvedProperty(
            path="test",
            label="Test",
            value="val",
            detail="Detail info",
            type="char",
        )
        tpl = Template(
            "{% load object_detail %}{% render_property prop %}"
        )
        html = tpl.render(Context({"prop": prop}))
        assert "Detail info" in html


class TestRenderPropertyValue:
    def test_char_value(self):
        prop = ResolvedProperty(path="t", label="T", value="hello", type="char")
        tpl = Template(
            "{% load object_detail %}{% render_property_value prop %}"
        )
        html = tpl.render(Context({"prop": prop}))
        assert "hello" in html

    def test_boolean_true(self):
        prop = ResolvedProperty(path="t", label="T", value=True, type="boolean")
        tpl = Template(
            "{% load object_detail %}{% render_property_value prop %}"
        )
        html = tpl.render(Context({"prop": prop}))
        assert "check-circle-fill" in html

    def test_boolean_false(self):
        prop = ResolvedProperty(path="t", label="T", value=False, type="boolean")
        tpl = Template(
            "{% load object_detail %}{% render_property_value prop %}"
        )
        html = tpl.render(Context({"prop": prop}))
        assert "x-circle-fill" in html

    def test_none_value(self):
        prop = ResolvedProperty(path="t", label="T", value=None, type="char")
        tpl = Template(
            "{% load object_detail %}{% render_property_value prop %}"
        )
        html = tpl.render(Context({"prop": prop}))
        assert "&mdash;" in html or "\u2014" in html

    def test_manytomany_list(self):
        prop = ResolvedProperty(
            path="t", label="T", value=["Alice", "Bob"], type="manytomany", is_many=True,
        )
        tpl = Template(
            "{% load object_detail %}{% render_property_value prop %}"
        )
        html = tpl.render(Context({"prop": prop}))
        assert "Alice" in html
        assert "Bob" in html
        assert "<li>" in html

    def test_custom_template(self):
        prop = ResolvedProperty(
            path="t", label="T", value="custom-test-value",
            template="test_custom_value.html",
        )
        tpl = Template(
            "{% load object_detail %}{% render_property_value prop %}"
        )
        html = tpl.render(Context({"prop": prop}))
        assert '<span class="custom-rendered">custom-test-value</span>' in html

    def test_default_fallback(self):
        prop = ResolvedProperty(
            path="t", label="T", value="anything", type="unknown_type",
        )
        tpl = Template(
            "{% load object_detail %}{% render_property_value prop %}"
        )
        html = tpl.render(Context({"prop": prop}))
        assert "anything" in html
