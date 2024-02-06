#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qi
import Tkinter
from robot import Pepper
import threading
import sys
import time

class KUpepper:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.window = Tkinter.Tk()
        self.robot = Pepper(self.ip, self.port)
        self.robot.say("HI Pepper")
        self.event = threading.Event()
        self.event2 = threading.Event()
        self.base_thread = threading.Thread(target=self.baseline)
        self.base_thread.daemon = True
        self.base_thread.start()        
        self.base_interface_robot()

        self.base_thread.join() 
        #connect
    def baseline(self):
        
        count = 0
        self.robot.set_security_distance(distance=0.5)
        try:
            while True:
                if self.event.is_set():
                    while True:
                        if self.event.is_set():
                            time.sleep(0.1)
                        else:
                            break
                else:
                    pass

                if count == 0:
                    self.localize = threading.Thread(target= self.localization())
                    self.localize.start()                
         
                if count == 1:
                    move_pepper = threading.Thread(target=self.move(0,0))
                    move_pepper.start()        

                if count == 3:
                    move_pepper = threading.Thread(target=self.move(3,0))
                    move_pepper.start()                      
                # self.sonar_getdata()
                # self.security_data()
                print(self.robot.user_session.getOpenUserSessions())
                if count == 99999:
                    explor = threading.Thread(target=self.robot.exploration_mode(1))
                    explor.start()
                    print("explor mode start")
                time.sleep(0.1)
                self.base_move()
                count += 1
                print(self.robot.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))
                if self.robot.memory_service.getData("Device/SubDeviceList/Head/Touch/Front/Sensor/Value"):
                    self.robot.say("Get your hands off my head loser")
                # print("laser x:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Vertical/Right/Seg01/X/Sensor/Value"))
                # print("laser y:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Vertical/Right/Seg01/Y/Sensor/Value"))
                print("a", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Reg/Status/Sensor/Value"))
                # if count > 3:
                #     pos =self.robot.navigation_service.getRobotPositionInMap()
                #     print("robot_pos: " ,pos)
        except KeyboardInterrupt:
            #stop
            sys.exit(0)
        print("exit")

    def localization(self):
        self.event2.set()
        self.robot.stop_localization()
        self.robot.load_map(file_name="map.png",file_path="./tmp_files/version_0/")
        self.robot.robot_localization()
        #print(self.robot.navigation_service.getMetricalMap())

        self.event2.clear()

    def base_interface_robot(self):
        self.window.geometry("1200x600")
        self.window.title("pepper")
        self.exploration_pepper_button()
        #마지막에 있어야함
        self.window.mainloop()
        
    def exploration_mode_button_push(self):
        self.event.set()
        self.robot.exploration_mode(1)
        self.event.clear()


    def move(self,x,y):
        self.event2.set()
        self.robot.navigate_to(x, y)
        self.event2.clear()
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



    def exploration_pepper_button(self):
        button = Tkinter.Button(self.window, text="맵핑 모드", command=self.exploration_mode_button_push)
        button.pack()
        self.window.bind("<")
        # label = Tkinter.Label(self.window, text="안녕하세요!")
        # # 레이블 위치 설정
        # label.place(x=150, y=150)
        

        # 버튼 위치 설정
        # button.place(x=180, y=200)

def main():
    pepper = KUpepper("192.168.0.125", "9559")
    pepper.localization()


if __name__ == "__main__":
    main()
    

    

    
