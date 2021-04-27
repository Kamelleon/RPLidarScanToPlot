from matplotlib import pyplot as plt
import pickle
import traceback

while True:
    try:
        y = pickle.load(open('y_pickled.pkl', 'rb'))
        x = pickle.load(open('x_pickled.pkl', 'rb'))
        # movement = pickle.load(open('movement_pickled.pkl', 'rb'))
        movement_f = pickle.load(open('movement_f.pkl', 'rb'))

        plt.title('LiDAR - scan')

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.xlim(-200, 200)
        plt.ylim(-200,400000)

        plt.gca().invert_xaxis()

        plt.scatter(x, movement_f, s=0.2, c=y, cmap='coolwarm_r', vmin=195, vmax=215, marker='s')  # Show plot

        plt.pause(0.01)
        plt.clf()

    except Exception:
        traceback.print_exc()
        continue