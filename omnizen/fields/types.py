"""
Module for creating enum choices.
"""

import enum


class _ChoicesMeta(enum.EnumMeta):
    """
    A metaclass for creating an enum choices.
    """

    @property
    def names(cls):
        return [member.name for member in cls]  # type: ignore

    @property
    def choices(cls):
        return [(member.value, member.label) for member in cls]  # type: ignore

    @property
    def labels(cls):
        return [label for _, label in cls.choices]

    @property
    def values(cls):
        return [value for value, _ in cls.choices]


class Choices(enum.Enum, metaclass=_ChoicesMeta):
    """
    Class for creating enum choices.
    """

    @property
    def value(self):
        if isinstance(self._value_, tuple):
            return self._value_[0]

        return self._value_

    @property
    def label(self):
        if isinstance(self._value_, tuple):
            return self._value_[1]

        return str(self._value_).replace("_", " ").title()
