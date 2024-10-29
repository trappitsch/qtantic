"""Tools to create a tabbed dialog based on multiple pydantic models.

The idea behind these multiple dialog model is that the user can combine
mutliple different pydantic models to create a tabbed dialog.
This is mostly for more complicated dialogs, however, for accept, cancel, and
reset to default features works similar to the SimpleDialog.

If you need several tabs that have the same layout but, e.g., represent multiple
of the same instruments, see the MultiTabbedDialog.
"""

from typing import List, Union

from pydantic import BaseModel, Field
from qtpy import QtWidgets

import qtantic.model_parser as mp


class TabbedDialogModel(BaseModel):
    """Pydantic model to crate a tabbed dialog.

    Import this with `from qtantic import TabbedDialogModel`.

    Attributes:
        title: Title of the dialog box. Defaults to "".
        tab_names: Names of the tabs as a list. Must be the same length as the entries.
        restore_defaults: Provide a button to reset all fields to their default values.
            Defaults to True.
        entries: List of Pydantic `BaseModel` that will be used to create the dialog.

    Examples:
        >>> from pydantic import BaseModel
        >>> from qtantic import TabbedDialogModel
        >>>
        >>> class MyFields1(BaseModel):
        >>>   input_field: str
        >>>
        >>> class MyFields2(BaseModel):
        >>>   input_field: float
        >>>
        >>> tabbed_model = TabbedDialogModel(entries=[MyFields1, MyFields2]
    """

    title: str = ""
    tab_names: Union[None, List[str]] = Field(
        None,
        description="Names of the tabs. Must be the same length as the entries. "
        "If not provided, the model names will be used.",
    )
    restore_defaults: bool = Field(
        default=True,
        description="Provide a button to reset all fields to their default values.",
    )
    entries: List[BaseModel]


class TabbedDialog(QtWidgets.QDialog):
    """Tabbed dialog that is based on a pydantic model.

    The dialog will be created based on the provided `TabbedDialogModel`.

    """

    def __init__(
        self,
        model: TabbedDialogModel,
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

        Raises:
            ValueError: If the number of tab names does not match the number of entries.
        """
        super().__init__(parent, *args, **kwargs)

        if model.tab_names and len(model.tab_names) != len(model.entries):
            raise ValueError("Number of tab names must match number of entries.")

        self._model: TabbedDialogModel = model
        self._tab_names: List[str] = model.tab_names
        self._tab_widgets: List[QtWidgets.QWidget] = []
        self._entries: List[BaseModel] = model.entries
        self._labels: List[dict] = []
        self._widgets: List[dict] = []

        self.setWindowTitle(model.title)

        self._setup_ui()

    @property
    def entries(self) -> List[BaseModel]:
        """Get the entries of the dialog."""
        return self._entries

    @property
    def labels(self) -> List[dict]:
        """Get the labeles of the dialog with model field names as keys."""
        return self._labels

    @property
    def tab_names(self) -> List[str]:
        """Get the names of the tabs."""
        return self._tab_names

    @property
    def widgets(self) -> List[dict]:
        """Get the entry fields of the dialog with model field names as keys."""
        return self._widgets

    def _setup_ui(self) -> None:
        """Setup the UI of the dialog based on the provided models."""
        tab_widget = QtWidgets.QTabWidget()
        tab_names = []

        for tt, tab in enumerate(self.entries):
            if self.tab_names:
                tab_name = self.tab_names[tt]
            else:
                tab_name = tab.model_json_schema()["title"]

            lbls = dict()
            wdgts = dict()

            for key in tab.model_fields.keys():
                lbl, widget = mp.field_parser(
                    key, getattr(tab, key), tab.model_json_schema()["properties"][key]
                )
                lbls[key] = lbl
                wdgts[key] = widget

            tab_names.append(tab_name)
            self._labels.append(lbls)
            self._widgets.append(wdgts)

        for tt, tab in enumerate(self.entries):
            current_widget = QtWidgets.QWidget()
            tab_widget.addTab(current_widget, tab_names[tt])

            tab_layout = QtWidgets.QVBoxLayout()
            edit_layout = QtWidgets.QFormLayout()

            for key in tab.model_fields.keys():
                edit_layout.addRow(self.labels[tt][key], self.widgets[tt][key])

            tab_layout.addLayout(edit_layout)
            tab_layout.addStretch()
            current_widget.setLayout(tab_layout)
            self._tab_widgets.append(current_widget)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tab_widget)
        layout.addStretch()

        if self._model.restore_defaults:
            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.RestoreDefaults
                | QtWidgets.QDialogButtonBox.Ok
                | QtWidgets.QDialogButtonBox.Cancel
            )
            buttons.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(
                self.restore_defaults
            )
        else:
            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

        self._tab_names = tab_names

    def accept(self) -> None:
        """Accept the dialog and close it."""
        for tt, tab in enumerate(self.entries):
            for key, widget in self.widgets[tt].items():
                setattr(self.entries[tt], key, mp.get_value_from_widget(widget))
        super().accept()

    def restore_defaults(self) -> None:
        """Restore all fields to their default values."""
        for tt, tab in enumerate(self.entries):
            for key in tab.model_fields.keys():
                default = self.entries[tt].model_fields[key].default
                widget = self.widgets[tt][key]
                mp.set_widget_value(widget, default)


def tabbed_dialog(
    model: TabbedDialogModel, *args, parent: QtWidgets.QWidget = None, **kwargs
) -> TabbedDialog:
    """Get a tabbed dialog QWidget.

    You can pass further `*args` and `**kwargs` that will be passed on to the
    QDialog widget.

    Args:
        model: Pydantic model that will be used to create the dialog.
        parent: Parent widget of the dialog, defaults to `None`.

    Returns:
        A TabbedDialog widget with the provided fields and entries,
            plus an `Ok` and `Cancel` and `Restore Defaults` (optional)
            button to accept / cancel the dialog.
            This widget subclasses `QtWidgets.QDialog`.

    Examples:
        >>> from pydantic import BaseModel
        >>> from qtantic import TabbedDialogModel, tabbed_dialog
        >>>
        >>> class MyFields1(BaseModel):  # Define entries for first tab
        >>>     input_field: str
        >>>
        >>> class MyFields2(BaseModel):  # Define entries for second tab
        >>>     age: int
        >>>
        >>> tabbed__dialog_model = TabbedDialogModel(entries=[MyFields1, MyFields2])
        >>> dialog = tabbed_dialog(tabbed_dialog_model)
    """
    return TabbedDialog(model, *args, parent=parent, **kwargs)
