from django.conf import settings

_UNSET = object()

ICON_LIBRARY_DEFAULTS = {
    "bootstrap": {
        "class": "bi",
        "type": None,
        "prefix": "bi",
    },
    "fontawesome": {
        "class": "fa",
        "type": "regular",
        "prefix": "fa",
    },
}

NAMED_ICONS_DEFAULTS = {
    "bootstrap": {
        "boolean-true": "check-circle-fill",
        "boolean-false": "x-circle-fill",
        "property-detail": "info-circle",
        "text-icon": "journal-text",
    },
    "fontawesome": {
        "boolean-true": "circle-check",
        "boolean-false": "circle-xmark",
        "property-detail": "circle-info",
        "text-icon": "file-lines",
    },
}


def get_layout_pack():
    return getattr(settings, "OBJECT_DETAIL_TEMPLATE_PACK_LAYOUT", "split-card")


def get_types_pack():
    return getattr(settings, "OBJECT_DETAIL_TEMPLATE_PACK_TYPES", "default")


def get_icons_library():
    return getattr(settings, "OBJECT_DETAIL_ICONS_LIBRARY", "bootstrap")


def get_icons_class():
    value = getattr(settings, "OBJECT_DETAIL_ICONS_CLASS", _UNSET)
    if value is not _UNSET:
        return value
    library = get_icons_library()
    return ICON_LIBRARY_DEFAULTS.get(library, {}).get("class", "")


def get_icons_type():
    value = getattr(settings, "OBJECT_DETAIL_ICONS_TYPE", _UNSET)
    if value is not _UNSET:
        return value
    library = get_icons_library()
    return ICON_LIBRARY_DEFAULTS.get(library, {}).get("type")


def get_icons_prefix():
    value = getattr(settings, "OBJECT_DETAIL_ICONS_PREFIX", _UNSET)
    if value is not _UNSET:
        return value
    library = get_icons_library()
    return ICON_LIBRARY_DEFAULTS.get(library, {}).get("prefix", "")


def get_named_icons():
    value = getattr(settings, "OBJECT_DETAIL_NAMED_ICONS", _UNSET)
    if value is not _UNSET:
        return value
    library = get_icons_library()
    return NAMED_ICONS_DEFAULTS.get(library, {})


def build_icon_class(icon_name):
    """Build a full CSS icon class string for the given icon name."""
    cls = get_icons_class()
    icon_type = get_icons_type()
    prefix = get_icons_prefix()

    if icon_type:
        base = f"{cls}-{icon_type}"
    else:
        base = cls

    return f"{base} {prefix}-{icon_name}"


def get_property_text_newline():
    return getattr(settings, "OBJECT_DETAIL_PROPERTY_TEXT_NEWLINE", "linebreaksbr")


def build_named_icon_class(name):
    """Resolve a named icon and return the full CSS class string."""
    named_icons = get_named_icons()
    icon_name = named_icons.get(name, "")
    if not icon_name:
        return ""
    return build_icon_class(icon_name)
