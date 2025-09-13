import os
import re
import subprocess
from string import Template
from typing import Optional

import httpx
import tomli

FRONTMATTER_TOTAL_DELIMITERS = 2
TAG_TEMPLATE = Template(
    """Search tags for the following topic and title. The topic is $topic and the title is $title. Show me four tags, only one word or two per tag with comma separated and don't include a preamble and don't include dot at the end.
"""
)
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "mistral:7b-instruct-v0.2-q4_K_S",
    "keep_alive": "5m",
    "stream": False,
}


class Helper:
    def get_settings() -> dict:
        try:
            with open("settings.toml", mode="rb") as fp:
                return tomli.load(fp)
        except FileNotFoundError:
            exit("settings.toml not found.")
        except KeyError:
            return ""
        except Exception:
            exit("settings.toml does not have the correct format.")

    def get_cheat_sheet() -> str:
        return """
::: important Custom important
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

    def get_icon_by_category(category: str = "General") -> str:
        # sourcery skip: instance-method-first-arg-name
        icons_list = {
            "General": "fa-regular fa-newspaper",
            "Raspberry Pi": "fa-brands fa-raspberry-pi",
            "Developer": "fa-solid fa-code",
            "Apple": "fa-brands fa-apple",
            "Linux": "fa-brands fa-linux",
            "Android": "fa-brands fa-android",
            "Arduino": "fa-brands fa-arduino",
            "Atomic Pi": "fa-solid fa-microchip",
            "Banana Pi": "fa-solid fa-ban",
            "ODROID": "fa-solid fa-microchip",
            "Orange Pi": "fa-solid fa-microchip",
        }

        return icons_list.get(category, "fa-regular fa-newspaper")

    def get_draft_file_content() -> dict:
        def _get_lines_between_tags_and_dashes(lines: list[str]) -> str:
            result = []
            for line in lines:
                if line.startswith("---"):
                    break
                else:
                    result.append(line)

            return ", ".join(result).replace("  - ", "").replace("\n", "")

        frontmatter = {}
        filename = [file for file in os.listdir() if file.endswith(".draft")]
        if not filename:
            return None

        with open(filename[0], "r") as file:
            lines = file.readlines()
            count_frontmatter_delimitier = 0

            for line in lines:
                if count_frontmatter_delimitier == FRONTMATTER_TOTAL_DELIMITERS:
                    frontmatter["content"] = line
                    frontmatter["content"] += "".join(lines[lines.index(line) + 1 :])
                    break

                if "---" in line:
                    count_frontmatter_delimitier += 1

                if match := re.match(r"(\w+):\s*(.*)", line):
                    key = match[1]
                    value = match[2]
                    if key == "author":
                        frontmatter["author"] = value
                    elif key == "category":
                        frontmatter["category"] = (
                            "".join(lines[lines.index(line) + 1])
                            .replace("  - ", "")
                            .replace("\n", "")
                        )
                    elif key == "date":
                        frontmatter["date"] = value
                    elif key == "icon":
                        frontmatter["icon"] = value
                    elif key == "tags":
                        frontmatter["tags"] = _get_lines_between_tags_and_dashes(
                            lines[lines.index(line) + 1 :]
                        )
                    elif key == "title":
                        frontmatter["title"] = value
        frontmatter["filename"] = filename[0]

        return frontmatter

    def save_file(self, output_directory: str, is_draft: bool = False) -> str:
        extension = "md.draft" if is_draft else "md"
        frontmatter = f"""---
title: {self._title.value}
icon: {Helper.get_icon_by_category(self._category.value)}
author: {self._author.value}
date: {self._date.value}
category:
  - {self._category.value}
tags:
  - {self.format_tags(self._tags.value)}
"""

        filename = f"{output_directory.rstrip('/')}/{self._title.value.lower().replace(' ', '_').replace('/', '_') if self._title.value else 'no_title'}.{extension}"
        draft_filename = f"{filename}.draft"

        if os.path.exists(draft_filename) and not is_draft:
            os.remove(draft_filename)

        #  TODO: Handle the case when the file already exists and error with open
        with open(filename, "w") as file:
            file.write(frontmatter)
            file.write("---\n")
            file.write(self._textarea.text)

        return filename

    def predice_ai_tags(category: str, title: str) -> Optional[str]:
        # sourcery skip: instance-method-first-arg-name
        prompt = TAG_TEMPLATE.substitute(topic=category, title=title)
        try:
            response = httpx.post(
                OLLAMA_ENDPOINT,
                json={"prompt": prompt, **OLLAMA_CONFIG},
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            if response.status_code != 200:
                return None
        except Exception:
            return None

        return response.json()["response"].strip().split("\n")[0]

    def get_vscode_path():
        try:
            return subprocess.check_output(
                ["where" if os.name == "nt" else "which", "code"], shell=True
            ).decode("utf-8")
        except subprocess.CalledProcessError:
            return False

    def open_vscode(directory):
        try:
            subprocess.check_call(["code", directory])
            print(f"VSCode opened at {directory}")
        except subprocess.CalledProcessError:
            print("Failed to open VSCode")

    def read_markdown_file(file_path, start_line, end_line):
        with open(file_path, "r") as file:
            lines = file.readlines()[start_line - 1 : end_line]
            return "".join(lines)


# Use the functions
# open_vscode(get_vscode_path())
# print(read_markdown_file('phpunit_using_laravel_in_x_minutes.md', 6, 34))
