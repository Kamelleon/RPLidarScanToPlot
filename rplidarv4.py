import time
import sys
import traceback
from math import cos, sin, pi, floor
import rplidar
import pickle


def lidar_handler():
    while True:
        try:
            lidar_scan_initialization()
        except rplidar.RPLidarException as e:
            traceback.print_exc()
            lidar.stop_motor()
            lidar.stop()
            lidar.disconnect()
            time.sleep(0.01)
            lidar.connect()
            lidar.start_motor()
            lidar.set_pwm(1000)
            time.sleep(3)
            print("\n[!] Restarting LiDAR device due to an error:", str(e), "\n")
            pass
        except KeyboardInterrupt:
            csv_file.close()
            print("[!] Ctrl+C detected. Exiting...")
            lidar.stop_motor()
            lidar.stop()
            lidar.disconnect()
            print("[+] LiDAR device correctly disconnected.")
            sys.exit()


def lidar_scan_initialization():
    print("[~] Starting motor of LiDAR device...")
    lidar.start_motor()
    print("[+] LiDAR motor started successfully")
    print("[~] Initializing the scan procedure...")
    time.sleep(3)
    for scan in lidar.iter_scans(max_buf_meas=1500):
        lidar.set_pwm(1000)
        for (scan_flag, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_lidar_data(scan_data)


def process_lidar_data(data):
    global movement_step
    global movement_step_for_list
    global movement_static_step
    global max_plot_length
    global stop
    global num
    global saved

    # For storing the data until it reaches 400000
    if not stop and movement_step_for_list <= 120:
        movement_step_for_list += 1
        movement_static_step += 1
        saved = False
    else:
        if not saved:
            pickle.dump(x_static, open('x_scan_' + str(num) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(y_static, open('distance_scan_' + str(num) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(movement_static, open('movement_scan_' + str(num) + '.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            x_static.clear()
            y_static.clear()
            movement_static.clear()
            movement_static_step = 0
            num += 1
            saved = True
        x_pickled.clear()
        distance.clear()
        movement_pickled.clear()
        movement_step_for_list = 0
        movement_step = 0

    # For updating the plot every scan
    if movement_step <= max_plot_length:
        movement_step += max_plot_length
    else:
        pickle.dump(x_pickled, open('x_pickled.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(distance, open('distance.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(movement_pickled, open('movement_pickled.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

    for angle in range(start_scan_range, end_scan_range):
        distance_raw = data[angle]

        if distance_raw < max_scan_distance:
            stop = False
            radians = angle * pi / 180.0

            x_pickled.append(distance_raw * cos(radians))
            x_static.append(distance_raw * cos(radians))

            distance.append(distance_raw * sin(radians))
            # print(distance_raw*sin(radians))
            y_static.append(distance_raw * sin(radians))

            movement_pickled.append(movement_step_for_list)
            movement_static.append(movement_static_step)

            csv_file.write(str(distance_raw * cos(radians)) + "," +
                           str(distance_raw * sin(radians)) + "," +
                           str(movement_static_step) + "\n")
        else:
            stop = True



if __name__ == "__main__":

    PORT = 'COM3'

    start_scan_range = 80
    end_scan_range = 100
    movement_static_step = 0

    max_scan_distance = 379

    stop = True
    movement_step_for_list = 0
    movement_step = 0
    movement_step_pickled = 0
    num = 1
    max_plot_length = 1
    saved = True
    x_pickled = []
    x_static = []
    distance = []
    y_static = []
    movement_pickled = []
    movement_static = []
    scan_data = [0] * 360

    csv_file = open("lidar_data.csv", "w")

    try:
        print("[~] Connecting with LiDAR device on port: " + str(PORT) + " ...")
        lidar = rplidar.RPLidar(PORT)
        print("[+] Successfully connected with LiDAR device")
    except Exception as e:
        print("[-] An error has occurred while trying to connect with LiDAR device:", str(e))
        traceback.print_exc()
        sys.exit()

    lidar_handler()
