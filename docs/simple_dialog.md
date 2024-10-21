# Simple Dialog

This tool helps you to create a simple dialog for your application
based on one simple pydantic model.
An example is shown here:

![Simple dialog example, light mode](assets/simple_dialog_light.png#only-light)
![Simple dialog example, dark mode](assets/simple_dialog_dark.png#only-dark)

This dialog consists of the following features:

- An overall title (here: "My cool dialog")
- Various dialog entries that have a description, a value widget, and a tooltip (see below). Each entry is on its own line.
- An optional "Restore Defaults" button that restores default values (where set) for all entries in the dialog (turned on by default).
- A "Cancel" and "Ok" button to discard or accept the dialog values.

## Example

The following gives the example code to create the dialog shown above.
As this is a dialog,
we create a simple main application around it which has as its main widget
a button that loads the dialog when clicked.
Detailed explanations are given in the code annotations: presse the `+` symbol in the code block to see them.

```python
import sys
from typing import Literal

from pydantic import BaseModel, Field
from qtpy import QtWidgets

from qtantic import SimpleDialogModel, simple_dialog

class MyFields(BaseModel, validate_assignment=True):  # (1)
    name: str = Field("John Doe", description="Name of the person")  # (2)
    age: int = Field(42, maximum=140, minimum=0, description="Age of the person")  # (3)
    some_value: float = Field(3.14, title="The value of pi")  # (4)
    true_false: bool = Field(
        description="A boolean value", title="True or False"
    ) # (5)
    combo_box: Literal["A", "B", "C"] = Field(
        "B", description="Select one from the dropdown", title="Combo box"
    ) # (6)


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        btn = QtWidgets.QPushButton("Open dialog")
        btn.clicked.connect(self.dialog)
        self.setCentralWidget(btn)

        # Create a simple dialog model
        self.model = SimpleDialogModel(
            title="My cool dialog", entries=MyFields(true_false=True)
        )  # (7)

        self.dialog()
        self.show()

    def dialog(self):
        dialog = simple_dialog(self.model)  # (8)
        if dialog.exec_():
            self.model.entries = dialog.entries  # (9)

        print(self.model.entries)  # (10)


# Run the application
app = QtWidgets.QApplication([])
window = MyApp()
exit_code = app.exec_()
sys.exit(exit_code)
```

1. This class defines our pydantic model that will be used for the entries of the dialog.
    Each entry contains a type at least.
    Default values, if given, are used when the user clicks the "Restore Defaults" button.
    The `title` value is used as the label text for each entry. If not given, the field name is used.
    The `description` value is used as the tooltip text for each entry.
    Constraining numeric fields is done with `minimum` and `maximum`. If not provided, widget defaults are used.
    Note the `validate_assignment=True` argument.
    This allows us to automatically check upon accepting new values if these are valid.
    Validation is thus fully integrated using pydantic.
2. The name entry is a string that defaults to "John Doe" and has a tooltip "Name of the person".
    Strings are automatically rendered as line edit widgets.
3. The age entry is an integer that defaults to 42 and has a tooltip "Age of the person".
    Here, the minimum and maximum values are set,
    which will limit the values that can be set in the SpinBox widget.
4. The some_value entry is a float that defaults to 3.14 and has a tooltip "The value of pi".
    The label text is set to "Teh value of pi" while the field name is "some_value".
    Since a float is used, a DoubleSpinBox widget will be used for rendering.
    No limits are given, so the default limits of any DoubleSpinBox [0.00, 99.99] are used.
5. A boolean value is used for the true_false entry. Label text and tooltip are set as for other fields.
    A boolean will be rendered as a CheckBox widget.
    This field does not have a default value, so it will not be changed when the "Restore Defaults" button is clicked.
6. The combo_box entry is a Literal type that can only be one of the given values.
    The default value here is set to "B", which must be part of the options.
    `Literal` types are renderd as ComboBox widgets.
7. The dialog model itself is created with outer arguments (e.g., the title of the dialog)
    and entries, which are described above in the `MyFields` pydantic class.
8. We can create the dialog simply by using the provided `simple_dialog` method that we imported above.
9. Here we execute the dialog first, and if the `Ok` button is clicked,
    the dialog is accepted and the `if` statement is entered.
    In this case, we update the model entries with the new values that the user set.
10. Finally, we print the new values to the console. This is useful for test purposes.


## Details

### Create a dialog model with `SimpleDialogModel`

Do create a simple dialog,
you should use the `SimpleDialogModel` pydantic data model to create the overarching model for the dialog itself.
You also need some entry fields.
The simplest possible setup is as following:

```python
from pydantic import BaseModel
from qtantic import SimpleDialogModel

class MyFields(BaseModel):
    input_field: str

model = SimpleDialogModel(entries=MyFields())
```

Here, `MyFields` is a pydantic model that contains the fields that you want to show in the dialog.
The `SimpleDialogModel` however has some additional arguments that you can use to customize the dialog.

## API Reference

::: qtantic.SimpleDialogModel
    options:
      show_root_heading: true
      heading_level: 3
      show_source: true

::: qtantic.simple_dialog
    options:
      show_root_heading: true
      heading_level: 3
      show_source: true
