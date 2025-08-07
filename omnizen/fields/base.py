"""
Field module for Omnizen models.
This module defines the base model for Omnizen, which combines Pydantic and contract functionalities.
"""

from typing import Literal, Optional, overload
from pydantic import Field


NameFieldType = Literal["unique", "autoincrement"]


@overload
def NameField(
    name_type: Literal["autoincrement"],
    *,
    autoincrement_prefix: str = "",
    autoincrement_padding: int = 0,
    autoincrement_next_sequence: int = 1,
    **kwargs,
): ...


@overload
def NameField(
    name_type: Optional[Literal["unique"]] = None,
    **kwargs,
): ...


@overload
def NameField(
    name_type: Optional[NameFieldType],
    **kwargs,
): ...


def NameField(
    name_type: Optional[NameFieldType] = None,
    *,
    autoincrement_prefix: str = "",
    autoincrement_padding: int = 0,
    autoincrement_next_sequence: int = 1,
    **kwargs,
):
    if name_type != "autoincrement" and (
        autoincrement_prefix != ""
        or autoincrement_padding != 0
        or autoincrement_next_sequence != 1
    ):
        raise ValueError(
            "autoincrement parameters are only valid for 'autoincrement' name_type"
        )

    existing_schema = kwargs.get("json_schema_extra", {})

    our_schema = {
        "type": name_type,
        "autoincrement_prefix": autoincrement_prefix,
        "autoincrement_padding": autoincrement_padding,
        "autoincrement_next_sequence": autoincrement_next_sequence,
    }

    if callable(existing_schema):
        original_func = existing_schema

        def enhanced_schema(schema, model_type):
            original_func(schema, model_type)
            schema.update(our_schema)

        kwargs["json_schema_extra"] = enhanced_schema
    else:
        kwargs["json_schema_extra"] = existing_schema | our_schema

    return Field(**kwargs)
