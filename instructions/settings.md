# Introduction

- I want additional configuration for the library in the settings
- This configuration should be available in all templates that are rendered
- Settings must have default values
- Must be easy to extend
- as a first step introduce: 
  - `PROPERTY_TEXT_NEWLINE` which defaults to the filter `linebreaksbr`
  - another option for `PROPERTY_TEXT_NEWLINE` could be `linebreaks`
  - update the template `django_object_detail/templates/django_object_detail/types/default/text.html` using this option

# Evaluate

There are two options
- Use a context processor to add the configuration to the context
- add the configuration to the template rendering code, i.e., in the template tag 

Evaluate both options and let me choose.

# Implementation
- update selected implementation
- update tests
- update documentation
- update example
