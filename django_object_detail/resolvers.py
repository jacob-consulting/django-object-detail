from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from django.core.exceptions import FieldDoesNotExist
from django.db import models

from django_object_detail.config import PropertyConfig, PropertyGroupConfig

FIELD_TYPE_MAP: dict[type[models.Field], str] = {
    models.CharField: "char",
    models.SlugField: "char",
    models.URLField: "char",
    models.EmailField: "char",
    models.TextField: "text",
    models.BooleanField: "boolean",
    models.NullBooleanField: "boolean",
    models.DateTimeField: "datetime",
    models.DateField: "date",
    models.IntegerField: "integer",
    models.SmallIntegerField: "integer",
    models.BigIntegerField: "integer",
    models.PositiveIntegerField: "integer",
    models.PositiveSmallIntegerField: "integer",
    models.PositiveBigIntegerField: "integer",
    models.AutoField: "integer",
    models.BigAutoField: "integer",
    models.SmallAutoField: "integer",
    models.FloatField: "float",
    models.DecimalField: "float",
    models.ForeignKey: "foreignkey",
    models.OneToOneField: "foreignkey",
    models.ManyToManyField: "manytomany",
    models.ManyToManyRel: "manytomany",
    models.ManyToOneRel: "manytomany",
}


@dataclass
class ResolvedProperty:
    path: str
    label: str
    value: Any
    detail: str | None = None
    type: str = "default"
    template: str | None = None
    is_many: bool = False


@dataclass
class ResolvedGroup:
    title: str
    description: str | None = None
    icon: str | None = None
    properties: list[ResolvedProperty] = field(default_factory=list)


def _get_field_type(field_obj: models.Field) -> str:
    """Map a Django field instance to a type string."""
    for field_class, type_name in FIELD_TYPE_MAP.items():
        if isinstance(field_obj, field_class):
            return type_name
    return "default"


def resolve_property(instance: models.Model, config: PropertyConfig) -> ResolvedProperty:
    """Resolve a PropertyConfig against a model instance.

    Walks the _meta chain for metadata (label, detail, type)
    and the instance chain for the runtime value.
    """
    segments = config.path.split("__")

    # Walk _meta to gather field metadata
    label = config.path
    detail = None
    field_type = "default"
    is_many = False
    current_model = type(instance)

    for i, segment in enumerate(segments):
        try:
            field_obj = current_model._meta.get_field(segment)
        except FieldDoesNotExist:
            # Could be a method/property — no further metadata to extract
            label = segment.replace("_", " ").title()
            break
        else:
            # Extract metadata from the field
            verbose = getattr(field_obj, "verbose_name", None)
            if verbose:
                label = str(verbose)
            else:
                label = segment.replace("_", " ").title()

            help_text = getattr(field_obj, "help_text", None)
            if help_text:
                detail = str(help_text)

            field_type = _get_field_type(field_obj)

            # Navigate into related models for FK/O2O
            if isinstance(field_obj, (models.ForeignKey, models.OneToOneField)):
                current_model = field_obj.related_model
            elif isinstance(field_obj, models.ManyToManyField):
                is_many = True
                current_model = field_obj.related_model
            elif isinstance(field_obj, (models.ManyToManyRel, models.ManyToOneRel)):
                is_many = True
                current_model = field_obj.related_model

    # Apply config overrides
    if config.title:
        label = config.title
    if config.detail is not None:
        detail = config.detail
    if config.type:
        field_type = config.type

    # Resolve the runtime value
    value = _resolve_value(instance, segments, is_many)

    return ResolvedProperty(
        path=config.path,
        label=label,
        value=value,
        detail=detail or None,
        type=field_type,
        template=config.template,
        is_many=is_many,
    )


def _resolve_value(instance: models.Model, segments: list[str], is_many: bool) -> Any:
    """Walk the instance to resolve the runtime value.

    Tracks a list of current objects to handle M2M fan-out.
    """
    current: list[Any] = [instance]

    for segment in segments:
        next_objects: list[Any] = []
        for obj in current:
            if obj is None:
                next_objects.append(None)
                continue

            attr = getattr(obj, segment, None)

            # Check if it's a manager (M2M or reverse FK)
            if hasattr(attr, "all"):
                next_objects.extend(attr.all())
            elif callable(attr):
                next_objects.append(attr())
            else:
                next_objects.append(attr)

        current = next_objects

    if is_many:
        return current
    elif len(current) == 1:
        return current[0]
    else:
        return current


def resolve_group(instance: models.Model, config: PropertyGroupConfig) -> ResolvedGroup:
    """Resolve all properties in a group."""
    return ResolvedGroup(
        title=config.title,
        description=config.description,
        icon=config.icon,
        properties=[resolve_property(instance, prop) for prop in config.properties],
    )


def resolve_all(
    instance: models.Model, groups: list[PropertyGroupConfig]
) -> list[ResolvedGroup]:
    """Resolve all groups for an instance."""
    return [resolve_group(instance, group) for group in groups]
