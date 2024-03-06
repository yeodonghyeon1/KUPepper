import qi
import argparse
import sys
import time
from robot import Pepper

robot = Pepper("192.168.0.125", 9559)
# robot.speech_service.unsubscribe("Test_tts")
# robot.autonomous_life_service.setState("solitary")

# robot.dialog_service.clearConcepts() #clear concepts
# robot.dialog_service.deactivateTopic()
# robot.dialog_service.unloadTopic()

robot.restart_robot()


