from Servo_control import Servo


cel = int(input('Type channel:'))

servo = Servo(cel)

while True:
    angel = input('Type angel:')

    if angel == 'q':
        print('Break!')
        break
    else:
        angel = int(angel)
    servo.run(angel)
