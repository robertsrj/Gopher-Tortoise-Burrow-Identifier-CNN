# Import Neccesary Libraries
from djitellopy import Tello
import threading
from datetime import datetime
import os; os.system("cls")
import cv2
from time import sleep

# Setup
tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()
print(tello.get_battery())

SPEED = 50
tello.set_speed(SPEED)

x_pos = 0
y_pos = 0
track_pos = False
orientation = 0
depth = 300 # Replace with user input


def seconds_measure():
    # Returns seconds from midnight, used for drone positioning
    return datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second

# Main code for the secondary thread
def second_thread():
    Running = True
    global track_pos
    global x_pos
    global y_pos

    # Main loop for secondary thread
    while Running == True:
        # Start tracking position
        if track_pos == True:

            # Forwards relative to start
            if orientation == 0:
                x_start_time = seconds_measure()
                starting_x_pos = x_pos

                while track_pos == True:
                    x_elapsed_time = seconds_measure() - x_start_time
                    x_pos = (x_elapsed_time * SPEED) + starting_x_pos
                    print(f"\r\033[KX Position: {x_pos} Y Position: {y_pos}", end = "", flush = True)

                    if x_elapsed_time >= depth / SPEED:
                        track_pos = False

            # Backwards relative to start
            if orientation == 180:
                x_start_time = seconds_measure()
                starting_x_pos = x_pos

                while track_pos == True:
                    x_elapsed_time = seconds_measure() - x_start_time
                    x_pos = (x_elapsed_time * (SPEED * -1)) + starting_x_pos
                    print(f"\r\033[KX Position: {x_pos} Y Position: {y_pos}", end = "", flush = True)

                    if x_elapsed_time >= depth / SPEED:
                        track_pos = False

            # Right relative to start
            if orientation == 90:
                y_start_time = seconds_measure()
                starting_y_pos = y_pos

                while track_pos == True:
                    y_elapsed_time = seconds_measure() - y_start_time
                    y_pos = (y_elapsed_time * SPEED) + starting_y_pos
                    print(f"\r\033[KX Position: {x_pos} Y Position: {y_pos}", end = "", flush = True)

                    if y_elapsed_time >= depth / SPEED:
                        track_pos = False

            # Left Relative to start
            if orientation == 270:
                y_start_time = seconds_measure()
                starting_y_pos = y_pos

                while track_pos == True:
                    y_elapsed_time = seconds_measure() - y_start_time
                    y_pos = (y_elapsed_time * (SPEED * -1)) + starting_y_pos
                    print(f"\r\033[KX Position: {x_pos} Y Position: {y_pos}", end = "", flush = True)

                    if y_elapsed_time >= depth / SPEED:
                        track_pos = False

def third_thread():
    while True:
        if tello.get_flight_time() % 4 == 0:
            # Convert BGR to RGB before saving
            rgb_frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f"Time {tello.get_flight_time()} X Pos  {x_pos} Y Pos  {y_pos}.png", rgb_frame)
        sleep(0.1)

# Start seperate threads
t2 = threading.Thread(target = second_thread)
t3 = threading.Thread(target = third_thread)
t2.start()
t3.start()

# Takeoff
tello.takeoff()

# Grid
track_pos = True
tello.move_forward(depth)

tello.rotate_clockwise(90)
orientation += 90

track_pos = True
tello.move_forward(depth)

tello.rotate_clockwise(90)
orientation += 90

track_pos = True
tello.move_forward(depth)

tello.rotate_clockwise(90)
orientation += 90

track_pos = True
tello.move_forward(depth)

tello.land()
t2.join()
t3.join()
tello.end()


# for i in range(width):
#     # Go forward and back in line
#     tello.move_forward(depth)
#     tello.rotate_clockwise(180)
#     tello.move_forward(depth)

#     # Turn and go 10 meters to the left and then turn back
#     tello.rotate_clockwise(90)
#     tello.move_forward(1000)
#     tello.rotate_counter_clockwise(90)

# tello.land()