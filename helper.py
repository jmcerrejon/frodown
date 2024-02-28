import os


class Helper:
    def get_categories() -> list[str]:
        categories_file_path = "categories.txt"
        categories = ["General"]

        if os.path.exists(categories_file_path):
            with open(categories_file_path, "r") as file:
                categories = file.read().splitlines()

        return categories

    def get_textarea_example() -> str:
        return """# Title
![Alt](/path/to/image.jpg)

Intro text here
- - -
## Subtitle
"""

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

    def get_icon_by_category(category:str = "General") -> str:
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
            "Orange Pi": "fa-solid fa-microchip"
        }
        return icons_list.get(category, "fa-regular fa-newspaper")