from django import template
from django.template.loader import select_template
from django.utils.safestring import mark_safe

from django_object_detail.conf import (
    build_icon_class,
    build_named_icon_class,
    get_layout_pack,
    get_property_text_newline,
    get_types_pack,
)
from django_object_detail.config import parse_property_display
from django_object_detail.resolvers import ResolvedGroup, resolve_all

register = template.Library()


@register.simple_tag(takes_context=True)
def render_object_detail(context, obj, groups=None, property_display=None):
    """Render all property groups for an object.

    ``groups`` can be pre-resolved ``ResolvedGroup`` instances (from the mixin)
    or a raw ``property_display`` list that will be parsed and resolved here.
    """
    if groups is None and property_display is not None:
        configs = parse_property_display(property_display)
        groups = resolve_all(obj, configs)

    pack = get_layout_pack()
    tpl = select_template([
        f"django_object_detail/layouts/{pack}/object_detail.html",
        "django_object_detail/object_detail.html",
    ])
    return mark_safe(tpl.render({"groups": groups or []}, context.get("request")))


@register.simple_tag(takes_context=True)
def render_group(context, group):
    """Render a single property group using the configured layout pack."""
    pack = get_layout_pack()
    tpl = select_template([
        f"django_object_detail/layouts/{pack}/group.html",
    ])
    return mark_safe(tpl.render({"group": group}, context.get("request")))


@register.simple_tag(takes_context=True)
def render_property(context, prop):
    """Render a single property row using the configured layout pack."""
    pack = get_layout_pack()
    tpl = select_template([
        f"django_object_detail/layouts/{pack}/property.html",
    ])
    return mark_safe(tpl.render({"prop": prop}, context.get("request")))


@register.simple_tag(takes_context=True)
def render_property_value(context, prop):
    """Render the value of a property using its type-specific template.

    Returns the rendered HTML string.
    """
    types_pack = get_types_pack()
    if prop.badge_css:
        template_names = [
            f"django_object_detail/types/{types_pack}/badge.html",
            "django_object_detail/types/default/badge.html",
        ]
    elif prop.template:
        template_names = [prop.template]
    else:
        template_names = [
            f"django_object_detail/types/{types_pack}/{prop.type}.html",
            f"django_object_detail/types/{types_pack}/default.html",
            "django_object_detail/types/default/default.html",
        ]

    tpl = select_template(template_names)
    od_settings = {
        "property_text_newline": get_property_text_newline(),
    }
    return tpl.render({"prop": prop, "value": prop.value, "od_settings": od_settings}, context.get("request"))


@register.filter
def icon_class(icon_name):
    """Return the full CSS class string for an icon name."""
    return build_icon_class(icon_name)


@register.filter
def named_icon_class(name):
    """Return the full CSS class string for a named icon."""
    return build_named_icon_class(name)
