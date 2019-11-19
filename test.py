import socketio
import time


sio = socketio.Client()

sio.connect('http://192.168.43.209:5000')
for x in range(0,100):  
    sio.emit('thruster', {'forward':100-x,'left':x})
    time.sleep(1/10)

time.sleep(5)
sio.disconnect()