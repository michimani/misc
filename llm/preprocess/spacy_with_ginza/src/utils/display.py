from datetime import UTC
from datetime import datetime as dt
from os import path
from typing import Final

import eel

HTML_DIR: Final[str] = "data/__html"

eel.init(HTML_DIR)


@eel.expose
def __new_window(filename: str):
    eel.start(filename, size=(800, 300))


def render_html(html: str):
    filename = f"{str(dt.timestamp(dt.now(tz=UTC)))}.html"
    file_path = path.join(HTML_DIR, filename)
    with open(file_path, "w") as f:
        f.write(html)
    __new_window(filename)
