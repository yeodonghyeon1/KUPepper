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
from flask import Flask, render_template, redirect, url_for, request

#main.htmpsdf
#main.htmp -> testaa
#main.htmpSASDASD
web_host = "192.168.0.107"
# web_page = "http://192.168.0.107/"
web_page = "https://google.com/"

app = Flask(__name__)
#웹 메인 페이지
@app.route('/', methods=['GET', 'POST'])
def main():
    #지도 정보를 가지고 있어야
    #get 같은걸로 ㅇ맵을 가져와야하는거 같은데
    if request.method == 'POST':
        print("aa")
        return redirect(url_for('test'))
    return render_template('main.html')

@app.route('/test')
def show_map_page(robot_map):
    pass
    # cv2.imshow("RobotMap", robot_map)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

#baseline
if __name__ == "__main__":
    #여기에 로봇 클래스 만들고
    robot = Pepper("192.168.0.125", "9559")
    robot.say("HI Pepper")

    #baseline 메서드를 불러와서 쓰레드로 동작
    # robot_map = robot.get_map()

    #서버로? 페이지로??
    # main()

    robot.show_web(web_page) #192.168.0.127 이라는 페이지 여는게 다임
    app.run(host=web_host, port=80, debug=True)
    # th1=threading.Thread(target=sv.app.run(host=web_host, port=80, debug=True))

    # th1.start()
    # print("111111")
    # print("222222222")


    

    

    
