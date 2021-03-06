# -*- coding: utf-8 -*-
from lettuce.django import django_url
from lettuce import before, after, world, step
from django.test import client
from django.test.utils import teardown_test_environment
from django.conf import settings
import os

import time
try:
    from lxml import html
    from selenium import webdriver
#    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#    from selenium.common.exceptions import NoSuchElementException
#    from selenium.webdriver.common.keys import Keys
#    import selenium
except:
    pass


def robust_string_compare(a, b):
    """ compare two strings but be a little flexible about it.

    try to handle case and whitespace variations without blowing up.
    this makes tests more robust in the face of template changes"""
    return a.strip().lower() == b.strip().lower()


def skip_selenium():
    return (os.environ.get('LETTUCE_SKIP_SELENIUM', False)
            or (hasattr(settings, 'LETTUCE_SKIP_SELENIUM')
            and settings.LETTUCE_SKIP_SELENIUM))


@before.harvest
def setup_browser(variables):
    world.using_selenium = False
    if skip_selenium():
        world.browser = None
        world.skipping = False
    else:
        browser = getattr(settings, 'BROWSER', 'Chrome')
        if browser == 'Chrome':
            world.browser = webdriver.Chrome()
        elif browser == 'Headless':
            world.browser = webdriver.PhantomJS()
        else:
            print "unknown browser: %s" % browser
            exit(1)
    world.client = client.Client()


# test_data/test.db was created by the following process
#
# 1) with a normal setup, add some pages, blocks, etc
# 2) create a phtc/settings_test.py that uses sqlite3 and test_data/test.db
# 3) ./manage.py dumpdata --indent=2 --format=json \
#      --natural > phtc/main/fixtures/test_data.json
# 4) ./manage.py syncdb --settings=phtc.settings_lettuce
# 5) ./manage.py migrate --settings=phtc.settings_lettuce
# 6) ./manage.py reset contenttypes --settings=phtc.settings_lettuce
# 7) ./manage.py reset auth --settings=phtc.settings_lettuce
# 8) ./manage.py loaddata phtc/main/fixtures/test_data.json \
#      --settings=phtc.settings_lettuce
# be sure to replace test_data/test.db with the newly generated lettuce.db file
# and rename it test.db

@before.harvest
def setup_database(_foo):
    # make sure we have a fresh test database
    os.system("rm -f lettuce.db")
    os.system("cp test_data/test.db lettuce.db")


@after.harvest
def teardown_database(_foo):
    os.system("rm -f lettuce.db")
    #a=1

@after.harvest
def teardown_browser(total):
    if not skip_selenium():
        world.browser.quit()
    teardown_test_environment()


@step(u'Using selenium')
def using_selenium(step):
    if skip_selenium():
        world.skipping = True
    else:
        world.using_selenium = True


@step(u'Finished using selenium')
def finished_selenium(step):
    if skip_selenium():
        world.skipping = False
    else:
        world.using_selenium = False


@before.each_scenario
def clear_selenium(step):
    world.skipping = False
    world.using_selenium = False


@step(r'I access the url "(.*)"')
def access_url(step, url):
    if world.skipping:
        return
    if world.using_selenium:
        world.browser.get(django_url(url))
    else:
        response = world.client.get(django_url(url), follow=True)
        world.dom = html.fromstring(response.content)


@step(u'I am not logged in')
def i_am_not_logged_in(step):
    if world.skipping:
        return
    if world.using_selenium:
        world.browser.get(django_url("/accounts/logout/"))
    else:
        world.client.logout()


@step(u'I am taken to a login screen')
def i_am_taken_to_a_login_screen(step):
    if world.skipping:
        return
    assert len(world.response.redirect_chain) > 0
    (url, status) = world.response.redirect_chain[0]
    assert status == 302, status
    assert "/login/" in url, "URL redirected to was %s" % url


@step(u'there is not an? "([^"]*)" link')
def there_is_not_a_link(step, text):
    if world.skipping:
        return
    found = False
    for a in world.dom.cssselect("a"):
        if a.text and robust_string_compare(a.text, text):
            found = True
    assert not found


@step(u'there is an? "([^"]*)" link')
def there_is_a_link(step, text):
    found = False
    for a in world.dom.cssselect("a"):
        if a.text and robust_string_compare(a.text, text):
            found = True
    assert found


@step(u'I click the "([^"]*)" link')
def i_click_the_link(step, text):
    if not world.using_selenium:
        for a in world.dom.cssselect("a"):
            if a.text:
                if text.strip().lower() in a.text.strip().lower():
                    href = a.attrib['href']
                    response = world.client.get(django_url(href))
                    world.dom = html.fromstring(response.content)
                    return
        assert False, "could not find the '%s' link" % text
    else:
        try:
            link = world.browser.find_element_by_partial_link_text(text)
            assert link.is_displayed()
            link.click()
        except:
            try:
                time.sleep(1)
                link = world.browser.find_element_by_partial_link_text(text)
                assert link.is_displayed()
                link.click()
            except:
                world.browser.get_screenshot_as_file("/tmp/selenium.png")
                assert False, link.location


