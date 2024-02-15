#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qi
import Tkinter
from robot import Pepper
import threading
import sys
import time
import numpy
import cv2

web_page = "https://google.com/"

#baseline
if __name__ == "__main__":
    #페퍼 연결
    robot = Pepper("192.168.0.125", "9559")
    robot.say("Pepper On the Line!")

    #웹 페이지 띄우기
    robot.show_web(web_page) #192.168.0.127 이라는 페이지 여는게 다임

    # robot_map = robot.get_map()

    #서버로? 페이지로??
    # main()

    # th1=threading.Thread(target=sv.app.run(host=web_host, port=80, debug=True))

    # th1.start()
    # print("111111")
    # print("222222222")


    

    

    
