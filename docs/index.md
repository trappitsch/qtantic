# Welcome to qtantic's documentation

Qtantic allows you to easily manage a settings or user input dialog
for your `Qt` based application.
Under the hood, it uses [`qtpy`](https://github.com/spyder-ide/qtpy) 
to provide compatibility with `PyQt` and `PySide`.
The dialogue will be rendered using a 
[`pydantic`](https://docs.pydantic.dev/latest/) model.
This means you can create dialog simply from a well constrained data model!

!!! warning
    
    This package is currently under active development and is not yet ready
    to use in production. Breaking changes may occur even in minor releases,
    while the major release is under `v0`.

If you have feedback on this project, please let me know!
I'm always happy to hear from you with your issues, 
enhancement ideas, contributions, etc.

## Other packages

Another package that does something similar is 
[`pyqtconfig`](https://github.com/pythonguis/pyqtconfig).
However, it is based on dictionaries,
which do not have the possibility to define metadata as can be done
for pydantic models.
Thus, data definition is more consise in `qtantic`, 
assuming you are familier with `pydantic`.

