from time import sleep
from Servo_control import *

servo0 = Servo(3)
timer = datetime.datetime.now()
print(time)

servo0.information()
while True:
    servo0.run(0)
    time.sleep(2)
    servo0.run(90)

