from math import cos, sin, pi, floor
import pickle
import rplidar
from sys import exit, platform
from time import sleep
from traceback import print_exc


def lidar_handler():
    while True:
        try:
            lidar_scan_initialization()
        except rplidar.RPLidarException as lidar_exception:
            print_exc()

            lidar.stop_motor()
            lidar.stop()
            lidar.disconnect()
            sleep(4)
            lidar.connect()
            lidar.start_motor()
            lidar.set_pwm(1000)

            sleep(3)
            print("\n[!] Restarting LiDAR device due to an error:", str(lidar_exception), "\n")
            pass
        except KeyboardInterrupt:
            # csv_file.close()
            print("[!] Ctrl+C detected. Exiting...")

            lidar.stop_motor()
            lidar.stop()
            lidar.disconnect()

            print("[+] LiDAR device correctly disconnected.")

            exit()


def lidar_scan_initialization():
    print("[~] Starting motor of LiDAR device...")
    lidar.start_motor()
    print("[+] LiDAR motor started successfully")
    print("[~] Initializing the scan procedure...")
    sleep(3)
    for scan in lidar.iter_scans(max_buf_meas=1500):
        # lidar.set_pwm(1000)
        for (scan_flag, raw_angle, raw_distance) in scan:
            raw_scan_data[min([359, floor(raw_angle)])] = raw_distance
        process_lidar_data(raw_scan_data)


def process_lidar_data(data):
    global current_movement
    global movement_step_for_live
    global movement_step_for_file
    global MAX_PLOT_LENGTH_TO_UPDATE
    global stop
    global scan_number
    global saved

    if not stop:
        movement_step_for_live += 1
        movement_step_for_file += 1
        saved = False
    else:
        if not saved:
            pickle.dump(x_for_file, open('x_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(distance_for_file, open('distance_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(movement_for_file, open('movement_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

            x_for_file.clear()
            distance_for_file.clear()
            movement_for_file.clear()

            movement_step_for_file = 0
            scan_number += 1

            saved = True

        x_for_live.clear()
        distance_for_live.clear()
        movement_for_live.clear()

        movement_step_for_live = 0
        current_movement = 0

    if current_movement <= MAX_PLOT_LENGTH_TO_UPDATE:
        current_movement += MAX_PLOT_LENGTH_TO_UPDATE
    else:
        pickle.dump(x_for_live, open('x_live.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(distance_for_live, open('distance_live.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(movement_for_live, open('movement_live.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

    for angle in range(START_SCAN_RANGE, END_SCAN_RANGE):
        raw_distance = data[angle]

        if raw_distance < MAX_SCAN_DISTANCE:
            stop = False

            radians = angle * pi / 180.0

            x_for_live.append(raw_distance * cos(radians))

            distance_for_live.append(raw_distance * sin(radians))

            x_for_file.append(raw_distance * cos(radians))

            distance_for_file.append(raw_distance * sin(radians))

            movement_for_live.append(movement_step_for_live)
            movement_for_file.append(movement_step_for_file)

            # csv_file.write(str(raw_distance * cos(radians)) + "," +
            #                str(raw_distance * sin(radians)) + "," +
            #                str(movement_step_for_file) + "\n")
        else:
            stop = True


if __name__ == "__main__":

    if platform == 'win32':
        PORT = 'COM3'
    else:
        PORT = '/dev/ttyUSB0'

    START_SCAN_RANGE = 80
    END_SCAN_RANGE = 100

    MAX_SCAN_DISTANCE = 379

    MAX_PLOT_LENGTH_TO_UPDATE = 1

    movement_step_for_live = 0
    current_movement = 0
    movement_step_pickled = 0
    movement_step_for_file = 0
    scan_number = 1

    stop = True
    saved = True

    x_for_live = []
    x_for_file = []
    distance_for_live = []
    distance_for_file = []
    movement_for_live = []
    movement_for_file = []

    raw_scan_data = [0] * 360

    # csv_file = open("lidar_data.csv", "w")

    try:
        print("[~] Connecting with LiDAR device on port: " + str(PORT) + " ...")
        lidar = rplidar.RPLidar(PORT)
        print("[+] Successfully connected with LiDAR device")
    except Exception as e:
        print("[-] An error has occurred while trying to connect with LiDAR device:", str(e))
        print_exc()
        exit()

    lidar_handler()
