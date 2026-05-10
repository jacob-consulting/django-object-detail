# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Package Does

`django-object-detail` is a Django library for displaying model instances in grouped, Bootstrap 5 layouts. It uses a declarative DSL (`property_display`) on class-based views to configure which fields to show, how to resolve them (including FK/M2M traversal), and how to render them (badges, links, icons, layout packs).

## Commands

### Testing

```bash
# Run full test matrix via nox (Python 3.12/3.13/3.14 × Django 4.2/5.2/6.0)
nox

# Run a specific session
nox -s "tests-3.12(django='4.2')"

# Run tests directly with pytest (after pip install -e ".[dev]")
pytest
pytest tests/test_resolvers.py          # single file
pytest tests/test_resolvers.py::TestFoo # single test class
pytest --cov=django_object_detail       # with coverage
```

### Development Setup

```bash
pip install -e ".[dev]"
```

### Run the Example App

```bash
cd example
pip install django django-bootstrap5 -e ..
python manage.py migrate
python manage.py loaddata catalog
python manage.py runserver
```

### Build & Release

```bash
python -m build
bump-my-version bump patch   # or minor / major
```

## Architecture

### Data Flow

1. A view sets `property_display` — a list of group dicts or `PropertyGroupConfig` objects.
2. `ObjectDetailMixin.get_context_data()` (in `views.py`) parses that config and calls `resolve_all()`.
3. `resolvers.py` walks Django's `_meta` API per field to extract `verbose_name`, `help_text`, and field type, then reads the value from the instance. Dotted paths like `"publisher__address__city"` traverse FK/O2O chains.
4. Badges and links are evaluated and attached to `ResolvedProperty` dataclasses.
5. `ResolvedGroup` and `ResolvedProperty` objects are passed to templates.
6. Template tags in `templatetags/object_detail.py` select the correct layout and type sub-templates and render everything.

### Key Modules

| File | Role |
|------|------|
| `config.py` | Pydantic models (`PropertyConfig`, `PropertyGroupConfig`, `BadgeConfig`, `LinkConfig`) + the `x()` convenience helper |
| `resolvers.py` | Field metadata extraction and value resolution; handles all relation types |
| `views.py` | `ObjectDetailMixin` — the only mixin users apply to their `DetailView` |
| `conf.py` | Settings access for icon library, named icons, layout/type template packs |
| `templatetags/object_detail.py` | Template tags: `render_object_detail`, `render_property_value`, `icon_class` |

### Configuration DSL

Properties can be plain strings (field name) or `x()` calls:

```python
property_display = [
    {
        "title": "Group Title",
        "icon": "book",
        "properties": [
            "field_name",                                        # plain field
            x("price", badge=BadgeConfig(color_fn=…)),          # with badge
            x("publisher", link="publisher-detail"),             # with link
            x("publisher__address__city", title="City"),         # FK traversal
            "view_computed_summary",                             # view method
        ],
    },
]
```

View methods named in `property_display` are called with the instance as the argument.

### Templates

Seven layout packs live under `django_object_detail/templates/django_object_detail/`:
- `split-card/` (default), `accordion/`, `tabs-vertical/`, `card-rows/`, `striped-rows/`, `list-group-3col/`, `table-inline/`

Each layout pack contains a `group.html` and defers per-field rendering to type templates under `types/default/` (e.g., `boolean.html`, `date.html`, `badge.html`).

### Supported Relation Types

`resolvers.py` handles: `ForeignKey`, `OneToOneField`, `ManyToManyField`, `OneToOneRel`, `ManyToOneRel`, `ManyToManyRel`. Dotted-path lookup chains through multiple hops.

### Settings (django_object_detail in Django settings)

| Key | Purpose |
|-----|---------|
| `ICONS_LIBRARY` | `"bootstrap-icons"` or `"font-awesome"` |
| `ICONS` | Dict mapping named icons to icon names |
| `LAYOUT_PACK` | Default layout pack name |
| `TYPE_PACK` | Default type template pack name |