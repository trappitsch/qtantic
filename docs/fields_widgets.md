# Fields and Widgets

Below is a complete list of all the pydantic fields versus qt widgets
that are currently supported by `qtantic`.
Also given are all the specific options that those fields support.
Overall options are given in the first section,
all fields support these.


## Overall options

The following options are available for all fields:
 
- `title`: The label that will be associated with a given field. If not set, the field name will be used.
- `description`: The description of a filed that will be shown as a tooltip when hovered over the widget or over the label. If not set, no tooltip will be available.

**Example:**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    first_name: str = Field("", title="User's first name", description="The first name of the user.")
```

This will create on field with a label and a tooltip.


## Text fields

These are associated with the `str` type.
By default, text fields are rendered as `QLineEdit` widgets.
If you want to use a `QTextEdit` widget,
you can overwrite the default behavior with by setting `json_scheme_extra={"widget": "QTextEdit"}`.

**Example:**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    name: Field("John"),
    address: str = Field("", json_scheme_extra={"widget": "QTextEdit"}) 
```

This create two fields, a `name` field with a default value of "John" and an `address` field with a default value of "".
The address field will be rendered as a `QTextEdit` widget and allows for multi-line editing.


## Integers

These are associated with the `int` type.
By default, integers are rendered as `QSpinBox` widgets.

The following options are checked:

- `minimum`: The minimum value that can be set (inclusive).
- `maximum`: The maximum value that can be set (inclusive).
- `multipleOf`: The step size that is used when the up or down buttons are clicked. Defaults to 1.

It is highly recommended that you set the `minimum` and `maximum` values for integer fields.
If not set, the default values of the `QSpinBox` that is available in your environment will be used.

**Example:**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    age: int = Field(42, minimum=0, maximum=120)
    my_integer: int = Field(0, minimum=-10, maximum=10, multipleOf=5)
```

This will create two fields. 
The first one has a default value of 42 and can go from 0 to 120 (inclusive).
The second one defaults to 0, goes from -10 to 10 (inclusive) and has a step size of 5.


## Floats

These are associated with the `float` type.
By default, floats are rendered as `QDoubleSpinBox` widgets.

The following options are checked:

- `minimum`: The minimum value that can be set (inclusive).
- `maximum`: The maximum value that can be set (inclusive).
- `multipleOf`: The step size that is used when the up or down buttons are clicked.

It is highly recommended that you set the `minimum`, `maximum`, and `multipleOf` values for float fields.
If not set, the default values of the `QDoubleSpinBox` that is available in your environment will be used.

**Example:**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    length: float = Field(3.14, minimum=0, maximum=100.0, multipleOf=0.01)
```

This will create one field with a default value of 3.14.
The field can go from 0 to 100 (inclusive) and has a step size of 0.01.


## Booleans / Checkbox

These are associated with the `bool` type.
By default, booleans are rendered as `QCheckBox` widgets.

**Example:**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    is_active: bool = Field(False)
```

This will create a single checkbox field with a default value of `False`.


## Enumerations / Combo box

These are associated with the `Literal` type.
By default, enumerations are rendered as `QComboBox` widgets.
The default value, if given, will be the one originally set.

**Example:**

```python
from typing import Literal

from pydantic import BaseModel

class MyModel(BaseModel):
    combo_box: Literal["A", "B", "C"] = Field("B")
```

This will create a single combo box field with a default value of `B`.
The user can select one of the three options: `A`, `B`, or `C`.


## Dates, Times, and DateTimes

These values are all associated with the `datetime.date`, `datetime.time`, and `datetime.datetime` types.
By default, these are rendered as `QDateEdit`, `QTimeEdit`, and `QDateTimeEdit` widgets, respectively
and are displayed as:

- Date: `yyyy-MM-dd`, e.g., `2023-12-31`
- Time: `HH:mm:ss`, e.g., `23:59:59`
- DateTime: `yyyy-MM-dd HH:mm:ss`, e.g., `2023-12-31 23:59:59`

The following options are available:

- `minimum`: The minimum value that can be set (inclusive). Must be of the same time as the field.
- `maximum`: The maximum value that can be set (inclusive). Must be of the same time as the field.

Extra option to select the format:

You can select the format by setting the `json_scheme_extra={"display": "format_string"}`, 
where `format_string` is a string that is supported by the selected widget.

**Example:**

```python
from datetime import datetime

from pydantic import BaseModel

class MyModel(BaseModel):
    datetime: datetime = Field(datetime.now(), json_scheme_extra={"display": "yyyy-MM-dd HH:mm"})
```

In this example, the user gets a `datetime` widget that does not display the seconds.

