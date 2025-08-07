"""
Base model for Omnizen models.
"""

from abc import ABC, abstractmethod
from typing import (
    Any,
    Optional,
    TypeVar,
    Generic,
    TypedDict,
)
from pydantic import BaseModel as PydanticBaseModel


T = TypeVar("T", bound="BaseModel")


class BulkResponse(TypedDict):
    """
    Response for bulk operations.
    """

    success: list
    errors: list


class BaseModel(PydanticBaseModel, ABC, Generic[T]):
    """
    Concrete base model for Omnizen models combining Pydantic and contract.
    """

    @abstractmethod
    def save(self) -> None:
        """
        Save the current instance.
        """
        ...

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the current instance.
        """
        ...

    @abstractmethod
    def refresh(self) -> None:
        """
        Refresh the current instance from the data source.
        """
        ...

    @classmethod
    @abstractmethod
    def get(cls, id: Any) -> T:
        """
        Get an instance by its ID.
        """
        ...

    @classmethod
    @abstractmethod
    def all(cls, *args: Any, **kwargs: Any) -> list[T]:
        """
        Get all instances.

        Optional pagination parameters can be implemented.

        By default, all instances are returned.
        """
        ...

    @classmethod
    @abstractmethod
    def search(cls, word: str, *args: Any, **kwargs: Any) -> list[T]:
        """
        Search for instances based on a search term.

        Optional pagination parameters can be implemented.

        By default, all instances are returned.
        """
        ...

    @classmethod
    @abstractmethod
    def filter(cls, query: Any, *args: Any, **kwargs: Any) -> list[T]:
        """
        Filter instances based on a query.

        Optional pagination parameters can be implemented.

        By default, all instances are returned.
        """
        ...

    @classmethod
    @abstractmethod
    def count(cls, *args: Any, **kwargs: Any) -> int:
        """
        Count the number of instances.

        Optional filtering parameters can be implemented.
        """
        ...

    @classmethod
    @abstractmethod
    def bulk_create(
        cls,
        items: list[T],
        fields: Optional[list[str]],
        wait_to_complete: bool,
        sleep: float,
        *args: Any,
        **kwargs: Any,
    ) -> None | BulkResponse:
        """
        Bulk create instances from a list of items.
        """
        ...

    @classmethod
    @abstractmethod
    def bulk_update(
        cls,
        items: list[T],
        fields: Optional[list[str]],
        wait_to_complete: bool,
        sleep: float,
        *args: Any,
        **kwargs: Any,
    ) -> None | BulkResponse:
        """
        Bulk update instances from a list of items.
        """
        ...

    @classmethod
    @abstractmethod
    def bulk_delete(
        cls,
        items: list[T],
        fields: Optional[list[str]],
        wait_to_complete: bool,
        sleep: float,
        *args: Any,
        **kwargs: Any,
    ) -> None | BulkResponse:
        """
        Bulk delete instances from a list of items.
        """
        ...

    @classmethod
    @abstractmethod
    def _format_bulk_response(cls, response: dict) -> BulkResponse:
        """
        Format the bulk response.
        """
        ...

    @classmethod
    @abstractmethod
    def _format_record(cls, record: dict) -> T:
        """
        Format a single record into an instance of the model.
        """
        ...

    @classmethod
    def get_fields_names(cls) -> list[str]:
        """
        Get the field names of the model.
        """
        return [f.title or name for name, f in cls.model_fields.items()]

    @classmethod
    def map_fields_types(cls) -> dict[str, type[Any] | None]:
        """
        Map field names to their types.
        """
        return {name: f.annotation for name, f in cls.model_fields.items()}

    @classmethod
    def map_fields_titles(cls, reverse: bool = False) -> dict[str, str]:
        """
        Map field names to their titles, or titles to field names if reverse is True.
        """
        mapping = {}
        for name, f in cls.model_fields.items():
            title = (
                f.title.strip()
                if getattr(f, "title", None) and isinstance(f.title, str)
                else name
            )
            if reverse:
                mapping[title] = name
            else:
                mapping[name] = title

        return mapping
