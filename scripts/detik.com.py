#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys


def create_driver_session(session_id):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX)
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver

print 'trying to open '+sys.argv[1]
if sys.argv[2] == "0":
   f = open("session.save","w")
   driver=webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX)
   f.write(driver.session_id)
   driver.get(sys.argv[1])
else:
   f = open("session.save","r")
   session = f.readline()
   driver=create_driver_session(session)
   driver.get(sys.argv[1])
   print driver.session_id
