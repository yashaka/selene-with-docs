# How to organize documentation

> We will provide some key points from [MkDocs User Guide][mkdocs-user-guide]
as well as specific notes for Selene documentation.

## File layout

Your documentation source should be written as regular Markdown files
(see [How to write documentation][syntax-guide]),
and placed in the documentation directory.
By default, this directory will be named `docs`
and will exist at the top level of your project,
alongside the `mkdocs.yml` configuration file.

- Name your files with lower case words separated by hyphen(s).  
For example, `quick-start.md`, `changelog.md` or `use-custom-webdriver.md`

!!! warning "Don't use names which begin with a dot"

    Files and directories with names which begin with a dot
    (for example: `.foo.md` or `.bar/baz.md`) are ignored by MkDocs,
    which matches the behavior of most web servers. There is no option to override this behavior.

The file layout you use determines the URLs that are used for the generated pages.
Given this layout, pages would be generated for the following URLs:

<!-- markdownlint-disable MD046 -->
=== "Layout"

    ```plain
    📁 docs/
    ├── 📁 user-guide/
        ├── 📄 getting-started.md
        └── 📄 configuration-options.md
    ├── 📄 index.md
    └── 📄 license.md
    ```

=== "URLs"

    /user-guide/getting-started/  
    /user-guide/configuration-options/  
    /  
    /license/
<!-- markdownlint-enable MD046 -->

## Navigation

The `nav` configuration setting in your `mkdocs.yml` file
defines which pages are included in the global site navigation menu
as well as the structure of that menu.

A minimal navigation configuration could look like this:

```yaml
nav:
    - Home: 'index.md'
    - About: 'about.md'
```

!!! warning "Avoid references to page headers in navigation menu"

    ```yaml
    nav:
    # ...
      - Release Process: CONTRIBUTING/#release-process  # This is BAD
    ```

- Write navigation section / sub-section / page title and related paths
without any quoting  
*(maybe it's contr-intuitive, but it's good for YAML syntax highlighting)*
- After completing new document **don't forget to update
navigation menu** in `mkdocs.yml` file.  
*(If it should be there.)*

## Selene docs structure

Selene has following file layout:  
==*(can be out-dated here, please look into `docs` folder
or ask project owner where to put new document)*==

!!! danger inline end "TBD"

    Need owner confirmation!

```plain
📁 docs/
├── 📁 contrib/
    ├── 📁 code/
        ├── 📄 code-conventions.md
        ├── 📄 how-to-contribute.md
        ├── 📄 release-workflow.md
    └── 📁 docs/
        ├── 📄 how-to-contribute.md
        ├── 📄 how-to-organize-docs.md
        ├── 📄 how-to-write-docs.md
├── 📁 examples/
    ├── 📄 ex-tbd-1.md
    └── 📄 ex-tbd-2.md
├── 📁 faq/
    ├── 📄 q-tbd-1.md
    └── 📄 q-tbd-2.md
├── 📁 guides/
    ├── 📄 g-tbd1.md
    └── 📄 g-tbd2.md
├── 📁 tutorials/
    ├── 📄 tut-tbd1.md
    └── 📄 tut-tbd2.md
├── 📄 changelog.md
├── 📄 index.md
└── 📄 license.md
```

Pay attention, that:

- `index.md` is almost full include (snippet) of README.md
from the root (except three links at the end).
Separate links are required because README is rendered on three place:
GitHub, PyPI and docs website.
- `license.md` and `changelog.md` are full snippets of
LICENSE.md and CHANGELOG.md from the root
- `how-to-contribute.md` is snippet of CONTRIBUTING.md from the root
(except two links at the end of the page)

How to use snippets, please refer to Markdown
[extension documentation][snippets-doc] page.

!!! danger "Approve images location"

    Need owner decision!

## Selene navigation structure

!!! danger "Approve nav structure"

    Need owner decision!

<!-- References -->
[mkdocs-user-guide]: https://www.mkdocs.org/user-guide/writing-your-docs/
[syntax-guide]: how-to-write-docs.md
[snippets-doc]: https://facelessuser.github.io/pymdown-extensions/extensions/snippets/
