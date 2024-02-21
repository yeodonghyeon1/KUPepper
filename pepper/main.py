#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qi
import Tkinter
from robot import Pepper
import threading
import sys
import time
import cv2
from flask import Flask, render_template, redirect, url_for, request

############################################################################################

#flask 웹서버


app = Flask(__name__)
web_host = "192.168.0.107"
web_page = "http://192.168.0.107/"


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('main.html')

@app.route('/test1', methods=['GET', 'POST'])
def test1():
    if request.method == 'POST':
        return "test page 1"
    else:
        return redirect(url_for('main'))

@app.route('/test2', methods=['GET', 'POST'])
def test2():
    if request.method == 'POST':
        return "test page 2"
    else:
        return redirect(url_for('main'))




#플라스크 변수: 전역변수랑 같음(웹 이벤트 작동 시 사용)
app.test2 = False

############################################################################################



class KUpepper:
    def __init__(self, ip, port):
        #페퍼 라이브러리
        self.ip = ip
        self.port = port
        self.robot = Pepper(self.ip, self.port)
        self.robot.say("HI Pepper")

        #베이스 라인 코드
        self.event = threading.Event()
        self.base_thread = threading.Thread(target=self.baseline)
        self.base_thread.daemon = True
        self.base_thread.start()

        #GUI
        self.window = Tkinter.Tk()
        self.base_interface_robot()

        self.result_map= 0 
        self.resolution=0 
        self.offset_x =0 
        self.offset_y =0

    #이벤트 작동 간 쓰레드 중지
    def stopThreadUntilOneTheEnd(self):
        if self.event.is_set():
            while True:
                if self.event.is_set():
                    time.sleep(0.1)
                else:
                    break

    #현재 상태 출력 모음
    def status_print(self):
        print("focus activity:", self.robot.autonomous_life_service.focusedActivity())
        print("context:", self.robot.memory_service.getData('Diagnosis/Temperature/Tablet/Error'))
        # print("key list:", self.robot.memory_service.getDataListName( ))
        # print("context:", self.robot.autonomous_life_service.getFocusHistory())    
        # print("context:", self.robot.autonomous_life_service.getFocusContext())
        # print("laser x:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Vertical/Right/Seg01/X/Sensor/Value"))
        # print("laser y:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Vertical/Right/Seg01/Y/Sensor/Value"))
        print("laser front value:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Reg/Status/Sensor/Value"))
        print("usersession:", self.robot.user_session.getOpenUserSessions())
        print("front sonar value:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))

    #기본 파라미터 구성
    def base_parameter(self):
        self.robot.set_security_distance(distance=0.2)
        self.load_map_and_localization()

        # print(self.robot.navigation_service.getMetricalMap())

    #페퍼 상호작용
    def interaction(self):
        #머리 터치 시 상호작용
        if self.robot.memory_service.getData("Device/SubDeviceList/Head/Touch/Front/Sensor/Value"):
            self.robot.say("Get your hands off my head loser")
    
    #웹 상호작용
    def web_interaction(self):
        #이동 상호작용
        if app.test2 == True:
            self.navigation_mode_button_push2()
            app.test2 = False

    #기본 루프
    def baseline(self):
        while_count = 0
        self.base_parameter()
        try:
            while True:
                self.stopThreadUntilOneTheEnd()
                # self.status_print()
                # self.base_move()
                self.web_interaction()
                self.interaction()
                time.sleep(0.1)
                while_count += 1
        except KeyboardInterrupt:
            #stop
            sys.exit(0)
        print("exit")

    #맵 종류
    #2024-02-14T082317.984Z.explo(8층 pbl실 기본 explore() 맵)
    #2024-02-16T133625.109Z.explo(앞 부분만 찍은 explore() 맵)
        #2024-02-16T140640.347Z.explo
        #2024-02-16T140903.087Z.explo( 의자로 맵 만든 거 explore())
        #2014-04-04T023359.452Z.explo( 의자로 맵 만든 거2)
        #2014-04-04T030206.953Z.explo(세번째)
    #맵 로드 후 로컬라이제이션
    def load_map_and_localization(self):
        self.event.set()
        self.robot.stop_localization()
        # self.robot.load_map(file_name="2024-02-15T080619.628Z.explo")
        # self.robot.load_map(file_name="2024-02-15T074705.482Z.explo")
        self.robot.load_map(file_name="2024-02-14T082317.984Z.explo")

        self.robot.first_localization()
        self.event.clear()
    

    def move(self,x,y):
        self.event.set()
        self.robot.navigate_to(x, y)
        self.event.clear()
        print("end")

    def session_reset(self):
        self.robot.session.reset

    #error
    def sonar_getdata(self):
        print("sonarleft" , self.robot.sonar_service.SonarLeftDetected())
        print("sonarright" ,self.robot.sonar_service.SonarRightDetected())
        print("sonarnothingleft", self.robot.sonar_service.SonarLeftNothingDetected())
        print("sonarnothingright",self.robot.sonar_service.SonarRightNothingDetected())
        pass

    #no need
    def security_data(self):
        print("othogna:" ,self.robot.motion_service.getOrthogonalSecurityDistance())
        print("tangential:" ,self.robot.motion_service.getTangentialSecurityDistance())
        print("enable security: ", self.robot.motion_service.getExternalCollisionProtectionEnabled("All"))
        # print("aa: ", self.robot.motion_service.isCollision())


    #기본 움직임
    def base_move(self):
        # print((round(self.robot.motion_service.getAngles("HeadPitch", True)[0],1)+0.5)*10)
        # self.robot.motion_service.move(0,0,(round(self.robot.motion_service.getAngles("HeadPitch", True)[0],1)+0.5)*10)
        # self.robot.motion_service.move(1,0,0)
        print((round(self.robot.motion_service.getAngles("HeadYaw", True)[0],1)))
        self.robot.motion_service.move(0,0,(round(self.robot.motion_service.getAngles("HeadYaw", True)[0],1)))
        self.robot.motion_service.move(1,0,0)


    #GUI에 기능 적용
    def base_interface_robot(self):
        self.window.geometry("1200x600")
        self.window.title("pepper")
        self.exploration_pepper_button()
        self.navigation_pepper_button()
        self.navigation_pepper_button2()
        self.webpage_reset_button()
        self.show_map_button()
        self.slam_start_button()
        self.slam_stop_button()
        #마지막에 있어야함
        self.window.mainloop()
    
    def exploration_mode_button_push(self):
        self.event.set()
        self.robot.exploration_mode(5)
        self.event.clear()

    def navigation_mode_button_push(self):
        self.event.set()           
        move_pepper = threading.Thread(target=self.move(0,2))
        move_pepper.start()  
        self.event.clear()

    def navigation_mode_button_push2(self):
        self.event.set()               
        move_pepper = threading.Thread(target=self.move(0,0))
        move_pepper.start()  
        self.event.clear()

    def show_map_button_push(self):
        self.event.set()               
        show_map_thread = threading.Thread(target=self.robot.show_map)
        show_map_thread.start()
        show_map_thread.join()
        imshow_map_thread = threading.Thread(target=self.imshow_map)
        imshow_map_thread.start()   
        self.event.clear()

    def imshow_map(self):
            cv2.imshow("RobotMap", self.robot.robot_map)
            cv2.setMouseCallback("RobotMap", self.mouse_callback)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flags, param):
        # 마우스 왼쪽 버튼을 클릭할 때
        if event == cv2.EVENT_LBUTTONDOWN:
            # map_y = (x * self.robot.resolution + self.robot.offset_x)
            # map_x = (y * self.robot.resolution - self.robot.offset_y)
            map_x = (x * self.robot.resolution + self.robot.offset_x)
            map_y = -1 * (y * self.robot.resolution - self.robot.offset_y)
            # map_x = x
            # map_y = y
            print("mouse click:", map_x, map_y)
            self.move(map_x,map_y)
            pos = self.robot.pos[0]
            goal_x = (pos[0] - self.robot.offset_x) / self.robot.resolution
            goal_y = -1 * ((pos[1] - self.robot.offset_y) / self.robot.resolution)
            self.show_map_button_push()
            self.robot.robot_map = cv2.circle(self.robot.robot_map, (int(goal_x), int(goal_y)), 3, (255, 0, 0), -1)

    def web_page_reset(self):
        self.event.set()
        self.web_thread = threading.Thread(target=self.robot.show_web(web_page))
        self.web_thread.start()     
        self.robot.say("web page reset")
        self.event.clear()

    def move(self,x,y):
        self.event.set()
        self.robot.navigate_to(x, y)
        self.event.clear()

    def slam_start_button_push(self):
        self.event.set()
        self.slam_start_thread = threading.Thread(target=self.robot.slam(status=True))
        self.event.clear()

    def slam_stop_button_push(self):
        self.event.set()
        self.slam_stop_thread = threading.Thread(target=self.robot.slam(status=False))
        self.event.clear()

    def session_reset(self):
        self.robot.session.reset


    #gui 기능(버튼 등) 설계
    def navigation_pepper_button(self):
        button = Tkinter.Button(self.window, text="이동(2,0)", command=self.navigation_mode_button_push)
        button.pack()
        self.window.bind("<")

    def navigation_pepper_button2(self):
        button = Tkinter.Button(self.window, text="이동(0,0)", command=self.navigation_mode_button_push2)
        button.pack()
        self.window.bind("<")

    def exploration_pepper_button(self):
        button = Tkinter.Button(self.window, text="맵핑 모드", command=self.exploration_mode_button_push)
        button.pack()
        self.window.bind("<")

    def webpage_reset_button(self):
        button = Tkinter.Button(self.window, text="웹페이지 리셋", command=self.web_page_reset)
        button.pack()
        self.window.bind("<")

    def show_map_button(self):
        button = Tkinter.Button(self.window, text="맵 확인", command=self.show_map_button_push)
        button.pack()
        self.window.bind("<")

    def slam_start_button(self):
        button = Tkinter.Button(self.window, text="수동 맵핑 시작", command=self.slam_start_button_push)
        button.pack()
        self.window.bind("<")

    def slam_stop_button(self):
        button = Tkinter.Button(self.window, text="수동 맵핑 금지", command=self.slam_stop_button_push)
        button.pack()
        self.window.bind("<")
        # label = Tkinter.Label(self.window, text="안녕하세요!")
        # # 레이블 위치 설정
        # label.place(x=150, y=150)
        # 버튼 위치 설정
        # button.place(x=180, y=200)

def main():
    pepper = KUpepper("192.168.0.125", "9559")
    

if __name__ == "__main__":
    base_thread = threading.Thread(target=main)
    base_thread.daemon = True
    base_thread.start()
    app.run(host=web_host, port=80, debug=False)

    # main()
    

    

    
