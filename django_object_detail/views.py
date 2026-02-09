from __future__ import annotations

from django_object_detail.config import PropertyGroupConfig, parse_property_display
from django_object_detail.resolvers import resolve_all


class ObjectDetailMixin:
    """Mixin for class-based views that adds resolved property groups to context.

    Set ``property_display`` on your view as a list of group dicts
    (the same DSL accepted by ``parse_property_display``).

    The resolved groups are added to the template context as
    ``object_detail_groups``.
    """

    property_display: list[dict] | list[PropertyGroupConfig] | None = None

    def get_property_display(self) -> list[PropertyGroupConfig]:
        raw = self.property_display
        if raw is None:
            return []
        if raw and isinstance(raw[0], PropertyGroupConfig):
            return raw
        return parse_property_display(raw)

    def get_object_for_detail(self):
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = self.get_property_display()
        if groups:
            instance = self.get_object_for_detail()
            context["object_detail_groups"] = resolve_all(instance, groups)
        return context
