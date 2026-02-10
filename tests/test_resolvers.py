import pytest
from django.utils import timezone
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

from django_object_detail.config import LinkConfig, PropertyConfig, PropertyGroupConfig, x
from django_object_detail.resolvers import (
    ResolvedGroup,
    ResolvedProperty,
    resolve_all,
    resolve_group,
    resolve_property,
)
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
def user2(db):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        username="otheruser",
        first_name="Other",
        last_name="User",
        password="testpass",
    )


@pytest.fixture
def info(db, now):
    return Info.objects.create(
        text="Some info text",
        is_public=True,
        create_dt=now,
        update_dt=now,
    )


@pytest.fixture
def report(db, info, user):
    return Report.objects.create(
        title="Test Report",
        info=info,
        owner=user,
    )


class TestResolvePropertySimpleFields:
    def test_char_field(self, report):
        cfg = PropertyConfig(path="title")
        rp = resolve_property(report, cfg)
        assert rp.value == "Test Report"
        assert rp.label == "Report title"
        assert rp.type == "char"
        assert rp.is_many is False

    def test_boolean_field(self, report):
        cfg = PropertyConfig(path="info__is_public")
        rp = resolve_property(report, cfg)
        assert rp.value is True
        assert rp.label == "Public"
        assert rp.type == "boolean"

    def test_text_field(self, report):
        cfg = PropertyConfig(path="info__text")
        rp = resolve_property(report, cfg)
        assert rp.value == "Some info text"
        assert rp.type == "text"
        assert rp.detail == "The info body text"

    def test_datetime_field(self, report, now):
        cfg = PropertyConfig(path="info__create_dt")
        rp = resolve_property(report, cfg)
        assert rp.value == now
        assert rp.type == "datetime"


class TestResolvePropertyFKTraversal:
    def test_fk_object(self, report, user):
        cfg = PropertyConfig(path="owner")
        rp = resolve_property(report, cfg)
        assert rp.value == user
        assert rp.type == "foreignkey"

    def test_fk_field_traversal(self, report, user):
        cfg = PropertyConfig(path="owner__username")
        rp = resolve_property(report, cfg)
        assert rp.value == "testuser"
        assert rp.type == "char"

    def test_o2o_traversal(self, report):
        cfg = PropertyConfig(path="info__text")
        rp = resolve_property(report, cfg)
        assert rp.value == "Some info text"

    def test_reverse_o2o_is_not_many(self, info, report):
        """Reverse OneToOneField should resolve as a single object, not a list."""
        cfg = PropertyConfig(path="report")
        rp = resolve_property(info, cfg)
        assert rp.value == report
        assert rp.type == "foreignkey"
        assert rp.is_many is False

    def test_reverse_o2o_traversal(self, info, report):
        cfg = PropertyConfig(path="report__title")
        rp = resolve_property(info, cfg)
        assert rp.value == "Test Report"
        assert rp.type == "char"
        assert rp.is_many is False

    def test_deep_chain(self, report):
        cfg = PropertyConfig(path="info__create_dt")
        rp = resolve_property(report, cfg)
        assert rp.type == "datetime"


class TestResolvePropertyMethods:
    def test_callable_method(self, report):
        cfg = PropertyConfig(path="title_upper")
        rp = resolve_property(report, cfg)
        assert rp.value == "TEST REPORT"

    def test_fk_method(self, report):
        cfg = PropertyConfig(path="owner__get_full_name")
        rp = resolve_property(report, cfg)
        assert rp.value == "Test User"


class TestResolvePropertyM2M:
    def test_m2m_fanout(self, report, user, user2):
        report.access_users.add(user, user2)
        cfg = PropertyConfig(path="access_users__get_full_name")
        rp = resolve_property(report, cfg)
        assert rp.is_many is True
        assert set(rp.value) == {"Test User", "Other User"}

    def test_m2m_empty(self, report):
        cfg = PropertyConfig(path="access_users__get_full_name")
        rp = resolve_property(report, cfg)
        assert rp.is_many is True
        assert rp.value == []


class TestResolvePropertyLabelCapitalization:
    def test_verbose_name_capitalized(self, report):
        """Auto-generated verbose_name (lowercase) should get first letter capitalized."""
        cfg = PropertyConfig(path="owner")
        rp = resolve_property(report, cfg)
        assert rp.label == "Owner"

    def test_explicit_verbose_name_preserved(self, report):
        """Explicit verbose_name already starting uppercase should be unchanged."""
        cfg = PropertyConfig(path="title")
        rp = resolve_property(report, cfg)
        assert rp.label == "Report title"


