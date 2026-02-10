from django.conf import settings


def get_layout_pack():
    return getattr(settings, "OBJECT_DETAIL_TEMPLATE_PACK_LAYOUT", "split-card")


def get_types_pack():
    return getattr(settings, "OBJECT_DETAIL_TEMPLATE_PACK_TYPES", "default")
