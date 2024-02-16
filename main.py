import datetime
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.containers import Container
from textual.widgets import (
    Static,
    Header,
    Footer,
    Input,
    Label,
    Select,
    TextArea,
    Button,
)

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


class Frodown(App[None]):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        Binding(key="ctrl+s", action="toggle_sidebar", description="Cheat Sheet"),
        Binding(key="ctrl+q", action="quit", description="Quit the App"),
        Binding(key="ctrl+t", action="toggle_dark", description="Toggle Light Mode"),
    ]

    _title: Input
    _author: Input
    _date: Input
    _category: Select
    _tags: Input
    _textarea: TextArea

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        self._title = Input(id="title", placeholder="Title of the article")
        self._author = Input(id="author", placeholder="Author", value=AUTHOR)
        self._date = Input(
            id="date", placeholder="Date", value=datetime.date.today().isoformat()
        )
        self._category = Select(
            ((line, line) for line in CATEGORIES), id="category", value="General"
        )
        self._tags = Input(
            id="tags", placeholder="Tags separeted with commas", valid_empty=True
        )
        self._textarea = TextArea(
            id="textarea", text=DEFAULT_TEXTAREA, language="markdown"
        )

        yield Container(
            Sidebar(classes="-hidden"),
            Header(show_clock=True),
            Label("Title"),
            self._title,
            Label("Author"),
            self._author,
            Label("Date"),
            self._date,
            Label("Category"),
            self._category,
            Label("Tags"),
            self._tags,
            Label("Article"),
            self._textarea,
            Button("Save", variant="primary"),
            Footer(),
        )

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

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

    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")


class Title(Static):
    pass


class OptionGroup(Container):
    pass


class Message(Static):
    pass


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Title("Cheat Sheet")
        yield OptionGroup(
            Message(
                """::: important Custom important
...
:::
__
::: info Custom info
...
:::
__
::: note Custom note
...
:::
__
::: tip Custom tip
...
:::
__
::: warning Custom warning
...
:::
__
::: caution Custom caution
...
:::
__
Use == == to mark. ==highlighted==

NOTE: My intention is to add a table, so you can select the code and then, the code will be copied to the Textarea.
"""
            )
        )


app = Frodown()

if __name__ == "__main__":
    app.run()
