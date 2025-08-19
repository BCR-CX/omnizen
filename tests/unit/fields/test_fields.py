"""
Tests for the field module.
This module tests the NameField function and its various configurations.
"""

from datetime import datetime, date
import pytest
from pydantic import BaseModel, Field
from unittest.mock import Mock

from omnizen.fields.base import NameField
from omnizen.fields.types import Choices


def test_name_field_default_behavior():
    """
    Test NameField with default parameters.
    """

    field = NameField()

    expected_schema = {
        "type": None,
        "autoincrement_prefix": "",
        "autoincrement_padding": 0,
        "autoincrement_next_sequence": 1,
    }
    assert field.json_schema_extra == expected_schema


def test_name_field_unique_type():
    """
    Test NameField with unique type.
    """

    field = NameField("unique")

    expected_schema = {
        "type": "unique",
        "autoincrement_prefix": "",
        "autoincrement_padding": 0,
        "autoincrement_next_sequence": 1,
    }
    assert field.json_schema_extra == expected_schema


def test_name_field_autoincrement_type():
    """
    Test NameField with autoincrement type and custom parameters.
    """

    field = NameField(
        "autoincrement",
        autoincrement_prefix="TEST_",
        autoincrement_padding=5,
        autoincrement_next_sequence=100,
    )

    expected_schema = {
        "type": "autoincrement",
        "autoincrement_prefix": "TEST_",
        "autoincrement_padding": 5,
        "autoincrement_next_sequence": 100,
    }
    assert field.json_schema_extra == expected_schema


def test_name_field_invalid_autoincrement_params():
    """
    Test that autoincrement parameters with non-autoincrement type raise ValueError.
    """

    with pytest.raises(
        ValueError,
        match="autoincrement parameters are only valid for 'autoincrement' name_type",
    ):
        NameField("unique", autoincrement_prefix="TEST_")


def test_name_field_with_existing_dict_schema():
    """
    Test NameField with existing json_schema_extra as dict.
    """

    existing_schema = {"custom_field": "custom_value"}
    field = NameField("unique", json_schema_extra=existing_schema)

    expected_schema = {
        "custom_field": "custom_value",
        "type": "unique",
        "autoincrement_prefix": "",
        "autoincrement_padding": 0,
        "autoincrement_next_sequence": 1,
    }
    assert field.json_schema_extra == expected_schema


def test_name_field_with_existing_callable_schema():
    """
    Test NameField with existing json_schema_extra as callable.
    """

    original_func = Mock()
    field = NameField(
        "autoincrement",
        autoincrement_prefix="AUTO_",
        json_schema_extra=original_func,
    )

    test_schema = {}
    test_model_type = Mock()
    field.json_schema_extra(test_schema, test_model_type)

    original_func.assert_called_once_with(test_schema, test_model_type)
    assert test_schema["type"] == "autoincrement"
    assert test_schema["autoincrement_prefix"] == "AUTO_"


def test_name_field_integration_with_pydantic_model():
    """
    Test NameField integration with a Pydantic model.
    """

    class TestModel(BaseModel):
        unique_name: str = NameField(name_type="unique")

    model = TestModel(unique_name="test")
    assert model.unique_name == "test"

    schema = TestModel.model_json_schema()
    assert schema["properties"]["unique_name"].get("type") == "unique"


def test_choices_class(color_choices, color_choice_with_labels):
    """
    Test Choices enum functionality.
    """

    assert color_choices.values == ["red", "green", "blue"]
    assert color_choices.labels == ["Red", "Green", "Blue"]
    assert color_choices.choices == [
        ("red", "Red"),
        ("green", "Green"),
        ("blue", "Blue"),
    ]
    assert color_choices.names == ["RED", "GREEN", "BLUE"]

    assert color_choice_with_labels.values == ["red", "green", "blue"]
    assert color_choice_with_labels.labels == ["Red Color", "Green Color", "Blue Color"]
    assert color_choice_with_labels.choices == [
        ("red", "Red Color"),
        ("green", "Green Color"),
        ("blue", "Blue Color"),
    ]
    assert color_choice_with_labels.names == ["RED", "GREEN", "BLUE"]


def test_choices_instance(color_choices, color_choice_with_labels):
    """
    Test Choices enum labels.
    """

    color = color_choices.RED
    assert color.value == "red"
    assert color.label == "Red"

    color_with_label = color_choice_with_labels.RED
    assert color_with_label.value == "red"
    assert color_with_label.label == "Red Color"


def test_choices_pydantic_base_model():
    """
    Test Choices with Pydantic BaseModel.
    """

    class ColorChoices(Choices):
        RED = "red", "Red Color"
        GREEN = "green", "Green Color"
        BLUE = "blue", "Blue Color"

    class TestModel(BaseModel):
        color: ColorChoices = Field(default=ColorChoices.RED)

    model = TestModel()
    assert model.color == ColorChoices.RED
    assert model.color.value == "red"
    assert model.color.label == "Red Color"
    assert model.model_dump_json() == '{"color":"red"}'


def test_list_choices_pydantic_base_model():
    """
    Test ListChoices with Pydantic BaseModel.
    """

    class ColorChoices(Choices):
        RED = "red", "Red Color"
        GREEN = "green", "Green Color"
        BLUE = "blue", "Blue Color"

    class TestModel(BaseModel):
        colors: list[ColorChoices] = Field(default_factory=lambda: [ColorChoices.RED])

    model = TestModel()
    assert model.colors == [ColorChoices.RED]
    assert model.colors[0].value == "red"
    assert model.colors[0].label == "Red Color"
    assert model.model_dump_json() == '{"colors":["red"]}'


def test_fields_conversion():
    """
    Test the conversion of fields.
    """

    class ColorChoices(Choices):
        RED = "red", "Red Color"
        GREEN = "green", "Green Color"
        BLUE = "blue", "Blue Color"

    class TestModel(BaseModel):
        date_field: date
        datetime_field: datetime
        choice_field: ColorChoices

    model = TestModel(
        date_field="2023-10-01",  # type: ignore
        datetime_field="2023-10-01T12:00:00",  # type: ignore
        choice_field="green",  # type: ignore
    )
    assert model.date_field == date(2023, 10, 1)
    assert model.datetime_field == datetime(2023, 10, 1, 12, 0)
    assert model.choice_field == ColorChoices.GREEN
