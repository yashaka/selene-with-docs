# Changelog

## > 2.0.0 release

TODOs:

- `config.quit_last_driver_on_reset` (`False` by default)?
- improve for other `all.*` methods (in addition to improved errors from `browser.all.element_by`)
- why in the past we had when outer_html this: `'<button class="destroy" type="submit" displayed:false></button>'`
  - but now we have this: `'<button class="destroy" type="submit"></button>'?`
    - can we improve it?
- add something like `element.click_with_offset`
- consider adding hold_driver_open_at_exit_on_failure
- case insensitive versions of conditions like have.attribute(...).value(...)
  - experimental impl was already added in 2.0.0a16
- consider adding more readable alias to by tuple, like in:
  `css_or_xpath_or_by: Union[str, tuple]`
- improve error messages
  - should we come back to the "actual vs expected" style in error messages?
- improve stacktraces
  - consider using something like `__tracebackhide__ = True`
- what about ActionChains?
  - with retries?
- what about soft assertions in selene?
- maybe somewhen in 3.0 consider adding selene.support.shared.selenide module
  - with selenide style api
    - like s, ss, open_url
    - SelenideElement#find, #find_all
    - ElementsCollection#find, #filter, #get
    - etc.

## < 2.0.0 release ? o_O

TODOs:

- manager or executor at `config._executor`?
- deprecate config.wait(entity) factory?
  - isn't it enough to have `config._build_wait_strategy(entity)`?
- decide on `config._reset_not_alive_driver_on_get_url` name
  - reset vs rebuild?
  - etc?
- decide on None as default in managed driver descriptor instead of ...
  taking into account that mypy does not like it
  - actually I tend to keep both `...` and `None`, yet using `...` as default
    in Selene's internals. But let's document this at least. 
    Mentioning also this: https://github.com/python/mypy/issues/7818
- consider a way to customize "locator description" [#439](https://github.com/yashaka/selene/issues/439)
  - consider storing "raw selector" of locator to be able to log it as it is [#438](https://github.com/yashaka/selene/issues/438)
  - consider storing `locator.name` and take it from class attribute name if Element object
    is used as descriptor (via `__set_name__` impl.)
    - while being a descriptor...
      check if `hassattr(owner, 'element')` (or context, or container?)
      then consider starting the search from the context 
      and make this configurable via `config.search_from_defined_context = True`
      (probably `False` by default)
      and being able to override somehow on element definition level
- ensure we can't element.type on invisible element; add test for that
- decide on have.size vs query.size
  - consider making have.size to work with elements too...
- review all `# type: ignore`
- review all typing.cast
- fix «too much screenshots»? if can reproduce
- what about accepting None as locator of Element?
  in such case it such element will just do nothing regardless of what command is called on it
  - even better, we can accept Locators in browser.element(here)!!!
    and so we can implement own behavior, locating some kind of proxy that skips all commands!
- deprecate `be.present`
- todo consider adding element.caching as lazy version of element.cached
- use `__all__` in selene api imports, etc
  - The variable `__all__` is a list of public objects of that module, as interpreted by `import *`. ... In other words, `__all__` is a list of strings defining what symbols in a module will be exported when `from module import *` is used on the module
- config.driver_proxy or config.driver_remote_proxy?

## 2.0.0rc? (to be released on ??.??.2023)

TODOs:

* implement run_cross_platform_with_fixture_and_custom_location_strategy example with:
  * location strategy
  * element actions logging to allure
  * jenkins pipeline with matrix job
* deprecate browser.switch_to?
  * add corresponding set of commands to be used as waiting commands via `browser.perform` 
    * make `command.switch_to_frame` to accept selene element?
    - add something like `browser.perform(switch_to_tab('my tab title'))`
          - maybe make browser.switch ... to work with retry logic
            or make separate command.switch...

## 2.0.0rc2 (to be released on 13.04.2023)

### Driver is guessed by config.driver_options too

Before:

  * `config.driver_name` was `'chrome'` by default

Now:

  * `config.driver_name` is `None` by default
    * and means "desired requested driver name"
  * setting `config.driver_options` usually is enough to guess the driver name,
    e.g., just by setting `config.driver_options = FirefoxOptions()`
    you already tell Selene to build Firefox driver.

### config.driver_service 

Just in case you want, e.g. to use own driver executable like:

```python
from selene import browser
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

browser.config.driver_service = Service('/path/to/my/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser.config.driver_options = chrome_options
```

## 2.0.0rc1.post1 (to be released on ??.??.2023)

* allow guessing local driver name based on config.driver_options
* examples with specifying binary location for driver, ignoring wdm

## 2.0.0rc1 (released on 11.04.2023)

### Changes

#### Any custom driver will now be automatically quit at exit

Any driver instance passed to `browser.config.driver` will be automatically quit at exit, unless `browser.config.hold_driver_at_exit = True`, that is `False` by default

#### Manually set driver can be still automatically rebuilt on next call to browser.open(url)

... if happened to be not alive, e.g. after quit or crash. This was relevant in the past, but not for manually set drivers. Not it works for all cases by default, including manually set driver by `browser.config.driver = my_driver_instance`. To disable this behavior set `browser.config._reset_not_alive_driver_on_get_url = False` (currently this option is still marked as experimental with `_` prefix, it may be renamed till final 2.0 release).

Once automatic rebuild is disabled, you can schedule rebuild on next access to driver by setting `browser.config.driver = ...` (besides ellipsis, setting to `None` also works). This is actually what is done inside `browser.open(url)` if `browser.config._reset_not_alive_driver_on_get_url = True` and driver is not alive.

There is another "rebuild" option in config that is disabled by default: `browser.config.rebuild_not_alive_driver`. It is used to rebuild driver on **any** next access to it, if it is not alive. This is different from `browser.config._reset_not_alive_driver_on_get_url` that resets driver (scheduling to be rebuilt) **only** on next call to `browser.open(url)`. Take into account that enabling this option may leed to slower tests when running on remote drivers, because it will check if driver is alive on any access to it, not only on `browser.open(url)`.


#### «browser» term is deprecated in a lot of places

... except `Browser` class itself, of course (but this might be changed somewhere in 3.0🙃)

For example, `config.browser_name` is deprecated in favor of `config.driver_name`. Main reason – «browser» term is not relevant to mobile testing, where in a lot of cases we test user actions in app, not browser.

### New

#### `from selene import browser`

– to be used instead of `from selene.support.shared import browser`. 

No difference between Config and SharedConfig anymore. The new, completely refactored, Config is now used everywhere and allows to customize browser instance in a more convenient way.

Adds ability to use `browser.with_(**config_options_to_override)` to create new browser instance, for example: 
     
```python
from selene import browser

chrome = browser
firefox = browser.with_(driver_name='firefox')
edge = browser.with_(driver_name='edge')
...
# customizing all browsers at once:
browser.config.timeout = 10
```
  
as alternative to:
    
```python
from selene import Browser, Config

chrome = Browser(Config())
firefox = Browser(Config(driver_name='firefox'))
edge = Browser(Config(driver_name='edge'))

...

# customizing all browsers:
chrome.config.timeout = 10
firefox.config.timeout = 10
edge.config.timeout = 10
```

#### `browser.config.driver_options` + `browser.config.driver_remote_url`

Finally, you can delegate building driver to config manager by passing `driver_options` and `driver_remote_url` to it:

```python
import dotenv
from selenium import webdriver
from selene import browser, have


def test_complete_task():
  options = webdriver.ChromeOptions()
  options.browser_version = '100.0'
  options.set_capability(
    'selenoid:options',
    {
      'screenResolution': '1920x1080x24',
      'enableVNC': True,
      'enableVideo': True,
      'enableLog': True,
    },
  )
  browser.config.driver_options = options  # <- 🥳
  project_config = dotenv.dotenv_values()
  browser.config.driver_remote_url = (  # <- 🎉🎉🎉
    f'https://{project_config["LOGIN"]}:{project_config["PASSWORD"]}@'
    f'selenoid.autotests.cloud/wd/hub'
  )

  browser.open('http://todomvc.com/examples/emberjs/')
  browser.should(have.title_containing('TodoMVC'))

  browser.element('#new-todo').type('a').press_enter()
  browser.element('#new-todo').type('b').press_enter()
  browser.element('#new-todo').type('c').press_enter()
  browser.all('#todo-list>li').should(have.exact_texts('a', 'b', 'c'))
```

#### `browser.open()` without args

Will just open driver or do nothing if driver is already opened.

Can also load page from `browser.config.base_url` if it is set and additional experimental `browser.config._get_base_url_on_open_with_no_args = True` option is set (that is `False` by default).

#### Automatic driver rebuilding still happens on `browser.open`, but...

but can be configured as follows:

* can be disabled by setting `browser.config.__reset_not_alive_driver_on_get_url = False`,
  that is `True` by default
* can be enabled on any explicit or implicit call to `browser.config.driver`,
  if set `browser.config.rebuild_not_alive_driver = True` (that is `False` by default)

#### Appium support out of the box:)

Yet you have to install it manually. But given installed via `pip install Appium-Python-Client` or something like `poetry add Appium-Python-Client`, running tests on mobile devices is as easy as...

##### Running locally against Appium server:

```python
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have

android_options = UiAutomator2Options()
android_options.new_command_timeout = 60
android_options.app = 'wikipedia-alpha-universal-release.apk'
android_options.app_wait_activity = 'org.wikipedia.*'
browser.config.driver_options = android_options
# # Possible, but not needed, because will be used by default:
# browser.config.driver_remote_url = 'http://127.0.0.1:4723/wd/hub'

by_id = lambda id: (AppiumBy.ID, f'org.wikipedia.alpha:id/{id}')

# GIVEN
browser.open()
browser.element(by_id('fragment_onboarding_skip_button')).click()

# WHEN
browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
browser.element(by_id('search_src_text')).type('Appium')

# THEN
browser.all(by_id('page_list_item_title')).should(
  have.size_greater_than(0)
)
```

##### Running remotely against Browserstack server:

```python
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have

options = UiAutomator2Options()
options.app = 'bs://c700ce60cf13ae8ed97705a55b8e022f13c5827c'
options.set_capability(
  'bstack:options',
  {
    'deviceName': 'Google Pixel 7',
    'userName': 'adminadminovych_qzqzqz',
    'accessKey': 'qzqzqzqzqzqzqzqzqzqz',
  },
)
browser.config.driver_options = options
browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'

by_id = lambda id: (AppiumBy.ID, f'org.wikipedia.alpha:id/{id}')

# GIVEN
browser.open()  # not needed, but to explicitly force appium to open app

# WHEN
browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
browser.element(by_id('search_src_text')).type('Appium')

# THEN
browser.all(by_id('page_list_item_title')).should(
  have.size_greater_than(0)
)

```

#### A lot of other local, remote and mobile test examples at...

https://github.com/yashaka/selene/tree/master/examples

#### autocomplete for entity.with_(HERE)

### Other

#### Deprecated 

- `browser.save_screenshot` in favor of `browser.get(query.screenshot_saved())`
- `browser.save_page_source` in favor of `browser.get(query.page_source_saved())`
- `browser.last_screenshot` in favor of `browser.config.last_screenshot`
- `browser.last_page_source` in favor of `browser.config.last_page_source`
- `match.browser_has_js_returned` in favor of `match.browser_has_script_returned`
- `have.js_returned` in favor of `have.script_returned`
- `have.js_returned_true(...)` in favor of `have.script_returned(True, ...)`
- `browser.config.get_or_create_driver`
- `browser.config.reset_driver`
  - use `selene.browser.config.driver = ...`
- `browser.config.browser_name` in favor of `browser.config.driver_name`

#### Removed

- from selene.support.shared import SharedConfig, SharedBrowser
- from selene.core.entity import BrowserCondition, ElementCondition, CollectionCondition 

#### Removed deprecated 
- shared.browser.config.desired_capabilities
- shared.browser.config.start_maximized
- shared.browser.config.start_maximized
- shared.browser.config.cash_elements
- shared.browser.config.quit_driver
- shared.browser.latest_page_source
- shared.browser.quit_driver
- shared.browser.set_driver
- shared.browser.open_url
- shared.browser.elements
- shared.browser.wait_to
- shared.browser.title
- shared.browser.take_screenshot
- jquery_style_selectors

#### Removed not deprecated

- shared.browser.config.Source
  - renamed to shared.browser.config._Source. 
    Currently, is used nowhere in Selene
- shared.browser.config.set_driver (getter and setter)
- shared.browser.config.counter
  - use shared.browser.config._counter instead, and better – not use it;)
- shared.browser.config.generate_filename
  - use shared.browser.config._generate_filename instead, and better – not use it;)

