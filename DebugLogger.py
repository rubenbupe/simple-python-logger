# Put "from DebugLogger import *" in your .py files to use
import inspect
import logging

_DEBUG_MODE = False
_LOG_MODE = True
_PRINT_FILE_DATA = True


class _Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    reset_bold = '\033[21m'
    disable = '\033[02m'
    underline = '\033[04m'
    reset_underline = '\033[24m'
    reverse = '\033[07m'
    reset_reverse = '\033[27m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    reset_invisible = '\033[28m'

    class Foreground:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class Background:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


INFO = "Info"
WARN = "Warning"
ERROR = "Error"

INFO_COLOR = _Colors.Background.green + _Colors.Foreground.black
ERROR_COLOR = _Colors.Background.red + _Colors.Foreground.black
WARN_COLOR = _Colors.Background.orange + _Colors.Foreground.black


# "File(without .py)" : _Colors.Foreground.black
# You can combine colors by concatenating them (_Colors.Foreground.black + _Colors.Background.red)
_FILE_COLORS = {
    "my_blue_text_file_name": _Colors.Foreground.blue,
}


def _get_call_info():
    try:
        frame = inspect.stack()[2]
        filename = frame[0].f_code.co_filename.split("/")[-1].split(".")[0]
        lineno = inspect.getframeinfo(frame[0]).lineno
        return [filename, lineno]
    except Exception:
        logging.error("Error al extraer datos de llamada")
        return None


def _get_color(filename):
    color = _FILE_COLORS.get(filename)
    if not color:
        color = ""
    return color


def _format_text(calldata, text, foreground_color=None, background_color=None, title=None):
    out = ""
    second_color = background_color if background_color else foreground_color if foreground_color else ""

    if _PRINT_FILE_DATA and calldata:
        out += "{}{}[{}:{}]{} ".format(foreground_color, _Colors.bold, calldata[0], calldata[1], _Colors.reset_bold)
    if title:
        out += "{}{}{}: {}".format(second_color, _Colors.bold, title, _Colors.reset_bold)
    out += second_color + text + _Colors.reset

    return out


# Debug functions (start with d). They print the parameter formatted as [debug, error, warning, info]
def dprint(text):
    if not _DEBUG_MODE:
        return
    calldata = _get_call_info()
    color = _get_color(calldata[0])

    print(_format_text(calldata, text, foreground_color=color))


def derror(text):
    if not _DEBUG_MODE:
        return
    calldata = _get_call_info()
    color = _get_color(calldata[0])

    print(_format_text(calldata, text, foreground_color=color, background_color=ERROR_COLOR, title=ERROR))


def dwarn(text):
    if not _DEBUG_MODE:
        return
    calldata = _get_call_info()
    color = _get_color(calldata[0])

    print(_format_text(calldata, text, foreground_color=color, background_color=WARN_COLOR, title=WARN))


def dinfo(text):
    if not _DEBUG_MODE:
        return
    calldata = _get_call_info()
    color = _get_color(calldata[0])

    print(_format_text(calldata, text, foreground_color=color, background_color=INFO_COLOR, title=INFO))


# Log functions (start with l). They print the parameter formatted as [debug, error, warning, info].
# You can save your logs to a file (not implemented)
def lprint(text):
    if not _LOG_MODE:
        return
    calldata = _get_call_info()
    color = _get_color(calldata[0])

    logging.debug(_format_text(calldata, text))


def lerror(text):
    if not _LOG_MODE:
        return
    calldata = _get_call_info()
    color = _get_color(calldata[0])

    logging.error(_format_text(calldata, text))


def lwarn(text):
    if not _LOG_MODE:
        return
    calldata = _get_call_info()
    color = _get_color(calldata[0])

    logging.warn(_format_text(calldata, text))


def linfo(text):
    if not _LOG_MODE:
        return
    calldata = _get_call_info()
    color = _get_color(calldata[0])

    logging.info(_format_text(calldata, text))


def set_debug(mode):
    global _DEBUG_MODE
    if type(mode) == bool and mode != _DEBUG_MODE:
        _DEBUG_MODE = mode
        _refresh_logging()


def set_log(mode):
    global _LOG_MODE
    if type(mode) == bool and mode != _LOG_MODE:
        _LOG_MODE = mode
        _refresh_logging()


def _refresh_logging():
    if _DEBUG_MODE:
        if logging.getLogger().level != logging.DEBUG:
            logging.getLogger().setLevel(logging.DEBUG)
    elif _LOG_MODE:
        if logging.getLogger().level != logging.INFO:
            logging.getLogger().setLevel(logging.INFO)


_refresh_logging()
