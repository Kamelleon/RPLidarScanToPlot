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
        for (scan_flag, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_lidar_data(scan_data)


def process_lidar_data(data):
    global movement_step
    # global movement_step_pickled
    global movement_step_f

    global max_plot_length

    # For storing the data until it reaches 400000
    if movement_step_f <= 400000:
        movement_step_f += 5000
    else:
        movement.clear()
        x_pickled.clear()
        y_pickled.clear()
        movement_step_f = 0

    # For updating the plot every 2 scans
    if movement_step <= max_plot_length:
        movement_step += 5000
        # movement_step_pickled += 5000
    else:
        pickle.dump(x_pickled, open('x_pickled.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(y_pickled, open('y_pickled.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        # pickle.dump(movement_pickled, open('movement_pickled.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(movement, open('movement_f.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        movement_step = 0

    for angle in range(start_scan_range, end_scan_range):
        distance = data[angle]
        if min_scan_distance < distance < max_scan_distance:
            radians = angle * pi / 180.0

            x_pickled.append(distance * cos(radians))

            y_pickled.append(distance * sin(radians))

            # movement_pickled.append(movement_step_pickled)

            movement.append(movement_step_f)

            csv_file.write(str(distance * cos(radians)) + "," +
                           str(distance * sin(radians)) + "," +
                           str(movement_step_pickled) + "\n")


if __name__ == "__main__":

    PORT = 'COM3'

    start_scan_range = 70
    end_scan_range = 110

    min_scan_distance = 0
    max_scan_distance = 400

    movement_step_f = 0
    movement_step = 0
    movement_step_pickled = 0

    max_plot_length = 5000

    x_pickled = []

    y_pickled = []

    movement_pickled = []

    movement = []

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
