# How to contribute to documentation

If you feel you have something to contribute,
stick to the same [contributing rules][contributing]
as for source code.
One key difference: name your branch
starting with `docs-`  
For instance, `docs-faq-custom-command` or `docs-ci-improve`

Before you start,
we recommend reading our two short pages:  
[How to organize docs][organizing-docs]
and
[How to write docs][writing-docs].

## How to preview docs

### Local deploy

For local docs deploy:

1. Get Selene code (clone / fork repo or pull PR)
2. In project root directory, execute:

    `poetry install --with docs`

3. Activate Python virtual environment. The easiest way is:

    `poetry shell`

4. Run mkdocs' local web server:

    `mkdocs serve`

5. Open URL in browser `http://127.0.0.1:8000/selene/`

While server is running, any changes in `docs` directory
will reload the browser tab.

To stop server press ++ctrl+c++ in your terminal
(where server was running).

!!! note "Editing included pages"

    When you edit "source" **root** page of include (snippet),
    for example, `README.md` for `index.md`.
    In that case you MUST to reload (stop & start)
    local web server manually to see your changes
    (because it watches only for file in `docs` folder)

### Web deploy

!!! danger "Not available at this moment"

    It's not possible *(not so easy, at least)*
    due to GitHub Pages deployment constraints
    (one website per repository)

## How to validate Markdown syntax

### Using VS Code extension

Install [markdownlint][markdownlint-extension] for VS Code.

Open **Problems** tab in VS Code ++ctrl+shift+m++, markdownlint warnings all begin with `MD###`.

### Using plugin for PyCharm

!!! danger inline end "TBD"

    Need investigation by PyCharm user!

==I'm not PyCharm user.
Quick search gave me this [Markdown](https://plugins.jetbrains.com/plugin/7793-markdown) plugin,
but in features list I can't see something "syntax checking",
"linter", etc.  
And one **deprecated** (old) plugin [Markdown Navigator](https://plugins.jetbrains.com/plugin/7896-markdown-navigator-enhanced/)  
Need to investigate.==

### Using npm package

If you have Node.js installed on your machine, you can use `markdownlint-cli2`
A fast, flexible, configuration-based command-line interface
for linting Markdown/CommonMark files with the `markdownlint` library.
This library (engine) is used in VS Code extension, mentioned above.

For installing and usage of this CLI utility,
please refer to its [GitHub page][markdownlint-cli2-github].

### Using CI job

!!! danger inline end "TBD"

    Need owner approvement and job setup.

<!-- References -->
[contributing]: ../code/how-to-contribute.md
[markdownlint-extension]: https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint
[markdownlint-cli2-github]: https://github.com/DavidAnson/markdownlint-cli2
[organizing-docs]: how-to-organize-docs.md
[writing-docs]: how-to-write-docs.md
