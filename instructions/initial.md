# Abstract
I Django I want to display Django model instance properties with custom templates.
The properties are grouped. Each group has a title, an optional description and an optional icon.

# Configuration
The configuration for the display takes into account that the properties to be displayed can be nested.
That means the configuration of the display can access instance's subobjects and also their properties and their subobjects.
To define nested properties, use the dot-dot notation, i.e. `info__update_dt` which means `info.update_dt` 
whereas `info` is the property ob the instance to display.

## Configuration Example

for the following modelstructure:

```python
from django.db import models

User = get_user_model()

class Info(models.Model):
    text = models.TextField()
    is_public = models.BooleanField()
    create_dt = models.DateTimeField()
    update_dt = models.DateTimeField()

class Report(models.Model):
    title = models.CharField(max_length=255)
    access_users = models.ManyToManyField(User)
    info = models.OneToOneField(Info)
    owner = models.ForeignKey(User)
```

The follwoing configuration will display the properties of the `Report` instance:

```python
property_display = [
        {
            "title": _("Report"),
            "description": _("Report description"),
            "properties": [
                "title",
                "owner",
                "owner__is_staff"
            ]
        },
        {
            "title": _("Info"),
            "properties": [
                # get a custom title
                x("info__text", title="custom title for text", detail="custom detail"),
                "info__is_public",
                "info__owner__get_full_name",
                x("info__owner", template="foo/bar/custom-user-template.html"),
                x("info__create_dt", type="timestamp"),
            ]
        },
        {
            "title": _("access_users"),
            "properties": [
                # this will render the full name of each user
                "access_users__get_full_name",
            ]
        }
]
```


## Parsing

The structure needs to be parsed into an object structure (pydantic?)

The simplest default is defined just by a string.

Detailed properties work via constructor `x` which is just a placeholder name for the constructor for now.

Each property is inspected via the django model field:
- label:
  - defaults to the field name
  - if there is a verbose_name, use it
  - or defined in the configuration
- detail:  
  - used from the field's help_text
  - or defined in the configuration
- type:
  - from the field's model type
- template
  - usually defined by type
  - can be overwritten in the configuration

# Rendering

the following template folder structure is used:
- layout
  - types
    - char.html 
    - text.html
    - boolean.html (renders a checkbox or icon)
    - date.html
    - datetime.html
    - timestamp.html
  - group.html

  For the layout there are drafts
- [object-detail-drafts-1.html](../templates/object-detail-drafts-1.html)
- [object-detail-drafts-2.html](../templates/object-detail-drafts-2.html)

