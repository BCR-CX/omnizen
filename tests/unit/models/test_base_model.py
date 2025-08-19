"""
Base model for testing purposes.
This class is a concrete implementation of the BaseModel abstract class,
allowing for instantiation in tests.
"""

import pytest
from omnizen.models.base import BaseModel
from omnizen.fields.base import Field


def test_base_model_cannot_instantiate_with_abstract_methods():
    """
    Ensure BaseModel cannot be instantiated if abstract methods are not implemented.
    """

    class TestIncompleteModel(BaseModel):
        pass

    with pytest.raises(TypeError):
        TestIncompleteModel()  # type: ignore


def test_base_model_can_instantiate_when_methods_implemented(concret_base_model):
    """
    Ensure BaseModel can be instantiated when all abstract methods are implemented.
    """

    callable_methods = [
        concret_base_model.save,
        concret_base_model.delete,
        concret_base_model.refresh,
        concret_base_model.get,
        concret_base_model.all,
        concret_base_model.filter,
        concret_base_model.search,
        concret_base_model.count,
        concret_base_model.bulk_create,
        concret_base_model.bulk_update,
        concret_base_model.bulk_delete,
        concret_base_model._format_bulk_response,
        concret_base_model._format_record,
    ]
    for method in callable_methods:
        assert callable(method)


def test_base_model_valid(concret_base_model):
    """
    Ensure BaseModel can be instantiated with valid data.
    """

    class PydanticModel(concret_base_model):
        name: str
        age: int

    model = PydanticModel(name="Test", age=30)
    assert model.name == "Test"
    assert model.age == 30
    assert isinstance(model, BaseModel)


def test_base_model_invalid_model(concret_base_model):
    """
    Ensure BaseModel raises validation errors for invalid data.
    """

    class InvalidPydanticModel(concret_base_model):
        name: str
        age: int

    with pytest.raises(ValueError):
        InvalidPydanticModel(name="Test", age="invalid_age")  # type: ignore


def test_text_fields(concret_base_model):
    """
    Test that TextField can be created with default value and name.
    """

    title = "Sample Text Field"

    class TestTextField(concret_base_model):
        text_field: str = Field(title=title)

    instance = TestTextField(text_field="Test value")
    assert isinstance(instance.text_field, str)
    assert instance.text_field == "Test value"


def test_date_fields(concret_base_model):
    """
    Test that DateField can be created with default value and name.
    """

    from datetime import date

    class TestDateField(concret_base_model):
        date_field: date = Field(default_factory=date.today)

    instance = TestDateField()
    assert isinstance(instance.date_field, date)
    assert instance.date_field == date.today()


def test_decimal_fields(concret_base_model):
    """
    Test that DecimalField can be created with default value and name.
    """

    from decimal import Decimal

    class TestDecimalField(concret_base_model):
        decimal_field: Decimal = Field(default=Decimal("0.00"))

    instance = TestDecimalField()
    assert isinstance(instance.decimal_field, Decimal)
    assert instance.decimal_field == Decimal("0.00")


def test_get_fields_names(concret_base_model):
    """
    Test that get_fields_names returns the correct field names.
    """

    class TestFieldsNamesModel(concret_base_model):
        field_one: str = Field(title="Field One")
        field_two: int = Field()

    field_names = TestFieldsNamesModel.get_fields_names()
    assert field_names == ["Field One", "field_two"]


def test_map_fields_types(concret_base_model):
    """
    Test that map_fields_types returns the correct field types.
    """

    class TestMapFieldsTypesModel(concret_base_model):
        field_one: str = Field(title="Field One")
        field_two: int = Field()

    field_types = TestMapFieldsTypesModel.map_fields_types()
    assert field_types == {"field_one": str, "field_two": int}


def test_map_fields_titles(concret_base_model):
    """
    Test that map_fields_titles returns the correct field titles.
    """

    class TestMapFieldsTitlesModel(concret_base_model):
        field_one: str = Field(title="Field One")
        field_two: int = Field()

    field_titles = TestMapFieldsTitlesModel.map_fields_titles()
    assert field_titles == {
        "field_one": "Field One",
        "field_two": "field_two",
    }


def test_map_fields_titles_reverse(concret_base_model):
    """
    Test that map_fields_titles with reverse=True returns the correct field names.
    """

    class TestMapFieldsTitlesModel(concret_base_model):
        field_one: str = Field(title="Field One")
        field_two: int = Field()

    field_titles = TestMapFieldsTitlesModel.map_fields_titles(reverse=True)
    assert field_titles == {
        "Field One": "field_one",
        "field_two": "field_two",
    }
