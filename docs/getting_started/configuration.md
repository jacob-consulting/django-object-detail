# Configuration

## Property Paths

Properties are referenced by field name. Use `__` to traverse relationships:

```python
"properties": [
    "title",                    # simple field
    "author__name",             # FK traversal
    "author__country__code",    # multi-hop FK
    "tags",                     # M2M (renders all related objects)
    "get_absolute_url",         # method or property
]
```

## The `x()` Helper

For more control over individual properties, use the `x()` shorthand to build a `PropertyConfig`:

```python
from django_object_detail import x

"properties": [
    "title",
    x("author__name", title="Writer"),
    x("published_date", detail="When the book was first published"),
    x("rating", type="integer"),
    x("notes", template="myapp/custom_notes.html"),
]
```

| Parameter  | Description |
|------------|-------------|
| `path`     | Field name or `__`-separated path (required) |
| `title`    | Override the auto-derived label |
| `detail`   | Help text shown below the value |
| `type`     | Override the auto-detected type (e.g. `"date"`, `"boolean"`) |
| `template` | Path to a custom template for rendering the value |
| `link`     | `LinkConfig` or URL name string (see [Links](links.md)) |
| `badge`    | `BadgeConfig` or color string (see [Badges](badges.md)) |

## Groups

Each entry in `property_display` is a group with a title and a list of properties:

```python
property_display = [
    {
        "title": "Basic Info",
        "description": "Core book metadata",
        "icon": "bi bi-book",
        "properties": [
            "title",
            "author__name",
            x("isbn", detail="International Standard Book Number"),
        ],
    },
]
```

| Parameter     | Description |
|---------------|-------------|
| `title`       | Group heading (required) |
| `description` | Subtitle or help text |
| `icon`        | CSS class for an icon (e.g. Bootstrap Icons) |
| `properties`  | List of strings, dicts, or `PropertyConfig` objects |

Properties can be mixed freely — plain strings, dicts with `PropertyConfig` fields, or `x()` / `PropertyConfig` instances.
