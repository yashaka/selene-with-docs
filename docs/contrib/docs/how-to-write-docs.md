# How to write documentation

All documentation files should be written in Markdown documents (`.md`).

If you are not familiar with the Markdown syntax, check out Adam Pritchard's [Markdown Cheatsheet][markdown-cheatsheet] which includes the standard Markdown syntax as well as the extended GFM (GitHub Flavored Markdown) that we will be utilizing in this guide.

For consistency reason, we recommend you to use syntax given in this guide
(*not using available alternatives*)

!!! info

    Such blocks as: **Footnotes**, **Tables**, **Blockquotes**, **Inline HTML**
    are the same as described in cheat sheet, mentioned above.
    Please refer to it.

## Preferred Markdown syntax

### Headers

- Use hash (pound) character(s) to define H1-H6 headers.

`# H1`  
`## H2`  
`### H3`  
`#### H4`  
`##### H5`  
`###### H6`  

??? tip "How to suppress linter's warnings MD046"

    In most cases H1 will be the first line of the page.  
    If you use something specific lines at the beginning (meta-data, include, etc)
    and you need suppress (ignore) linter's warning,
    you can add special comment lines:  
    `<!-- markdownlint-disable MD046 -->`  
    `... ignored markdown block ...`  
    `<!-- markdownlint-enable MD041 -->`  

### Emphasis

- Use asterisks (\*) for emphasis (aka italics).
- Use double asterisks (\**) for strong emphasis (aka bold).
- Use double tilde (~~) for strikethrough text.
- Use double equals (==) for highlighted text.

<!-- markdownlint-disable MD046 -->
=== "Markdown"

    ```plain
    I'm *italics* text.  
    I'm **bold** text.  
    I'm ~~strikethrough~~ text.  
    I'm ==highlighted== text.
    ```

=== "Result"

    I'm *italics* text.  
    I'm **bold** text.  
    I'm ~~strikethrough~~ text.  
    I'm ==highlighted== text.
<!-- markdownlint-enable MD046 -->

### Lists

- Use minus (-) followed by space for unordered list.
- Use **four** spaces indentation for unordered lists.  
(in standard syntax it is two spaces,
and `markdownlint` will show warning MD007,
disable it or configure to 4 spaces in config file)
- Use four spaces indentation for paragraphs within list items (after blank line).
- To have a line break without a paragraph, you will need to use two trailing spaces.

<!-- markdownlint-disable MD046 -->
=== "Markdown"

    ```plain
    1. First ordered list item
    2. Another item
        - Unordered item
            - Nested item
    3. Third item

        Blank line and four space indentation for paragraph.
        This line  
        was interrupted by two trailing spaces.
    ```

=== "Result"

    1. First ordered list item
    2. Another item
        - Unordered item
            - Nested item
    3. Third item

        Blank line and four space indentation for paragraph.
        This line  
        was interrupted by two trailing spaces.
<!-- markdownlint-enable MD046 -->

### Links

- Use the reference links wherever possible.
- Reference text can be arbitrary and case-insensitive,
but use words in lower case separated by hyphen(s).
- For relative links to other pages in `docs` folder,
don't forget extension `.md`
- In rare and reasonable cases, you can use an inline-style link.
- Add HTML comment before reference list,
to distinct list from the rest of content.

<!-- markdownlint-disable MD046 -->
=== "Markdown"

    ```plain
    [Selene][selene-github] is cool,  
    especially with good [docs][home-docs].  
    [I'm an inline-style link](https://t.me/selene_py_ru)

    <!-- References -->
    [selene-github]: https://github.com/yashaka/selene/
    [home-docs]: ../../index.md
    ```

=== "Result"

    [Selene][selene-github] is cool, 
    especially with good [docs][home-docs].  
    [I'm an inline-style link](https://t.me/selene_py_ru)

    [selene-github]: https://github.com/yashaka/selene/
    [home-docs]: ../../index.md
<!-- markdownlint-enable MD046 -->

### Images

- For better accessibility, we encourage you
to specify alt text and title for images.

<!-- markdownlint-disable MD046 -->
=== "Markdown"

    ```plain
    Here's our logo (hover to see the title text):

    Inline-style: 
    ![selene logo](https://yashaka.github.io/selene/assets/images/apple-touch-icon.png "Selene logo")

    Reference-style: 
    ![alt text][logo]

    [logo]: https://yashaka.github.io/selene/assets/images/apple-touch-icon.png "Logo Title Text 2"
    ```

=== "Result"

    Here's our logo (hover to see the title text):

    Inline-style: 
    ![selene logo](https://yashaka.github.io/selene/assets/images/apple-touch-icon.png "Selene logo")

    Reference-style: 
    ![alt text][logo]

    [logo]: https://yashaka.github.io/selene/assets/images/apple-touch-icon.png "Logo Title Text 2"
<!-- markdownlint-enable MD046 -->

!!! question "Where to store images for individual page?"

    TO DO: After answer update example above and add statment about storing images

### Code and Syntax Highlighting

- Use only fenced code blocks (fenced by lines with three back-ticks ```).
- Write language identificator right after back-ticks (**without space**).
- For plain text (console output) use `plain` language identificator.

<!-- markdownlint-disable MD046 -->
=== "Markdown"

    ```plain
    from selene.support.shared import browser
    from selene import by, be, have

    browser.open('https://google.com/ncr')
    browser.element(by.name('q')).should(be.blank)\
    .type('selenium').press_enter()
    browser.all('.srg .g').should(have.size(10))\
    .first.should(have.text('Selenium automates browsers'))
    ```

=== "Result"

    ```python
    from selene.support.shared import browser
    from selene import by, be, have

    browser.open('https://google.com/ncr')
    browser.element(by.name('q')).should(be.blank)\
    .type('selenium').press_enter()
    browser.all('.srg .g').should(have.size(10))\
    .first.should(have.text('Selenium automates browsers'))
    ```
<!-- markdownlint-enable MD046 -->

### Horizontal Rule

- Use three hyphens (minuses) `---` between to blank lines
to insert horizontal rule
(if you really need to do that)

<!-- markdownlint-disable MD046 -->
=== "Markdown"

    ```plain
    text above the line

    ---

    text under the line
    ```

=== "Result"

    text above the line

    ---

    text under the line
<!-- markdownlint-enable MD046 -->

### Line Breaks

- Use **two trailing space every time**
when you want to insert new line in the same paragraph
on rendered page too (analog `<br>` in HTML).
- Use [semantic linefeeds][semantic-linefeeds],
wrapping lines by 72-80 characters
except for links and images and .md files in project root
(because GitHub renders each newline character).
- Paragraphs are separated by a blank line.

<!-- markdownlint-disable MD046 -->
=== "Markdown"

    ```plain
    Selene was inspired by Selenide from Java world.

    Tests with Selene can be built either in
    a simple straightforward "selenide' style
    or with PageObjects composed from Widgets
    i.e.  
    reusable element components.
    ```

=== "Result"

    Selene was inspired by Selenide from Java world.

    Tests with Selene can be built either in
    a simple straightforward "selenide' style
    or with PageObjects composed from Widgets
    i.e.  
    reusable element components.
<!-- markdownlint-enable MD046 -->

<!-- References -->
[markdown-cheatsheet]: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
[semantic-linefeeds]: https://rhodesmill.org/brandon/2012/one-sentence-per-line/
