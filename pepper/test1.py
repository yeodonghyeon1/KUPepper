import qi
import argparse
import sys
import time
from robot import Pepper

robot = Pepper("192.168.0.125", 9559)
# Display the index.html page of a behavior name j-tablet-browser
# The index.html must be in a folder html in the behavior folder
robot.tablet_service.loadApplication("The dialog ")
robot.tablet_service.showWebview()

time.sleep(30)

# Hide the web view
robot.tablet_service.hideWebview()