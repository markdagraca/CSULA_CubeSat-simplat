import socketio
import time
# standard Python
sio = socketio.Client()

sio.connect('http://localhost:5000')
for x in range(0,100):  
    sio.emit('move', {'x':100-x,'y':x})
    time.sleep(1/10)

time.sleep(5)
sio.disconnect()