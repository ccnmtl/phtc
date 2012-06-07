# -*- coding: utf-8 -*-
from lettuce.django import django_url
from lettuce import before, after, world, step
from django.test import client
from django.core.management import call_command
from django.test.utils import setup_test_environment, teardown_test_environment
import sys
import os
from pagetree.models import Hierarchy, Section

import time
try:
    from lxml import html
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.keys import Keys
    import selenium
except:
    pass


def robust_string_compare(a,b):
    """ compare two strings but be a little flexible about it.

    try to handle case and whitespace variations without blowing up.
    this makes tests more robust in the face of template changes"""
    return a.strip().lower() == b.strip().lower()


@before.harvest
def setup_browser(variables):
#    ff_profile = FirefoxProfile()
#    ff_profile.set_preference("webdriver_enable_native_events", False)
#    world.firefox = webdriver.Firefox(ff_profile)
    world.browser = webdriver.Chrome()
    world.client = client.Client()
    world.using_selenium = False

# test_data/test.db was created by the following process
#
# 1) with a normal setup, add some pages, blocks, etc
# 2) create a phtc/settings_test.py that uses sqlite3 and test_data/test.db
# 3) ./manage.py dumpdata --indent=2 --format=json \
#      --natural > phtc/main/fixtures/test_data.json
# 4) ./manage.py syncdb --settings=phtc.settings_test
# 5) ./manage.py migrate --settings=phtc.settings_test
# 6) ./manage.py reset contenttypes --settings=phtc.settings_test
# 7) ./manage.py reset auth --settings=phtc.settings_test
# 8) ./manage.py loaddata phtc/main/fixtures/test_data.json \
#      --settings=phtc.settings_test

@before.harvest
def setup_database(_foo):
    # make sure we have a fresh test database
    os.system("rm -f lettuce.db")
    os.system("cp test_data/test.db lettuce.db")

@after.harvest
def teardown_database(_foo):
    os.system("rm -f lettuce.db")

@after.harvest
def teardown_browser(total):
    world.browser.quit()
    teardown_test_environment()

@step(u'Using selenium')
def using_selenium(step):
    world.using_selenium = True

@step(u'Finished using selenium')
def finished_selenium(step):
    world.using_selenium = False

@before.each_scenario
def clear_selenium(step):
    world.using_selenium = False

@step(r'I access the url "(.*)"')
def access_url(step, url):
    if world.using_selenium:
        world.browser.get(django_url(url))
    else:
        response = world.client.get(django_url(url), follow=True)
        world.dom = html.fromstring(response.content)

@step(u'I am not logged in')
def i_am_not_logged_in(step):
    if world.using_selenium:
        world.browser.get(django_url("/accounts/logout/"), follow=True)
    else:
        world.client.logout()

@step(u'I am taken to a login screen')
def i_am_taken_to_a_login_screen(step):
    assert len(world.response.redirect_chain) > 0
    (url,status) = world.response.redirect_chain[0]
    assert status == 302, status
    assert "/login/" in url, "URL redirected to was %s" % url


@step(u'there is not an? "([^"]*)" link')
def there_is_not_a_link(step, text):
    found = False
    for a in world.dom.cssselect("a"):
        if a.text and robust_string_compare(a.text,text):
            found = True
    assert not found

@step(u'there is an? "([^"]*)" link')
def there_is_a_link(step, text):
    found = False
    for a in world.dom.cssselect("a"):
        if a.text and robust_string_compare(a.text,text):
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
        assert False, "this step needs to be implemented for the django test client"

    world.browser.find_element_by_id(field_name).send_keys(value)

@step(u'I submit the "([^"]*)" form')
def i_submit_the_form(step, id):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"

    world.browser.find_element_by_id(id).submit()

@step('I go back')
def i_go_back(self):
    """ need to back out of games currently"""
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    world.browser.back()

@step(u'I wait for (\d+) seconds')
def wait(step,seconds):
    time.sleep(int(seconds))


@step(r'I see the header "(.*)"')
def see_header(step, text):
    if world.using_selenium:
        found = False
        for h1 in world.browser.find_elements_by_css_selector("h1"):
            if robust_string_compare(text,h1.text):
                found = True
                break
        assert found, "header %s found" % text
    else:
        found = False
        for h1 in world.dom.cssselect('h1'): 
            if robust_string_compare(text,h1.text_content()):
                found = True
                break
        assert found, "header %s found" % text

@step(r'I see the h3 "(.*)"')
def see_h3(step, text):
    if world.using_selenium:
        found = False
        for h3 in world.browser.find_elements_by_css_selector("h3"):
            if robust_string_compare(text,h3.text):
                found = True
                break
        assert found, "h3 %s found" % text
    else:
        found = False
        for h3 in world.dom.cssselect('h3'): 
            if robust_string_compare(text,h3.text_content()):
                found = True
                break
        assert found, "h3 %s found" % text


@step(r'I see the page title "(.*)"')
def see_title(step, text):
    if world.using_selenium:
        assert text == world.browser.title
    else:
        assert text == world.dom.find(".//title").text
