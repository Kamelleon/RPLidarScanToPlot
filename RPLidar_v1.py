from math import cos, sin, pi, floor
import rplidar
import matplotlib.pyplot as plt
import traceback
import sys


def lidar_information():
    lidar.get_info()  # Get information about hardware, model etc. - check if LiDAR is connected


def process_data(data):
    global x  # Get lists of coordinates
    global y
    for angle in range(360):
        distance = data[angle]
        if distance > 0:  # Ignore initially ungathered data points
            radians = angle * pi / 180.0  # For changing degrees to radians
            x.append(distance * cos(radians))  # Calculate x coordinate
            y.append(distance * sin(radians))  # Calculate y coordinate

    plt.clf()  # Clear plot

    plt.ylim(-200, 600)  # Set plot limits on x and y
    plt.xlim(-300, 300)

    plt.title('LiDAR - scan')  # Set plot title
    plt.xlabel("X") # Set X label
    plt.ylabel("Y") # Set Y label

    plt.gca().invert_xaxis()  # Invert x-axis direction to show correctly left and right sides

    plt.scatter(x, y, s=6890, c=y, cmap='coolwarm_r', vmin=180, vmax=220, marker='s')  # Show plot

    x.clear()  # Clear lists of coordinates
    y.clear()

    plt.pause(0.01)  # Pause plot


if __name__ == "__main__":

    PORT = 'COM3'  # LiDAR Port

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
        sys.exit() # Exit program


    try:
        print("[~] Starting LiDAR...")
        lidar_information() # Check connection with LiDAR by getting info about the device
        print("[+] LiDAR device started successfully")
    except rplidar.RPLidarException as e:
        if "descriptor" in str(e):
            print("[-] ERROR: " + str(e) + "\n[~] Attempting to restart LiDAR device...")
            lidar.stop_motor()
            lidar.stop()
            lidar.disconnect()
            lidar.connect()
            lidar.start_motor()
            lidar_information()
            print("[+] LiDAR device started successfully.")
        else:
            print(traceback.print_exc())
    try:
        print("[~] Creating LiDAR plot...")
        print("[!] Press Ctrl+C in console window in order to exit the program")
        for scan in lidar.iter_scans(max_buf_meas=10000):  # Set max buffer size for data and keep scanning
            for (_, angle, distance) in scan:
                if 70 <= floor(angle) <= 110:  # Set scan angle
                    scan_data[min([359, floor(angle)])] = distance

            process_data(scan_data)  # Push data into function
    except KeyboardInterrupt:  # If 'ctrl+c' in console then disconnect LiDAR device to prevent descriptor error on next run
        print("[!] Ctrl+C detected: Exiting...")
        lidar.stop()
        lidar.disconnect()
        print("[+] LiDAR device correctly disconnected")
        sys.exit()