@step(u'I fill in "([^"]*)" in the "([^"]*)" form field')
def i_fill_in_the_form_field(step, value, field_name):
    # note: relies on input having id set, not just name
    if not world.using_selenium:
        assert False, ("this step needs to be implemented for the "
                       + "django test client")

    world.browser.find_element_by_id(field_name).send_keys(value)


@step(u'I submit the "([^"]*)" form')
def i_submit_the_form(step, id):
    if not world.using_selenium:
        assert False, ("this step needs to be implemented for the "
                       + "django test client")

    world.browser.find_element_by_id(id).submit()


@step('I go back')
def i_go_back(self):
    """ need to back out of games currently"""
    if not world.using_selenium:
        assert False, ("this step needs to be implemented for the "
                       + "django test client")
    world.browser.back()


@step(u'I wait for (\d+) seconds')
def wait(step, seconds):
    time.sleep(int(seconds))


@step(r'I see the header "(.*)"')
def see_header(step, text):
    if world.skipping:
        return
    assert has_element(
        "h1",
        lambda element: compare_element_string(element, text)
        ), "h1 %s found" % text


def compare_element_string(element, text):
    if hasattr(element, 'text_content'):
        return robust_string_compare(element.text_content(), text)
    else:
        return robust_string_compare(element.text, text)


def has_element(css_selector, test_func, root=None):
    if root is None:
        if world.using_selenium:
            root = world.browser
        else:
            root = world.dom

    collection = []
    if world.using_selenium:
        collection = root.find_elements_by_css_selector(css_selector)
    else:
        collection = root.cssselect(css_selector)

    for element in collection:
        if test_func(element):
            return True

    return False


@step(r'I see the h3 "(.*)"')
def see_h3(step, text):
    assert has_element(
        "h3",
        lambda element: compare_element_string(element, text)
        ), "h3 %s found" % text


@step(r'I see the page title "(.*)"')
def see_title(step, text):
    if world.using_selenium:
        assert text == world.browser.title
    else:
        assert text == world.dom.find(".//title").text


@step(r'there is an? "([^"]+)" field')
def there_is_a_form_field(step, field_id):
    if not world.using_selenium:
        assert len(world.dom.cssselect("input#%s" % field_id)) > 0


@step(r'there is an? "([^"]+)" select')
def there_is_a_select(step, select_id):
    if not world.using_selenium:
        assert len(world.dom.cssselect("select#%s" % select_id)) > 0


@step(u'there is a "([^"]*)" submit button')
def there_is_a_submit_button(step, label):
    assert has_element(
        "input[type=submit]",
        lambda element: robust_string_compare(element.attrib['value'], label)
        ), "found submit button with the right label"


@step(u'I am logged as a student')
def i_am_logged_as_a_student(step):
    if world.skipping:
        world.client.login(username='demo', password='demo')

    if not world.using_selenium:
        world.client.login(username='test123', password='test123')

    else:
        world.browser.get(django_url("/accounts/login/"))
        username_field = world.browser.find_element_by_id("id_username")
        password_field = world.browser.find_element_by_id("id_password")
        form = world.browser.find_element_by_id("login-form")
        username_field.send_keys("test123")
        password_field.send_keys("test123")
        form.submit()


@step(u'I am logged in as an admin')
def i_am_logged_in_as_an_admin(step):
    if world.skipping:
        return
    world.client.login(username='jed2161', password='jedavis13')


@step(u'I do not see an edit link')
def i_do_not_see_an_edit_link(step):
    assert len(world.dom.cssselect("a#test-edit-link")) == 0


@step(u'I see an edit link')
def then_i_see_an_edit_link(step):
    assert len(world.dom.cssselect("a#test-edit-link")) > 0


''' HANDOFF TESTS '''

@step(u'When I access the handoff url "([^"]*)"')
def when_i_access_the_handoff_url(step, url):
    if world.skipping:
        return
    world.browser.get(django_url(url))
    h1 = world.browser.find_element_by_id('section-header')
    if h1.text == 'Part 1: Introduction to Qualitative Research':
        assert True
    else:
        assert False


@step(u'Then I see the handoff module "([^"]*)"')
def then_i_see_the_handoff_module(step, courseID):
    if world.skipping:
        return
    else:
        header = world.browser.find_element_by_id('section-header')
        assert header.text == 'Part 1: Introduction to Qualitative Research'


@step(u'And I click on the link "([^"]*)"')
def and_i_click_on_the_link_group1(step, link_id):
    if world.skipping:
        return
    link = world.browser.find_element_by_id(link_id)
    link.click()


@step(u'And it fails when I try to use my NYLearns login info')
def and_it_fails_when_i_try_to_use_my_nylearns_login_info(step):
    login_user('nylearns_username', 'nylearns_pass')


