from math import cos, sin, pi, floor
import rplidar
import matplotlib.pyplot as plt
import traceback
import sys
import numpy as np
import time


def lidar_information():
    lidar.get_info()  # Get information about hardware, model etc. - check if LiDAR is connected


def process_data(data):
    global x  # Get lists of coordinates
    global y
    global iteracja
    global old_scan
    global dystansik
    global scan_data

    if (iteracja <= 200000):
        iteracja += 4500
    else:
        plt.clf()
        iteracja = 0

    if old_scan[70:75] != scan_data[70:75]:
        for angle in range(70, 110):
                        distance = data[angle]
                        if distance > 0 and distance < 400:  # Ignore initially ungathered data points
                            radians = angle * pi / 180.0  # For changing degrees to radians
                            # Calculate x coordinate
                            y.append(distance * sin(radians))  # Calculate y coordinate
                            x.append(distance * cos(radians))
                            # x.extend(range(y[1], len(y)))
                            przesuniecie.append(1 + iteracja)
                            # dystansik.append(distance)
                            # print("X:", distance * cos(radians), "\nY:", distance * sin(radians))
                            # old_scan.clear()
                            # scan_data.clear()

    del old_scan

    # plt.clf()  # Clear plot
    plt.ylim(-200, 200000)  # Set plot limits on x and y
    plt.xlim(-200, 200)

    plt.title('LiDAR - scan')  # Set plot title
    plt.xlabel("X")  # Set X label
    plt.ylabel("Y")  # Set Y label

    plt.gca().invert_xaxis()  # Invert x-axis direction to show correctly left and right sides

    plt.scatter(x, przesuniecie, s=1, c=y, cmap='coolwarm_r', vmin=190, vmax=210, marker='s')  # Show plot

    x.clear()  # Clear lists of coordinates
    y.clear()


    przesuniecie.clear()


    plt.pause(0.01)  # Pause plot



if __name__ == "__main__":

    PORT = 'COM3'  # LiDAR Port


    iteracja = 0
    przesuniecie = []
    x = []  # Initialize lists with coordinates of object
    y = []

    scan_data = [0] * 360  # Initialize list with scan angle indexes

    try:
        print("[~] Connecting to LiDAR device on port: " + str(PORT) + " ...")
        lidar = rplidar.RPLidar(PORT)  # Initialize LiDAR connection
        print("[+] Connected to LiDAR device")
    except rplidar.RPLidarException as e:  # If couldn't detect LiDAR device on specified port
        print("[-] Critical Error: " + str(e))
        print("[!] Consider changing port or install drivers for your LiDAR device")
        sys.exit()  # Exit program

    try:
        print("[~] Starting LiDAR...")
        lidar_information()  # Check connection with LiDAR by getting info about the device
        print("[+] LiDAR device started successfully")
    except rplidar.RPLidarException as e:
        if "descriptor" in str(e):
            print("[-] ERROR: " + str(e) + "\n[~] Attempting to restart LiDAR device...")
            lidar.stop_motor()
            lidar.stop()
            lidar.disconnect()
            lidar.connect()
            lidar.start_motor()
            lidar.set_pwm(1000)
            lidar_information()
            print("[+] LiDAR device started successfully.")
        else:
            print(traceback.print_exc())

    try:
        print("[~] Creating LiDAR plot...")
        print("[!] Press Ctrl+C in console window in order to exit the program")
        time.sleep(3)
        z = 0
        lidar.set_pwm(700)
        for scan in lidar.iter_scans(max_buf_meas=10000):  # Set max buffer size for data and keep scanning
            old_scan = scan_data[:]
            for (_, angle, distance) in scan:
                if 70 <= floor(angle) <= 110:  # Set scan angle
                    scan_data[min([359, floor(angle)])] = distance


            # scan_data = [round(x) for x in scan_data]

            process_data(scan_data)  # Push data into function









    except Exception as e:  # If 'ctrl+c' in console then disconnect LiDAR device to prevent descriptor error on next run
        print(e)
        print("[!] Ctrl+C detected: Exiting...")
        lidar.stop()
        lidar.disconnect()
        print("[+] LiDAR device correctly disconnected")
        sys.exit()
