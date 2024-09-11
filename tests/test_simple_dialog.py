"""Tests for the SimpleDialog model and returner."""

from pydantic import BaseModel, Field

from qtantic import SimpleDialogModel, simple_dialog


def test_simple_dialog_model(qtbot):
    """Test the SimpleDialog model."""

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
    widget.accept()

    assert widget.entries.value_a == "BBB"
    assert widget.entries.value_b == 43
    assert widget.entries.value_c == 3.15