@step(u'And I fill out the form')
def and_i_fill_out_the_form(step):
    if world.skipping:
        return
    username = world.browser.find_element_by_id('id_username').send_keys('test123') 
    email = world.browser.find_element_by_id('id_email').send_keys('testing@gmail.com')
    pass1 = world.browser.find_element_by_id('id_password1').send_keys('test123')
    pass2 = world.browser.find_element_by_id('id_password2').send_keys('test123')
    fname = world.browser.find_element_by_id('id_fname').send_keys('test123')
    lname = world.browser.find_element_by_id('id_lname').send_keys('test123')
    age = world.browser.find_element_by_id('id_age').send_keys('20-29')
    sex = world.browser.find_element_by_id('id_sex').send_keys('male')
    origin = world.browser.find_element_by_id('id_origin').send_keys('no')
    ethnicity = world.browser.find_element_by_id('id_ethnicity').send_keys('Other')
    degree = world.browser.find_element_by_id('id_degree').send_keys('Masters Degree')
    work_city = world.browser.find_element_by_id('id_work_city').send_keys('test City')
    work_state = world.browser.find_element_by_id('id_work_state').send_keys('NY')
    zipcode = world.browser.find_element_by_id('id_work_zip').send_keys('12345')
    position = world.browser.find_element_by_id('id_position').send_keys('Biostatistics')
    location = world.browser.find_element_by_id('id_employment_location').send_keys('Academia')
    dept_health = world.browser.find_element_by_id('id_dept_health').send_keys('No')
    geo_dept_health = world.browser.find_element_by_id('id_geo_dept_health').send_keys('New York City (NY)')
    experience = world.browser.find_element_by_id('id_experience').send_keys('0-5')
    umc = world.browser.find_element_by_id('id_umc').send_keys('Yes')
    rural = world.browser.find_element_by_id('id_rural').send_keys('No')
    register = world.browser.find_element_by_css_selector('input.btn-primary').click()


@step (u'the previous section is available')
def previous_section(step):
    if world.skipping:
        return
    link = world.browser.find_element_by_link_text('Part 1: Introduction to Qualitative Research')
    assert link


''' Feature: Hide Section  '''

@step (u'I am logged out')
def i_am_logged_out(step):
    if world.skipping:
        return
    btn = world.browser.find_element_by_id('login-logout')
    if btn.text == "Log out":
        btn.click()


@step (u'Then I re-login as an admin')
def relogin_as_admin(step):
    if world.skipping:
        return
    world.browser.get(django_url("/accounts/login/"))
    username_field = world.browser.find_element_by_id("id_username")
    password_field = world.browser.find_element_by_id("id_password")
    form = world.browser.find_element_by_id("login-form")
    username_field.send_keys("jed2161")
    password_field.send_keys("jedavis13")
    form.submit()


@step (u'And go to module one edit screen')
def mod_one_edit(step):
    if world.skipping:
        return
    world.browser.get(django_url('/edit/module-1/'))

@step (u'Then I click the edit button')
def click_edit(step):
    if world.skipping:
        return
    link = world.browser.find_element_by_link_text('Edit Section')
    link.click()


@step (u'And submit hide in the section css')
def click_edit(step):
    if world.skipping:
        return
    css_field = world.browser.find_element_by_id('id_section_css_field')
    css_field.send_keys('hide')
    form = world.browser.find_element_by_id('section_css')
    form.submit()


@step (u'Then module 1 has css class of hide')
def verify_mod_1_class(step):
    if world.skipping:
        return
    world.browser.get(django_url('/dashboard/'))
    links = world.browser.find_elements_by_class_name('module')
    mod1_link = links[0]
    if not mod1_link.is_displayed():
        assert True
    else:
        assert False
    

''' Feature: Video Module '''

@step (u'And go to module two edit screen')
def mod_one_edit(step):
    if world.skipping:
        return
    world.browser.get(django_url('/edit/module-2/'))


@step (u'And submit video in the module type')
def click_edit(step):
    if world.skipping:
        return
    type_field = world.browser.find_element_by_id('id_module_type_form')
    type_field.send_keys('video')
    form = world.browser.find_element_by_id('module-type')
    form.submit()


@step(u'Then module 2 is now under video section')
def then_module_2_is_now_under_video_section(step):
    if world.skipping:
        return
    world.browser.get(django_url('/dashboard/'))
    modules = world.browser.execute_script('return jQuery(".video").next().next()')
    for mod in modules:
        if mod.get_attribute('rel') =='/module-2/':
            return True
    
    if not mod1_link.is_displayed():
        assert True
    else:
        assert False

''' Question Label Feature '''
@step (u'And I insert an image in the label field of a question')
def insert_image_in_question(step):
    if world.skipping:
        return
    link = world.browser.find_element_by_link_text("Quiz")
    link.click()
    link_manage=world.browser.find_element_by_link_text("manage questions/answers")
    link_manage.click()
    world.browser.get(django_url('_quiz/edit_answer/310/'))
    label = world.browser.find_element_by_id('id_label')
    label.send_keys('<img id="selenium-img" src="'+django_url("/site_media/img/banner.jpg") + '"/>' )
    form = world.browser.find_element_by_css_selector('form')
    form.submit()
    world.browser.get(django_url('/module-1/three/evaluation/'))    
    assert(world.browser.find_element_by_id('selenium-img'))

