# Settings Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `OBJECT_DETAIL_TEMPLATE_PACK_LAYOUT` | `"split-card"` | Which layout pack to use for group/property structure |
| `OBJECT_DETAIL_TEMPLATE_PACK_TYPES` | `"default"` | Which type template pack to use for value rendering |
| `OBJECT_DETAIL_ICONS_LIBRARY` | `"bootstrap"` | Icon library to use for defaults. Supported: `"bootstrap"`, `"fontawesome"` |
| `OBJECT_DETAIL_ICONS_CLASS` | per library | Base CSS class (`"bi"` for Bootstrap, `"fa"` for Font Awesome) |
| `OBJECT_DETAIL_ICONS_TYPE` | per library | Icon type/family. `None` for Bootstrap, `"regular"` for Font Awesome |
| `OBJECT_DETAIL_ICONS_PREFIX` | per library | Icon name prefix (`"bi"` for Bootstrap, `"fa"` for Font Awesome) |
| `OBJECT_DETAIL_NAMED_ICONS` | per library | Dict mapping named icons to icon names (see below) |

## Icon libraries

By default, Bootstrap Icons are used. To switch to Font Awesome:

```python
OBJECT_DETAIL_ICONS_LIBRARY = "fontawesome"
OBJECT_DETAIL_ICONS_TYPE = "solid"  # included in the free tier
```

The icon CSS class is built as `{CLASS}[-{TYPE}] {PREFIX}-{ICON_NAME}`:

- Bootstrap: `bi bi-check-circle-fill`
- Font Awesome (solid): `fa-solid fa-circle-check`

### Named icons

Named icons are used internally in templates for special purposes (e.g. boolean indicators). Each library provides defaults:

| Name | Bootstrap | Font Awesome |
|------|-----------|--------------|
| `boolean-true` | `check-circle-fill` | `circle-check` |
| `boolean-false` | `x-circle-fill` | `circle-xmark` |
| `property-detail` | `info-circle` | `circle-info` |
| `text-icon` | `journal-text` | `file-lines` |

Override individual named icons via `OBJECT_DETAIL_NAMED_ICONS`:

```python
OBJECT_DETAIL_NAMED_ICONS = {
    "boolean-true": "thumbs-up",
    "boolean-false": "thumbs-down",
    "property-detail": "circle-info",
    "text-icon": "file-lines",
}
```
