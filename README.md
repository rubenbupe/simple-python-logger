# Simple-Python-Logger
Simple Python Logger that lets you color the logs depending on the file they come from. You can also see the line of code where it comes from.

## How to use
* Import the file into your project and put "from DebugLogger import *" in your .py files to use the logger functions. You can also use "import DebugLogger as something" and call the functions like this: "something.function(args)".

* Put the files that you want to color in the _FILE_COLORS dictionary.

## How does it work?
* Debug functions (start with d) print the parameter formatted as [debug, error, warning, info]. They are printed using print() and they will only work if _DEBUG_MODE is True (it is not by default). You can change it using set_debug(bool).

* Log functions (start with l). They print the parameter formatted as [debug, error, warning, info]. They are printed using logging and they will only work if _LOG_MODE is True (it is by default). You can change it using set_log(bool).

You can save your logs to a file (not implemented)
