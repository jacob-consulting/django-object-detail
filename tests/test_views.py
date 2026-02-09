import pytest
from django.test import RequestFactory
from django.views.generic import DetailView
from django.utils import timezone

from django_object_detail.config import x
from django_object_detail.resolvers import ResolvedGroup
from django_object_detail.views import ObjectDetailMixin
from tests.models import Info, Report


class ReportDetailView(ObjectDetailMixin, DetailView):
    model = Report
    template_name = "django_object_detail/object_detail.html"
    property_display = [
        {
            "title": "Report",
            "description": "Report details",
            "icon": "file-text",
            "properties": [
                "title",
                "owner",
            ],
        },
        {
            "title": "Info",
            "properties": [
                x("info__text", title="Custom text"),
                "info__is_public",
            ],
        },
    ]


@pytest.fixture
def report(db):
    now = timezone.now()
    info = Info.objects.create(text="body", is_public=True, create_dt=now, update_dt=now)
    return Report.objects.create(title="My Report", info=info, owner=None)


@pytest.fixture
def factory():
    return RequestFactory()


class TestObjectDetailMixin:
    def test_context_has_groups(self, report, factory):
        request = factory.get(f"/reports/{report.pk}/")
        view = ReportDetailView()
        view.request = request
        view.object = report
        view.kwargs = {"pk": report.pk}
        context = view.get_context_data()
        assert "object_detail_groups" in context
        groups = context["object_detail_groups"]
        assert len(groups) == 2
        assert isinstance(groups[0], ResolvedGroup)
        assert groups[0].title == "Report"
        assert groups[0].icon == "file-text"

    def test_property_values(self, report, factory):
        request = factory.get(f"/reports/{report.pk}/")
        view = ReportDetailView()
        view.request = request
        view.object = report
        view.kwargs = {"pk": report.pk}
        context = view.get_context_data()
        groups = context["object_detail_groups"]
        # First group: title and owner
        props = groups[0].properties
        assert props[0].value == "My Report"
        assert props[1].value is None  # no owner

    def test_no_property_display(self, report, factory):
        class EmptyView(ObjectDetailMixin, DetailView):
            model = Report
            template_name = "django_object_detail/object_detail.html"

        request = factory.get(f"/reports/{report.pk}/")
        view = EmptyView()
        view.request = request
        view.object = report
        view.kwargs = {"pk": report.pk}
        context = view.get_context_data()
        assert "object_detail_groups" not in context
