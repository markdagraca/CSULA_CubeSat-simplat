'''
This code will listen for events from a controller connected to the robot.

                F = (-1,0,0)
              Servo 0, Axis 1
(-0.707,-0.707,0)    ^     (-0.707,0.707,0)
                 \   |    /
                   -----
    L = (0,-1,0)  |     |  R = (0,1,0)
  Servo 1, Axis 0 |     | Servo 3, Axis 0
                   -----
                 /       \
 (0.707,-0.707,0)         (0.707,0.707,0)
                B = (1,0,0)
              Servo 2, Axis 1

		Rotate: Axis 3 (CCW -1, CW 1)
			  
Notes:				  
 - Servo PWM signal ranges from full clockwise speed = 1300us, no movement = 1520us, full counter clockwise = 1700us
 - Bluetooth connection notes: https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html
 - Make sure that ServoBlaster is started with the --pcm flag (when using pygame)
 - This script can be auto launched by adding it to the /etc/rc.local file
'''

import pygame
from pygame import locals
import os

pygame.init()
pygame.joystick.init() # main joystick device system

try:
	j = pygame.joystick.Joystick(0) # create a joystick instance
	j.init() # init instance
	print 'Enabled joystick: ' + j.get_name()
	print '  Number of axis: ' + str(j.get_numaxes())
	print '  Number of buttons: ' + str(j.get_numbuttons())
except pygame.error:
	print 'no joystick found.'
	quit()

deadband = 0.2		# This is used to provide a dead band for the controller
pwm_no_motion = 1520    # This is the pwm for no motion in us (1520us)
pwm_delta_full_speed = 180    # This is the pulse width that will be added/subtracted from the no motion pwm in us (180us)

servo_0 = pwm_no_motion    # Initialize the servo pwm as no motion
servo_1 = pwm_no_motion    # Initialize the servo pwm as no motion
servo_2 = pwm_no_motion    # Initialize the servo pwm as no motion
servo_3 = pwm_no_motion    # Initialize the servo pwm as no motion

servo_0p = pwm_no_motion    # Previous servo command
servo_1p = pwm_no_motion    # Previous servo command
servo_2p = pwm_no_motion    # Previous servo command
servo_3p = pwm_no_motion    # Previous servo command
	
while True:
	pygame.event.pump()
	
	a0,a1,a3 = j.get_axis(0), j.get_axis(1), j.get_axis(3)
	# keys = pygame.key.get_pressed()
	# print keys
	# if keys[K_ESCAPE]:
		# print 'Escape key'
	
	# a0,a1,a2,a3,a4,a5 = j.get_axis(0), j.get_axis(1), j.get_axis(2), j.get_axis(3), j.get_axis(4), j.get_axis(5)
	# print 'a0, a1, a2, a3, a4, a5 : ' + str(a0) +' , '+ str(a1)+' , '+ str(a2)+' , '+ str(a3)+' , '+ str(a4)+' , '+ str(a5)
	# print j.get_axis(0), j.get_axis(1), j.get_axis(3)
	
	if abs(a0)<=deadband:
		a0=0
	
	if abs(a1)<=deadband:
		a1=0
					
	if abs(a3)<=deadband:
		a3=0
		
	# print a0,a1,a3		
	
	if a3!=0:  # Rotation
		# print ('Rotate')
		servo_0 = int(pwm_no_motion + a3 * pwm_delta_full_speed)    # Determine the pwm for the desired motion
		servo_2 = int(pwm_no_motion + a3 * pwm_delta_full_speed)    # Determine the pwm for the desired motion

		servo_1 = int(pwm_no_motion + a3 * pwm_delta_full_speed)    # Determine the pwm for the desired motion
		servo_3 = int(pwm_no_motion + a3 * pwm_delta_full_speed)    # Determine the pwm for the desired motion
		
	elif a0!=0 or a1!=0:  # Translation
		# print('Translate')
		servo_0 = int(pwm_no_motion + a0 * pwm_delta_full_speed)    # Determine the pwm for the desired motion
		servo_2 = int(pwm_no_motion - a0 * pwm_delta_full_speed)    # Determine the pwm for the desired motion

		servo_1 = int(pwm_no_motion - a1 * pwm_delta_full_speed)    # Determine the pwm for the desired motion
		servo_3 = int(pwm_no_motion + a1 * pwm_delta_full_speed)    # Determine the pwm for the desired motion
	else:
		# print ('Stop')
		servo_0 = pwm_no_motion
		servo_1 = pwm_no_motion
		servo_2 = pwm_no_motion
		servo_3 = pwm_no_motion
			

	# print servo_0,servo_1,servo_2,servo_3
	
	# print 'Servo 0:', servo_0
	# print 'Servo 1:', servo_1
	# print 'Servo 2:', servo_2
	# print 'Servo 3:', servo_3

	os.system("echo 0=" + str(servo_0) + "us > /dev/servoblaster")
	os.system("echo 1=" + str(servo_1) + "us > /dev/servoblaster")
	os.system("echo 2=" + str(servo_2) + "us > /dev/servoblaster")
	os.system("echo 3=" + str(servo_3) + "us > /dev/servoblaster")
