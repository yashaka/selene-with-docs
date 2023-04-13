# MIT License
#
# Copyright (c) 2015-2022 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from selene import browser, have, by, be

# app_url = f'file://{os.path.abspath(os.path.dirname(__file__))}/../resources/todomvcapp/home.html'
app_url = 'https://todomvc4tasj.herokuapp.com/'
# is_TodoMVC_loaded = ('return '
#                      '$._data($("#new-todo").get(0), "events").hasOwnProperty("keyup") && '
#                      '$._data($("#toggle-all").get(0), "events").hasOwnProperty("change") && '
#                      '$._data($("#todo-list").get(0), "events").hasOwnProperty("change") && '
#                      '$._data($("#clear-completed").get(0), "events").hasOwnProperty("click")')
is_TodoMVC_loaded = 'return (Object.keys(require.s.contexts._.defined).length === 39)'


class TestTodoMVC:
    def test_selene_demo(self):
        tasks = browser.all('#todo-list>li')
        active_tasks = tasks.by(have.css_class('active'))

        browser.open(app_url)
        browser.should(have.script_returned(True, is_TodoMVC_loaded))

        for task_text in ['1', '2', '3']:
            browser.element('#new-todo').set_value(task_text).press_enter()
        tasks.should(have.texts('1', '2', '3')).should(have.css_class('active').each)
        browser.element('#todo-count').should(have.text('3'))

        tasks[2].element('.toggle').click()
        active_tasks.should(have.texts('1', '2'))
        active_tasks.should(have.size(2))

        tasks.by(have.css_class('completed')).should(have.texts('3'))
        tasks.element_by(have.no.css_class('completed')).should(have.text('1'))
        tasks.by(have.no.css_class('completed')).should(have.texts('1', '2'))

        tasks.even.should(have.texts('2'))

        tasks.odd.should(have.texts('1', '3'))
        # or
        tasks.sliced(step=2).should(have.texts('1', '3'))

        tasks.sliced().should(have.texts('1', '2', '3'))
        # or
        tasks[::].should(have.texts('1', '2', '3'))

        browser.element(by.link_text('Active')).click()
        tasks[:2].should(have.texts('1', '2'))
        tasks[2].should(be.hidden)

        browser.element(by.id('toggle-all')).click()
        browser.element('//*[@id="clear-completed"]').click()
        tasks.should(have.size(0))
