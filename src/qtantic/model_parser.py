"""Parser functions to process models and their components."""

# TODO: Implement additional properties for the fields, e.g., widget selector, using `json_scheme_extra` in `Field`.
# see https://github.com/pydantic/pydantic/discussions/2419#discussioncomment-8632072
# This would allow, e.g., to set a QTextEdit for a string field with a large description instead of the default QLineEdit.
# Or the user can set their own widgets, as long as they have the same interface as the default ones.
# I'll need to provide a compatibility list.
# - QTextEdit for string fields
# - QSlider for integer (and float???) fields

from typing import Any, Tuple, Union

from pydantic_core import PydanticUndefined
from qtpy import QtWidgets


def get_value_from_widget(widget: QtWidgets.QWidget) -> Any:
    """Get the value from a widget.

    Args:
        widget: Widget to get the value from.

    Returns:
        Value of the widget.

    """
    if isinstance(widget, QtWidgets.QSpinBox):
        return widget.value()
    elif isinstance(widget, QtWidgets.QDoubleSpinBox):
        return widget.value()
    elif isinstance(widget, QtWidgets.QLineEdit):
        return widget.text()
    elif isinstance(widget, QtWidgets.QCheckBox):
        return widget.isChecked()
    elif isinstance(widget, QtWidgets.QComboBox):
        return widget.currentText()
    else:
        raise NotImplementedError(f"Widget type {type(widget)} not implemented.")


def field_parser(
    name: str, value: Any, field: dict
) -> Tuple[QtWidgets.QLabel, QtWidgets.QWidget]:
    """Parse a field and create a label and a widget for it.

    Label will be created with the name or, if the field has a title, with the
    title of the field. The widget will be created based on the type of the
    field itslef.

    If the field has a description, it will be used as a tooltip for the widget
    and the label.

    Args:
        name: Name of the field.
        value: Current value of the field.
        field: Field definition.

    Returns:
        Tuple with a label and a widget for the field.

    Raises:
        NotImplementedError: If the field type is not implemented yet.
    """
    lbl_txt = field.get("title", name)
    lbl = QtWidgets.QLabel(lbl_txt)

    if "description" in field:
        lbl.setToolTip(field["description"])

    if (ftp := field["type"]) in ["integer", "number"]:
        widget = _create_number_widget(value, field)
    elif ftp == "string":
        if "enum" in field.keys():  # Literal
            widget = _create_combobox_widget(value, field)
        else:
            widget = _create_text_entry_widget(value, field)
    elif ftp == "boolean":
        widget = _create_bool_widget(value, field)
    else:
        raise NotImplementedError(f"Field type {ftp} not implemented yet.")

    return lbl, widget


def set_widget_value(widget: QtWidgets.QWidget, value: Any) -> None:
    """Set the value of a widget.

    If the value is set to `None` or `PydanticUndefined`, this function will not do anythin.

    Args:
        widget: Widget to set the value of.
        value: Value to set.

    Raises:
        NotImplementedError: If the widget type is not implemented yet.
    """
    if value in (None, PydanticUndefined):
        return

    if isinstance(widget, QtWidgets.QSpinBox) or isinstance(
        widget, QtWidgets.QDoubleSpinBox
    ):
        widget.setValue(value)
    elif isinstance(widget, QtWidgets.QLineEdit):
        widget.setText(value)
    elif isinstance(widget, QtWidgets.QCheckBox):
        widget.setChecked(value)
    elif isinstance(widget, QtWidgets.QComboBox):
        widget.setCurrentText(value)
    else:
        raise NotImplementedError(f"Widget type {type(widget)} not implemented.")


def _create_bool_widget(value: bool, field: dict) -> QtWidgets.QWidget:
    """Create a widget for a boolean field.

    Args:
        field: Field definition.

    Returns:
        Widget for the boolean field.

    """
    widget = QtWidgets.QCheckBox()
    widget.setChecked(value)

    if "description" in field:
        widget.setToolTip(field["description"])

    return widget


def _create_combobox_widget(value: str, field: dict) -> QtWidgets.QWidget:
    """Create a widget for a combobox field.

    Args:
        field: Field definition.

    Returns:
        Widget for the combobox field.

    """
    widget = QtWidgets.QComboBox()
    widget.addItems(field["enum"])
    widget.setCurrentText(value)

    if "description" in field:
        widget.setToolTip(field["description"])

    return widget


def _create_number_widget(value: Union[int, float], field: dict) -> QtWidgets.QWidget:
    """Create a widget for an integer or float field.

    Args:
        field: Field definition.

    Returns:
        Widget for the integer field.

    """
    if field["type"] == "integer":
        widget = QtWidgets.QSpinBox()
    else:  # float
        widget = QtWidgets.QDoubleSpinBox()

    widget.setValue(value)

    minimum = field.get("minimum", field.get("exclusiveMinimum", None))
    maximum = field.get("maximum", field.get("exclusiveMaximum", None))
    if minimum:
        widget.setMinimum(minimum)
    if maximum:
        widget.setMaximum(maximum)

    if "description" in field:
        widget.setToolTip(field["description"])
    if "multipleOf" in field:
        widget.setSingleStep(field["multipleOf"])

    return widget


def _create_text_entry_widget(value: str, field: dict) -> QtWidgets.QWidget:
    """Create a widget for a text entry field.

    Args:
        field: Field definition.

    Returns:
        Widget for the text entry field.

    """
    widget = QtWidgets.QLineEdit()

    widget.setText(value)

    if "description" in field:
        widget.setToolTip(field["description"])

    return widget
