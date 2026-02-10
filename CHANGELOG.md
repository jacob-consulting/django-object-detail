# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.4] - 2026-02-10

### Added
- Initial public release
- Declarative configuration for displaying Django model instance properties in groups
- Pydantic v2-based configuration with `PropertyConfig`, `PropertyGroupConfig`, and `x()` shorthand
- Automatic field type detection with `FIELD_TYPE_MAP` (text, number, boolean, date, datetime, etc.)
- FK and M2M relationship traversal for nested property resolution
- `ObjectDetailMixin` view mixin for Django class-based views
- Template tags: `render_object_detail`, `render_group`, `render_property`, `render_property_value`
- Bootstrap 5 layouts: split card (default), accordion, and vertical tabs
- Per-type template rendering via `types/` subdirectory
- Badge and link support on properties
- Support for Django 4.2, 5.2, and 6.0
- Support for Python 3.12 and 3.13

[0.1.4]: https://github.com/jacob-consulting/django-object-detail/releases/tag/v0.1.4
