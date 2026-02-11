# Introduction
Currently, the project uses bootstrap icons.
The module `django-object-detail` should also implement the font awesome icons
and be open to any other icon library in the future.

# Bootstrap vs Font Awesome
Bootstrap icons use the class `bi` and the icon class itself starts with `bi-<name>` where name is the icon name.

Font Awesome uses the class `fa-<type>` and the icon class itself starts with `fa-<name>` where name is the icon name.
Font Awesome types, sometimes called families, are: 
- solid
- regular
- light
- thin
- duotone
- brands

# Implementation

## Settings
Add the following to the settings.py file:
- OBJECT_DETAIL_ICONS_LIBRARY: used to choose defaults
- OBJECT_DETAIL_ICONS_CLASS: the basic class depending on the library 
- OBJECT_DETAIL_ICONS_TYPE: the icon type, only for Font Awesome icons
- OBJECT_DETAIL_ICONS_PREFIX: the prefix for the icon class, basically the same as OBJECT_DETAIL_ICONS_CLASS, but to be flexible for other icon libraries.

So a clas will be formatted like this:

```html
<i class="{{ OBJECT_DETAIL_ICONS_CLASS }}[-{{ OBJECT_DETAIL_ICONS_TYPE }}] {{ OBJECT_DETAIL_ICONS_PREFIX }}-{{ ICON_NAME }}"></i>
```
> Note: OBJECT_DETAIL_ICONS_TYPE is optional, depending on the library.

For Bootstrap icons the configuration should be:
```python
OBJECT_DETAIL_ICONS_LIBRARY = "bootstrap"
OBJECT_DETAIL_ICONS_CLASS = "bs"
OBJECT_DETAIL_ICONS_TYPE = None
OBJECT_DETAIL_ICONS_PREFIX = "bs"
```

For Font Awesome icons the configuration should be:
```python
OBJECT_DETAIL_ICONS_LIBRARY = "fontawesome"
OBJECT_DETAIL_ICONS_CLASS = "fa"
OBJECT_DETAIL_ICONS_TYPE = "regular"
OBJECT_DETAIL_ICONS_PREFIX = "fa"
```

Default should be set to bootstrap.

## Filter
Create a filter called `icon_class` in `object_detail/templatetags/object_detail_tags.py`

## Named Icons

In the templates there are icons used in some cases for special purposes, i.e., boolean values.

The named icons are defined in the settings by a dictionary [name,class_name]:

```python
OBJECT_DETAIL_NAMED_ICONS = {...}
```

Depending on the library, defaults are provided for each library, if the user does not define `OBJECT_DETAIL_NAMED_ICONS`.

```python
OBJECT_DETAIL_NAMED_ICONS_DEFAULTS_BOOTSTRAP = {
    "boolean-true": "check-circle-fill",
    "boolean-false": "circle-fill",
    "property-detail": "info-circle",
    "text-icon": "journal-text",
}

OBJECT_DETAIL_NAMED_ICONS_DEFAULTS_FONTAWESOME = {
    "boolean-true": "solid",
    "boolean-false": "circle-xmark",
    "property-detail": "circle-info",
    "text-icon": "file-lines",
}
```

Add and use a filter called `named_icon_class` for this to be used like this:

```html
<i class='"boolean-true"|named_icon_class'></i>
```

Update all existing usages (currently bootstrap) of these named icons to use the new filter. 

