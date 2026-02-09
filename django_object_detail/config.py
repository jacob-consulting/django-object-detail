from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, field_validator


class LinkConfig(BaseModel):
    """Configuration for linking a property value to a URL."""

    url: str
    args: Optional[list[str]] = None
    kwargs: Optional[dict[str, str]] = None


class PropertyConfig(BaseModel):
    """Configuration for a single property to display."""

    path: str
    title: Optional[str] = None
    detail: Optional[str] = None
    type: Optional[str] = None
    template: Optional[str] = None
    link: Optional[LinkConfig] = None

    @field_validator("link", mode="before")
    @classmethod
    def normalize_link(cls, v):
        if isinstance(v, str):
            return LinkConfig(url=v)
        return v


class PropertyGroupConfig(BaseModel):
    """Configuration for a group of properties."""

    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    properties: list[PropertyConfig]

    @field_validator("properties", mode="before")
    @classmethod
    def normalize_properties(cls, v: list) -> list:
        result = []
        for item in v:
            if isinstance(item, str):
                result.append(PropertyConfig(path=item))
            elif isinstance(item, PropertyConfig):
                result.append(item)
            elif isinstance(item, dict):
                result.append(PropertyConfig(**item))
            else:
                raise ValueError(f"Invalid property config: {item!r}")
        return result


def x(path: str, **kwargs) -> PropertyConfig:
    """Convenience constructor for PropertyConfig."""
    return PropertyConfig(path=path, **kwargs)


def parse_property_display(raw: list[dict]) -> list[PropertyGroupConfig]:
    """Parse a raw property_display list into PropertyGroupConfig objects."""
    return [PropertyGroupConfig(**group) for group in raw]