class TestResolvePropertyOverrides:
    def test_title_override(self, report):
        cfg = x("title", title="Custom Title")
        rp = resolve_property(report, cfg)
        assert rp.label == "Custom Title"

    def test_detail_override(self, report):
        cfg = x("title", detail="Custom detail")
        rp = resolve_property(report, cfg)
        assert rp.detail == "Custom detail"

    def test_type_override(self, report, now):
        cfg = x("info__create_dt", type="timestamp")
        rp = resolve_property(report, cfg)
        assert rp.type == "timestamp"
        assert rp.value == now

    def test_template_override(self, report):
        cfg = x("title", template="custom/template.html")
        rp = resolve_property(report, cfg)
        assert rp.template == "custom/template.html"


class TestResolvePropertyNullSafety:
    def test_null_fk(self, db):
        report = Report.objects.create(title="No owner", owner=None, info=None)
        cfg = PropertyConfig(path="owner__username")
        rp = resolve_property(report, cfg)
        assert rp.value is None

    def test_null_o2o(self, db):
        report = Report.objects.create(title="No info", owner=None, info=None)
        cfg = PropertyConfig(path="info__text")
        rp = resolve_property(report, cfg)
        assert rp.value is None


class TestResolvePropertyLinkUrl:
    def test_fk_auto_pk(self, report, user):
        """FK value with string link shorthand auto-uses kwargs={"pk": pk}."""
        cfg = x("owner", link="user-detail")
        rp = resolve_property(report, cfg)
        assert rp.link_url == f"/users/{user.pk}/"

    def test_explicit_kwargs(self, report, user):
        cfg = x("owner", link=LinkConfig(url="user-detail", kwargs={"pk": "pk"}))
        rp = resolve_property(report, cfg)
        assert rp.link_url == f"/users/{user.pk}/"

    def test_explicit_args(self, report, user):
        cfg = x("owner", link=LinkConfig(url="user-detail", args=["pk"]))
        rp = resolve_property(report, cfg)
        assert rp.link_url == f"/users/{user.pk}/"

    def test_null_fk_returns_none(self, db):
        report = Report.objects.create(title="No owner", owner=None, info=None)
        cfg = x("owner", link="user-detail")
        rp = resolve_property(report, cfg)
        assert rp.link_url is None

    def test_o2o_link(self, report, info):
        cfg = x("info", link="info-detail")
        rp = resolve_property(report, cfg)
        assert rp.link_url == f"/info/{info.pk}/"

    def test_no_link_config_returns_none(self, report):
        cfg = PropertyConfig(path="owner")
        rp = resolve_property(report, cfg)
        assert rp.link_url is None

    def test_bad_url_name_returns_none(self, report):
        cfg = x("owner", link="nonexistent-url")
        rp = resolve_property(report, cfg)
        assert rp.link_url is None

    def test_is_many_returns_none(self, report, user):
        report.access_users.add(user)
        cfg = x("access_users", link="user-detail")
        rp = resolve_property(report, cfg)
        assert rp.link_url is None


class TestResolveGroup:
    def test_resolve_group(self, report):
        cfg = PropertyGroupConfig(
            title="Report",
            description="Details",
            icon="file-text",
            properties=["title", "owner"],
        )
        rg = resolve_group(report, cfg)
        assert isinstance(rg, ResolvedGroup)
        assert rg.title == "Report"
        assert rg.description == "Details"
        assert rg.icon == "file-text"
        assert len(rg.properties) == 2


class TestResolveAll:
    def test_resolve_all(self, report):
        configs = [
            PropertyGroupConfig(title="G1", properties=["title"]),
            PropertyGroupConfig(title="G2", properties=["owner"]),
        ]
        groups = resolve_all(report, configs)
        assert len(groups) == 2
        assert groups[0].title == "G1"
        assert groups[1].title == "G2"


class TestLazyStringResolution:
    """Lazy translation strings should pass through config into resolved objects."""

    def test_title_override_stays_lazy(self, report):
        cfg = x("title", title=_("Custom Title"))
        rp = resolve_property(report, cfg)
        assert isinstance(rp.label, Promise)
        assert str(rp.label) == "Custom Title"

    def test_detail_override_stays_lazy(self, report):
        cfg = x("title", detail=_("Custom detail"))
        rp = resolve_property(report, cfg)
        assert isinstance(rp.detail, Promise)
        assert str(rp.detail) == "Custom detail"

    def test_group_title_stays_lazy(self, report):
        cfg = PropertyGroupConfig(
            title=_("Report Info"),
            description=_("Details about the report"),
            properties=["title"],
        )
        rg = resolve_group(report, cfg)
        assert isinstance(rg.title, Promise)
        assert isinstance(rg.description, Promise)
        assert str(rg.title) == "Report Info"
        assert str(rg.description) == "Details about the report"
