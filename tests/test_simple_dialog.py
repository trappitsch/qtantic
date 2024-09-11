"""Tests for the SimpleDialog model and returner."""

from typing import Literal

from pydantic import BaseModel, Field

from qtantic import SimpleDialogModel, simple_dialog


def test_simple_dialog_model_accept(qtbot):
    """Test the SimpleDialog model."""

    class Entries(BaseModel):
        value_a: str = Field(
            default="A", title="This is value A", description="Tooltip value A"
        )
        value_b: int = Field(default=42, description="Tooltip value B")
        value_c: float = Field(default=3.14, title="Approx. pi", description="Tooltip value C")
        value_d: bool = Field(default=True, description="Tooltip value D")
        value_e: Literal["A", "B", "C"] = Field(default="B", description="Tooltip value E", title="Select one from DropDown")

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


    widget.widgets["value_a"].setText("BBB")
    widget.widgets["value_b"].setValue(43)
    widget.widgets["value_c"].setValue(3.15)
    widget.widgets["value_d"].setChecked(False)
    widget.widgets["value_e"].setCurrentIndex(0)

    widget.accept()

    assert widget.entries.value_a == "BBB"
    assert widget.entries.value_b == 43
    assert widget.entries.value_c == 3.15
    assert widget.entries.value_d is False
    assert widget.entries.value_e == "A"


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
