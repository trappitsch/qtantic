# Tabbed Dialog

This tool helps you to create a tabbed dialog for your application
based on one simple pydantic model.
An example is shown here:

![Tabbed dialog tab 1 example, light mode](assets/tabbed_dialog_1_light.png#only-light)
![Tabbed dialog tab 2 example, light mode](assets/tabbed_dialog_2_light.png#only-light)
![Tabbed dialog tab 1 example, dark mode](assets/tabbed_dialog_1_dark.png#only-dark)
![Tabbed dialog tab 2 example, dark mode](assets/tabbed_dialog_2_dark.png#only-dark)

This dialog consists of the following features:

- An overall title (here: "My tabbed dialog").
- Two tabs with different tab titles.
- Various dialog entries for each tab.
- An optional "Restore Defaults" button that restores default values (where set) for all entries in the dialog (turned on by default).
- A "Cancel" and "Ok" button to discard or accept the dialog values.

## Example

The following gives the example code to create the dialog shown above.
As this is a dialog,
we create a simple main application around it which has as its main widget
a button that loads the dialog when clicked.
Detailed explanations are given in the code annotations: presse the `+` symbol in the code block to see them.
Many parts of this dialog are analog to the
[simple dialog](simple_dialog.md) example.
Here, we only discuss the specific parts of the tabbed dialog.


```python
from datetime import date
import sys
from typing import Literal

from pydantic import BaseModel, Field
from qtpy import QtWidgets

from qtantic import TabbedDialogModel, tabbed_dialog


class PersonalInfo(BaseModel):  # (1)
    name: str = Field(default="John Doe", description="Your name")
    birthday: date = Field(
        default=date(1982, 1, 1),
        description="Your birthday",
        minimum=date(1900, 1, 1),
    )
    emergency_contact: str = Field(
        default="Jane Doe", description="Name of your emergency contact"
    )


class Favorites(BaseModel):  # (2)
    color: Literal["Red", "Green", "Blue", "Purple", "Orange", "Yellow"] = Field(
        "Blue", description="What's your favorite color from this list?"
    )
    favorite_number: int = Field(default=42, description="Your favorite number")
    favorite_pet: str = Field(
        default="Snowball", description="Name of your favorite pet"
    )


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        btn = QtWidgets.QPushButton("Open dialog")
        btn.clicked.connect(self.dialog)
        self.setCentralWidget(btn)

        self.model = TabbedDialogModel(  # (3)
            title="My tabbed dialog",  # (4)
            tab_names=["Personal", "Favorites"],  # (5)
            entries=[PersonalInfo(), Favorites()],  # (6)
        )

        self.dialog()
        self.show()

    def dialog(self):
        dialog = tabbed_dialog(self.model)
        if dialog.exec_():
            self.model.entries = dialog.entries

        print(self.model.entries)


app = QtWidgets.QApplication([])
window = MyApp()
exit_code = app.exec_()
sys.exit(exit_code)
```

1. Base model for the first tab.
2. Base model for the second tab.
3. Create a tabbed dialog model.
4. Set the window title of the overall dialog. If not given, defaults to no title.
5. Set the tab names. If not given, defaults to names of the models that populate the tabs.
6. Set the model entries for the tabs. This must be given as a list.


## Details

### Create a dialog model with `TabbedDialogModel`

Do create a simple dialog,
you should use the `TabbedDialogModel` pydantic data model to create the overarching model for the dialog itself.
You also need some entry fields.
The simplest possible setup is as following:

```python
from pydantic import BaseModel
from qtantic import TabbedDialogModel

class MyFields(BaseModel):
    input_field: str


model = TabbedDialogModel(entries=MyFields())
```

This would create a tabbed dialog with one tab.
Here, `MyFields` is a pydantic model that contains the fields that you want to show in the dialog.
The `TabbedDialogModel` however has some additional arguments that you can use to customize the dialog.

## API Reference

::: qtantic.TabbedDialogModel
    options:
      show_root_heading: true
      heading_level: 3
      show_source: true

::: qtantic.tabbed_dialog
    options:
      show_root_heading: true
      heading_level: 3
      show_source: true
