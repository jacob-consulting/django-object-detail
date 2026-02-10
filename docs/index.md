# Django Object Detail

Display Django model instances in grouped, Bootstrap 5 layouts with a declarative configuration.

Define which fields to show, how to group them, and pick a layout — `django-object-detail` handles type detection, value resolution (including FK/M2M traversal), and rendering.

## Installation

```bash
pip install django-object-detail
```

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django_object_detail",
]
```

## Quick Start

Use the mixin in your view:

```python
from django.views.generic import DetailView
from django_object_detail.views import ObjectDetailMixin

class BookDetailView(ObjectDetailMixin, DetailView):
    model = Book
    property_display = [
        {
            "title": "Basic Info",
            "properties": ["title", "author", "isbn"],
        },
        {
            "title": "Details",
            "properties": ["published_date", "page_count", "is_available"],
        },
    ]
```

Render it in your template:

```html
{% load object_detail %}

{% render_object_detail object object_detail_groups %}
```

That's it — fields are auto-detected, labels are derived from `verbose_name`, and the default `split-card` layout is applied.

## Next Steps

- [Configuration](getting_started/configuration.md) — property paths, the `x()` helper, and groups
- [Links](getting_started/links.md) — make property values clickable
- [Badges](getting_started/badges.md) — render values as Bootstrap badges
- [Layout Packs](getting_started/layout_packs.md) — choose from 7 built-in layouts
- [Example Application](getting_started/example.md) — run the demo bookshop app
