"""This class will allow us to create a simple dialog box.

The idea of this dialog is that it allows simple creation of a query
dialog, i.e., to ask a user to provide some input variables in the form
of a dialog.

It takes a `pydantic` model as input and creates a dialog box with an
`Ok` and `Cancel` button to either accept or reject the new values.
The dialog box will return a `pydantic` model filled with the new values.
If `Cancel` was pressed, None will be returned.
"""

from pydantic import BaseModel
from qtpy import QtWidgets

import qtantic.model_parser as mp


class SimpleDialogModel(BaseModel):
    """Model that needs to be provided for the SimpleDialog class."""

    title: str | None = None
    entries: BaseModel


class SimpleDialog(QtWidgets.QDialog):
    """Simple dialog that is based on a pydantic model.

    The dialog will be created based on the provided `SimpleDialogModel`.

    """

    def __init__(
        self,
        model: SimpleDialogModel,
        *args,
        parent: QtWidgets.QWidget = None,
        **kwargs,
    ) -> None:
        """Initialize the dialog box.

        You can pass further *args and **kwargs that will be passed on to the
        QDialog widget.

        Args:
            model: Pydantic model that will be used to create the dialog.
            parent: Parent widget of the dialog or None.
        """
        super().__init__(parent, *args, **kwargs)

        self._model: SimpleDialogModel = model
        self._entries: BaseModel = model.entries
        self._labels: dict = {}
        self._widgets: dict = {}

        title = (
            model.title if model.title else model.entries.model_json_schema()["title"]
        )
        self.setWindowTitle(title)

        self._setup_ui()

    @property
    def entries(self) -> BaseModel:
        """Get the entries of the dialog."""
        return self._entries

    @property
    def labels(self) -> dict:
        """Get the labeles of the dialog with model field names as keys."""
        return self._labels

    @property
    def widgets(self) -> dict:
        """Get the entry fields of the dialog with model field names as keys."""
        return self._widgets

    def _setup_ui(self) -> None:
        """Setup the UI of the dialog based on the provided model."""
        for key in self.entries.model_fields.keys():
            lbl, widget = mp.field_parser(
                key,
                getattr(self.entries, key),
                self.entries.model_json_schema()["properties"][key],
            )
            self._labels[key] = lbl
            self._widgets[key] = widget

        layout = QtWidgets.QVBoxLayout()
        edit_layout = QtWidgets.QFormLayout()
        for key in self.entries.model_fields.keys():
            edit_layout.addRow(self.labels[key], self.widgets[key])

        layout.addLayout(edit_layout)
        layout.addStretch()

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def accept(self) -> None:
        """Accept the dialog and return the new values."""
        for key, widget in self.widgets.items():
            setattr(self.entries, key, mp.get_value_from_widget(widget))
        super().accept()


def simple_dialog(
    model: SimpleDialogModel, *args, parent=None, **kwargs
) -> SimpleDialog:
    """Get a simple dialog QWidget.

    You can pass further *args and **kwargs that will be passed on to the
    QDialog widget.

    Args:
        model: Pydantic model that will be used to create the dialog.
        parent: Parent widget of the dialog, defaults to `None`.

    Returns:
        A SimpleDialog widget with the provided fields and entries,
        plus an `Ok` and `Cancel` button to accept / cancel the dialog.
    """
    return SimpleDialog(model)
