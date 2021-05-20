from matplotlib import pyplot as plt
import pickle
import traceback
import sys
from math import floor
import warnings


def on_close(arg):
    global plot_update

    try:
        print("[~] Closing plot...")
        plt.close('all')
        print("[+] Plot has been closed.")
        print("[~] Exiting loop...")
        plot_update = False
        print("[~] Exiting program...")
        sys.exit()
    except Exception:
        pass


def update_plot():
    global printed_warn_right_top, printed_warn_left_top, printed_warn_right_bottom, printed_warn_left_bottom

    while plot_update:
        try:
            plt.rcParams['toolbar'] = 'None'
            plt.rcParams["figure.figsize"] = (10, 9)
            plt.title('LiDAR - skan na żywo')
            plt.gcf().canvas.set_window_title('Skan laseru LiDAR')

            x = pickle.load(open('x_live.pkl', 'rb'))
            distance = pickle.load(open('distance_live.pkl', 'rb'))
            movement = pickle.load(open('movement_live.pkl', 'rb'))

            plt.xlabel("X")
            plt.ylabel("Y")

            plt.xlim(-200, 200)
            # plt.ylim(-7, 130)

            plt.gcf().canvas.mpl_connect('close_event', on_close)

            # plt.gca().invert_xaxis()

            left_bottom_value = distance[0]
            right_bottom_value = distance[movement.index(1) - 1]
            left_top_value = distance[movement.index(movement[-1])]
            right_top_value = distance[-1]

            plt.scatter(x, movement, s=0.5, c=distance, cmap='coolwarm_r', vmin=min_color_value,
                        vmax=max_color_value)

            if floor(left_bottom_value) == color_avg or floor(left_bottom_value) == color_avg + 1 or floor(
                    left_bottom_value) == color_avg - 1:
                plt.annotate(round(left_bottom_value, 2), (x[0] + 43, movement[0] - 5))
                printed_warn_left_bottom = False
            else:
                plt.annotate(round(left_bottom_value, 2), (x[0] + 43, movement[0] - 5), color='red')
                if not printed_warn_left_bottom:

                    if floor(left_bottom_value) > color_avg:
                        print("Zbyt nisko w lewym dolnym rogu:", round(left_bottom_value, 2), ". Prawidłowa wartość:",
                              floor(color_avg))

                    else:
                        print("Zbyt wysoko w lewym dolnym rogu:", round(left_bottom_value, 2), ". Prawidłowa wartość:",
                              floor(color_avg))
                    printed_warn_left_bottom = True

            if floor(right_bottom_value) == color_avg or floor(right_bottom_value) == color_avg + 1 or floor(
                    right_bottom_value) == color_avg - 1:
                plt.annotate(round(right_bottom_value, 2),
                             (x[movement.index(1) - 1] - 8, movement[movement.index(1) - 1] - 5))
                printed_warn_right_bottom = False
            else:
                plt.annotate(round(right_bottom_value, 2),
                             (x[movement.index(1) - 1] - 8, movement[movement.index(1) - 1] - 5), color='red')
                if not printed_warn_right_bottom:

                    if floor(right_bottom_value) > color_avg:
                        print("Zbyt nisko w prawym dolnym rogu:", round(right_bottom_value, 2), "Prawidłowa wartość:",
                              floor(color_avg))
                    else:
                        print("Zbyt wysoko w prawym dolnym rogu:", round(right_bottom_value, 2), "Prawidłowa wartość:",
                              floor(color_avg))
                    printed_warn_right_bottom = True

            if floor(left_top_value) == color_avg or floor(left_top_value) == color_avg + 1 or floor(
                    left_top_value) == color_avg - 1:
                plt.annotate(round(left_top_value, 2), (x[movement.index(movement[-1])] + 43, movement[-1] + 1))
                printed_warn_left_top = False
            else:
                plt.annotate(round(left_top_value, 2), (x[movement.index(movement[-1])] + 43, movement[-1] + 1),
                             color='red')
                if not printed_warn_left_top:

                    if floor(left_top_value) > color_avg:
                        print("Zbyt nisko w lewym górnym rogu:", round(left_top_value, 2), "Prawidłowa wartość:",
                              floor(color_avg))
                    else:
                        print("Zbyt wysoko w lewym górnym rogu:", round(left_top_value, 2), "Prawidłowa wartość:",
                              floor(color_avg))
                    printed_warn_left_top = True

            if floor(right_top_value) == color_avg or floor(right_top_value) == color_avg + 1 or floor(
                    right_top_value) == color_avg - 1:
                plt.annotate(round(right_top_value, 2), (x[-1] - 5, movement[-1] + 1))
                printed_warn_right_top = False
            else:
                plt.annotate(round(right_top_value, 2), (x[-1] - 5, movement[-1] + 1), color="red")
                if not printed_warn_right_top:

                    if floor(right_top_value) > color_avg:
                        print("Zbyt nisko w prawym górnym rogu:", round(right_top_value, 2), "Prawidłowa wartość:",
                              floor(color_avg))
                    else:
                        print("Zbyt wysoko w prawym górnym rogu:", round(right_top_value, 2), "Prawidłowa wartość:",
                              floor(color_avg))
                    printed_warn_right_top = True

            plt.pause(0.01)

            plt.clf()

        except Exception:
            print("\n[-] Error has occured:\n")
            traceback.print_exc()
            continue

        except KeyboardInterrupt:
            i = 0
            on_close(i)


if __name__ == "__main__":

    warnings.filterwarnings("ignore")

    min_color_value = 350
    max_color_value = 362
    color_avg = (min_color_value + max_color_value) / 2

    plot_update = True

    printed_warn_right_bottom = False
    printed_warn_left_bottom = False
    printed_warn_left_top = False
    printed_warn_right_top = False


    print("[~] Creating plot...")

    update_plot()
