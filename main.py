import datetime
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Input, Label, Select, TextArea, Button

AUTHOR = "Jose Cerrejon"
CATEGORIES = """General
Raspberry Pi
Developer
Apple
Linux
Android
Arduino
Atomic Pi
Banana Pi
ODROID
Orange Pi""".splitlines()

DEFAULT_TEXTAREA = """# Title
![Alt](/path/to/image.jpg)

Intro text here
- - -
## Subtitle
"""


class Frodown(App):
    BINDINGS = [
        Binding(key="ctrl+t", action="toggle_dark", description="Toggle light mode"),
        Binding(key="ctrl+q", action="quit", description="Quit the app"),
    ]

    CSS = """
    Input.-valid {
        border: tall;
    }
    Input.-valid:focus {
        border: tall $success;
    }
    Input {
        margin: 1 1;
    }
    Label {
        margin: 1 2;
    }
    Select {
        border: tall;
    }
    Button {
        margin: 1 2;
    }
    """

    _title: Input
    _author: Input
    _date: Input
    _category: Select
    _tags: Input
    _textarea: TextArea

    def compose(self) -> ComposeResult:
        self._title = Input(placeholder="Title of the article")
        self._author = Input(placeholder="Author", value=AUTHOR)
        self._date = Input(placeholder="Date", value=datetime.date.today().isoformat())
        self._category = Select(((line, line) for line in CATEGORIES), value="General")
        self._tags = Input(placeholder="Tags separeted with commas", valid_empty=True)
        self._textarea = TextArea(text=DEFAULT_TEXTAREA, language="markdown")

        yield Header()
        yield Label("Title")
        yield self._title
        yield Label("Author")
        yield self._author
        yield Label("Date")
        yield self._date
        yield Label("Category")
        yield self._category
        yield Label("Tags")
        yield self._tags
        yield Label("Article")
        yield self._textarea
        yield Button("Save", variant="primary")
        yield Footer()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        pass

    def format_tags(self, tags: str) -> str:
        return "\n  -".join(tags.split(","))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        frontmatter = f"""title: {self._title.value}
author: {self._author.value}
date: {self._date.value}
category:
  - {self._category.value}
tags:
  - {self.format_tags(self._tags.value)}
"""

        filename = f"./{self._title.value.lower().replace(' ', '_')}.md"

        with open(filename, "w") as file:
            file.write(frontmatter)
            file.write("\n---\n")
            file.write(self._textarea.text)

        self.exit(message=f"Article {self._title.value} saved as {filename}!")


app = Frodown()

if __name__ == "__main__":
    app.run()
