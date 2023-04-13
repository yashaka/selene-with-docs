from selene import by, be, have, browser

__author__ = 'yashaka'

_elements = browser.all("#todo-list>li")

app_url = 'https://todomvc4tasj.herokuapp.com/'


def visit():
    browser.open(app_url)
    clear_completed_js_loaded = (
        "return $._data($('#clear-completed').get(0), 'events').hasOwnProperty('click')"
    )
    browser.with_(timeout=browser.config.timeout * 3).wait.for_(
        have.script_returned(True, clear_completed_js_loaded)
    )


def filter_active():
    browser.element(by.link_text("Active")).click()


def filter_completed():
    browser.element(by.link_text("Completed")).click()


def add(*task_texts):
    for text in task_texts:
        browser.element("#new-todo").should(be.enabled).set_value(text).press_enter()


def toggle(task_text):
    _elements.element_by(have.exact_text(task_text)).element(".toggle").click()


def should_be(*task_texts):
    _elements.by(be.visible).should(have.exact_texts(*task_texts))


def clear_completed():
    browser.element('#clear-completed').click()
