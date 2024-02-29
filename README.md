# Frodown

![Frodown](./screenshot.png)

## Frontmatter + Markdown editor

This is a simple markdown editor with frontmatter support. It's built with _Python_ + a great _TUI (Terminal User Interface)_ called _Textual_ (+ info at [textualize.io](https://textualize.io)).

It's a simple tool that I use to write my blog posts and other markdown files. My blog is built using [VuePress 2](https://v2.vuepress.vuejs.org) + [Hope](https://theme-hope.vuejs.press) theme. Visit me at https://misapuntesde.com

## Features

- [x] Frontmatter support.
- [x] Markdown editor.
- [x] Save to a file.
- [x] Add a footer.
- [x] Light theme (because I think some people prefer brightness 🤷‍♂️).
- [x] Markdown cheat sheet on the sidebar.
- [x] Markdown zen mode & improvements.
- [x] Move categories and other constants to an environment or text file.
- [x] Save a draft & Open with the latest values if you quit without saving the information previously.
- [ ] If you have multi-language support on your site, create multiple markdown files.
- [ ] Implement AI to suggest tags and categories, or translate the article.
- [ ] Package it as a standalone app.

## How to use

Change the constant in the `main.py & categories.txt` files to match your needs. Then, run the following commands:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Clicking on **[Save]** will save it to the same directory with the title 'slugged' with the extension '.md'.

## License and credits

Frodown © 2024 by [Jose Cerrejon](https://github.com/jmcerrejon) is licensed under [CC BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1)

I'm using _Conventional Commits v1.0.0_. More information can be found at https://www.conventionalcommits.org/en/v1.0.0/.

You can use it for free on your own. If you want to support me, you can!:

- 🪙 [paypal.me/jmcerrejon](https://paypal.me/jmcerrejon)

- ☕️ [ko-fi.com > Buy me a coffee](https://ko-fi.com/cerrejon)

- 🟡 Bitcoin: 32XtfF8eKkWkAGJsHvBsjqsted5NKsGBcv
