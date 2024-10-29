"""Tests for the TabbedDialog model and returner."""

from datetime import date, datetime, time
from typing import Literal

from pydantic import BaseModel, Field
import pytest
from qtpy import QtWidgets

from qtantic import TabbedDialogModel, tabbed_dialog


def test_tabbed_dialog_model_accept(qtbot):
    """Test the TabbedDialog model."""

    class Entries1(BaseModel):
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

    class Entries2(BaseModel):
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

    model = TabbedDialogModel(title="Test Dialog", entries=[Entries1(), Entries2()])

    widget = tabbed_dialog(model)
    qtbot.addWidget(widget)

    assert widget.windowTitle() == "Test Dialog"
    assert widget.entries == model.entries

    assert widget.widgets[0]["value_a"].toolTip() == "Tooltip value A"
    assert widget.widgets[0]["value_b"].toolTip() == "Tooltip value B"
    assert widget.widgets[0]["value_c"].toolTip() == "Tooltip value C"
    assert widget.widgets[0]["value_d"].toolTip() == "Tooltip value D"
    assert widget.widgets[0]["value_e"].toolTip() == "Tooltip value E"
    assert isinstance(widget.widgets[1]["value_i"], QtWidgets.QTextEdit)

    widget.widgets[0]["value_a"].setText("BBB")
    widget.widgets[0]["value_b"].setValue(43)
    widget.widgets[0]["value_c"].setValue(3.15)
    widget.widgets[0]["value_d"].setChecked(False)
    widget.widgets[0]["value_e"].setCurrentIndex(0)
    widget.widgets[1]["value_f"].setDate(date(2021, 12, 31))
    widget.widgets[1]["value_g"].setTime(time(17, 0))
    widget.widgets[1]["value_h"].setDateTime(datetime(2021, 12, 31, 11, 59, 59))

    widget.accept()

    assert widget.entries[0].value_a == "BBB"
    assert widget.entries[0].value_b == 43
    assert widget.entries[0].value_c == 3.15
    assert widget.entries[0].value_d is False
    assert widget.entries[0].value_e == "A"
    assert widget.entries[1].value_f == date(2021, 12, 31)
    assert widget.entries[1].value_g == time(17, 0)
    assert widget.entries[1].value_h == datetime(2021, 12, 31, 11, 59, 59)


def test_tabbed_dialog_model_reject(qtbot):
    """Test the TabbedDialog model - no change on rejection."""

    class Entries1(BaseModel):
        value_a: str = Field(
            default="A", title="This is value A", description="Tooltip value A"
        )
        value_b: int = Field(default=42)
        value_c: float = Field(default=3.14, title="Approx. pi")

    class Entries2(BaseModel):
        tab2_value: str = Field(default="B")

    model = TabbedDialogModel(title="Test Dialog", entries=[Entries1(), Entries2()])

    widget = tabbed_dialog(model)
    qtbot.addWidget(widget)

    assert widget.windowTitle() == "Test Dialog"
    assert widget.entries == model.entries

    widget.widgets[0]["value_a"].setText("BBB")
    widget.widgets[0]["value_b"].setValue(43)
    widget.widgets[0]["value_c"].setValue(3.15)
    widget.widgets[1]["tab2_value"].setText("CCC")

    widget.reject()

    assert widget.entries == model.entries


def test_tabbed_dialog_model_restore_defaults(qtbot):
    """Restore defaults for values that have them."""

    class Entries1(BaseModel):
        value_a: str = Field(
            default="A", title="This is value A", description="Tooltip value A"
        )
        value_b: int = Field(default=42, description="Tooltip value B")
        value_c: float = Field(
            default=3.14, title="Approx. pi", description="Tooltip value C"
        )
        value_d: str = Field(
            title="This is value D",
            description="Tooltip value D",
            json_scheme_extra={"widget": "QTextEdit"},
        )

    class Entries2(BaseModel):
        value_e: Literal["A", "B", "C"] = Field("A")
        value_f: date = Field(date(2020, 1, 1))
        value_g: time = Field(time(9, 0))
        value_h: datetime = Field(datetime(2021, 1, 1, 15, 0, 0))

    model = TabbedDialogModel(
        title="Test", entries=[Entries1(value_d="Initial D"), Entries2()]
    )

    widget = tabbed_dialog(model)
    qtbot.addWidget(widget)

    widget.widgets[0]["value_a"].setText("BBB")
    widget.widgets[0]["value_b"].setValue(43)
    widget.widgets[0]["value_c"].setValue(3.15)
    widget.widgets[0]["value_d"].setText("Edited D")
    widget.widgets[1]["value_e"].setCurrentIndex(2)
    widget.widgets[1]["value_f"].setDate(date(2021, 12, 31))
    widget.widgets[1]["value_g"].setTime(time(17, 0))
    widget.widgets[1]["value_h"].setDateTime(datetime(2021, 12, 31, 11, 59, 59))

    widget.restore_defaults()

    assert widget.widgets[0]["value_a"].text() == "A"
    assert widget.widgets[0]["value_b"].value() == 42
    assert widget.widgets[0]["value_c"].value() == 3.14
    assert widget.widgets[0]["value_d"].toPlainText() == "Edited D"
    assert widget.widgets[1]["value_e"].currentIndex() == 0
    assert widget.widgets[1]["value_f"].date() == date(2020, 1, 1)
    assert widget.widgets[1]["value_g"].time() == time(9, 0)
    assert widget.widgets[1]["value_h"].dateTime() == datetime(2021, 1, 1, 15, 0, 0)


@pytest.mark.parametrize("tab_names", [["Tab 13", "Tab 42"], None])
def test_tabbed_dialog_names(qtbot, tab_names):
    """Ensure tab names and window name are set correctly."""
    if tab_names is None:
        tab_names_exp = ["ent1", "ent2"]
        window_title = ""
    else:
        tab_names_exp = tab_names
        window_title = "Test"

    class ent1(BaseModel):
        value_a: str = Field("A")

    class ent2(BaseModel):
        value_b: int = Field(42)

    model = TabbedDialogModel(
        title=window_title, tab_names=tab_names, entries=[ent1(), ent2()]
    )

    widget = tabbed_dialog(model)
    qtbot.addWidget(widget)

    assert widget.windowTitle() == window_title
    assert widget._tab_names == tab_names_exp
