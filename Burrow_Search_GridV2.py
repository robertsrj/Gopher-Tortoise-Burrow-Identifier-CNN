from djitellopy import Tello
import threading
import cv2
from time import sleep

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

#Takeoff
tello.takeoff()
print(tello.get_battery())

width = input("Search Area Width (meters):")
depth = input("Search Area Depth (meters):")

def take_pic():
    count = 0
    while True:
        # Convert BGR to RGB before saving
        rgb_frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(f"picture{count}.png", rgb_frame)
        count += 1
        sleep(4)

# Start seperate thread
threading.Thread(target = take_pic, daemon=True).start()

# Grid
for i in range(width):
    tello.move_forward(int(depth) * 100)
    tello.rotate_clockwise(180)
    tello.move_forward(int(depth) * 100)
    tello.rotate_counter_clockwise(90)
    tello.move_forward(1000)
    tello.rotate_counter_clockwise(90)

tello.land()