import datetime
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.events import Blur
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

settings = Helper.get_settings()

AUTHOR = settings["default"]["author"] if "author" in settings["default"] else "Anonymous"
CATEGORIES = settings["default"]["categories"] if "categories" in settings["default"] else ["General"]
DEFAULT_TEXTAREA = settings["default"]["textarea_default_content"] if "textarea_default_content" in settings["default"] else ""
TEXTAREA_THEME = settings["default"]["theme"] if "theme" in settings["default"] else "monokai"
_save_button = Button

original_text_area_position = (0, 0)
is_textarea_expanded = False
textarea_height = "0%"

class ExtendedTextArea(TextArea):
    def _change_text(self, event, text: str, insert_text: str, move_cursor_relative: int = 0) -> None:
        if event.character == text:
            self.insert(insert_text)
            self.move_cursor_relative(columns=move_cursor_relative)
            event.prevent_default()

    def _on_blur(self, event: Blur) -> None:
        self.tab_behavior = "indent"

    def _on_key(self, event: events.Key) -> None:
        """Handle key events and modify/replace text inserted inside TextArea."""
        self._change_text(event, text="(", insert_text="()", move_cursor_relative=-1)
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
    _date: Input
    _category: Select
    _tags: Input
    _textarea: TextArea

    def compose(self) -> ComposeResult:
        field = self.get_field_values()
        self._title = Input(
            id="title", placeholder="Title of the article", value=field["title"]
        )
        self._author = Input(id="author", placeholder="Author", value=field["author"])
        self._date = Input(id="date", placeholder="Date", value=field["date"])
        self._category = Select(((line, line) for line in CATEGORIES), id="category", value=field["category"])
        self._tags = Input(id="tags", placeholder="Tags separeted with commas", value=field["tags"],  valid_empty=True)
        self._textarea = ExtendedTextArea(
            id="textarea",
            text=field["content"],
            language="markdown",
            theme=TEXTAREA_THEME,
            tab_behavior="indent",
        )
        _save_button = Button("Save", variant="primary")

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
            _save_button,
            Footer(),
        )
        self.original_text_area_position = self._textarea.styles.offset
        self.textarea_height = self._textarea.styles.height

    def get_field_values(self) -> dict:
        draft_content = Helper.get_draft_file_content()

        return {
            "title": draft_content["title"] if draft_content is not None else "",
            "author": draft_content["author"] if draft_content is not None else AUTHOR,
            "date": draft_content["date"] if draft_content is not None else datetime.date.today().isoformat(),
            "category": draft_content["category"] if draft_content is not None else "General",
            "tags": draft_content["tags"] if draft_content is not None else "",
            "content": draft_content["content"] if draft_content is not None else DEFAULT_TEXTAREA,
            "is_default_values": draft_content is None,
            "filename": draft_content["filename"] if draft_content is not None else None,
        }

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def form_has_change(self) -> bool:
        fields = self.get_field_values()

        return fields["title"] != self._title.value or fields["author"] != self._author.value or fields["date"] != self._date.value or fields["category"] != self._category.value or fields["tags"] != self._tags.value or fields["content"] != self._textarea.text

    def action_quit(self) -> None:
        # TODO: Add a confirmation dialog?
        message = "Bye! 👋"
        is_change = self.form_has_change()

        if is_change:
           filename = Helper.save_file(self, is_draft = True)
           message = f"Article saved as {filename}!\nBye! 👋"

        exit(message)

    def action_expand_textarea(self) -> None:
        global is_textarea_expanded

        # TODO: Hide categories list If displayed
        self._textarea.styles.offset = self.original_text_area_position if is_textarea_expanded else (0, -35)
        self._textarea.styles.height = self.textarea_height if is_textarea_expanded else "100%"

        is_textarea_expanded = not is_textarea_expanded

    def on_select_changed(self, event: Select.Changed) -> None:
        if self._tags.value != "":
            return
        # TODO: Better handle of the tags, because the Select field keep opened
        self._tags.value = Helper.predice_ai_tags(category = self._category.value, title = self._title.value)

    def format_tags(self, tags: str) -> str:
        return "\n  -".join(tags.split(","))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        filename = Helper.save_file(self)
        exit(f"Article saved as {filename}!\nBye! 👋")

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
