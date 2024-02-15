# Frodown

![Frodown](./screenshot.png)

## Frontmatter + Markdown editor

This is a simple markdown editor with frontmatter support. It's built with _Python_ + a great _TUI (Terminal User Interface)_ called _Textual_ (+ info at [textualize.io](https://textualize.io).

It's a simple tool that I use to write my blog posts and other markdown files. My blog is built using [VuePress 2](https://v2.vuepress.vuejs.org) + [Hope](https://theme-hope.vuejs.press) theme.

## Features

- [x] Frontmatter support.
- [x] Markdown editor.
- [x] Save to file.
- [ ] Markdown cheatsheet.
- [ ] Markdown cheatsheet on sidebar.
- [ ] Markdown preview.
- [ ] Move categories and other constants to an env file.

## How to use

Change the constant in the `main.py` file to match your needs. Then, run the following commands:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

When you click on **[SAVE]**, it will be saved in the same directory as the original file with the same name as the title 'slugged' and the extension `.md`.

## License and credits

Frodown © 2024 by [Jose Cerrejon](https://github.com/jmcerrejon) is licensed under [CC BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1)

You can use it for free on your own. If you want to support me, you can!:

- [paypal.me/jmcerrejon](https://paypal.me/jmcerrejon)

- [Buy me a coffee](https://ko-fi.com/cerrejon)

- Bitcoin: 32XtfF8eKkWkAGJsHvBsjqsted5NKsGBcv
