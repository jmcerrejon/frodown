import datetime
from textual import on, events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.events import Blur
from textual.reactive import reactive
from textual.containers import Container
from helper import Helper

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
CATEGORIES = Helper.get_categories()
DEFAULT_TEXTAREA = Helper.get_textarea_example()
TEXTAREA_THEME = "monokai"
_save_button = Button

original_text_area_position = (0, 0)
is_textarea_expanded = False
textarea_height = "0%"

class ExtendedTextArea(TextArea):

    def _change_text(self, event, text: str, insert_text:str, move_cursor_relative:int = 0) -> None:
        if event.character == text:
            self.insert(insert_text)
            self.move_cursor_relative(columns=move_cursor_relative)
            event.prevent_default()

    def _on_blur(self, event: Blur) -> None:
        self.tab_behavior = "indent"

    def _on_key(self, event: events.Key) -> None:
        """ Handle key events and modify/replace text inserted inside TextArea. """
        self._change_text(event, text="(", insert_text="()",move_cursor_relative=-1)
        if event.character == "!" and self.cursor_at_start_of_line:
            self.insert('![alt]("alt")')
            self.move_cursor_relative(columns=-6)
            event.prevent_default()
        # Special case for the tab key If you are at the end of the TextArea, it will set focus to the next widget. _on_blur will set the tab_behavior to "indent" again.
        if event.key == "tab" and self.cursor_at_last_line:
            self.tab_behavior = "focus"


class Frodown(App[None]):
    CSS_PATH = "main.tcss"
    BINDINGS = [
        Binding(key="ctrl+s", action="expand_textarea", description="Zen mode"),
        Binding(key="ctrl+z", action="toggle_sidebar", description="Cheat Sheet"),
        Binding(key="ctrl+t", action="toggle_dark", description="Toggle Light Mode"),
        Binding(key="ctrl+q", action="quit", description="Quit the App"),
    ]

    _title: Input
    _author: Input
    _icon: Input
    _date: Input
    _category: Select
    _tags: Input
    _textarea: TextArea

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:

        self._title = Input(id="title", placeholder="Title of the article")
        self._author = Input(id="author", placeholder="Author", value=AUTHOR)
        self._icon = Input(id="icon", placeholder="Icon", value="fa-regular fa-newspaper")
        self._date = Input(
            id="date", placeholder="Date", value=datetime.date.today().isoformat()
        )
        self._category = Select(
            ((line, line) for line in CATEGORIES), id="category", value="General"
        )
        self._tags = Input(
            id="tags", placeholder="Tags separeted with commas", valid_empty=True
        )
        self._textarea = ExtendedTextArea(
            id="textarea", text=DEFAULT_TEXTAREA, language="markdown", theme=TEXTAREA_THEME, tab_behavior="indent"
        )
        _save_button = Button("Save", variant="primary")

        yield Container(
            Sidebar(classes="-hidden"),
            Header(show_clock=True),
            Label("Title"),
            self._title,
            Label("Author"),
            self._author,
            Label("icon"),
            self._icon,
            Label("Date"),
            self._date,
            Label("Category"),
            self._category,
            Label("Tags"),
            self._tags,
            Label("Article"),
            self._textarea,
            _save_button,
            Footer(),
        )
        self.original_text_area_position = self._textarea.styles.offset
        self.textarea_height = self._textarea.styles.height

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_expand_textarea(self) -> None:
        global is_textarea_expanded

        # TODO: Hide categories list If displayed and refactor the code
        if is_textarea_expanded:
            self._textarea.styles.offset = self.original_text_area_position
            self._textarea.styles.height = self.textarea_height
        else:
            self._textarea.styles.offset = (0, -40)
            self._textarea.styles.height = "100%"

        is_textarea_expanded = not is_textarea_expanded

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        pass

    def format_tags(self, tags: str) -> str:
        return "\n  -".join(tags.split(","))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        frontmatter = f"""---
title: {self._title.value}
icon: {self._icon.value}
author: {self._author.value}
date: {self._date.value}
category:
  - {self._category.value}
tags:
  - {self.format_tags(self._tags.value)}
"""

        filename = f"./{self._title.value.lower().replace(' ', '_').replace('/', '_')}.md"

        with open(filename, "w") as file:
            file.write(frontmatter)
            file.write("---\n")
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
        yield OptionGroup(Message(Helper.get_cheat_sheet()))


if __name__ == "__main__":
    app = Frodown()
    app.run()
