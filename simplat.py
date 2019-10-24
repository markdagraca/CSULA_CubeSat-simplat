class simplat():
    def __init__(self):
        from apscheduler.schedulers.background import BackgroundScheduler

        self.scheduler=BackgroundScheduler()
        self.seconds=1.0/10
        self.percent=10
        self.scheduler.add_job(self.__Servoblaster,'interval', seconds=self.seconds)
        self.scheduler.start()
        self.x=0
        self.y=0        
        self.joystick_x=0
        self.joystick_y=0
    def update(self,joystick_x,joystick_y):
        import pygame
        from pygame import locals

        self.joystick_x=joystick_y
        self.joystick_y=joystick_x

        pwm_no_motion = 1520    # This is the pwm for no motion in us (1520us)
        pwm_delta_full_speed = 180    # This is the pulse width that will be added/subtracted from the no motion pwm in us (180us)

        servo_0 = int(pwm_no_motion + self.x/100 * pwm_delta_full_speed)    # Determine the pwm for the desired motion
        servo_2 = int(pwm_no_motion - self.x/100 * pwm_delta_full_speed)    # Determine the pwm for the desired motion

        servo_1 = int(pwm_no_motion - self.y/100 * pwm_delta_full_speed)    # Determine the pwm for the desired motion
        servo_3 = int(pwm_no_motion + self.y/100* pwm_delta_full_speed)    # Determine the pwm for the desired motion

        import os
        os.system("echo 0=" + str(servo_0) + "us > /dev/servoblaster")
        os.system("echo 1=" + str(servo_1) + "us > /dev/servoblaster")
        os.system("echo 2=" + str(servo_2) + "us > /dev/servoblaster")
        os.system("echo 3=" + str(servo_3) + "us > /dev/servoblaster")




    def __Servoblaster(self):
        formula=self.seconds*self.percent/100
        print("formula "+str(formula))

        self.joystick_x=formula*self.joystick_x
        self.joystick_y=formula*self.joystick_y
        self.x+=self.joystick_x
        self.y+=self.joystick_y





        if(abs(self.x)>100):
            self.x=100*self.x/abs(self.x)
        if(abs(self.y)>100):
            self.y=100*self.y/abs(self.y)
        print("X: "+str(self.x))
        print("Y: "+str(self.y)+" \n \n")





simplat=simplat()

import pygame
from pygame import locals
import os

pygame.init()
os.putenv('SDL_VIDEODRIVER', 'fbcon')
pygame.display.init()
pygame.joystick.init() # main joystick device system


try:
	j = pygame.joystick.Joystick(0) # create a joystick instance
	j.init() # init instance
	print ('Enabled joystick: ' + j.get_name())
	print ('  Number of axis: ' + str(j.get_numaxes()))
	print ('  Number of buttons: ' + str(j.get_numbuttons()))
except pygame.error:
	print ('no joystick found.')
	quit()

deadband = 0.2		# This is used to provide a dead band for the controller


while True:
    pygame.event.pump()

    a0,a1,a3 = j.get_axis(0), j.get_axis(1), j.get_axis(3)


    if abs(a0)<=deadband:
        a0=0

    if abs(a1)<=deadband:
        a1=0

    x=0
    y=0

    # print a0,a1,a3		
    if(a0!=0 or a1!=0):
        # print('Translate')
        x = int(a0 * 100)    # Determine the pwm for the desired motion
        y = int(a1 * 100)    # Determine the pwm for the desired motion


    else:
        # print ('Stop')
        x = 0
        y = 0

    simplat.update(x,-y)
