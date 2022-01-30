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
            print("\n[!] Restarting LiDAR device due to an error:", str(lidar_exception), "\n")
            lidar.stop_motor()
            lidar.stop()
            lidar.disconnect()
            sleep(10)
            lidar.connect()
            lidar.start_motor()
            lidar.set_pwm(1023)

            sleep(3)
            pass
        except KeyboardInterrupt:
            print("[!] Ctrl+C detected. Exiting...")

            lidar.stop_motor()
            lidar.stop()
            lidar.disconnect()

            print("[+] LiDAR device correctly disconnected.")

            exit()


def lidar_scan_initialization():
    global first_scan
    global SCANNER_SPEED
    print("[~] Starting motor of LiDAR device...")
    lidar.start_motor()
    print("[+] LiDAR motor started successfully")
    print("[~] Initializing the scan procedure...")
    sleep(4)
    try:
        for scan in lidar.iter_scans(max_buf_meas=1500):
            lidar.set_pwm(SCANNER_SPEED)
            if first_scan:
                print("[+] Scanning procedure started successfully!\n")
                print("[~] Scanning in progress... Press Ctrl+C to stop.\n")
                first_scan = False
            for (scan_flag, raw_angle, raw_distance) in scan:
                raw_scan_data[min([359, int(raw_angle)])] = raw_distance
            process_lidar_data(raw_scan_data)
    except KeyboardInterrupt:
        lidar.stop_motor()
        lidar.stop()
        lidar.disconnect()
        print("[!] Ctrl+C detected. Exiting...")
        exit()


def process_lidar_data(data):
    global current_movement
    global movement_step_for_live
    global movement_step_for_file
    global MAX_PLOT_LENGTH_TO_UPDATE
    global stop
    global scan_number
    global saved
    global stop_scaning

    # if not stop:
    #     movement_step_for_live += 1
    #     movement_step_for_file += 1
    #     saved = False
    # else:
    #     if not saved:
    #         pickle.dump(x_for_file, open('x_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    #         pickle.dump(distance_for_file, open('distance_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    #         pickle.dump(movement_for_file, open('movement_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    #
    #         x_for_file.clear()
    #         distance_for_file.clear()
    #         movement_for_file.clear()
    #
    #         movement_step_for_file = 0
    #         scan_number += 1
    #
    #         saved = True
    #
    #     x_for_live.clear()
    #     distance_for_live.clear()
    #     movement_for_live.clear()
    #
    #     movement_step_for_live = 0
    #     current_movement = 0

    print("Prędkość obrotu lasera:",SCANNER_SPEED,"PWM")
    if not stop:
        movement_step_for_live += 1
        movement_step_for_file += 1
        saved = False

    if current_movement <= MAX_PLOT_LENGTH_TO_UPDATE:
        current_movement += MAX_PLOT_LENGTH_TO_UPDATE
    else:
        pickle.dump(x_for_live, open('x_live.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(distance_for_live, open('distance_live.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(movement_for_live, open('movement_live.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

    if len([*filter(lambda x: x >= 900, data[80:100])]) > 0:
        print("Bret pod laserem: NIE")
        stop_scaning = True
    else:
        stop_scaning = False
        print("Bret pod laserem: TAK")
    for angle in range(START_SCAN_RANGE, END_SCAN_RANGE+1):
        raw_distance = data[angle]

        print("Kąt:",angle,"Wartość:", data[angle])

        if raw_distance < MAX_SCAN_DISTANCE:
            # print("Not stopped")
            stop = False

            radians = angle * pi / 180.0

            x_for_live.append(raw_distance * cos(radians))

            distance_for_live.append(raw_distance * sin(radians))

            x_for_file.append(raw_distance * cos(radians))

            distance_for_file.append(raw_distance * sin(radians))

            movement_for_live.append(movement_step_for_live)
            movement_for_file.append(movement_step_for_file)
       # elif raw_distance > MAX_SCAN_DISTANCE and raw_distance < 1200:
            #continue
        elif stop_scaning:
            # print("Stopped")
            stop = True
            # if not saved:
            #     pickle.dump(x_for_file, open('x_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            #     pickle.dump(distance_for_file, open('distance_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            #     pickle.dump(movement_for_file, open('movement_scan_' + str(scan_number) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            #
            #     x_for_file.clear()
            #     distance_for_file.clear()
            #     movement_for_file.clear()
            #
            #     movement_step_for_file = 0
            #     scan_number += 1
            #
            #     saved = True

            x_for_live.clear()
            distance_for_live.clear()
            movement_for_live.clear()

            movement_step_for_live = 0
            current_movement = 0

if __name__ == "__main__":

    if platform == 'win32':
        PORT = 'COM5'
    else:
        PORT = '/dev/ttyUSB0'

    START_SCAN_RANGE = 55
    END_SCAN_RANGE = 125

    MAX_SCAN_DISTANCE = 1000
    SCANNER_SPEED =400
    MAX_PLOT_LENGTH_TO_UPDATE = 1
    stop_scaning = False
    movement_step_for_live = 0
    current_movement = 0
    movement_step_pickled = 0
    movement_step_for_file = 0
    scan_number = 1

    first_scan = True
    stop = True
    saved = True

    x_for_live = []
    x_for_file = []
    distance_for_live = []
    distance_for_file = []
    movement_for_live = []
    movement_for_file = []

    raw_scan_data = [0] * 360


    try:
        print("[~] Connecting to LiDAR device on port: " + str(PORT) + " ...")
        lidar = rplidar.RPLidar(PORT)
        print("[+] Successfully connected to LiDAR device!")
    except Exception as e:
        print("[-] An error has occurred while trying to connect with LiDAR device:", str(e))
        print_exc()
        exit()

    lidar_handler()
