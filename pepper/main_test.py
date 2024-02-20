#!/usr/bin/env python
# -*- coding: utf-8 -*-


#testing code
    # robot.set_english_language()
    # print(robot.speech_service.getLanguage()) #English
    # print(robot.speech_service.loadVocabulary("")) None
    # print(robot.speech_service.setVocabulary(["pepper", "페퍼"]),True)
    # robot.listen_to(["pepper","hello"])
    # loaded_topic = robot.dialog_service.loadTopic("/home/nao/pepper_test_enu.top") #load topic
    # robot.dialog_service.runDialog() #application manifest에 있는 모든 토픽(collaborative로 마크된)을 검색하고 load하고 complie함
    # robot.dialog_service.loadTopicContent("pepper_test_enu.top") #load topic이랑 똑같이 작동함
    # robot.dialog_service.startPush() #dialog engine이 자동으로 proposal을 만들기 시작(Focuse기반)
    # print(len(words)) #2
    # print(type(words)) #list
    # print(words[0])


import qi
import Tkinter
from robot import Pepper
import threading
import sys
import time
import numpy
import cv2

web_page = "https://google.com/"
def set_vocabulary(robot):
    #setVocabulary
    robot.speech_service.pause(True) 
    robot.speech_service.removeAllContext() #context를 지워야하는지 몰루
    robot.speech_service.deleteAllContexts()
    robot.speech_service.setVocabulary(["hi",'pepper'],False) #true 하면 "<...> hi <...>" 이렇게 나옴
    robot.speech_service.pause(False)
    
def wait_until_finished(robot):
    while True:
        if robot.memory_service.getData("ALSpeechRecognition/Status") == "EndOfProcess":
            time.sleep(0.1)
            break

def say_hi(robot):
    robot.autonomous_life_service.setState("interactive")
    robot.speech_service.subscribe("Test_tts")
    while True:
        words = robot.memory_service.getData("WordRecognized")
        print(words)
        print(robot.memory_service.getData("ALSpeechRecognition/Status"))

        # if robot.memory_service.getData("ALSpeechRecognition/Status") == "SpeechDetected":
        if words[1]>=0.40:
            if words[0] == "hi":
                robot.memory_service.removeData("WordRecognized")
                robot.say("hi~")
                time.sleep(0.3)

            if words[0] == "pepper":
                robot.say("yes?~")
                time.sleep(0.3)
                robot.say("Do you need help?")
                time.sleep(0.6)
                robot.say("I can guide some places for you")
                time.sleep(1.3)

def test_dialog(robot):

    #미구현1 시작전에 사람을 찾고 
    #미구현2 사람을 찾으면 사람이 있는 방향으로 이동및 눈도 맞추고
    #미구현3 사람이 없으면 랜덤하게 돌아다니기-이거 여기넣는게 맞나..?

    topicContent = ("topic: ~mytopic()\n"
                    "language: enu\n"
                    "proposal: hello 1\n"
                    "proposal: hello 2\n"
                    "u:(hi) hello human\n"
                    "u:(how's the weather today) It's sunny\n")
    
    topicContent1 = ("topic: ~mytopic1()\n"
                     "language: enu\n"
                     "dynamic: user_help\n"
                     "proposal: This is KUPepper\n"
                     "proposal: How to help you??\n"
                     "u:(can you _~user_help) oh!, you need $1!.. wait for seconds. \n")

    # robot.autonomous_life_service.setState("disabled")
    #추가로 에플리케이션 작동 상태로 변경해주고 동작하면 깔끔하게 비프음 들리는 state로 빠짐z
    robot.autonomous_life_service.setState("interactive")
    robot.autonomous_life_service.switchFocus("pepper_test-c675d3/behavior_1") #package-uuid/behavior-path
    loaded_topic=robot.dialog_service.loadTopicContent(topicContent1) #load topic content
    robot.dialog_service.activateTopic(loaded_topic) #activate topic
    robot.dialog_service.subscribe("my_dialog") #start dialog engine
    robot.dialog_service.setConcept("user_help", "English",["help", "guide", "direction", "information"]) #set concept
    # robot.dialog_service.setFocus("mytopic") #set focus to the topic
    robot.dialog_service.forceOutput() #force output
    robot.dialog_service.forceOutput() #force output

    
    try:
        raw_input("Press the enter key to exit")    
    finally:
        robot.dialog_service.unsubscribe("my_dialog")
        robot.dialog_service.deactivateTopic(loaded_topic)
        robot.dialog_service.unloadTopic(loaded_topic)
        robot.autonomous_life_service.stopAll()
        robot.autonomous_life_service.setState("solitary")



def check_life_state(robot):
    while True:
        print(robot.autonomous_life_service.getState())
        time.sleep(0.7)

def test_dialog1(robot):
    topicContent1 = ("topic: ~mytopic()\n"
                    "language: enu\n"
                    "proposal: hello\n"
                    "u:(hi) hello human\n"
                    "u:(how's the weather today) It's sunny\n")
    
    topicContent2 = ("topic: ~mytopic()\n"
                    "language: enu\n"
                    "proposal: hello\n"
                    "u:(hi) hello human\n"
                    "u:(how's the weather today) It's sunny\n")
    loaded_topic=robot.dialog_service.loadTopicContent(topicContent1) #load topic content
    robot.dialog_service.activateTopic(loaded_topic) #activate topic
    robot.dialog_service.subscribe("my_dialog") #start dialog engine
    try:
        raw_input("Press the enter key to exit")    
    finally:
        robot.dialog_service.unsubscribe("my_dialog")
        robot.dialog_service.deactivateTopic(loaded_topic)
        robot.dialog_service.unloadTopic(loaded_topic)
        robot.autonomous_life_service.stopAll() #이거는 스택도 다 날림
        # robot.autonomous_life_service.stopFocus()
        robot.autonomous_life_service.setState("solitary")


#baseline
if __name__ == "__main__":
    robot = Pepper("192.168.0.125", "9559")
    test_dialog(robot)





    

    
