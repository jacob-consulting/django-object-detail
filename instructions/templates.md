# Introduction
I want to make the templating more flexible and customizable.
So I want to introduce template packs sets for groups and properties.

# Folder Structure

Currently, in `templates/django_object_actions` are the templates for
  - group.html
  - object detail.html 
  - property.html
  - types (folder with one template for each type)

The types don't vary so much, so I decided to have to template pack configurations one for types and one for packs.

Keep `templates/object_detail.html` in place.

Move `templates/django_object_actions/types` to `templates/django_object_actions/types/default`
and the files `templates/group.html`, `templates/property.html` to `templates/django_object_actions/layouts/default`.

As you can see, these locations define the template packs for types and layout.

# Implementation

Add a configuration via DJANGO_SETTINGS_MODULE

```python
OBJECT_DETAIL_TEMPLATE_PACK_TYPES = "default"
OBJECT_DETAIL_TEMPLATE_PACK_LAYOUT = "default"
```

Make the templates use the template pack configuration when rendering.

# Templates pack

Here are the layouts 
- [object-detail-drafts-1.html](../templates/object-detail-drafts-1.html)
- [object-detail-drafts-2.html](../templates/object-detail-drafts-2.html)

The one currently implemented is "Object Detail Layouts — Part 2 / 5 Split Card — Left Header / Right Properties".
Rename it to a reasonable name and use this name as default for the configuration.

Add the following template packs to the template layouts directory, give the template layout packs a meaningful but short name for the folder.

- Object Detail Layouts / 1 Card Layout — Horizontal Rows with Tooltip Annotations
- Object Detail Layouts / 2 Table Layout — Inline Annotations Below Values
- Object Detail Layouts / 4 List Group Layout — Three-Column with Dedicated Annotation Column
- Object Detail Layouts — Part 2 / 6 Accordion — Collapsible Groups with Summary Badges
- Object Detail Layouts — Part 2 / 7 Tabbed Groups — Vertical Tabs with Definition List
- Object Detail Layouts — Part 2 / 8 Striped Rows — Compact Grouped Sections with Alternating Rows

Currently, there are no additional template packs for types.

