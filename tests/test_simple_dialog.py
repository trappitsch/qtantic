"""Tests for the SimpleDialog model and returner."""

from datetime import date, datetime, time
from typing import Literal

from pydantic import BaseModel, Field
from qtpy import QtWidgets

from qtantic import SimpleDialogModel, simple_dialog


def test_simple_dialog_model_accept(qtbot):
    """Test the SimpleDialog model."""

    class Entries(BaseModel):
        value_a: str = Field(
            default="A", title="This is value A", description="Tooltip value A"
        )
        value_b: int = Field(default=42, description="Tooltip value B")
        value_c: float = Field(
            default=3.14, title="Approx. pi", description="Tooltip value C"
        )
        value_d: bool = Field(default=True, description="Tooltip value D")
        value_e: Literal["A", "B", "C"] = Field(
            default="B", description="Tooltip value E", title="Select one from DropDown"
        )
        value_f: date = Field(
            default=date(2021, 1, 1),
            description="User date",
            minimum=date(2020, 1, 1),
            maximum=date(2021, 12, 31),
        )
        value_g: time = Field(
            default=time(12, 0),
            description="Noon",
            minimum=time(9, 0),
            maximum=time(17, 0),
        )
        value_h: datetime = Field(
            default=datetime(2021, 12, 15, 15, 30),
            description="Current date and time",
            minimum=datetime(2021, 1, 1),
            maximum=datetime(2021, 12, 31, 11, 59, 59),
        )
        value_i: str = Field(
            default="",
            description="Enter your address",
            json_scheme_extra={"widget": "QTextEdit"},
        )

    model = SimpleDialogModel(title="Test Dialog", entries=Entries())

    widget = simple_dialog(model)
    qtbot.addWidget(widget)

    assert widget.windowTitle() == "Test Dialog"
    assert widget.entries == model.entries

    assert widget.widgets["value_a"].toolTip() == "Tooltip value A"
    assert widget.widgets["value_b"].toolTip() == "Tooltip value B"
    assert widget.widgets["value_c"].toolTip() == "Tooltip value C"
    assert widget.widgets["value_d"].toolTip() == "Tooltip value D"
    assert widget.widgets["value_e"].toolTip() == "Tooltip value E"
    assert isinstance(widget.widgets["value_i"], QtWidgets.QTextEdit)

    widget.widgets["value_a"].setText("BBB")
    widget.widgets["value_b"].setValue(43)
    widget.widgets["value_c"].setValue(3.15)
    widget.widgets["value_d"].setChecked(False)
    widget.widgets["value_e"].setCurrentIndex(0)
    widget.widgets["value_f"].setDate(date(2021, 12, 31))
    widget.widgets["value_g"].setTime(time(17, 0))
    widget.widgets["value_h"].setDateTime(datetime(2021, 12, 31, 11, 59, 59))

    widget.accept()

    assert widget.entries.value_a == "BBB"
    assert widget.entries.value_b == 43
    assert widget.entries.value_c == 3.15
    assert widget.entries.value_d is False
    assert widget.entries.value_e == "A"
    assert widget.entries.value_f == date(2021, 12, 31)
    assert widget.entries.value_g == time(17, 0)
    assert widget.entries.value_h == datetime(2021, 12, 31, 11, 59, 59)


def test_simple_dialog_model_reject(qtbot):
    """Test the SimpleDialog model - no change on rejection."""

    class Entries(BaseModel):
        value_a: str = Field(
            default="A", title="This is value A", description="Tooltip value A"
        )
        value_b: int = Field(default=42)
        value_c: float = Field(default=3.14, title="Approx. pi")

    model = SimpleDialogModel(title="Test Dialog", entries=Entries())

    widget = simple_dialog(model)
    qtbot.addWidget(widget)

    assert widget.windowTitle() == "Test Dialog"
    assert widget.entries == model.entries

    widget.widgets["value_a"].setText("BBB")
    widget.widgets["value_b"].setValue(43)
    widget.widgets["value_c"].setValue(3.15)
    widget.reject()

    assert widget.entries == model.entries


def test_simple_dialog_model_restore_defaults(qtbot):
    """Restore defaults for values that have them."""

    class Entries(BaseModel):
        value_a: str = Field(
            default="A", title="This is value A", description="Tooltip value A"
        )
        value_b: int = Field(default=42, description="Tooltip value B")
        value_c: float = Field(
            default=3.14, title="Approx. pi", description="Tooltip value C"
        )
        value_d: str = Field(title="This is value D", description="Tooltip value D", json_scheme_extra={"widget": "QTextEdit"})
        value_e: Literal["A", "B", "C"] = Field("A")
        value_f: date = Field(date(2020, 1, 1))
        value_g: time = Field(time(9, 0))
        value_h: datetime = Field(datetime(2021, 1, 1, 15, 0, 0))

    model = SimpleDialogModel(title="Test", entries=Entries(value_d="Initial D"))

    widget = simple_dialog(model)
    qtbot.addWidget(widget)

    widget.widgets["value_a"].setText("BBB")
    widget.widgets["value_b"].setValue(43)
    widget.widgets["value_c"].setValue(3.15)
    widget.widgets["value_d"].setText("Edited D")
    widget.widgets["value_e"].setCurrentIndex(2)
    widget.widgets["value_f"].setDate(date(2021, 12, 31))
    widget.widgets["value_g"].setTime(time(17, 0))
    widget.widgets["value_h"].setDateTime(datetime(2021, 12, 31, 11, 59, 59))

    widget.restore_defaults()

    assert widget.widgets["value_a"].text() == "A"
    assert widget.widgets["value_b"].value() == 42
    assert widget.widgets["value_c"].value() == 3.14
    assert widget.widgets["value_d"].toPlainText() == "Edited D"
    assert widget.widgets["value_e"].currentIndex() == 0
    assert widget.widgets["value_f"].date() == date(2020, 1, 1)
    assert widget.widgets["value_g"].time() == time(9, 0)
    assert widget.widgets["value_h"].dateTime() == datetime(2021, 1, 1, 15, 0, 0)


def test_simple_dialog_widget_constraints(qtbot):
    """Test field restrictions using the SimpleDialog model."""

    class Entries(BaseModel):
        value_a: int = Field(default=42, ge=3, le=100)
        value_b: float = Field(default=3.1, gt=2.1, lt=10, multiple_of=0.1)

    model = SimpleDialogModel(title="Test Dialog", entries=Entries())

    widget = simple_dialog(model)
    qtbot.addWidget(widget)

    assert widget.widgets["value_a"].minimum() == 3
    assert widget.widgets["value_a"].maximum() == 100
    assert widget.widgets["value_b"].minimum() == 2.1
    assert widget.widgets["value_b"].maximum() == 10
    assert widget.widgets["value_b"].singleStep() == 0.1