## 2.0.0b15-b17

### Dependencies
- update selenium (with weakened dependency to >=4.4.3)
- update webdriver_manager (with weakened dependency to >=3.8.5)

## 2.0.0b14 (released on 06.10.2022)

### NEW

#### command.js.set_style_property(name, value)

```python
from selene.support.shared import browser
from selene import command

# calling on element
overlay = browser.element('#overlay')
overlay.perform(command.js.set_style_property('display', 'none'))

# can be also called on collection of elements:
ads = browser.all('[id^=google_ads][id$=container__]')
ads.perform(command.js.set_style_property('display', 'none'))
```


#### added conditions: `have.values` and `have.values_containing`

#### all conditions like `have.texts` & `have.exact_texts` – flatten passed lists of texts

This allows to pass args as lists (even nested) not just as varagrs. 

```python
from selene.support.shared import browser
from selene import have

"""
# GIVEN html page with:
<table>
  <tr class="row">
    <td class="cell">A1</td><td class="cell">A2</td>
  </tr>
  <tr class="row">
    <td class="cell">B1</td><td class="cell">B2</td>
  </tr>
</table>
"""

browser.all('.cell').should(
    have.exact_texts('A1', 'A2', 'B1', 'B2')
)

browser.all('.cell').should(
    have.exact_texts(['A1', 'A2', 'B1', 'B2'])
)

browser.all('.cell').should(
    have.exact_texts(('A1', 'A2', 'B1', 'B2'))
)

browser.all('.cell').should(
    have.exact_texts(
        ('A1', 'A2'),
        ('B1', 'B2'),
    )
)
```

#### removed trimming text on conditions like have.exact_text, have.texts, etc.

because all string normalization is already done by Selenium Webdriver.

##### but added query.text_content to give access to raw element text without space normalization

## 2.0.0b13 (released on 04.10.2022)

### NEW

### have.text, have.exact_text, have.texts and have.exact_texts strip/trim text when matching

#### config.window_width and config.window_height can be set separately

Now, you can set only one axis dimension for the browser, and it will change it on `browser.open`. Before it would change browser window size only if both width and height were set;)

#### access to self.locate() as `element` or `self` from the script passed to element.execute_script(script_on_self, *arguments)

Examples: 

