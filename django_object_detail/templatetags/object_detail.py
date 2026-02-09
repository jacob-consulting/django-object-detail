from django import template
from django.template.loader import select_template

from django_object_detail.config import parse_property_display
from django_object_detail.resolvers import ResolvedGroup, resolve_all

register = template.Library()


@register.inclusion_tag("django_object_detail/object_detail.html")
def render_object_detail(obj, groups=None, property_display=None):
    """Render all property groups for an object.

    ``groups`` can be pre-resolved ``ResolvedGroup`` instances (from the mixin)
    or a raw ``property_display`` list that will be parsed and resolved here.
    """
    if groups is None and property_display is not None:
        configs = parse_property_display(property_display)
        groups = resolve_all(obj, configs)

    return {"groups": groups or []}


@register.inclusion_tag("django_object_detail/group.html")
def render_group(group):
    """Render a single property group (split-card layout)."""
    return {"group": group}


@register.inclusion_tag("django_object_detail/property.html")
def render_property(prop):
    """Render a single property row."""
    return {"prop": prop}


@register.simple_tag(takes_context=True)
def render_property_value(context, prop):
    """Render the value of a property using its type-specific template.

    Returns the rendered HTML string.
    """
    if prop.template:
        template_names = [prop.template]
    else:
        template_names = [
            f"django_object_detail/types/{prop.type}.html",
            "django_object_detail/types/default.html",
        ]

    tpl = select_template(template_names)
    return tpl.render({"prop": prop, "value": prop.value}, context.get("request"))