```python
from selene.support.shared import browser

browser.element('[id^=google_ads]').execute_script('element.remove()')
# OR
browser.element('[id^=google_ads]').execute_script('self.remove()')
'''
# are shortcuts to
browser.execute_script('arguments[0].remove()', browser.element('[id^=google_ads]')())
'''

browser.element('input').execute_script('element.value=arguments[0]', 'new value')
# OR
browser.element('input').execute_script('self.value=arguments[0]', 'new value')
'''
# are shortcuts to
browser.execute_script('arguments[0].value=arguments[1]', browser.element('input').locate(), 'new value')
'''
```

#### `collection.second` shortcut to `collection[1]`

#### `element.locate() -> WebElement`, `collection.locate() -> List[WebElement]` [#284](https://github.com/yashaka/selene/issues/284)

... as more human-readable aliases to element() and collection() correspondingly

#### `entity.__raw__`

It's a «dangled» property and so consider it an experimental/private feature. 
For element and collection – it's same as `.locate()`.
For `browser` it's same as `.driver` ;)

Read more on it at this [comment to #284](https://github.com/yashaka/selene/issues/284#issuecomment-1265619606)

... as aliases to element(), collection() correspondingly

### NEW: DEPRECATED: 

#### element._execute_script(script_on_self, *args)

... in favor of .execute_script(script_on_self, *arguments) that uses access to arguments (NOT args!) in the script.

#### collection.filtered_by(condition) in favor of collection.by(condition)

#### browser.close_current_tab()

Deprecated because the «tab» term is not relevant for mobile context. 
Use a `browser.close()` or `browser.driver.close()` instead.

The deprecation mark was removed from the `browser.close()` correspondingly.

#### `browser.clear_session_storage()` and `browser.clear_local_storage()`

Deprecated because of js nature and not-relevance for mobile context;
Use `browser.perform(command.js.clear_session_storage)` and `browser.perform(command.js.clear_local_storage)` instead

### NEW: BREAKING CHANGES

#### arguments inside script passed to element.execute_script(script_on_self, *arguments) starts from 0

```python
from selene.support.shared import browser

# before this version ...
browser.element('input').execute_script('arguments[0].value=arguments[1]', 'new value')
# NOW:
browser.element('input').execute_script('element.value=arguments[0]', 'new value')
```

#### removed earlier deprecated 

- `browser.elements(selector)` in favor of `browser.all(selector)`
- `browser.ss(selector)` in favor of `browser.all(selector)`
- `browser.s(selector)` in favor of `browser.element(selector)`
- `element.get_actual_webelement()` in favor of `element.locate()`
- `collection.get_actual_webelements()` in favor of `collection.locate()`

#### renamed collection.filtered_by_their(selector, condition) to collection.by_their(selector, condition) 

#### removed collection.should_each ... [#277](https://github.com/yashaka/selene/issues/277)

- ... and ability to pass element_condition to `collection.should(HERE)`
- Use instead: `collection.should(element_condition.each)`
  - like in `browser.all('.selene-user').should(hava.css_class('cool').each)`

## 2.0.0b12 (released on 26.09.2022)

### NEW: collection.should(condition.each) [#277](https://github.com/yashaka/selene/issues/277)

The older style is totally **deprecated** now:
- Instead of:
  - `collection.should(element_condition)` and `collection.should_each(element_condition)`
- Use:
  - `collection.should(element_condition.each)`
  - see more examples at [tests/integration/condition_each_test.py](https://github.com/yashaka/selene/tree/master/tests/integration/condition_each_test.py)

### NEW: BREAKING CHANGE: removed SeleneElement, SeleneCollection, SeleneDriver

use instead:

```python
import selene

element: selene.Element = ...
collection: selene.Collection = ...
browser: selene.Browser = ...
```

or:

```python
from selene import Element, Collection, Browser

element: Element = ...
collection: Collection = ...
browser: Browser = ...
```

## 2.0.0b11 (released on 24.09.2022)

### NEW: upgraded selenium to 4.4.3 & webdriver-manager to 3.8.3

### BREAKING CHANGE: removed 'opera' support for shared.browser.config.browser_name

see reasons at:
- [Selenium Changelog for 4.3.0](https://github.com/SeleniumHQ/selenium/blob/31190f8edd801a2ead8ba3d49982cbdbc838885d/py/CHANGES#L22)
- [[🐛 Bug]: Opera Browser in Selenium 4 Usage](https://github.com/SeleniumHQ/selenium/issues/10835)

## 2.0.0b10 (released on 14.09.2022)

### NEW: BREAKING CHANGE: removed deprecated selene.core.entity.Collection.:

- `caching(self)` in favor of `cashed(self)`
- `all_by(self, condition) -> Collection` in favor of `by(conditioin)`
- `filter_by(self, condition) -> Collection` in favor of `by(condition)`
- `find_by(self, condition) -> Element`
- `size(self) -> int` in favor of `__len__(self)`

## 2.0.0b9 (released on 14.09.2022)

### NEW: `browser.all(selector).by(condition)` to filter collection

```python
import examples.run_cross_platform.wikipedia_e2e_tests.utils.locators
from selene.support.shared import browser
from selene import have

browser.open('https://todomvc.com/examples/emberjs/')
browser.element('#new-todo').type('a').press_enter()
browser.element('#new-todo').type('b').press_enter()
browser.element('#new-todo').type('c').press_enter()

examples.run_cross_platform.wikipedia_e2e_tests.utils.locators.by(have.text('b')).first.element('.toggle').click()

examples.run_cross_platform.wikipedia_e2e_tests.utils.locators.by(have.css_class('active')).should(have.texts('a', 'c'))
examples.run_cross_platform.wikipedia_e2e_tests.utils.locators.by(have.no.css_class('active')).should(have.texts('b'))
```

Hence, considering to deprecate:
- `collection.filtered_by(condition)` in favor of `collection.by(condition)`
- `collection.element_by(condition)` in favor of `collection.by(condition).first`

### NEW: `collection.even` and `collection.odd` shortcuts

```python
from selene.support.shared import browser
from selene import have

browser.open('https://todomvc.com/examples/emberjs/')

browser.element('#new-todo').type('1').press_enter()
browser.element('#new-todo').type('2').press_enter()
browser.element('#new-todo').type('3').press_enter()

browser.all('#todo-list>li').even.should(have.texts('2'))
browser.all('#todo-list>li').odd.should(have.texts('1', '3'))
```

### NEW: defaults for all params of `collection.sliced(start, stop, step)`

Now you can achieve more readable `collection.sliced(step=2)` instead of awkward `collection.sliced(None, None, 2)`

Remember that you still can use less readable but more concise `collection[::2]` ;)

### DEPRECATED:

- selene.core.entity.SeleneElement
  - you can use selene.core.entity.Element
- selene.core.entity.SeleneCollection
  - you can use selene.core.entity.Collection
- selene.core.entity.SeleneDriver
  - you can use selene.core.entity.Browser

### NEW: BREAKING CHANGE: removed deprecated

- selene.browser module
- selene.browsers module
- selene.bys module
- selene.driver module
- selene.wait module
- selene.elements module
- selene.core.entity.Browser:
  - .quit_driver(self) in favor of .quit(self)
  - .wrap(self, webdriver) in favor of Browser(Config(driver=webdriver))
  - .find(self, css_or_xpath_or_by: Union[str, tuple]) -> Element:
    - in favor of .element(self, selector) -> Element
  - .find_all(self, css_or_xpath_or_by: Union[str, tuple]) -> Collection:
    - in favor of .all(self, selector) -> Collection
  - .find_elements in favor of browser.driver.find_elements
  - .find_element in favor of browser.driver.find_element
- selene.core.entity.Collection:
  - .should(self, condition, timeout)
    - in favor of selene.core.entity.Collection.should(self, condition)
      with ability to customize timeout via collection.with_(timeout=...).should(condition)
  - .should_each(self, condition, timeout)
    - in favor of selene.core.entity.Collection.should_each(self, condition)
      with ability to customize timeout via collection.with_(timeout=...).should_each(condition)
  - .assure*(self, condition) -> Collection
  - .should_*(self, condition) -> Collection
- selene.core.entity.Element:
  - .should(self, condition, timeout)
    - in favor of selene.core.entity.Element.should(self, condition)
      with ability to customize timeout via element.with_(timeout=...).should(condition)
  - .assure*(self, condition) -> Element
  - .should_*(self, condition) -> Element
  - .caching(self)
  - .find(self, css_or_xpath_or_by: Union[str, tuple]) -> Element
  - .find_all(self, css_or_xpath_or_by: Union[str, tuple]) -> Collection
  - .parent_element(self) -> Element
    - use .element('..') instead
  - .following_sibling(self) -> Element
    - use .element('./following-sibling::*') instead
  - .first_child(self) -> Element
    - use .element('./*[1]')) instead
  - .scroll_to(self) -> Element
    - use .perform(command.js.scroll_into_view) instead
  - .press_down(self) -> Element
    - use .press(Keys.ARROW_DOWN) instead
  - .find_element(self, by, value)
  - .find_elements(self, by, value)
  - .tag_name(self)
  - .text(self)
  - .attribute(self, name)
  - .js_property(self, name)
  - .value_of_css_property(self, name)
  - .get_attribute(self, name)
  - .get_property(self, name)
  - .is_selected(self)
  - .is_enabled(self)
  - .is_displayed(self)
  - .location(self)
  - .location_once_scrolled_into_view(self)
  - .size(self)
  - .rect(self)
  - .screenshot_as_base64(self)
  - .screenshot_as_png(self)
  - .screenshot(self, filename)
  - .parent(self)
  - .id(self)


## 2.0.0b8 (released on 05.09.2022)

### NEW: `selene.support._logging.wait_with(context, translations)`

Added selene.support._logging experimental module with «predefined recipe» of wait_decorator for easier logging of Selene waiting commands (yet riskier, cause everything marked as experimental is a subject to change).

Now, given added allure dependency to your project, you can configure logging Selene commands to Allure report as simply as:

```python
from selene.support.shared import browser
from selene import support
import allure_commons

browser.config._wait_decorator = support._logging.wait_with(
  context=allure_commons._allure.StepContext
)
```

... or implement your own version of StepContext – feel free to use [Alure's context manager](https://github.com/allure-framework/allure-python/blob/481ea54759b0d8f6aa083a9f70f66cca33cae67c/allure-python-commons/src/_allure.py#L151) as example or the one from Selene's [browser__config__wait_decorator_with_decorator_from_support_logging_test.py](https://github.com/yashaka/selene/tree/master/tests/integration/shared_browser/browser__config__wait_decorator_with_decorator_from_support_logging_test.py) test.

You also can pass a list of translations to be applied to final message to log, something like:

```python
from selene.support.shared import browser
from selene import support
import allure_commons

browser.config._wait_decorator = support._logging.wait_with(
  context=allure_commons._allure.StepContext,
  translations=(
        ('browser.element', '$'),
        ('browser.all', '$$'),
  )
)
```

But check the default value for this parameter, maybe you'll be fine with it;)

And remember, the majority of selene extensions from the support.* package, including its `_logging` module – are things you'd better implement on your side to be less dependent to 3rd party helpers;) Feel free to Copy&Paste it into your code and adjust to your needs.

## 2.0.0b7 (released on 02.09.2022)
- BREAKING_CHANGE: change type of config._wait_decorator to access entities, not just commands on them
  - from `Callable[[F], F]`
  - to `Callable[[Wait[E]], Callable[[F], F]]`
  - i.e. now it should be not a simple decorator 
    that maps function F to a new F with for example added logging,
    but it should be «decorator with parameter»
    or in other words – a «decorator factory» function 
    that based on passed parameter of Wait type will return an actual decorator
    to be applied to the main logic of waiting inside Wait#for_ method.
  - This change will allow inside the decorator
    to access entities (browser, element, element-collection),
    for example, to log them too;)
  - see examples at:
    - simpler one: [examples/log_all_selene_commands_with_wait.py](https://github.com/yashaka/selene/tree/master/examples/log_all_selene_commands_with_wait.py)
    - more «frameworkish» one: [examples/log_all_selene_commands_with_wait__framework](https://github.com/yashaka/selene/tree/master/examples/log_all_selene_commands_with_wait__framework)


## 2.0.0b6 (released on 31.08.2022)
- NEW: added "opera" and "edge" support for shared browser
  - example:

    ```python
    from selene.support.shared import browser

    # browser.config.browser_name = 'opera'
    browser.config.browser_name = 'edge'
    ```

- NEW: added config._wait_decorator
  - decorating Wait#for_ method 
    - that is used when performing any element command 
      and assertion (i.e. should)
    - hence, can be used to log corresponding commands with waits
      and integrate with something like allure reporting;)
  - prefixed with underscore, indicating that method is experimental,
    and can be e.g. renamed, etc.
  - see example at [examples/log_all_selene_commands_with_wait.py](https://github.com/yashaka/selene/tree/master/examples/log_all_selene_commands_with_wait.py)

- NEW: added config.click_by_js [#420](https://github.com/yashaka/selene/issues/420)
  - for usage like in:

    ```python
    from selene.support.shared import browser
    
    # browser.config.click_by_js = True
    # '''
    # if we would want to make all selene clicks to work via JS
    # as part of some CRAZY workaround, or maybe to make tester faster o_O :p
    # (it was a joke, nothing will be much faster :D with click via js)
    # '''
    
    button = browser.element('#btn').with_(click_by_js=True)
    '''
    to make all clicks for element('#btn') to work via js
    as part of some workaround ;)
    '''
    
    button.click()
    ...
    button.click()
    ```

## 2.0.0b5 (released on 24.06.2022)
- NEW: added command.js.*:
  - remove
  - set_style_display_to_none
  - set_style_display_to_block
  - set_style_visibility_to_hidden
  - set_style_visibility_to_visible
  Example: 
  ```
  browser.all('[id^=google_ads]').perform(command.js.remove)
  ```


## 2.0.0b4 (released on 15.06.2022)
- NEW: upgrade selenium to 4.2.0 & webdriver-manager to 3.7.0
- FIX: set_window_size in shared.browser.open
- FIX: provide correct chrome type for wdm 

## 2.0.0b3 (released on 29.05.2022)
- added support of python 3.10.* [#393](https://github.com/yashaka/selene/issues/393)
- upgraded webdriver-manager to 3.5.4 [#408](https://github.com/yashaka/selene/issues/393)

## 2.0.0b2 (released on 29.03.2022)
- first steps on simplifying the current browser management, 
  yet making it more powerful
  - now you can pass a lambda to `browser.config.driver = HERE`
    providing more smart logic of driver management
    see a dummy example at this [test](https://github.com/yashaka/selene/tree/master/tests/acceptance/custom_driver_source/test_adding_todos.py)

## 2.0.0b1 (to be released on 23.02.2022)
- added support selenium 4.1 [#375](https://github.com/yashaka/selene/issues/375)
  - the =4.1 version is frozen/hardcoded as dependency
    - without backwards compatibility to selenium 3
      - the newly added service arg have been added to automatic driver management on the selene side 
        - yet, if anyone needs backwards compatibility, we can consider implementing it in following patches, feel free to file an issue;)
  - fixed [#398](https://github.com/yashaka/selene/issues/398)
- Upgrade [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) 3.5.0 -> 3.5.3 ([see changes](https://github.com/SergeyPirogov/webdriver_manager/compare/v3.5.0...v.3.5.3))
- removed deprecation
  - from:
    - collection.should_each(element_condition)
      - reason:
        - making collection.should(condition) so smart that it can accept both collection_condition and element_condition might be not a good idea – it violates KISS
        - maybe keeping things simpler with extra method like should_each is better...
        - let's see...
    - element.send_keys(keys)
      - reason:
        - yes, send_keys is low level, but sometimes somebody needs this low level style, because of the nature and context of send_keys usage, like sending keys to hidden fields
        - yet not sure about this decision... let's see...

## 2.0.0a40 (released on 09.10.2021)
- added `browser.config.wait_for_no_overlap_found_by_js` (`False` by default)
  - making following element methods to wait for no overlap:
    - type(text)
    - set_value(value)
    - press(*keys)
    - clear()
    - submit()
    - double_click()
      - btw normal `.click()` does not need it because have such waiting built in
    - context_click()
    - hover()

## 2.0.0a39 (released on 26.07.2021)
- Upgrade [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) 3.4.1 -> 3.4.2 ([see changes](https://github.com/SergeyPirogov/webdriver_manager/compare/v3.4.1...v.3.4.2))

## 2.0.0a38 (released on 05.05.2021)
- Upgrade [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) 3.3.0 -> 3.4.1 ([see changes](https://github.com/SergeyPirogov/webdriver_manager/compare/v3.3.0...v.3.4.1))

## 2.0.0a37 (released on 24.04.2021)
- Upgrade [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) 2.3.0 -> 3.3.0 [#299](https://github.com/yashaka/selene/issues/299)
- New release and publish process of selene [#246](https://github.com/yashaka/selene/issues/246#issuecomment-825897200)

## 2.0.0a36 (released on 30.03.2021)
Contributors release.
- Moved selene from Pipenv to [Poetry](https://python-poetry.org/) as a greater python dependency resolver of 2021 (see #302).
- Moved to a new release process with Poetry: added bash aliases in `./.run/*.sh` (see #304).
- Moved from setup.py and setup.cfg to pyproject.toml config-file.
- Updated README.md "Release process".
- Updated CONTRIBUTING.md with `black` and `pylint` job description.

## 2.0.0a35 (released on 27.03.2021)
- added command.js.click
- if you set driver for `shared.browser` manually via `browser.config.driver = ...`
  now it will automatically close previous driver, if it is alive
- in selene 1.0 if you could do mixed driver management, 
  like: use automatic driver, then manual, then automatic...
  in selene 2.0 this behaviour was broken, and this version fixes this;)
- deprecated `shared.config.quit_driver`; use `shared.config.reset_driver` instead
  - actually, you don't need this method,
    in most cases you just need `shared.browser.quit()` – use it if you don't know what you do;)
- fixed `browser.switch_to_tab(index_or_name)` when arg is of `int` type    
    
## 2.0.0a34 (released on 22.12.2020)
- fixed [#231](https://github.com/yashaka/selene/issues/225): Need additional option to turn off logging outerHTML
  - added `support.shared.config.log_outer_html_on_failure` (`False` by default)

## 2.0.0a33 (released on 10.09.2020)
- fixed [#225](https://github.com/yashaka/selene/issues/225): Failed to get last_screenshot from shared browser if element with custom config failed

## 2.0.0a32 (released on 10.09.2020)
- broken release:)

## 2.0.0a31 (released on 31.07.2020)
- fixed type hints in `*.should(here)`
  - latest PyCharm 2020.2 revealed the hidden issue with typing

## 2.0.0a30 (released on 30.07.2020)
- fixed `selene.support.shared.browser.with_`
  - to return sharedbrowser instance instead of browser instance
- made `browser.config.hold_browser_open` to influence browser quit logic 
  - even if set after calling `browser.open` or resetting `browser.config.driver`

## 2.0.0a29 (released on 30.07.2020)
- fixed shared browser automatic quit on process exit
  - that led to session error 
    in case you quit shared browser manually in your fixture

## 2.0.0a28 (released on 21.05.2020)
- added support of xpath to start with `(` in `s(selector)`, etc.
  - example: `ss('(//h1|//h2)[contains(text(), "foo")]').should(have.size(10))`

## 2.0.0a27 (released on 19.05.2020)
- fixed command.js.type and configuration.type_by_js + element.type

## 2.0.0a26 (released on 19.05.2020)
- if driver was set like `shared.config.driver = my_custom_driver`
  - then it's not mandatory to call `shared.browser.open` first
    
## 2.0.0a25 (released on 18.05.2020)
- fixing [#172](https://github.com/yashaka/selene/issues/172)
  - added `shared.config.set_driver: callable[[], webdriver]`
    as alternative to `shared.config.driver: webdriver`
    - now if config.set_driver is set - it will be used 
      to create and reload the driver instance according to your needs
    - setting `shared.config.driver = my_driver` is equivalent to setting 
      then `shared.config.set_driver = lambda: my_driver`
    - only `shared.browser.open(url)` now makes `set_driver` 
      to be triggered on first start and if driver was crashed or quit
      - i.e. if driver is crashed
        any further action on `shared.browser.element` will crash too
        unless you call `shared.browser.open` again
        - browser.open will also crash 
          if you used `shared.config.driver = my_driver` before
- **removed** implementation of "re-creating browser" if shared.config.browser_name was changed
  - this should make shared.browser more friendly with appium
  - and nevertheless shared.config should be used only "after quit and before open"... 
      
    
## 2.0.0a24 (to be released on 17.05.2020)
- fixed [#210](https://github.com/yashaka/selene/issues/210)
  - when installing using pip -- unicodedecodeerror: 'charmap' codec can't decode byte
  
## 2.0.0a23 (released on 15.04.2020)

- fixed element.cached to not fail on non-existing element

- fixed conditions that "compare lists" (like "have.exact_texts")
  - failed earlier if one collection (expected or actual) was empty

- added logging of webelement outer html to the error message of failed waiting for element
  - if actually webelement was found, but something was wrong with it (like hidden or non-interactable)
  
- improved errors from browser.all.element_by
  - TODO: improve for other all.* methods

was:

```
timed out after 4s, while waiting for:
browser.all(('css selector', '#task-list>li')).element_by(has exact text a).double click
reason: assertionerror: cannot find element by condition «has exact text a» from webelements collection:
[[]]
```

now:

```
timed out after 4s, while waiting for:
browser.all(('css selector', '#task-list>li')).element_by(has exact text a).double click

reason: assertionerror: 
	cannot find element by condition «has exact text a» 
	among browser.all(('css selector', '#task-list>li'))
	actual webelements collection:
	[]
```

  
## 2.0.0a22 (released on 20.03.2020)

- fixed [#206 – "after manually quitting, setting a new driver fails"](https://github.com/yashaka/selene/issues/206)
- fixed `have.texts` when actual collection has bigger size than actual
- added (yet marked with "experimental" warning)
  - `element_by_its`
  - `filtered_by_their`
  - ... see code examples below:

```
# given
#
#    .result
#        .result-title
#        .result-url
#        .result-snippet

# in addition to

results = browser.all('.result')
results.element_by(lambda result: have.text('browser tests in python')(
                          result.element('.result-title')))\
    .element('.result-url').click()

# you can now write:
results.element_by_its('.result-title', have.text('browser tests in python'))
    .element('.result-url').click()

# results.filtered_by_their('.result-title', have.text('python'))
    .should(have.size(...))

# or even
class result:
    def __init__(self, element):
        self.element = element
        self.title = self.element.element('.result-title')
        self.url = self.element.element('.result-url')

result(results.element_by_its(lambda it: result(it).title, have.text('browser tests in python')))\
    .url.click()

# it's yet marked as experimental because probably it would be enough
# to make it possible to accept callable[[element], bool] in element_by to allow:

results.element_by(
    lambda it: it.element('.result-title').matching(have.text('browser tests in python')))
    .element('.result-url').click()

# moreover... if failed, the error becomes weird if using lambdas:

# timed out after 4s, while waiting for:
# browser.all(('css selector', '.result')).element_by(<function collection.element_by_its.<locals>.<lambda> at 0x10df67f28>).element(('css selector', '.result-url')).click
# reason: assertionerror: cannot find element by condition «<function collection.element_by_its.<locals>.<lambda> at 0x10df67f28>» from webelements collection:

```
  -  
## 2.0.0a21 (released on 22.01.2020)
- fixed hooks for entities created via entity.with_(Config(...))

## 2.0.0a20 (released on 21.01.2020)
- Fixed UnicodeEncodeError: 'charmap' codec
  - thanks to [PR-197](https://github.com/yashaka/selene/pull/197) from @ak40u

## 2.0.0a19 (released on 16.01.2020)
- removed deprecation from shared.config.counter and reports_folder
- removed backports.functools-lru-cache from project dependencies
- removed six from explicit project dependencies
- removed selene.version.py (moved version number to selene.__init__.__version__)
- deprecated: by.be_following_sibling, be_parent, be_first_child
  - use xpath explicitly to not hide complexity in workaround
  - yet you can create you own xpath helpers to to show that you are using xpath but in a more readable style
    - like: x.following_sibling, ...
  - the only exception is by.text
    - it uses xpath under the hood, but so complicated that no way to use it explicitly :)
- removed warning from `collection.first`
  - it's nevertheless useless. 
  - `first` is the one of things that breaks your code when migrating to 2.*
    - after migration, just find&replace every `.first()` to `.first`, and that's it:)
    

## 2.0.0a18 (released on 14.01.2020)
- deprecated finally `send_keys`, added `press(*keys)` instead
  - use `type` for 'typing text', use `press` or `press_enter` & co for 'pressing keys' 
- removed s, ss from selene.support.shared (were added by mistake in a17)
  - yet unsure... maybe it was a good idea... to keep s, ss in shared.__init__.py too... let's think on this more...
- removed selene.api.base and selene.api.shared from distribution
  - even selene.api is not needed anymore... let's not use it... 
  - it was needed in the past for * style imports, 
    - but nevertheless it's a bad practice to do so... 
- updated readme and project long description for pypy

## 2.0.0a17 (released on 14.01.2020)
- deprecated selene.config, use `from selene.support.shared import config` instead
  - where you also can find shared browser: `from selene.support.shared import browser, config`
  - you also can go the minimalistic way with the only `browser` import:
    - `from selene.support.shared import browser`
    - `browser.config.browser_name = 'firefox'`
    - `browser.config.base_url= 'https://google.com'`
    - `browser.config.timeout = 2`
    - `browser.open('/ncr/')`
- deprecated selene.support.jquery_style_selectors
  - because it's technically is based on selene.support.shared.*, so was structured incorrectly
  - use selene.support.shared.jquery_style instead
- separate core from shared selene api in selene.*
  - now to get shared browser or config you have to import them explicitly from selene.support.shared
  - added some base docs into selene.__init__ 

## 2.0.0a16 (released on 13.01.2020)
- fixed absent screenshots for customized elements through with_
  - e.g. in `browser.element(...).with_(timeout=...).should(be.visible)`
  - as impl: moved main auto-saving screens/page_source logic to SharedConfig
  - deprecated latest_* methods in Browser in favour of last_*
- added experimental syntax for ignore_case in:
  - `browser.element(...).should(have.attribute('foo').value('bar', ignore_case=True)`
  - `browser.element(...).should(have.attribute('foo').value_containing('bar', ignore_case=True)`
  - open points:
    - while it's more or less ok here... but is it ok in:
      - `browser.all(...).should(have.texts('a', 'b', 'c', ignore_case=True')`
      - or better?
      - `browser.element(...).should(have.texts_ignoring_case('a', 'b', 'c')`
      - taking into account that one day there might be an ask for:
        - `browser.all(...).should(have.texts('a', 'b', 'c', in_any_order=True)`
        - or
        - `browser.all(...).should(have.texts_in_any_order('a', 'b', 'c')`
        - seems like better to have options over predefined names... to combine them whatever you like
          - but what then to do with conditions like value_containing? move _containing to option to?
            - `browser.element(...).should(have.value('a', contained=True, ignore_case=True')`
            - ooo, and this is also technically possible:
              - `browser.element(...).should(have.value('a').contained.ignoring_case)`

## 2.0.0a15 (released on 13.01.2020)
- fixed len(collection) to wait if collection can't be found
- made query.size to work with both element and collection
  - element.get(query.size) will return the size of the element (as a Dict)
  - collection.get(query.size) will return the size of collection (as int)
- added shared config.save_screenshot_on_failure (True by default)
- added shared config.save_page_source_on_failure (True by default)
- refactored and hardened behaviour of shared config
  - refactored waiting (moved base wait impl for entities to config.wait(entity)

## 2.0.0a14 (released on 10.01.2020)
- removed deprecation from shared.browser.save_screenshot, save_page_source, latest_screenshot, latest_page_source
  - since they nevertheless are used internally by selene
  - and methods looks like better named than original selenium ones, like `get_screenshot_as_png` :)
- refactored hooks to the style: `config.hook_wait_failure = lambda e: e`
  - the hook should be a function that receives failure as argument, 
  - process it, and return back potentially new failure object
  - by default it's just an "identity" function, returning itself
    - for shared config the default is overwritten by hook adding screenshot and page_source to the failure message
    - to disable default screenshot and page_source on failure
      - just do `config.hook_wait_failure = None`
        - yet, we may add in future explicit things like `config.screenshot_on_failure = False # True by default`
  - no other hooks avaialbe so far... somewhen in future we will add more hooks, 
    - like `config.hook_wait_command`, etc.
- fixed original `collection.all` and `collection.map` implementations (were broken in previous versions)
- marked `collection.all` with FutureWarning (yet unclear what naming would be best)
- renamed `collection.map` to `collection.all_first`, marked it as FutureWarning (yet unclear what naming would be best)
- added collection.collected(finder)
  - as a more low level, and more universal approach over collection.all and collection.all_first/map
    - given books = browser.all('.books')
    - then
    - `books.all('.author) == books.collected(lambda book: book.all('.author'))`
      - reflects all authors of all books
    - `books.all_first('.author) == books.collected(lambda book: book.element('.author'))`
      - reflects only first authors of all books
      - pay attention... all_first is not same as all(...).first:
        - `books.all('.author).first != books.all_first('.author)`
        - `books.all('.author).first == books.collected(lambda book: book.all('.author')).first`
        - `books.all('.author).first == books.first.element('.author')`
          - i.e. reflecting only the first author of the first book
- switched in wait from webdriver TimeoutException to selene.core.exceptions.TimeoutException
  - actually no need to reuse webdriver one
  - and this might help with reporting selene failure in allure reports, let's see...
- tried to implement something special for configuring remote driver management in shared config... 
  - but... just left some comments for future... 
  - it's too complicated to be implemennted in a consistent way in selene. 
  - so far the main strategy is just to create an instance on your own 
  - and then set it in config by `config.driver = webdriver.Remote(...)`, KISS ;)

## 2.0.0a13 (released on 10.01.2020)
- added temporary Collection#filter_by as deprecated 
- added temporary Collection#find_by as deprecated 
- fixed shared browser.latest_screenshot (and added browser.latest_page_source)
  - made it as property (as method it will still work as deprecated)
    - actually if you `from selene import browser` 
    - you will get deprecated browser module with latest_screenshot as method
    - the warning then will tell you to use import `from selene.support.shared import browser`
    - which will have it as a property

## 2.0.0a12 (released on 09.01.2020)
- fixed [#195](https://github.com/yashaka/selene/issues/195): added len(collection)

## 2.0.0a11 (released on 08.01.2020)
- added logging screenshot and page source hooks for failures of any waiting in shared browser behaviour
  - this is enabled by default, no option in config.* to disable such behaviour
  - yet you can turn it off by `config.hooks = Hooks(wait=WaitHooks(failure=lambda e: e)`
    - but the style/syntax of setting hooks is not completely defined, it may change in future...
- removed  SyntaxWarning for element.s and element.ss

## 2.0.0a10 (released on 08.01.2020)
- enhanced migratability
  - added syntax warning to collection.first with a hint 
    - to use .first as a property over .first() as a method
  - added selene.wait.py with wait_for alias (deprecated)
- moved all new modules from selene to selene.core
  - old deprecated modules will be removed in beta
- tuned imports to be cleaner
  - try to import everything `from selene import ...`
    - the main things you might need are: browser, config, by, be, have, Browser, Config
      - yet browser here, is old deprecated selene.browser module... 
      - so temporary import browser from selene.support.shared 
        - later once selene.browser.py is removed, you can import new browser object from selene too
    - only s and ss you will not find there, 
      - but you can import them from selene.support.jquery_style_selectors as in 1.*
- changed DeprecationWarning to SyntaxWarning for element.s and element.ss

## 2.0.0a9 (released on 07.01.2020)
- enhanced migratability of 2.*:
  - temporally added deprecated modules
    - selene.elements
    - selene.browsers
    - selene.driver
  - ensured proper config can be imported from selene (`from selene import config`)
- ensured everything potentially needed in real use is available after `from selene.api import *`
  - it includes mentioned below selene.api.base.* and selene.api.shared.* imports
- added selene.api.base for "hardcore" users
  - with `from selene.api.base import *`
  - included only Browser + Config for manual driver creation
  - and by, be, have for extra selectors and conditions
- added selene.api.shared for "easy tests with selene" with automatic driver creation
  - with `from selene.api.shared import *`
  - you can get browser.* and config.* for automatically created driver, 
    - with customization through config.*
- added also all usually needed imports to selene.*
- yet unsure what imports will be left in the end :) thinking...

## 2.0.0a8 (released on 06.01.2020)
- fixed config.* setters (timeout, base_url, etc...)

## 2.0.0a7 (released on 05.01.2020)
- removed some deprecation markings
  - from selene.common.helpers warn helpers
  - from selene.condition.not_, selene.condition.Condition#not_
  - from be.clickable

## 2.0.0a6 (released on 05.01.2020)
- fixed `entity.with_(...)`
  - where entity = browser | element | collection

## 2.0.0a5 (released on 03.01.2020)
- enhanced migratability of 2.*:
    - reflected all "old and redundant" SeleneElement methods as deprecated in Element
      - added corresponding conditions
    - reflected all "old and redundant" SeleneCollection methods as deprecated in Collection
      - did not add methods that were already deprecated in 1.*
    - temporally added selene.browser module to reflect browser.* methods from 1.* as deprecated
    - moved jquery_style_selectors.py module back to selene.support
- fixed autocomplete for *.should methods
- fixed browser.switch_to
- added `entity.with_(timeout=6)` style in addition to `entity.with_(Config(timeout=6))`
  - where entity = browser | element | collection

### known issues:
- entity.with_ does not work in case of shared browser :(
  - where entity = browser | element | collection


## 2.0.0a4 (released on 30.12.2019)
- fixed default browser_name handling in shared config; implemented some old opts in config

## 2.0.0a3 (released on 30.12.2019)
- removed from selene.support.past all not used old implementations
- tuned selene.__init__ imports to have browser (reimported from selene.support.shared)
- fixed extra modules in build for publishing
- removed six from dependencies in setup.py

## 2.0.0a2 (released on 30.12.2019)
- fixed packages to be published

## 2.0.0a1 (released on 28.12.2019, broken:))
- complete reincarnation of Selene for python version >= 3.7 :). Current limitations:
  - no test coverage; 
  - do updated docs
    - you can check the only one working test at `tests/acceptance/shared_browser/straightforward_style_test.py`
    - and use it as a fast intro 
    - keep in mind that it describes old style + new style; 
    - so you will not see there some guides for newer style; wait for that;)
  - no hooks (and so no screenshots in error messages); 
  - no temporal support for 1.0.0 aliases for some methods
    - will be added as deprecated and kept for some time to allow smoother migration

  - old implementation of everything still exists in `selene.support.past.*`
  
## 1.0.1 (released on 28.12.2019)
- no changes; just releasing latest version (before refactoring) as stable

## 1.0.0ax (next from master branch)
- removed
  - tbd
- defaults changes:
  - tbd
- naming changes:
  - tbd
- removed deprecated things: 
  - tbd
- deprecated (will produce `DeprecationWarning`):
  - tbd
- marked as "considering to deprecate" (will produce `FutureWarning`):
  - tbd
- new features:
  - tbd
  
## 1.0.0a16
- new features:
  - added `SeleneElement#matching(condition)` and `SeleneCollection#matching(condition)` 
    - as "non-waiting-predicate" version of should
    - e.g. to be used like 
        - `browser.element('#foo').matching(be.visible)` 
        - over 
        - `browser.element('#foo').is_displayed()`
          - this version will be deprecated in next versions...
- fixed `not_` usage in `SeleneCollection#element_by/filtered_by`

## 1.0.0a15
- new features:
  - added `by.id`
  - now `browser.element` can parse xpath in string selector passed as parameter

## 1.0.0a14
- removed
  - ConditionMismatchException.message (use `str(exOfConditionMismatchExceptionType)` for the same purpose)
- defaults changes:
  - changed default `browser_name` to `BrowserName.CHROME`
- added
  - `have.size_greater_than_or_equal` alias for `have.size_at_least`
  - `element.type` alias for `element.send_keys`
  - `be`, `by`, and `have` imports to `selene` module

## 1.0.0a12-13
- naming changes:
  - tbd
- removed deprecated things: 
  - `selene.tools` (use `selene.browser` instead)
  - `SeleneElement#`
    - `insist` (use `should` instead)
    - `insist_not` (use `should_not` instead)
  - `SeleneCollection#`
    - `insist` (use `should` instead)
    - `insist_not` (use `should_not` instead)
    - `filterBy` (use `filtered_by` instead)
    - `findBy` (use `element_by` instead)
    - `find` (use `element_by` instead)
- deprecated (will produce `DeprecationWarning`):
  - `SeleneCollection#`
    - `filtered` (use `filtered_by` instead)
    - `ss` (use `filtered_by` instead)
    - `s` (use `element_by` instead)
- marked as "considering to deprecate" (will produce `FutureWarning`):
  - `SeleneCollection#`
    - `filter` (consider using `filtered_by` instead)
    - `filter_by` (consider using `filtered_by` instead)
    - `find_by` (consider using `element_by` instead)
- new features:
  - [#15](https://github.com/yashaka/selene/issues/15): added `browser.title()` shortcut for `browser.driver().title`
    
## 1.0.0a11 (to be released 13.05.2017)
  - naming changes:
    - browser.visit() renamed to browser.open_url()
    - config.maximize_windows -> config.start_maximized
    - config.screenshot_folder -> config.reports_folder
  - improvements
    - screenshot link is now clickable in console output
  - bug fixes:
    - [#124](https://github.com/yashaka/selene/issues/124): If by.xpath contains utf8 symbols and not condition get UnicodeEncodeError: 'ascii'   
  - planned to remove in next version:
    - selene.tools
 
## 1.0.0a10 (released 01.03.2017)
  - [#103](https://github.com/yashaka/selene/issues/103): NEW API entry points
    - now all main selene API is available via single wildcard import: `from selene.api import *`
      - you can use the "old direct imports way" but at least until 1.0 release "the new way" will result in more stable API. We may move modules between packages, but your new way imports remain stable. See more explantains in issue description #103   
    - read Quick Start section in README.MD for more details.
  - **UPCOMING BREAKING CHANGES**:
    - deprecated selene.config.app_host, use `selene.config.base_url` instead 
      - selene.config.app_host still works but will be removed in next versions
    - [#101](https://github.com/yashaka/selene/issues/101): deprecated selene.tools, use selene.browser and selene.support.jquery_style_selectors instead or just the "new way imports from #103"
  - new features
    - [#51](https://github.com/yashaka/selene/issues/51): added ability to configure selene via passing/setting system variables
    
## 1.0.0a9 (to be released 01.03.2017)
  - skipped:)

## 1.0.0a8 (released 16.02.2017)
  - new features added
    - #76: config.maximize_window (set to True by default)
    - #68: config.hold_browser_open (set to False by default)
    - #78: config.desired_capabilities (set to None by default)
    - #92: selene.tools.latest_screenshot() (returns NoneObject if no screenshot have been added yet)
    - #85: SeleneElement#context_click()
    - #77: SeleneElement#scroll_to() (not needed in all cases, but may be usefull in some browsers sometimes...)
    - #75: support for phantomjs browser
    - conditions: url, url_containing, title_containing
    - refactored aliases implementation from selene.support.conditions.have
      - now they are implemented as method definitions giving better hints during autocomplete
  - project infrastracture
    - #84: improved travis job: added archiving build artifacts (test results)
  
## 1.0.0a7 (released 22.01.2017)
  - fixed #71: weird paths of screenshots for windows
  - updated #56: now selene should work with python 3 (but feature is not fully tested)
    
## 1.0.0a6 (released 17.01.2017)
  - added selene.tools.wait_to to wait for driver conditions like have.title, have.js_returned_true
  - added Title and JsReturnedTrue webdriver conditions
  - added selene.tools.execute_script
    
## 1.0.0a5 (released 16.01.2017)
  - refactored conditions implementation
  - broken support for python 3 (will be fixed in next versions)

## 1.0.0a4 (next from master branch)
  - added automatic screenshots on failed "should" methods
    - by default screenshots are created in {user_home}/.selene/screenshots/{id_of_current_tests_run}
    - by default the "previous run" screenshots are not cleared on "next run"
  - screenshot can be created manually by `selene.tools.take_screenshot`

## 1.0.0a3 (next from master branch)
  - improvements:
    - error messages are cleaner
      - TODO: still lacks proper test coverage of all cases...
  - internal
    - refactored wait_for implementation, made it cleaner
      - TODO: still need to refactor condition implementation
    
## 1.0.0a2 (not published, available via direct install from sources)
- new features:
  - automatic driver management (thanks to PR from @SergeyPirogov)
    - no more need to `set_driver`, 
      just use any command from `selene.tools`, 
      like `visit`, `s`, or `ss` and driver will be opened automatically,
      and then closed automatically (unless you decide to set it manually via `set_driver`)
    - includes automatic installation of needed drivers via [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)
    
## 1.0.0a1 (not published, available via direct install from sources)
- internal
  - improved test coverage
    - added "given-helpers" for preconditions for atomic tests
  - completely refactored implementation to be more structural and solid
    - on the way found non-stable behavior of old implementation and fixed it
- new features:
  - object oriented paradigm is now supported in context of webdriver usage
    - Don't like "static" s, ss helpers (from selene.tools module) using global driver instance set by set_driver(...)?
    - now you can use driver.element, driver.all correspondingly
        - where driver = SeleneDriver.wrap(FirefoxDriver()), etc.
        - SeleneDriver has almost the same interface as WebDriver, but with additional methods
          - so you can do everything you can do with raw selenium when needed
  - additional "helpers" from selene.support package
    - more readable and convenient API to retrieve conditions via selene.support.(be|have)
      - e.g. `s('#element').should(have.text('foo'))`
    - more readable and convenient API to retrieve by locators via selene.support.by
      - e.g. 
        - `s(by.text('foo')).click()`
        - `s('#element').element(by.be_following_sibling).click()`
    - SeleneElement relative search shortcut-methods:
      - `s('#element').parent_element.click()`
      - `s('#element').following_sibling.click()`
      - `s('#element').first_child.click()`
- breaking changes:
  - removed out of the box but overcomplicated Widgets support via extending SElement
    - you still can create reusable Widgets in much simpler way
      - see more explanation in [#17](https://github.com/yashaka/selene/issues/17)
  - removed access by config.driver to the driver instance that was set by set_driver(...) from selene.tools
    - it's mandatory to use get_driver(...) from selene.tools for this

## 0.0.8 (released 08.12.2016)
- locked the selenium version to 2.53.1
- fixed encoding issues when working with text of elements in conditions
- added bys.by_name

## 0.0.7 (released 01.03.2016)
- fixed python3 support
- fixed the is_displayed method - now it contains implicit wait for "exist in DOM" instead of "visible"
- added ss(".element", of=Task) syntax in addition to ss(".element").of(Task)
- removed "general interceptor of all unknown methods" SElement's base class (actually commented it in code:)
- refactored lazy inner collection classes to use extend in __init__ and not use SElementsCollectionWrapper (removed the latter and SElementWrapper)
- refactored: removed unnecessary extend from "inner" selement collections (it is needed obviously only for "inner" selement collection element classes)

## 0.0.6 (released 22.02.2016)
- added alias methods:
```
    insist_not = assure_not
    should_not = assure_not
    should_not_be = assure_not
    should_not_have = assure_not
```
- removed stopit from dependencies
- optimized element actions (now they wait for visibility only if first try failed)
  - now selene is as fast as selenium with research of elements before any action. Manual cashing is also available when "raw selenium" speed is needed (semi-automatic customizable cashing will be added later)
- optimized SElementsCollection#find implementation - now it returns first match, not filter everything and then get first among all matches
- mapped all webelement methods to selement (almost all) - now autocompletion works fully for selement
- optimized logic of "inner lazy elements" of collection, removed a bit of magic from it.

## 0.0.5 (released 20.02.2016)

- big refactoring
  - removed currently unstable things
    - automatic driver management (Firefox)
        - so now management is manual but you can use any driver you want (Firefox, Chrome, etc...)
    - screenshooting
  - removed "too complicated" things
    - automatic Loading of widgets
      - so now no any difference between insist, assure, should
  - added aliases (maybe too much... some may be marked as deprecated in future)
    - insist, assure, should, should_be, should_have
    - find more in elements.py, etc.
  - added more overloaded element methods... removed some magic in implementation, still needed to simplify more...
  - added tests, still not enough though
  - added support of other locators (in addition to css)

## 0.0.4
...
## 0.0.3
...
## 0.0.2
...
## 0.0.1
...
